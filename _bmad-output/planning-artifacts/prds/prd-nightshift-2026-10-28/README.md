# Nightshift PRD: folder guide

## Main files

| File | What it is |
|---|---|
| `prd.md` | **The PRD** (final, updated 2026-11-03). Start here. |
| `addendum.md` | Design depth handed to the architecture, the UX and the privacy and security review. |
| `.memlog.md` | Every decision, change and override, in order, with its source. The last `event` line is the resume point. |

## `history/`: how the PRD was made

The supporting files were moved here on 2026-11-03 to keep the folder clear (Amine). They are kept for traceability, and `AI_LOG.md` and the memlog refer to them by name. In the git history before that date, they sit directly in this folder.

| Folder | Contents |
|---|---|
| `history/reviews/` | Reviewer reports. First validation (2026-10-30): `review-rubric`, `review-adversarial`, `review-security`, `review-judge`, `review-memlog-audit`, `validation-report`. Second validation (2026-10-31): `review-after-*`, `validation-report-after`. Update of 2026-11-02: `review-update-*`. Update of 2026-11-03: `review-update2-*`. |
| `history/reconciles/` | Checks of the PRD against its inputs: the challenge brief, the product brief, the UX run (`reconcile-ux-memlog`, `reconcile-ux-2026-11-03`), and the final check of 2026-11-03 (`reconcile-latest-2026-11-03`). |
| `history/snapshots/` | Earlier versions kept for comparison: `prd-final-2026-10-31`, `prd-before-polish-2026-11-02`, `prd-before-update-2026-11-03`, and the matching addendum snapshots. |
| `history/polish/` | Structure and prose polish findings for each round (`polish-*`, `polish-update-*`, `polish-update2-*`). |
| `history/notes/` | Working notes: the exact edit lists of each Update (`update-notes-*`), the review triage of 2026-11-03, the source extract of the brief trail and the ID mapping of 2026-10-31. |

## Kept private

To keep Orvex's correspondence and the challenge document out of the public repository, these files live outside it, under `~/nightshift-private/` with the same paths (Amine, 2026-11-03):
- `extract-challenge-and-research.md`
- `reconcile-danny-qa.md`
- `reconcile-exchange5.md`
- `../../danny-qa.md`

The memlog and some reviews still mention them by name. The published summary of Danny's answers is `../../danny-qa-summary.md`.
