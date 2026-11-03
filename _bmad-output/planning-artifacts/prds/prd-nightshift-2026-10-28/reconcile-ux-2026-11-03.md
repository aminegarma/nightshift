# Reconciliation: UX run of 2026-11-03 against the PRD Update of 2026-11-03

Read-only check. Nothing in `prd.md` or `addendum.md` was edited.

**Inputs:** `ux-designs/ux-nightshift-2026-10-31/.working/open-items-2026-11-03.md` (section 2, the PRD queue; section 1, open items for architecture), the UX `.memlog.md` entries from "UX run resumed (2026-11-03)" to the end (later entries win), and `EXPERIENCE.md` ("Authorisation & approvals", "Privacy & outbound channels", "State Patterns › Approval validity / Decisions", plus the surface states and Voice and Tone rules that state product behaviour).
**Targets:** `prd.md` and `addendum.md` as updated, the two diffs of this Update, `update-notes-2026-11-03.md` and the PRD `.memlog.md` entries of 2026-11-03.
**Statuses:** Captured · Captured (note) · Missing · Contradicted · Rightly UX (layout, wording, interaction, or a detail the UX already hands to architecture).
**Not covered:** the deferred review findings in `open-items-2026-11-03.md` section 3. They are still open product questions for the next UX Update, not decisions yet.

## 1. UX → PRD: queued items and UX product rules

### 1a. The PRD queue (open-items section 2)

| # | Item | Where in the PRD | Status | Note |
|---|---|---|---|---|
| Q1 | Fleet heartbeat required; strict no-outbound can't use managed Fleet; drop the two "status unknown" texts | FR-6, NFR-4, PRIV-9 lead and "Without the heartbeat", Glossary "No outbound data", addendum "For the UX" | Captured (note) | FR-15 still says "If the customer permits no outbound channel…", which can't happen in managed Fleet now (see P1). |
| Q2 | Onboarding defaults; confirming the channel screen is the explicit permission | PRIV-9 "At onboarding", Section 10 item 22 | Captured (note) | **Qualitative idea dropped:** the UX record says Amine chose pre-ticked boxes *knowing* a pre-ticked box may not count as "explicitly permits". The PRD states the rule but not the known risk or trade-off. Worth one line in PRIV-9 or Section 10 so a later reviewer doesn't treat it as an oversight. |
| Q3 | Approval validity is a catalogue field; close item 18 | Glossary "Repair catalogue", FR-22, item 18 moved to "Answered and decided" | Captured | "Orvex sets the value when testing the entry" matches O-2. |
| Q4 | An unanswered request doesn't expire: it stays open with current evidence, is re-issued on a material change and is withdrawn if the problem resolves | FR-22 bullet 3 | Captured | FR-23 needed no change. FR-34 now says "expired approvals". |
| Q5 | Manual repairs: time window, the performer re-runs the pre-start check, the recovery plan is reviewed by the Orvex engineer who gives technical approval | FR-52 "Before the person performs it" | Captured (note) | "Outside it, the approvers are asked again" doesn't carry the UX rule that the window limits only when work may **start** (see U12 and P4). |
| Q6 | Addendum statuses add "Waiting for Orvex" and "Manual repair needed"; remove the heartbeat texts | addendum "For the UX" | Captured | |
| Q7 | Carried over: FR-14 recovery plan (rollback only when certain); request usable on a phone; FR-15 freshness, never stale-as-healthy; FR-32 one Orvex approval per problem group, recorded per cluster | FR-14, FR-15, FR-32 | Captured (note) | FR-32 has per-cluster recording, re-checks and waves, but not the frozen target set (U10). "Problem group" isn't defined in the Glossary. |
| Q8 | A text message with every phone call; a text instead of a call on request | FR-13, FR-14, PRIV-2, PRIV-9, Glossary "Approval" | Captured (note) | 3.1 still lists "phone calls, alerts, dashboards…" without text messages. Trivial. |
| Q9 | Turning off portal access: blocks new remote approvals, revokes nothing silently, approvals already given stay valid | PRIV-9 "Without the portal" | Captured | Amine confirmed the UX proposal in this Update. The UX spine still marks it as a proposal to confirm (P11). |
| Q10 | Withdraw until the repair starts; undo Reject until the other approvers are told; the server orders decisions; the history keeps every step | FR-22, FR-50 | Captured | |
| Q11 | Statuses Work in progress, Mitigated and Problem still there | addendum "For the UX" (final status sets) | Captured | The addendum sets match EXPERIENCE.md exactly: 5 incident statuses, 13 repair statuses, 3 severities. |

