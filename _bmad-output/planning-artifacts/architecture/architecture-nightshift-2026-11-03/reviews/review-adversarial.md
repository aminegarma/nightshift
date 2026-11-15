# Adversarial review: ARCHITECTURE-SPINE.md (pairwise compatibility and security invariants)

Reviewed 2026-11-11. Read-only review of `ARCHITECTURE-SPINE.md` (updated 2026-11-11, AD-1..AD-66, conventions, stack, seed, deferred).

Method: for each finding, two units one level down are built by two teams. Both obey every AD and convention to the letter, but the results do not fit together, or the result still lets a compromised portal, relay, Fleet, agent, gateway or cluster break an AD's Prevents line. Each finding names the units, the compliant-but-incompatible build, the gap in the spine, and the fix (a new or tightened AD or convention).

Severity: **critical** means that core trust or safety fails, or the two builds cannot work together on the main path. **High** means that a Prevents line can be broken by a compliant build, or that two owners or two vocabularies will clash on a path many units use. **Medium** means a real clash or weakening with a narrower blast radius. **Low** means hardening or a clarification.

Counts: **critical 3 · high 14 · medium 17 · low 5**.

---

## Critical

### C-1. Receipts have no trust anchor the person can rely on (relay / portal vs executor)

- **Units:** decision relay plus portal (receipt display) vs executor (receipt signer).
- **Compliant build:** The executor signs receipts with "the cluster receipt key" (AD-23, AD-40). The portal team needs the matching public key. Nothing says where it comes from, so they fetch it from Fleet's cluster registry, the same place the relay lives. A compromised relay or Fleet registers its own key for the cluster, withholds a customer's stop, and returns a forged receipt that says "applied". The person sees the stop as effective. A compromised portal can skip verification altogether and show "applied". Both builds meet AD-23 as written ("the relay never signs receipts": it does not, it signs with a key it substituted).
- **Gap:** AD-23's Prevents line ("people believing a decision took effect when the cluster has not applied it") needs a receipt key that Fleet and the portal cannot substitute, and a verifier that the portal cannot fake. AD-40 says how audit-service keys are registered but says nothing about receipt-key registration or pinning. The convention for receipts has no key ID.
- **Fix:** New convention plus a tightened AD-23. (1) The cluster generates its receipt key at installation. Its fingerprint goes into the customer-admin-signed roster (or a customer-signed cluster record) and is shown on the in-cluster dashboard. Fleet only stores a copy and is never the source of trust. (2) A receipt carries `receipt_key_id`. (3) State the limit: when the portal is compromised, the portal's "applied" display proves nothing. For stops, the authoritative confirmation is either the cluster-originated post-decision SMS notice (extend AD-18's notice to stops, withdrawals and alert-only) or the dashboard. (4) Fleet changing a registered receipt key is an alerted, customer-visible event.

### C-2. No unit owns which release Flux applies, so AD-46 and AD-53 have no enforcer (Flux / rollout controller vs executor / rollback guard)

- **Units:** Flux configuration plus the Fleet rollout controller vs the executor (AD-53 policy check) and the rollback guard (AD-45).
- **Compliant build:** The Flux team configures `OCIRepository` to follow a semver range or tag, with cosign verification required. That satisfies "pinned by digest with signature verification required" (AD-43), because Flux resolves a digest and verifies it. The rollout controller moves the tag for each wave. The executor team implements AD-53 by checking release metadata when a new release appears. By then Flux has already applied it, so "refused with a receipt" is after the fact. A compromised Fleet, using only release-key-signed artefacts and no key compromise, can:
  - move the tag back to an older signed release with a known flaw. Flux checks signatures, not monotonic versions, which breaks AD-46.
  - push a signed release outside the customer's window or update type, which breaks AD-53.

  The rollback guard also writes the same Flux objects ("suspend Nightshift Flux object, restore known-good release"), and so does the separate install path (AD-43). That gives three writers of one entity.
