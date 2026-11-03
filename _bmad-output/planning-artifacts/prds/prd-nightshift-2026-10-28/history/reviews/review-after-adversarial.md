# Adversarial review (second pass, after fixes): PRD Nightshift

Reviewed: `prd.md` (updated 2026-10-31) and `addendum.md`. Judged as it stands now; earlier review files were not read.
Reviewer stance: hostile expert. Bracketed source tags and style are out of scope. Section 10 deferrals are flagged only where deferring is unsafe for UX or architecture.

## Verdict

The PRD is much tighter on the main approval path (FR-21 to FR-24, SEC-1, SEC-7). It still has two direct paths to changes in customer production that bypass the approval model: FR-41 tuning, and a compromised agent that holds its own execution and egress rights. It also has several contradictions an architect cannot resolve without a product decision: where authorisation is enforced versus local autonomy, one release everywhere versus customer-controlled updates, and the code-fix review path versus FR-39 and FR-40. The staffing claim, which carries the business case, rests on an unverified 90% figure and leaves out most of the human review work the PRD itself creates.

## Counts

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 15 |
| Medium | 17 |
| Low | 7 |

---

## Critical

### C-1. FR-41 tuning is a change to customer production with no authorisation, even in alert-only mode
- **Where:** FR-41; Glossary "Customer production", "Alert-only mode", "Prohibited action"; FR-17; FR-21.
- **Text:** FR-41: "Nightshift may tune the cluster's settings only within the limits set by the tested release; anything bigger goes to Orvex as a proposal." Glossary: "A change that can affect customer production needs the customer's advance permission (a tick in the settings checklist) or the customer's approval per action." Alert-only mode: "never executes **repairs**".
- **Problem:** tuning is not called a repair, is not said to come from the repair catalogue, and is not linked to FR-21, ticks, modes or FR-34. As written it bypasses every authorisation rule. Alert-only mode only forbids *repairs*, so tuning still runs there. Larger changes go "to Orvex as a proposal", not to the customer, so Orvex alone can approve a larger change to the customer's cluster. FR-17 and the "Prohibited action" definition ("improvised repairs that are not in the repair catalogue") contradict FR-41 unless tuning is in the catalogue, and the PRD never says it is.
- **Failure scenario:** a customer in alert-only mode runs a latency-sensitive database. Nightshift "tunes" its CPU limits or HPA minimum replicas within the release limits at 3 AM. Checkout latency doubles. Nothing in FR-34 records who permitted it, and SM-4 cannot count it because no approval record was expected. Repeated small changes, each within the limits, add up to a large one, and FR-30 limits only *repairs*.
- **Fix:** define tuning as a class of repair catalogue entries with risk levels, subject to FR-21, ticks, modes, FR-30 and FR-34. Route "anything bigger" to the customer as an approval request, with Orvex technical approval on top, not to Orvex alone. Add a cumulative-drift limit per setting.

### C-2. SEC-2 contains approvals but not execution or egress: a compromised agent can change production and exfiltrate data without forging anything
- **Where:** SEC-2, SEC-3, SEC-4, FR-25, PRIV-4, FR-35, SM-4.
- **Text:** SEC-2 "Approvals: The agent cannot approve its own repairs, forge approvals or change its permissions. Enforcement sits outside the agent." FR-25 "Nightshift applies the repair". 3.2 "Nightshift still has permitted diagnostic access". FR-35 "the agent can add to it but cannot change or delete entries."
- **Problem:** SEC-3 moves only *hardware* credentials out of the agent. The Kubernetes credentials needed to drain, restart, delete pods, clean node disks (hostPath, which in practice means node root) and read customer databases remain, by implication, in the agent that "applies the repair". A compromised agent does not need to forge an approval; it calls the Kubernetes API directly. Likewise, PRIV-4's outbound check and the PRIV-3 allowlists have no required location, so if they run inside the agent, a compromised agent skips them. FR-35 also lets the agent *add* entries, so it can write plausible execution records. SM-4 compares those with approval records, so the comparison relies on what the attacker wrote. The SEC-2 table has no "customer data / egress" row at all.
- **Failure scenario:** a log-parsing bug gives an attacker code execution in the agent. The attacker uses the agent's service account to cordon and drain every node (outage), reads customer tables through "permitted diagnostic access", and sends them out in hosted-model calls disguised as sanitised prompts. No approval was forged, so SEC-2 is met on paper.
- **Fix:** add SEC-2 rows: (a) **Execution:** mutating credentials live in a separate executor outside the agent. The executor accepts only signed catalogue actions, each with a verifiable authorisation token from the approval service, and the agent itself has read-only RBAC. (b) **Egress:** the PRIV-3 allowlist and the PRIV-4 check are enforced at a network egress point outside the agent, and the agent has no other route out. (c) **Records:** approval records come only from the approval service, never from the agent, and SM-4 is computed from executor logs, approval-service logs and Kubernetes or BMC audit logs, not from agent-written records.