### 1b. Other UX decisions that state a product rule

| # | UX rule (source) | Where in the PRD | Status | Note |
|---|---|---|---|---|
| U1 | Policy versions: changes within the agreed scope apply; widening changes stay off until accepted; never "the old version stays in force" (memlog, FR-51 correction) | FR-51 "Changes", Glossary | Captured | |
| U2 | Severity → FR-13 level: Critical = call (+ text), only when failure is happening or imminent; Warning = alert when a decision is needed; a prediction like UJ-1's is Warning | FR-13, UJ-1 ("alerts"), addendum severity set | Captured | |
| U3 | A failed or inconclusive pre-start check blocks the work, manual repairs included; a fresh approval can't override it | FR-22, FR-52 | Captured | |
| U4 | A valid tick supplies the customer's permission; Orvex technical approval stays separate; dangerous repairs need the customer personally, never a delegate | FR-21, FR-52 | Captured | |
| U5 | Switching to alert-only cancels approvals given but not used; they are recorded as Cancelled **and the approvers are told** | FR-21 | Captured (note) | The PRD says they are cancelled and recorded, but doesn't say the approvers are told. |
| U6 | The last-resort no-answer line appears only when every required permission exists and the checks pass; it never overrides a rejection, alert-only mode or the dangerous/manual rules | FR-24, FR-50 Scope, Glossary "Alert-only mode", FR-52 | Captured | |
| U7 | Several people deciding: a Reject by any required approver blocks; **among a customer's administrators the first decision counts**, but anyone authorised can still withdraw or reject before the repair starts | FR-50, FR-22 (server ordering, record) | Missing | Blocking and ordering are captured. The rule that the first decision counts among several administrators isn't in the PRD. It could also go to architecture with O-5. |
| U8 | Separate, role-labelled approvals; where two are required they come from two different people | addendum "Approval surface" (handover only) | Captured (note) | It is only a handover item for architecture and security, not a PRD requirement. That is acceptable, since the UX also treats the mechanism as O-5. |
| U9 | A decision is bound to the version shown and validated again on the server; a re-issued request voids approvals given on the old version | Glossary "Approval" (tied to repair, target, catalogue version and evidence shown), FR-22, SEC-8/9 | Captured | |
| U10 | Fleet batch: **targets frozen at the click and displayed; clusters added later need a new approval** (memlog review fix 9) | FR-32 (new bullet) | Missing | This is an authorisation-scope rule, not layout. Without it, "one approval per problem group" could be read as covering clusters that join the group later. |
| U11 | Orvex approves the candidates, but each cluster waits for its customer's permission and its own checks; clusters without Fleet reports are excluded and keep their local permissions | FR-32, UJ-5 edge case, PRIV-9 "Without Fleet reports" | Captured | |
| U12 | Manual window: it **limits when work may start**. If work can't start inside it, the approvers are asked again. Work in progress when the window ends is finished or recovered under the reviewed plan, never abandoned (accepted by Amine as a design proposal, memlog review fix 3) | FR-52 | Missing | **Qualitative idea dropped.** FR-52 says only "outside it, the approvers are asked again". |
| U13 | A recovery-plan review that materially changes the plan asks the customer again | — | Missing | The approval binding (Glossary) doesn't list the recovery plan, so nothing in the PRD forces a new approval. |
| U14 | During manual work the coordinator blocks conflicting repairs on the target but **never necessary recovery actions** | FR-29 (covers changes made by people) | Captured (note) | The exception for recovery actions isn't stated. |
| U15 | Mitigated: the problem stays open until the hardware is replaced and Nightshift's own health check passes; the customer's confirmation alone isn't enough | FR-20, FR-52 | Captured | |
| U16 | "Who permitted it" sources: tick · management policy **(version)** · approved at the time (by whom, when, on whose behalf) · **last-resort condition** | FR-34 | Missing | FR-34 lists only tick, policy and approval at the time. The last-resort condition and the policy version are missing. This gap predates this Update, but the UX now depends on it. |
| U17 | Only administrators change settings, including **Accept this change** (policy), source-code consent and Dispute | SEC-7 | Missing | SEC-7's list doesn't include accepting a policy change (FR-51), source-code consent (FR-43) or disputing a classification (FR-21). |
| U18 | Every panel shows how current its data is; never a stale green or healthy words on stale data | FR-15 | Captured | |
| U19 | Orvex-only platform repairs are shown to the customer as information, without buttons | FR-12 routing | Captured | |
| U20 | Heartbeat fields explained at onboarding; source code off until the customer opts in | FR-6, FR-43, PRIV-6 | Captured | |
| U21 | Templates, not AI, write unlabelled lines: a version-1 design choice, not a SEC-1 rule | FR-11, SEC-1 | Rightly UX | |
| U22 | A confirmation sheet before every consequential decision | — | Rightly UX | The withdraw and undo rules behind it are in the PRD (Q10). |
| U23 | "What we're asking" summary; plain explanations on tap | FR-11, NFR-8 (intent) | Rightly UX | |
| U24 | Pause live updates; server-side safety checks stay live | FR-22 | Rightly UX | |
| U25 | After sign-in the pending request is preserved, never an unsent approval, and revalidated; accessible sign-in | FR-14, O-5 | Rightly UX | |
| U26 | Performer actions only for the named performer; the window is proposed by the performer | O-8, [ASSUMPTION] | Rightly UX | Architecture owns it. |
| U27 | O-1 to O-12 (freshness threshold, validity values, two approvals with one expiring, fleet waves, roles, rendering, in-cluster dashboard, performer authentication, support role, production signals, notification contents, brand) | addendum "For the architecture" (pointer), "Approval surface", H9 | Rightly UX | They are correctly left open, and the addendum points to them. |
| U28 | Keyboard support; WCAG 2.2 AA as an untested target | — | Rightly UX | |

