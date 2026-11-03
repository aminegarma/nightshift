# Extract: brief trail (source material for the PRD)

Extracted 2026-10-28 from the brief's supporting files. No new ideas added; statuses kept as the sources state them.

Source keys: **ADD** = `briefs/brief-nightshift-2026-10-25/addendum.md`; **ML** = `briefs/brief-nightshift-2026-10-25/.memlog.md` (line number + opening words); **REV** = `briefs/brief-nightshift-2026-10-25/review-2026-10-28.md`; **S1** = `session-1-notes.md`; **S2** = `session-2-understanding-check.md`.

Tags: [Danny] Danny said it; [Amine decision]; [assumption]; [estimate]; [unverified claim] (includes Claude's coaching feedback in S2, which S2 says was not checked against primary sources); [Codex-checked] (figures/opinions as reported by Codex, not re-checked by Claude); [open question].

## 1. Repair risk rating and the repair catalogue

- Every repair in the catalogue is rated safe, risky or dangerous and handled accordingly. — ADD § Repair catalogue ratings; ML L112 "(decision) Repair catalogue (Amine)" — [Amine decision]
- When Nightshift meets something new and it gets solved, the fix is added to the catalogue and tested before release. — ADD § Repair catalogue ratings; REV § Amine's decisions (S3) — [Amine decision]
- Risk (safe/risky/dangerous) and authorisation (permitted/approved) are separate questions; there is no mapping from ratings to "kinds of fix". — ADD § Repair catalogue ratings ("Superseded (same day)"); ML L115 "(override) Amine corrected the AI's fix tiers" — [Amine decision]
- "Dangerous" is not yet defined; the PRD must define it and decide whether a dangerous repair can ever be permitted in advance or always needs approval at the time. — ADD § Repair catalogue ratings ("For the PRD"); ML L118 "'Dangerous' left for the PRD to define" — [open question]
- Prohibited actions can never become permitted through advance approval. — ADD § Repair catalogue ratings; ML L115 — [Amine decision]
- Changing or deleting customer data, databases or backups is never allowed, even with approval, not even in emergencies (permanent Ground Rule). — ML L81 "(decision) Out of first version (Amine)"; ML L85 "(override) ... never allowed, even with approval" — [Amine decision]
- No improvised repairs: only repairs from a catalogue of known problems and fixes, tested before release; the AI may not invent repairs, especially generated shell scripts or commands. Now a permanent Ground Rule. — ML L81; ML L111 "(decision) Review decisions (Amine)"; REV § Amine's decisions (S3) — [Amine decision]
- Who decides what counts as a "high-confidence" repair. — ADD § Other open questions for Danny — [open question]
- Claude coaching feedback: prefer small, reversible actions; when in doubt hold steady (cordon, watch, escalate) and call a person; never take a bigger action because nobody answered. — S2 § Gaps #1 Safety mindset — [unverified claim]
- Claude coaching feedback: the model explains and suggests, plain code decides and acts; actions come from a fixed catalogue, checked by plain code and limited by RBAC. — S2 § Gaps #4 AI design — [unverified claim]
- "What does 'safe repair' mean? Name one safe and one not" was posed to Amine; no answer recorded in these files. — S1 § Questions for you, Q8 — [open question]

## 2. Authorisation

- Danny's model: customer picks alert-only or automatic high-confidence repairs, ticks allowed actions, approves via Slack/portal, and may delegate to Orvex support. — ML L12 "(event) Danny answered" — [Danny]
- Customer settings decide: what Nightshift may read (infrastructure only, or also the app and its code); which fixes it may run without asking; who approves everything else (the owner, or Orvex support if delegated); which pre-agreed fixes it may use as a last resort. — ADD § Moved from the brief (Customer settings) — [Amine decision]
- Customer pre-authorises a list of fixes via contract or portal; needs no DevOps staff. — ML L19 "(decision) Customer needs no DevOps staff" — [Amine decision] (portal/contract per [Danny])
- Flexible per-customer contracts, same Nightshift release everywhere; permissions are granted and removed in cluster settings. — ML L42 — [Amine decision]
- Read is not act: permission to read does not allow changes; Nightshift asks before acting. — ML L43 — [Amine decision]
- Risky fix without authority: do nothing to fix it; keep monitoring and alerting until the owner answers; silence is not approval. — ML L38 — [Amine decision]
- Customer's decisions are bounded "within Orvex's safety limits"; some fixes need Orvex approval after the customer's. — ML L54 "(override) ... the customer's decisions are bounded"; ML L56 — [Amine decision]
- Two-step approval for some risky fixes: customer approves, then Orvex approves, so customer settings can't damage their own app. — ML L55 — [Amine decision]
- Whether Orvex approving after the customer fits Danny's approval model (danny-qa follow-up #8; kept as an open question in the brief). — ML L55; ML L105 — [open question]
- Orvex reviews dangerous cases even after the customer approves; the customer doesn't approve everything alone. — ML L119 "(override) ... Q&A tip premise" — [Amine decision]
- Pre-approved and last-resort fixes need both customer and Orvex approval; Nightshift never changes anything on its own. — ML L89 "(override) ... pre-approved and last-resort fixes need both" — [Amine decision]
- Fix tiers permitted / approved / last-resort were adopted from review S10 ... — REV § Amine's decisions (S10); ML L111 — [Amine decision] (later corrected, see next line)
- ... then corrected: last resort is an execution condition on a fix permitted in advance, not a third kind of fix. — ADD § Repair catalogue ratings ("Superseded"); ML L115 — [Amine decision]
- Last-resort condition: for known problems the customer can agree in advance to a specific fix that Nightshift applies only if there is no answer and failure is about 30 minutes away; otherwise keep watching without changing anything. — ML L44 — [Amine decision]
- The 30-minute threshold is Amine's idea and "a proposal to validate". — ADD § Repair catalogue ratings; ML L115; REV § Amine's decisions (S10) — [assumption]
- An unanswered request or a predicted failure within 30 minutes never grants extra permissions. — ADD § Repair catalogue ratings; ML L115 — [Amine decision]
- Source of the fix-tier correction: Amine's own idea, reformulated with Codex. — ML L117 — [Amine decision]
- Plain-language explanations so a non-expert owner can approve (AI had implied a technical approver). — ML L20 "(override) Amine corrected the AI" — [Amine decision]
- Sudden failures: detect fast, apply a permitted repair if one exists, otherwise report and request human help. — ML L45 — [Amine decision]
- Parked question: at 3am, a risky fix not pre-authorised and owner asleep: wait vs delegated Orvex support. — ML L22 — [open question] (L38 later says: do nothing, keep alerting; delegation remains a customer setting)
- Whether customers approve changes to Orvex platform components (emailed to Danny 2026-10-28). — ADD § Other open questions; ML L91 — [open question]
- Original challenge firm rule: human approval before any change to customer production. — S1 § Important points #3 — [Danny]
- Claude coaching feedback: human approval can be fooled, so show the raw action and the original evidence; signed approvals happen outside the cluster. — S2 § Gaps #4, #6 — [unverified claim]
- Separate "what Nightshift may read" from "what it may fix" and "who approves". — ADD § Alert and approval routing (Open points raised in coaching) — [open question]

## 3. Failure behaviour

- No response: keep monitoring and alerting, change nothing; alerts state time left (e.g. "about 4 hours") and what happens without an answer ("we keep watching and change nothing"). — ML L38; ML L43 — [Amine decision]
- No response near failure: only a fix agreed in advance (by customer and Orvex) may run as last resort, ~30 minutes before failure (proposal to validate). — ML L44; ML L89; ADD § Repair catalogue ratings — [Amine decision] / 30 min [assumption]
- Repair fails or makes things worse: "repairs that caused damage" is a separate success signal from "repairs that didn't work"; every case recorded and traced; target to be set. — ML L100 — [Amine decision]
- "Unsuccessful but harmless" and "caused damage" need separate measures; at 250 repairs a night, 95% success still leaves about 12.5 unsuccessful attempts a night. — ADD § Codex's check (Success targets) — [Codex-checked]
- Claude coaching feedback: kill switch and action limits; fleet rollouts gradual with rollback. — S2 § Gaps #6, #7 — [unverified claim]
- Nightshift unavailable: Nightshift must not go blind when the control plane fails; central Orvex part watches for clusters that go silent. — S2 § Gaps #3 Architecture shape — [unverified claim]
- A heartbeat whose absence is itself the alert (Amine's answer, endorsed in feedback). — S2 § What Amine got right — [assumption]
- Fleet-wide events: plan for peaks such as a bad release hitting hundreds of clusters at once. — ADD § Codex's check (Incidents); ADD § To test — [Codex-checked]; still to settle per ML L94 [open question]
- Claude coaching feedback on failure mechanics: node dies → Deployment pods move, StatefulSet/database pods with local disks get stuck; root cause vs symptoms (timing, location, dependencies, known patterns). — S2 § Gaps #2 — [unverified claim]
- Kubernetes waits about 5 minutes by default before evicting pods from an unreachable node. — S2 § Claims still to verify — [unverified claim]
- Conflicting fixes: no content in these five sources (nearest: multi-cluster "treat a customer's clusters as one unit?" emailed to Danny, ML L91). — — [open question]

## 4. Privacy, data protection and security

- Original challenge rules: logs hold customer data and stay in the cluster; a hosted model sees only what it must; everything Nightshift reads or changes is recorded where the customer can see it, with least-privilege rights. — S1 § Important points #4, #6 — [Danny]
- Shared inference is to be evaluated for cost, not assumed safe. Only approved, sanitised diagnostic fields built into a small message may leave a cluster; raw logs and secrets stay inside; unapproved fields blocked; sensitive cases stay local; residual privacy risk tested; savings measured. — ML L75, L76; ADD § Privacy approach for shared inference — [Amine decision] (from Codex note)
- Removing recognisable secrets isn't enough (example: `Database error: acquisition_of_company_X payment table unavailable`). Build the message from approved fields only (Service / Error category / Failure rate / Duration). — ADD § Privacy approach — [Codex-checked]
- Defensible claim: "We will evaluate shared inference to reduce cost. Only approved, sanitised diagnostic information may leave each cluster; raw logs and secrets remain inside. We will test the remaining privacy risks." — ADD § Privacy approach — [Codex-checked]
- The design doesn't need to prove zero risk; it needs evidence it meets the privacy requirement, and measurements of actual savings. — ADD § Privacy approach — [Codex-checked]
- Filtering test plan: seed fake emails, passwords, keys and confidential business details; inspect real outbound requests; check unapproved fields and unexpected formats are blocked; test bypass paths around the gateway; check diagnosis still works on sanitised data. — ADD § Codex's check (Filtering test plan) — [Codex-checked]
- Honest result wording: "no seeded secrets escaped in these tests", with test scope stated, not proof of 100% privacy (to test). — ADD § To test — [open question]
- Presidio's own docs say automated detection can't guarantee finding everything. — ADD § Codex's check — [Codex-checked]; "Presidio as open-source detector" still to verify — S2 § Claims — [unverified claim]
- Claude coaching feedback: allow-list fields rather than delete private ones; placeholders with mapping kept in cluster; assume some leak, send as little as possible; proof needs a single gateway, append-only record and stripping rules customers can test; provider data use relies on contract and can't be proven. — S2 § Gaps #5 — [unverified claim]
- Customer sees items related to them, especially changes touching their data. — ML L6 — [Amine decision]
- With code-read permission, Nightshift explains a code problem in plain words without touching customer data. — ADD § Alert and approval routing — [Amine decision]
- Which hosted models and regions count as "trusted". — ADD § Other open questions; S1 § Questions for Danny Q3 — [open question]
- GPU sharing within one customer's clusters vs the in-cluster privacy rule: see section 9. — ADD § Amine's cost and GPU thinking — [open question]
- Security, Claude coaching feedback: prompt injection works because instructions and data travel in the same text; human approval can be fooled too. — S2 § Gaps #4 — [unverified claim]
- Security, compromised agent (Claude coaching feedback): keep the record out of the agent's reach; signed approvals outside the cluster; the part that reads untrusted text is separate from the part that holds rights; fleet lessons only proposals, reviewed and signed centrally; kill switch and action limits. — S2 § Gaps #6 — [unverified claim]
- Amine's own understanding (endorsed): read-only diagnosis + execution gate + approval; isolation between clusters + outbound firewall; a person reviews fleet lessons. — S2 § What Amine got right — [assumption]
- Study item: OWASP Top 10 for LLM applications (prompt injection). — S2 § Study list — [open question]

## 5. Measurement

- Early detection: ≥80% of supported, slowly developing failures caught before customer impact; measured first in controlled tests comparing alert timestamps with failure-injection records and app health checks. — ML L57; ADD § How each success signal is measured — [estimate]
- Failure injection = deliberately injecting problems with known solutions to test that rules and the repair guidebook work as designed. — ML L63 — [Amine decision]
- Repair success: ≥95% of authorised attempts restore health without a new incident; measured by action logs and traces, before/after health checks, incident reviews. — ML L57; ADD § How each success signal is measured — [estimate]
- Repairs that caused damage: separate signal, every case recorded and traced; target to be set. — ML L100; ADD § How each success signal is measured — [Amine decision]; target [open question]
- Alert quality: ≥90% useful; operators label each alert "actionable", "duplicate" or "false alarm". — ML L57; ADD § How each success signal is measured — [estimate]
- Operators = Orvex support and the Nightshift team. — ML L113; REV § Amine's decisions (P10) — [Amine decision]
- Customer feedback on clarity and usefulness of explanations measured separately; target to set. — ML L113; REV § Amine's decisions ("New") — [Amine decision]; target [open question]
- Success targets are proposed acceptance targets, not observed performance. — ADD § Codex's check (Success targets) — [Codex-checked]
- Availability: 99.9% monthly for customer-facing platform services (~43 min downtime/month), clearly an assumption; measurement method to be defined. — ML L70; ADD § How each success signal is measured — [assumption]
- The reliability number remains an open question for Danny (kept in brief). — ML L105 — [open question]
- Unapproved changes to customer production = 0; measured by comparing execution audit records against approval records and policy decisions. — ML L61; ADD § How each success signal is measured — [Amine decision]
- Cost: monthly Nightshift cost per cluster (GPU, monitoring, storage, model usage, shared infrastructure), modelled then measured at 100 and 10,000 clusters, with hosted AI and with an in-cluster GPU; target "as low as realistically possible at near public-cloud reliability". — ML L62, L67; ADD § How each success signal is measured — [Amine decision] (target wording [Danny])
- Clusters per engineer: measure human handling on the first 100 clusters, then extrapolate; engineer mainly approves/denies, monitors, guides Nightshift; Nightshift-team and support workloads estimated separately. — ML L58; ADD § How each success signal is measured — [Amine decision]
- Working range 350-400 clusters per engineer; "a range to test, not a commitment". — ML L95, L99 — [estimate]
- Staffing arithmetic: 500/400/350 clusters per engineer = 20/25/29 engineers for 10,000 (headcount, not per shift); at 250 incidents/night, 90% auto at 20 min each ≈ 8.3 human hours/night, 60% auto at 45 min each ≈ 75 hours. — ADD § Codex's check (Staffing) — [Codex-checked]
- Incident definition: one failure = one incident however many alerts it fires; alerts not counted as incidents. — ML L98; ADD § To test — [Amine decision]
- Planning load: 250 distinct incidents a night, up to 500 on a bad night; to validate against operational records. — ML L94 — [estimate]
- 250 a night across 10,000 clusters = one incident per cluster every 40 nights; separate incidents Nightshift resolves alone from outages needing a person. — ADD § Codex's check (Incidents) — [Codex-checked]
- Model comparison (to test): local vs hosted on the same incident cases: diagnosis accuracy, unsupported claims, tool-call correctness, response time, simultaneous incidents. — ADD § To test — [open question]

## 6. First-version scope and boundaries (incl. experimental code fixes)

- Danny: include customer-code repair in day-1 scope as an experiment that may not stay in the final basic product; wants feedback on everything. — ML L40 "(event) Danny (Exchange 2)" — [Danny]
- Customer's own app/code monitored only with opt-in; value there is predicting and alerting hours before failure. — ML L18 — [Amine decision]
- Customer-code bugs in scope as an opt-in (Amine overruled the AI's doubt). — ML L24 — [Amine decision]
- Code fixes: AI-generated, tested, then an Orvex engineer must approve after testing before deployment; Nightshift never applies a code fix on its own; never touches databases, backups or customer data. — ML L86; ADD § Moved from the brief (Code fixes) — [Amine decision]
- Code fixes only with customer approval; the customer can refuse freely. — ML L82 — [Amine decision]
- Code fixes apply only if the customer has allowed Nightshift to read and change their code. — ADD § Alert and approval routing (Amine's update) — [Amine decision]
- Code fixes as a paid Orvex service priced by contract by cost (tokens) or difficulty: Amine's proposal; Danny hasn't addressed it. — ADD § Alert and approval routing; ADD § Moved from the brief; ML L40 — [open question]
- In-scope list confirmed: nothing too much for v1; every item decided deliberately. — ML L82 — [Amine decision]
- Scope "Out" says nothing is deferred; permanent exclusions live in Ground Rules. — ML L114 — [Amine decision]
- Kubernetes and platform-service failures are the part Nightshift takes on: detect early, investigate, handle well-understood repairs, protect customer data. — ML L77 — [Amine decision]
- "Fully managed" = no customer intervention for nodes, disks, database service, queues. — ML L16 — [Amine decision]
- Build on existing open-source tools rather than compete or rebuild. — ML L47 — [Amine decision]
- Same tested Nightshift release everywhere; Nightshift tunes only within limits Orvex sets; bigger changes are proposals. — S1 § Important points #5 — [Danny]
- "Same tested release" means the same Nightshift everywhere, not identical clusters (hardware, capacity, workloads differ). — ML L49 — [Amine decision]
- Prototype: small prototype on this VM, after PRD and architecture; needn't cover everything. — ML L83 — [Amine decision]
- Deliverable is a design (PRD + architecture) defended in a 15-minute walkthrough. — S1 § Important points #2; ML L7 — [Danny]

## 7. Users, notification channels, explanations

- Who This Serves (final): primary = Orvex Nightshift team (Orvex can't succeed without Nightshift); secondary = customer's business owner; then Orvex support. — ML L116 — [Amine decision]
- Customer-side reader is the shop owner or senior staff, not the app's developer (kept despite AI push); the shop owner is Amine's example, not from Danny. — ML L29, L32, L49 — [Amine decision]
- Nightshift team (engineers) watches over Nightshift itself; a separate support team handles customer incidents. — ADD § Alert and approval routing (Amine's update); ML L31 — [Amine decision]
- Nightshift explains to Orvex too, not only to the owner. — ML L54 — [Amine decision]
- Owner alerted as soon as something unusual is detected, with possible fixes; example message about checkout memory (adapted to ask approval for a fix, not for investigating). — ML L37, L46 — [Amine decision]
- Nightshift alerts Orvex support depending on contract and always tells the customer (full view of their app). — ML L36 — [Amine decision]
- Phone call only for critical: checkout failing, or strong evidence something important (checkout, a database) is about to fail. — ML L41; ADD § Moved from the brief (Notification detail) — [Amine decision]
- Alert only when a problem becomes risky. — ML L41 — [Amine decision]
- Dashboard and morning summary for the rest: metrics, recurring patterns (e.g. a 3am traffic peak needing more resources), permitted repairs that succeeded. — ML L41; ADD § Notification detail — [Amine decision]
- Customer may have a live view of their app's health; every problem needing a person first appears on a Nightshift monitoring page. — ML L27; ADD § Alert and approval routing — [Amine decision]
- Morning summary: problems, fixes, anything unusual; Nightshift and app activity overnight; for risky problems the full timeline from the first thing noticed. — ML L28, L39; ADD § Notification detail — [Amine decision]
- Routing proposal (Amine's first proposal, "still under discussion"): full approval → support, platform team, customer; no permission → customer and platform team, then support; mixed → allowed action to support, not allowed → customer notification and alert. — ADD § Alert and approval routing — [open question]
- Whether the platform team should get customer incidents at all. — ADD § Alert and approval routing (Open points) — [open question]
- Approvals arrive via Slack/portal. — ML L12 — [Danny]

## 8. Multi-cluster, fleet learning, OMK vs EKS, hardware

- Clusters are single-customer; a customer may run one control-plane cluster plus several worker clusters. — ML L12 — [Danny]
- Ground Rule: "A cluster belongs to one customer; a customer may have several clusters (Danny)". — ML L109 — [Amine decision]
- What the multi-cluster control-plane cluster runs, and whether to treat a customer's clusters as one unit (emailed to Danny 2026-10-28). — ML L91; ADD § Other open questions — [open question]
- Whose bare metal / how the infrastructure is organised (emailed to Danny). — ML L91; ADD § Other open questions — [open question] **ANSWERED: danny-qa Exchange 4.**
- Bare metal and infrastructure (incl. EKS) are Orvex's responsibility (Amine's reading of Danny's email). — ML L69 — [assumption] **SUPERSEDED 2026-10-28 by danny-qa Exchange 4: customers are responsible for their own hardware; OMK manages OS and Kubernetes.**
- Differentiation: not better at any single problem; designed for Quornex (tested repairs reused across the fleet, fleet learning), privacy by design, combines existing tools. — ML L50 — [Amine decision]
- Uniqueness unproven; Codex corrected: HolmesGPT not diagnosis-only, AWS DevOps Agent claims multicloud/on-prem, Datadog has private runners. — ML L96 — [Codex-checked]
- One tool for bare metal (incl. hardware) and EKS (merged into "Built for one platform"). — ML L53; REV S6 — [Amine decision]
- Claude coaching feedback, fleet learning pipeline: sanitised evidence → person diagnoses → rule + fix → replay test → shadow run across fleet → gradual rollout with rollback → signed, versioned, in tested release. — S2 § Gaps #7 — [unverified claim]
- Hardware: assume cheap, unreliable, possibly poorly maintained bare metal. — ADD § Cost and model inputs from Danny; ML L66 — [Danny]
- Hardware failures are a central case, not an edge case: disks, network cards, memory, links. — ADD § For the failure catalogue; ML L73 — [Amine decision]
- On EKS, Nightshift watches what AWS and the chosen node setup expose. — ADD § For the failure catalogue; ML L88 — [Amine decision]
- Hardware is watched on OMK, not EKS (prose fix P4 accepted). — REV § Prose P4 + Amine's decisions — [Amine decision]
- Claude coaching feedback: on bare metal report hardware faults, on EKS replace the node; AWS runs the EKS control plane; architecture per node (collector DaemonSet), per cluster (brain, executor, approval queue, record), central (fleet learning, approvals, signed rule releases, silent-cluster watch); GPU model once per cluster. — S2 § Gaps #3 — [unverified claim]
- `NETDEV WATCHDOG ... transmit queue timed out` as a sign of a hung network card; classics: memory creep, expired certificates, network links. — S2 § Claims still to verify; § Gaps #2 — [unverified claim]

## 9. Cost, GPU and model options

- Rely heavily on hosted AI for at least 3 years; minimise inference and token costs. — ADD § Cost and model inputs from Danny; ML L66 — [Danny]
- Rules, monitoring and automation first; AI calls only where needed. — ADD § Cost and model inputs from Danny — [Danny]
- GPU options to evaluate: ~$1,000 consumer GPU 24 GB, ~$10,000 GPU 96 GB, and GPU sharing across clusters (check against privacy; within one customer's clusters a possible middle ground). — ADD § Cost and model inputs from Danny — [Danny]
- Target: lowest realistic cost at near public-cloud reliability, at 100 and 10,000 clusters; no fixed budget; Orvex must make money. — ADD § Cost and model inputs from Danny; ML L66 — [Danny]
- $1 less per cluster saves about $10,000 a month at 10,000 clusters. — ADD § Amine's cost and GPU thinking; ML L102 (typo fix of L71) — [estimate]
- Use open-source tools; compare hosted vs in-cluster GPU including GPU cost; cheaper options must not mean slower responses or less capacity. — ADD § Amine's cost and GPU thinking; ML L71 — [Amine decision]
- GPU sharing only among one customer's dedicated clusters; logs stay inside; Nightshift filters what may go out, with confirmation. — ADD § Amine's cost and GPU thinking; ML L72 — [Amine decision]
- Does sharing across one customer's clusters satisfy the brief's "only an in-cluster GPU keeps private data in" rule? To settle in architecture, possibly with Danny. — ADD § Amine's cost and GPU thinking; ML L72 — [open question]
- $1,000 and $10,000 are Danny's hypotheticals; 96 GB cards listed ~$14,080-16,000 (out of stock); a $1,000 24 GB card is not verified. — ADD § Codex's check (GPUs); ADD § To test — [Codex-checked]
- Qwen3-32B 4-bit ≈ 19.1 GB at tiny input, ≈ 27.7 GB at 30,720-token input; RTX 3090 = 24 GB, RTX PRO 6000 Blackwell = 96 GB. GPU fitting is not usefulness. — ADD § Codex's check (GPUs); ML L93 — [Codex-checked]
- GPU purchase only over 36 months: $1,000 = $27.78/month dedicated or $2.78/cluster shared by 10; $10,000 = $277.78 or $27.78 shared by 10; excludes host server, power, cooling, maintenance, spare capacity, operating effort. — ADD § Codex's check — [Codex-checked]
- Hosted example at illustrative $2/M input, $10/M output (rates Codex attributes to Claude Sonnet 5): $0.04 per 10k+2k call; 10 calls/incident × 250 incidents/night ≈ $3,000/month fleet, ≈ $0.30/cluster; one extra such call per cluster per day ≈ +$1.20/cluster/month. — ADD § Codex's check — [Codex-checked]
- Main cost driver = how often Nightshift calls AI and how much context it sends; GPU sharing savings vs hosted not established. — ADD § Codex's check; ML L93 — [Codex-checked]
- Claude coaching feedback on cost: split fixed (team, central system) from variable (GPU, tokens, storage, network, human time per incident); GPU cost per cluster roughly flat because each cluster needs its own GPU; tokens = calls × tokens per call × price; sensitivity analysis; compare with human DevOps, cluster, outage cost and monitoring per-server prices. — S2 § Gaps #8 — [unverified claim]
- AWS `g4dn.xlarge` (T4) ≈ $0.50/hour ≈ $380/month; Datadog-style per-server prices as a reference. — S2 § Claims still to verify — [unverified claim]
- Is an in-cluster GPU optional per cluster? — S1 § Questions for Danny Q3 — [open question]
- Two model options: a hosted model, and a model on a GPU in the cluster (wording fix P3). — REV § Prose P3 — [Amine decision]

## 10. Anything else a PRD would need

- Main problem (Amine's words): Orvex wants to be the managed-cloud provider for many companies at 10,000 clusters without a large ops team per cluster; a cheap public-cloud-like experience with monitoring, healing and alerting, using AI and trusted open-source tools. — ML L77 — [Amine decision]
- For the customer, Quornex is "a cheap public cloud" (AI's sovereign/private-cloud framing removed). — ML L79 — [Amine decision]
- Danny's vision: sovereign cloud for a million companies at low cost; private cloud today complex, expensive, needs specialists; Quornex a complex mix of open-source parts. — ML L66 — [Danny]
- Vision kept (ultimate DevOps platform that runs, monitors and heals the cloud); hosted-AI outlook stays in Vision (REV S5 rejected). — ML L80; REV § Amine's decisions — [Amine decision]
- Failure condition: if Orvex needs as many DevOps engineers as customers would have had, Nightshift has failed. — ML L16 — [Amine decision]
- How failures are handled today, and what monitoring, alerting and night cover Orvex has, is unknown. — ML L17, L25; ADD § Other open questions; S1 § Questions for Danny Q1 — [open question]
- Timeline 2-3 weeks per Amine, dates unconfirmed; exact hand-in date unknown. — ML L9; ADD § Other open questions; S2 § New questions Q7 — [open question]
- Claims in `research-landscape.md` (release dates, some vendor claims) are unchecked. — ADD § To test; ML L11 — [unverified claim]
- Honest-thinking habit: label every claim "brief says / I assume / verified (source, date)". — S2 § Gaps #9 — [unverified claim] (coaching guidance)
- Use one set of fix-authorisation terms everywhere (review found permitted repair / fix agreed in advance / pre-authorise / pre-approved / last-resort used loosely). — REV § Structure S10 — [Amine decision]
- Introduce Danny's role once; expand OMK; "Quornex, Orvex's cloud platform"; name files rather than "the addendum". — REV § Prose P5-P7 (accepted) — [Amine decision]
- Style: British spelling, no serial comma. — REV § Amine's decisions; ML L111 — [Amine decision]
- Record every decision, correction and overrule immediately (AI_LOG.md / memlog). — ML L26 — [Amine decision]
- Length: 1-2 page target was the BMAD skill's guideline, not Danny's; trimmed brief kept, detail in addendum.md. — ML L108, L110 — [Amine decision]

## Conflicts and reversals

1. **Primary user** — S1 / ML L6: Orvex ops team primary → ML L34 (2026-10-27): customer's business owner primary → ML L116 (final): Orvex Nightshift team primary, owner secondary, then support.
2. **Fix tiers** — REV S10 / ML L111: three tiers permitted / approved / last-resort → ML L115 / ADD "Superseded": last resort is an execution condition, not a tier; authorisation = permitted/approved only. (Brief rewritten to the latter.)
3. **Ratings-to-tiers mapping** — ML L112: "mapping of ratings to fix tiers left for the PRD" vs ADD § Repair catalogue "Superseded" / ML L115: no mapping, risk and authorisation separate. Open remainder: define "dangerous" and whether it can ever be permitted in advance.
4. **Who approves last-resort / pre-approved fixes** — ML L44 and ADD § Customer settings: the customer agrees in advance → ML L89: both customer and Orvex must approve; Nightshift never changes anything on its own.
5. **Which fixes get extra Orvex review** — ML L55: "some risky fixes" need Orvex approval after the customer's → ML L119: Orvex reviews "dangerous cases" after the customer approves. Rating word shifts from risky to dangerous; not reconciled.
6. **Deleting/changing customer data** — ML L81: "changing customer data without approval" excluded → ML L85: never allowed, even with approval ("with approval" meant code fixes only).
7. **Firm rule vs auto repairs** — S1 #3: human approval before any change to customer production vs Danny (ML L12) auto high-confidence repairs and ML L45 "apply a permitted repair if one exists"; reconciled in brief via advance approval (ML L89), but "high-confidence" owner is open (ADD).
8. **No-response instinct** — S2 Round 5: Amine's early "silence = act anyway" flagged as breaking the firm rule → ML L38 / L115: silence is not approval; no extra permissions from an unanswered request.
9. **Customer-code changes** — ML L33: pending Danny, unconfirmed scope → ML L40: Danny puts it in day-1 scope as an experiment. ML L84 asked how AI-generated code fixes fit "no improvised repairs" → ML L86: generated, tested, Orvex-engineer-approved, never applied alone. ADD first proposal ("if the customer approves, fixing it becomes Orvex's job") predates the Orvex-engineer approval step.
10. **Staffing** — ML L21: 10-15 engineers (approvals, checks) → ML L31: those 10-15 watch Nightshift itself, separate support team → ML L16: ~5 engineers target guess → ML L60: AI's 700-1,000/engineer corrected to ~500 → ML L95/L99: 350-400 per engineer (range to test).
11. **Incident volume** — ML L15: 100+ incidents a night (guess) → ML L94: 250 a night, up to 500 on a bad night (to validate).
12. **Alert routing** — ADD first proposal routes some cases to the platform team first → ADD Amine's update: platform team not paged for every customer incident (support handles them); still under discussion.
13. **GPU per cluster vs GPU sharing** — S2 Gaps #3/#8 (Claude feedback): GPU model runs once per cluster, cost flat because each cluster needs its own GPU; S2 Round 6 flags "shared GPU breaking privacy" → Danny (ADD) asks to evaluate sharing; Amine (ML L72) shares within one customer's clusters; fit with in-cluster privacy rule open.
14. **Cost target** — ML L62: target to be set with Danny → ML L67: "as low as realistically possible at near public-cloud reliability".
15. **Cluster/customer Ground Rule** — ML L106: not added → ML L109: added after clarification.
16. **Customer framing** — AI's "private/sovereign cloud with a public-cloud experience" removed (ML L79); Danny's own vision uses "sovereign cloud" (ML L66).
17. **Shared-inference note source** — ML L75: "source not stated" → ML L76: Codex.
18. **Cost typo** — ML L71 lost dollar amounts → ML L102: "$1 less per cluster saves about $10,000 a month at 10,000 clusters".