---

## High

### H-1. Authorisation is not re-checked at execution time: revocation races produce unapproved changes
- **Where:** FR-22 third bullet; FR-21 (delegation "can revoke it at any time"); SEC-6; SEC-7.
- **Text:** "Right before every run, Nightshift re-checks the repair's **safety preconditions** from the repair catalogue. If they still hold, it runs."
- **Problem:** the run-time re-check covers safety preconditions only. It does not cover authorisation state: tick still present, mode still approval-enabled, delegation still in force, catalogue entry not switched off (SEC-6), last-resort still ticked, approver still authorised.
- **Failure scenario:** at 02:00 Orvex support, under delegation, approves a risky restart, and Josh gives Orvex technical approval. The repair waits in the coordinator queue (FR-29) behind a drain. At 02:05 the customer revokes the delegation, or switches to alert-only mode, because they are handling it themselves. At 02:10 the restart runs: an unapproved change to customer production that the customer explicitly withdrew.
- **Fix:** FR-22: "Right before every run, the enforcement point re-checks authorisation (mode, tick and tick version, delegation, approval validity, last-resort, kill switch) together with the safety preconditions; any change cancels the run." Make it a testable consequence.

### H-2. Local autonomy contradicts enforcement outside the agent
- **Where:** 5.7, NFR-5, Vision ("Each cluster looks after itself when central coordination is unavailable") versus SEC-2 ("Enforcement sits outside the agent") and SEC-7 ("alert-only mode is enforced outside the Nightshift agent").
- **Problem:** if the enforcement point (ticks, mode, approval validity) is central, a disconnected cluster cannot run even ticked safe repairs, which breaks NFR-5. If it is local, it is inside the cluster the agent controls, so "outside the agent" needs a definition. The PRD does not say which, and the answer changes the architecture: a local policy enforcer, cached signed policy, revocation latency and the offline audit buffer.
- **Failure scenario:** a network split cuts a cluster off from Fleet and the portal. Either (a) a disk fills and the ticked cleanup does not run, because the external enforcer is unreachable, or (b) the agent enforces from its own cache, a customer's untick made during the split is never seen, and the repair runs after permission was withdrawn.
- **Fix:** state that the enforcement point is a separate in-cluster component outside the agent's trust boundary, enforcing a signed policy snapshot. Define its behaviour when offline: ticked safe repairs run; nothing that needs a fresh approval runs; revocations take effect on reconnect, with a stated maximum staleness. State that offline audit records are buffered by that component, not by the agent.

### H-3. Delegation plus Orvex technical approval means Orvex alone approves risky changes, including its own platform changes
- **Where:** FR-21 (delegation), Glossary "Orvex technical approval" ("so the customer cannot damage their own app"), FR-47, Q1.
- **Problem:** for a risky repair, the customer's approval can come from Orvex support and the technical approval from the Orvex Nightshift team, so both "keys" belong to Orvex. Nothing requires two different people or prevents one person from holding both roles. Under FR-47 a delegated customer approval also lets Orvex approve changes to Orvex's own software in the customer's production, which is a conflict of interest that the "customer's permissions" framing was meant to prevent.
- **Failure scenario:** one Orvex engineer with both support and Nightshift-team roles clicks both approvals for a risky restart of a single-replica service at 3 AM. The customer learns of it from the after-the-fact notification.
- **Fix:** require that the delegated approver and the technical approver are different people with separate roles, enforced by the approval service. State whether delegation can cover FR-47 platform changes; recommend that it cannot by default. Add delegation-scoped approvals to FR-34.

### H-4. Individually safe repairs can run concurrently on different targets and invalidate each other's safety preconditions
- **Where:** FR-29 ("on the same target"), Glossary risk table ("Restart an affected replica, when the healthy replicas can carry the traffic ... Safe"), FR-30.
- **Problem:** the coordinator serialises only per target. Two safe repairs on *different* replicas or nodes of the same service each check "healthy replicas can carry the traffic" at the same moment, both pass, and together remove too much capacity. FR-30's "rate limits ... based on the impact on workloads" and "checks for conflicting changes" have no definition of impact, scope or threshold, so they cannot be tested.
- **Failure scenario:** memory creep on 3 checkout replicas. The rule fires for replicas A and B within the same second. Each restart sees 2 healthy peers and is classified safe. Both run, one replica carries all checkout traffic and falls over. No approval was ever requested because each repair was safe and ticked.
- **Fix:** coordinate at the level of the *safety domain* (the service or PodDisruptionBudget, the node pool), not the target. Re-evaluate preconditions under a lock that covers that domain. Define FR-30's impact measure (for example, capacity removed per service per window) as a testable limit.

