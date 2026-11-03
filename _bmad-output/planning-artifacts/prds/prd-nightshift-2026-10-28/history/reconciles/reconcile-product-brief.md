# Reconciliation: final product brief → PRD

*2026-10-30. Input: `briefs/brief-nightshift-2026-10-25/brief.md` (status final, including "Corrections after finalisation") and its `addendum.md`. Checked against `prd.md`, `addendum.md` and `.memlog.md` in this folder. "memlog Lnn" means line nn of this folder's `.memlog.md`. Read-only check; no PRD file was changed.*

Status key: **Covered** = in the PRD or PRD addendum. **Partial** = the PRD has part of the item, but something substantive is missing. **CHANGED** = a later PRD decision deliberately replaced the item. **GAP** = missing, and no memlog decision drops it.

## 1. Brief: Summary and The Problem

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 1 | Managed cloud for many companies across 10,000 clusters, on bare metal and EKS, with no large ops team per cluster (L14) | Covered | Vision ¶2; NFR-1 |
| 2 | Predict before customers feel it, explain in plain words, repair from a tested catalogue with approvals, protect data (L14) | Covered | Vision ¶1; FR-8–FR-11, FR-17, 3.5, Section 4 |
| 3 | Builds on proven open-source tools (e.g. Prometheus) rather than rebuilding them (L16, L60; addendum L32) | **GAP** | "open-source" appears nowhere in the PRD. Prometheus appears only in the PRD addendum, as something FR-4's checker must be independent from |
| 4 | AI only where rules and automation can't do the job (L16, L98) | Covered | 3.2 description, FR-17, FR-47, Section 5 |
| 5 | Lowest realistic cost per cluster at close to public-cloud reliability (L16) | Covered | COST-4, SM-10 |
| 6 | For the customer, "feels like a cheap public cloud"; for Orvex, a cloud it can run profitably at scale (L16) | CHANGED / Covered | Customer framing replaced by "operate their own cloud at low cost, with a public-cloud-like experience and control over their data and compute" (memlog L55, Vision Q3). Profitability is covered by Vision proof 4 and COST-5 |
| 7 | Customer problem: today, private cloud is complicated and expensive, needs specialists, and gives a much worse experience (Danny) (L20) | **GAP** | The PRD has no Problem or background section. The chosen section order (memlog L19) left it out as a structural choice, not as a decision to drop the content |
| 8 | Orvex problem: Quornex is "a complex mess of open-source components with a million things that can go wrong" (Danny), on cheap, unreliable, possibly poorly maintained bare metal (L22) | Partial | The Glossary says customer hardware is "possibly badly configured" (Danny Ex. 4). The Danny quote and "cheap, unreliable" are missing. The addendum's "hardware failures are a central case, not an edge case" (addendum L64) is reflected only implicitly, in FR-1, FR-7, FR-8 and 3.4 |
| 9 | About 250 incidents a night, up to 500 on a bad night (planning assumptions) (L22) | CHANGED | These now count problems of every type, and false alerts are not counted (memlog L85). See NFR-1 and open question 13 |
| 10 | Without Nightshift, hundreds of engineers would be needed: the customer's DevOps cost simply moves to Orvex, and cheap cloud stops making money (L22) | Partial | Vision proof 4 and COST-5 cover "does it cost more or less than engineers". The "cost moves to Orvex" argument is not stated |
| 11 | **Example night, today:** an online shop at 2 AM; memory creeps up and the service restarts in a loop; checkout fails; shoppers notice first, the owner hears it from them, Orvex finds out last; sales, trust and in the end the customer are lost (L24) | **GAP** | No "without Nightshift" story anywhere. UJ-1 starts once checkout is already failing |

