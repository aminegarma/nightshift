# Triage of the three reviews (2026-11-03)

Sources: `review-rubric.md` (0 critical, 1 high), `review-accessibility.md` (1 critical, 6 high), `review-adversarial.md` (2 critical, 14 high). Mediums and lows go into the spines during the fix pass without separate questions where they are mechanical.

## Part 1: product choices for Amine (asked separately)

- **Q1. One-tap decisions** (accessibility critical; adversarial high on Reject; accessibility high on "Approve rollback for these 300 clusters" and "Accept this change").
- **Q2. Length of the approval screen for non-experts** (accessibility high; B3 has 10 sections and B3-M has 11 before the decision).
- **Q3. Route from the phone call to the portal** (accessibility high; a call carries no link, and deaf or hard-of-hearing owners get no usable alert).

## Part 2: fixes that follow existing rules (one yes/no)

Each fix applies a rule already in the PRD or the record. Source in brackets.

1. **Decision tied to the version shown** (adversarial critical; accessibility high). The screen freezes the version of the request it shows. If the request is re-issued or withdrawn, a banner says "This request has changed" (or "This request is no longer needed") and both buttons are disabled until the person opens the new version. The decision carries the version ID; "Try again" never resends a decision made on an old version. [FR-22; Glossary "Approval": tied to the evidence shown; Amine 2026-11-03: a material change invalidates an approval]
2. **Two-key rule visible in A3** (adversarial critical). A3 shows separate, role-labelled actions: **Give Orvex technical approval** and, only for Orvex support with delegation, **Approve on the customer's behalf (delegated)**. The same person is never offered both for one repair. [FR-21; addendum "Approval surface": two different people where two approvals are needed; Amine 2026-11-03 on ticks and delegation]
3. **Manual-repair lifecycle** (adversarial highs):
   - New repair status **Work in progress**, set when the performer presses **Start now** after the pre-start check passes. While it lasts, the coordinator blocks other repairs on the target. [FR-29]
   - A failed or inconclusive pre-start check blocks the work, and a fresh approval can't override it. [Amine 2026-11-03; FR-22, SEC-8]
   - The window limits when work may **start**. Work already in progress when the window ends is finished or recovered under the reviewed recovery plan, never abandoned, and the history notes it. [AI draft]
   - The history states facts as they were reported: "Started 01:10 · reported done by Marc 01:22 · checked by Nightshift". [FR-34, FR-52]
   - A workaround on hardware ends as **Mitigated**: "Connection stable on the standby interface. The network card still needs replacing; the fault stays open until you confirm the replacement." [FR-20]
   - The recovery plan shows "Review needed" until it has been reviewed. A review that changes the plan materially asks the customer again. [FR-22; FR-52]
4. **Honest no-answer line** (adversarial high). When a last-resort tick exists for the repair, the customer sees: "If you don't answer: we keep watching. Because you allowed it as a last resort, this repair may run on its own if failure is about 30 minutes away." [FR-23, FR-24]
5. **No healthy words on stale data** (adversarial high). On B1 and A1, an out-of-date card replaces its impact line ("Checkout works normally") with "Out of date: last data 02:10". It never shows healthy words in a stale state. [Amine L10: never a stale green]
6. **Mode and channel changes with requests open** (adversarial highs):
   - The console shows each cluster's mode ("Alert-only") on A1, A2 and A3.
   - Switching to alert-only, or turning off portal access, cancels open requests and approvals not yet used. They are recorded as Cancelled, and the approvers are told. [Glossary "Alert-only mode"; PRIV-9: without the portal no approval can be given]
7. **Conflicting decisions** (adversarial high). A Reject by any required approver blocks the repair (FR-50). Among a customer's administrators, the first decision counts and the others see it. The history names the person for every approval, for example "Lea (Orvex support), on your behalf, 01:03". [FR-34 "by whom"]
8. **No AI text in unlabelled lines** (adversarial high). Lead sentences, card impact lines, Slack lines and summary lines are built from templates and structured fields. AI wording appears only inside the labelled explanation block. [SEC-1; open item A6]
9. **Fleet approval says what it covers** (adversarial high; accessibility high). The button reads "Approve rollback for 288 eligible clusters", with the breakdown beside it: 12 can't be included (Fleet reports off) and 112 still need their customer. The set is frozen at the click; clusters added later need a new approval. [UJ-5; FR-32]
10. **Console live refresh** (accessibility high). A "Pause live updates" control, plus a rule that a refresh never moves the row in focus or the person's place in the list. [Amine 2026-11-03: auto-refresh keeps focus]
11. **Accessible sign-in** (accessibility high). Added to open item A5 as constraints: password managers, paste and passkeys allowed; a warning before the session times out, with a way to stay signed in; the pending decision survives a new sign-in. [WCAG 2.2 3.3.8 and 2.2.1 as a design target]
12. **Rubric mechanics:**
    - Specify the customer cluster card and the timeline entry in both spines.
    - "Waiting for later waves" becomes an A4 progress label, not a repair status.
    - Remove "Out of date" from the repair-status list.
    - Rename the open items O-1 to O-12 so they don't clash with screen IDs.
    - Raise text-secondary on the dark stale hatch to 4.5:1 or more.
    - Show time zones on times.
    - Fix the customer wireframe's label for the memory-leak scenario (UJ-1, not UJ-2) and its severity (Warning).
    - Fix the A5 wording "accepted by customer, 20 Oct" to "scope agreed 20 Oct".
    - Regenerate the B3 mock with Warning, and the A1 mock's manual row to match the wireframe (C-0450 · shop-us-2).
