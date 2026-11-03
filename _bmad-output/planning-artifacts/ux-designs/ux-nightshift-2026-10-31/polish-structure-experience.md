# Polish: structure lens, EXPERIENCE.md

Lens: `structure` (bmad-review, editorial). Reader: humans. Style: author's (British spelling, no serial comma, plain English). Word counts from `word_metrics.py` (before: 9,995 words).

**Read:** this document exists to help designers, engineers and the architect build how Nightshift behaves for Orvex engineers and customer approvers: surfaces, wording, states, flows and approval rules.
**Structure model:** Reference/Database, with narrative Key Flows. Top-level section order follows the bmad-ux template and is kept.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Open items — "Pending PRD changes" as one run-on paragraph with ten inline numbers (~300 words) | MOVE into a numbered list 1–10, numbers unchanged | Scanning; numbers still match `.working/open-items-2026-11-03.md` (0 words) |
| structure | §Foundation — Wireframes bullet (~75 words) mixing links, superseded files, the precedence rule, placeholder data and what's newer | CONDENSE into three bullets: Wireframes · Key-screen mocks · precedence rule (stated once) | One idea per bullet (+~60 words with the requested mock links) |
| structure | §Surface → journey closure — gaps paragraph (~120 words, three kinds of gap) | CONDENSE into three labelled bullets: No journey exercises · Not wireframed or designed · Stated needs with no dedicated surface | Scanning (+~10 words) |
| structure | §Foundation — "The Key Flows omit the zone for brevity." | CUT (Key Flows' own intro says "Times omit the zone here; screens show it.") | True redundancy (−8 words) |
| structure | §Component Patterns — Approval card and Manual-repair panel cells (~200 and ~250 words) carry the full B3 and B3-M order inline | QUESTION: move each order into a numbered list below the table? | Not applied: reshapes the component table that IA rows point to; the author's call |
| structure | §Voice and Tone — Reject result row vs §Authorisation › Reject | PRESERVE | One is the screen copy, the other the rule |
| structure | §Inspiration & Anti-patterns — "references for look and feel, not integrations", also in DESIGN.md | PRESERVE | Each spine stands alone |
| structure | §Interaction Primitives keyboard and live-data bullets vs §Accessibility Floor | PRESERVE | Behaviour vs accessibility floor; reinforcement |
| structure | §State Patterns › Surface states (29 rows) | PRESERVE | Reference table; grouping by surface would split cross-surface states |

**Requested edits (not lens findings):** frontmatter `sources` and Foundation links moved to `wireframes/` and `mockups/`; key-screen mocks, palette sheet and contrast report linked in Foundation; contrast report linked in Accessibility Floor; one line in Open items pointing to `.working/open-items-2026-11-03.md` section 3.

**Summary:** 9 recommendations (4 edits, 4 PRESERVE, 1 QUESTION). Applied: 4; kept: 4; skipped: 1. Lens findings alone are about neutral in length; the document grows to 10,082 words with the requested links. No comprehension trade-offs.