## 2. Brief: Who This Serves

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 12 | Primary user is the Orvex Nightshift team, at 350–400 clusters per engineer (L28) | CHANGED | About 15 engineers, about 670 clusters each (memlog L117, L123, L157). See Section 6 and SM-8 |
| 13 | Why the team is primary: Orvex can't run Quornex at scale without Nightshift, so Nightshift serves Orvex first (L28) | Partial | Section 6 names the primary user but not the reason |
| 14 | The team watches over Nightshift itself (limits, proposals, fleet lessons) and is not paged for every customer incident (L28) | Covered | FR-12, Section 6 |
| 15 | Business owner: chose Quornex to avoid DevOps staff; plain words; answers requests; chooses permitted fixes; live health view; morning summary (L29) | Covered | Section 6, FR-11, FR-15, FR-16, FR-20 |
| 16 | Orvex support handles customer incidents and answers requests when approval is delegated (L30) | Covered | Section 6, FR-12, Glossary "Approval" |

## 3. Brief: The Solution and tone

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 17 | Same release in every cluster; only permissions in settings differ (L34) | Covered | NFR-3, FR-38, FR-44 |
| 18 | Risk (safe, risky, dangerous) and "who said yes" are separate questions; definitions to settle in the PRD (L36–40) | Covered | Glossary risk levels (memlog L15, L59, L62, L63, L86); 3.5 |
| 19 | A permitted fix runs without asking because the customer **and Orvex** approved it in advance (L38, L90) | CHANGED | Safe and ticked runs with no Orvex approval; risky and ticked needs the Nightshift team's yes each time; dangerous can't be ticked (memlog L87, L116; FR-20) |
| 20 | A low-risk repair may still need approval because it affects production (L40) | Covered | Glossary "Customer production"; FR-20, where an unticked safe repair needs the customer's yes |
| 21 | Last resort is a condition, not a kind of fix: about 30 minutes, Amine's proposal to validate; never grants extra permissions; prohibited actions excluded (L42) | Covered + CHANGED | Glossary, FR-23, open question 14. Refined: the customer must tick it, it covers safe and risky only, and Orvex's advance permission replaces the run-time yes (memlog L89, L116, L122) |
| 22 | Example message: "Your checkout service is using more memory than usual… If you don't answer, we'll keep watching and won't change anything." (L46) | Covered | FR-11, quoted verbatim. Note: since memlog L160, an already-authorised repair may still run on silence, so "won't change anything" holds only when nothing is ticked or last-resort permitted. FR-14 words this correctly |
| 23 | **Example night, with Nightshift:** an alert hours before trouble; approve → apply, verify, undo; no answer → no change; sudden failure → a permitted fix, otherwise report and call; morning summary with the timeline (L44–50) | Partial | Each step exists (FR-9, FR-11, FR-24, FR-22, FR-19, FR-13, FR-16), but no user journey follows the **predictive** path, which is the core promise. UJ-1 to UJ-3 all start after failure (memlog L152). "Sudden failure → permitted fix, otherwise report and call for help" is only implied by FR-18 to FR-20 |
| 24 | **"Quiet unless it matters"**: phone call only for critical problems; alert when a decision is needed; everything else to the dashboard and summary (L52) | Covered | 3.3 description ("It stays quiet unless something matters"), FR-12 ("visible does not mean notified"), FR-13 |
| 25 | **Plain words** for a non-expert owner (L14, L29) | Covered | FR-11, NFR-8, SM-5; Danny's "a few sentences anyone can follow" in 3.3 |
| 26 | Customer chooses **what Nightshift may read** (infrastructure only, or also app and code) (L54; addendum L68) | Partial | Opt-in for the app (FR-1, FR-8) and for code (3.10) is there, but there is no read-scope setting in the Glossary or FRs |
| 27 | **"Permission to read never means permission to change"** (L54) | **GAP** | The principle is not stated. It is implied only by the two separate catalogues and FR-20 |
| 28 | Customer chooses who answers fix requests (L54) | Covered | Glossary "Approval" (customer, or delegated Orvex support) |
| 29 | **Some** risky fixes need Orvex's approval after the customer's (L54) | CHANGED | **All** risky repairs need it (memlog L80, L87); the approver is the Nightshift team only (memlog L110, L113) |
| 30 | Nightshift explains what it sees and does to both the customer and Orvex (L54) | Covered | 3.3 description, FR-12 |
| 31 | Code fixes (experimental): opt-in; an Orvex engineer tests and approves; never applied alone; in v1 to learn (L56) | Covered + CHANGED | 3.10. They now follow the repair path (memlog L133), run only with an in-cluster model (memlog L134), and use customer-specific catalogue entries (memlog L137, L138) |