### H-5. Stale or failed monitoring still feeds safety-precondition checks
- **Where:** FR-4 ("When these checks fail, Nightshift opens a monitoring failure case"), FR-22, Glossary "Safe repair".
- **Problem:** FR-4 opens a case but says nothing about what happens to automatic repairs while Nightshift's own data is stale. The checks "healthy replicas can carry the traffic" and "the runtime confirms removal is safe" are only as good as data freshness.
- **Failure scenario:** Prometheus stalls at 02:00. At 02:20 a ticked safe restart checks replica health from 02:00 data, which still shows 3 healthy replicas when in fact 2 crashed at 02:10. It restarts the last healthy one.
- **Fix:** add a testable consequence to FR-4 and FR-22: every precondition carries a maximum data age; past it, the precondition fails closed. While a monitoring failure case is open in a cluster, automatic repairs there are suspended.

### H-6. Silent-node mitigation without fencing causes split-brain data corruption
- **Where:** FR-20 "Report uncertainty": "it may run only a mitigation that is valid whatever the cause"; FR-3; FR-7 "Node goes silent without out-of-band management".
- **Problem:** the standard mitigation for a silent node, rescheduling its pods elsewhere, is *not* valid whatever the cause. In a network partition the node is alive and its stateful pods are still writing. Without fencing (power-off through the BMC, which is dangerous) or a storage-level lock, moving a StatefulSet pod or a ReadWriteOnce volume creates two writers. In limited-visibility mode fencing is impossible by definition.
- **Failure scenario:** a top-of-rack switch fault isolates node C, which runs the primary of a Quornex-managed database. Nightshift treats rescheduling as cause-agnostic, force-detaches the volume and starts a new primary on node D. Node C is still serving local clients. The data diverges.
- **Fix:** state that any mitigation that moves stateful workloads off a silent node requires confirmed fencing, and is dangerous otherwise. In limited-visibility mode, stateful failover from a silent node is never automatic. Add this as a must-have entry in the failure catalogue.

### H-7. Code-fix review path contradicts FR-39, FR-40 and NFR-3
- **Where:** FR-44 steps 4 to 6, FR-42 step 3, FR-39, FR-40, NFR-3.
- **Text:** FR-44 "An Orvex engineer reviews ... **The engineer** approves or rejects the patch. An approved patch enters the repair catalogue". FR-39 "A new or changed repair catalogue entry needs **two reviewers**." FR-40 "never as one-off changes to single clusters". NFR-3 "differences between customers are only their permissions and settings".
- **Problem:** a customer-specific code-fix entry is by definition a one-off change to one customer's clusters, delivered outside the "tested release", so it breaks FR-40 and NFR-3. It is approved by one engineer, which breaks FR-39. The PRD also never says what risk level an AI-written code deployment can have. If Orvex classifies one as "safe", a customer who ticks it gets AI-written code deployed to production automatically.
- **Failure scenario:** one engineer approves a patch whose regression tests pass but whose fix changes the rounding in a pricing function. It is marked safe and ticked, deploys automatically at the next occurrence, and silently mis-charges customers.
- **Fix:** apply FR-39's two reviewers to code-fix entries. Add an explicit exception to FR-40 and NFR-3 for customer-specific entries, with their own signing and distribution path (SEC-5). Set a floor of "risky" for any code deployment, so it can never run on a tick alone.

### H-8. A customer's proprietary code can become a fleet-wide catalogue entry for other customers
- **Where:** FR-42 step 3 ("as a fleet-wide entry if it is reusable"), FR-38 ("lessons (rules, catalogue entries, fixes)"), PRIV-1, PRIV-6.
- **Problem:** a code fix is derived from customer A's source code. Orvex alone decides it is "reusable" and publishes it to the fleet. The patch, together with the code context and test it carries, reaches other customers. Nothing requires customer A's consent, and it breaks the spirit of PRIV-1 and PRIV-6 (code stays in the cluster). It may also break customer A's intellectual-property rights.
- **Failure scenario:** a fix to customer A's custom payment-retry module becomes a fleet entry. Customer B, a competitor, sees the entry in their catalogue checklist, including its description and diff.
- **Fix:** a code fix derived from a customer's code is always customer-specific. Promoting it to the fleet requires the originating customer's explicit written consent and an Orvex rewrite that contains none of their code.

