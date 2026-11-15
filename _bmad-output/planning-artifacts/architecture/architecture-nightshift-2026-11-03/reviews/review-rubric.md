# Rubric review: ARCHITECTURE-SPINE.md (Nightshift, updated 2026-11-11)

Reviewer: independent, read-only. Authority for what was decided: `.memlog.md` (same folder). PRD checked by headings and grep only.

Checklist used: the spine fixes the real divergence points for the level below and misses none; every AD's Rule is enforceable and prevents its stated divergence; nothing under Deferred could let two units diverge; named tech is verified-current; PRD capabilities are covered; the operational and environmental envelope is decided, deferred or open; mermaid is valid; no placeholders; decisions not rationale; both platforms covered; ADs are internally consistent.

**Verdict:** The trust, mutation and offline rules are strong and carefully limited. However, one adopted rule contradicts another (group approvals against per-cluster decision verification). Several cross-unit contracts are also still deferred or placed with no unit: where cluster state is stored, how the gateway and executor exchange messages, transport to the management agent, the canonical encoding of D, and how releases are gated. The Fleet and installation parts of the operational envelope are thin. Fix these before epics are cut.

**Counts:** critical 1 · high 9 · medium 10 · low 6

---

## Critical

### C1 · AD-48 contradicts AD-17 / AD-18 (group approvals cannot pass the cluster's own checks)
- **Problem:** AD-17 counts a decision only if D is "rebuilt from its own RepairRun" and the "nonce [is] issued by this cluster for this request version". AD-18 has *the cluster* store D and send the SMS code. AD-48 has one signed group decision covering many clusters, bound to a Merkle root and a wave plan. No single cluster issued its nonce, no cluster's RepairRun matches the group statement, and it is not defined which cluster sends the SMS or checks the code. So the executor team has two choices: refuse every group decision, or loosen AD-17 on its own. Either one is a divergence on the authorisation path. Replay protection for group decisions (no cluster nonce) is also undefined.
- **Fix:** Add a group branch to AD-17 explicitly. For example: the Fleet group console builds a group statement G with a Fleet-issued group_nonce. The SMS code is issued by the decision relay, or the group path is passkey-only under a signed group policy, recorded as such. Each executor accepts G when the Merkle proof binds its own (cluster_id, request_id, request_version, evidence_digest) leaf, decision_id is unused locally, and the rest of the AD-17 list passes. Then add the G field list and leaf encoding to Consistency Conventions. If this is not settled, mark AD-48 "proposed" and list it as an open question that blocks the group-approval epic.

## High

### H1 · AD-2, AD-15: cluster-held state has no location and no owner row
- **Problem:** AD-2 forbids any CRD or private persistent store for repair state beyond RepairRun and the ledger. Yet the rules require durable cluster state with no stated home:
  - used decision_ids and issued cluster_nonces (AD-22)
  - stored D and the keyed SMS-code hash with attempt counter (AD-18)
  - the executor epoch (AD-7)
  - the cluster halt (AD-58)
  - fleet switch-off statements (AD-57)
  - cached rosters, customer-signed settings and consents, maintenance and rollback policies, the management policy and the platform map (AD-24, AD-53, AD-54, AD-56)

  AD-15 has no rows for settings, policies, the halt, switch-offs or the epoch. Executor, gateway (which verifies consent, AD-54), dashboard and checker will each invent storage.
- **Fix:** Extend AD-15 with one row per item: sole writer, signer, readers (the gateway must read the customer roster and settings), and location. For example: per-request items in RepairRun status, the epoch and halt in the ledger, and signed objects as verified files held by the executor and gateway. Then amend AD-2 to say which of these are allowed outside the two CRs.

### H2 · Option B sequence, Conventions, Deferred: D never reaches the portal, and its encoding is deferred anyway
- **Problem:** In the sequence diagram the executor builds D (with cluster_nonce) and the person then makes "a fresh passkey assertion over D" in the portal. But no message carries D or the challenge back to the portal. The portal must therefore either rebuild D, which needs the nonce and the canonical encoding, or receive it, which is a missing step. Deferred says "canonical encoding of D … no unit depends on them beyond the conventions", which is false. The portal or Fleet console (group statements, Merkle leaves) and the executor must produce byte-identical encodings.
- **Fix:** Add steps E→G→R→PO carrying decision_id, D and the challenge bytes. The portal passes the challenge unchanged and never rebuilds it. Decide the canonical encoding now (for example RFC 8785 JCS, or deterministic CBOR per RFC 8949 §4.2) plus the Merkle leaf and hash rules, and remove the encoding from Deferred.

