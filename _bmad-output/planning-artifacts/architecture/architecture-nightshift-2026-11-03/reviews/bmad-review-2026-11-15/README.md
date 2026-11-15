# bmad-review of architecture-orvex.md (2026-11-15)

- **Content:** `architecture-orvex.md` (docs, defines behaviour).
- **Lenses run:** adversarial, edge-case hunter, editorial structure, then editorial prose on top of structure. Verification gap was skipped because it applies to code only.

| Lens | Findings | File |
|---|---|---|
| adversarial | 20 | lens-adversarial.md |
| edge-case-hunter | 25 | lens-edge-case-hunter.json |
| structure | 18 recommendations | lens-structure.md |
| prose | 40 rows (+9 minor) | lens-prose.md |

## Overlaps between lenses (signal, not duplicates)

| Topic | Flagged by |
|---|---|
| Clock rollback and skew vs validity tiers | adversarial 5; edge cases 12–14 |
| Stops refused when audit storage is full | adversarial 11; edge case 16 |
| Unanswered requests filling the run quota | adversarial 10; edge case 11 |
| Recovery retry without revalidation | adversarial 4; edge cases 1–2 |
| Working-file links in a hand-in document | adversarial 18; structure (question) |
| Inconsistent gateway-bypass statements | adversarial 12; structure (condense); prose |
| Header date against content | adversarial 17; prose |

## Conflicts with decisions already taken

- **Edge case 24** proposes narrowing-only settings changes on the local dashboard. Amine decided D15 (2026-11-11): follow PRIV-9, so settings changes are allowed there. Keep D15 unless Amine reopens it.

## Follow-up (2026-11-15)

- **Editorial changes** and answers from existing decisions were applied (see `applied-changes.md`).
- **The 26 "needs Amine" items** were then decided one at a time, or in batches for routine edge cases: A1–A20, edge cases E3, E6, E8, E9, E13, E14, E16–E18 and E21–E23.
  - Each decision is in `.memlog.md` and reflected in the spine (new AD-72; amended AD-2, AD-7, AD-8, AD-18, AD-19, AD-23, AD-24, AD-44, AD-45, AD-47, AD-48, AD-50, AD-62, AD-65, AD-69) and in `architecture-orvex.md`.
  - Corrections to the AI are in AI_LOG #74–#83.
- **A12** (the attention-notice flow) was documented in appendix A, row 6a, with its channel to confirm.
- **Not applied:** edge case 24, because it conflicts with D15.
