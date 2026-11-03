# Reconcile: Danny's challenge brief vs PRD

- **Input:** `brief.pdf` (Danny's 2-page challenge brief). Text from `brief-pdf.txt` (session scratchpad); item IDs A1-A62 follow `extract-challenge-and-research.md` Part A.
- **Checked against:** `prd.md` (draft, updated 2026-10-29/30) and `addendum.md`.
- **Overrides applied:** danny-qa.md Exchanges 1-4 take precedence where they conflict with the brief (e.g. customers own their hardware; customer picks alert-only or automatic; one cluster per customer). Those items are marked "Resolved (danny-qa)", not gaps.
- **Separate deliverables:** architecture, failure catalogue (top 20), cost-model numbers, privacy and security review. The PRD only needs to set requirements for them, so "Deferred" is fine *if* the PRD hands the item off. Where it doesn't, the item is marked GAP (handoff).
- Read-only check, 2026-10-30. Status key: **Covered**, **Partial**, **GAP**, **Deferred** (other deliverable, handed off), **Resolved (danny-qa)**, **Not PRD** (process or small print).

## Table

### Context (A1-A8)

| ID | Item | Where covered | Status |
|---|---|---|---|
| A1 | Quornex = developer cloud, fully managed by Orvex | Glossary "Quornex" | Covered |
| A2 | 10,000 clusters | Vision; NFR-1; COST-1 | Covered |
| A3 | OMK on bare metal or hosted K8s such as EKS | Glossary "Platforms"; NFR-2 | Covered |
| A4 | Clusters fail in small ways, so companies keep DevOps teams | Vision ("replaces much of the DevOps work"); COST-5; SM-8 | Covered |
| A5 | Strict, tuned configuration, with Nightshift looking after it | NFR-3; FR-38; FR-39 | Covered |
| A6 | Vision: logs and metrics, **tuning** and self-healing, alerting before problems | Vision; 3.1-3.6. Tuning: only FR-39, which reads as Nightshift tuning "its settings" | Partial: tuning the cluster isn't a capability anywhere |
| A7 | "Keeps watch overnight, fixes what it safely can, warns us before things break" | Vision; FR-16 morning summary; FR-22 night duty; FR-20 | Covered |
| A8 | Three-state legend: Fixed on its own / Waiting for a person / Being watched | Not referenced; states are implied by FR-13/FR-14/FR-16 | GAP (minor) |

### What it must do (A9-A16)

| ID | Item | Where covered | Status |
|---|---|---|---|
| A9 | 01 Watch the whole stack, from hardware to platform services | Vision; FR-1; FR-5; FR-7; 9.1. Hardware ownership per Exchange 4 | Covered / Resolved (danny-qa) |
| A10 | 02 See trouble coming (disk filling, memory creeping) | 3.2 FR-8 to FR-10; SM-1 | Covered |
| A11 | 03 Fix what's safe, check it worked, undo if not | FR-17; FR-20; FR-24; FR-26; FR-27 | Covered |
| A12 | 04 Risky changes and any change to customer production wait for a person | Glossary "Customer production", "Approval"; FR-20 to FR-23; SM-4. Approver and modes per Exchange 1/4 | Covered / Resolved (danny-qa) |
| A13 | 05 Explain plainly: what's wrong, why it matters, what it did, **"in a few sentences anyone can follow"** | 3.3 description (quote); FR-11; NFR-8; SM-5 | Partial: content and audience are testable, but brevity ("a few sentences") isn't. Nothing caps length or jargon, and the morning summary and phone call have no plain-language rule of their own |
| A14 | 06 Protect customer data; hosted model sees only what it must | PRIV-1 to PRIV-6; Section 5 | Covered |
| A15 | 07 Learn across the fleet: one cluster's new problem readies every cluster | 3.9 FR-35 to FR-38; FR-36 (lessons, not data) | Partial: no success metric (e.g. time from first sighting to fleet-wide catalogue entry), and no requirement that every cluster *first* sees the new problem in the incident catalogue |
| A16 | 08 Cost known and sensible | 4.3 COST-1 to COST-5; SM-10 | Covered |

### Ground rules (A17-A21)

| ID | Item | Where covered | Status |
|---|---|---|---|
| A17 | Two kinds of cluster, one tool, including bare-metal hardware | NFR-2; FR-1; FR-5; FR-7; Glossary. Hardware per Exchange 4 | Covered / Resolved (danny-qa) |
| A18 | Two ways to run the model; only in-cluster GPU keeps private data in | Section 5 (adds a third option, shared GPU, held to the hosted boundary); PRIV-2; FR-41 | Covered. "Trusted" hosted model is open (Q10.6), as it should be |
| A19 | Same tested release everywhere; tune within limits; bigger changes go to Orvex as a proposal | NFR-3; FR-38; FR-44; FR-39 | Partial: the proposal path (who receives a proposal, how it's decided, how it becomes a release) is only named, in FR-39 and FR-12 |
| A20 | Everything read and changed is recorded where the customer can see it | 3.8 FR-31 to FR-34; FR-15 | Covered |
| A21 | Holds only the rights it needs | SEC-4; SEC-2; SEC-3 | Covered (one line; per-platform rights belong in the architecture, see A24) |

### What your documents must answer (A22-A40)

| ID | Question | Where covered | Status |
|---|---|---|---|
| A22 | Technology: which open-source projects to collect, store, spot, act | None; no handoff to the architecture | GAP (handoff) |
| A23 | Technology: what was rejected and why | None; no handoff | GAP (handoff) |
| A24 | What runs on each node, per cluster, centrally | FR-6 (three levels); FR-28 (coordinator per cluster); FR-2 (node heartbeat). Nothing per node | Partial: the per-node layer isn't handed off |
| A25 | What changes between bare metal and EKS | Vision; Glossary; FR-1; FR-5; FR-7; 3.4 EKS line; 9.2 | Covered (EKS escalation path open, Q10.9) |
| A26 | What if Nightshift fails | FR-4; FR-6; FR-29; 3.7; NFR-4; NFR-5 | Covered |
| A27 | Given failures: hung NICs, full memory, disks, links | FR-1; FR-3; FR-8 (storage, memory, network congestion) | Covered ("hung" NIC as distinct from dead isn't named, which is fine for a PRD) |
| A28 | Which twenty failures matter most | Glossary "Incident/Repair catalogue" only. No requirement for a top-20 failure catalogue or its ranking criteria | GAP (handoff to the failure catalogue) |
| A29 | Which can it predict, fix or only report | FR-8 (predict), repair catalogue (fix), incident catalogue and 3.4 hardware (report) | Partial: the three-way split exists but isn't required per failure in the catalogue |
| A30 | Where rules and statistics suffice vs where an LLM is worth its cost | FR-17 (AI only to match evidence or write explanations); FR-47; COST-4; Section 5 | Partial: the principle is clear, but there's no requirement that the architecture justify each LLM use against its cost |
| A31 | How it works with a GPU in the cluster, and without | Section 5; FR-41; PRIV-5 | Partial: no behaviour defined for when the hosted model is unreachable or over budget (does the rules-only path keep detecting and repairing?) |
| A32 | Privacy: limit what a hosted model sees | PRIV-2; Section 5 | Covered |
| A33 | Strip private data first | PRIV-2 (placeholders); PRIV-3 | Covered |
| A34 | Prove it to a customer | PRIV-6 (record, planted-secret tests, outside audit); SM-C3 | Covered |
| A35 | Security: a crafted log line or a compromised agent | SEC-1; SEC-2; SEC-3; FR-33; PRIV-3 | Covered |
| A36 | Safety: how a repair avoids making things worse | FR-18; FR-21 (precondition re-check); FR-25; FR-27; SM-2; SM-3 | Covered. No limit on how many automatic repairs run per cluster or per fleet in a time window, beyond FR-27/FR-30 |
| A37 | What stops two fixes fighting | FR-28 repair coordinator; 3.7 | Covered |
| A38 | When it stops and calls a person | FR-19; FR-22; FR-26; FR-27; FR-29 | Covered |
| A39 | Cost per cluster per month at 100 and 10,000, with GPU and with hosted model | COST-1 (two scale points); COST-2; Section 5 | Partial: COST-1 doesn't require one figure per model option (in-cluster GPU, shared GPU, hosted) at each scale point |
| A40 | What moves the cost most | None | GAP (handoff to the cost model: require a sensitivity analysis / main cost drivers) |

### Process, deliverables, small print (A41-A51, A59-A62)

| ID | Item | Where covered | Status |
|---|---|---|---|
| A41-A42 | Use AI heavily; BMAD; VM; bmad-help | Provenance tags throughout the PRD ((Amine), (AI), Codex) | Not PRD (shown in AI_LOG) |
| A42a | Step 3: "Requirements and success measures, then validate the PRD" | Sections 3, 7, 8. Front-matter `status: draft` | Partial: PRD validation hasn't run yet (process step, not content) |
| A43-A44 | GitHub repo; PRD with BMAD | This PRD | Covered |
| A45 | Architecture, with diagrams | addendum.md "For the architecture" (4 notes) | Partial: no list of what the architecture must answer (see A22-A24, A28, A30, A40) |
| A46 | Privacy and security review | Section 4 sets the requirements | Partial: the review isn't named as the place that checks PRIV/SEC |
| A47 | Failure catalogue and cost model | 4.3 (cost requirements); catalogue concepts in the Glossary | Partial: see A28, A29, A39, A40 |
| A48 | AI_LOG.md with 3-5 overrules | Outside the PRD | Not PRD |
| A49 | README ending with open questions | Section 10 is the natural source | Covered (as the source) |
| A50 | 15-minute walkthrough | n/a | Not PRD |
| A51 | Prototypes optional | n/a | Not PRD |
| A59-A60 | Fee; IP and Apache 2.0 notice | n/a | Not PRD |
| A61 | No secrets or private Orvex data in the repo | Provider name generalised (Glossary, addendum) | Covered |
| A62 | Ask Danny early | Section 10 "For Danny"; danny-qa.md | Covered |

### How we'll judge it (A52-A58)

| ID | Criterion | Where covered | Status |
|---|---|---|---|
| A52 | Technology choices: sound, alternatives weighed | None (see A22, A23) | GAP (handoff) |
| A53 | One clear design for bare metal and EKS | NFR-2; FR-1; FR-5; FR-7 | Covered |
| A54 | Customer data protected, agent locked down | Section 4.1, 4.2 | Covered |
| A55 | Credible cost numbers for a service people will pay for | 4.3; COST-5 | Partial: "people will pay for" (price or willingness to pay vs cost) isn't stated as a requirement. COST-5 compares only with engineers replaced |
| A56 | AI fluency: you steer the AI and check its work | Provenance tags; "[AI] ... accepted by Amine"; Codex checks | Covered (in form; AI_LOG carries the evidence) |
| A57 | Honest thinking: **what you know and what you'd test next** | Section 10 "To test" (13-17); [OPEN]/[AI]/[DESIGN ASSUMPTION] tags; Section 8 note ("proposed, not observed") | Partial: the To-test list has no priority, no test method and no pass/fail signal, so it reads as a list rather than "what I'd test next". Nothing separates known (sourced) from assumed in one place |
| A58 | Hard problem: show how you think, make clear choices, be honest about uncertainty | Clear choices (FR-20, PRIV-1, FR-41); Section 10 | Covered |

## Gaps and suggestions

1. **A22/A23/A52 Technology choices (GAP, handoff):** add a short "Requirements for the architecture" section saying it must name the open-source projects to collect, store, detect and act, plus the alternatives it rejected and why (the research digest's tools are the starting list).
2. **A28/A29 Top-20 failure catalogue (GAP, handoff):** require the failure catalogue to rank 20 failures by stated criteria (frequency × impact) and tag each as predict / fix (risk level) / report only, on OMK and EKS separately. Include hung NICs and full memory, disk and links.
3. **A40 What moves cost most (GAP, handoff):** add COST-6: the cost model must show the main cost drivers and a sensitivity range (e.g. LLM calls per problem, problems per night, GPU price, engineer count).
4. **A39 Cost per model option (Partial):** extend COST-1 to require each number for each model option (in-cluster GPU, shared GPU, hosted) at 100 and 10,000 clusters.
5. **A13 "A few sentences anyone can follow" (Partial):** add a testable brevity and wording rule to FR-11/NFR-8 (e.g. at most about 5 sentences, no unexplained technical terms), and apply it to phone calls and the morning summary too.
6. **A57 "What you'd test next" (Partial):** turn Section 10 "To test" into a prioritised list with method and pass/fail signal for each item, and mark which statements are known (sourced) vs assumed.
7. **A6/A19 Tuning and proposals (Partial):** make FR-39 say Nightshift tunes the *cluster* configuration within release-set limits (recorded, verified, reversible like a repair), and define the proposal path to Orvex (who reviews, how it becomes a release).
8. **A15 Fleet learning measure (Partial):** add a success metric, such as time from a new problem's first sighting to a tested catalogue entry on every cluster.
9. **A31 Without a model (Partial):** state the behaviour when the hosted model is unreachable or rate-limited (rules-only detection and catalogue repairs continue; explanations fall back to templates).
10. **A24/A45/A46 Handoff to the other deliverables (Partial):** in that same section, list what the architecture must answer (per node / per cluster / central, rights per platform, diagrams) and say the privacy and security review checks PRIV-1 to PRIV-6 and SEC-1 to SEC-4.
11. **A55 "A service people will pay for" (Partial):** add one line that the cost model compares cost per cluster with a plausible price or the customer's alternative (a DevOps hire), not only Orvex's engineers.
12. **A8 Three-state legend (GAP, minor):** consider making "Fixed on its own / Waiting for a person / Being watched" the problem states shown on the dashboard and morning summary (FR-15, FR-16).
13. **A36 Repair rate limit (minor):** consider a cap on automatic repairs per cluster or per hour, so a misfiring rule can't keep repeating "safe" repairs.
