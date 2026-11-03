# Polish: structure lens, DESIGN.md

Lens: `structure` (bmad-review, editorial). Reader: humans. Style: author's (British spelling, no serial comma, plain English), over the Microsoft Writing Style Guide baseline. Word counts from `word_metrics.py` (before: 4,322 words).

**Read:** this document exists to help designers and front-end engineers build both Nightshift experiences from one neutral token set and one component vocabulary.
**Structure model:** Reference/Database (random access, consistent schema per item). Section order is locked by the DESIGN.md spec.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | §Colors — "Rules that carry the meaning" (5 bullets, ~120 words) after two tables and the contrast detail | MOVE to directly after the Source paragraph | The rules carry the meaning of every colour; front-loads them (0 words) |
| structure | §Components — 24 flat bullets (1,299 words) | MOVE into six `###` groups: Status and evidence · Actions and focus · Decision surfaces · Cards, rows and tiles · Freshness · Settings (Info card joins the cards; Manual-repair panel and Check table join the decision surfaces) | Scanning by kind in the longest section (+~15 words) |
| structure | Preamble — "Wireframes and the palette sheet live in `.working/` for now (links below)" | CONDENSE: "Wireframes, the palette sheet and the key-screen mocks are linked in the sections they illustrate"; precedence rule kept | Stale scaffolding; files have moved (0 words) |
| structure | §Layout & Spacing — wireframe references in mid-sentence parentheses (customer bullet ~95 words) | MOVE the references to a closing "See …" sentence in each bullet | Keeps the layout rule readable; references sit together (0 words before new links) |
| structure | §Colors — "Dark stale-hatch stripe" paragraph (~55 words), change history spread over three clauses | CONDENSE: new value first, old value and ratio in one parenthesis | Restates the YAML comment; history kept in brief (−5 words) |
| structure | §Typography — closing note "only the two body densities were decided" vs the `customer-lead` row marked "Decided density" | QUESTION: which is right? | Not applied: needs the author's decision |
| structure | §Components — Status chips' five families vs §Colors Status roles "Means" column | PRESERVE | Two lookup directions (hue → words, field → hue) |
| structure | §Do's and Don'ts — restates rules from Colors and Components | PRESERVE | Required spec section; a recap for retention |
| structure | §Brand & Style — "references for look and feel, not integrations", also in EXPERIENCE.md | PRESERVE | Each spine must stand alone |

**Requested link updates (not lens findings):** frontmatter `sources` and body links moved to `wireframes/` and `mockups/`; links added to the palette sheet and contrast report (Colors), the A1 mock (Layout, console) and the B3 and B3-M mocks (Layout, customer).

**Summary:** 9 recommendations (5 edits, 3 PRESERVE, 1 QUESTION). Applied: 5; kept: 3; skipped: 1. Reduction if all accepted: about +10 words from the lens findings alone (grouping headings outweigh the condense); the document grows to 4,426 words with the requested links. No comprehension trade-offs.