## 4. Brief: What Makes This Different

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 32 | Honest positioning: not better than existing tools at any single task; like K8sGPT and HolmesGPT (existing models and monitoring) and HolmesGPT, Datadog and Azure SRE Agent (approval and pre-approved fixes) (L60) | **GAP** | No positioning or competitive section; none of these names appear |
| 33 | Value lies in the combination and the fit to Quornex, building on proven open-source tools (L60) | **GAP** | See row 3 |
| 34 | Caveat: whether the combination is unique "is a claim to demonstrate, not a fact" (see `research-landscape.md`) (L60) | **GAP** | Also, memlog L12 asks to "preserve uncertainty markings" from the research, but the PRD never cites `research-landscape.md` |
| 35 | Built for one platform: test a repair once and reuse it fleet-wide; one cluster's lesson prepares the others (L62) | Covered (as features) | 3.9 (Danny quote), FR-35–FR-38. It is not presented as a differentiator |
| 36 | Privacy by design, with the caveat "not a claim that nobody else offers it" (L63) | Partial | The privacy requirements are fully covered (Section 4). The honesty caveat is gone |

## 5. Brief: Success criteria and measurement methods

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 37 | Targets are estimates, checked first in controlled tests, then on the first 100 clusters (L67) | Covered | Section 8 header |
| 38 | Early detection ≥ 80%; method: alert times vs injected-failure records and app health checks (addendum L76) | Covered | SM-1 |
| 39 | Repairs ≥ 95%; method: action logs and traces, before/after health checks, incident reviews (addendum L77) | Covered | SM-2 |
| 40 | Repairs that caused damage, counted separately, every case reviewed (L73) | Covered | SM-3; target still open (open question 12). CHANGED: zero harm is a goal, not a pass/fail condition (memlog L54) |
| 41 | Codex's caveat: at 250 repairs a night, 95% still leaves about 12.5 failed attempts a night (addendum L60) | Partial | The "proposed, not observed" caveat is kept; the 12.5-a-night illustration is not |
| 42 | Alerts ≥ 90% needing attention; method: label each alert actionable, duplicate or false alarm (addendum L77) | Covered | SM-6 |
| 43 | Customer feedback on explanations, measured separately, target to set (L75) | Covered | SM-5, with the three-check method (memlog L156) |
| 44 | Clusters per engineer; method: measure on the first 100 clusters, then extrapolate (addendum L78) | Covered + CHANGED | SM-8, with about 15 engineers (memlog L117) |
| 45 | Estimate the Nightshift-team and support workloads **separately** (addendum L54, L78) | Partial | COST-1 lists support as a cost; SM-8 and SM-9 cover only the Nightshift team. Support headcount is not estimated |
| 46 | Staffing: the pessimistic scenario (60% automated, 45 min each ≈ 75 human hours a night) alongside the optimistic one (90%, 20 min ≈ 8.3 h) (addendum L54) | **GAP** | SM-8 quotes only the optimistic scenario, yet SM-9 (share needing a person) is still "target to set". The case that would break the 15-engineer estimate is silently gone |
| 47 | Availability ≥ 99.9% (assumption); "measurement method to be defined" (L77; addendum L79) | Partial | SM-7 states the target. That the method is undefined is said nowhere, not even in open question 12 |
| 48 | Unapproved changes = 0; method: compare execution, approval and policy records (addendum L80) | Covered | SM-4, FR-32 |
| 49 | Cost: model, then measure at 100 and 10,000 clusters, **with hosted AI and with an in-cluster GPU**, including GPU, monitoring, storage, model use and shared infrastructure (addendum L81) | Partial | COST-1 to COST-3 and SM-10 cover the components and scales. Measuring per model option is not required |

