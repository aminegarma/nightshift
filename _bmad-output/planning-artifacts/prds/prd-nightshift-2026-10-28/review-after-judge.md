# Judge review (second pass): PRD Nightshift

Reviewer stance: Danny at Orvex AI, author of the brief, reading the PRD as it stands on 2026-10-31 (`prd.md` updated 2026-10-31, `addendum.md`). Inputs: the brief (`brief.pdf` text), `danny-qa.md` Exchanges 1-4 (Exchange 5 still awaiting a reply). Earlier review files were not read.

## Overall verdict

A disciplined, honest, well-traced PRD that answers most of the brief's "must answer" questions at requirement level and hands the rest cleanly to the other deliverables. Its main weaknesses are not missing sections but design tensions it has not confronted yet: the approval model (two humans for every risky repair, customer approval of Orvex's own platform) collides with Danny's "self-managing", "fully managed by us" and "close to public-cloud reliability" goals and with the cost target. And the compromised-agent story covers everything except the cluster the agent sits in.

## Per-criterion verdicts

| Criterion | Verdict | One-line reason |
|---|---|---|
| Technology choices | **Adequate for a PRD (handed off)** | Correctly deferred to the architecture (Section 11), but the PRD leaves the requirements that would discriminate between tools (footprint, retention, timing) as "target to set" |
| Architecture clarity (bare metal and EKS) | **Good, with gaps** | The three-level model, out-of-band rules, limited-visibility mode and "each cluster on its own" are clear. EKS is under-described, the case without a BMC on cheap hardware is treated as the exception, and the PRD never says what happens when the model is unavailable |
| Privacy and security | **Good on privacy, one major security gap** | Allowlists on every outbound channel, placeholders, an outbound check, planted-secret tests and honest proof claims are strong. A compromised agent's power inside its own cluster is not addressed, and the PRD does not say whether free-text log lines ever leave the cluster |
| Cost credibility | **Structure good, credibility at risk** | Two numbers per cluster, a without-Nightshift baseline, full GPU cost and who pays are all right. But the PRD's own design choices make human time the dominant cost, it never says so, and the 100-cluster case will not be "a few dollars" |
| AI fluency | **Strong** | Every statement is tagged with its source; AI suggestions are marked as accepted, reworded or unconfirmed; Codex's figures are labelled "partly checked". The volume of provenance tags hurts readability, and some AI-sourced tables are not visibly verified |
| Honest thinking | **Strong** | Uses [OPEN], [To test] and "proposed, not observed" labels; makes no 100%-privacy claim; validates rare events with failure injection; shows staffing sensitivity arithmetic. It falls short on the tensions between its own requirements, which it does not name (approval latency vs 99.9%, one engineer vs its own workload arithmetic) |

## Findings

### Critical

None. Nothing in the PRD would make Danny reject it outright. The high findings below are what he will push on hardest.

### High

**H1. A compromised agent's blast radius inside its own cluster is not covered (SEC-2, SEC-4).**
SEC-2's table covers other clusters, audit records, approvals and hardware credentials, but not the cluster the agent runs in. If the Nightshift agent holds standing Kubernetes write rights (drain, restart, scale, roll back) and read access to Secrets, then a compromised agent can do all of that directly. "Enforcement sits outside the agent" cannot work if the agent holds the credentials that carry out repairs. This is exactly the brief's question: "How do you stop … a compromised agent from doing harm?"
*Fix:* add SEC-8. The observing and reasoning agent has read-only rights and no access to Secrets by default. Repairs run through a separate executor that receives a short-lived credential for one catalogue action on one target, only after the rule-based policy check and approval verification, which sit outside the agent (for example an admission or policy controller). List what a compromised agent can still do (read diagnostics, send false evidence, refuse to act) and how each is limited or detected.

**H2. The approval model conflicts with the 99.9% availability target, and the PRD does not say so (FR-21, FR-23, FR-24, SM-7).**
An unticked risky repair needs the customer (a non-expert business owner, possibly asleep) and an Orvex engineer at the same moment. The last-resort condition covers only failure *predicted* within 30 minutes, not failure already in progress (UJ-2: checkout is down). One unanswered night uses up the 43-minute monthly budget. Danny said "safe repairs should be automatic" and wants it "as close to self-managing as possible".
*Fix:* add a requirement or metric for approval latency (time from request to decision, by hour of day). Extend the last-resort condition to cover outages in progress for ticked repairs. State explicitly in Section 10 that the availability target depends on approval latency and on how many risky repairs customers tick, and make it something to test.