### H-9. Orvex unilaterally controls what leaves the cluster and can widen it through a routine update
- **Where:** PRIV-3 ("Orvex defines and owns the list of allowed fields, recipients and destinations"), FR-47 routine updates under the maintenance policy, Vision ("only approved, sanitised information" leaves).
- **Problem:** "approved" is approved by Orvex alone. A routine Nightshift release can add fields, recipients or destinations, such as a new hosted-model provider or region, and it rolls out under the maintenance policy without the customer seeing that their data boundary changed. For a product sold on *sovereignty*, the customer has no control over its own egress policy.
- **Failure scenario:** release 2.5 adds "service name" and "error message template" to the hosted-model allowlist and switches to a model endpoint in another jurisdiction. It deploys under the routine maintenance policy, and the customer's data now leaves under terms they never saw.
- **Fix:** make PRIV-3 lists versioned and visible to the customer. Any widening (new field, recipient, destination, provider or region) needs the customer's explicit consent, like a changed tick (FR-22), and never rides along in a routine update. The customer can choose a stricter list.

### H-10. Code sent to a hosted model contradicts "secrets never leave", and the absolute claim rests on an untested sanitiser
- **Where:** Vision ("Raw data and secrets never leave the cluster"), PRIV-2, PRIV-6 ("This is the only exception to PRIV-1"), FR-43, Section 7 (hosted model is the first-version focus), Q16.
- **Problem:** (a) Source code commonly contains hard-coded credentials, internal hostnames and customer identifiers. FR-43 sends "the relevant code" raw; nothing applies PRIV-2 or PRIV-4 sanitising to code, so "secrets never leave" is false for every consenting customer. (b) FR-44 step 4 lets an Orvex engineer access customer code remotely, which is a second exception, so "the only exception" is also false. (c) For everything else, the absolute "never" depends on free-text log sanitising that Q16 still lists as *to test*, while Section 7 makes the hosted model the default path for all explanations.
- **Failure scenario:** `config.py` in the relevant code holds a Stripe live key. It is sent to the hosted model and stored in the provider's logs.
- **Fix:** require secret scanning and redaction of code before any hosted transfer, with the transfer blocked on a hit. List all exceptions (hosted code transfer, engineer access to the test environment). Restate the Vision claim as a design goal that is tested by PRIV-7, not as a guarantee.

### H-11. One release everywhere (FR-46, NFR-3) contradicts customer-controlled updates (FR-47)
- **Where:** FR-46 "Every cluster runs the same tested Nightshift release"; NFR-3; FR-47 "Routine updates run under a maintenance policy the customer has authorised".
- **Problem:** if the customer can choose update types and windows, or never authorise a policy, clusters will run different Nightshift, catalogue, OMK and Quornex versions, possibly for a long time. That affects catalogue compatibility, the versions ticks are bound to (FR-22), SEC-6 switch-off across versions, security patching, and the FR-46 canary logic (customer windows decide which clusters can be in the first group).
- **Failure scenario:** a customer never authorises a maintenance policy. Their cluster stays on a release with a known sanitiser bug (H-10) and a catalogue entry later found harmful. Their old agent does not recognise the SEC-6 switch-off format.
- **Fix:** pick one: (a) security and safety updates (sanitiser, kill switch, signature roots) are mandatory and outside the customer's policy, stated explicitly, while feature updates are policy-gated; or (b) define a supported version window (N and N-1) and what happens to clusters outside it.

### H-12. A compromised Fleet can still do harm through signed artefacts and orchestration; SEC-5 overclaims
- **Where:** SEC-5 ("so a compromised Quornex Fleet or release pipeline cannot push unapproved changes"), FR-32 (Fleet "stops the update ... and coordinates recovery"), FR-47 emergency rollback, SEC-6.
- **Problem:** signatures prove origin, not freshness or intent. A compromised Fleet can (a) start "emergency rollbacks" to an older, validly signed release with known vulnerabilities (a downgrade attack) on every cluster with a rollback policy, (b) switch off safety-critical catalogue entries fleet-wide (SEC-6), (c) pause all rollouts, and (d) if the portal or approval service runs in Fleet, which the PRD does not exclude, forge approvals. None of these needs an unsigned artefact.
- **Failure scenario:** an attacker in Fleet declares a "correlated failure" on 2,000 clusters and rolls them back to v2.1, which has a known RBAC escalation. Every step uses signed artefacts and authorised rollback policies.
- **Fix:** add anti-rollback (a minimum allowed version per cluster) and signed, time-limited rollback and kill-switch commands from a separate signing authority. State that the approval service is isolated from Fleet. Reword SEC-5 to what signatures actually guarantee.

