# Nightshift

**Status: design challenge in progress.** This repository holds my work on the Orvex AI "Nightshift" design challenge. It is a design (product brief, PRD and, later, architecture), not a working product. Documents marked `draft` are still changing.

Nightshift is an ops agent that runs inside every Quornex cluster. It watches the cluster, fixes what is safe to fix, warns before things break, and explains what it did to the people responsible. The challenge is to design it so that private cloud on cheap, unreliable bare metal can be operated reliably and at very low cost per cluster.

## How the work is done

The documents are produced with [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) workflows and Claude Code, with Codex used for some cross-checks. Every decision traces back to the challenge brief, to Danny's recorded answers, or to my own decisions. `AI_LOG.md` records how the AI was used, including the times I overruled it and the corrections I made to its output.

Process order:

1. Product brief (final, 2026-10-28)
2. PRD (in progress)
3. PRD validation
4. UX: simple wireframes for the dashboard, incident explanations, the approval flow and action history
5. Architecture
6. Adversarial review
7. Small prototype (optional)

## Repository layout

| Path | What it is |
|---|---|
| `AI_LOG.md` | Session log, times I overruled the AI, corrections to the AI's output |
| `_bmad-output/planning-artifacts/requirements-checklist.md` | Deliverables, constraints and evaluation criteria extracted from the challenge brief |
| `_bmad-output/planning-artifacts/danny-qa-summary.md` | Questions to Danny and his answers, paraphrased, with my interpretations marked (the correspondence itself is kept private, outside the repository) |
| `_bmad-output/planning-artifacts/briefs/brief-nightshift-2026-10-25/` | Product brief (final), addendum, decision log (`.memlog.md`), landscape research and review |
| `_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/` | PRD (draft), addendum, decision log (`.memlog.md`) and source extracts |
| `_bmad-output/planning-artifacts/research/` | Technical research on open-source building blocks for the architecture |
| `_bmad-output/planning-artifacts/session-*.md` | Notes from the first two sessions (requirements discovery and an understanding check) |
| `_bmad/`, `.claude/skills/` | The BMAD-METHOD 6.12.4 install and workflow skills used to produce the documents |

Every `.memlog.md` is an append-only decision log. Its last `event` line shows where the work stopped.

## Licence

Copyright 2026 Orvex AI. Licensed under the Apache License, Version 2.0; see `LICENSE` and `NOTICE`.

The BMAD-METHOD files in `_bmad/` and `.claude/skills/` are third-party software, Copyright (c) 2025 BMad Code, LLC, under the MIT License; see `THIRD_PARTY_LICENSES/BMAD-METHOD-LICENSE.txt`. BMad, BMad Method and BMad Core are trademarks of BMad Code, LLC.

## Open questions

The current list (2026-10-30). The live copies are Section 10 of the PRD and the follow-ups in `danny-qa-summary.md`.

1. May private diagnostic data move from a workload cluster to the customer's control cluster, for example to feed a combined dashboard? Design decision or Danny (partly answered).
2. Who approves risky changes to OMK and Quornex themselves, as opposed to the customer's applications? (Partly answered.)
3. Danny's "safe repairs should be automatic" is read as "automatic once permitted in advance". Is Orvex's advance permission still needed alongside the customer's, as the original brief says?
4. Does a customer's control cluster also run its own Nightshift agent for its own health?
5. What monitoring, alerting and night cover does Orvex have today?
6. What does "close to public cloud reliability" mean as a number? Working assumption: 99.9% monthly availability for customer-facing platform services.
