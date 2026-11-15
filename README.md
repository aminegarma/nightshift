# Nightshift

**Status (2026-11-15): design complete for hand-in.** The product brief, PRD, UX and architecture are final; the privacy and security review, failure catalogue and cost model are written. This is a design, not a working product: no control or repair described here has been tested yet.

Nightshift is an ops agent that runs inside every Quornex cluster, on bare metal (OMK) and on EKS. It watches the cluster, fixes what is safe to fix, warns before things break, and explains what it did to the people responsible. Quornex Fleet watches and updates all Nightshift agents centrally, so that Orvex can run 10,000 clusters with a small team.

## The hand-in

| Asked for | Where it is |
|---|---|
| **The PRD, produced with BMAD** | [`prd.md`](_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/prd.md) (final, updated 15 November with the architecture's changes AP-1 to AP-20), with its [`addendum.md`](_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/addendum.md) and decision log |
| **The architecture, with diagrams** | [`architecture-orvex.md`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/architecture-orvex.md) (the readable document, with a 15-minute reading path at the top) and [`ARCHITECTURE-SPINE.md`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/ARCHITECTURE-SPINE.md) (the build contract: 72 decisions). Appendices: [A. outbound flows](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/appendix-a-outbound-flows.md), [B. PRD changes](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/appendix-b-proposed-prd-changes.md), [C. failure-catalogue sources](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/appendix-c-failure-catalogue-sources.md). Tool choices and rejected alternatives: [`tool-comparison.md`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/tool-comparison.md) |
| **A privacy and security review** | [`privacy-security-review.md`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/privacy-security-review.md): specified design controls, remaining risks and validation not yet performed, kept separate |
| **A failure catalogue** | [`failure-catalogue.md`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/failure-catalogue.md): the top 20 failures, each *predict*, *fix* or *only report*, for OMK and EKS |
| **A cost model** | [`cost-model/`](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/cost-model/README.md): a reproducible script and its [results](_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/cost-model/cost-model-results.md) at 100 and 10,000 clusters, every input labelled with its source or as a placeholder |
| **AI_LOG.md** | [`AI_LOG.md`](AI_LOG.md): how Claude and BMAD were used, **five overrules to read first**, the full list of overrules, and every correction to the AI's output |
| **A README ending with open questions** | This file |

Also: the UX ([`EXPERIENCE.md`](_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/EXPERIENCE.md), [`DESIGN.md`](_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/DESIGN.md), wireframes and mockups) and the [product brief](_bmad-output/planning-artifacts/briefs/brief-nightshift-2026-10-25/brief.md).

## Where to look for each judging criterion

| Criterion | Start here |
|---|---|
| Technology choices | `tool-comparison.md`; Orvex document §10 (open-source choices and rejected alternatives) |
| One design for bare metal and EKS | Orvex document §2 (what runs where, and what changes between OMK and EKS) |
| Privacy and security | `privacy-security-review.md`; Orvex document §4–§5 |
| Cost | Orvex document §12 and `cost-model/` (Orvex cash and customer footprint shown separately; savings hold only under the stated assumptions) |
| AI fluency | `AI_LOG.md`: the five overrules, then the corrections |
| Honest thinking | The validation plan in `privacy-security-review.md`, PRD Section 10, and the open questions below |

## How the work was done

The documents were produced with [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) workflows and Claude Code, with Codex used for some cross-checks. Every decision traces back to the challenge brief, to Danny's recorded answers, or to my own choices, and is logged in an append-only `.memlog.md` in each workspace.

| Step | Status |
|---|---|
| 1. Product brief | Final, 28 October |
| 2. PRD | Final, last updated 15 November (architecture reconciliation, AP-1 to AP-20) |
| 3. PRD validation | Two full validation rounds (30 and 31 October), focused reviews of the November updates, and a finalisation check on 15 November |
| 4. UX | Final, 3 November; references updated 15 November |
| 5. Architecture | Final, 15 November, after a reviewer gate (four independent reviewers), a `bmad-review` of the Orvex document and focused consistency checks |
| 6. Adversarial review | Done on the architecture (reports in `architecture-…/reviews/`) |
| 7. Prototype | Not built: optional in the challenge brief |

**What I'd test next** (nothing below has been run):
- **Prompt injection:** seeded malicious logs, names, field values, model responses and source-code comments, checking permissions, evidence validation, queue limits and what reaches outbound messages and approval screens.
- **Privacy:** planted-secret tests (PRIV-7).
- **Network:** default-deny rules and the three purpose-specific outbound controls, on both OMK and EKS.
- **AI usage checks:** isolation, revocation and logging tests for the per-cluster AI credentials.
- **Approvals:** feasibility and usability of the passkey plus SMS confirmation, including its latency targets.
- **Clock and restore:** clock rollback, restarts and state-restore behaviour against the offline validity tiers.
- **Cost inputs:** footprints, handling times and the share of problems needing a person, measured on the first clusters.

## Repository layout

| Path | What it is |
|---|---|
| `AI_LOG.md` | Session log, overrules, corrections to the AI's output |
| `_bmad-output/planning-artifacts/requirements-checklist.md` | Deliverables, constraints and evaluation criteria extracted from the challenge brief |
| `_bmad-output/planning-artifacts/danny-qa-summary.md` | Questions to Danny and his answers, paraphrased, with my interpretations marked. The correspondence itself is kept private, outside the repository |
| `_bmad-output/planning-artifacts/briefs/brief-nightshift-2026-10-25/` | Product brief, addendum, decision log, landscape research and review |
| `_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/` | PRD, addendum, decision log, update notes and reviews; older material in `history/` |
| `_bmad-output/planning-artifacts/ux-designs/ux-nightshift-2026-10-31/` | UX: `DESIGN.md`, `EXPERIENCE.md`, wireframes, mockups, reviews |
| `_bmad-output/planning-artifacts/architecture/architecture-nightshift-2026-11-03/` | Architecture: spine, Orvex document, privacy and security review, failure catalogue, cost model, appendices, tool comparison, reviews; `.working/` keeps the process history |
| `_bmad-output/planning-artifacts/research/` | Technical research on open-source building blocks |
| `_bmad/`, `.claude/skills/` | The BMAD-METHOD install and workflow skills used to produce the documents |

## Licence

Copyright 2026 Orvex AI. Licensed under the Apache License, Version 2.0; see `LICENSE` and `NOTICE`.

The BMAD-METHOD files in `_bmad/` and `.claude/skills/` are third-party software, Copyright (c) 2025 BMad Code, LLC, under the MIT License; see `THIRD_PARTY_LICENSES/BMAD-METHOD-LICENSE.txt`. BMad, BMad Method and BMad Core are trademarks of BMad Code, LLC.

## Open questions

Live copies: PRD Section 10, `danny-qa-summary.md` and the Deferred table of the spine.

**For Danny and Orvex** (not yet asked unless stated):
1. What monitoring and night cover does Orvex have today?
2. Which hosted models and regions count as "trusted"? Partly answered: consent and zero retention are required. Our design lets each customer choose its permitted AI Regions.
3. How should code fixes be priced? (My proposal: by tokens or difficulty.)
4. Who decides what counts as a "high-confidence" repair? (Never sent; our answer: the repair catalogue entry defines the evidence needed.)
5. What happens when an approval request gets no answer at 3 AM? (Never sent; our proposal: nothing runs that isn't already authorised, and Nightshift alerts again.)
6. OMK details we couldn't confirm: the Kubernetes distribution, network plugin, storage system, BMC Redfish support and how platform updates are applied and rolled back.
7. Where Quornex Fleet is hosted, and whether Quornex's identity system can be reused.
8. Is the "about 15 engineers for 10,000 clusters" target the Nightshift team alone, or all of Orvex's incident work? The cost model shows what would have to be true for each.

**Design decisions still open:**
9. Code-fix engineer access to the isolated test environment: needs its own consent and channel design.
10. Targets still to set: harmful repairs, explanation feedback, Nightshift's footprint and the share of problems needing a person.
11. The legal basis for the pre-ticked service settings at onboarding (for a legal review, owned by Orvex).

**Assumptions still to test:** about 250 problems a night (500 on a bad night) and about 15 engineers; the 30-minute last-resort threshold; the offline validity tiers (1 hour, 24 hours) and the 2-minute undo window; whether a model on a 24 GB or 96 GB GPU is useful enough; whether sanitising keeps private data in the cluster; how well the chosen signals predict failures.