### H-13. The staffing estimate that carries the business case is unverified, and the arithmetic leaves out most of the human work
- **Where:** SM-8, SM-9, Section 2 ("one on night duty"), FR-21 (risky repairs need Orvex technical approval "each time"), FR-39, FR-44, SM-6, Vision bullet 4.
- **Problem:** (a) The 90% "handled automatically" figure is assumed. SM-9 measures something else, "the share that needs Orvex technical approval", which is not the same as "handled automatically": problems escalated to customers or approved only by customers are not automatic but do not need Orvex either. (b) The arithmetic counts only incident handling. It leaves out FR-39 two-reviewer catalogue reviews, review of every fleet lesson, FR-44 code-fix reviews, SM-6 labelling of every alert, FR-21 recovery-plan reviews, and the fact that *every* risky repair, ticked or not, needs Orvex approval each time. (c) At the base case one night engineer is already 100% loaded (8.3 hours of work in an 8-hour shift), and during a UJ-5 fleet incident every other approval queues behind them. Seats for 24/7 rotation, holidays and day shifts are not derived.
- **Failure scenario:** a bad night (500 problems, 17 hours of work) coincides with a 300-cluster incident. The one engineer is busy for 2 hours. Risky repairs across the fleet wait, last-resort conditions fire unattended, and the "15 engineers" claim fails on day one.
- **Fix:** model human load as the sum of all human-gated activities in the PRD, per role. Derive seats from shift coverage. Make "approval latency at P95 per risky request" a success metric. Present 15 engineers as a hypothesis with its sensitivity range, not as an estimate.

### H-14. Rollback, the flagship repair, has no risk level and no handling of data migrations
- **Where:** UJ-2, UJ-4, UJ-5, FR-32, FR-47; 3.2 non-goal (never "modify ... databases").
- **Problem:** rollback is the repair the journeys rely on, but its risk level is never stated, and the risk-level table does not include it. A rollback across a forward-only schema migration either corrupts data (the old code writes in the old format to the new schema) or needs a down-migration, which modifies a database and is a prohibited action. FR-47 emergency rollbacks run "without fresh approval" whenever "safety conditions pass", and those conditions are undefined.
- **Failure scenario:** checkout v42 adds a non-null column. UJ-4's pre-ticked rollback to v41 runs at 2:20 AM, inserts fail, and orders are lost, while the morning summary says "Checkout recovered".
- **Fix:** add rollback to the risk-level table with its conditions: no schema or data-format change between versions means safe or risky, and otherwise dangerous or not permitted. Make "no irreversible migration in the diff" a mandatory safety precondition of every rollback catalogue entry, for both application and platform rollbacks.

### H-15. Deferring "which hosted models and regions are trusted" (Q6) is unsafe for the architecture
- **Where:** Section 10 Q6 and the triage ("none of the remaining items blocks UX or architecture"); Section 7 (hosted model is the first-version focus); Vision ("sovereign cloud").
- **Problem:** the first version's main AI path is a hosted model, yet whether it may be a US-jurisdiction provider, an EU-hosted provider or a self-hosted Orvex service decides the architecture: endpoints, egress control, data residency, the cost model and contracts. It also decides the core sovereignty promise. Q1 (who approves OMK and Quornex changes) and Q2 (whether Orvex technical approval fits Danny's model) likewise shape the approval UX flows, so the triage claim is wrong for them too.
- **Failure scenario:** the architecture and cost model are built on a US hyperscaler model API. Danny later answers "EU-sovereign only", and the cost model, latency figures and egress design have to be redone after hand-in.
- **Fix:** make a working assumption now, for example "hosted = EU-jurisdiction provider with zero retention, or Orvex-operated shared GPU", label it a design assumption, and have the cost model show the alternative as a sensitivity case.

### H-16. No validation that the BMC endpoint belongs to the node it is said to manage
- **Where:** FR-7 (installation validates "credentials, power status and hardware health reporting"), SEC-3 ("allowed actions are listed per machine"), Glossary "Customer hardware" ("may be badly configured").
- **Problem:** installation checks that each BMC answers, not that BMC X is node Y. With customer hardware the PRD itself expects to be badly configured, a swapped inventory entry is likely. The approver sees "power-cycle node-7", while the action goes to node-3's BMC. The allowlist "per machine" applies the wrong mapping faithfully.
- **Failure scenario:** node-7 goes silent and a dangerous power cycle is approved. The BMC mapped to node-7 is actually node-3, the healthy database primary. Power-cycling it causes an outage and possible data loss, and node-7 stays down.
- **Fix:** FR-7 consequence: installation proves the identity binding between node and BMC (serial, system UUID or MAC match, or a controlled LED or identity test), and Nightshift re-verifies the binding right before any BMC action. A mismatch blocks the action.