## 2. PRD → UX: does the updated PRD contradict the final spines?

| # | Area | PRD text | UX spine | Status | Note |
|---|---|---|---|---|---|
| P1 | In-cluster-only dashboard | FR-15: "If the customer permits no outbound channel, their problems are visible only on an in-cluster dashboard" | "Portal and notifications not permitted → problems only on the in-cluster dashboard" (O-7); the heartbeat is required | Contradicted | Stale since the heartbeat became required. PRIV-9 "Without notifications as well" already has it right. Reword FR-15 to "neither the portal nor notifications". |
| P2 | UJ-1 climax | "Nightshift applies the fix, checks that it worked, and undoes it if it did not" | The UJ-1 repair is a restart, which can't be undone (FR-27); the UX UJ-1 says "where the repair can be undone" | Contradicted | The UX distiller resolved this on its side; the PRD journey still promises an undo. |
| P3 | UJ-2 edge case | "…so Cris is told that Orvex is checking it" | Voice and Tone forbids "Orvex is checking it" before anyone has looked; it uses "Waiting for Orvex technical approval" | Contradicted | Wording only, but it is the PRD's own journey text. |
| P4 | Manual window | FR-52: "The approvals cover a stated time window; outside it, the approvers are asked again" | The window limits the start; work in progress at the end of the window is finished or recovered, never abandoned | Contradicted (reading) | Read literally, the PRD could require re-approval or a stop in the middle of the work. Same gap as U12. |
| P5 | Statuses | addendum "Final statuses, owned by the UX EXPERIENCE.md" | State Patterns › Severity, statuses and risk | Captured | Identical sets. |
| P6 | Heartbeat states | FR-6: "No data since 02:10"; "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation" | Freshness and cluster connection; the old states are "Never shown" | Captured | FR-46 "clusters whose heartbeat Fleet cannot see" still makes sense for a stopped heartbeat. |
| P7 | Channel lists | PRIV-9: external AI, heartbeat, Fleet reports, notifications (Slack, call, text), portal | B6b: the same five, plus source code as a separate permission (FR-43) | Captured | "Fleet diagnostic reports" (UX) and "Fleet reports" (PRD) are synonyms. |
| P8 | Validity | FR-22, Glossary "Approval" | State Patterns › Approval validity | Captured | |
| P9 | Manual-repair lifecycle | FR-52, FR-20, FR-27, FR-34 ("manual repair reported done" + verification result) | Manual repair needed → Work in progress → Verifying → Succeeded / Mitigated / Problem still there; mapped to FR-34 | Captured | Apart from P4. |
| P10 | Policy acceptance after the FR-51 correction | FR-51 "Changes", Glossary, SEC-9 | B6b and Flow 6 step 7: "Off until you accept it"; the rest of the version applies | Captured | No PRD text left saying the last accepted version stays in force, except the sentence recording what was replaced. |
| P11 | Portal access turned off | PRIV-9: decided, confirming the UX proposal | Surface states: "[ASSUMPTION: proposal, to confirm]"; "pending PRD change N" markers throughout the spine | Captured (note) | The PRD is now ahead of the UX. Next UX Update: drop the assumption tag and the "pending PRD change" markers (changes 1–10 are all applied). |
| P12 | Recorded outcomes | FR-34: "Rejected requests and expired approvals are recorded" | Repair status → FR-34 table: "Rejected · Expired → recorded requests" | Captured (note) | UX row wording is stale; "Expired" now means an approval, not a request. |
| P13 | Repairs on an out-of-date cluster | NFR-5, SEC-8: local enforcement keeps working when the cluster is cut off; no PRD rule blocks repairs because Fleet lacks data (addendum H-5 covers Nightshift's own stale data, locally) | Freshness: "Repairs on an out-of-date cluster: shown as Blocked — no data from cluster since 02:10" (A5) | Contradicted (to check) | The console may claim "Blocked" for repairs that are in fact running locally under a tick or policy. Either the UX shows "Unknown", or architecture decides that H-5 pauses repairs and the console can know it. |
| P14 | Without the portal | PRIV-9: "no approval can be given…"; only safe ticked, policy and last-resort repairs run | Same rule in B6b and Surface states | Captured (note) | Shared open point: it isn't said whether Orvex-only technical approvals (given in the Orvex console, [ASSUMPTION] "the Orvex-side portal surface") are also blocked when a customer turns off its portal channel. |
| P15 | Non-goal "never through a channel the customer has not permitted" | 3.2, PRIV-9 lead ("accepted with the service") | Heartbeat required, "explained and accepted when you start the service" | Captured | |

## 3. Counts

- **UX → PRD (39 rows):** Captured 17 · Captured (note) 8 · Missing 6 · Contradicted 0 · Rightly UX 8.
  - Queue items alone (11): Captured 6 · Captured (note) 5.
- **PRD → UX (15 rows):** Captured 7 · Captured (note) 3 · Contradicted 5 (P1–P4 on the PRD side, P13 on the UX side, to check).

## 4. Suggested follow-ups

1. **PRD (small Update or polish):**
   - FR-52: the window limits the start, and work in progress is finished or recovered (U12, P4).
   - FR-52: a materially changed recovery plan asks the customer again (U13).
   - FR-32: frozen targets, and later clusters need a new approval (U10).
   - FR-15: reword "no outbound channel" (P1).
   - UJ-1 climax: undo only where possible (P2).
   - UJ-2 edge-case wording (P3).
   - FR-34: add the last-resort condition and the policy version as sources (U16).
   - SEC-7: add policy acceptance, source-code consent and Dispute (U17).
   - FR-50: first decision counts among administrators (U7).
   - FR-21: the approvers are told when alert-only cancels their approvals (U5).
   - FR-29: never block necessary recovery actions (U14).
   - PRIV-9 or Section 10: record the known pre-ticked consent trade-off (Q2).
2. **UX (next Update):**
   - Remove the "pending PRD change" markers and the portal-off assumption (P11).
   - Fix the "Rejected · Expired" row (P12).
   - Settle P13 ("Blocked" versus "Unknown" on out-of-date clusters).
3. **Architecture:** O-1 to O-12 as handed over, plus P14.
