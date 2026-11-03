# Nightshift

**Status (2026-11-03): product brief, PRD and UX are final; the architecture is in progress.** This repository holds my work on the Orvex AI "Nightshift" design challenge. It is a design, not a working product.

Nightshift is an ops agent that runs inside every Quornex cluster. It watches the cluster, fixes what is safe to fix, warns before things break, and explains what it did to the people responsible. The challenge is to design it so that private cloud on cheap, unreliable bare metal can be operated reliably and at very low cost per cluster.

## How the work is done

The documents are produced with [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) workflows and Claude Code, with Codex used for some cross-checks. Every decision traces back to the challenge brief, to Danny's recorded answers, or to my own decisions. `AI_LOG.md` records how the AI was used, including the times I overruled it and the corrections I made to its output.

| Step | Status |
|---|---|
| 1. Product brief | Final, 28 October |
| 2. PRD | Final, updated 3 November |
| 3. PRD validation | Done: two full validation rounds (30 and 31 October) and focused reviews of the updates of 2 and 3 November. Latest consolidated report: [`validation-report-after.md`](_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/history/reviews/validation-report-after.md). Remaining findings are listed below. |
| 4. UX | Final, 3 November: two experiences (Orvex console and customer view), wireframes, three key-screen mockups and a three-lens review |
| 5. Architecture | In progress: started 3 November (draft spine, decision log and working notes). The technical research on open-source building blocks (29 October) is an input, not adopted. |
| 6. Adversarial review | After the architecture |
| 7. Small prototype | Optional |

**Remaining validation findings:**
- **PRD:** the critical and high findings of the 3 November review were decided or fixed. One high is deferred as a proposal: an independent reviewer for manual dangerous repairs. Some medium and low findings were fixed in the same round. The rest stay open in [`review-update2-rubric.md`](_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/history/reviews/review-update2-rubric.md) and [`review-update2-adversarial.md`](_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/history/reviews/review-update2-adversarial.md). Design-level findings from the earlier rounds are handed to the architecture and the security review in the PRD addendum.
- **UX:** the 3 critical and 21 high findings were resolved. The remaining medium and low findings are deferred to the next UX update: see section 3 of [`open-items-2026-11-03.md`](_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/.working/open-items-2026-11-03.md).

## Repository layout

| Path | What it is |
|---|---|
| `AI_LOG.md` | Session log, times I overruled the AI, corrections to the AI's output |
| `_bmad-output/planning-artifacts/requirements-checklist.md` | Deliverables, constraints and evaluation criteria extracted from the challenge brief |
| `_bmad-output/planning-artifacts/danny-qa-summary.md` | Questions to Danny and his answers, paraphrased, with my interpretations marked. The correspondence itself is kept private, outside the repository. |
| `_bmad-output/planning-artifacts/briefs/brief-nightshift-2026-10-25/` | Product brief (final), addendum, decision log, landscape research and review |
| `_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/` | PRD (`prd.md`, final), `addendum.md`, decision log and a `README.md` at the top level. Supporting reviews, reconciliations, snapshots, polish findings and notes are in `history/`. |
| `_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/` | UX: `DESIGN.md` (visual identity, light and dark), `EXPERIENCE.md` (behaviour, flows, open items), `wireframes/` (Excalidraw: Orvex console and customer view), `mockups/` (palette sheet, three key screens, measured contrast), reviews and validation report |
| `_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/` | Architecture (in progress): `ARCHITECTURE-SPINE.md` (draft), decision log and working notes |
| `_bmad-output/planning-artifacts/research/` | Technical research on open-source building blocks for the architecture |
| `_bmad-output/planning-artifacts/session-*.md` | Notes from the first two sessions (requirements discovery and an understanding check) |
| `_bmad/`, `.claude/skills/` | The BMAD-METHOD 6.12.4 install and workflow skills used to produce the documents |

Every `.memlog.md` is an append-only decision log. Its last `event` line shows where the work stopped.

## Licence

Copyright 2026 Orvex AI. Licensed under the Apache License, Version 2.0; see `LICENSE` and `NOTICE`.

The BMAD-METHOD files in `_bmad/` and `.claude/skills/` are third-party software, Copyright (c) 2025 BMad Code, LLC, under the MIT License; see `THIRD_PARTY_LICENSES/BMAD-METHOD-LICENSE.txt`. BMad, BMad Method and BMad Core are trademarks of BMad Code, LLC.

## Where the questions stand

Live copies: Section 10 of the PRD and the follow-ups in `danny-qa-summary.md`.

**Confirmed by Danny:**
- **Approval:** not every repair needs both the customer and Orvex. Routine, tested platform repairs run automatically. Risky platform changes need an authorised Orvex engineer, and changes affecting customer production also need the customer. Dangerous repairs stay manual at first.
- **Privacy:** the proposed boundary is a good starting point. External AI is allowed with the customer's consent and zero data retention, or a local model if nothing may leave.
- **Reliability:** 99.9% a month is a working target, not a promise.
- **Hardware:** customers are responsible for their own hardware, and a cluster belongs to one customer.
- **Code fixes:** in the first version, as an experiment.

**Our design policies** (decided by us, not confirmed by Danny):
- **Approval:** risky repairs to the customer's own app need both the customer's approval and Orvex technical approval. This is our conservative interpretation of Danny's approval model (Exchange 5 speaks about platform changes), decided rather than open.
- **Monitoring:** a customer's control cluster runs its own Nightshift agent, and Quornex Fleet watches it like any other.
- **Escalation:** provider-side problems on hosted Kubernetes go through the customer.
- **Code fixes:** a code fix is never approved on automated test results alone.
- **Approval validity:** each repair in the catalogue states how long an approval stays valid.
- **Outbound channels:** the Fleet heartbeat is required for the managed service. A strict no-outbound deployment is not offered in version 1.

**Assumptions still to test:** about 250 problems a night (500 on a bad night) and about 15 engineers; the 30-minute last-resort threshold; whether a model on a 24 GB or 96 GB GPU is useful enough; whether sanitising keeps private data in the cluster; how well the predictive signals work.

## Open questions

**For Danny** (not yet asked unless stated):
1. What monitoring and night cover does Orvex have today?
2. Which hosted models and regions count as "trusted"? Partly answered: consent and zero retention are required.
3. Code fixes use an in-cluster model by default and a hosted model only with the customer's consent. Does that fit Danny's wish to see them in real use? And how should they be priced?
4. Who decides what counts as a "high-confidence" repair? (Never sent; our answer: the repair catalogue entry defines the evidence needed.)
5. What happens when an approval request gets no answer at 3 AM? (Never sent; our proposal: nothing runs that isn't already authorised, and Nightshift alerts again.)

**Design decisions still open:**
6. Timing targets: how long a node heartbeat may be missing, when data counts as out of date, and the length of the window for undoing a rejection (for the architecture).
7. Targets for harmful repairs, explanation feedback, Nightshift's footprint and the share of problems needing a person.
8. The legal basis for the pre-ticked service settings at onboarding (for a legal review, owned by Orvex).
9. Architecture-dependent UX details O-1 to O-13, such as approver roles, how a revocation reaches the cluster and the in-cluster dashboard (`EXPERIENCE.md`, Open items).