---

## Medium

### M-1. FR-34 cannot record half of the PRD's permission sources, which breaks the SM-4 measurement
- **Where:** FR-34 ("who permitted it (ticked, or approved at the time, by whom and when)"), FR-24, FR-47, FR-21 delegation, SEC-7.
- **Problem:** the record has no field for the last-resort condition, the maintenance policy, the rollback policy, a delegated approval ("on behalf of"), or Orvex's half of the last-resort advance permission. SEC-7 says only *customer* administrators change the last-resort condition, so who at Orvex grants Orvex's advance permission, and how it is recorded, is undefined. SM-4 compares executions against approval records and "policy decisions", so every legitimate policy-driven change is either counted as unapproved or excluded by hand.
- **Fix:** list all permission sources in FR-34, each with an identifier, version and signer. Define Orvex's last-resort grant: who grants it, its scope, its expiry and how it is recorded.

### M-2. The last-resort condition is untestable and gameable
- **Where:** FR-24, FR-23 ("If they do not answer in time"), FR-22 ("There are no timers to manage").
- **Problem:** (a) "Nobody answers" has no timeout, yet FR-22 says there are no timers; the PRD contradicts itself, and FR-24 cannot be tested. (b) Non-answer is not distinguished from non-delivery: a Slack or telephony outage, or a cluster cut off from the network, satisfies "nobody answers", so an outage or attacker that blocks egress turns a request into an execution. (c) It applies only when failure is *predicted* within 30 minutes. Once checkout has already failed, nothing is "predicted", so the worst case, an outage in progress, gets *less* automation than an imminent one.
- **Fix:** define a response timeout per request (shorter than time to impact), require proof of delivery to at least one approver channel before silence counts as no answer, and decide explicitly whether last-resort applies to failures already in progress.

### M-3. A fleet-wide approval (UJ-5) contradicts the definition of a single-use approval
- **Where:** UJ-5 ("he approves"), Glossary "Approval" ("single-use and tied to the exact repair, target ..."), FR-32.
- **Problem:** does Josh approve once for 300 targets, or 300 times? The first breaks the definition; the second makes UJ-5 impossible at 3 AM. Each customer's own approval (FR-47) is also needed, so the per-customer approval UX at scale is undefined.
- **Fix:** define a batch approval: one signed approval naming an explicit list of targets, each target checked individually against its customer's authorisation at run time (H-1).

### M-4. An approval has no expiry, and binding it to the "evidence shown" is either ignored or causes endless re-asking
- **Where:** Glossary "Approval" ("tied to ... evidence shown"), FR-22 ("no timers").
- **Problem:** in a fast-moving incident the evidence changes every scrape, so binding it strictly forces a new request each time and an approver never catches up. With loose binding, an approval clicked six hours late on an old Slack message still executes if the preconditions hold, even though the request said "if you don't answer, we won't change anything".
- **Fix:** give approvals a maximum age, set per risk level, and define which evidence fields are binding (problem ID, target, repair version, severity band) and which may drift.

### M-5. Who coordinates multi-cluster recovery: Fleet or the management agent?
- **Where:** FR-29 ("Repairs that affect more than one cluster are coordinated by the management agent, and wait while it is unavailable") versus FR-32 ("Quornex Fleet ... coordinates recovery across all the affected clusters"); Glossary (control cluster "optional").
- **Problem:** the 300 clusters in FR-32 belong to many customers, and the management agent is per customer. A customer with several workload clusters but no control cluster has no management agent, so under FR-29 their multi-cluster repairs wait forever.
- **Fix:** state that Fleet coordinates only Orvex platform rollouts and rollbacks, and management agents coordinate customer-scope repairs. Define the fallback for multi-cluster customers without a control cluster.

### M-6. Coordinator marks both expire (FR-29) and persist (FR-31); NFR-4 overclaims
- **Where:** FR-29 ("its marks expire"), FR-31 ("The coordinator's marks ... stay in place"), NFR-4 ("Nightshift failing never harms the customer").
- **Problem:** if the agent is down longer than the mark lifetime, the marks expire mid-repair and Kubernetes or a person acts on a half-drained node. If marks never expire, a dead Nightshift leaves nodes cordoned and capacity reduced indefinitely, which is harm caused by Nightshift failing.
- **Fix:** marks expire only if the owning repair is confirmed dead, with Fleet alerting on orphaned marks. Restate NFR-4 as a testable bound, for example "no Nightshift-held cordon or lock outlives the agent by more than X without a person being notified".