**H3. The default mode and the default checklist are undefined, so it is unclear whether safe repairs are automatic out of the box (Glossary, FR-21).**
Danny (Exchange 4): "Safe repairs should be automatic, while risky changes require approval." The PRD makes safe repairs automatic only if ticked. It never says whether a new customer starts in alert-only or approval-enabled mode, or with an empty or pre-ticked checklist. If the checklist starts empty, a non-expert owner is asked to approve disk cleanups at 3 AM. That defeats the persona ("chose Quornex so they would not need DevOps staff") and adds load to SM-8 and SM-9.
*Fix:* state the defaults. Proposal: approval-enabled mode, with safe repairs pre-ticked and the customer able to untick them; risky repairs unticked. Record it as a proposal and list it among Danny's open questions.

**H4. Customer approval of Orvex's own platform changes departs from "fully managed by us" and "the same tested release everywhere" (FR-47, Glossary "Customer production", NFR-3).**
Because "customer production" covers any layer, repairs and updates to Quornex's managed databases and to OMK need the customer's policy or approval. If a customer never authorises a maintenance policy, versions drift apart, which contradicts NFR-3 and the brief's ground rule. Public clouds do not ask before failing over a managed database. The PRD marks this as pending Danny (Exchange 5 Q2), which is honest, but it does not acknowledge the conflict with NFR-3 or offer a fallback.
*Fix:* name the conflict in FR-47. Propose a contract-level default: Orvex has authority over its own platform components within a maintenance window agreed in the contract, with notice and the right to defer for a bounded period (for example N days), after which the update is mandatory. Per-action customer approval would remain only for changes that touch customer apps or data.

**H5. Requiring Orvex technical approval for every risky repair, even when ticked, is the largest cost and latency driver, and the PRD does not present it as a trade-off (FR-21, SM-8, SM-9, COST-1).**
Danny's model (Exchange 1) is that the customer approves, optionally delegating to Orvex support. The extra Orvex approval is Amine's addition (Exchange 5 Q1, unanswered). It puts one night engineer between every risky repair across 10,000 clusters and the action. The PRD's own arithmetic (SM-8) shows staffing swinging from about 8 to about 75 hours a night depending on the automatic share, yet Section 7 and COST-1 do not name human approval as the main cost lever.
*Fix:* in the cost section, state that human time, driven by the share of repairs needing Orvex approval, is expected to dominate the per-cluster cost, and require the cost model to show the sensitivity. Offer a path to earn autonomy: after N verified successes under defined conditions, a reviewed reclassification can drop the per-run Orvex approval (FR-21 already allows reviewed reclassification, so connect the two).

**H6. Nothing says how Nightshift behaves with no model available (Section 7, NFR-4, NFR-5).**
There is no requirement that detection, rule-based matching, safe repairs, notifications and the record keep working when the hosted model is down, rate-limited or too expensive, or when a sovereignty-minded customer refuses any hosted model. The "time and type only" strict mode suggests this case but never states the consequence. It matters for availability ("what if Nightshift fails" extends to its dependencies), for cost (it caps model spend) and for Danny's sovereign-cloud pitch.
*Fix:* add NFR-9. The safety loop (detect, match by rules, authorise, act, verify, record) needs no model. Without one, explanations fall back to templates built from the rule-based facts. List what is lost without a model (help matching new problems, richer explanations, code fixes).

### Medium

**M1. It is unclear whether free-text log excerpts ever leave the cluster (PRIV-2 to PRIV-4).** PRIV-2 describes "a small message built from approved fields", while PRIV-4 checks "every whole line about to leave", which implies log lines do leave. That is the heart of the brief's question "strip private data first". *Fix:* say explicitly which applies. Either only structured, allowlisted fields leave, or sanitised log excerpts may leave under these conditions. Give one worked example (the memory-leak case) of exactly what the hosted model receives.

**M2. The outbound check (PRIV-4) checks for injected instructions but does not explicitly check for leftover private data.** *Fix:* the check also scans for leftover secrets and personal data (patterns, entropy, known customer identifiers) and blocks the message if any are found. Planted-secret tests (PRIV-7) then measure how well this works.

**M3. "Private data" is not defined.** Is it only PII and secrets, or also hostnames, IP addresses, service and table names, and business data in queries? For a sovereign-cloud customer, the names in their architecture may be sensitive. *Fix:* add a Glossary entry with categories, and state that the allowlist (PRIV-3) is the operative control, not the definition.

