# Open items after the 2026-11-03 UX update

## 1. Architecture-dependent details: kept explicitly open in the spines

The UX shows the behaviour; the mechanism or the value belongs to `bmad-architecture` (or to Orvex). Each item appears in EXPERIENCE.md as `[OPEN: architecture, O-n]` (IDs O-1 to O-12, renamed from A1–A11 and B1 on 2026-11-03 so they don't clash with screen IDs) with the UX behaviour that is already fixed.

| # | Open detail | What the UX already fixes | Source |
|---|---|---|---|
| O-1 | Freshness threshold: when a panel switches to "out of date" | Every panel shows "Updated 40 s ago"; past the threshold it goes grey and hatched with words; never a stale green | PRD item 8; FR-4 |
| O-2 | Approval validity values (per repair catalogue entry) | Shown as "Valid until 02:44" once an approval is given; unanswered requests don't expire | PRD item 18 → catalogue field (Amine, 2026-11-03) |
| O-3 | Two approvals needed and one runs out before the other is given: who is re-asked, and how | The person whose approval ran out is told "Your approval ran out at 23:10; you were asked again", and the history records it | Addendum "From the review…" (adversarial H9) |
| O-4 | Fleet-wide approval (A4) across waves: does one approval cover every wave, or is Josh re-asked when it runs out? | Approval recorded per cluster; each cluster re-checked; progress by wave | UJ-5; FR-32, FR-47 |
| O-5 | Approver roles, step-up authentication, mapping portal identities to customers, two different people where two approvals are needed | Approval only in the authenticated portal; Slack/phone only notify | Addendum "Approval surface" (SEC-R2-03/05, H-3) |
| O-6 | Rendering action and target only from structured data; neutralising names and links an attacker controls | The UX rule: repair, target and steps come from the catalogue and structured fields, never from AI text | Addendum "Approval surface" |
| O-7 | In-cluster-only dashboard: where it runs and how a person reaches it | Exists when neither the portal nor notifications are permitted; no approvals there | FR-15, PRIV-9 |
| O-8 | Who may press "I've done it: check now" on a manual repair, and how that is authenticated | Only the named performer sees it; Nightshift checks before closing | FR-52 |
| O-9 | Orvex support's restricted role: exact permissions | Same console, restricted; approves on a customer's behalf only where delegated; never manual dangerous repairs | Addendum; FR-21, FR-52 |
| O-10 | Which signals decide "can affect customer production" | The UX displays the catalogue field and the Dispute action; in doubt, customer-production rules apply | FR-21; adversarial H3 |
| O-11 | What a Slack message or phone call may contain (allowlisted fields) | No raw logs, secrets or customer data; links to the portal | PRIV-2 to PRIV-4 |
| O-12 | Mapping neutral tokens onto the Quornex portal's design system | DESIGN.md defines neutral tokens; brand mapping later | Amine, 2026-11-03 (Orvex) |

## 2. Queued for the next `bmad-prd` Update (decided in the UX run)

1. **Fleet heartbeat required (PRIV-9, FR-6, NFR-4, item 22):** the minimal heartbeat is a required service channel, explained with its purpose and exact fields before the customer accepts the service, and still authenticated and checked. A strict no-outbound deployment can't use managed Fleet. Drop the status texts "Heartbeat not permitted by the customer: status unknown" and "Remote monitoring disabled by policy: status unknown"; a cluster with reports off shows "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation".
2. **Onboarding defaults (PRIV-9, item 22):** Fleet reports, notifications and portal start ticked; external AI starts with nothing selected. Reword PRIV-9: confirming the onboarding channel screen is the explicit permission.
3. **Approval validity (FR-22, Glossary "Repair catalogue", item 18):** each catalogue entry states how long an approval given at the time stays valid. Close item 18.
4. **Unanswered requests (FR-22/FR-23):** an unanswered request doesn't expire. It stays open with current evidence, is re-issued on a material change and is withdrawn if the problem resolves.
5. **Manual dangerous repairs (FR-52):** approvers approve a stated time window; outside it they are asked again; the performer re-runs the pre-start evidence check. The recovery plan is reviewed by the Orvex engineer who gives technical approval.
6. **Addendum "For the UX":** statuses now include "Waiting for Orvex" and "Manual repair needed"; remove the two heartbeat status texts.
8. **Text message with every phone call (FR-13, FR-14, PRIV-9 notifications channel):** each call is paired with a text message carrying the portal link, and customers can choose a text instead of a call. SMS becomes a notification medium within the allowlisted fields (Amine, 2026-11-03).
9. **Turning off portal access (PRIV-9):** blocks new remote approvals. It doesn't silently revoke ticks, the management policy or last-resort permissions. Its effect on approvals already given must be stated; the UX proposal is that they stay valid until their validity ends (Amine, 2026-11-03; proposal still to confirm).
10. **Withdraw and undo (FR-22, FR-50):** an approval can be withdrawn until the repair starts. A Reject can be undone until the other approvers have been notified. The server orders decisions, and the history keeps every step (Amine, 2026-11-03).
7. **Carried over from `reconcile-ux-memlog.md` section 2, not applied in the 2026-11-02 Update:** FR-14 shows the recovery plan (rollback only when certain); the approval request can be read and answered on a phone; FR-15: every dashboard shows how current its data is and never shows stale data as healthy; FR-32/UJ-5: one Orvex approval may cover one problem group, recorded per cluster.
11. **Statuses for the addendum "For the UX" (adds to item 6):** Work in progress, Mitigated and Problem still there (manual-repair lifecycle, 2026-11-03).

## 3. Deferred review findings (next UX Update)

Medium and low review findings, and a few highs, that need a product decision or are polish. Amine asked to keep the 2026-11-03 Finalize focused, so they are listed here, not decided. Full text is in `review-adversarial.md`, `review-accessibility.md` and `review-rubric.md`.

- **Manual repairs:**
  - What happens after "Problem still there", and after a blocked pre-start check (a new request? escalation?).
  - There is no flow for a repair performed by the customer or their provider, or for handing evidence to a hardware provider.
  - Notices to the performer, and reassigning the work.
  - Flow 7's performer: moving the node's IP to its standby interface is operating-system network configuration, which OMK manages, so an Orvex engineer performs it; replacing the card is the customer's (FR-52). Confirm this reading.
  - Is Flow 7's Critical (card failing, failure about 1 hour away) "imminent" under FR-13?
- **Status colours** for Work in progress (blue), Mitigated (orange) and Problem still there (red), and the incident status while a problem is Mitigated: [ASSUMPTION].
- **Adversarial findings:**
  - The info card can go stale or be reclassified.
  - "Heartbeat OK" tiles read as healthy.
  - There is no FR-28 "repairs stopped" banner and no Resume action.
  - How far a rejection reaches over ticked repairs for the same problem.
  - The green "Safe" chip clashes with "green means verified".
  - The default for delegation, and what revoking it does.
  - A request code against phishing.
  - Names an attacker controls, shown inside prose.
  - Settings changes in the history.
  - Each approval's validity, and the tick's version, on A3.
  - "Valid until, or sooner".
  - Where "Accept this change" sits, and whether it can be undone.
  - Who gets credit in the morning summary.
  - Wording when a request is withdrawn while an approval was waiting.
- **Accessibility findings:**
  - Rules for live regions and the meaning of progress steps for screen readers.
  - Console reflow and the 11px labels.
  - Chips wrapping at 200% text.
  - A help route (WCAG 3.2.6).
  - Table semantics.
  - The focus ring has the same colour as the primary button fill (1.00:1).
  - Hatching behind body text.
  - Motion.
  - Keyboard use and 24px targets in the health grid.
  - Where focus goes after a decision.
- **Wording:** a customer-facing name for "Orvex technical approval" (the review suggested "Orvex engineer's check").
- **Assumptions added in the fix pass:**
  - Times in the viewer's own time zone.
  - Collapsible sections start closed.
  - Link style and console button size.
  - The "F" and "?" tiles.
  - The colour of the "request changed" banner.
  - The wording when no tested repair exists.