### M-7. Dangerous repairs that disconnect the node cannot be verified or rolled back; the recovery plan may be improvised
- **Where:** Glossary "Dangerous repair" ("anything on a live node that could disconnect it from Nightshift"), FR-21 ("plus a recovery plan reviewed before the repair runs"), FR-25, FR-17.
- **Problem:** FR-25 assumes Nightshift can check the result and undo the repair. After a NIC or IP change cuts the link, it can do neither. The PRD does not say who writes the "recovery plan" or who reviews it. If the AI writes it, or the engineer writes it ad hoc, it is an improvised repair that FR-17 forbids.
- **Fix:** each dangerous catalogue entry includes a pre-tested recovery plan and an automatic node-local revert (a dead-man switch: revert unless confirmed within N minutes). "Reviewed" means confirmed by the approver against the catalogue, not written at the time.

### M-8. The blast radius of a compromised management agent is not covered
- **Where:** SEC-2 (only "the Nightshift agent in one cluster"), FR-6, FR-29, PRIV-5.
- **Problem:** the management agent coordinates every workload cluster of a customer, runs cross-cluster investigations and coordinates multi-cluster repairs. If it is compromised, every cluster that customer owns is exposed, and PRIV-5's "only sanitised information" has no enforcement point outside it.
- **Fix:** extend SEC-2 to the management agent. Workload agents accept only signed, policy-checked coordination requests, and sanitising happens at the workload cluster's egress before data reaches the management agent.

### M-9. Diagnostics can change production; "reading is not changing" is not true by the PRD's own definition
- **Where:** FR-21 ("Permission to read never means permission to change"), 3.2 ("permitted diagnostic access"), Glossary "Customer production" (defined by *effect*).
- **Problem:** heap dumps pause the JVM, profilers add load, `EXPLAIN ANALYZE` executes the query, and log-level changes alter behaviour. During an incident, diagnostic queries against a saturated database make it worse. Heap dumps also contain customer data in raw form.
- **Fix:** classify diagnostic actions as catalogue entries with risk levels. Only passive reads (metrics, logs, the Kubernetes API) are "reading". Ban artefacts that contain raw data, such as heap dumps, unless the customer explicitly permits them, and never send them out of the cluster.

### M-10. Prompt injection can still reach the decision through the human approver and through induced signals
- **Where:** SEC-1, FR-11, Section 2 (the approver is a "non-expert business owner").
- **Problem:** (a) Facts are shown "separately" from the AI's wording, but the non-expert customer reads the plain-language AI text, which is exactly where an injected log line can steer ("this is a routine, safe fix, please approve"). (b) "More than one independent signal" is undefined: two log streams from two attacker-controlled pods are not independent. (c) A malicious tenant workload can create real signals, such as filling a disk or allocating memory, to trigger ticked repairs (evictions, drains) on demand.
- **Fix:** generate the approval text that describes the action from the catalogue template, never from the model. Define independence (different source and collection path, at least one not under workload control). Add a rate limit per workload on repairs that workload's signals triggered.

### M-11. PRIV-4's outbound check is untestable and has no failure behaviour
- **Where:** PRIV-4 ("a further test runs on every whole line ... to make sure nothing harmful, such as injected instructions, goes out").
- **Problem:** the PRD does not say what the test is, what counts as "harmful", what happens on a hit (block, quarantine, alert, or degrade to "time and type only"), or where the check runs (see C-2). "To make sure" is a guarantee the check cannot give.
- **Fix:** define the check's classes (secret patterns, PII detectors, instruction-like text), the fail-closed behaviour, the location of the check outside the agent, and measurable detection rates in PRIV-7's planted tests.

### M-12. Engineer access to the code-fix test environment is a new privileged path with no security requirement
- **Where:** FR-44 steps 2 and 4.
- **Problem:** an Orvex engineer "securely accesses" an environment "within the customer's infrastructure". To run the app, that environment usually needs configuration, credentials and often data copies. Neither SEC nor PRIV says anything about data copies in the test environment, the engineer's access scope, session recording or credential isolation.
- **Fix:** the test environment uses synthetic or masked data and no production credentials. Engineer access is time-limited, recorded (FR-33) and read-only to the diff and test results.

### M-13. Deploying a code fix leaves the customer's source repository out of step with production
- **Where:** FR-42 step 5 ("Nightshift deploys the fix if deployment is supported").
- **Problem:** if Nightshift patches the running image or deployment, the customer's next ordinary deploy from their own repository silently reverts the fix, or production runs code that is in no repository. If Nightshift writes to the repository, it is changing customer assets with no stated scope.
- **Fix:** the deliverable of a code fix is a pull request or patch in the customer's source control, to be deployed through their pipeline. Nightshift does not deploy directly, or does so only as a temporary hotfix marked to expire.