- **Gap:** AD-15 has no row for the Flux source reference or the desired-release pointer. AD-46 names no enforcing unit. AD-53 says "before applying", but in the topology the executor does not apply releases: Flux does.
- **Fix:** New AD "In-cluster release gate":
  - A single named in-cluster writer (the executor, or a dedicated release gate with its own identity) is the sole writer of the digest pin in the Flux source object.
  - It sets the pin only after it verifies four things: the signed release metadata (strictly increasing release sequence number, expiry, update type, allowed rollback targets), the customer-signed maintenance policy, the window measured by the cluster clock, and AD-46.
  - Flux never follows tags or semver ranges.
  - The rollback guard may only (a) suspend reconciliation and (b) set the pin to the `allowed_rollback_target` named in the current release's signed metadata.
  - The install path is the only other writer, and it runs out of band.
  - Add a row to AD-15.

### C-3. The challenge cannot be computed the same way on both sides, and D never reaches the browser (portal vs executor; also gateway)

- **Units:** portal (browser code that calls `navigator.credentials.get` with challenge = SHA-256(tag ‖ canonical(D))) vs executor (rebuilds D and recomputes the challenge).
- **Compliant build:** The portal team uses JSON Canonicalization Scheme (RFC 8785), RFC 3339 times and role strings exactly as written ("delegated Orvex support"). The executor team uses deterministic CBOR, Unix seconds and snake_case enums. Every assertion fails verification. The Consistency Conventions say "canonical encoding chosen with the stack", and the Deferred list says "no unit depends on them beyond the conventions". That is false: two independently built units depend on byte-identical encoding.
- Separately, the option B sequence diagram never sends D from the executor back to the portal (step 4 builds D; step 8 has the person sign "over D"). The gateway team, following AD-26, has no allowlisted "decision statement" outbound message type, so it refuses to send D. D carries `target` and `evidence_digest`, and the target is an untrusted identifier.
- Other signed objects (roster changes, ticks, consents, delegations, policy acceptance, local dashboard stops, group decisions) have no challenge format or domain tag. If two of them share an encoding, an assertion over one could be accepted as the other.
- **Gap:** Byte-level encoding, field types, enum spellings, the D return path and per-object-type domain separation are all undefined.
- **Fix:** Tighten the conventions now, not "with the stack":
  - Fix one canonical encoding (for example RFC 8785 JCS), with exact field names, types (UTC integer seconds), enum tokens, and target encoded as `{kind, uid}` (UID only, no name).
  - Give one domain tag per signed-object type: `nightshift-decision-v1`, `nightshift-group-decision-v1`, `nightshift-roster-v1`, `nightshift-setting-v1`, `nightshift-local-stop-v1`, and so on.
  - Add an explicit "pending decision statement" outbound message type to the AD-26 allowlist, assembled by the gateway from D's typed fields.
  - Add the D-return step to the sequence diagram.
  - Publish shared test vectors that both teams must pass.

---

## High

### H-1. A stop can be lost between relay, gateway and executor (relay vs gateway vs executor)

- **Compliant build:** The gateway team treats relay fetches like the outbox. It acknowledges each decision to the relay as soon as it fetches it, then hands it to the executor through an in-memory call (push or pull between gateway and executor is still deferred). The gateway crashes before handing over a withdrawal. The relay has marked it delivered, so it never redelivers. The executor restarts and runs AD-7 step (1), "receive and apply pending stop decisions", but there are none to receive. The approval it already holds runs. AD-28's outbox is outbound only. AD-2 forbids a private persistent store for repair state, so the gateway team is right not to persist inbound decisions.
- **Gap:** There are no acknowledgement semantics for inbound decisions and no durable inbound owner. "A stop that reached the cluster" (AD-22) does not say whether that means the gateway or the executor.
- **Fix:** New convention. The relay keeps a decision pending until it holds a cluster receipt for that `decision_id`, and it redelivers until then. Fetching is not acknowledgement. The executor records the received stop (RepairRun status, or the cluster-state object in H-9) before it emits the receipt. Define "reached the cluster" as "recorded by the executor".

### H-2. The decision and role vocabularies are incomplete, so each team invents its own (portal / dashboard / management agent vs executor)

