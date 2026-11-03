# Nightshift: Requirements Checklist

Source: `brief.pdf` (Orvex AI Intern design brief, 2 pages). Extracted 2026-10-25.
Status: DRAFT from session 1. Not yet reviewed by Danny.

## Challenge in plain English

Orvex AI sells Quornex, a managed developer cloud (databases, queues, storage, deployment). They plan about 10,000 Kubernetes clusters, on bare metal with Orvex Managed Kubernetes (OMK) or on hosted Kubernetes such as EKS. Nightshift is an ops agent inside every cluster: it watches logs and metrics, spots trouble early, fixes safe problems itself and asks a human about risky ones.

The task is a **design** (PRD plus architecture), made with BMAD and Claude, defended in a 15-minute walkthrough followed by questions. Prototypes are optional. The brief says nobody has solved this yet, so honest reasoning matters more than perfect answers.

## Deliverables (GitHub repo)

- [ ] PRD, produced with BMAD
- [ ] Architecture, with diagrams
- [ ] Privacy and security review
- [ ] Failure catalogue (the 20 most important failures)
- [ ] Cost model (per cluster per month, at 100 and 10,000 clusters, with a GPU in the cluster and with a hosted model)
- [ ] `AI_LOG.md`: how Claude and BMAD were used, plus 3-5 times the AI was overruled
- [ ] README ending with open questions
- [ ] 15-minute walkthrough, then questions

## Prescribed workflow

1. Set up: `npx bmad-method install` (done)
2. Frame: `bmad-product-brief`
3. Specify: `bmad-prd`, then validate the PRD
4. Design: `bmad-architecture`
5. Challenge: `bmad-review` (adversarial lens), then fix what it finds

## Capabilities Nightshift must have

(The PDF's numbering is ambiguous in text extraction, so none is used here.)

- [ ] Watch the whole stack: hardware, Kubernetes, and Quornex's own services
- [ ] Explain itself plainly: what is wrong, why it matters, what it did
- [ ] Protect customer data: logs stay in the cluster, and a hosted model sees only what it must
- [ ] Learn across the fleet: a new problem in one cluster prepares all the others
- [ ] Cost what it is worth: cost per cluster known and sensible
- [ ] See trouble coming (slow build-ups such as disk filling or memory creep)
- [ ] Fix what is safe: well-understood repairs, verify each, undo if it failed
- [ ] Ask before anything risky, and before ANY change to customer production (firm requirement)

## Ground rules

- [ ] One tool covers OMK bare metal (including hardware) and EKS
- [ ] Two model modes: a GPU model inside the cluster (keeps private data in), or a trusted hosted model with limited visibility
- [ ] Every cluster runs the same tested release; Nightshift tunes only within limits Orvex sets; anything bigger is a proposal to Orvex
- [ ] Nothing done in secret: all reads and changes recorded where the customer can see them; least-privilege rights

## Questions the documents must answer

- [ ] **Technology:** open-source projects to collect, store, detect and act with; what was rejected and why
- [ ] **Architecture:** per node, per cluster, central at Orvex; bare metal vs EKS differences; what happens if Nightshift fails
- [ ] **Failures:** top 20 (hung NICs, full memory, disks, links...); for each: predict, fix, or only report
- [ ] **Intelligence:** rules and statistics vs LLM; operation with and without an in-cluster GPU
- [ ] **Privacy:** limit and strip private data before a hosted model; prove it to a customer
- [ ] **Security:** crafted log lines (untrusted text) and a compromised agent with powerful rights
- [ ] **Safety:** repairs that do not make things worse; no two fixes fighting; when to stop and call a person
- [ ] **Cost:** per cluster per month at 100 and 10,000 clusters, GPU vs hosted; what moves it most

## Evaluation criteria

- [ ] Technology choices: sound, alternatives weighed
- [ ] Architecture: one clear design for bare metal and EKS
- [ ] Privacy and security: customer data protected, agent locked down
- [ ] Cost: credible numbers for a paid service
- [ ] AI fluency: Amine steers the AI and checks its work
- [ ] Honest thinking: clear about what is known and what to test next

## Small print

- Fee: $100 on completion
- Orvex AI owns the IP; may be published under Apache 2.0 with "Copyright 2026 Orvex AI"
- No secrets or private Orvex data in the repo
- Questions to Danny (Orvex AI); early questions welcome

## Confirmed vs assumed vs unclear

**Confirmed:** everything listed above is stated in the brief. The only platform facts known are the names OMK, EKS, Quornex and Nightshift. No Quornex internals have been assumed.

**Assumptions (unconfirmed):**
- A1. "Human approval" means a person at Orvex, the customer, or both (brief does not say). **Answered by Danny: the customer chooses alert-only or automatic high-confidence repairs, can tick which actions run automatically, and can delegate approval to Orvex support. See `danny-qa.md`.**
- A2. Fleet learning shares anonymised patterns or runbooks, not raw logs (inferred from the privacy rule).
- A3. No UI is required, so `bmad-ux` is probably skippable. **Overridden by Amine (2026-10-28): include `bmad-ux` after the PRD (check timing with `bmad-help`), with simple wireframes for the dashboard, incident explanations, approval flow and action history. No interface implementation.**

**Ambiguities:**
- U1. "Hardware" on bare metal is undefined (BMC/IPMI, SMART, NICs, GPUs?). **Partly answered by Danny (Exchange 4): customers are responsible for their own hardware; OMK manages the OS and Kubernetes; Nightshift must detect disk, NIC and power-supply failures, L2/L3 networking problems, misconfigurations and Kubernetes issues. See `danny-qa.md`.**
- U2. Who "the customer" is (a company using Quornex, or tenants within it). **Answered by Danny: a cluster is not shared; one customer may have several clusters (one control-plane cluster plus worker clusters). See `danny-qa.md`.**
- U3. What "customer's production" means inside a managed service.
- U4. Whether customer visibility of Nightshift's record must be live or on request.
- U5. What counts as a "trusted" hosted model and as "private data".

**Questions for Danny (not yet sent):**
1. What do Quornex clusters run today, and what monitoring or alerting already exists?
2. Is the approver Orvex staff, the customer, or configurable? **(Answered, see `danny-qa-summary.md`)**
3. Which hosted models and regions count as trusted? Is an in-cluster GPU optional per cluster?
4. Is there a target price or margin per cluster for the cost model? **(Answered: no fixed budget; find the realistic minimum at near public-cloud reliability, at 100 and 10,000 clusters, and explore 24 GB and 96 GB GPUs and GPU sharing. See `danny-qa.md` Exchange 3.)**

## Next step

`bmad-product-brief` (menu code CB), run in a fresh context.
