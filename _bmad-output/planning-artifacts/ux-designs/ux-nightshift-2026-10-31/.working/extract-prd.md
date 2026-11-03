# Extract: PRD → UX source material (Nightshift)

Sources (read in full): `prds/prd-nightshift-2026-10-28/prd.md` (status: final, updated 2026-10-31), `addendum.md`, `validation-report-after.md` (run 2026-10-31T15:31; several of its findings were applied to the PRD afterwards as "after-review fix, 2026-10-31" — noted per item in I). Anything not stated in the sources is marked [INFERRED].

---

## A. Users, roles, personas, who approves what

**User types (PRD §2, verbatim names):**
- **"Primary: the Orvex Nightshift team."** "watch over Nightshift itself and give Orvex technical approval for risky and dangerous repairs. About 15 engineers, one on night duty (Amine's estimate, to test)." SM-8: "one engineer is on duty, with 2 or 3 backup engineers who help remotely from home only when needed".
- **"Secondary: the customer's business owner** (or another senior person)." "Not a technical expert; they chose Quornex so they would not need DevOps staff." NFR-8: every message understandable "by a business owner without infrastructure expertise".
- **"Secondary: Orvex support."** "handle customer problems and answer approval requests when a customer delegates approval to them."
- SEC-7 names one more role: **"authenticated customer administrators"** — only they "can change modes, ticks, the last-resort condition, delegation and read scope". Relation to business owner undefined (validation, Glossary drift).

**UJ protagonists (verbatim):** UJ-1 "the owner of an online shop running on several Quornex clusters" (unnamed); UJ-2 **Cris** ("owns an online shop running on Quornex"); UJ-3 **Josh** ("the Nightshift engineer on night duty"); UJ-4 **Samira** ("a customer's business owner"); UJ-5 **Josh** ("the Orvex Nightshift engineer on night duty"). No journey for Orvex support; none for the settings checklist.

**Who approves what — FR-21 (approval-enabled mode only):**

| Risk level | Customer can tick in advance? | If ticked | If not ticked |
|---|---|---|---|
| Safe | Yes | "Runs automatically, no Orvex technical approval" | "The customer's approval at the time" |
| Risky | Yes | "Orvex technical approval each time it is about to run, after Nightshift confirms the customer ticked it" | "The customer's approval and Orvex technical approval, at the time" |
| Dangerous | No | — | "The customer's approval and Orvex technical approval, at the time, plus a recovery plan reviewed before the repair runs" |

- Prohibited action: "can never be ticked or approved" (FR-21; Glossary).
- Alert-only mode: Nightshift "informs and recommends, but never executes repairs or asks for approval to execute them" (Glossary).
- Defaults: "A new customer starts in approval-enabled mode with safe repairs ticked by default; the customer can untick any of them" (Glossary, Approval-enabled mode).
- Orvex sets risk levels: "customers cannot change it" (Glossary, Risk level). Same action can carry different levels depending on conditions; "each catalogue repair states the conditions its risk level assumes".
- Reclassification: success history "never lowers its risk level or removes approvals automatically" (FR-21).
- Orvex technical approval: "a technical check by the Orvex Nightshift team, in addition to the customer's approval, so the customer cannot damage their own app" (Glossary).

**Delegation (FR-21):** "Orvex support may give it instead if the customer has delegated approval to them." "**Delegation never covers dangerous repairs: the customer always approves those personally** (Amine, 2026-10-31)." "The customer sets the delegation's scope, can revoke it at any time, and is notified of every approval given on their behalf." Note: Glossary "Approval" still reads "The customer approves, or Orvex support if the customer delegates to them" with no dangerous exception (validation L-3, not fixed).

**Last-resort condition (FR-24):** customer must tick it; "Orvex never applies it on its own"; covers "only repairs the customer is allowed to tick (safe and risky), never dangerous or prohibited"; applies "only when nobody answers and failure is predicted within about 30 minutes" (to validate, Q14). For risky: "Orvex's permission given in advance replaces Orvex technical approval at that moment." Who at Orvex grants it / screen: unspecified.

