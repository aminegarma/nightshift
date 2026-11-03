# Validation Report — Nightshift

- **DESIGN.md:** `/home/amine/nightshift/_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/DESIGN.md` (status: draft)
- **EXPERIENCE.md:** `/home/amine/nightshift/_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/EXPERIENCE.md` (status: draft)
- **Run at:** 2026-11-03T15:41:02+00:00

## Overall verdict
The pair is a usable contract. All five PRD journeys (verbatim names) plus Flow 6 and Flow 7 have a protagonist, numbered steps, a climax and a failure path. Every colour token has a hex value with a `-dark` twin and stated contrast. The 16 named components appear under identical names in both spines with real rules, and all 72 `{token}` references resolve. Nothing is critical. The gaps are at the edges: unnamed components that carry real screens (the B1 cluster card, timeline entries, links, console-sized buttons), a few statuses and states with no definition ("Waiting for later waves", "Out of date" listed as a repair status), open-item IDs that collide with surface IDs, and a lot of provenance narration that downstream readers do not need.

The two extra reviewers shift the picture. The rubric checks whether the contract is complete and consistent, and it largely is. The accessibility and adversarial reviewers check whether the behaviour it commits to is safe for a half-awake person at 3 AM, and both say the pair is **not ready to hand off**, with three criticals between them, all at the moment of decision: Approve and Reject are irreversible single taps on a phone with no confirmation, undo or withdrawal (accessibility); an approval can be committed on evidence other than what the person read, because nothing ties the tap to the version on screen (adversarial); and in A3 the single **Approve this repair** button can collapse the customer's approval and Orvex technical approval into one click by Orvex (adversarial). Their high findings sit at the same edges: evidence changing under the reader, several people deciding one request, the manual-repair lifecycle between "approved" and "I've done it", alert-only and channel switches with requests open, healthy words on out-of-date customer cards, AI text in unlabelled lines, and live console refresh with no pause or focus rule. They also converge with the rubric on undefined link and interactive states, the fleet-reports-off grid tile and dark-mode text on the stale hatch (4.28:1). Across all three reviewers: 3 critical, 21 high, 41 medium, 26 low.

## Category verdicts
- Flow coverage — adequate
- Token completeness — adequate
- Component coverage — adequate
- State coverage — adequate
- Visual reference coverage — adequate
- Bloat & overspecification — adequate
- Inheritance discipline — adequate
- Shape fit — strong

## Findings by severity

| Reviewer | Critical | High | Medium | Low |
|---|---|---|---|---|
| Rubric | 0 | 1 | 16 | 16 |
| Accessibility | 1 | 6 | 12 | 4 |
| Adversarial | 2 | 14 | 13 | 6 |
| **Total** | **3** | **21** | **41** | **26** |

### Critical (3)

**[Accessibility reviewer]** — Approve and Reject are irreversible single taps on a phone with no confirmation, no undo and no withdrawal. (§ EXPERIENCE.md › Interaction Primitives "Decisions commit on one tap; the result screen is the confirmation"; Component Patterns › Primary button, Secondary button "Reject commits on one tap… no extra dialog"; DESIGN.md › Layout "full-width buttons at the end")
The buttons are stacked full-width at the bottom of a long scroll, 12px apart, used one-handed by a half-awake non-expert. Reject is the worse case: it blocks the repair and "won't ask for this repair again on its own", so a stray tap at 02:15 can leave checkout to fail at 06:00. A safe, not-ticked repair needs only the customer's approval (Authorisation table), so a stray Approve runs a production change with no second human. WCAG 3.3.4 (Error Prevention: reversible, checked or confirmed) is the closest criterion and the spines meet none of its three options.
Fix: keep one tap, but make it reversible: after either tap, show the result screen with an **Undo** (e.g. 10–15 s, decision not sent until it lapses) and, for Approve, "Withdraw my approval" until the repair starts; record withdrawals in history. If undo is architecturally hard, use a bottom-sheet confirmation that restates action, target and interruption ("Restart checkout-api now? Checkout may be down 30–60 s.") with the confirm button in the same position as the original. Also add at least 24px between Approve and Reject on phone.

**[Adversarial reviewer]** — An approval can be committed on evidence the person didn't read, or on stale evidence. (§ Interaction Primitives "Live data"; State Patterns › Surface states "Request re-issued", "Decision not recorded"; Approval validity "always shows current evidence"; Authorisation & approvals "tied to the exact … evidence shown")
*Scenario:* Cris opens B3 at 02:13 and his phone locks. At 02:20 Nightshift re-issues the request: memory is climbing faster and the replica count has changed. He unlocks at 02:31. Mobile browsers suspend background timers, so the tab still shows the 02:13 render, and he taps **Approve this repair**. Variants: an automatic refresh swaps sections 3–7 just as his thumb lands; "try again" after a network error resends the old decision; Josh approves in A3 while the cluster has been out of date since 02:10. The spines say an approval is tied to the evidence shown, but nothing says the tap carries the version that was on screen. Nothing says what the screen does when that version is out of date, or whether Approve is offered on an out-of-date cluster at all. Only A5 shows "Blocked", afterwards.
Fix: give each request version an ID and have the decision carry the version that was rendered. The server refuses a mismatch, and the screen says "This request changed at 02:20 while you were reading. Nothing was approved. Review the new version.", with the changed sections marked. Decision screens never replace sections 1–8 in place; a banner announces new evidence instead. Approve stays unavailable until every section has loaded, and while the cluster is out of date ("You can't approve this now: no data from shop-eu-1 since 02:10"). "Try again" re-reads the request before resending. A second tap never creates a second decision. Add this failure path to UJ-1 and UJ-3.

**[Adversarial reviewer]** — In A3 one button can stand for either of two approvals, so the two-key rule can collapse into one click by Orvex. (§ Information Architecture › A3 "'Approved on behalf of the customer' (delegation)" and the Orvex support row; Voice and Tone › Exact labels "Approval buttons"; Authorisation & approvals table)
*Scenario:* the customer has delegated risky repairs to Orvex support. An unticked risky repair needs both the customer's approval and Orvex technical approval. In the same console, someone with support and engineer rights (or two colleagues side by side) opens A3 and clicks the one **Approve this repair** button. The screen doesn't say which approval the click gives. It could be recorded as both, or as the delegated one followed by a technical one from the same person. "Two different people" is [OPEN: architecture], but a single, undifferentiated button makes the unsafe result the easy one.
Fix: separate actions labelled with the role they exercise: **Give Orvex technical approval** and **Approve on Customer C-0142's behalf (delegated)**. Never offer both to the same person on the same request. Afterwards A3 says "You gave Orvex technical approval at 02:14. The customer's approval must come from someone else." "Approvals still required" names each approval and its person, and the history keeps them as two rows.

### High (21)

**[Component coverage]** — The **cluster card** has no spec in either spine. (§ IA › B1, B2 "Reached from: Cluster card", B4; State Patterns › Freshness)
It is the main element of B1 (one per cluster: severity, status, impact in words, freshness) and has its own states: current, "Out of date · Last updated 02:10", resolved, alert-only. The **timeline entry** that B4 Activity and the A2 Timeline are built from has no spec either; Progress steps covers only part of a B4 row.
Fix: add "Cluster card" and "Timeline entry" to DESIGN.md Components (tokens and prose) and EXPERIENCE.md Component Patterns (behaviour, states, click target).