## 6. Brief: Scope, Ground Rules, open questions, to test

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 50 | v1 scope list; nothing deferred (L83–85) | Covered | 9.1 |
| 51 | "Both model options" (L83, L92) | CHANGED | Three options, adding a shared GPU (memlog L149, L151; Section 5) |
| 52 | Hardware: customer's responsibility; faults detected, not physically repaired (Corrections L123–125) | Covered | Glossary, 3.4, 9.2 (memlog L26, L45) |
| 53 | One customer per cluster; customer control cluster; each cluster looks after itself (L97; Corrections L124) | Covered | Glossary, 3.7, FR-46, NFR-5 |
| 54 | Same configuration everywhere; tuning within Orvex's limits (L93) | Covered | NFR-3, FR-39 |
| 55 | Nothing done in secret; least privilege (L94) | Covered | FR-31–FR-33, SEC-4 |
| 56 | Only approved, sanitised information leaves; raw logs and secrets stay (L99) | Covered + CHANGED | PRIV-2. Tightened: private data does not move even between one customer's clusters (memlog L142) |
| 57 | Customer data, databases and backups never changed or deleted (L100) | Covered | 9.2, Glossary "Prohibited action"; wording refined by memlog L160 |
| 58 | No improvised repairs; tested catalogue; AI invents no scripts; solved fixes added (L101) | Covered + CHANGED | FR-17, FR-35. Two catalogues (memlog L66, L77); a fix enters only once tested and well controlled (memlog L20) |
| 59 | Open questions for Danny: 99.9% meaning; Orvex approval after the customer's; how a night like the example is handled today (L106–108) | Covered | Open questions 4, 2 and 5 |
| 60 | To test: every estimate, starting with 250 a night (L110) | Covered | Open question 13 |
| 61 | To test: whether a 24 GB or 96 GB model is useful enough, not just whether it fits (L110) | Covered | Section 5, open question 15 |
| 62 | To test: whether GPU sharing meets the privacy rule and saves money (L110) | CHANGED / Covered | Privacy settled by decision: a shared GPU has the same boundary as a hosted model (memlog L149). Savings: open question 15 |
| 63 | To test: whether filtering keeps private data inside (L110) | Covered | PRIV-6, open question 16 |

## 7. Brief: Vision

| # | Brief item | Status | Where / note |
|---|---|---|---|
| 64 | Orvex becomes "the ultimate DevOps platform": it runs, monitors and heals the cloud for its customers (L114) | **GAP** | The PRD Vision (memlog L21, L55, L58) is functional; this ambition is missing |
| 65 | "Nightshift is not a side product. Orvex's main goal needs it." (L114) | **GAP** | Not stated |
| 66 | Danny's goal: **let a million companies operate their own cloud at low cost**, so that **"a small underfunded startup in Tunisia"** has the same setup as a well-funded enterprise, and private cloud genuinely competes with public cloud (L116) | **GAP** | Neither phrase, nor the "compete with public cloud" aim, appears. Vision Q3 (memlog L55) changed the customer framing, but no decision drops the why |
| 67 | At least 3 years of heavy reliance on hosted AI (L118) | Covered | Section 5, FR-41 |
| 68 | As GPUs get cheaper and open models improve, more can run inside the cluster (Danny) (L118) | **GAP** | The direction of travel is missing, though it matters for FR-41's small sample |
| 69 | v1 is a way to learn; features such as code fixes may or may not stay (L118) | Covered | 9.1, 3.10 |

## 8. Brief addendum

