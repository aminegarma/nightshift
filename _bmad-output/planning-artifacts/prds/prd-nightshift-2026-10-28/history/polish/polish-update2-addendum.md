# Polish of the 2026-11-03 update: addendum.md

**Purpose read:** this document exists to help the owners of the downstream deliverables (architecture, privacy and security review, UX, cost model) pick up design depth that the Nightshift PRD pushed out to them, with each item traced to its source.

**Scope:** only text changed or added on 2026-11-03 (`diff addendum-before-update-2026-11-03.md addendum.md`): five new items under "For the architecture", the "For the UX" intro and status lines, the "UX" item under the 2026-11-02 review, and the new "From the review of the 2026-11-03 update" section.

**Structure model:** Reference (random access, one item per topic, each item tagged with its source). Sections named after a deliverable hold settled inputs from Amine; sections named after a review hold that review's hand-offs.

**Voice and style to preserve:** terse, note-like register; bold lead-in labels; fragments; bracketed source tags and finding IDs; British spelling; no serial comma.

**Status:** every row marked "Applied" was applied to `addendum.md` on 2026-11-03. Rows marked "Skipped" need a decision from Amine.

| Pass | Original Text | Revised Text | Changes | Status |
| ---- | ------------- | ------------ | ------- | ------ |
| structure | ## From the review of the 2026-11-03 update | Add one line under the heading: "The decisions from this review that the architecture must design are under "For the architecture" above." | Missing scaffolding. Four of the review's hand-offs sit under "For the architecture", tagged "review of the update", while this section holds only the deferred proposal. Without a pointer, a reader of this section thinks the review handed over one item. +17 words. | Applied |
| structure | - **Status for dangerous repairs (FR-52):** dangerous repairs now show "Manual repair needed". | **QUESTION.** CUT, since the next bullet's final status list includes "Manual repair needed"? | The new "Final statuses" bullet makes this one redundant. Cutting it removes a quoted status string, so it is left for Amine. | Skipped |
| structure | - **Cluster status when Fleet reports are not permitted (FR-6, PRIV-9):** "Heartbeat OK · ..." | **PRESERVE.** | The PRD's FR-6 now holds the same string. The UX hand-off list keeps it as a lookup for the UX owner. | Preserved |
| structure | - **UX open items:** ... ‖ **Revocation reaches the cluster:** ... ‖ **Undoing a rejection:** ... ‖ **In-cluster dashboard:** ... ‖ **Defined manual procedures for inconclusive checks:** ... | **PRESERVE** under "For the architecture". | They are settled inputs for the architecture, so they fit the deliverable section; the new pointer row above links the review section to them. | Preserved |
| prose | **UX open items:** UX open items O-1 to O-12 | **UX open items:** items O-1 to O-12 | The label repeated in the body. | Applied |
| prose | withdrawals, alert-only and unticks take effect ‖ withdrawals, alert-only and settings when the portal is off | "withdrawals, a switch to alert-only and unticks take effect" ‖ "withdrawals, the switch to alert-only and settings changes when the portal is off" | "Alert-only" is a mode, not an action; the PRD says "a switch to alert-only" and "settings changes" (FR-22, PRIV-9). | Applied |
| prose | (FR-22, D1) (Amine, ...) ‖ (FR-50) (Amine, ...) ‖ (PRIV-9) (Amine, ...) ‖ (FR-22, FR-52) (Amine, ...) | One bracket each, reference first: "(FR-22, D1; Amine, 2026-11-03, review of the update)" and so on. Tag text unchanged. | Same house pattern as in the PRD. | Applied |
| prose | As handed over: the settings journey is still missing and now carries more: ‖ Nine UX decisions from 2026-10-31 are stale after this update | "As handed over, the settings journey was still missing and carried more:" ‖ "Nine UX decisions from 2026-10-31 were stale after this update" | The item now opens with "done in the UX run of 2026-11-03", so the present tense read as if the gaps were still open. The past tense matches "As handed over", and the colon after it is gone, leaving one colon before the list. | Applied |

## Summary

- **Recommendations:** 4 structure (1 added scaffolding line, 2 PRESERVE, 1 QUESTION) and 4 prose (all applied).
- **Word impact:** `addendum.md` went from 1,295 to 1,315 words (+20, +1.5%), almost all from the scaffolding line.
- **Comprehension trade-offs:** none.