**[Accessibility reviewer]** — The approval screen can change or disappear while the user is reading it. (§ EXPERIENCE.md › Approval validity "always shows current evidence… re-issued if the evidence or conditions materially change… withdrawn if the problem resolves"; State Patterns › Surface states "Request re-issued: current evidence replaces the old", "Request withdrawn: …no buttons remain"; Interaction Primitives › Live data "Panels refresh on their own")
If evidence is swapped in place, a person who read version 1 can tap Approve on version 2 (the Glossary ties approval to "evidence shown"); if buttons vanish, keyboard and screen-reader focus is lost to the page body and the thumb lands on whatever moved up (WCAG 3.2.2 / 3.2.5 spirit, 2.4.3).
Fix: never mutate B3/B3-M/A3/A3-M content in place. Freeze the version on screen, show a polite, persistent banner "This request has changed. Review the new version" (role=status, announced once), disable both buttons until the new version is opened, and send the version ID with the decision so the server rejects a stale one. On withdrawal, replace the buttons with a sentence ("The problem went away at 02:31; nothing to decide") and move focus to it.

**[Accessibility reviewer]** — The phone call that wakes a Critical-severity customer has no designed route to the portal, and Critical relies on a voice call alone. (§ EXPERIENCE.md › State Patterns › Severity "Critical → Phone call"; Information Architecture › Slack notification "(and phone call)"; Surface → journey closure "Phone-call content is not designed [OPEN: architecture A11]"; UJ-2 step 2 "He opens the request in the portal", Flow 7 step 2)
A call carries no link, so Cris must find the portal, sign in and locate the request himself at 3 AM; a Deaf or hard-of-hearing owner gets no usable Critical alert at all.
Fix: state in the spines that every Critical call is paired with a text notification (SMS/push/Slack) carrying the deep link, that the call says so ("We've sent you a link by text") and offers to repeat, and that B1 opens with "Needs your decision" first after sign-in (already true). Let the customer choose text-only for Critical in B6b.

**[Accessibility reviewer]** — Sign-in and step-up authentication sit on the critical path of every approval but carry no accessibility constraint. (§ EXPERIENCE.md › Interaction Primitives "Notifications deep-link through sign-in… Step-up authentication and approver roles [OPEN: architecture]"; Open items A5)
WCAG 2.2 3.3.8 Accessible Authentication (Minimum) forbids cognitive function tests (remembering or transcribing codes) without an alternative; a portal session that expires while a screen-reader or magnifier user works through ten sections, then bounces Approve to a sign-in page, breaks 2.2.1 and loses the decision.
Fix: add to the Accessibility Floor: sign-in and step-up allow password managers and paste, offer passkeys or a device prompt, never require transcribing a code without a copy/paste or autofill path; deep links survive sign-in and land on the same request version; if the session will expire on B3/B3-M/A3, warn at least 20 s ahead with "Stay signed in", and after re-authentication return to the request with the pending decision preserved (never auto-submitted).

**[Accessibility reviewer]** — The customer approval screen asks a non-expert to process ten (B3) or eleven (B3-M) sections before reaching the decision, partly in infrastructure language. (§ EXPERIENCE.md › Component Patterns › Approval card "B3 order: 1… 10", Manual-repair panel "B3-M order: 1… 11"; Key Flows UJ-1 step 4 "restart checkout-api (its only replica)", Flow 7 "stable on the standby interface", "node n-7"; Voice and Tone "Orvex technical approval", "repair catalogue", "rollback")
The content is right (memlog L11 requires it before approving), but there is no at-a-glance summary and no plain-language gloss for "replica", "rollback", "catalogue", "node", "checkout-api" or "Orvex technical approval".
Fix: add a three-line "What we're asking" summary directly under the lead sentence (action in plain words · expected interruption · what happens if you do nothing) with a "Go to decision" link; keep sections 1–9 in order but let 6 (Recovery plan) and 7 (Evidence) open as expandable sections with a one-line summary each; add a short plain-words gloss in the repair line ("Restart the checkout program (there's only one copy running, so checkout pauses briefly)"); rename "Orvex technical approval" for customers to "Orvex engineer's check". Write the gloss rules into Voice and Tone.

**[Accessibility reviewer]** — Fleet approval and policy acceptance also commit on one click (§ EXPERIENCE.md › Interaction Primitives "Decisions commit on one tap"; UJ-5 step 5; Privacy & outbound channels › Agreed management policy)
Consequential console and settings actions also commit on one click: **Approve rollback for these 300 clusters** and **Accept this change** (which widens what Nightshift may do in production). "Accept this change" modifies the customer's stored permissions, squarely the data-modification case of WCAG 3.3.4; the fleet approval has the largest blast radius in the product.
Fix: for the fleet approval, a confirmation step that restates counts ("300 clusters · 112 will still wait for their customer · runs in 6 waves") with the confirm control in place; for policy acceptance, a review-then-confirm step plus "Undo acceptance" while nothing has yet run under it. Record either in history.

**[Accessibility reviewer]** — Live refresh in the console has no pause and no rule for focus or re-sorting. (§ EXPERIENCE.md › Interaction Primitives › Live data "[ASSUMPTION] Panels refresh on their own"; Component Patterns › Attention-queue row "Sort: customer impact, then time to impact")
A queue that re-sorts as times to impact change moves the row under the pointer or keyboard focus; a screen-reader user loses their place on every refresh. WCAG 2.2.2 (Pause, Stop, Hide) applies to auto-updating content shown alongside other content.
Fix: keep focus on the same item across refreshes; don't re-order rows while focus or pointer is in the table: show "3 changes · Show" (role=status, announced once) and apply on request; add a visible "Pause live updates" toggle per page that also pauses the freshness counters; never steal focus on refresh.

**[Adversarial reviewer]** — A manual repair has no "work started" state, so nobody (and no automatic repair) knows a person is working on the target. (§ Component Patterns › Progress steps "Manual repair needed → Verifying"; Key Flows › Flow 7 steps 5–6)
*Scenario:* at 01:10 Marc runs the pre-start check and starts moving traffic to the standby interface. Cris and Josh still see violet "Manual repair needed", which reads as waiting. A ticked safe repair or a policy repair on node n-7 fires halfway through Marc's work, because the repair coordinator (FR-29) doesn't know a person holds the target. In B4 Cris sees "waiting" and assumes nobody has started.
Fix: after a passing pre-start check, the performer presses **I'm starting now**. This records the start, registers the target with the coordinator and holds conflicting automatic repairs on that target. Status: "Manual repair in progress: Marc started 01:10". **I've done it: check now** appears only after a start.

**[Adversarial reviewer]** — A window that ends mid-work, and a pre-start check that fails or can't decide, are not designed. (§ State Patterns › Approval validity "Manual repairs"; Surface states "Manual repair, outside the window"; Flow 7 failure line)
*Scenario:* Marc starts at 02:50 and the work runs to 03:15. At 03:00 "outside it they are asked again" fires, so Cris is called at 03:00 to re-approve work that is already half-done, or **I've done it** is refused. Separately, the pre-start check fails, or can't run because the cluster is out of date. Nothing stops a person from carrying on, and the spines only say "he doesn't start [ASSUMPTION]".
Fix: the window governs the start. Work that started inside it may finish; an overrun shows "Running past the approved window (ended 03:00)" and is reported to the approvers, without asking them to approve again. The check result gates **I'm starting now**. On Fail or "Can't tell" the screen says "Don't start: the evidence has changed. Your approvals no longer cover this; the approvers are being asked again." The approvals are cancelled and recorded, and any later "done" report is recorded as work done outside approval.

**[Adversarial reviewer]** — The history states a self-report as fact and makes up a time span. (§ Key Flows › Flow 7 step 8 "performed by Marc (Orvex) 01:10–01:22 · checked by Nightshift"; State Patterns › Repair status → FR-34 outcome)
*Scenario:* Marc presses **I've done it** without doing the steps. The network card recovers on its own, Nightshift's check passes, and B4 and A5 say "performed by Marc 01:10–01:22 · Succeeded" for good. 01:10 was the pre-start check, not the start. A customer looking into a later outage trusts the record.
Fix: record only what is known: "Pre-start check passed 01:10 · Marc reported it done at 01:22 · Nightshift's check at 01:25: problem gone". Use FR-34's own words, "manual repair reported done". Show a start time only if a start was recorded (previous finding). Say that the check confirms the symptom is gone, not that the steps were followed.