| # | Addendum item | Status | Where / note |
|---|---|---|---|
| 70 | Routing proposal: full, no or mixed permission (L5–11) | CHANGED | FR-12, which says it replaces the proposal (memlog L111, L113) |
| 71 | Every problem that needs a person first appears on a monitoring page; optional live view (L7) | Covered | FR-14, FR-15 |
| 72 | 10–15 engineers watch over Nightshift; a separate support team handles customer incidents (L16) | Covered | Section 6, FR-12 (memlog L117) |
| 73 | **Code fixes as a service, priced by contract by tokens or difficulty** (Amine's proposal, pending Danny) (L17, L70) | **GAP** | No pricing anywhere and no decision dropping it. FR-43 measures cost but not price |
| 74 | Coaching points: separate read, fix and approve; should the platform team get customer incidents; does Nightshift change customer code (L19) | Partial | Fix and approve are separated (FR-20); the platform team point is settled by FR-12; code is settled by 3.10. "Read" is not separated (rows 26–27) |
| 75 | Danny: minimise inference and token cost by every technique; rules first (L23–24) | Covered | FR-47, COST-4 |
| 76 | GPU options: about $1,000 for 24 GB, about $10,000 for 96 GB, and sharing (L25) | Covered | Section 5 (with Codex's $14k–16k) |
| 77 | Sharing within one customer's clusters as a middle ground (L25, L34) | CHANGED | PRIV-1: private data stays in its originating cluster (memlog L142); shared GPU gets sanitised data only (memlog L149) |
| 78 | Target at 100 and 10,000 clusters; **no fixed budget** (L26) | Partial | COST-1, COST-4; "no fixed budget" is missing |
| 79 | "$1 less per cluster saves about $10,000 a month at 10,000 clusters" (Amine) (L31) | Partial | COST-4 has Danny's "a few dollars per cluster makes a huge difference"; Amine's arithmetic is missing |
| 80 | **Cheaper options must stay reliable: no slower responses and no loss of capacity** (L33) | **GAP** | No requirement or counter-metric. SM-C3 guards privacy against cost, but nothing guards latency or capacity against cost |
| 81 | Codex: removing recognisable secrets isn't enough (the `acquisition_of_company_X` example); build messages from approved fields only (L39–46) | Covered (partial) | PRIV-2 (approved fields, placeholders). The example that motivates it is not kept |
| 82 | Keep sensitive cases local when they can't be safely summarised (L47) | Partial | PRIV-2's "time and type only" for strict customers is close, but there is no per-case fallback rule |
| 83 | Defensible claim: evaluate shared inference; test the remaining risks; evidence, not proof of zero risk (L48–49) | Covered | PRIV-6, Section 5 |
| 84 | Incident definition (one failure = one incident), split self-resolved from human-needed, plan for fleet-wide peaks (L53) | CHANGED / Covered | New fault, failure, incident and problem terms (memlog L82, L84); SM-9; FR-30 |
| 85 | GPU memory facts: Qwen3-32B 4-bit about 19.1 GB short vs 27.7 GB at 30k tokens; RTX 3090 and RTX PRO 6000 (L55) | **GAP** | Belongs in the PRD addendum for architecture and cost; not carried |
| 86 | GPU purchase spread over 36 months ($27.78/month, $2.78 shared by 10, …), excluding host, power and operations (L56) | Partial | COST-2 lists the exclusions as costs to include. The figures are not carried; 4.3 defers numbers to the cost model |
| 87 | Hosted example: $0.04 a call, about $3,000 a month fleet-wide, about $0.30 per cluster; +$1.20 per extra daily call (L57) | **GAP** | Not carried to the PRD addendum, so the cost-model author has no PRD-side source |
| 88 | **Main cost driver: how often Nightshift calls AI and how much context it sends**; GPU savings not established (L58) | Partial | FR-47 says "every trick". The driver itself is not named and no metric tracks calls or context per problem |
| 89 | Filtering test plan: seed fakes, inspect outbound requests, block unexpected formats, **test bypass paths around the gateway**, **check that diagnosis still works on sanitised data**; Presidio caveat (L59) | Partial | PRIV-6 covers planted secrets only. Bypass testing and diagnosis quality on sanitised data are missing |
| 90 | Hardware failures are a central case (L64) | Partial | See row 8 |
| 91 | Customer settings detail: read scope, permitted fixes, approver, last-resort fixes (L68) | Partial | All but read scope are covered (Glossary, FR-20, FR-23) |
| 92 | Code-fix detail: never touches databases, backups or customer data (L70) | Covered | 9.2 applies generally; FR-40 |
| 93 | Notification detail: phone criteria; dashboard and summary hold metrics, patterns (the 3 AM peak) and successful repairs (L72) | Covered | FR-13, FR-16 |
| 94 | Other open questions: who decides what is a "high-confidence" repair; night cover today; trusted models and regions; hand-in date (L83) | Covered / CHANGED | Open questions 5–7. "High-confidence" is superseded in effect by evidence-to-act per catalogue entry (memlog L57, FR-18), but this is not closed explicitly |
| 95 | To test: compare local and hosted models on the same cases (**diagnosis accuracy, unsupported claims, tool-call correctness, response time, simultaneous incidents**) (L87) | Partial | Open question 15 says only "useful enough". The evaluation criteria are dropped |
| 96 | To test: the honest filtering result, with scope stated (L88) | Covered | PRIV-6 |
| 97 | To test: claims in `research-landscape.md` are unchecked (L89) | **GAP** | Not carried, because the positioning was dropped (rows 32–34) |
| 98 | Ratings: define "dangerous"; can a dangerous repair be permitted in advance? (L95) | Covered | Glossary; FR-20 says it cannot be ticked |

## Gaps, with a suggestion for each

The most important ones come first.

1. **Vision: the "why" is gone** (rows 64–66, 68). Add a short paragraph to the Vision covering Danny's "million companies" and "small underfunded startup in Tunisia", private cloud genuinely competing with public cloud, Nightshift as what Orvex's main goal needs, and the move toward in-cluster AI as GPUs get cheaper.
2. **Positioning and its honesty caveats** (rows 3, 32–34, 36, 97). Add a short "Positioning" note to Vision or an appendix: not better at any single task; similar to K8sGPT, HolmesGPT, Datadog and Azure SRE Agent; value in the combination and the Quornex fit, building on open-source tools; uniqueness "a claim to demonstrate"; privacy not unique; `research-landscape.md` claims unchecked.
3. **Problem and example night story** (rows 7, 8, 10, 11, 23). Add a brief "Problem" lead-in (the before story: shoppers notice first, Orvex last) and a journey UJ-0 that follows the predictive memory-creep path end to end (alert hours ahead → approve → verify or undo; no answer → no change), because no current journey shows prediction.
4. **"Permission to read never means permission to change", and the read-scope setting** (rows 26, 27, 74, 91). Add a Glossary entry or FR for read scope (infrastructure only, plus app, plus code) and state the principle explicitly.
5. **Pessimistic staffing scenario** (row 46). Next to the 90% / 20-minute case in SM-8, add Codex's 60% / 45-minute case (about 75 human hours a night) so the 15-engineer estimate is defended against its worst case.
6. **Cheaper must not mean slower** (row 80). Add a cost counter-metric (SM-C4): lower cost is good, but not at the price of slower responses or lost capacity.
7. **Support workload estimated separately** (row 45). Add support headcount, or a support workload estimate, to SM-8 or COST-1.
8. **Code-fix pricing** (row 73). Either record a memlog decision dropping "code fixes as a service" pricing, or add it as an open question for Danny.
9. **Cost and GPU inputs not carried downstream** (rows 79, 85–88). Copy Codex's figures (Qwen memory at short and long inputs, 36-month GPU spread, $0.04-a-call hosted example, "main driver = call frequency × context size", $1 per cluster ≈ $10k a month, no fixed budget) into the PRD addendum's "For the architecture" section, marked as unverified.
10. **Model-comparison criteria** (row 95). Extend open question 15 with the comparison criteria: diagnosis accuracy, unsupported claims, tool-call correctness, response time and simultaneous problems.
11. **Filtering test scope** (rows 82, 89). Add to PRIV-6: bypass-path tests around the outbound gateway, blocking unexpected formats, checking diagnosis quality on sanitised data, and keeping a case local when it can't be summarised safely.
12. **Availability method** (row 47). Mark in SM-7, or in open question 12, that the availability measurement method is still to be defined.
13. **Cost per model option** (row 49). Make SM-10 require cost to be measured with hosted AI and with an in-cluster GPU.
14. **Minor items** (rows 13, 41, 94). Give the reason the Nightshift team is the primary user; add the "about 12.5 failed repairs a night at 95%" illustration to SM-2; close "high-confidence" explicitly as superseded by FR-18.
