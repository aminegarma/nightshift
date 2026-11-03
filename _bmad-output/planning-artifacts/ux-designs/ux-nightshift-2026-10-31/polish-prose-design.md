# Polish: prose lens, DESIGN.md

Lens: `prose` (bmad-review, editorial), run after `structure`. Reader: humans. Style: British spelling, no serial comma, plain English; exact labels, quoted microcopy, tokens, IDs and tags untouched.

**Read:** this document exists to help designers and front-end engineers build both Nightshift experiences from one neutral token set and one component vocabulary.
**Voice noted and preserved:** terse spec register, bold lead-ins, noun-phrase fragments ("Cool graphite neutrals, white working surfaces …"), middle-dot lists, British spelling.

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| prose | the customer "Needs your decision" card on B1 is the compact version: problem sentence, severity chip, "Asked 02:13 CET", the card itself is the tap target (inside the Approval card heading) | Moved to the end of the bullet: B1's "Needs your decision" card is the compact version: problem sentence, severity chip and "Asked 02:13 CET"; the whole card is the tap target. | Comma splice inside a long parenthesis broke the heading; now its own sentence |
| prose | then the sections in a fixed order (EXPERIENCE.md, B3 and B3-M) | then the sections in the fixed order EXPERIENCE.md sets for B3 and B3-M | Ambiguous parenthesis |
| prose | "Approve rollback for these 288 clusters", and the confirm button | "Approve rollback for these 288 clusters" and the confirm button | Serial comma removed (author's style) |
| prose | Do: Use `border` for dividers only · Don't: … only outline; use `text-secondary` | Do: Use `border` for dividers only; outline controls and clickable cards in `text-secondary` · Don't: … only outline | The instruction sat in the Don't column |
| prose | only shades varied between the rendered options | only the shades differed between the rendered palette options | Clarity |
| prose | in progress reads like Running | Work in progress reads like Running | Names the status in full |
| prose | min 6.9 / 6.1 on background or raised | min 6.9 / 6.1 on `background` or `surface-raised` | Names the tokens meant |
| prose | with the sentence from EXPERIENCE.md. | with the sentence from EXPERIENCE.md › Surface states (Not an administrator). | Unclear reference |
| prose | `{rounded.container}`, customer gutter. (Cluster card) | `{rounded.container}`, `{spacing.customer-gutter}` padding. | Matches the Approval card wording; the reference resolves |
| prose | Small square per cluster in a group of 100 | One small square per cluster, in groups of 100 | Clarity |
| prose | From the sheet's two radii: | Two radii come from the palette sheet: | Fragment with an unclear "sheet" |
| prose | "Failed – did not work, undone" (en dash) here and in EXPERIENCE.md vs "Failed — undone after it didn't work", "Blocked — no data …" (em dash) in EXPERIENCE.md | Consider: one dash style in status microcopy? | Not applied: quoted microcopy, the author decides |

12 rows: 11 applied, 1 skipped.
