# Applied changes: architecture-orvex.md review follow-up (2026-11-15)

Scope: Amine's decision of 2026-11-15 (apply editorial changes; document answers that follow existing decisions; bring new behaviour to Amine). Only `architecture-orvex.md` was edited.

- **Backup of the previous version:** `/tmp/claude-1000/-home-amine-nightshift/4c1d45da-342e-4062-9ddd-1d25a6f0e645/scratchpad/architecture-orvex.before-review-edits.md` (scratchpad; not durable).
- **Word count (`wc -w`, including tables and diagrams):** 11,623 before, about 12,490 after. The editorial cuts were outweighed by the answers and stated limits added under B and the cost totals.

## 1. Structure (lens-structure.md)

| Row | Applied as |
|---|---|
| ADD bottom line in §1 | "Bottom line" paragraph at the top of §1: nothing tested, cost result under assumptions, top Orvex dependencies; links to 11, 12, 13.2 |
| ADD reading guide | "15-minute walkthrough" line under the header |
| ADD id sources to legend | New "Ids" line: AD, AP (Appendix B), FR/NFR/SEC/PRIV/COST/SM, O-n (UX open items), M2, D and G |
| MOVE: split §4 | §4 Trust and approvals (4.1–4.9); new §5 Security boundaries and outbound data (5.1 boundaries, 5.2 flows, 5.3 compromise cases); later sections renumbered 6–13 |
| MOVE group approvals | Old 7.6 is now 4.4 (after option B); pointer left in the Fleet services table (8.1) |
| MERGE old 4.9 into signing section | Now one bullet in 4.9 ("Relay, registry and group-confirmation service carry no authority") |
| CONDENSE gateway-bypass restatements | Full statement kept in 5.1 and AP-8; §2.2 is a pointer; §1 item 7 points to 5.1 |
| MOVE inline evidence runs (§2.3, §5) | Replaced by compact "Sources" notes pointing to tool-comparison.md §3–§5, keeping the links not covered there |
| CONDENSE §6.6 input table | Input table condensed into one sentence in 7.6; derived table kept. **Deviation:** not moved to cost-model/README.md, because only this file could be edited |
| MOVE "What moves the cost most" | Now 12.1, opening the cost section |
| CUT "Decided since the last version" | Removed from 13.3 |
| QUESTION `.working/` links | Resolved per Amine: links now go to appendix-a/b/c; the only remaining `.working/` mention is one sentence in the "What this is" box |
| QUESTION offline tiers | Tiers table kept in 4.7; cross-reference added from 9.1 (and from 4.7 to 9.1) |
| CUT fine-tuned row in rejected tools | Removed |
| CONDENSE heading numbering and status labels | All subsections numbered (1.1–1.3, 10.1–10.2); "round 4", "M2", "provisional", "AP-6 pending" moved from headings into bodies |
| QUESTION failure catalogue placement | Kept after the tool choices (now §11); referenced from the §1 bottom line and the reading guide |
| PRESERVE rows | Kept: both diagrams, crash example, compromise table, registers |
| Header | Date 2026-11-15; status "draft for review (synced with spine AD-1..AD-71, final 2026-11-15)"; links to spine, failure-catalogue.md, cost-model/, tool-comparison.md and the three appendices |

All internal cross-references were renumbered (for example 4.6→4.7, 7.3→8.3, 7.6→4.4, 4.11→5.2, 12.2→13.2).

## 2. Prose (lens-prose.md)

- 4.2: 70-word condition sentence split into a seven-item list.
- 4.7 "after expiry only … leave" rewritten ("After expiry, only three things leave: …").
- Double negatives: 3.4 expired claim; 4.9 relay statements ("don't show that every stop was delivered").
- 3.4 compressed phrasing opened up ("an entry absent from the map counts as customer production"; "Any doubt selects the customer-production rules, and misclassifications count against SM-4").
- §1 main choices: "Hybrid C", "reality re-read" and "three named exceptions" replaced by defined wording.
- Missing verbs and units: "delayed accounting can't enforce a cap"; dangerous entries "carry manual steps only"; "80% input and 20% output tokens"; executor "Make any change its approved entries allow"; "after that, a person recovers through a manual runbook on the separate install path".
- 4.6 receipt pinning: the receipt *public key* is pinned at installation, signed by the first customer admin and the Orvex people-list key (AD-23).
- 5.3 audit row: "about 32 bytes" now named as a covert channel through the checkpoint fields.
- 5.2: "a flow not in the table is not allowed".
- Consistency: "Sent — not yet effective in the cluster" spelled in full everywhere; "Until AP-1 is accepted"; "Fleet reports" channel; "option B" lowercase in running text.
- Style guide: "e.g." → "for example"; "via" → "through" (including diagram labels).
- Audience: "round 4" removed from the body; "Never asked" → "Not yet asked"; "not adopted" → "not yet decided"; "Exchange 3" attributed to Orvex's answers.
- The lens file lists only its main rows; the 40 + 9 detailed rows weren't in the report, so only the listed ones were applied.

## 3. Adversarial findings (lens-adversarial.md)