**[Adversarial reviewer]** — "Succeeded" on a workaround hides a hardware fault that is still open. (§ Key Flows › Flow 7 steps 1 and 7; State Patterns › Incident status; FR-20, FR-52)
*Scenario:* Flow 7 ends "the connection is stable on the standby interface: Succeeded", and the incident goes to Resolved (green). The network card is still failing, so nobody replaces it, and next week the standby fails with no spare. The flow also has an Orvex engineer performing what looks like hardware work, while FR-52 gives hardware to the customer or their provider.
Fix: add an incident state "Worked around: hardware fault still open", not green, with the next step in words: "Ask your hardware provider to replace the network card on n-7. Here's the evidence to send them." Make Flow 7 explicitly an OMK network-configuration workaround done by Orvex. The fault closes only after the customer reports the hardware fixed and Nightshift has checked (FR-20).

**[Adversarial reviewer]** — The recovery plan reads as already reviewed when the customer approves, and a review that changes the plan doesn't ask the customer again. (§ Component Patterns › Manual-repair panel item 8 "Reviewed by Orvex before the work starts"; Key Flows › Flow 7 steps 2–4)
*Scenario:* Cris approves at 23:58. At 00:20 Josh's review changes the plan: n-7 must be drained first, so the interruption is longer. Cris approved the old plan and nothing asks him again. At midnight the past tense "Reviewed by Orvex" reads as done.
Fix: show the review state literally: "Not reviewed yet: Orvex reviews this before work starts", then "Reviewed by Josh (Orvex) at 00:20". If the review changes the steps, plan, interruption or window, that is a material change (FR-22): the customer's approval is cancelled and they are asked again. Consider asking for Orvex's review before asking the customer.

**[Adversarial reviewer]** — The "If you don't answer" line hides a last-resort run. (§ Voice and Tone › Exact labels "No answer (customer)"; Component Patterns › Approval card item 9; Authorisation & approvals "Last-resort condition")
*Scenario:* Samira ticked the last-resort condition for "Restart the only replica". A request arrives at 02:13 with failure predicted around 02:40. B3 tells her "we keep watching and change nothing that isn't already authorised". She reads that as "nothing will happen" and leaves it for the morning, or means to reject and is too late.
Fix: when the last-resort condition covers the repair, item 9 says so: "If nobody answers and checkout is predicted to fail within about 30 minutes, this restart will run on its own (you ticked the last-resort condition on 12 Oct). Reject now if you don't want that." Show the earliest time it could run, and the same in A3.

**[Adversarial reviewer]** — Customer cards keep healthy words on out-of-date data. (§ Information Architecture › B1 'impact in words ("Checkout works normally")'; State Patterns › Freshness "Customer card: Out of date · Last updated 02:10"; Component Patterns › Stale panel "Does not hide the last known values")
*Scenario:* the cluster stops reporting at 02:10 just as checkout starts failing. At 02:40 B1 still says "Checkout works normally" in large type, next to a small "Out of date" tag. A non-expert reads the sentence, not the tag. The console replaces impact with "Unknown"; the customer view doesn't.
Fix: on an out-of-date card the impact line becomes "We don't know how checkout is doing: no data since 02:10". The last known value moves to a secondary line ("Last known at 02:10: checkout working"). Apply the same rule to B2 and B5 ("still watching").

**[Adversarial reviewer]** — Alert-only mode is invisible in the console, and switching mode with requests open is undefined. (§ State Patterns › Surface states "Alert-only mode"; Authorisation & approvals "Alert-only mode"; Information Architecture › A1–A3)
*Scenario:* at 02:10 the customer switches to alert-only. At 02:14 Josh approves a platform-only repair for that cluster in A3, because nothing on A1, A2 or A3 shows the mode. The executor refuses it (SEC-7), so Josh sees an unexplained "Blocked" or believes the platform is repaired. The other way round: when the customer switches back to approval-enabled, do approvals given before the switch revive? Do requests opened before alert-only still show **Approve**?
Fix: show the mode on A1 rows, the A2 header and A3 ("Customer in alert-only mode: Nightshift won't run this. Recommend only."), and don't offer Approve there. On a switch to alert-only, open requests become recommendations and given-but-unused approvals are cancelled, recorded and reported to the approvers. Switching back revives nothing. B6's mode confirmation lists what will happen to the open items, and ticks show "Paused: alert-only mode".

**[Adversarial reviewer]** — Turning a channel off leaves requests in flight in an undefined state. (§ Privacy & outbound channels table; State Patterns › Surface states "Portal not permitted"; Key Flows › Flow 6 failure line; Authorisation & approvals "Delegation")
*Scenario:* at 02:16 an administrator unticks portal access. Cris's approval is waiting for Orvex and two requests are open: are they cancelled, kept or merely invisible? Slack still sends "Open in Quornex portal to review" to a portal with nothing to show. With notifications off and delegation on, "You're notified of every approval made on your behalf" can't be honoured. SEC-7's "changes are notified" has no channel either.
Fix: before an untick takes effect, show its consequences with counts: "2 open requests will be withdrawn. Cris's approval from 02:14 will be cancelled. Orvex support can no longer approve on your behalf, because you couldn't be told." Notifications offer the portal link only while the portal is permitted. Delegation needs a working notification route and is suspended, in words, without one. State where notices of settings changes go once notifications are off.

**[Adversarial reviewer]** — Reject commits on one tap and can't be undone for this occurrence. (§ Component Patterns › Secondary button; Voice and Tone › Exact labels "Reject result"; FR-50)
*Scenario:* at 03:00 Cris scrolls to the end and his thumb lands on the full-width **Reject**. The result screen tells him the repair is blocked and that Nightshift won't ask again unless the problem becomes critical or changes. Checkout fails two hours later and he had no way to say yes in between.
Fix: reopening at the person's own request is not automatic resubmission. The Reject result offers "I rejected this by mistake: show me the request again", valid for this occurrence while the evidence still holds, and recorded. Alternatively, add a short confirmation for Reject on phones. Either way, fix the order of the two buttons and keep space between them.

**[Adversarial reviewer]** — Conflicting decisions by different people are undefined. (§ Component Patterns › Approval card item 8; Voice and Tone › Exact labels "After Approve" and "Reject result"; Authorisation & approvals "Delegation")
*Scenario:* (a) Cris approves and Josh then rejects. Cris's B3 still says "Waiting for Orvex technical approval", so he goes back to sleep expecting a repair. (b) Orvex support approves on the customer's behalf at 01:03; at 01:05 Cris opens the same request and taps Reject. Which decision wins? (c) Two customer administrators: Samira approves on desktop while Cris rejects on his phone.
Fix: every approval screen shows each decision already made, with name and time, and tells everyone who acted: "Josh (Orvex) rejected this at 02:20. The repair won't run." Write the rule down: a rejection by any required approver blocks the repair, and the customer's own rejection overrides a delegated approval that hasn't been used yet. A second person sees the first decision and can't submit a decision based on an older screen (first critical finding).

**[Adversarial reviewer]** — Delegated approvals hide who gave them. (§ Voice and Tone › Exact labels History "Approved by Orvex support on your behalf at 01:03"; FR-34 "by whom")
*Scenario:* an Orvex support agent approves a risky restart that causes an outage. The customer's history says only "Orvex support", so they can't tell who it was or challenge it. Ticks are just as anonymous ("Ticked in your settings on 12 Oct").
Fix: "Approved on your behalf by Dana K. (Orvex support) at 01:03 · delegation set by Samira on 20 Oct · scope: risky repairs, all clusters". Name the person on ticks too: "Ticked by Samira on 12 Oct".