### M-14. "Harmful", "makes things worse" and "worth alerting" have no definitions, so SM-2, SM-3 and SM-6 cannot be measured consistently
- **Where:** FR-9 ("weighs four factors"), FR-28 ("if a repair makes things worse"), SM-2 ("without causing another problem"), SM-3.
- **Problem:** FR-28's automatic stop trigger, the vision's "zero harm" count and the alert decision have no operational definition. Two reviewers will classify the same event differently, and the agent cannot run FR-28 without a rule.
- **Fix:** define a harmful repair (for example, a worsened health signal or a new incident on the same target or safety domain within T after the repair). Make FR-28's trigger a catalogue-defined guard. Give FR-9 a decision rule or scoring rule, even if its thresholds are deferred.

### M-15. Ticks lapse silently on release, and implementation changes skip re-consent
- **Where:** FR-22 ("if a release changes the repair's action, conditions or risk level, the customer must tick it again").
- **Problem:** (a) After a release, the customer's expected automatic repairs quietly stop running until they tick again. The PRD does not say they are told, so the 3 AM cleanup they relied on does not run. (b) Changes to the *implementation* (how the action is executed) that keep the same declared action, conditions and risk level carry the old tick over, so changed behaviour runs on a tick given for the old version.
- **Fix:** notify the customer of every tick invalidated by a release, before it deploys, and show the lapse on the dashboard. Bind ticks to a hash of the whole signed entry, or define which implementation changes count as material.

### M-16. Maximum-privacy customers get no AI explanations, but FR-11 still promises them
- **Where:** PRIV-2 ("In strict cases, only the time and type of a problem leave"), FR-11, Section 7.
- **Problem:** with no in-cluster GPU and a hosted model that receives only time and type, nothing can write a contextual plain-language explanation. FR-11 and SM-5 still apply.
- **Fix:** require template-based explanations from catalogue entries as the baseline for every supported problem. AI wording is an enhancement, and the morning summary states which mode produced each message.

### M-17. Nothing watches Fleet, and a Fleet outage looks like a fleet-wide failure
- **Where:** FR-6 (Fleet is the external watchdog), FR-32.
- **Problem:** if Fleet's ingestion fails or Fleet loses network reach to a region, thousands of agents look silent. FR-32's correlation logic may raise a false "300 clusters failing" alert, or pause rollouts. Nothing monitors Fleet itself.
- **Fix:** require an independent watchdog for Fleet. Before declaring agents silent across many clusters, check a sample through a second path.

---

## Low

### L-1. Duplicate open-question ID
Section 10 uses "7a" and "7b" (for Danny) and also "7" (hand-in date, answered). **Fix:** renumber.

### L-2. Three catalogue names, with no mapping between them
"Failure catalogue" (Section 11, FR-1, tags *predict / fix / only report*), "incident catalogue" and "repair catalogue" (Glossary). FR-1's tested scope is 20 failures, while FR-8 lists about 30 predictable problems, so SM-1's denominator ("supported, slowly developing problems") is ambiguous. **Fix:** state that the failure catalogue deliverable is the first-version content of the incident and repair catalogues, and that SM-1 counts only its *predict* entries.

### L-3. The Glossary's "Approval" leaves out the exception for dangerous repairs
Glossary: "The customer approves, or Orvex support if the customer delegates to them". FR-21 excludes dangerous repairs from delegation. **Fix:** add "except dangerous repairs" in the Glossary.

### L-4. "All three model options" versus "Focus: the hosted model"
3.1 lists all three options as in scope; Section 7 makes the hosted model the first-version focus. **Fix:** say that all three are *costed and compared*, and the hosted model is *built*.

### L-5. SM-1 measured on injected faults is biased towards the faults that were designed for
SM-1 validated with failure injection measures recall on the faults the team chose to inject. **Fix:** also track SM-C1 (missed problems) on real clusters, and report SM-1 with its injection scope.

### L-6. The coordinator ignores actions taken by the hosted-Kubernetes provider
FR-29 considers "Kubernetes' own controllers, the customer's deployments and people", but not EKS node auto-repair, autoscaling-group scale-in or managed node-group upgrades, which drain nodes on their own. **Fix:** add provider actions to the coordinator's inputs on hosted Kubernetes.

### L-7. FR-28's stop has no resume path and halts unrelated safe repairs
"Stops further automatic repairs on that cluster" does not say who resumes them, and blocks ticked repairs for unrelated problems, such as a disk filling, while the stop lasts. **Fix:** scope the stop to the affected safety domain, and name who can lift it.
