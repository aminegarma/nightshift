---
review: accessibility
target: DESIGN.md, EXPERIENCE.md (status draft, 2026-11-03)
standard: WCAG 2.2 AA plus practical use (phone at 3 AM; dense desktop console)
date: 2026-11-03
---

# Accessibility review: Nightshift UX spines

## Verdict

**Not ready to finalise; the palette is sound, the behaviour is the risk.** Every load-bearing text pair in Graphite Ledger passes AA in light and dark except one (`text-secondary` on the dark stale-hatch stripe, 4.28:1), and the palette sheet's stated ratios check out. Colour is consistently backed by words. The real gaps are behavioural: consequential one-tap decisions with no undo or confirmation on a phone, content that can change under the user's thumb on the approval screen, an undefined path from a 3 AM phone call to the portal (and none for people who can't hear a call), unconstrained sign-in/step-up, and a ten-section approval screen in partly technical language. Most of the Accessibility Floor is still `[ASSUMPTION]`, and screen-reader behaviour for live data, chips and progress steps is unspecified.

Counts: 1 critical · 6 high · 12 medium · 4 low.

## Findings

### Critical

- **[critical]** Approve and Reject are irreversible single taps on a phone with no confirmation, no undo and no withdrawal (EXPERIENCE.md › Interaction Primitives "Decisions commit on one tap; the result screen is the confirmation"; Component Patterns › Primary button, Secondary button "Reject commits on one tap… no extra dialog"; DESIGN.md › Layout "full-width buttons at the end"). The buttons are stacked full-width at the bottom of a long scroll, 12px apart, used one-handed by a half-awake non-expert. Reject is the worse case: it blocks the repair and "won't ask for this repair again on its own", so a stray tap at 02:15 can leave checkout to fail at 06:00. A safe, not-ticked repair needs only the customer's approval (Authorisation table), so a stray Approve runs a production change with no second human. WCAG 3.3.4 (Error Prevention: reversible, checked or confirmed) is the closest criterion and the spines meet none of its three options. *Fix:* keep one tap, but make it reversible: after either tap, show the result screen with an **Undo** (e.g. 10–15 s, decision not sent until it lapses) and, for Approve, "Withdraw my approval" until the repair starts; record withdrawals in history. If undo is architecturally hard, use a bottom-sheet confirmation that restates action, target and interruption ("Restart checkout-api now? Checkout may be down 30–60 s.") with the confirm button in the same position as the original. Also add at least 24px between Approve and Reject on phone.

### High

- **[high]** The approval screen can change or disappear while the user is reading it (EXPERIENCE.md › Approval validity "always shows current evidence… re-issued if the evidence or conditions materially change… withdrawn if the problem resolves"; State Patterns › Surface states "Request re-issued: current evidence replaces the old", "Request withdrawn: …no buttons remain"; Interaction Primitives › Live data "Panels refresh on their own"). If evidence is swapped in place, a person who read version 1 can tap Approve on version 2 (the Glossary ties approval to "evidence shown"); if buttons vanish, keyboard and screen-reader focus is lost to the page body and the thumb lands on whatever moved up (WCAG 3.2.2 / 3.2.5 spirit, 2.4.3). *Fix:* never mutate B3/B3-M/A3/A3-M content in place. Freeze the version on screen, show a polite, persistent banner "This request has changed. Review the new version" (role=status, announced once), disable both buttons until the new version is opened, and send the version ID with the decision so the server rejects a stale one. On withdrawal, replace the buttons with a sentence ("The problem went away at 02:31; nothing to decide") and move focus to it.

- **[high]** The phone call that wakes a Critical-severity customer has no designed route to the portal, and Critical relies on a voice call alone (EXPERIENCE.md › State Patterns › Severity "Critical → Phone call"; Information Architecture › Slack notification "(and phone call)"; Surface → journey closure "Phone-call content is not designed [OPEN: architecture A11]"; UJ-2 step 2 "He opens the request in the portal", Flow 7 step 2). A call carries no link, so Cris must find the portal, sign in and locate the request himself at 3 AM; a Deaf or hard-of-hearing owner gets no usable Critical alert at all. *Fix:* state in the spines that every Critical call is paired with a text notification (SMS/push/Slack) carrying the deep link, that the call says so ("We've sent you a link by text") and offers to repeat, and that B1 opens with "Needs your decision" first after sign-in (already true). Let the customer choose text-only for Critical in B6b.

- **[high]** Sign-in and step-up authentication sit on the critical path of every approval but carry no accessibility constraint (EXPERIENCE.md › Interaction Primitives "Notifications deep-link through sign-in… Step-up authentication and approver roles [OPEN: architecture]"; Open items A5). WCAG 2.2 3.3.8 Accessible Authentication (Minimum) forbids cognitive function tests (remembering or transcribing codes) without an alternative; a portal session that expires while a screen-reader or magnifier user works through ten sections, then bounces Approve to a sign-in page, breaks 2.2.1 and loses the decision. *Fix:* add to the Accessibility Floor: sign-in and step-up allow password managers and paste, offer passkeys or a device prompt, never require transcribing a code without a copy/paste or autofill path; deep links survive sign-in and land on the same request version; if the session will expire on B3/B3-M/A3, warn at least 20 s ahead with "Stay signed in", and after re-authentication return to the request with the pending decision preserved (never auto-submitted).

- **[high]** The customer approval screen asks a non-expert to process ten (B3) or eleven (B3-M) sections before reaching the decision, partly in infrastructure language (EXPERIENCE.md › Component Patterns › Approval card "B3 order: 1… 10", Manual-repair panel "B3-M order: 1… 11"; Key Flows UJ-1 step 4 "restart checkout-api (its only replica)", Flow 7 "stable on the standby interface", "node n-7"; Voice and Tone "Orvex technical approval", "repair catalogue", "rollback"). The content is right (memlog L11 requires it before approving), but there is no at-a-glance summary and no plain-language gloss for "replica", "rollback", "catalogue", "node", "checkout-api" or "Orvex technical approval". *Fix:* add a three-line "What we're asking" summary directly under the lead sentence (action in plain words · expected interruption · what happens if you do nothing) with a "Go to decision" link; keep sections 1–9 in order but let 6 (Recovery plan) and 7 (Evidence) open as expandable sections with a one-line summary each; add a short plain-words gloss in the repair line ("Restart the checkout program (there's only one copy running, so checkout pauses briefly)"); rename "Orvex technical approval" for customers to "Orvex engineer's check". Write the gloss rules into Voice and Tone.

- **[high]** Consequential console and settings actions also commit on one click: **Approve rollback for these 300 clusters** and **Accept this change** (which widens what Nightshift may do in production) (EXPERIENCE.md › Interaction Primitives "Decisions commit on one tap"; UJ-5 step 5; Privacy & outbound channels › Agreed management policy). "Accept this change" modifies the customer's stored permissions, squarely the data-modification case of WCAG 3.3.4; the fleet approval has the largest blast radius in the product. *Fix:* for the fleet approval, a confirmation step that restates counts ("300 clusters · 112 will still wait for their customer · runs in 6 waves") with the confirm control in place; for policy acceptance, a review-then-confirm step plus "Undo acceptance" while nothing has yet run under it. Record either in history.

- **[high]** Live refresh in the console has no pause and no rule for focus or re-sorting (EXPERIENCE.md › Interaction Primitives › Live data "[ASSUMPTION] Panels refresh on their own"; Component Patterns › Attention-queue row "Sort: customer impact, then time to impact"). A queue that re-sorts as times to impact change moves the row under the pointer or keyboard focus; a screen-reader user loses their place on every refresh. WCAG 2.2.2 (Pause, Stop, Hide) applies to auto-updating content shown alongside other content. *Fix:* keep focus on the same item across refreshes; don't re-order rows while focus or pointer is in the table: show "3 changes · Show" (role=status, announced once) and apply on request; add a visible "Pause live updates" toggle per page that also pauses the freshness counters; never steal focus on refresh.

### Medium

- **[medium]** Live text will over-announce or not announce at all; the spines don't say which (EXPERIENCE.md › Accessibility Floor "status changes… are announced to screen readers" [ASSUMPTION]; Component Patterns › Freshness line "every panel and card"; DESIGN.md › Freshness line "Updated 40 s ago"). A freshness line on every panel ticking each second, if marked live, makes a console page unusable with a screen reader; if not, the stale transition is silent. *Fix:* specify: freshness lines are plain text, never live regions; one polite live region per page announces only state transitions (current → out of date, repair status changes, "Needs your decision (n)" count changes), debounced and batched ("2 panels out of date: eu-2, eu-4"); customer view spells units out ("Updated 40 seconds ago").

- **[medium]** Progress steps show the current step by chip styling only, and join steps with "→" (DESIGN.md › Components › Progress steps "Repair-status words joined by arrows, current step as its chip"; EXPERIENCE.md › Component Patterns › Progress steps). "Which step are we on" is conveyed by visual treatment alone (WCAG 1.3.1, 1.4.1), and screen readers read "right arrow" between words. *Fix:* render as an ordered list with arrows decorative (aria-hidden); mark the current step with `aria-current="step"` and a visible word ("Now: Verifying"); mark completed steps with a visible tick plus hidden "done". Same for the A4 wave strip ("Wave 2: running").

- **[medium]** Most of the Accessibility Floor is still an assumption (EXPERIENCE.md › Accessibility Floor: "[ASSUMPTION] Target WCAG 2.2 AA", "[ASSUMPTION] Tap targets ≥44px", "[ASSUMPTION] Keyboard-operable… announced… 200%"; DESIGN.md button min-height "[ASSUMPTION]"). Downstream builders can drop assumptions. *Fix:* have Amine decide them and remove the tags; add the missing floor items from this review (authentication, live regions, reduced motion, undo, help, zoom).

- **[medium]** The console has no zoom or reflow rule beyond tables (EXPERIENCE.md › Responsive & Platform "Desktop web, wide screens only… No phone layout in v1"; DESIGN.md › Layout "Problem detail puts Verified facts and Nightshift's explanation side by side"; Typography console-column-label 11px uppercase, console-chip and console-mono 12px). WCAG 1.4.10 exempts the data tables but not the summary tiles, panels, A2/A3 detail and A4 steps at 400% zoom (1280px → 320 CSS px); 11px uppercase labels are hard going for a tired engineer. *Fix:* state that non-table console content reflows to one column below ~700 CSS px (A2 blocks stack: facts first), tables keep horizontal scroll with a sticky first column, and the minimum console text is 12px with column labels in sentence case or ≥12px.

- **[medium]** Customer chips may not reflow at 200% text on a 360px phone (EXPERIENCE.md › Accessibility Floor "text scales to 200%" [ASSUMPTION]; DESIGN.md › customer-chip 15px/600; Component Patterns "customer screens prefix the field ('Repair status: Waiting for approval')"; the palette sheet's chip CSS uses `white-space: nowrap`). At 30px, "Repair status: Waiting for approval" is wider than the 320px content box, forcing horizontal scroll (1.4.4, 1.4.10). *Fix:* state that customer chips wrap (no nowrap, min-height not fixed height), buttons grow in height with their label, and IDs and cluster names break; test B3 at 200% text and 1.4.12 text spacing.

- **[medium]** Clickable cards and tiles are bounded only by the faint `border`, against DESIGN.md's own rule (DESIGN.md › Colors "`border`… never a control's only outline"; Components › Summary tile `1px {colors.border}` while EXPERIENCE.md says "Click filters to or opens the matching items"; B1 cluster card and "Needs your decision" card are tappable per IA "Cluster card → B2"). Computed: border vs background 1.34:1 light / 1.68:1 dark; surface vs background 1.10:1 in both. *Fix:* give every clickable card or tile either a `text-secondary` outline or an explicit affordance in `primary` text ("Review ›", "Open ›") that names the action; the outline is simplest and consistent with the rule.

- **[medium]** Last-known values on a stale panel fail AA in dark mode (DESIGN.md › Components › Freshness line "text-secondary, on every panel and card", Stale panel "stale hatch… Does not hide the last known values" in EXPERIENCE.md › Component Patterns › Stale panel). Computed `text-secondary-dark` `#A3A9B3` on `stale-hatch-stripe-dark` `#3E4248` = **4.28:1** (< 4.5). Light passes (5.19:1). *Fix:* on stale surfaces use `neutral-ink` (5.64:1 on the dark stripe) for all text including the freshness line, or lighten the dark stripe to ≤ `#383B41`, and say so in the Stale panel component.

- **[medium]** Several interactive states have no tokens: links, error messages, disabled, checked tick/radio fill, selected/hover row (DESIGN.md frontmatter `colors` and › Components; EXPERIENCE.md uses inline links "Ticked in your settings on 12 Oct", "See full activity", "Read the policy", and an error state "Decision not recorded"). Without a link style, links in body text may be colour-only (1.4.1) or invisible; without an error style, the one error that matters most is undesigned. *Fix:* add `link` (= `primary`, always underlined in body text), `error` (reuse critical ink/fill with an icon and the word "Not recorded"), `checked` (`primary` fill, `primary-ink` mark, ≥3:1), and a selected-row treatment that isn't colour-only (left bar + `aria-selected`).

- **[medium]** The 100-tile health grid has no keyboard, screen-reader or target-size spec, and two tile states lack a visual (DESIGN.md › Health-grid tile; EXPERIENCE.md › Health-grid tile "[ASSUMPTION] Clicking a tile with a problem opens its A2", tile "Heartbeat OK · Fleet reports not permitted"). 100 tab stops is unusable; tiles named only "C" or "W" are meaningless to a screen reader; the "Fleet reports not permitted" tile has no token at all, and the stale tile has no letter (hatch alone at tile size is easy to miss). *Fix:* one tab stop with arrow-key navigation (grid pattern) or a "Show as list" toggle; accessible name per tile ("shop-eu-1: critical problem; opens problem"); tiles ≥24×24 CSS px (2.5.8); give stale tiles a letter ("?") and define the fleet-reports-off tile (e.g. surface with dashed `text-secondary` outline and "F").

- **[medium]** Focus and announcements after a decision or a failed decision are unspecified (EXPERIENCE.md › Component Patterns › Primary button "the next screen confirms the result"; State Patterns › "Decision not recorded… offers to try again" [ASSUMPTION]). Screen-reader users won't know the decision landed or failed (4.1.3, 2.4.3). *Fix:* after a decision, move focus to the result heading ("You approved at 02:14"); on failure, keep the request, show the error next to the buttons with role=alert, keep focus on a "Try again" button, and never show both an error and a success.

- **[medium]** No help or contact route on the customer decision screens (EXPERIENCE.md › Information Architecture › B3, B3-M; Component Patterns › Approval card order). A non-expert unsure at 3 AM has no way to ask Orvex; WCAG 2.2 3.2.6 (Consistent Help) requires any help mechanism to sit in the same place across pages. *Fix:* add a fixed "Talk to Orvex on-call" (phone/chat) entry in the same position on B1–B5, and on B3/B3-M next to the "If you don't answer" section.

- **[medium]** Console table semantics are unspecified (EXPERIENCE.md › A1 attention queue columns and sort; A5 "Filterable table… Dropdown filters"; Component Patterns "Click opens A2"). Whole-row click handlers are not keyboard- or screen-reader-reachable; sort order and filter results aren't announced; the A2 header chips ("Critical", "Needs attention") lack the field name the customer view adds. *Fix:* real `<table>` with `<caption>` and `<th scope>`; the "Customer impact" cell is the row's link; `aria-sort` on the sorted column and a visible "Sorted by customer impact, then time to impact"; announce filter results ("12 rows"); visually hidden field prefixes on chips outside table cells.

### Low

- **[low]** The focus ring is the same colour as the primary button (DESIGN.md › Colors `focus-ring` = `primary` `#2B59C3`; dark `#8AB0FF` vs `#6E9BF5`). Computed ring vs button fill 1.00:1 light, 1.27:1 dark: visibility depends entirely on the 2px offset gap; any container that clips the outline (overflow hidden, edge of a card) makes the focused primary button look unchanged. *Fix:* use a two-tone ring (2px `surface` inner + 3px `focus-ring` outer, e.g. box-shadow) or `text-primary` for focus on primary-filled controls; state "outlines are never clipped".

- **[low]** Hatching is too faint on rows and too busy behind text (DESIGN.md › stale row hatch, stale hatch; memlog L10 "stale states must be obvious"). Computed stripe vs base: row hatch 1.16:1 / 1.20:1, chip/panel hatch 1.24:1 / 1.37:1, so the row hatch is nearly invisible on many monitors (the chip and words carry it, so no WCAG failure), while a full 5px diagonal pattern under the stale panel's sentence hurts reading for low-vision and dyslexic users. *Fix:* put the hatch on a left band or header strip and set the text on a solid `neutral-fill` plate; add the stale left bar in `neutral-line` to rows.

- **[low]** Times lack a time zone and use mixed formats (EXPERIENCE.md › Exact labels "Valid until 02:44", "Asked 02:13"; UJ-4 "2:25 AM"; Manual "tonight 01:00–03:00"). A customer in a different zone from Orvex or the cluster can't tell when an approval runs out. On WCAG 2.2.1: approval validity limits a decision already given, not the user's time to act (unanswered requests never expire), so 2.2.1 doesn't apply; the manual window is an essential real-world constraint. *Fix:* show times in the viewer's zone with the zone on decision screens ("Valid until 02:44 (your time, CET)"), one format per audience, and machine-readable `<time>`.

- **[low]** Motion is not addressed (DESIGN.md has no motion section; EXPERIENCE.md › Live data, Progress steps). Implementers may add pulsing Critical chips, spinners or auto-scroll. *Fix:* add a rule: no flashing or pulsing status; transitions ≤200 ms and none under `prefers-reduced-motion`; no auto-scroll on new rows; "Nightshift is checking" uses text and a static or reduced-motion-safe indicator.

## Checked and fine

- All status ink-on-fill pairs, both block bodies (Verified facts, explanation), button labels, text on all three neutral surfaces and the focus ring against `background`/`surface`/`surface-raised` pass AA in both modes; the palette sheet's stated ratios match the computed ones to 0.01.
- Colour is never the only signal: every chip carries its word, customer chips add the field name, grid tiles carry C/W plus a legend, stale states are labelled. Same-lightness fills (e.g. Running vs Waiting, 1.00:1; Critical vs Warning tile fill, 1.01:1) are fine because the word or letter differs.
- Controls outlined in `text-secondary` (7.56:1 / 6.83:1) meet 1.4.11; severity bars (≥7.7:1) are redundant with the severity chip.
- Button labels are specific and unique ("Approve this repair", not "OK"); Reject is not styled as dangerous or disabled.
- Unanswered requests never expire, so there is no hidden timer on the decision itself.

## Contrast table (computed, WCAG 2.x relative luminance)

Light = light-mode pair, Dark = `-dark` twins. "Need": 4.5 for text, 3 for non-text (UI boundaries, focus indicators); "-" = informational (pattern or hue distinction, not a WCAG pair).

| Pair | Light | Dark | Need | Result |
|---|---|---|---|---|
| text-primary / background | `#111827`/`#F3F4F6` **16.12** | `#E8EAED`/`#16181C` **14.75** | 4.5 | Pass |
| text-primary / surface | `#111827`/`#FFFFFF` **17.74** | `#E8EAED`/`#1E2126` **13.39** | 4.5 | Pass |
| text-primary / surface-raised | `#111827`/`#F9FAFB` **16.98** | `#E8EAED`/`#262A30` **11.96** | 4.5 | Pass |
| text-secondary / surface | `#4B5563`/`#FFFFFF` **7.56** | `#A3A9B3`/`#1E2126` **6.83** | 4.5 | Pass |
| text-secondary / background | `#4B5563`/`#F3F4F6` **6.87** | `#A3A9B3`/`#16181C` **7.52** | 4.5 | Pass |
| text-secondary / surface-raised (table headers) | `#4B5563`/`#F9FAFB` **7.23** | `#A3A9B3`/`#262A30` **6.10** | 4.5 | Pass |
| primary-ink / primary (button label) | `#FFFFFF`/`#2B59C3` **6.33** | `#0E1420`/`#6E9BF5` **6.73** | 4.5 | Pass |
| primary / surface (button edge, link-as-text) | `#2B59C3`/`#FFFFFF` **6.33** | `#6E9BF5`/`#1E2126` **5.90** | 3 | Pass |
| primary / background | `#2B59C3`/`#F3F4F6` **5.75** | `#6E9BF5`/`#16181C` **6.49** | 3 | Pass |
| focus-ring / background | `#2B59C3`/`#F3F4F6` **5.75** | `#8AB0FF`/`#16181C` **8.24** | 3 | Pass |
| focus-ring / surface | `#2B59C3`/`#FFFFFF` **6.33** | `#8AB0FF`/`#1E2126` **7.48** | 3 | Pass |
| focus-ring / surface-raised | `#2B59C3`/`#F9FAFB` **6.05** | `#8AB0FF`/`#262A30` **6.68** | 3 | Pass |
| focus-ring / primary (ring vs button fill) | `#2B59C3`/`#2B59C3` **1.00** | `#8AB0FF`/`#6E9BF5` **1.27** | 3 | FAIL both |
| focus-ring / critical-fill (adjacent grid tile) | `#2B59C3`/`#FDE8E8` **5.39** | `#8AB0FF`/`#3D1A1C` **7.14** | 3 | Pass |
| focus-ring / stale-hatch-stripe | `#2B59C3`/`#D4D6D9` **4.34** | `#8AB0FF`/`#3E4248` **4.69** | 3 | Pass |
| border / surface (divider) | `#D1D5DB`/`#FFFFFF` **1.47** | `#3A3F47`/`#1E2126` **1.52** | 3 | FAIL both |
| border / background (card edge on page) | `#D1D5DB`/`#F3F4F6` **1.34** | `#3A3F47`/`#16181C` **1.68** | 3 | FAIL both |
| surface / background (card tone) | `#FFFFFF`/`#F3F4F6` **1.10** | `#1E2126`/`#16181C` **1.10** | 3 | FAIL both |
| text-secondary outline / surface (controls) | `#4B5563`/`#FFFFFF` **7.56** | `#A3A9B3`/`#1E2126` **6.83** | 3 | Pass |
| critical ink / fill | `#9B1C1C`/`#FDE8E8` **6.94** | `#FFA8A8`/`#3D1A1C` **8.38** | 4.5 | Pass |
| warning ink / fill | `#8A3B0C`/`#FDEBD8` **6.66** | `#FFC08A`/`#3B2614` **8.93** | 4.5 | Pass |
| info ink / fill | `#1E429F`/`#E3ECFB` **7.56** | `#A9C6FF`/`#182A47` **8.36** | 4.5 | Pass |
| waiting ink / fill | `#5B32B4`/`#EDE9FB` **6.89** | `#CDB8FF`/`#2A2045` **8.55** | 4.5 | Pass |
| success ink / fill (also Verified facts body) | `#146C3A`/`#E1F3E8` **5.62** | `#8FE0AE`/`#15301F` **9.12** | 4.5 | Pass |
| explanation ink / fill (explanation body) | `#6B4E00`/`#FCF4CF` **6.99** | `#F2D675`/`#3A3112` **9.00** | 4.5 | Pass |
| neutral ink / fill | `#444B55`/`#ECEDEF` **7.52** | `#BCC2CB`/`#2A2D33` **7.70** | 4.5 | Pass |
| text-secondary / success-fill (freshness line in facts block) | `#4B5563`/`#E1F3E8` **6.55** | `#A3A9B3`/`#15301F` **6.02** | 4.5 | Pass |
| text-secondary / explanation-fill | `#4B5563`/`#FCF4CF` **6.83** | `#A3A9B3`/`#3A3112` **5.46** | 4.5 | Pass |
| text-primary / critical-fill (critical summary tile count) | `#111827`/`#FDE8E8` **15.11** | `#E8EAED`/`#3D1A1C` **12.78** | 4.5 | Pass |
| text-secondary / critical-fill (tile sub-line) | `#4B5563`/`#FDE8E8` **6.44** | `#A3A9B3`/`#3D1A1C` **6.52** | 4.5 | Pass |
| text-secondary / info-fill (freshness on info card) | `#4B5563`/`#E3ECFB` **6.35** | `#A3A9B3`/`#182A47` **6.08** | 4.5 | Pass |
| neutral ink / stale-hatch-base | `#444B55`/`#ECEDEF` **7.52** | `#BCC2CB`/`#2A2D33` **7.70** | 4.5 | Pass |
| neutral ink / stale-hatch-stripe | `#444B55`/`#D4D6D9` **6.05** | `#BCC2CB`/`#3E4248` **5.64** | 4.5 | Pass |
| text-secondary / stale-hatch-stripe | `#4B5563`/`#D4D6D9` **5.19** | `#A3A9B3`/`#3E4248` **4.28** | 4.5 | FAIL dark |
| text-primary / stale-row-stripe | `#111827`/`#EDEEEF` **15.27** | `#E8EAED`/`#2B2F34` **11.18** | 4.5 | Pass |
| text-secondary / stale-row-stripe | `#4B5563`/`#EDEEEF` **6.51** | `#A3A9B3`/`#2B2F34` **5.70** | 4.5 | Pass |
| hatch stripe / hatch base (pattern visibility) | `#D4D6D9`/`#ECEDEF` **1.24** | `#3E4248`/`#2A2D33` **1.37** | - | info |
| row stripe / row base (pattern visibility) | `#EDEEEF`/`#FFFFFF` **1.16** | `#2B2F34`/`#1E2126` **1.20** | - | info |
| critical-line / surface (3px severity bar) | `#9B1C1C`/`#FFFFFF` **8.15** | `#FFA8A8`/`#1E2126` **8.78** | 3 | Pass |
| warning-line / surface | `#8A3B0C`/`#FFFFFF` **7.74** | `#FFC08A`/`#1E2126` **10.12** | 3 | Pass |
| info-line / surface | `#1E429F`/`#FFFFFF` **8.99** | `#A9C6FF`/`#1E2126` **9.39** | 3 | Pass |
| critical-fill / surface (grid tile fill) | `#FDE8E8`/`#FFFFFF` **1.17** | `#3D1A1C`/`#1E2126` **1.05** | - | info |
| warning-fill / critical-fill (C vs W tile by colour) | `#FDEBD8`/`#FDE8E8` **1.01** | `#3B2614`/`#3D1A1C` **1.08** | - | info |
| info-fill / waiting-fill (Running vs Waiting chip by colour) | `#E3ECFB`/`#EDE9FB` **1.00** | `#182A47`/`#2A2045` **1.05** | - | info |
| primary / info-ink (button vs blue chip ink) | `#2B59C3`/`#1E429F` **1.42** | `#6E9BF5`/`#A9C6FF` **1.59** | - | info |

Notes on the "FAIL" rows: `border` and the surface/background tone fail 3:1 by design and are acceptable as dividers only; they become findings only where a clickable card or tile relies on them (see medium findings). The focus ring vs primary fill passes only through the 2px offset gap (see low findings). `text-secondary` on the dark stale stripe (4.28:1) is a real text failure (see medium findings).