**[Adversarial reviewer]** — AI text can fill the most-read, unlabelled lines. (§ Component Patterns › Approval card items 1–2 and Explanation block; Information Architecture › B2 "FR-11 message first", B1 "impact in words", Slack "one-sentence risk"; SEC-1)
*Scenario:* a crafted log line steers the model. The lead sentence at the top of B3 says "Routine maintenance, no impact expected", or the B1 card says "Checkout works normally". The rule keeps only action, target and steps out of AI text. The problem sentence, the impact line, the Slack sentence and the B5 summary sentences have no stated source and no label, and they sit above or outside the yellow block.
Fix: state the source of every field on B1, B2, B3, B3-M, B5 and the Slack message. Render items 1–2 and the card impact lines from templates over structured fields (impact, time to impact). AI wording appears only inside the labelled yellow block. List the fields that must come from structured data: risk, interruption, recovery plan, validity, approvals still required, What this changes, performer and window.

**[Adversarial reviewer]** — The fleet button says "300" but means something else, and the set can change under the click. (§ Voice and Tone › Exact labels "Approve rollback for these 300 clusters"; Key Flows › UJ-5 steps 3–6; State Patterns › Freshness "12 clusters can't be included")
*Scenario:* 300 clusters are affected and "12 can't be included", yet the wave totals add up to 300, and 112 of those still need their customer. Josh reads "these 300" and believes all 300 will roll back. The 12 clusters with Fleet reports off may still be on v2.4, and nobody acts or tells those customers. A cluster that joined the group after he opened A4, or one grouped by mistake, rides on his click, and he can't take one out.
Fix: the button names the exact set it covers when rendered, and the click is refused if the set has changed ("3 clusters joined since you opened this. Review them."). Split the summary: "288 clusters in this approval · 112 also need their customer · 12 not included (Fleet reports off): their customers are told separately". Allow excluding a single cluster. In Step 1, list the exceptions (Fail, out of date, no permission) first instead of a 300-row table.

### Medium (41)

**[Flow coverage]** — UJ-1's severity is still undecided. (§ Key Flows › UJ-1 step 2; State Patterns › Severity)
The customer wireframe (B1, B2, B3, Slack) shows "Severity: Critical", and State Patterns maps Critical to a phone call, but UJ-1 step 2 sends a Slack alert. The memlog's last entry lists this as "Open for Amine", yet it is not in EXPERIENCE › Open items, so a mock or story built from the wireframe will show Critical plus a call.
Fix: decide (Warning fits "alert when a decision is needed") and record it in UJ-1, or add it to Open items.

**[Flow coverage]** — No flow for a customer-performed manual repair or hardware escalation (§ Key Flows; IA › Customer view)
There is no flow for the customer-performed manual repair or for hardware escalation (FR-20, FR-52: "the customer, or their hardware provider, for hardware and for the customer's own app"; Nightshift "prepares the evidence for the customer to send"). The only coverage is one sentence in Component Patterns › Manual-repair panel and a wireframe annotation next to B3-M after Approve. The evidence hand-off to a provider has no surface.
Fix: add a variant to Flow 7 or a short Flow 8: the customer performs it or forwards the evidence, then presses **I've done it: check now**, then Nightshift checks.