### H3 · Deferred: three cross-unit interfaces are left open
- **Problem:** Each of these deferrals lets two units build against each other in different ways:
  - "push or pull between gateway and executor": the gateway and executor teams.
  - "Transport between workload clusters and the management agent": AD-11 makes multi-cluster repairs wait on the management agent, but there is no protocol for cross-cluster claims or coordination. AD-66 and AD-4 only say what it must not do.
  - "Transport for audit checkpoints before AP-1": AD-16 requires external checkpoints, but no channel exists. The audit service team and the Fleet store team diverge, and the AD-16 rule cannot be enforced.
- **Fix:** Decide each one.
  - Example for gateway and executor: the executor polls an authenticated gateway API, so all inbound decisions flow executor-pull.
  - Example for the management agent: workload gateways push sanitised facts to it; it publishes coordination proposals that workload executors fetch through their gateways; per-cluster claims stay local and multi-cluster claims are two-phase with a timeout that fails closed.
  - Example for checkpoints: they ride the Fleet-reports channel until AP-1, with the stated gap when that channel is unticked.

  Otherwise move each one to an Open Question that names the epic it blocks.

### H4 · AD-53 and AD-46: release and update gating has no enforcing unit
- **Problem:** AD-53 says "before applying any release or platform update, the executor checks it". But Flux applies Nightshift releases (AD-43), and the executor has neither RBAC on Flux objects (AD-5) nor a place in that path. Platform updates (OMK, Quornex, EKS control plane) are applied by tools outside Nightshift entirely. AD-46 (accept only newer releases or signed rollback targets) also names no unit, and Flux does not enforce version order. As written, a compromised Fleet that pushes a signed release outside the customer's policy is not stopped, which is exactly what AD-53 claims to prevent.
- **Fix:** Name one cluster-side "release gate" owned by the executor or rollback guard. It is the only writer of the digest in the Nightshift OCIRepository and Kustomization. It advances the digest only after the policy, window, version-order and metadata-expiry checks, and it gets matching RBAC in AD-5. For platform updates, state the limit: Nightshift can issue or refuse a cluster-signed permit that the Quornex or OMK update tooling must present, or it detects and reports updates outside policy (SM-4). It cannot block them.

### H5 · PRIV-9 makes the outbound flow-to-channel table an architecture output, but it is deferred
- **Problem:** PRIV-9: "The architecture assigns every other outbound flow to one of these channels." The spine defers the whole table ("Needed before build"): registry pulls, relay fetches and receipts, credential vending, Bedrock, SMS, telephony, Slack, the FR-12 signal, checkpoints and the management agent. The gateway's per-channel enforcement (AD-26, AD-54) and behaviour when a channel is off depend on it. In addition:
  - The SMS provider is on the approval path but has no stated choice, no jurisdiction rule, and no credential model (10,000 per-cluster credentials, or relay through Fleet).
  - Phone numbers leave the cluster to that provider.
- **Fix:** Add the table to Conventions now (flow → PRIV-9 channel → allowlist reference → behaviour when off). Add an AD or Deferred row for the SMS provider: how the provider is chosen, the data residency rule, and per-cluster or Fleet-relayed credentials.

### H6 · AD-15 and the AD-4 diagram leave out the gateway and rollback guard as audit appenders
- **Problem:** The audit chain's appenders are "agent, executor and dashboard". The gateway is the only unit that knows exactly what left the cluster (PRIV-7, AD-26 "recorded where the customer can see it"). The rollback guard's recovery "is recorded" (AD-45). The audit service will enforce its append ACL from AD-15, so both would be refused. The diagram has no GW→AU or RG→AU edge.
- **Fix:** Add the gateway (outbound records) and the rollback guard (recovery records) to the AD-15 appenders, and add both edges to the AD-4 diagram.

### H7 · AD-40 and AD-15: missing signers, and no trust-anchor lifecycle
- **Problem:**
  - Several signed objects have no named key or requester: the platform map ("key not specified"), fleet switch-off statements (AD-57), Orvex's signed advance last-resort permission (AD-55), release metadata expiry (AD-46), and model weights (AD-37).
  - The same map goes by three names ("platform map", "platform-only map", "signed map authorises Orvex") in AD-10, AD-12, AD-13 and AD-15.
  - Nothing says how clusters first receive the verification keys for release, catalogue, policy, people-list and relay (for both Flux and the executor), how those keys rotate, or how a compromised key is revoked. Flux and the executor could end up holding different trust roots.