**M4. EKS is described only as "the signals the provider makes available".** On EKS with managed node groups, worker nodes are EC2 instances in the customer's account, so node OS, disk and memory signals are fully visible. Only the control plane is the provider's. Node replacement through the Auto Scaling group is a possible (risky) repair. A hosted model in the customer's own cloud account (for example Bedrock in the same region) is a privacy option Section 7 does not consider. *Fix:* add a short OMK vs EKS comparison table (visible layers, repair levers, hardware path, model options) or require it of the architecture in Section 11.

**M5. Without out-of-band management, limited-visibility mode is likely the common case on cheap hardware, but it is treated as the exception (FR-7, FR-8).** Danny describes "cheap, unreliable and potentially poorly maintained bare metal". *Fix:* define the in-band hardware baseline (SMART, ECC/EDAC, NIC counters and link state, kernel logs, temperature sensors) as always present, and the BMC as an enhancement. Ask the failure catalogue to tag each failure as visible in-band, needs a BMC, or invisible.

**M6. Fleet learning has no speed target and only one, slow path (FR-37 to FR-40).** Every lesson goes through a person, two reviewers and a full tested release. The brief asks that a new problem "make every other cluster ready for it". *Fix:* split the paths. Detection and explanation rules, which only alert, can ship faster through a lighter signed channel. New repairs go through the full release. Add a metric: time from first occurrence to fleet readiness.

**M7. Tuning is one line (FR-41).** The brief's opening quote is "tuning and self-healing". It is unclear whether a tuning change is a repair (risk level, tick, verification, rollback) or a separate mechanism, and what "limits" look like. *Fix:* state that every tuning change is a catalogue repair with bounds set by the release, a risk level, verification and rollback. Give one or two examples (requests and limits, autoscaler bounds, disk-pressure eviction thresholds).

**M8. There is no requirement for detecting problems that are not in any catalogue.** FR-19 handles new problems once found, but nothing requires generic symptom-based detection (service-level-objective burn, error-rate and latency anomalies, log-pattern changes) to catch them. *Fix:* add an FR for symptom-based detection that is independent of the catalogue.

**M9. The workload estimates look optimistic against Danny's framing, and the staffing claim contradicts its own arithmetic (NFR-1, SM-8).** 250 problems a night across 10,000 clusters is one problem per cluster every 40 nights, on hardware Danny calls unreliable, under a platform he calls "a complex mess … a million things can go wrong". And "one engineer on duty" faces about 8 hours of work at 250 problems and about 17 at 500, under the PRD's own best case. *Fix:* give the source or reasoning behind 250, run the cost model over a range (for example 250 to 2,500), and make the night staffing a function of the automatic share instead of a fixed headcount.

**M10. Model call volume is not bounded in the PRD.** Section 11 asks the architecture for it, but the PRD never states whether the model reads logs continuously ("constantly looking at logs") or is called only per problem. That decides whether model cost is negligible or dominant. *Fix:* state the intended mode: called per problem, with rules and statistics on the continuous stream. Ask the cost model to test both.

**M11. Section 11 under-specifies the failure catalogue and the privacy and security review.** *Fix:* the failure catalogue gives its ranking criteria (frequency × impact × whether it can be detected), plus per failure the detection signals, time to impact, catalogue repair with risk level and approval path, and in-band vs BMC visibility. The privacy and security review includes a data-flow diagram per outbound channel, the first allowlist, a threat model (STRIDE or similar) and the compromised-agent analysis from H1.

### Low

**L1. The provenance tags are dense** ("review fix, 2026-10-30, approved by Amine" appears about 20 times). They are good for AI fluency but slow down a 15-minute read. *Fix:* keep short tags, or move them to a trace table, and leave one line explaining the convention.

**L2. Naming collision:** "Incident" means user-visible disruption, while the "incident catalogue" holds any problem without a tested fix. *Fix:* rename it, for example "investigation catalogue" or "known-problem catalogue".

**L3. App monitoring is either fully opted in or off.** Quornex deploys the customer's app, so platform-level health (restarts, golden signals) could be watched without reading app logs or code. UJ-1 and UJ-2 depend on opt-in. *Fix:* separate "platform-level health of the customer's app (always)" from "app logs and code (opt-in)".

**L4. Code fixes do not say where code comes from or goes to** (repository access, pull request vs direct deploy) or who pays for the isolated test environment (COST-3). *Fix:* one line each.

**L5. Sanitised evidence vs judging a repair.** An Orvex engineer approving a risky repair sees only sanitised evidence (PRIV-2 covers Slack and the portal). Say whether that is enough to judge it, and if not, how in-cluster evidence is viewed without exporting it.