| # | Finding | Disposition |
|---|---|---|
| 1 | Cluster-admin and node root missing from compromise table | **NEEDS AMINE (new behaviour):** who holds cluster-admin per platform and whether cluster keys need KMS/HSM/sealed storage isn't decided anywhere |
| 2 | Receipt shown by the portal it checks | **NEEDS AMINE (new behaviour):** in-browser receipt verification is new. Stated limit added (4.6, 5.3: a compromised portal can show a false status; receipts also appear on the local dashboard, AD-23) |
| 3 | No fence for non-delete actions | Answered from existing decision (AD-6, AD-7, AD-10; §3.2 rule 2): every mutation carries UID and resourceVersion preconditions, epoch re-read before each mutation. The old text wrongly limited this to deletes and evictions |
| 4 | Recovery retry without revalidation | Answered from existing decision (AD-7; §3.3 diagram and text): stops, then revalidate authorisation, validity, evidence before the retry. Sub-point "does a crashed attempt count as started for validity" not settled: NEEDS AMINE |
| 5 | Cluster clock rollback | **NEEDS AMINE (new behaviour):** monotonic or authenticated time and a backward-jump alarm aren't in the spine (only own clock with fixed skew, AD-25) |
| 6 | Gateway sees the SMS code | Limit stated from existing decision (AD-18; 4.3, 5.3): against a compromised gateway the code adds no proof of possession, the passkey over D still applies. **NEEDS AMINE (new behaviour):** provider-side rate, spend and template limits |
| 7 | First-admin code issuer unclear | Partly answered (AD-19; 4.5): code goes to the contract contact; Fleet pin limit stated (spine Deferred). **NEEDS AMINE (new behaviour):** who generates the code and on which channel it's shown |
| 8 | Release can break its own rollback trigger | **NEEDS AMINE (new behaviour):** dead-man's-switch probation and keeping guard and checker outside the release aren't decided (AD-45 only puts Flux outside releases) |
| 9 | Admission webhook failure policy | **NEEDS AMINE (new behaviour):** fail-open versus fail-closed, recovery-write exemption and outage test aren't decided (tool chosen at build) |
| 10 | Unanswered requests vs run quota | **NEEDS AMINE (new behaviour):** quota treatment of pending approvals not decided (AD-2 caps open runs; AD-25 requests never expire) |
| 11 | Full audit volume refuses stops | Limit stated (AD-50; 9.2): stops accepted only while audit space permits; behaviour after that isn't settled. **NEEDS AMINE (new behaviour)** |
| 12 | Inconsistent gateway exception | Editorial fix applied (5.1 fact-builder bullet now names all three AD-67 bypass paths). The fixed attention notice (AD-24) has no row in Appendix A; stated in 5.2. Adding its row and path: NEEDS AMINE |
| 13 | Dashboard vs no-inbound rule | Editorial fix applied (AD-42, AD-51; 2.2, 5.1, 9.3): rule qualified; dashboard listed as the one inbound endpoint |
| 14 | No approval latency budget | **NEEDS AMINE (new behaviour):** no budget, poll interval or SMS expiry derivation exists (values listed as to set) |
| 15 | Group assurance overstated | Limit stated (AD-48; 4.4, 5.3): clusters don't see the SMS step, so group assurance rests on the service's attestation. **NEEDS AMINE (new behaviour):** changing the recorded label or binding an SMS-session hash |
| 16 | Cost frames only Orvex's saving | Editorial fix applied (12.2): 100-cluster equality explained (round-the-clock cover); total-system rows (Orvex cash + customer footprint, sums of existing results figures) and text added; bottom line mentions it |
| 17 | Header date | Editorial fix applied: 2026-11-15, synced spine status stated |
| 18 | Rules rest on `.working/` drafts | Editorial fix applied: links now to appendices A, B, C |
| 19 | Executor node loss pauses repairs | Partly answered (AD-7; 3.2 rule 5, 3.5): epoch acquired by optimistic-concurrency write; one executor in v1, pause stated. **NEEDS AMINE (new behaviour):** Lease, shorter toleration, anti-affinity or fenced standby |
| 20 | BMC binding checked at install only | Limit stated (AD-62; 2.3). **NEEDS AMINE (new behaviour):** re-verification on every use (UUID match) |

## 4. Edge cases (lens-edge-case-hunter.json, numbered in file order)