- **Compliant build:** D's `decision` takes approve, reject, withdraw or undo-reject. `role` takes customer approver, delegated Orvex support, Orvex technical approver or manual-repair performer. The spine also requires signed person actions that fit neither list:
  - "Start now" and "I've done it" (AD-21)
  - claim release (AD-9)
  - clearing a halt (AD-58)
  - alert-only on and off, and untick (AD-22, AD-51)
  - Orvex advance permission for last resort (AD-55)
  - local stops by a "customer administrator", a role absent from the list

  The dashboard team encodes the alert-only switch as `withdraw` on a synthetic request. The portal team adds `start_now` with role `performer`. The executor team rejects anything outside the listed enums, so "Start now" and halt clearing never work, or the executor accepts free-form values and the wrong action is matched to the wrong authority.
- Nonces are unclear as well. Does a withdraw need its own freshly issued `cluster_nonce`, adding a round trip through a polled gateway, or does it reuse the approval's nonce? Can an undo-reject get a nonce for a request version that is already closed (AD-22 closes it; AD-25 undoes it)? Two compliant executors answer differently.
- **Fix:** Close the enums in the conventions: every decision kind, every role (including customer admin), and for each kind the required role, the scope it affects and whether it needs a fresh nonce. Proposed rule: stops reuse the version's issued nonce with a new `decision_id`; undo-reject has its own nonce issued against the closed version only inside the undo window.

### H-3. Dashboard passkeys cannot pass AD-17, or they pass too broadly (dashboard vs executor)

- **Compliant build:** AD-17 requires "portal origin and RP ID". The executor team implements exactly that, so every locally signed dashboard stop (AD-51, RP ID equal to the cluster hostname) fails verification. Local stops then do not exist, which breaks AD-51's Prevents line. Another executor team relaxes the rule to "any RP ID listed in the roster for that credential". If the roster entry does not bind the allowed decision kinds to each RP ID, a local credential can sign approvals, which contradicts "the dashboard gives no approvals".
- **Fix:** Tighten AD-17. Each roster credential entry binds `(credential_id, rp_id, allowed_origin, allowed_decision_kinds)`. Portal credentials may sign everything the role allows. Local credentials may sign only the stop-type kinds (and settings, if that deferred question is decided). The executor checks origin and RP ID against that credential's entry, not a global one.

### H-4. Group decisions cannot satisfy AD-17 and AD-18 as written (Fleet console / relay vs executor)

