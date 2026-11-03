# Information layout proposal v1 (2026-10-31)

Status: proposal for Amine to review. Not styled. Items marked [AI] are the AI's proposals; everything else is drawn from Amine's words this session or from the PRD (IDs given).

## Form factors

- **Orvex console**: desktop web, wide screens. Users: the Orvex Nightshift engineer on duty (Josh, UJ-3, UJ-5) and Orvex support (no journey yet; uses the same console, and can approve on a customer's behalf only where delegated, never for dangerous repairs, FR-21) [AI placement].
- **Customer view**: the Quornex portal (FR-15), responsive: desktop for browsing, phone for approvals. Users: the customer's business owner (shop owner UJ-1, Cris UJ-2, Samira UJ-4).
- **Notifications**: Slack and phone calls (FR-13, FR-14). A call only notifies.

## Shared patterns (both experiences)

1. **Freshness on every panel.** Each panel shows "Updated 40 s ago". Past a threshold (open in the PRD, Q8), the panel switches to an explicit out-of-date state: greyed, with words such as "No data from cluster eu-2 since 02:10. What you see may be out of date." Never a stale green. Colour is never the only signal. (Amine; FR-4, FR-6)
2. **Two labelled blocks, always apart.** "Verified facts" (from the rule-based checks) and "Nightshift's explanation (written by AI)". (Amine; SEC-1, FR-11)
3. **Approval status in plain words.** E.g. "You approved at 02:14. Waiting for Orvex technical approval." (Amine; FR-21)
4. **Status labels from the challenge brief**: "Fixed on its own", "Waiting for a person", "Being watched". (challenge brief p.1)
5. **Severity = the PRD's notification levels** [AI]: Critical (phone call), Needs a decision (alert), For information (dashboard and morning summary). (FR-13; the PRD has no other severity scale)
6. **What Nightshift cannot see** is stated, not hidden (limited-visibility mode). (FR-5, FR-7)

## A. Orvex console (desktop)

**A1. Fleet overview (home).** In the first five seconds:
- Top strip, left to right: approvals waiting for Orvex (count, oldest wait) · critical problems · fleet-wide problems (FR-32) · clusters with no data or stale data.
- Attention queue (table), sorted by customer impact, then time to impact. Columns: customer impact · level · customer · cluster(s) · status · time to impact · approvals still needed · updated.
- Cluster groups of 100 (FR-15) as a health grid; stale or disconnected tiles are hatched with a label.
Why: the queue comes before the grid because the engineer acts on problems, not on clusters.

**A2. Problem detail (incident explanation).** Header: problem, customer impact, level, status, freshness. Body: Verified facts | Nightshift's explanation, side by side. Below: timeline, what Nightshift cannot see, proposed repair, link to the approval.

**A3. Approval review.** The same order as the customer approval (B3), plus technical depth: catalogue entry and version, safety preconditions, the customer's tick or approval, delegation ("approved on behalf of"), and for dangerous repairs the recovery-plan review.

**A4. Fleet-wide problem (UJ-5).** One problem, the clusters it affects grouped by approval state (authorised in advance / waiting for the customer / waiting for Orvex), progress as clusters recover.

**A5. Action history.** Filterable table: time · customer · cluster · repair · risk level · who permitted it (ticked / approved by whom, when / on behalf of) · progress · result (worked / did not work / harmful, rolled back). Each row opens the full record (FR-34).

## B. Customer view (portal; approvals phone-first)

**B1. Home: my clusters.** Top: "Needs your decision" (pending approvals). Then one card per cluster with: status label, customer impact in words ("Checkout works normally"), freshness line. Combined view across clusters (FR-15, PRIV-5).

**B2. Problem page.** The FR-11 plain-words message first ("Your checkout service is using more memory than usual…"), then "Verified facts" and "Nightshift's explanation (written by AI)" as separate blocks, then "If you don't answer: we keep watching and change nothing that isn't already authorised" (FR-14, FR-23).

**B3. Approval (phone, one column, in this order):**
1. The problem, in one sentence
2. Customer impact (now, and time to impact)
3. The exact repair and target ("Restart checkout-api, replica 2 of 3, cluster shop-eu-1")
4. Risk level, in words
5. Expected interruption
6. Recovery plan (the rollback for safe and risky repairs; the reviewed recovery plan for dangerous ones)
7. Verified facts · Nightshift's explanation (written by AI)
8. Approvals still required ("You: needed · Orvex technical approval: needed"). For a dangerous repair: "Your own approval is needed: Orvex support cannot approve this on your behalf."
9. What happens if you don't answer
10. Buttons: **Approve this repair** · **Reject**
One repair per approval; never bundled. (Amine; Glossary "Approval")

**B4. Activity (action history).** A timeline, PagerDuty-style. Each repair shows its progress steps (Approved → Running → Checking the result → Worked / Did not work, undone) and who permitted it. (Amine; FR-33, FR-34)

**B5. Morning summary (UJ-4).** Last night's activity: what happened, what Nightshift fixed, and what it is still watching (FR-16).

## Out of the four wireframes, but referenced

- **Settings checklist** (ticks, mode, delegation, last-resort condition): not wireframed. Approvals and history show "Ticked in your settings on 12 Oct" as read-only, with a link [AI].