**[Flow coverage]** — FR-19 (no tested repair: explain, state uncertainty, escalate, don't repair) has no flow and no B2/A2 variant. (§ IA › A2, B2; State Patterns › Surface states)
Both IA rows assume a proposed repair always exists.
Fix: add a "No tested repair" state for A2/B2: what replaces the proposed-repair section, and who is told.

**[Token completeness]** — Several component values are prose rather than tokens (§ DESIGN.md frontmatter `components`)
Several component values are prose rather than tokens, so code that mirrors the spine has to parse them by hand: `'hatch 135deg {colors.stale-hatch-base} 5px / {colors.stale-hatch-stripe} 5px'` (chip-stale, stale-panel; 6px in attention-queue-row-stale), `severity-bar: '3px inset left, … by severity'`, `summary-tile.critical-variant: '… with … border'`, `health-grid-tile.no-open-problem: '… with 1px … outline'`, and `focus: '3px solid …, offset 2px'`.
Fix: split them into structured sub-keys (`hatch-angle`, `hatch-stripe-width`, `base`, `stripe`; `bar-width`; `outline-width`, `outline-offset`) or give the literal CSS as the palette sheet does (`repeating-linear-gradient(135deg, … 0 5px, … 5px 10px)`).

**[Token completeness]** — Contrast is not stated for `text-secondary` on tinted fills and on hatch, which are load-bearing pairs: the freshness line closes the Verified facts block, and stale customer cards read "Out of date · Last updated 02:10". (§ DESIGN.md › Colors; Components › Freshness line, Stale panel)
Computed values: dark `#A3A9B3` on `stale-hatch-stripe-dark` `#3E4248` is **4.28:1, below 4.5:1**. Light on the stale stripe is 5.19:1. On success, explanation and critical fills it is 6.4–6.8 (light) and 5.5–6.5 (dark).
Fix: say that text on a stale panel or card uses `neutral-ink` (5.6:1 dark), or adjust the dark stripe, and add the text-secondary-on-fill rows to the contrast table.

**[Component coverage]** — Links and text actions are not defined (§ DESIGN.md › Do's and Don'ts; EXPERIENCE.md › Interaction Primitives)
Links and text actions are not defined: "Review the proposed repair", "Review approval →", "Open in Quornex portal to review", "See full activity", "Ticked in your settings on 12 Oct", "Read the policy", "Dispute", "Revoke delegation", "Data leaving your cluster and management policy ›". The spines don't say which are buttons and which are links, or give a link colour or focus treatment. `primary` is reserved for the one decision per screen.
Fix: add a `link` component (colour, underline, focus) and assign each of these labels to button-secondary or link.

**[Component coverage]** — There are no console-sized buttons. (§ DESIGN.md frontmatter `button-*`; Layout & Spacing › Console)
`button-primary` and `button-secondary` hard-wire `{typography.customer-action}` (17px) and `{spacing.customer-tap-min}` (44px), but A3, A3-M and A4 also use **Approve this repair**, **Reject** and **Approve rollback for these 300 clusters** in the dense console.
Fix: add a console size variant (console-chip or console-body type, compact padding).

**[Component coverage]** — Interactive state appearance is missing beyond focus (§ DESIGN.md › Components; EXPERIENCE.md › State Patterns › Surface states)
Interactive state appearance is missing beyond focus: hover and pressed for buttons, queue rows and tiles; the selected group in the A1 selector; disabled or read-only controls for "Not an administrator" (B6, B6b) and "Orvex support, not delegated" (A3, A3-M).
Fix: add hover, pressed, selected and read-only tokens or rules. A disabled ink token would also cover read-only settings.

**[Component coverage]** — The health-grid "Fleet reports not permitted" state has no visual spec (§ EXPERIENCE.md › Component Patterns › Health-grid tile; DESIGN.md `health-grid-tile`)
The health-grid tile state "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation" is in EXPERIENCE.md › Component Patterns › Health-grid tile and in the A1 legend, but DESIGN.md `health-grid-tile` defines only critical, warning, no-open-problem and out-of-date.
Fix: add its visual treatment (for example a no-open-problem tile with a marker and legend entry).

**[Component coverage]** — Three A4 and A2/B2 elements have no component (§ IA › A2, A4, B2)
Three A4 and A2/B2 elements have no component: the A4 wave progress (Step 3: "Wave 1 of 6 done…"), the A4 per-cluster table (permission, safety checks, repair status), and the **What Nightshift cannot see** block on A2 and B2. Because green means verified and yellow means explanation, a builder has to know this block is neither.
Fix: name them. State that "What Nightshift cannot see" sits on a plain surface, and that the A4 table reuses Check table with a repair-status column.

**[State coverage]** — "Waiting for later waves" is not a defined repair status (§ State Patterns › Repair status; UJ-5 step 6; A4 wireframe)
"Waiting for later waves" (UJ-5 step 6; A4 wireframe) is used as a per-cluster repair status but is not among the State Patterns › Repair status values and has no chip mapping in DESIGN.md.
Fix: define it as an A4-only rollout state with its chip (neutral or waiting), or add it to the repair status values.

**[State coverage]** — B3 and B3-M lack "already decided" and "may not approve" states (§ State Patterns › Surface states; Open items A5)
B3 and B3-M have no state for a request someone else has already answered (a delegate approved it, or another administrator rejected it) or for a signed-in person who may not approve (permission denied). Approver roles are [OPEN], but the screen state can be fixed now.
Fix: add "Already decided by <name> at <time>" (no buttons) and "You can't approve this request" (says who can).

**[Bloat & overspecification]** — Provenance and supersession narration runs through EXPERIENCE.md (§ Foundation, Voice and Tone, State Patterns, Key Flows Flow 6 and Flow 7, Privacy)
Provenance and supersession narration runs through EXPERIENCE.md: "(Amine, 2026-11-03)", "accepted 2026-11-03", "superseded 2026-11-03", "as corrected the same day", "PRD change pending", dozens of times. Two rows of the Voice and Tone "Don't" column record withdrawn strings ("Expires at 02:44", "Heartbeat not permitted…") rather than anti-patterns a writer might reach for. This history belongs in the memlog.
Fix: strip the attributions and keep each "Don't" only where it is a real temptation.

**[Bloat & overspecification]** — The same rules are stated in several places, which invites drift. (§ Voice and Tone; Interaction Primitives; Authorisation & approvals; IA; State Patterns)
The Reject behaviour appears in Voice › Reject result, Interaction Primitives › Banned, Authorisation & approvals › Reject and Inspiration. The B3-M order appears in IA, Component Patterns › Manual-repair panel and Flow 7 step 2. Approval validity appears in State Patterns, Voice › After Approve and Open items A2.
Fix: give each rule one home and cross-reference it from the others.

**[Inheritance discipline]** — Two ID schemes collide. (§ EXPERIENCE.md › Open items)
Open items are numbered A1–A11 and B1, the same IDs as the surfaces A1–A5 and B1–B6. "[OPEN: architecture A6]" (Component Patterns › Explanation block) and "[OPEN: architecture A11]" (IA closure note) read like screen references, and "B1 Mapping neutral tokens" clashes with "B1 Home".
Fix: renumber the open items (OI-1… or ARCH-1… / ORVEX-1) and update the inline references.

**[Inheritance discipline]** — DESIGN.md puts freshness inside the repair-status family. (§ DESIGN.md frontmatter `repair-status-chip`, Components › Status chips)
`repair-status-chip.out-of-date` and the prose list end with "Out of date (02:10)" (stale hatch). This contradicts EXPERIENCE.md's "four separate fields, never merged" and its repair status values; the queue shows "Out of date (02:10)" in the Updated column, not as a repair status.
Fix: move it to a separate `freshness-chip` / `chip-stale` usage under Freshness.

**[Accessibility reviewer]** — Live text will over-announce or not announce at all; the spines don't say which. (§ EXPERIENCE.md › Accessibility Floor "status changes… are announced to screen readers" [ASSUMPTION]; Component Patterns › Freshness line "every panel and card"; DESIGN.md › Freshness line "Updated 40 s ago")
A freshness line on every panel ticking each second, if marked live, makes a console page unusable with a screen reader; if not, the stale transition is silent.
Fix: specify: freshness lines are plain text, never live regions; one polite live region per page announces only state transitions (current → out of date, repair status changes, "Needs your decision (n)" count changes), debounced and batched ("2 panels out of date: eu-2, eu-4"); customer view spells units out ("Updated 40 seconds ago").

**[Accessibility reviewer]** — Progress steps show the current step by chip styling only, and join steps with "→". (§ DESIGN.md › Components › Progress steps "Repair-status words joined by arrows, current step as its chip"; EXPERIENCE.md › Component Patterns › Progress steps)
"Which step are we on" is conveyed by visual treatment alone (WCAG 1.3.1, 1.4.1), and screen readers read "right arrow" between words.
Fix: render as an ordered list with arrows decorative (aria-hidden); mark the current step with `aria-current="step"` and a visible word ("Now: Verifying"); mark completed steps with a visible tick plus hidden "done". Same for the A4 wave strip ("Wave 2: running").

**[Accessibility reviewer]** — Most of the Accessibility Floor is still an assumption. (§ EXPERIENCE.md › Accessibility Floor: "[ASSUMPTION] Target WCAG 2.2 AA", "[ASSUMPTION] Tap targets ≥44px", "[ASSUMPTION] Keyboard-operable… announced… 200%"; DESIGN.md button min-height "[ASSUMPTION]")
Downstream builders can drop assumptions.
Fix: have Amine decide them and remove the tags; add the missing floor items from this review (authentication, live regions, reduced motion, undo, help, zoom).

**[Accessibility reviewer]** — The console has no zoom or reflow rule beyond tables. (§ EXPERIENCE.md › Responsive & Platform "Desktop web, wide screens only… No phone layout in v1"; DESIGN.md › Layout "Problem detail puts Verified facts and Nightshift's explanation side by side"; Typography console-column-label 11px uppercase, console-chip and console-mono 12px)
WCAG 1.4.10 exempts the data tables but not the summary tiles, panels, A2/A3 detail and A4 steps at 400% zoom (1280px → 320 CSS px); 11px uppercase labels are hard going for a tired engineer.
Fix: state that non-table console content reflows to one column below ~700 CSS px (A2 blocks stack: facts first), tables keep horizontal scroll with a sticky first column, and the minimum console text is 12px with column labels in sentence case or ≥12px.

**[Accessibility reviewer]** — Customer chips may not reflow at 200% text on a 360px phone. (§ EXPERIENCE.md › Accessibility Floor "text scales to 200%" [ASSUMPTION]; DESIGN.md › customer-chip 15px/600; Component Patterns "customer screens prefix the field ('Repair status: Waiting for approval')"; the palette sheet's chip CSS uses `white-space: nowrap`)
At 30px, "Repair status: Waiting for approval" is wider than the 320px content box, forcing horizontal scroll (1.4.4, 1.4.10).
Fix: state that customer chips wrap (no nowrap, min-height not fixed height), buttons grow in height with their label, and IDs and cluster names break; test B3 at 200% text and 1.4.12 text spacing.

**[Accessibility reviewer]** — Clickable cards and tiles are bounded only by the faint `border`, against DESIGN.md's own rule. (§ DESIGN.md › Colors "`border`… never a control's only outline"; Components › Summary tile `1px {colors.border}` while EXPERIENCE.md says "Click filters to or opens the matching items"; B1 cluster card and "Needs your decision" card are tappable per IA "Cluster card → B2")
Computed: border vs background 1.34:1 light / 1.68:1 dark; surface vs background 1.10:1 in both.
Fix: give every clickable card or tile either a `text-secondary` outline or an explicit affordance in `primary` text ("Review ›", "Open ›") that names the action; the outline is simplest and consistent with the rule.

**[Accessibility reviewer]** — Last-known values on a stale panel fail AA in dark mode. (§ DESIGN.md › Components › Freshness line "text-secondary, on every panel and card", Stale panel "stale hatch… Does not hide the last known values" in EXPERIENCE.md › Component Patterns › Stale panel)
Computed `text-secondary-dark` `#A3A9B3` on `stale-hatch-stripe-dark` `#3E4248` = **4.28:1** (< 4.5). Light passes (5.19:1).
Fix: on stale surfaces use `neutral-ink` (5.64:1 on the dark stripe) for all text including the freshness line, or lighten the dark stripe to ≤ `#383B41`, and say so in the Stale panel component.

**[Accessibility reviewer]** — Several interactive states have no tokens (§ DESIGN.md frontmatter `colors` and › Components; EXPERIENCE.md uses inline links "Ticked in your settings on 12 Oct", "See full activity", "Read the policy", and an error state "Decision not recorded")
Several interactive states have no tokens: links, error messages, disabled, checked tick/radio fill, selected/hover row. Without a link style, links in body text may be colour-only (1.4.1) or invisible; without an error style, the one error that matters most is undesigned.
Fix: add `link` (= `primary`, always underlined in body text), `error` (reuse critical ink/fill with an icon and the word "Not recorded"), `checked` (`primary` fill, `primary-ink` mark, ≥3:1), and a selected-row treatment that isn't colour-only (left bar + `aria-selected`).

**[Accessibility reviewer]** — The 100-tile health grid has no keyboard, screen-reader or target-size spec, and two tile states lack a visual. (§ DESIGN.md › Health-grid tile; EXPERIENCE.md › Health-grid tile "[ASSUMPTION] Clicking a tile with a problem opens its A2", tile "Heartbeat OK · Fleet reports not permitted")
100 tab stops is unusable; tiles named only "C" or "W" are meaningless to a screen reader; the "Fleet reports not permitted" tile has no token at all, and the stale tile has no letter (hatch alone at tile size is easy to miss).
Fix: one tab stop with arrow-key navigation (grid pattern) or a "Show as list" toggle; accessible name per tile ("shop-eu-1: critical problem; opens problem"); tiles ≥24×24 CSS px (2.5.8); give stale tiles a letter ("?") and define the fleet-reports-off tile (e.g. surface with dashed `text-secondary` outline and "F").

**[Accessibility reviewer]** — Focus and announcements after a decision or a failed decision are unspecified. (§ EXPERIENCE.md › Component Patterns › Primary button "the next screen confirms the result"; State Patterns › "Decision not recorded… offers to try again" [ASSUMPTION])
Screen-reader users won't know the decision landed or failed (4.1.3, 2.4.3).
Fix: after a decision, move focus to the result heading ("You approved at 02:14"); on failure, keep the request, show the error next to the buttons with role=alert, keep focus on a "Try again" button, and never show both an error and a success.

**[Accessibility reviewer]** — No help or contact route on the customer decision screens. (§ EXPERIENCE.md › Information Architecture › B3, B3-M; Component Patterns › Approval card order)
A non-expert unsure at 3 AM has no way to ask Orvex; WCAG 2.2 3.2.6 (Consistent Help) requires any help mechanism to sit in the same place across pages.
Fix: add a fixed "Talk to Orvex on-call" (phone/chat) entry in the same position on B1–B5, and on B3/B3-M next to the "If you don't answer" section.

**[Accessibility reviewer]** — Console table semantics are unspecified. (§ EXPERIENCE.md › A1 attention queue columns and sort; A5 "Filterable table… Dropdown filters"; Component Patterns "Click opens A2")
Whole-row click handlers are not keyboard- or screen-reader-reachable; sort order and filter results aren't announced; the A2 header chips ("Critical", "Needs attention") lack the field name the customer view adds.
Fix: real `<table>` with `<caption>` and `<th scope>`; the "Customer impact" cell is the row's link; `aria-sort` on the sorted column and a visible "Sorted by customer impact, then time to impact"; announce filter results ("12 rows"); visually hidden field prefixes on chips outside table cells.

**[Adversarial reviewer]** — The Orvex-only info card is static and absolute. (§ Voice and Tone › Exact labels "Orvex-only info card"; Component Patterns › Info card; Authorisation & approvals table)
*Scenario:* the card says "Orvex is repairing … No effect on your service expected. No action needed." But the repair is only waiting for Orvex approval, or it fails, or the pre-run check reclassifies it as affecting production (FR-21) and it becomes the customer's request. The card doesn't change. It has no time, status, outcome, link or route to Dispute. In alert-only mode it is simply untrue.
Fix: the card carries the repair status, time and freshness, and links to a read-only detail page with "What this changes" and **Dispute**. It turns into a request card when the repair is reclassified and closes into B4 and B5 with its outcome. It is never shown as an ongoing repair while the customer is in alert-only mode.

**[Adversarial reviewer]** — "Heartbeat OK" on a tile reads as healthy. (§ Component Patterns › Health-grid tile; State Patterns › Freshness "Fleet reports off")
*Scenario:* at 3 AM Josh sees "Heartbeat OK" on 12 tiles and moves on. Orvex can't see problems on those clusters, and the grid may count them as "No open problem".
Fix: these tiles never show "No open problem". Label them "Agent running · problems not reported to Orvex (customer's choice)", keep them out of the "No open problem" count and use neutral styling.

**[Adversarial reviewer]** — "Repairs stopped on this cluster" (FR-28) never shows outside the history row. (§ Voice and Tone › Exact labels "Recovery plan"; Key Flows › UJ-2 failure line)
*Scenario:* after a harmful repair the customer assumes their ticked repairs still protect them. No state on B1 or A1 shows the pause, and no surface or person resumes it.
Fix: add a cluster banner on B1, B2 and A1 (tile and queue): "Automatic repairs stopped on shop-eu-1 since 21:40 after a repair made things worse. Ticked repairs won't run until Orvex resumes them." Add a recorded **Resume** action in the console.

**[Adversarial reviewer]** — The reach of a rejection over the same problem is ambiguous. (§ Voice and Tone › Exact labels "Reject result": "Other automatic repairs keep working", "swap in another repair to get around your decision")
*Scenario:* Cris rejects the restart. A ticked safe repair for the same problem (move traffic) then runs, or FR-27 proposes the next repair. Cris either reads "nothing will be done about this" or expects his ticks to stop.
Fix: the result names them: "Repairs you've ticked for this problem may still run: Move traffic to a healthy copy (ticked 12 Oct). Nothing else will be tried for this problem without asking you."

**[Adversarial reviewer]** — The green "Safe" chip contradicts "green means verified", and the grey "Blocked" chip looks calm. (§ DESIGN.md › Colors "Rules that carry the meaning"; `risk-level-chip.safe` → `chip-success`; `repair-status-chip.blocked` → neutral)
*Scenario:* on B3 at 3 AM, a green chip beside the repair reads as checked or approved. On a critical problem, a grey "Blocked" chip reads as settled while nothing is being repaired.
Fix: give Safe a non-green treatment, keeping green for verified, succeeded and resolved. When a repair is Blocked and its problem is still open, B1, B2 and A1 add "Nothing is being repaired".

**[Adversarial reviewer]** — There is no customer-side state for someone who may not approve. (§ State Patterns › Surface states lists "Not an administrator" for B6 and B6b only; Interaction Primitives "approver roles [OPEN: architecture]")
*Scenario:* a staff member without approval rights follows the Slack link and finds **Approve this repair** on B3. The mechanism is open, but the screen state isn't designed.
Fix: define "You can't approve this. Samira or Cris can; we've told them." on B3 and B3-M, without Approve. Send decision notifications only to people who can decide.

**[Adversarial reviewer]** — The delegation default and the effect of revoking it on approvals in flight are undefined. (§ Key Flows › Flow 6 step 5; Surface → journey closure gap "Revoke delegation"; Authorisation & approvals "Delegation")
*Scenario:* the channels start ticked at onboarding, so does delegation too? Samira revokes delegation at 01:04, one minute after an on-behalf approval that hasn't run yet: does it still run?
Fix: state that delegation starts off. Revoking it cancels any unused on-behalf approvals immediately, with words on screen and in the history. B6 shows the current scope and the last approval given on the customer's behalf.

**[Adversarial reviewer]** — Sign-in through a Slack deep link teaches people to fall for phishing. (§ Information Architecture › Slack notification "(signs in)"; Interaction Primitives "Notifications deep-link through sign-in")
*Scenario:* an attacker sends a lookalike "Nightshift proposes a repair that needs your approval. Open in Quornex portal" leading to a credential-harvesting page, and a half-awake owner signs in.
Fix: each notification carries a short request code that the portal also shows. Add a line such as "If unsure, open the Quornex portal yourself; the request is waiting there." Keep this tied to A11.

**[Adversarial reviewer]** — Names an attacker controls, and AI markup, can pass for labels. (§ Voice and Tone › Exact labels "What this changes: your production (checkout on shop-eu-1)"; Key Flows › UJ-1 step 4 "restart checkout-api (its only replica)"; Component Patterns › Explanation block)
*Scenario:* a deployment named `checkout-api-approved-by-orvex` reads naturally inside a prose sentence. AI text in the yellow block contains its own "Verified facts:" heading or "Orvex has approved this". [OPEN: architecture A6] owns the neutralising mechanism, but the spines put names inside prose.
Fix: show identifiers as distinct tokens behind a fixed label ("Target: deployment `checkout-api`, namespace `shop`"), truncated and never turned into links. Render AI text as plain text with no headings, links or formatting. The UI, never the text, provides the block titles.

**[Adversarial reviewer]** — The manual performer's notices, reassignment and identity are not designed. (§ Key Flows › Flow 7 step 4 "Ready for Marc"; Open items A8; FR-52 "Who performs it")
*Scenario:* nothing reminds Marc when the window opens, so it lapses and everyone is asked again. If Marc is ill, there is no way to reassign. A hardware provider has no portal identity, so the customer presses **I've done it** for work they didn't do, and the record names them as the performer.
Fix: notify the performer when all approvals are in and again when the window opens. Add **Reassign performer**: the approvers are told, and the customer is asked again if the performer's organisation changes. Record "Reported done by Cris (work done by the hardware provider)".

**[Adversarial reviewer]** — Manual outcomes use three vocabularies and leave gaps. (§ Voice and Tone › Exact labels "Manual repair progress" uses "Problem still there"; Component Patterns › Progress steps uses "Succeeded / Failed"; State Patterns › Repair status → FR-34 outcome; Surface states "next step not recorded")
*Scenario:* the check can't decide because the data is out of date, or the manual work makes things worse. Neither case has a status, an FR-34 outcome or a next step. After "Problem still there" it is unclear whether the approvals are used up.
Fix: use one set of words: "Nightshift's check: problem gone / problem still there / can't tell yet (no data since …)". Map each to FR-34. After "still there" the problem stays open, the approvers are told and the next catalogue step is proposed. "Made things worse" follows FR-28.

**[Adversarial reviewer]** — Changes to settings, mode, delegation and policy acceptance are missing from the history. (§ Information Architecture › B4, A5; Component Patterns › Settings row "Changes are recorded and notified")
*Scenario:* the customer can't see who turned notifications off or widened delegation. Josh can't see when a customer switched to alert-only.
Fix: B4 and A5 include settings events with the person and time: "Notifications turned off by Samira at 22:04".

**[Adversarial reviewer]** — For double approvals, neither side sees the other's validity, and only the customer-first order is designed. (§ State Patterns › Approval validity; Voice and Tone › Exact labels "Approvals still required", "After Approve")
*Scenario:* in A3 Josh doesn't see that Cris's approval runs out in 4 minutes, so it lapses and Cris is woken again. When Orvex approves first, the customer's screen has no wording for an Orvex approval that is already given or about to run out.
Fix: "Approvals still required" lists each approval with its state and its own "valid until". A3 shows "Cris's approval runs out at 02:44 (in 12 min)", and the A1 queue ranks by it. Draft wording for the Orvex-first order.

### Low (26)

**[Component coverage]** — Navigation, filters, selector, legend and compact decision card have no visual spec (§ EXPERIENCE.md › IA; DESIGN.md › Components › Approval card)
The top navigation bar, the A5 dropdown filters, the A1 group selector, the health-grid legend and B1's compact "Needs your decision" card are named but have no visual spec beyond "compact version".
Fix: one line each, or point to the Quornex system once it is mapped.

**[Component coverage]** — Only `severity-chip` carries typography. (§ DESIGN.md frontmatter)
The incident, repair and risk chip families and the base `chip-*` tokens have no type, padding or height, so console and customer chips may differ in size.
Fix: put typography and padding on the base `chip-*` tokens.

**[State coverage]** — Several empty states are missing: A5 when the filters match nothing, B4 with no activity yet, and B5 after a quiet night. (§ State Patterns › Surface states)
The B5 wireframe shows "Nothing needs your decision right now." but no "nothing happened" summary.
Fix: add one line each.

**[State coverage]** — Load and save failures outside decisions are not covered: settings changes failing to save (B6, B6b, onboarding), and the console or portal failing to load at all. (§ State Patterns › Surface states, "Decision not recorded" covers decisions only)
That is different from one cluster being stale.
Fix: extend the "not recorded" rule to settings and add a page-level load error.

**[State coverage]** — Two states are marked as not settled: "Request withdrawn" (wording not drafted) and "Manual repair, problem still there" (next step not recorded). (§ State Patterns › Surface states)
Neither is in Open items, so it is unclear who closes them.
Fix: draft the wording or list both in Open items with an owner.

**[State coverage]** — A3 has no state for two Orvex engineers deciding the same request at once. (§ A3; Open items A5 "two different people")
Fix: reuse the "Already decided" state above.

**[Visual reference coverage]** — Every visual link points into `.working/`. (§ DESIGN.md banner, Colors, Layout; EXPERIENCE.md Foundation)
That is acceptable before Finalize, but the links and both frontmatter `sources` lists will break when the files are promoted.
Fix: when promoting to `wireframes/`, update the links and sources in both spines in the same edit.

**[Visual reference coverage]** — EXPERIENCE.md's visual references are file-level only (§ EXPERIENCE.md › IA, Key Flows)
EXPERIENCE.md's references are file-level only: the IA tables and Key Flows never point at a frame, while DESIGN.md › Layout does ("frame A1", "frames B3, B3-M").
Fix: add a frame reference per IA row (the surface IDs already match the frame titles).

**[Visual reference coverage]** — Wireframe placeholder data contradicts the spine scenarios in ways a mock renderer will copy. (§ .working wireframes A3-M and customer header; Key Flows › Flow 7, UJ-1)
A3-M uses shop-us-2 / C-0450 / 03:00–05:00 with the customer approving at 02:05, while Flow 7 uses shop-us-1 / 01:00–03:00 / 23:58. The customer wireframe header labels the memory-leak scenario "UJ-2" (it is UJ-1). The spines-win rule covers this, but the three mocks being rendered may inherit it.
Fix: align the wireframe text with Flow 7 and UJ-1 when promoting.

**[Bloat & overspecification]** — The Authorisation & approvals table and the Privacy & outbound channels table restate FR-21 and FR-6/PRIV-9 at length. (§ EXPERIENCE.md › Authorisation & approvals, Privacy & outbound channels)
The UX additions (queue labels, surfaces, "what No means" copy) earn their place; the restated rule text does not.
Fix: cite the FR for the rule and keep only the UX layer.

**[Bloat & overspecification]** — The "Pending PRD changes" paragraph is a work queue for `bmad-prd`, not something a downstream consumer reads. (§ EXPERIENCE.md › Open items, last paragraph)
Fix: move it to `.working/open-items-2026-11-03.md` and the memlog.

**[Bloat & overspecification]** — DESIGN.md Components prose repeats pixel values the tokens carry (§ DESIGN.md › Components)
DESIGN.md › Components prose repeats pixel values the tokens already carry ("4px left border", "3px left bar", "1.5px … outline", "3px … 2px offset").
Fix: reference the token, or accept it as readable restatement.

**[Inheritance discipline]** — The spines intentionally diverge from the current PRD (§ EXPERIENCE.md › State Patterns › Freshness, Open items › Pending PRD changes)
The spines intentionally diverge from the current PRD: the heartbeat is required (PRD FR-6, PRIV-9 and NFR-4 still say optional, and addendum "For the UX" still lists the two dropped status texts); unanswered requests don't expire; FR-52 gets a time window; and onboarding defaults change. This is tracked, but an architecture reader taking PRD and spines together meets conflicting rules.
Fix: run the queued `bmad-prd` Update before architecture starts, or point architecture at the spine for these items.

**[Inheritance discipline]** — Customer screens prefix "Severity:" and "Repair status:", but the spine gives no prefix for incident status. (§ Component Patterns › Status chips)
The wireframes show "Status: Waiting for customer".
Fix: name the customer label for incident status.

**[Inheritance discipline]** — "Incident status" is broader than the PRD's "incident" (§ State Patterns › Severity, statuses and risk)
"Incident status" covers every problem (an informational disk cleanup included), while the PRD Glossary defines an *incident* as a user-facing disruption and a *problem* as any fault, failure or incident. The term is inherited from the PRD addendum, so this is noted rather than to be fixed here.
Fix: none needed now; flag it for the PRD glossary.

**[Inheritance discipline]** — Weak citations. (§ State Patterns › Freshness; IA › A2)
Freshness cites "(FR-4, FR-6)", but FR-4 is Nightshift's self-monitoring and the freshness rule is the pending FR-15 change. A2 cites "Danny, Exchange 5", but no Danny Q&A file is in `sources` (`.working/extract-challenge-danny.md` exists).
Fix: cite the pending FR-15 change, and add the Danny extract to sources or drop the citation.

**[Accessibility reviewer]** — The focus ring is the same colour as the primary button. (§ DESIGN.md › Colors `focus-ring` = `primary` `#2B59C3`; dark `#8AB0FF` vs `#6E9BF5`)
Computed ring vs button fill 1.00:1 light, 1.27:1 dark: visibility depends entirely on the 2px offset gap; any container that clips the outline (overflow hidden, edge of a card) makes the focused primary button look unchanged.
Fix: use a two-tone ring (2px `surface` inner + 3px `focus-ring` outer, e.g. box-shadow) or `text-primary` for focus on primary-filled controls; state "outlines are never clipped".

**[Accessibility reviewer]** — Hatching is too faint on rows and too busy behind text. (§ DESIGN.md › stale row hatch, stale hatch; memlog L10 "stale states must be obvious")
Computed stripe vs base: row hatch 1.16:1 / 1.20:1, chip/panel hatch 1.24:1 / 1.37:1, so the row hatch is nearly invisible on many monitors (the chip and words carry it, so no WCAG failure), while a full 5px diagonal pattern under the stale panel's sentence hurts reading for low-vision and dyslexic users.
Fix: put the hatch on a left band or header strip and set the text on a solid `neutral-fill` plate; add the stale left bar in `neutral-line` to rows.

**[Accessibility reviewer]** — Times lack a time zone and use mixed formats. (§ EXPERIENCE.md › Exact labels "Valid until 02:44", "Asked 02:13"; UJ-4 "2:25 AM"; Manual "tonight 01:00–03:00")
A customer in a different zone from Orvex or the cluster can't tell when an approval runs out. On WCAG 2.2.1: approval validity limits a decision already given, not the user's time to act (unanswered requests never expire), so 2.2.1 doesn't apply; the manual window is an essential real-world constraint.
Fix: show times in the viewer's zone with the zone on decision screens ("Valid until 02:44 (your time, CET)"), one format per audience, and machine-readable `<time>`.

**[Accessibility reviewer]** — Motion is not addressed. (§ DESIGN.md has no motion section; EXPERIENCE.md › Live data, Progress steps)
Implementers may add pulsing Critical chips, spinners or auto-scroll.
Fix: add a rule: no flashing or pulsing status; transitions ≤200 ms and none under `prefers-reduced-motion`; no auto-scroll on new rows; "Nightshift is checking" uses text and a static or reduced-motion-safe indicator.

**[Adversarial reviewer]** — "Valid until 02:44" overpromises, and repeated re-asks invite rubber-stamping. (§ Voice and Tone › Exact labels "After Approve")
*Scenario:* a material change cancels the approval at 02:20, although the screen promised 02:44. Being asked again at 03:00 for Orvex's delay teaches people to approve without reading.
Fix: "Valid until 02:44, or sooner if the situation changes." Every repeat request opens with what is different since last time.

**[Adversarial reviewer]** — Wording drift around "Orvex" and "checking". (§ Voice and Tone › Exact labels "Customer approved; waiting for Orvex review"; Key Flows › UJ-2 step 4 "He is told Orvex is checking it"; "Nightshift is checking")
*Scenario:* "Orvex is checking" tells Cris someone is already looking when nobody has seen it yet, and "review" and "technical approval" read as two different steps.
Fix: always say "Waiting for Orvex technical approval". Use "checking" only for Nightshift's verification.

**[Adversarial reviewer]** — **Accept this change** sits beside **Read what changed**. (§ Privacy & outbound channels › "Agreed management policy")
*Scenario:* an administrator accepts a change that widens permissions without opening it.
Fix: put **Accept this change** inside the change detail, below what it widens.

**[Adversarial reviewer]** — A3 doesn't show that the tick matches the catalogue version. (§ Key Flows › UJ-3 step 4)
*Scenario:* Josh approves a ticked repair, assuming the 12 Oct tick covers restart-only-replica v3. The executor then blocks it because the tick needs renewing.
Fix: "Ticked by Samira on 12 Oct for v3 (current)", or "Tick needs renewing: v4 changed the conditions".

**[Adversarial reviewer]** — The morning summary flattens who permitted what. (§ Key Flows › UJ-4 step 3 "Authorised by you. Worked.")
*Scenario:* a risky ticked rollback also had Orvex technical approval, but the summary credits only the customer, which weakens FR-34's "who permitted it".
Fix: "Ticked by you on 12 Oct · Orvex technical approval by Josh at 02:20 · Worked."

**[Adversarial reviewer]** — The wording for a withdrawn request isn't drafted, including when the customer's approval was waiting. (§ State Patterns › Surface states "Request withdrawn")
*Scenario:* Cris approved, the problem went away and the buttons vanished. He can't tell whether his approval was used.
Fix: "The problem went away at 02:30. Your approval wasn't used and has been cancelled. Nothing was changed."

## Mechanical notes
- **Names:** the 16 component names are identical across DESIGN.md › Components, the DESIGN.md frontmatter keys (kebab-case equivalents) and EXPERIENCE.md › Component Patterns. "Focus" is a DESIGN.md › Components entry only, which is correct since it is an interaction primitive in EXPERIENCE.md.
- **Token references:** 62 in DESIGN.md and 10 in EXPERIENCE.md, 0 unresolved. 68 colour tokens, each light token with a `-dark` twin and none orphaned. Defined but never referenced by `{…}`: `colors.background` (used by name in prose), `typography.console-title`, `typography.customer-title`, and spacing scale `1`–`8`. That is harmless, but the title roles have no component consumer.
- **Hex parity:** every colour value in DESIGN.md matches `.working/color-themes-1.html` (Graphite Ledger v1 comment block and `.t-v1-light` / `.t-v1-dark` variables). The radii 4px (`--rc`) and 10px (`--rk`) match; 5px and 8px are derived and marked [ASSUMPTION].
- **Frontmatter:** both spines have `status: draft`, `created`, `updated` and 9 `sources` that resolve on disk. DESIGN.md has `description`; EXPERIENCE.md has none, as in the examples. `{planning_artifacts}` paths are quoted for YAML.
- **Cross-references:** EXPERIENCE.md › IA A5 lists filters in parentheses and then "Columns:", which is ambiguous on first read; label the parenthesised list "Filters:". A3-M's internal numbering (time window as row 9, approvals as row 10) matches the console wireframe.
- **Mermaid:** none in either spine.
- **Visual sources:** links point into `.working/` (acceptable before Finalize; promote and relink). `mockups/` and `wireframes/` don't exist yet, and `imports/` is empty.

## Reviewer files
- `review-rubric.md`
- `review-accessibility.md` (includes the full computed contrast table)
- `review-adversarial.md`