**Platform updates (FR-47, pending Danny):** routine updates under a customer-authorised **maintenance policy** (update types + maintenance windows); security updates "required by the customer contract: the customer chooses the window, within a short deadline"; **emergency rollback** without fresh approval only under a pre-authorised **rollback policy** whose safety conditions pass; otherwise "asks for approval and escalates. An emergency alone grants no permission." FR-32 table: "Approve any other rollback — A Nightshift team engineer, plus the customer's approval".

**Code fixes (FR-44):** an Orvex engineer reviews, "approves or rejects the patch"; customer must authorise engineer access or "the patch is rejected". Then FR-21 applies.

**Routing (FR-12):** customer-only approval → "goes only to the customer"; also needs Orvex → "goes to the Orvex Nightshift team as well"; "Either way, Orvex receives a signal whenever the customer confirms something." Nightshift team "not called or alerted for problems handled by safe repairs".

---

## B. User journeys (steps → surfaces)

**UJ-1. "The shop owner is warned hours before checkout fails."** (FR-8–11, 21, 25)
1. Night: checkout memory grows; trend becomes real risk (FR-9) → alert to owner (+ Orvex support "if the contract says so").
2. Message: checkout still works, memory runs out "in about 4 hours", cause "not confirmed yet", proposes fix; "If nobody answers, Nightshift keeps watching and changes nothing that is not already authorised."
3. Owner approves → apply, verify, undo if not working. 4. Checkout never fails.
Surfaces: notification/alert → incident explanation → approval flow → action history (+ morning summary). Note (validation): doesn't say if the fix is risky (if so, Orvex approval also needed).