| # | Trigger | Disposition |
|---|---|---|
| 1 | Recovery retry gets 429 or pod still runs | Answered from existing decision (AD-6; §3.3 text): verification fails, a person takes over, no further retry |
| 2 | Crash during the retry | Answered from existing decision (AD-6; §3.3): the retry writes its own intent (attempt 2), so attempts are distinguishable |
| 3 | 429 during normal execution | **NEEDS AMINE (new behaviour):** wait or back off within validity versus hand over isn't decided; doc only says never retried blindly (3.2) |
| 4 | 409, re-read shows a different UID | Answered from existing decision (AD-6, AD-17; 3.2 rule 2): a different UID is a different occurrence the approval doesn't cover |
| 5 | Expired claim can never be confirmed | Answered from existing decision (AD-6, AD-9; 3.4): unconfirmable means ambiguous, which goes to a person |
| 6 | Audit append fails before action | **NEEDS AMINE (new behaviour):** whether a failed intent append blocks the action isn't a stated rule, though "no repair runs unrecorded" implies it |
| 7 | Verification inconclusive (stale signals) | Answered from existing decision (AD-6, AD-31; 3.2 rule 4): unknown or stale never counts as success |
| 8 | Repeat cap per pod UID | **NEEDS AMINE (new behaviour):** counting per owning workload isn't decided (AD-65 says entry and target) |
| 9 | Stop arrives mid-run | **NEEDS AMINE (new behaviour):** whether a stop interrupts a multi-step repair in progress isn't decided |
| 10 | First approval lapses during re-ask | Answered from existing decision (AD-17, AD-25; 4.7): every approval must be valid at start; each lapsed approver is re-asked |
| 11 | Unanswered requests fill the quota | **NEEDS AMINE (new behaviour):** same as adversarial 10 |
| 12 | Tier age exactly 1 h or 24 h | Editorial fix applied (4.7): "up to 1 h", "over 1 h up to 24 h", "over 24 h", following the spine's wording |
| 13 | Clock jumps backward | **NEEDS AMINE (new behaviour):** same as adversarial 5 |
| 14 | Skew can't be measured | **NEEDS AMINE (new behaviour):** when a clock counts as "unsynchronised" with unknown skew isn't defined |
| 15 | SMS limits exhausted or no phone | Answered from existing decision (AD-18, AD-49; 4.3): request stays open, escalation continues, "Confirmation code could not be sent" |
| 16 | Audit space exhausted, then a stop | **NEEDS AMINE (new behaviour):** same as adversarial 11 |
| 17 | Outbox full | Partly answered (AD-50; 8.2): ordinary reports dropped with a recorded gap. **NEEDS AMINE (new behaviour):** what happens when reserved stop and receipt capacity fills |
| 18 | etcd restore rolls back the ledger | **NEEDS AMINE (new behaviour):** ledger-regression detection and replay protection after restore aren't designed |
| 19 | Management mode unknown | Answered from existing decision (AD-11, AD-13; 2.4 new row): missing check blocks node actions |
| 20 | No recovery version exists | Answered from existing decision (AD-45; 8.4): no named previous release means no automatic rollback; a person recovers |
| 21 | Final wave has no comparison cohort | **NEEDS AMINE (new behaviour):** baseline for the last wave isn't defined (AD-44 compares against not-yet-updated clusters) |
| 22 | Rollout paused indefinitely | **NEEDS AMINE (new behaviour):** no alert or timeout for a long pause is defined |
| 23 | New problem group has no baseline | **NEEDS AMINE (new behaviour):** minimum threshold for groups with no history isn't defined (thresholds are assumptions) |
| 24 | Local dashboard settings while offline | Answered from existing decision (AD-51, D15: settings allowed on the dashboard per PRIV-9). **Not applied**: narrowing-only would reverse D15 |
| 25 | Leaf mismatch at group approval | Answered from existing decision (AD-23, AD-48; 4.4): the cluster refuses with a "refused as invalid" receipt, the console shows sent versus confirmed, and only a re-ask covers it again |

## 5. Totals

- Adversarial (20): 2 answered, 5 editorial, 13 NEEDS AMINE (several with an existing limit now stated).
- Edge cases (25): 11 answered (including 24, not applied per D15), 1 editorial, 13 NEEDS AMINE.
- Overall: 13 answered, 6 editorial, 26 NEEDS AMINE.

## 6. NEEDS AMINE list (one line each)

- A1: cluster-admin holders per platform and key storage (KMS, HSM or sealed).
- A2: verify receipts outside the portal (browser or dashboard).
- A4 (sub-point): does a crashed attempt count as "started" for approval validity.
- A5 / E13: monotonic or authenticated time, backward-jump alarm.
- A6: SMS provider rate, spend and template limits.
- A7: who generates the first-admin code and where it's shown.
- A8: dead-man's-switch probation; guard and checker outside the probed release.
- A9: admission failure policy, recovery-write exemption, outage test.
- A10 / E11: pending approvals versus the open-run quota.
- A11 / E16: stop handling once audit space is exhausted.
- A12: path and Appendix A row for the post-expiry attention notice.
- A14: approval latency budget, poll interval, SMS expiry.
- A15: group assurance label or SMS-session binding.
- A19: faster executor takeover (Lease, toleration, standby).
- A20: re-verify BMC-to-node binding on every use.
- E3: behaviour after a 429 in a normal run.
- E6: block action when the intent append to audit fails.
- E8: count repeats per owning workload.
- E9: whether a stop interrupts a running multi-step repair.
- E14: definition of "unsynchronised" when skew can't be measured.
- E17: reserved outbox capacity exhausted.
- E18: ledger rollback after etcd restore or reinstall.
- E21: health baseline for the final wave.
- E22: alert or timeout for an indefinitely paused rollout.
- E23: alert threshold for new problem groups with no history.