- **Fix:**
  - Extend the AD-40 key table with each missing artefact, its key and its requester.
  - Settle on one name and schema for the map.
  - Add an AD for trust roots: pinned at install through the privileged install path; rotated by a key-set statement signed by the old and new key with valid_until; compromise handled by an emergency key-set update through the install path. Flux and executor verification keys come from the same source.

### H8 · Operational envelope: the Fleet side is undecided and not deferred
- **Problem:** Only "Fleet hosting unconfirmed" appears. Nothing is decided, deferred or raised as a question for:
  - Fleet availability targets and HA/DR for the relay, registry and signing system
  - how long the audit-checkpoint store keeps data and how it survives loss (AD-16 depends on it)
  - who watches Fleet's own watchdog: the paradigm says every level is "watched from outside itself", and Fleet is not
  - Fleet intake capacity at 10,000 clusters
  - Fleet on-call and runbooks
- **Fix:** Add an AD or Open Question rows covering Fleet availability and DR, checkpoint-store durability, external monitoring of Fleet (for example a second-region probe or a third-party uptime check), and capacity assumptions at NFR-1 scale. Pair each with what the clusters do meanwhile (AD-49 already covers the cluster side).

### H9 · AD-43, AD-42: the privileged install and upgrade path is undefined
- **Problem:** CRDs, ClusterRoles, admission webhooks, Flux itself, first-admin pinning (AD-19), in-cluster key generation (AD-40), coverage discovery (AD-33), trust-root pinning and the manual runbook (AD-45) all go through a "separately authorised installation and upgrade path". That path has no actor, no credential model and no trigger, and it sits in tension with AD-42 ("no … central delivery component … holds cluster credentials"). It is the only path that can widen the executor's RBAC.
- **Fix:** Define it in the spine. For example: run per cluster by a named Orvex person; time-bound credentials issued by the customer or platform owner, never kept by Fleet; checked against the customer maintenance policy; recorded in the audit chain and the Kubernetes audit log; identical on OMK and EKS apart from how credentials are obtained. Or list it in Deferred as blocking the install epic.

## Medium

| # | Location | Problem | Fix |
| --- | --- | --- | --- |
| M1 | AD-35, AD-36 | "The executor checks the account mode and the model's allowed modes", but the executor has no Bedrock path; the gateway calls Bedrock (AD-36, diagram). Also, the return path for AI output (Bedrock → gateway → agent, or → portal) is not shown | Assign the check to credential vending (refuse to vend) and the gateway (refuse to call); add the response path to the AD-4 diagram |
| M2 | AD-60 vs AD-21, AD-9 | "The executor rejects any dangerous-risk RepairRun", yet manual dangerous repairs need executor-held claims, "Start now" acceptance, a coordinator mark and verification after "I've done it" | Reword: the executor never *executes an action* for a dangerous entry; manual-repair RepairRuns carry approval, claim and verification only |
| M3 | Capability map 5.6; FR-26, FR-27 | Repair ranking (safest first) and the next-repair rule (safe only; risky needs Orvex approval; dangerous goes to manual) have no owner. If the untrusted agent ranks, it chooses the order | Add a rule: the executor picks the next repair from the signed entry's ranked list and enforces FR-27; the agent only proposes the entry |
| M4 | FR-2, FR-3, FR-23, NFR-7 | No unit owns node-heartbeat absence or silent-node diagnosis (verification from neighbour nodes, then BMC or EC2 status), or escalation after no answer (re-alert, then call when critical). NFR-7 latency has no budget or open question in the spine | Assign FR-2/FR-3 to the agent with the checker as a second vantage point; FR-23 escalation timers to the executor (in-cluster, survives Fleet loss) or Fleet; add NFR-7 to Open Questions |
| M5 | AD-27, AD-50, AD-58, AD-66, Conventions | Heartbeat "status" values are not fixed (FR-6: alive or degraded). AD-58 puts the halt in the status, AD-50 "degraded". AD-66's proposal (the control cluster's checker reports the management agent) conflicts with FR-6, under which the management agent sends its own heartbeat | Fix the enum in Conventions (alive, degraded; halt and storage-full map to degraded); drop or reword the AD-66 proposal to match FR-6 |
| M6 | AD-17 vs AD-22, AD-51 | AD-17 requires the "portal origin and RP ID". Dashboard-signed stops use the local RP ID (AD-51) and are "verified locally like approvals" (AD-22), so they would fail AD-17. Whether stops and "Start now" from the dashboard need the SMS step is unstated | Make AD-17's origin check "portal origin, or the cluster's registered local RP ID for stop-type decisions only"; state SMS requirements per decision type |
| M7 | AD-38, AD-27, AD-24 vs PRD FR-43, SEC-8, PRIV-9 | Adopted rules contradict the current PRD pending AP-6, AP-8 and AP-4: hosted code fixes first; the heartbeat, Flux pulls and the AWS poller bypass the gateway; the expired tier stops ticked and policy repairs that PRIV-9 says run without the portal. Builders face two authorities | Add one line under Invariants: until each AP lands, the spine governs and the conflicting PRD clause is listed; or keep the PRD behaviour until acceptance |
| M8 | AD-3, AD-5, AD-4 diagram | RBAC is given only for the agent and executor. Gateway, audit, checker, guard, dashboard, adapters, AWS poller and management agent rights are unstated. The dashboard and management agent are missing from the AD-3 boundary list. The dashboard→executor channel (API or Kubernetes object) is unclear, and the diagram says "stops and settings" while AD-51 leaves settings open | List the rights for each unit in AD-5; add the dashboard, management agent and AWS poller to AD-3; fix the edge label to "stops" |
| M9 | Conventions, Deferred | No convention for schema versions on cross-boundary messages (outbox, heartbeat, decisions, receipts, RepairRun CRD versions). Waves guarantee that Fleet sees mixed cluster versions, and "supported version skew" is pushed to release-process design | Add a convention: every cross-boundary message and CR carries a schema version; Fleet accepts N and N-1; CR versions are served through conversion |
| M10 | Operational envelope (environments) | No decision or deferral on: test environments per platform for catalogue testing before signing (FR-39, FR-40, AD-52); what wave-0 test clusters contain; customer network prerequisites (egress allowlist or proxy for the registry, relay, Bedrock, SMS); OMK sites with restricted egress | Add Deferred or Open Question rows: a catalogue test environment on OMK and EKS, and a network prerequisites list per platform |