**UJ-2. "Cris approves a rollback while checkout is failing."** (FR-11, 13, 14, 21, 25)
1. Checkout failing; critical → phone call (FR-13). 2. "he opens the approval request in the portal". 3. Plain-words explanation + proposed rollback; Cris approves. 4. Rollback done; recovery confirmed after check. 5. "the action and his approval are in the record and the morning summary".
Edge: risky rollback → also Orvex technical approval, "so Cris is told that Orvex is checking it".
Surfaces: phone call → approval flow (portal; customer, phone-usable [INFERRED from Amine's wish]) → pending-Orvex state → action history → morning summary.

**UJ-3. "Josh approves a ticked risky repair."** (FR-11, 14, 21, 22, 23, 25, SEC-1)
1. Memory creep, single replica; repair "restarting the only replica" = risky; customer ticked it → needs only Orvex technical approval.
2. Josh "gets the request in Slack or the portal and signs in". Sees "the facts from the rule-based checks (memory trend, time to impact) separately from the AI's explanation, plus the customer's tick and the repair's safety conditions."
3. Approves → "Nightshift re-checks the conditions, restarts the replica, verifies that the service recovered, and records everything." 4. Customer sees it in morning summary.
Edge: no answer → "the repair waits, Nightshift alerts again, and a backup engineer can step in. Nothing runs on silence."
Surfaces: Orvex approval flow (desktop) → action history; customer morning summary.

**UJ-4. "Samira reads the night's summary."** (FR-16, 21, 34)
At 9 AM opens morning summary: "Checkout recovered at 2:25 AM after the rollback you authorised." (pre-ticked). Resolution: "knows what happened overnight without having been woken up."
Surfaces: morning summary (customer) → links into action history / incident explanation [INFERRED]. Channel/time zone of summary undefined (validation Low).

**UJ-5. "Josh handles one big problem across 300 clusters."** (FR-6, FR-32; also FR-47)
1. "one consolidated urgent alert about a single fleet-wide problem affecting 300 clusters". 2. Reviews evidence and impact; checks proposed solution "and which approvals it requires". 3. Approves. 4. "watches the result as the clusters recover."
Edge: customers with pre-authorised rollback policy → rollback runs if safety conditions pass; others "wait for each customer's approval" (danny-qa follow-up #1 open).
Example alert (FR-32, "to feed the UX wireframes"): "**Quornex Fleet: correlated update failure.** Critical. / 300 affected clusters · 1 fleet-wide problem · suspected update: v2.4 / Fleet action: pause the rollout, preserve the cluster reports, notify the on-duty engineer, and investigate the common cause."
Surfaces: Orvex fleet dashboard → fleet incident explanation → (batch) approval → fleet action history/recovery progress; per-customer approval flows.

---

## C. Requirements by surface

### C1. Dashboard / fleet view
- FR-15: "Each cluster has its own dashboard, reached through the Quornex portal." "A customer sees all their clusters and can combine them in one dashboard; the combined view uses only sanitised information from each cluster (PRIV-5)." "The customer can watch their app's health live." "**Orvex has grouped dashboards per 100 clusters**, because a single view of 10,000 clusters is unreadable."
- FR-12: "Every problem in the customer's clusters is visible to the customer, who has a full view of them." "Visible does not mean notified."
- FR-9: prediction with nothing useful to do → "goes to the dashboard and the morning summary, not to an alert". FR-13: "Dashboard and morning summary — Everything else".
- FR-14: "Every problem that needs a person first appears on a **Nightshift monitoring page**" (relation to FR-15 dashboards undefined — validation Medium).
- FR-10: warnings updated when time/risk changes, withdrawn automatically, "explains why the warning changed".
- FR-5 / FR-7: reports "openly what it cannot see"; **monitoring coverage report** per cluster; **limited-visibility mode**.
- FR-6: Fleet sees per-agent liveness ("I'm alive") incl. management agent; if control cluster down "Fleet still sees which workload clusters are alive".
- FR-32: consolidated alert, "not 300 separate ones"; Fleet "stops the update immediately"; "Risky repairs wait"; "The affected clusters' reports are preserved".
- FR-48: Fleet multi-tenant; "one customer's information is never visible to another customer"; Fleet holds only "approved, sanitised information".
- NFR-1 scale: 10,000 clusters; ~250 problems/night fleet-wide, up to 500 bad night.
- FR-28 state: after a harmful repair, "stops further automatic repairs on that cluster, and calls a person" → a "repairs stopped" cluster state [INFERRED]; no resume path defined (validation L-7).
- Not in PRD: "severity" as a defined scale; explicit "data freshness/last updated" on dashboards; mobile layout.

### C2. Incident explanation
- FR-11 (every message about a problem): understandable by non-expert; evidence-based; "says so when the cause is unknown". Must state: "the current state, and the impact on the service"; "the time to impact, for a prediction"; "whether the cause is confirmed, and if not, what is known and what is not"; "what Nightshift did, or the fix it proposes"; "for a request, what happens if nobody answers". "a few sentences anyone can follow".
- "the facts from the rule-based checks are shown separately from the AI's wording (SEC-1)".
- Canonical example: *"Your checkout service is using more memory than usual. Purchases still work, but at this rate memory runs out in about 4 hours and checkout may become unavailable. We haven't confirmed the cause yet. We suggest [fix]. Do you approve? If you don't answer, we'll keep watching and won't change anything."*
- FR-19: incident catalogue / unknown problems: "does not repair. It explains with the evidence it has, states its uncertainty, and escalates."
- FR-20 hardware: Mitigate / Report uncertainty ("states what it observed, the possible causes, what it cannot tell, and what would tell them apart") / Escalate to the customer ("what failed, the impact, what to ask the hardware provider, and the evidence") / Escalate to hardware provider "only through the customer" — Nightshift "prepares the evidence for the customer to send". Same for EKS provider. Mitigated fault "stays open until the customer confirms the hardware is fixed and Nightshift has checked". → needs "customer reports hardware fixed" action [INFERRED].
- FR-3 silent node: network card / power loss / node crash / network outage, or uncertainty. FR-7 table: "Report the node unreachable; root cause unknown"; "Recommend manual customer intervention".
- FR-16 morning summary: problems, fixes, anything unusual, Nightshift's and app's activity; for risky-repair problems "the full timeline from the first thing noticed"; recurring patterns (e.g. "a 3 AM traffic peak"); "authorised repairs that succeeded".
- SM-5: explanation measured on FR-11 parts present, later correctness, customer clarity → feedback control [INFERRED].

### C3. Approval flow
- Channels (FR-14): "Slack and the Quornex portal". "A phone call only notifies; the approval itself is given in Slack or the portal, by an authenticated person." Request explains problem as FR-11 and "says what happens without an answer: Nightshift keeps watching, and changes nothing that is not already authorised".
- Approval (Glossary): "a yes given by an authenticated person at the time, for one repair"; "**single-use and tied to the exact repair, target, catalogue version and evidence shown**".
- SEC-1: "Approval requests show the facts from the rule-based checks separately from the AI's wording." "Model responses are treated as untrusted."
- Risk classes / approvers: table in A. Dangerous adds "a recovery plan reviewed before the repair runs" (reviewer not named — validation SEC-R2-27).
- FR-22 validity:
  - Tick "stays permitted until the customer unticks it"; "tied to the repair's version: if a release changes the repair's action, conditions or risk level, the customer must tick it again."
  - "An approval given on request is valid for that one time only. If the problem happens again, or another problem appears, a new approval is needed."
  - "Right before every run, Nightshift re-checks the repair's safety preconditions… If something has changed, it does not run and Nightshift asks again. **There are no timers to manage**."
  - Executor re-checks authorisation: "the tick or approval is still valid, has not been revoked or unticked, and the customer's mode still allows the repair. If not, the repair does not run."
- FR-23 silence: "silence grants no new permission." Authorised repairs (ticked / last-resort) may still run "if its conditions pass". Engineer doesn't answer in time → "the repair waits; Nightshift keeps watching, alerts again, and calls if the problem becomes critical." "[Possible feature, Amine] For dangerous cases, Nightshift calls a member of the Orvex Nightshift team."
- FR-27: "a previous approval never automatically approves the next or any other repair"; next repair auto only if safe; else Orvex technical approval (+ customer's if unticked).
- FR-26: repairs ranked; "Nightshift always tries the safest repair expected to work first".
- FR-29 coordinator: no conflicting repairs on same target → "waiting for another repair" state [INFERRED].
- FR-31: after crash, "if the state is uncertain, it asks a person".
- Addendum (handed to security review/architecture, not PRD reqs): "render the action and target only from structured data, never from AI text; neutralise links and names an attacker controls; define approver roles, step-up authentication and how Slack identities map to customers; require two different people where two approvals are needed".

**Settings checklist / advance permission (no UJ covers it):**
- Glossary: customer "ticks, in a settings checklist, the repairs Nightshift may run… once, from the repair catalogue". "The checklist is in the settings for all customers."
- Settings items present across PRD: mode (alert-only / approval-enabled, SEC-7); ticks per repair with risk level, dangerous not tickable (FR-21); re-tick after version change (FR-22); last-resort tick (FR-24); delegation scope + revoke (FR-21); read scope "the infrastructure only, or also their app and its code" — "Permission to read never means permission to change" (FR-21); app monitoring opt-in (FR-8); code-fix opt-in + separate hosted-model consent, withdrawable (FR-43); engineer access authorisation for code-fix review (FR-44); maintenance policy + rollback policy (FR-47); limited-visibility acknowledgement at installation (FR-7). SEC-7: "changes are recorded and notified".
- Customer production (Glossary): change "needs the customer's advance permission (a tick in the settings checklist) or the customer's approval per action".

### C4. Action history / audit
- FR-33: "Everything Nightshift reads and changes is recorded where the customer can see it." Reads: "what was accessed, when, why and by whom, without copying customer data into the record".
- **FR-34 record per repair:** "the problem and its evidence, the repair and its risk level, who permitted it (ticked, or approved at the time, by whom and when), the result of the verification, and any rollback." Unapproved changes countable; target 0 (SM-4).
- FR-35: agent "can add to it but cannot change or delete entries".
- FR-36 other records: harmful repairs ("every case is recorded and traced"); prediction outcomes; monitoring coverage report; "The signal to Orvex whenever the customer confirms something"; "Repair progress, for crash recovery".
- FR-25: verify via catalogue entry; undo if didn't work and can be undone. FR-28: auto-rollback what it can on harm.
- FR-47: "Updates and rollbacks are recorded and visible to the customer like any other change".
- FR-43 / PRIV-7: every code transfer "recorded where the customer can inspect it"; "a record of exactly what left the cluster, which the customer can inspect".
- Harmful repair (Glossary): "service or cluster is worse than before it ran… as shown by the health checks before and after"; "did not work" counted separately (SM-2, SM-3) → three outcomes: worked / did not work / harmful [INFERRED from definition].
- Validation M-1 (unfixed): FR-34 has no field for last-resort, maintenance policy, rollback policy, "on behalf of" delegated approvals.

### C5. Notifications / alerts
- FR-13 levels: **Phone call** "Only for critical problems: an important service such as checkout or a database is failing, or there is strong evidence it is about to fail"; **Alert** "A problem becomes a real risk and needs a decision (see FR-9)"; **Dashboard and morning summary** "Everything else".
- FR-9 four factors: Time to impact, Confidence, Criticality, Actionability ("required for every alert").
- FR-12 routing (see A). Orvex support told "when the customer's contract says so".
- FR-32: "one consolidated urgent alert".
- FR-21: customer "notified of every approval given on their behalf". SEC-7 settings changes "notified".
- Who designates critical services / call list: undefined (validation Medium).

---

## D. Freshness, connectivity, disconnected clusters, degraded modes
- FR-2 heartbeat per node; "[OPEN] How long a heartbeat may be missing before it counts as missing" (Q8).
- FR-4: checks "the agent's heartbeat, and the freshness of its data"; independent checker detects "a missing heartbeat or stale data"; failures open a **"monitoring failure case"** (term not in Glossary).
- FR-5 limited visibility: "reports openly what it cannot see… and reports with the evidence it collected".
- FR-6 three levels; Fleet = "external watchdog"; every agent reports alive directly to Fleet.
- FR-7 table: OOB available → full; missing → **Limited-visibility mode**; silent node w/o OOB → "Report the node unreachable; root cause unknown".
- §5.7 / NFR-5: "Every Nightshift agent must keep operating locally when the management agent, the customer control cluster, or the network connection to them is unavailable." Single-cluster customer: agent "works alone, connected only to Quornex Fleet" [DESIGN ASSUMPTION].
- FR-29: local repairs keep working when central coordination unavailable; multi-cluster repairs "wait while it [management agent] is unavailable".
- SEC-8: executor and gateway in-cluster → "enforcement keeps working when the cluster is cut off".
- NFR-4: "If Nightshift stops, the customer's workloads keep running… Quornex Fleet notices the silence."
- NFR-7: "[OPEN] Numeric targets" for warnings.
- PRIV-2 strict mode: "only the time and type of a problem leave" → degraded explanation detail for max-privacy customers.
- Addendum (architecture input): "**Stale monitoring:** pause automatic repairs while Nightshift's own data is stale (adversarial H-5)"; "**Working without a model:** the core loop (detect, check, act, verify, record) works when no model is available (judge H6)" → template explanations [INFERRED from validation M-16].
- Not in PRD: how a dashboard displays stale/disconnected state, "last updated" timestamps, offline approval behaviour (validation H-2 proposal: offline "nothing that needs a fresh approval runs" — not adopted in PRD).

---

## E. Privacy/security constraints on display
- PRIV-1: private data stays in its cluster, "even between clusters of the same customer".
- **PRIV-2: applies to "the portal, dashboards and the morning summary", "notifications (Slack, phone)", Fleet, hosted model.** "Raw data and secrets never leave the cluster; only approved, sanitised information does." "Private values are replaced by placeholders such as `<email>`." Strict: "only the time and type of a problem leave".
- PRIV-3: per channel, Orvex-owned list of allowed fields, recipients, destinations; "anything else is blocked". → each surface shows only allowlisted fields [INFERRED].
- PRIV-4: mandatory outbound check on "every whole line about to leave, by every channel".
- PRIV-5: customer combined dashboard uses only sanitised info per workload cluster.
- PRIV-7: customer-inspectable record of exactly what left; planted-secret test wording: "no planted secrets escaped in these tests", "never as proof of 100% privacy"; outside audit.
- FR-48: Fleet multi-tenant; no cross-customer visibility. Orvex grouped views of 100 clusters mix customers → validation SEC-R2-23: grouped views show only PRIV-3 fields (not in PRD).
- Customer-specific entry: "only that customer can access or execute it".
- SEC-1: untrusted log text/model output; facts separate from AI wording.
- SEC-7: only authenticated customer administrators change settings.
- SEC-9: approvals/ticks/delegations/policies "are signed", verified in-cluster; "a compromised portal, Slack integration or Quornex Fleet cannot forge them". → approve action involves signing by the person [INFERRED].
- Validation L5 (unresolved): Orvex engineer approving sees only sanitised evidence; whether enough, and how in-cluster evidence is viewed, unstated.
- Validation SEC-R2-25 (not in PRD): calls/messages never ask for credentials.

---

## F. Glossary — use verbatim
Fault ("an underlying technical problem"), Failure ("a service failing"), Incident ("a service disruption experienced by users"), Problem ("any fault, failure or incident"), Supported problem, Incident catalogue ("supported problems whose fix is not yet tested or confirmed"), Repair catalogue ("problems whose fix is known"), Customer-specific entry, Risk level (Safe / Risky / Dangerous), Safe repair ("will not interrupt the customer's service or lose data"), Risky repair ("can interrupt a service or reduce redundancy"), Dangerous repair ("side effects could corrupt data, create an opening for injection or cause loss of access"), Harmful repair, Disk cleanup, Prohibited action ("not a risk level but a rule"), Customer production, Customer contract, Alert-only mode, Approval-enabled mode, Advance permission ("ticks… in a settings checklist"), Approval, Orvex technical approval, Last-resort condition, Maintenance policy, rollback policy, Out-of-band management, Limited-visibility mode, Monitoring coverage report, Customer hardware, OMK, Quornex, Hosted Kubernetes, Quornex Fleet, Customer control cluster, Workload cluster, Nightshift agent, Nightshift management agent. Other recurring terms: morning summary, monitoring failure case, Nightshift monitoring page, Quornex portal, mitigate / report uncertainty / escalate, consolidated urgent alert, Orvex Nightshift team, Orvex support, tick / untick / ticked.
Naming caveats (validation): "incident catalogue" holds non-incidents (L2); "failure catalogue" (deliverable) vs incident/repair catalogues (L-2); "Nightshift engineer"/"Nightshift team engineer"/"Orvex Nightshift team" interchangeable.

---

## G. Open questions / pending Danny affecting UX
- PRD §10 triage: "none of the remaining items blocks UX or architecture" (validation H-15 disputes this for Q1/Q2: they "shape the approval UX flows").
- **Q1** who approves risky changes to OMK and Quornex themselves (danny-qa follow-up #1) → FR-47 maintenance/rollback policy UI is a proposal.
- **Q2** does Orvex technical approval on top of customer approval fit Danny's model (danny-qa #8; Exchange 5 Q1 pending) → the dual-approval states depend on it.
- **Q3** PRIV-1 no data between a customer's clusters → affects combined customer dashboard.
- Q6 trusted hosted models; Q7a code-fix hosted consent.
- **Q8** heartbeat/timing targets (FR-2, NFR-7) → staleness thresholds on dashboards.
- **Q14** 30-minute last-resort threshold.
- FR-47 entirely "our proposal, pending Danny's confirmation"; Section 7 "trusted hosted model" rules pending Danny.
- [DESIGN ASSUMPTION] Quornex Fleet internals; single-cluster customer has no control cluster.
- FR-23 "[Possible feature]" call an Orvex team member for dangerous cases — undecided.

---

## H. CONFLICTS / GAPS: Amine's UX wishes vs PRD

1. **Approval expiry — CONFLICT.** Amine: "re-ask approval if … approval expires". PRD FR-22: "There are no timers to manage"; approval "valid for that one time only"; Glossary "single-use and tied to the exact repair, target, catalogue version and evidence shown". No expiry exists in the PRD. Validation M-4 ("give approvals a maximum age, set per risk level") and SEC-R2-19 ("Every approval has an expiry (proposed: minutes, set per risk level)") flag this; not applied. Also FR-23 "If they do not answer in time" has no defined time (validation M-2: contradiction with "no timers").
2. **Material change → re-ask — PARTIAL.** Amine: "re-ask approval if action/conditions materially change". PRD FR-22: preconditions re-checked; "If something has changed, it does not run and Nightshift asks again"; executor re-checks tick/approval/mode; tick must be re-given if "a release changes the repair's action, conditions or risk level". Gap: "materially" undefined; which evidence fields bind is undefined (validation M-4: "define which evidence fields are binding (problem ID, target, repair version, severity band) and which may drift"). Customer not notified when ticks lapse on release (validation M-15, unfixed).
3. **Dangerous repairs cannot use delegated customer approval — ALIGNED in FR-21** ("Delegation never covers dangerous repairs: the customer always approves those personally"), **but Glossary "Approval" omits the exception** ("The customer approves, or Orvex support if the customer delegates to them"; validation L-3). Also: dangerous repairs cannot be ticked or covered by last-resort (FR-21, FR-24). Validation SEC-R2-05 proposed "Dangerous repairs are approved only in the portal" (not Slack) — not in PRD; relevant to phone approvals.
4. **"Never bundle unrelated actions" — NOT STATED explicitly.** PRD support: approval is "for one repair"; FR-27 "a previous approval never automatically approves the next or any other repair". Tension: UJ-5 "he approves" one fix across 300 clusters (validation M-3: "one approval for 300 targets… breaks the definition"; SEC-R2-05: "One click never authorises more than one customer"). Batch approval for fleet events undefined.
5. **Buttons "Approve this repair" / "Reject" — GAP.** PRD names no button labels and defines no outcome of an explicit rejection for repairs (only "approves or rejects the patch" for code fixes, FR-44). What happens after Reject (keep watching? escalate? offer next repair?) is not specified. [INFERRED: likely treated like no answer — "changes nothing that is not already authorised" — but unconfirmed.]
6. **"Customer approved; waiting for Orvex review" — ALIGNED in substance, different wording.** PRD UJ-2: "Cris is told that Orvex is checking it". PRD term is "Orvex technical approval", not "Orvex review". FR-12: Orvex gets a signal "whenever the customer confirms something". Missing-approval display not specified as a requirement.
7. **Risk level, expected interruption, recovery plan on every approval — PARTIAL.** Catalogue repair defines "the action, its safety preconditions, risk level, authorisation, verification and rollback" (Glossary). No "expected interruption" field; only implied by risk definitions (safe "will not interrupt", risky "can interrupt a service or reduce redundancy"). "Recovery plan" in PRD is required only for dangerous ("a recovery plan reviewed before the repair runs"); for others the PRD term is "rollback". Who reviews the recovery plan is unnamed (SEC-R2-27); validation M-7: recovery plan should be pre-tested from the catalogue, not written at the time (FR-17 forbids improvisation).
8. **Problem, customer impact, exact repair and target — ALIGNED.** FR-11 "the current state, and the impact on the service"; Glossary approval bound to "exact repair, target". Addendum: render "action and target only from structured data, never from AI text".
9. **Verified evidence separate from AI explanation — ALIGNED, wording differs.** PRD: "the facts from the rule-based checks are shown separately from the AI's wording" (FR-11, SEC-1). Validation SEC-R2-03 proposed label "AI explanation, unverified" and no links/markup in AI text (in addendum as input, not PRD). Note: "verified evidence" is Amine's wording; PRD's is "facts from the rule-based checks".
10. **Approvals still required — ALIGNED** with FR-21 table and FR-12 routing; UJ-5 "checks… which approvals it requires".
11. **Action history shows progress and verification result — PARTIAL.** FR-34 includes "the result of the verification, and any rollback". Progress appears only as "Repair progress, for crash recovery" (FR-31, FR-36) — not stated as customer-visible; UJ-5 "watches the result as the clusters recover" implies live progress for Orvex.
12. **Dashboard first 5 s: impact, severity, affected clusters, pending approvals, currency — PARTIAL.** FR-15 defines dashboards (per cluster, combined customer, Orvex per 100 clusters) but not their content. "Severity" is not a PRD-defined scale (closest: FR-13 levels phone/alert/dashboard; FR-9 "Criticality"; FR-32 example label "Critical"). Pending approvals on dashboard: FR-14 "Nightshift monitoring page" only. **Stale/disconnected obvious: no display requirement**; PRD only has FR-4 freshness detection, FR-5 "reports openly what it cannot see", FR-6 Fleet liveness, coverage report.
13. **Two experiences (Orvex desktop fleet / customer simpler + phone approvals) — NOT IN PRD, no conflict.** PRD has no device/mobile requirement; approvals via "Slack and the Quornex portal"; phone *call* "only notifies". Orvex grouped views "per 100 clusters" (FR-15) — fleet dashboard must respect grouping. **Gap: Orvex support** (third user type, delegated approver) is not in either experience as described; validation also notes no UJ for Orvex support.
14. **Settings checklist (advance permission) not in Amine's four surfaces** — yet UJ-3/UJ-4/UJ-5 depend on ticks/policies; validation's High finding "No journey shows the customer configuring permissions" is still open. Wireframing ticks/delegation/mode may be needed or explicitly out of scope.
15. **Silence behaviour not in Amine's list** — PRD requires every request to state it (FR-11, FR-14): "If you don't answer, we'll keep watching and won't change anything."

---

## I. Validation-report findings still relevant to UX
Already applied to PRD (no action): harmful repair defined; FR-41 tuning now catalogue repairs; default mode/checklist defined; SEC-8/SEC-9 added; authorisation re-check (FR-22); UJ-2 persona renamed Cris; delegation scope/revoke/notify.
Still open (UX-relevant):
- **No settings/permissions journey** (Shape fit, High): mode, ticks with risk levels (dangerous not tickable), re-tick after release, last-resort tick, delegation scope/revocation, read scope, two code-fix consents, limited-visibility acknowledgement.
- **No Orvex support journey**; delegated approval never exercised (Medium).
- **Approval expiry** (M-4, SEC-R2-19) and binding evidence fields; "in time" undefined (M-2).
- **Fleet batch approval** (M-3; SEC-R2-05 per-cluster authorisation).
- **Approval surface hardening** (SEC-R2-03, in addendum): structured-only action/target/risk/impact; AI text escaped, no links; label "AI explanation, unverified"; never ask for credentials.
- **Approver identity** (SEC-R2-05, in addendum): roles per customer, MFA/step-up for risky/dangerous, Slack identity → roster, two different people, dangerous only in portal (proposal).
- **Tick lapse notification** on release, show lapse on dashboard (M-15).
- **Tick scope** (clusters/namespaces/services) undefined (SEC-R2-20).
- **Critical services + call list** designation undefined (Medium).
- **FR-28 stop**: no resume path, who lifts it; scope to safety domain (Medium, L-7).
- **Morning summary**: no time basis or channel (Low).
- **"Nightshift monitoring page"** vs FR-15 dashboards undefined; "monitoring failure case" undefined (Medium).
- **Orvex side of last-resort**: no actor, no screen (Medium); recovery-plan reviewer unnamed (SEC-R2-27).
- **FR-34 missing permission sources**: last-resort, maintenance/rollback policy, "on behalf of" delegation (M-1).
- **Stale monitoring** → pause automatic repairs (H-5, addendum).
- **No-model / max-privacy** → template explanations; summary states which mode produced each message (M-16, H6).
- **Sanitised evidence for Orvex approvers** may be insufficient; how to view in-cluster evidence (L5).
- **Grouped Orvex views** mix customers → only PRIV-3 fields (SEC-R2-23).
- **Orvex staff reads** of customer data should be recorded where customer sees them (SEC-R2-17).
- **Customers cannot see/narrow outbound field lists** (SEC-R2-15, H-9) — possible customer-facing privacy view.
- **Rollback risk level** undefined; schema-migration risk (H-14) — affects UJ-2/UJ-4 rollback approval display.
- **Approval latency vs 99.9%** (judge H2) — approval UX speed matters; last-resort doesn't cover failures already in progress.
- **UJ-1 protagonist unnamed**; UJ-1 doesn't say if fix is risky.
- **Glossary "Approval" lacks dangerous-delegation exception** (L-3).