- **Compliant build:** AD-48 says a group decision goes "via AD-18". AD-17 requires a nonce "issued by this cluster for this request version", D built by the cluster, and an SMS code sent by the cluster. One signature over a Merkle root cannot carry a different cluster nonce for each of N clusters, and no single cluster sends the code. An executor team applying AD-17 to the letter rejects every group decision. The Fleet team builds group decisions without nonces. The Merkle tree is also unspecified: leaf encoding, hash function, ordering, leaf and node domain separation, and what a leaf binds (cluster_id only, or cluster_id plus target UID plus the cluster's request version). Without leaf and node separation, an internal node can be presented as a membership proof. Without request versions in the leaves, a group approval can be replayed against later occurrences.
- **Fix:** Add a group-decision AD that states its replay protection. Each leaf carries `{cluster_id, target uid, request_id, request_version, cluster_nonce}`, with nonces collected from each cluster before signing. Clusters that have not supplied a nonce are not in the set. Or state an explicit alternative: `decision_id` stored as used per cluster, plus validity. Use RFC 6962-style hashing (0x00 for a leaf, 0x01 for a node), sorted leaves and the `nightshift-group-decision-v1` tag. Say which party sends the code for a group (proposed: none; a group needs the passkey plus a Fleet-independent confirmation, or it is passkey-only under an Orvex-signed policy and recorded as such).

### H-5. The untrusted agent owns occurrence identity, so a rejection can be bypassed (agent vs executor)

- **Compliant build:** The agent is the sole creator of the RepairRun spec (AD-15). It assigns `request_id` and, implicitly, the occurrence. After a customer rejects entry A on pod P, a compromised or buggy agent creates a new RepairRun with a new occurrence for entry B, which is safe and ticked, on the same target. The executor has no rule that relates the two, B needs no approval, and it runs. AD-22 ("a rejection also blocks substitute entries for the same occurrence") and AD-55 ("never runs after a rejection") are broken.
- The same gap produces clashing builds for request versions. The agent team creates a new RepairRun when evidence changes. The executor team increments `request_version` in status. The result is two live requests for one problem, and the "material evidence change" (AD-25) judged by two units by different rules. `evidence_digest` is not defined either: a digest of the agent's evidence, or of the executor's re-run queries, which change every scrape so "D matches field by field" never holds.
- **Fix:** New AD. The executor derives the occurrence key itself (target UID plus failure class from the catalogue, within a cluster-timed window) and keeps the rejection state per key. Request versions are issued only by the executor in status; the agent never sets them. Define `evidence_digest` as a digest of the executor's own snapshot of the entry's fixed-query results, stored when D is built. "Material change" is a per-entry rule in the signed catalogue.

### H-6. No anti-rollback for signed long-lived objects, and withdrawing consent is not stop-class (Fleet / relay vs executor / gateway)

- **Compliant build:** Rosters, policies, consents, ticks, delegations, the platform map, the catalogue and switch-offs all carry `valid_until` (AD-24) and a signature. No AD requires a strictly increasing version. A compromised relay or Fleet serves the previous customer roster, signed by an admin and still inside `valid_until`, that still lists a removed approver. That re-adds an approver, which AD-19 is meant to prevent. Fleet can serve the previous catalogue to re-enable an entry that was switched off (AD-57 forbids only re-enabling "by validity tier"). If a customer withdraws external-AI consent through the portal, a compromised relay simply withholds the new object, and the gateway keeps sending to Bedrock. AD-23's "withheld is detected" covers stops and receipts only. Consent is not a stop.
- **Fix:** New convention. Every signed long-lived object carries a strictly increasing `seq` per object stream. Verifiers keep the highest `seq` seen and refuse lower values. Withdrawals of consent, channel permission and delegation are stop-class: they have priority, they return a receipt, and the dashboard can issue them locally. Missing receipts are surfaced as for stops.

### H-7. The audit chain cannot record what the spine requires, and any appender can forge or flood (gateway / rollback guard / checker vs audit service; agent vs audit service)

- **Compliant build:** AD-15 lists only the agent, executor and dashboard as appenders. The gateway must record every outbound message (AD-26, PRIV-7). The rollback guard's rollback "is recorded" (AD-45). The halt and its clearing are recorded (AD-58). The gateway team builds its own outbound log, which is a second owner of the record. The guard team writes Kubernetes events. Neither is in the hash chain. In the other direction, the audit service team exposes "append" without stamping the authenticated caller on each record or limiting record types per caller. A compromised agent then appends records that look like the executor's ("stop applied", "verification passed") into customer-visible history, or fills the volume until AD-50's "storage full" suspends all repairs.
- **Fix:** Tighten AD-15 and AD-16. Give an explicit list of appenders with allowed record types per identity (add gateway, rollback guard, checker and management agent). The audit service stamps the verified workload identity on every record. Each identity has a quota, with reserved capacity for the executor's stop and receipt records that other appenders cannot use.

### H-8. RepairRun as a CRD lets the agent write executor state and exhaust etcd (agent vs executor; agent vs customer workloads)

- **Compliant build:** AD-2 and AD-5 give the agent "create RepairRun only". If the CRD does not enable the `/status` subresource (the spine does not require it), the agent's create can include a status block: a recorded intent, an epoch, an "attempt n done", or a D with a nonce the agent chose. The executor treats status as its own, so the agent is effectively a second writer. A create-only agent can also create RepairRuns without limit until etcd reaches its quota (2 GiB, which AD-2 cites). That stops all API writes, customer workloads included, which breaks AD-64. No unit is named to delete finished RepairRuns, and the executor has no delete right listed, so normal use grows without bound too.
- **Fix:** Add to AD-2: the status subresource is mandatory, and the executor treats any status present at creation as untrusted and empty. A validating policy restricts creates to the agent identity and checks spec fields. A ResourceQuota on the count of RepairRun objects plus an executor-side rate limit apply. The executor owns RepairRun garbage collection after closure plus retention (it gets the delete right). Used `decision_id` values must survive that deletion (see H-9).

### H-9. Cluster-wide authorisation state has no declared home (executor vs dashboard vs checker vs gateway)

- **Compliant build:** Several pieces of state are cluster-wide or outlive one RepairRun:
  - the cluster halt (AD-58)
  - the alert-only switch and current mode
  - the executor epoch (AD-7)
  - used `decision_id` values and issued nonces (AD-22)
  - applied revocations
  - the pinned first-admin credential (AD-19)
  - cached rosters and settings with their highest `seq`

  AD-2 allows two CRDs and no private stores for repair state. Team A puts the halt and the epoch in the claims ledger. Team B uses a ConfigMap (arguably a private store), or a Lease for the epoch. The dashboard reads one location and the checker (which reports the halt in the heartbeat) reads another. Used `decision_id` values kept in RepairRun status disappear when the RepairRun is garbage-collected (H-8). That opens replay of any decision whose nonce can still be resolved.
- **Fix:** Tighten AD-2. Either (a) the claims ledger is renamed and widened to a per-cluster "cluster state" object with named sections (claims, halt, mode, alert-only, epoch, used decision_ids with retention at least the maximum validity, highest seq per signed stream, pinned anchors), or (b) a declared third object. Either way, list every reader of that object in AD-15.

### H-10. The heartbeat cannot carry what the rollout needs, and the identity namespaces differ (checker vs rollout controller / correlation / watchdog)

- **Compliant build:** AD-27 fixes the heartbeat to agent ID, timestamp and status, behind a strict validator. AD-44 needs each cluster's current release, and its probation and rollback state, to compare updated clusters with clusters not yet updated. AD-58 needs the halt "in the heartbeat status". AD-50 needs "degraded". The checker team emits `status: ok|fail`. The rollout team reads the release from report intake (the gateway path). A cluster whose guard rolled it back looks "healthy on release N+1", so the bad wave continues. The watchdog keys clusters by "agent ID". D and the relay key them by `cluster_id`. With no defined mapping, the rollout controller cannot join the two.
- **Fix:** Define the heartbeat `status` as a closed, typed structure inside the FR-6 field: a health enum, `release_digest`, a probation state enum (none, in probation, passed, failed and rolled back, held back), a halt flag and a degraded-reason enum. That keeps it fixed-schema and free of data. Queue it with AP-1 if the PRD requires that. Use one cluster identity (`cluster_id`, bound at installation to the cluster's keys) everywhere, and drop "agent ID".

### H-11. The platform-only map's signing key is unspecified, so any Fleet key can downgrade production impact (Fleet / policy authoring vs executor)

- **Compliant build:** AD-15 lists the map as "Orvex-signed (key not specified)". The executor team accepts the management-policy key, which per AD-40 a single "policy authoring" requester can obtain, and two-reviewer gating is only "proposed" in AD-56. A compromised or careless policy author marks a customer's namespace as platform-only. Under AD-12 the executor then treats repairs there as not affecting customer production and skips customer approval, which is exactly what AD-12 is meant to prevent.
- **Fix:** Name a dedicated map key in AD-40, gated by two Orvex reviewers. Make the customer see changes to the map entries that cover their clusters (signed acceptance, or at least notice before the change takes effect). The executor accepts the map only under that key and that `seq` (H-6).

### H-12. Metric evidence can be forged by workloads through a shared Prometheus (Prometheus configuration vs executor / AD-65)

- **Compliant build:** AD-29 reuses "suitable existing Quornex monitoring". That monitoring scrapes customer ServiceMonitors, possibly with `honor_labels` or a remote-write receiver. A customer or compromised workload exports series labelled `job="node-exporter", instance=<node>` and `vantage="bmc"`. The executor re-runs the entry's fixed queries "at the source" (AD-12) and sees two independent signals (AD-65, where "vantage point" is just a label). A ticked safe repair, such as cordon and drain, then runs on attacker evidence. The OMK and EKS adapter teams also label vantage differently ("node" vs "node-agent", both on the same host), so an independence count that is correct on one platform is wrong on the other.
- **Fix:** New convention. Evidence used by the executor comes only from scrape jobs Nightshift owns, with `honor_labels: false`, and no remote-write or push sources. Vantage point is a closed enum assigned by the scrape configuration, never by the exporter, and the independence pairs are listed per platform in the catalogue. If Quornex monitoring is reused, only the jobs Nightshift owns count as evidence.

### H-13. OMK fencing trusts a BMC-to-node mapping that has not been verified (BMC reader vs executor)

- **Compliant build:** AD-62 fences stateful pods on OMK using "BMC power state". The BMC reader team reports power state for the BMC addresses in its list. The binding check between each BMC and its node is deferred together with the hardware-action component. A wrong mapping (miscabled, or a reused address) reports node X as powered off while it is running. The executor force-deletes its stateful pods, the workload runs twice, and AD-62 is broken.
- **Fix:** Move the binding check out of Deferred and into AD-62 or AD-31. The installation verifies the binding (for example, the system serial or UUID from Redfish against the node's SMBIOS `system-uuid` in Node status). The BMC reader reports power state keyed by the verified node UID and rechecks the binding every time. With no verified binding, the reading is unknown and fencing escalates.

### H-14. First-admin enrolment and reinstalls let Orvex become the trust root (installer / Fleet vs executor)

- **Compliant build:** AD-19 sends the first-admin code "to the contract contact", and the cluster pins that credential. The contract contact record lives in Orvex systems. Nothing says where the pin is stored or whether it survives a reinstall. An installer acting in bad faith deletes the Nightshift namespaces. That is within the install path, and the pin lived in a namespaced object. On reinstall the cluster has no pin, enrols again, and the code goes to a contact that Orvex controls. AD-19's Prevents line ("Orvex silently adding approvers") is broken.
- **Fix:** Tighten AD-19. The pinned anchor and the current roster `seq` are registered somewhere Orvex cannot rewrite on its own (for example, the customer keeps the pin fingerprint, and the Fleet copy is append-only and visible to the customer). A reinstall of an existing `cluster_id` needs the existing customer admins, or goes through the delayed and visible recovery path. Every first enrolment is notified through a second out-of-band contact the customer chose.

---

## Medium

| # | Units | Compliant-but-incompatible build | Gap | Fix |
| --- | --- | --- | --- | --- |
| M-1 | Executor vs gateway (SMS) | The sequence diagram has the executor write "SMS naming the action with code". AD-26 has the gateway assemble every outbound message. The two teams each render the text, and the SMS no longer matches the portal's rendering. The gateway also records every outbound message where the customer can see it (PRIV-7), so the one-time code ends up in dashboard and portal history | Owner of the SMS template; treatment of secrets in the PRIV-7 record | The gateway renders from a signed template using D's fields. The executor passes only `decision_id` and the code. The outbound record stores a placeholder for the code |
| M-2 | Executor vs portal / relay (receipts) | The receipt convention lacks `cluster_id`, the assurance level (which AD-18 requires "in decision, receipt and history"), a D digest and a key ID. Its `effect` enum lacks: superseded by stop, refused (out of policy, AD-53), unverifiable and recorded, late undo, and pending code. The portal maps a receipt with a missing field to "applied" | Incomplete receipt shape and vocabulary | Add the fields `cluster_id`, `d_digest`, `assurance`, `receipt_key_id` and `reason_code`, and close the `effect` enum |
| M-3 | Executor vs checker vs Fleet (time) | "The cluster's clock" is not defined. The executor uses its node clock and the checker measures skew against the API server's `Date` header, so "unsynchronised" has two meanings. `valid_until` is fixed in D when it is built, yet AD-25 says validity "starts at approval", so the time the code took eats into validity in one build and not in the other. The age of the status statement is measured from the relay's `issued_at` in one build and from receipt in another. Maintenance windows have no time zone or DST rule, so the rollout controller and the cluster gate disagree about the window | Time source and time semantics | Name the reference (NTP-synchronised node clock checked by chrony or timex, with the maximum skew in the conventions). D carries `valid_for_seconds`, and the executor sets `valid_until` from when it accepts the assertion. Statement age is measured from the cluster's receipt time, bounded by `issued_at` plus skew. Windows are stored in UTC with an IANA zone, and the cluster is authoritative |
| M-4 | Relay vs executor (AD-24 status statement) | The content of the status statement is undefined. The relay signs "cluster X reachable at T". The executor treats that as fresh for every long-lived object, including a roster version that has since been superseded | Statement is not bound to object versions | The statement lists the current `seq` and digest for each long-lived stream for that cluster, plus the highest revocation `seq` |
| M-5 | Dashboard vs executor (expired tier) | AD-24 says local stops keep working against the cached roster. "Every signed authorisation object carries `valid_until`", so a strict verifier refuses the expired roster and local stops fail after more than 24 hours offline | Stop verification is not exempt from expiry | Rule: stops verify against the newest roster held, whatever its expiry. Approvals need an unexpired roster |
| M-6 | Gateway vs executor (roster and settings caches) | Each unit verifies customer signatures (AD-54) against its own cached roster and settings, fetched separately. They diverge: the gateway sends AI traffic under consent the executor already sees as revoked | Two copies of one entity | One in-cluster store of signed objects (H-9). Both units check the same `seq` |
| M-7 | Executor vs roster builders (distinct people) | The customer and Orvex rosters each assign person IDs. The executor counts distinct `person_id` strings. Two different people with ID "p1" in different rosters count as one, and the same human enrolled in both rosters counts as two | Identity namespace | People are counted by `(roster, person_id)`. Forbid one human holding credentials in both rosters, or add an explicit cross-roster link |
| M-8 | Agent / executor vs gateway / Fleet intake (message IDs) | The gateway assigns a UUID when a message enters the outbox. The agent retries after the gateway crashes and the same fact gets two IDs. Fleet correlation counts the problem twice, crosses its rate threshold and stops the rollout | Idempotency key is minted at the wrong end | The producer assigns the message ID (producer identity plus a producer sequence or content hash) |
| M-9 | Gateway (OMK / EKS) vs Fleet correlation | The "allowed-field fingerprint" is computed in the cluster by one team's algorithm and recomputed in Fleet by another's, so the same problem is split into two groups, which AD-47 is meant to prevent. One compromised cluster floods reports and triggers a fleet-wide urgent alert or stops the rollout | Undefined fingerprint; no per-cluster weighting | Define the fingerprint once (fields, order, hash) in the conventions. Count distinct clusters, not reports, and cap each cluster's contribution |
| M-10 | OMK BMC reader vs EKS poller vs agent (signal values) | Freshness is taken from the BMC's own clock by one team and from the scrape time by another. "Unknown" is shown by an absent series in one build and a NaN or 0 in another. A PromQL query over an absent series returns nothing, and the agent's rule reads that as "no problem" | Encoding of coverage and freshness | Every source exports `nightshift_signal_coverage{family,source,state}`. Freshness comes from the scrape timestamp only. Fixed queries must use `absent()` guards that map to unknown |
| M-11 | Executor vs gateway (Bedrock mode check) | AD-35 says "the executor checks the account mode and the model's allowed modes". The executor has no AWS path, and AD-32 forbids other components from obtaining AWS credentials. The gateway team does not check, because it was not told to | Wrong owner | Assign the check to the gateway (or credential vending) before every session. The executor plays no part |
| M-12 | Rollback guard vs checker vs Flux | What counts as a "failed probation check" is not defined (release-declared checks, or generic liveness). Nobody is named to resume Flux after the guard suspends it, so a cluster stays held back indefinitely, and a compromised guard can do this silently (AD-46 detects only expired metadata) | Probation contract; resume owner | Each release's signed metadata declares its probation checks and window. Suspension appears in the heartbeat probation state (H-10). Only the release gate (C-2) or the install path resumes |
| M-13 | Fleet vs executor (AD-57 switch-off) | No key in AD-40 is assigned to switch-off statements. The Fleet team signs them with the relay key ("status statement"), and the executor team accepts only the catalogue key. Re-enabling an entry has no defined path | Key and lifecycle | Add a switch-off key (or catalogue key with one reviewer for disabling only). Re-enabling needs a catalogue version with a higher `seq` (H-6) |
| M-14 | Agent vs gateway (fact builder) | The gateway checks field types only. A compromised agent encodes log bytes into numbers, durations and "placeholders", a covert channel that leaks raw logs. Kubernetes names in notification fields can carry customer-sensitive strings | Typed is not the same as safe | Codes and IDs are closed enums or catalogue IDs. Numbers are bounded and quantised per field. Rate and size caps per channel. Names leave only where the channel's allowlist permits it, otherwise as UID or hash |
| M-15 | Gateway vs executor vs portal (latency) | Push or pull between gateway and executor is deferred, and the relay poll interval is not set. With a 60-second poll, the option B round trips (start, then the code, then the assertion) and the 2-minute undo-reject window cannot both fit | Unstated latency budget | Set the relay fetch as long polling, with an end-to-end budget per flow in the conventions. Time the undo window from receipt at the cluster to the cluster's issue of the undo nonce |
| M-16 | Executor vs dashboard / agent / checker (RepairRun phases) | No phase or status enum. The dashboard, the agent's de-duplication and the checker's reports each assume different phase names and transitions (ambiguous waiting for a person, blocked by a missing check, waiting for the management agent, halted) | Unspecified status vocabulary | Add a closed phase enum and transition table to the conventions |
| M-17 | Management agent vs workload executors (multi-cluster claims) | AD-11 makes multi-cluster repairs wait for the management agent. Only executors write ledgers. The management-agent team builds a cross-cluster lock of its own, which is a second owner of the claim, while executors wait for a signal nobody has defined. One ledger object per cluster with nested scopes at about 10,000 pods also approaches the 1.5 MiB request limit | Claim ownership across clusters; ledger size | The management agent only proposes. Each executor claims locally and reports back. Shard the ledger, or cap claims per object |

## Low

| # | Units | Issue | Fix |
| --- | --- | --- | --- |
| L-1 | EKS node vs executor (AD-13) | The node management mode is read from Node labels. A compromised kubelet can set labels that NodeRestriction does not restrict (for example, faking "self-managed, auto-repair off") | Take the mode from the AWS poller or the signed map only, never from labels the node can write |
| L-2 | Audit service vs Fleet checkpoint store | A reinstall or reset registers a new audit key and the chain starts again at seq 0 with no visible break | Key changes are an alerted event. The new chain's first record cites the last checkpoint of the previous key |
| L-3 | Portal vs executor / gateway | "Start confirmation" is unauthenticated to the cluster (portal-verified only). A compromised portal can trigger repeated SMS codes (bombing, cost, approval fatigue) | Per-request and per-person rate limits on code issuance, enforced in the cluster |
| L-4 | Relay vs gateways | Per-cluster authorisation on relay fetches is implied ("customer isolation") but not stated. A cluster that fetches another cluster's pending D leaks target UIDs across customers | The relay serves only `cluster_id` values bound to the authenticated cluster identity, and this is tested |
| L-5 | Compromised cluster vs rollout controller | One customer-controlled cluster can report a healthy status falsely and push wave progression forward | Progression needs a minimum count of independent healthy clusters per platform, and no single cluster can unblock a wave |

---

## Pattern

Most holes come from four things the spine left as "fixed at build" or "not specified", which turn out to cross unit boundaries:

1. Canonical bytes: encoding, enums, Merkle construction, fingerprints.
2. A home and an owner for cluster-wide state: halt, epoch, used decision_ids, signed-object caches, the Flux pin.
3. Monotonic versions and trust anchors for every signed stream: rosters, consents, catalogue, map, receipt key.
4. Acknowledgement and ownership on the inbound decision path.

Fixing these four in the Consistency Conventions and AD-2, AD-15, AD-17 and AD-24 closes most of the findings above.