## Low

| # | Location | Problem | Fix |
| --- | --- | --- | --- |
| L1 | AD-5 / AD-15; AD-7 / AD-49; AD-19 / AD-22 | The same rule appears twice: sole ledger writer, stops before resume on reconnect, revocation as a stop | Keep each rule in one AD and reference it from the other |
| L2 | AD-45, AD-37, AD-52 | Rationale inside the Rules: "(its authority; not NFR-4, since the executor does touch workloads)", "(fine-tuning deferred, not shown uneconomic)", "the number of repairable failure types is not the share of incidents resolved" | Move these to the Orvex document or the memlog |
| L3 | Stack | "W3C Web Authentication Level 3" carries no verification note (status Candidate Recommendation vs Recommendation not checked). ipmi_exporter is listed, but no AD or diagram says it is the OMK BMC reader | Add "(status checked YYYY-MM-DD)"; name ipmi_exporter, or "Redfish reader to choose", in AD-31 |
| L4 | Front matter | `altitude: initiative` vs memlog `altitude: feature (PRD features 5.1-5.11; keeps epics)` | Align with the memlog, or record the change in the memlog |
| L5 | Conventions timing, Deferred values | Some values read as placeholders: "group cap e.g. 4 h", "reserved storage size (e.g. 7 days …)" | State them as starting values ("4 h, assumption to test") |
| L6 | AD-62, EKS | Fencing on EKS needs instance state, which only the optional AWS poller provides (AD-32). Without the poller the outcome is implied, not stated | Add: "without a verified fencing source the executor always escalates" |

## Checks that passed

- **Mermaid:** all four diagrams parse by inspection (flowchart quoting, `<-->|label|`, nested subgraphs, sequence `autonumber` and aliases). No template comments, TODOs or `{{ }}` placeholders.
- **AD ids:** AD-1..AD-66 are all defined; every reference points to an existing AD.
- **Both platforms:** covered throughout (AD-13, AD-31, AD-32, AD-44, AD-51, AD-62, topology diagram), with OMK unknowns listed in Deferred.
- **Named tech:** versions are given only where verified (policy/v1, meta/v1 Preconditions, Prometheus 3.15.1 as of 2026-11-04, Claude prices 2026-11-04); everything else says "pin at build".
- **PRD coverage:** every FR, SEC, PRIV and COST id appears in `binds`, directly or through a range. The real gaps are those noted above: FR-2, FR-3, FR-23, FR-26, FR-27, NFR-7 and the PRIV-9 assignment.
- **Memlog fidelity:** adopted decisions are reflected faithfully (paradigm, P1–P6, option B with its limits, the coordinator points, 3.1–3.4, M1–M3, 5.1–5.6, round 6 D1–D6, round 7). The PRD-carried ADs 53–66 are correctly marked "[PRD; mechanism proposed]".