**L6. The success targets (80%, 95%, 90%) have no reasoning behind them.** *Fix:* one line on why each threshold was chosen, or label them as placeholders.

## Where the PRD departs from Danny's stated wishes

| # | Danny said | PRD does | Status |
|---|---|---|---|
| 1 | "Safe repairs should be automatic" (Ex 4) | Automatic only if the customer ticks them; the default is undefined | Not raised with Danny; see H3 |
| 2 | Customer approves, optionally via Orvex support (Ex 1) | Adds Orvex technical approval for every risky and dangerous repair, even when ticked | Asked in Ex 5 Q1; pending |
| 3 | Quornex "fully managed by us"; "same tested release everywhere" (brief) | Platform updates and repairs need a customer maintenance policy or approval | Asked in Ex 5 Q2; conflict with NFR-3 not acknowledged (H4) |
| 4 | GPUs shared across clusters worth exploring (Ex 3) | PRIV-1 forbids private data moving even between one customer's clusters, so a shared GPU gets only sanitised data | Asked in Ex 5 Q3; stricter than the brief requires, and defensible |
| 5 | Code fixes in the first version, to see them in real use (Ex 2); heavy hosted-AI use (Ex 3) | Hosted model only with separate consent; a mandatory Orvex engineer reads the code, and the patch is rejected if the customer refuses access | Open question 7a; defensible, but limits the experiment's reach |
| 6 | "Make every other cluster ready for it" (brief) | Fully human-gated, release-bound learning, with no speed target | Not raised; see M6 |
| 7 | "Tuning and self-healing" (brief quote) | Tuning reduced to one line | Not raised; see M7 |
| 8 | "Our bare metal" (brief) | Follows Ex 4: customers own the hardware | Correct; Ex 4 overrides |
| 9 | Exchange 5 email: dangerous repairs need "a more thorough recovery review"; privacy boundary named "raw logs and secrets" | FR-21 now has "a recovery plan reviewed before the repair runs"; PRIV-1 covers all private data | Aligned in substance; the broader privacy wording is stricter than the email. Make sure the walkthrough uses the PRD's wording |

## Likely Q&A questions

1. "It's 3 AM, checkout is down, the owner is asleep and the repair is risky and unticked. Walk me through the next 30 minutes. How does that fit with 99.9%?" (H2)
2. "Someone owns the Nightshift agent in one cluster. What can they do *in that cluster*? Where do the write credentials live?" (H1)
3. "Give me the number: cost per cluster per month at 100 and at 10,000 clusters. What dominates it? Isn't it your engineers?" (H5, M9)
4. "Why does Orvex need to approve a risky repair the customer already ticked? Doesn't that make us the bottleneck?" (H5)
5. "Why would a customer approve our own platform updates? What if they never do: do we run 10,000 different versions?" (H4)
6. "Show me exactly what the hosted model sees in the memory-leak example. Do log lines leave the cluster?" (M1)
7. "Where is a language model actually worth it? How many calls per cluster per day? What happens when the model provider is down?" (M10, H6)
8. "Most cheap servers have no working BMC. What can you still see?" (M5)
9. "On EKS the worker nodes are EC2 instances the customer runs. Why only 'the signals the provider makes available'?" (M4)
10. "How long until a lesson from one cluster protects the other 9,999?" (M6)
11. "Where does 250 problems a night come from? I told you a million things go wrong." (M9)
12. "Which parts of this did Claude or Codex write, and how did you check them? Show me where you overruled it." (AI fluency; for example the FR-8 table and the GPU prices)
13. "What does Nightshift itself cost the customer in CPU, RAM and storage per cluster?" (NFR-6 target not set)

## What the PRD sets up well for the other deliverables

- **Architecture:** the three levels, the coordinator in each cluster, the independent self-monitor, signed releases, the append-only audit record and the out-of-band management rules are all concrete enough to design against.
- **Failure catalogue:** the FR-8 table and FR-20 (mitigate, report uncertainty, escalate) give a ready classification. M11 adds the ranking criteria.
- **Cost model:** COST-1 to COST-6 and the SM-8 sensitivity arithmetic give a clean structure. It needs the call-volume and footprint inputs (M10, NFR-6).
- **Privacy and security review:** PRIV-1 to PRIV-7 and SEC-1 to SEC-7 give it a strong spine. It needs H1 and M1 resolved first.
- **README open questions:** Section 10 is already triaged and can be carried over directly.
