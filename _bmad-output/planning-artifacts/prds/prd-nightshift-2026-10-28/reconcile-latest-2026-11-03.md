# Reconciliation: 2026-11-03 decisions vs prd.md, addendum.md, EXPERIENCE.md

Scope: `.memlog.md` entries from "FR-51 'Changes' and Glossary" to the end (later entries supersede earlier ones). Checked against `prd.md`, `addendum.md` (this folder) and `ux-designs/ux-nightshift-2026-10-31/EXPERIENCE.md`. Read-only; nothing else edited.

**Counts:** OK 29 · Missing 2 · Contradiction 1

| # | Decision (memlog) | PRD / addendum location | UX location (EXPERIENCE.md) | Status |
|---|---|---|---|---|
| 1 | FR-51 correction: clusters follow Orvex's current approved release; acceptance governs permissions, not staying on an old version; replaces 2026-11-02 rule | FR-51 "Changes"; Glossary "Agreed management policy" | Privacy & outbound › Agreed management policy; Voice & Tone Do/Don't; Flow 6 step 7; Surface states "Policy change pending" | OK |
| 2 | FR-51 scope = conditions no less restrictive; corrected steps still tested and reviewed; disputed = expanding; production-affecting change leaves policy, follows FR-21 | FR-51 "Changes" sub-bullets; Glossary; SEC-7 | Privacy & outbound › Agreed management policy | OK |
| 3 | Fleet heartbeat is a required service channel | FR-6; PRIV-9; NFR-4; Section 10 item 22 | Privacy & outbound table; Freshness "Heartbeat not permitted: never shown"; Flow 6 step 1; Anti-patterns | OK |
| 4 | D3: strict no-outbound not offered in v1 (limitation, non-goal) | 3.2 Non-goals; FR-6 "Strict no-outbound"; Glossary "No outbound data"; PRIV-9 "Without the Fleet heartbeat"; NFR-4 cleaned | Privacy & outbound table (Fleet heartbeat "No" column); Foundation (B6b wireframe string superseded) | OK |
| 5 | D2: Fleet reports, notifications, portal pre-ticked as service settings, not consent; administrator confirms, never installer; external AI opt-in; legal basis [OPEN] | PRIV-9 "At onboarding"; Section 10 item 23 + triage paragraph | IA "Onboarding channel screen"; Privacy & outbound "Service settings, not consent"; Flow 6 steps 2, 3, 6 | OK |
| 6 | Approval validity per catalogue entry (closes item 18) | FR-22; Glossary "Repair catalogue"; Section 10 item 18 | State Patterns › Approval validity; O-2 | OK |
| 7 | Unanswered requests don't expire | FR-22; FR-34 | Approval validity; Voice & Tone Do/Don't; UJ-1 failure | OK |
| 8 | Manual window limits when work may start; in-progress work finished or recovered, never abandoned | FR-52 "Before the person performs it", "Approvers and window" | Approval validity "Manual repairs"; Flow 7 failure | OK |
| 9 | Material change (incl. recovery plan changed in review) needs renewed approval from the relevant approvers, the customer where production is affected | FR-52 "Approvers and window" | Approval validity "Recovery-plan review": only "a review that materially changes it asks the customer again" (no "where production is affected" qualifier, no other relevant approvers); Flow 7 step 4 | Missing (partial in UX) |
| 10 | Performer re-runs pre-run check before start; recovery plan reviewed by the Orvex engineer giving technical approval | FR-52 | Manual-repair panel lifecycle; Authorisation table; Flow 7 | OK |
| 11 | Text message with every phone call; text instead of call | FR-13; FR-14; PRIV-2/PRIV-9; Glossary "Approval" | Foundation; Notifications; Privacy & outbound "Phone calls"; Accessibility | OK |
| 12 | Recovery plan and phone use in approval request | FR-14 | Approval card sections 6, Voice & Tone "Recovery plan"; Responsive | OK |
| 13 | Freshness on every dashboard, never stale as healthy | FR-15 | Freshness line, Stale panel, Freshness and cluster connection | OK |
| 14 | Group approval: one repair, one catalogue version, frozen set; per cluster; each target needs a valid unexpired approval; later waves can't reuse an expired one; never manual; customer permission still needed | FR-32; Glossary "Approval" exception | Authorisation › Fleet-wide; Approval validity; UJ-5; O-4 | OK (UX doesn't spell out "one catalogue version"; not contradictory) |
| 15 | Portal-off: ticks, policy and last-resort permissions are not revoked; given approvals stay valid; open requests visible only in-cluster | PRIV-9 "Without the portal" ("does not revoke") | Surface states "Portal access turned off": "not **silently** revoked" | Contradiction (wording weakens the rule) |
| 16 | Withdraw an approval until the repair starts; undo a reject | FR-22; FR-50 | Confirmation sheet; Voice & Tone "After Approve", "Reject result" | OK |
| 17 | D1: withdrawal, alert-only, untick take effect when the executor receives them; "Sent; not yet confirmed by the cluster"; both times recorded; validity caps life | FR-22 withdraw bullet; addendum "Revocation reaches the cluster" | Decisions "Revocation takes effect in the cluster"; Voice & Tone "Sent, not yet in effect", History; Settings row; Timeline entry | OK |
| 18 | With portal off, withdrawals, alert-only and settings stay possible on the in-cluster dashboard | PRIV-9 "Without the portal"; addendum "In-cluster dashboard" | IA in-cluster dashboard; Decisions; Surface states; O-7 | OK |
| 19 | Failed pre-run check blocks (incl. manual); fresh approval can't override | FR-22; FR-52 | Check table; Surface states "Manual: pre-run check fails"; Flow 7 failure | OK |
| 20 | D4 (override): inconclusive check → defined manual procedure with alternative evidence; record per condition; telemetry gap never waives; escalate if no safe procedure; authorisation and safety-check compliance reported separately | FR-22; FR-52 record bullet; addendum "Defined manual procedures" | Check table; Surface states "Manual: remote pre-run check inconclusive", "Manual: work outside the procedure"; Flow 7 failure | OK |
| 21 | Alert-only cancels pending execution authorisations; ticks and policy stay recorded but don't run | FR-21 | Surface states "Switch to alert-only…"; Authorisation › Alert-only | OK (UX doesn't restate that ticks stay recorded) |
| 22 | Part 2 item 2 (override): different people for customer and Orvex approval where both required (incl. delegated); Orvex approver may perform; no inferred performer/reviewer separation | FR-21 delegation bullet; FR-52 "Approvers and window"; addendum "Approval surface" | Authorisation "Separate, role-labelled approvals"; A3 IA; Approval validity "Recovery-plan review"; O-5 | OK |
| 23 | Independent reviewer is a deferred proposal, not a requirement | Absent from PRD requirements; addendum "From the review of the 2026-11-03 update" labelled "Deferred proposal, not a requirement" | Absent | OK |
| 24 | Last-resort 30 min stays an assumption; grants no extra permission; can't override a rejection | FR-24; FR-50 Scope; Glossary; Section 10 item 14 | Authorisation "Last-resort condition" ([ASSUMPTION]); Voice & Tone "No answer" | OK |
| 25 | Undo-reject: bounded window, length from the architecture; undo only reopens; others told when window ends | FR-50; Section 10; addendum "Undoing a rejection" | Confirmation sheet; Reject result; Authorisation › Reject; O-13 | OK |
| 26 | Stale-data wording "Current repair status unknown; last reported [status] at [time]", never implying unblocked | (UX-only rule) | Voice & Tone "Repair status on stale data"; Freshness "Repairs on an out-of-date cluster"; Foundation superseded strings | OK |
| 27 | "Pre-run check" as the one term | FR-22, FR-52 (no "pre-start" left) | Used throughout; Foundation notes A3-M wireframe string superseded | OK |
| 28 | Node heartbeat (FR-2) vs Fleet heartbeat (FR-6); FR-4 agent heartbeat kept distinct | FR-2, FR-3, FR-4, FR-6, FR-46, NFR-4, PRIV-9 | "Fleet heartbeat" in B6b/Privacy table/Flow 6; "Heartbeat OK" string matches PRD FR-6 | OK |
| 29 | Server orders decisions consistently; FR-34 records last-resort and policy version; SEC-7 extensions | FR-22; FR-34; SEC-7 | Decisions "Several people deciding"; FR-34 mapping "Who permitted it"; Settings row | OK |
| 30 | FR-15: neither notifications nor portal → in-cluster dashboard only | FR-15; PRIV-9 | Surface states "Portal and notifications not permitted"; IA | OK |
| 31 | UJ-1 climax / 5.6 "undo only where possible"; UJ-2 "Orvex technical approval still needed" | UJ-1; UJ-2; 5.6 Description | UJ-1 step 7; UJ-2 | OK |
| 32 | Addendum pointer to UX open items after O-13 added (round-2 change) | addendum "For the architecture" › "UX open items": still "O-1 to O-12" | Open items table has O-13 (undo-reject window) | Missing (addendum stale) |

## Notes

- Row 9: the PRD rule covers any material change and any relevant approver. EXPERIENCE.md's general "Request re-issued" pattern (old approvals no longer count) covers most of it, but the recovery-plan line says the customer is asked again without the "where their production is affected" qualifier, which reads wrong for a platform-only manual repair.
- Row 15: PRD PRIV-9 and the memlog say "not revoked"; EXPERIENCE.md says "not silently revoked", which implies they could be revoked with notice.
- Row 32: the addendum still says O-1 to O-12. The architecture item for O-13 is already covered by the addendum's own "Undoing a rejection" bullet, so only the range is out of date.
- AI_LOG #27 partial supersession and the reviewer-pass choice are process entries, so no PRD text is expected. Both documents match the supersession: the heartbeat is required and never optional.
- Minor, not counted: FR-50's first list says it "notifies the other approvers concerned", and a later bullet says they are notified when the undo window ends. The UX uses "when the window ends" throughout. The PRD could say the same in one place.
