# Addendum: Product Brief, Nightshift

Detail Amine contributed that is too deep for the brief but useful for the PRD or architecture.

## Alert and approval routing (Amine's first proposal, 2026-10-27; still under discussion)

- Every problem that needs a person first appears on a Nightshift monitoring page. The customer can have a live view of their app's health if they want one.
- Routing depends on what the customer has allowed:
  - **Full approval granted:** alert Orvex support first, then the platform team, then the customer.
  - **No permission granted:** alert the customer and the platform team directly, then support.
  - **Mixed (some actions allowed):** if the action is allowed, it goes to support; if not, it goes to the customer as a notification and alert.
- A good morning for the primary user: a summary of the night (problems, fixes, anything unusual).
- If the customer allows Nightshift to read their code, Nightshift explains a code problem in plain words and how it would be fixed safely, without touching customer data.

Amine's update (later on 2026-10-27):
- The 10-15 engineers watch over Nightshift itself. A separate **support team** handles customer incidents, so the Nightshift/platform team is not paged for every customer incident.
- **Code fixes as a service (pending Danny):** if a bug in the customer's code can be fixed safely, Nightshift explains it in plain words. If the customer approves, fixing it becomes Orvex's job, priced by contract according to cost (tokens) or difficulty. This applies only if the customer has allowed Nightshift to read and change their code.

Open points raised in coaching: separating "what Nightshift may read" from "what it may fix" and "who approves"; whether the platform team should get customer incidents at all; whether Nightshift ever changes customer code.

## Cost and model inputs from Danny (2026-10-28), for the architecture and cost model

- Expect to rely heavily on hosted AI for at least 3 years; minimise inference and token costs with every available technique.
- Rules, monitoring and automation first; AI calls only where they are needed.
- GPU options to evaluate: ~$1,000 consumer GPU with 24 GB VRAM, ~$10,000 GPU with 96 GB, and GPU sharing across clusters (check against the privacy rule; sharing within one customer's clusters is a possible middle ground).
- Target: lowest realistic cost at near public-cloud reliability, at 100 and 10,000 clusters. No fixed budget.
- Hardware: assume cheap, unreliable and possibly poorly maintained bare metal. *(Corrected 2026-10-28, danny-qa Exchange 4: the customer is responsible for this hardware, and it may be badly configured; OMK manages the OS and Kubernetes.)*

## Amine's cost and GPU thinking (2026-10-28)

- Aim for the lowest possible cost: $1 less per cluster saves about $10,000 a month at 10,000 clusters.
- Use open-source tools. Compare hosted models with in-cluster GPU models, including the GPU's cost.
- Cheaper options must stay reliable: no slower responses and no loss of capacity.
- GPU sharing: share one GPU among several dedicated clusters **of the same customer**. Logs and anything about the customer stay inside; Nightshift filters what may go out, with confirmation. *Open point: the data then leaves the individual cluster but stays within the customer's clusters. Does that satisfy the brief's rule that only an in-cluster GPU keeps private data in? To settle in the architecture, and possibly with Danny.*

## Privacy approach for shared inference (from Codex, the AI assistant integrated on Amine's machine, which Amine used for a second opinion; pasted 2026-10-28)

- Controlling what leaves the cluster can make shared inference a reasonable, cheaper option, but it doesn't prove 100% safety. The savings are a reason to *evaluate* it, not evidence that the filtering always works.
- Removing recognisable secrets isn't enough. Example: `Database error: acquisition_of_company_X payment table unavailable` contains no email or password, yet reveals confidential business information.
- Stronger approach: Nightshift **builds a small message from approved fields only**, for example:
  ```
  Service: <service1>
  Error category: database connection timeout
  Failure rate: 30%
  Duration: 5 minutes
  ```
- Still required: test the filtering, block unapproved fields, and keep sensitive cases local when they can't be safely summarised.
- Defensible claim for the brief: *"We will evaluate shared inference to reduce cost. Only approved, sanitised diagnostic information may leave each cluster; raw logs and secrets remain inside. We will test the remaining privacy risks."*
- The design doesn't need to prove zero risk. It needs evidence that it meets the privacy requirement, and measurements of how much it actually saves.

## Codex's check of estimates, GPUs and cost (2026-10-28; figures as reported by Codex, not re-checked by Claude)

- **Incidents:** 250 a night across 10,000 clusters is one incident per cluster every 40 nights. Define an incident (one failure with many alerts = one incident). Separate incidents Nightshift resolves alone from outages needing a person. Plan for peaks such as a bad release affecting hundreds of clusters at once.
- **Staffing:** 500, 400 and 350 clusters per engineer mean 20, 25 and 29 engineers for 10,000 clusters (headcount, not people per shift). Two scenarios, both at 250 incidents a night: 90% resolved automatically, at 20 minutes each, is about 8.3 human hours a night; 60% resolved automatically, at 45 minutes each, is about 75 hours. Estimate the Nightshift team and support separately.
- **GPUs:** Qwen's benchmark reports about 19.1 GB for Qwen3-32B in 4-bit with a tiny input and about 27.7 GB at a 30,720-token input, so a model can fit 24 GB with short inputs and exceed it with long ones. NVIDIA lists the RTX 3090 at 24 GB and the RTX PRO 6000 Blackwell at 96 GB. 96 GB cards are listed at about $14,080-16,000 (out of stock). A $1,000 24 GB card is not verified.
- **GPU cost spread over 36 months (purchase only):** $1,000 = $27.78/month dedicated, or $2.78 per cluster if shared by 10; $10,000 = $277.78/month dedicated, or $27.78 if shared by 10. Excludes the host server, power, cooling, maintenance, spare capacity and operating effort.
- **Hosted example:** at an illustrative $2 per million input and $10 per million output tokens (rates Codex attributes to Claude Sonnet 5), one call of 10,000 input + 2,000 output tokens costs $0.04. Ten calls per incident at 250 incidents a night comes to about $3,000 a month fleet-wide, or about $0.30 per cluster. One extra call of that size per cluster per day adds about $1.20 per cluster per month.
- **Main cost driver:** how often Nightshift calls AI and how much context it sends. GPU sharing is worth evaluating, but savings against hosted inference are not established.
- **Filtering test plan:** seed fake emails, passwords, keys and confidential business details. Inspect real outbound requests. Check that unapproved fields and unexpected formats are blocked. Test for bypass paths around the gateway. Check that diagnosis still works on the sanitised data. Presidio's own docs say automated detection can't guarantee finding everything.
- **Success targets** are proposed acceptance targets, not observed performance. At 250 repairs a night, 95% success still leaves about 12.5 unsuccessful attempts a night. "Unsuccessful but harmless" and "caused damage" need separate measures.

## For the failure catalogue (2026-10-28)

- Because Quornex runs on cheap, unreliable and possibly poorly maintained bare metal, **hardware failures are a central case, not an edge case** (Amine confirmed): disks, network cards, memory, links. On EKS, Nightshift watches what AWS and the chosen node setup expose.

## Moved from the brief when it was trimmed (2026-10-28)

**Customer settings (detail):** in their cluster settings, the customer decides what Nightshift may read (the infrastructure only, or also their app and its code), which fixes it may run without asking, who approves everything else (the owner, or Orvex support if delegated), and which pre-agreed fixes it may use as a last resort.

**Code fixes (detail):** Nightshift generates the fix, it is tested, and an Orvex engineer must approve it after testing before deployment. Nightshift never applies a code fix on its own, and a code fix never touches databases, backups or customer data. Pricing by usage or complexity is Amine's proposal; Danny hasn't addressed it.

**Notification detail:** phone calls are for checkout failing, or strong evidence that something important (checkout, a database) is about to fail. The dashboard and morning summary hold metrics, recurring patterns (such as a 3am traffic peak that needs more resources) and permitted repairs that succeeded. The morning summary also records what Nightshift did overnight.

**How each success signal is measured:**
- Early detection: at first in controlled tests, comparing alert times with the records of deliberately injected failures and with application health checks.
- Successful repairs and repairs that caused damage: action logs and traces of each repair, health checks before and after, incident reviews.
- Useful alerts: operators label each alert "actionable", "duplicate" or "false alarm".
- Clusters per engineer: measure human handling on the first 100 clusters, then extrapolate. The engineer mainly approves or denies requests, monitors and guides Nightshift. Estimate the Nightshift-team and support workloads separately.
- Availability: measurement method to be defined.
- Unapproved changes: compare execution audit records against approval records and policy decisions.
- Cost: model and then measure at 100 and 10,000 clusters, with hosted AI and with an in-cluster GPU, including GPU, monitoring, storage, model usage and shared infrastructure.

**Other open questions for Danny (not in the brief):** who decides what counts as a "high-confidence" repair; what monitoring, alerting and night cover Orvex has today; which hosted models and regions count as "trusted"; the exact hand-in date. (Questions about whose bare metal it is, approvals for platform components, and multi-cluster deployments were emailed to Danny on 2026-10-28. *Answered after finalisation in danny-qa Exchange 4: the bare-metal question fully, the other two in part.*)

**To test (detail):**
- An "incident" is one failure, however many alerts it fires. Plan for fleet-wide events too, such as a bad release hitting hundreds of clusters at once.
- Compare local and hosted models on the same incident cases: diagnosis accuracy, unsupported claims, tool-call correctness, response time, simultaneous incidents. The $1,000 and $10,000 GPU prices are Danny's hypotheticals; Codex found 96 GB cards listed at about $14,000-16,000.
- For filtering, the honest result is "no seeded secrets escaped in these tests", with the test scope stated, not proof of 100% privacy.
- The remaining claims in `research-landscape.md` (release dates, some vendor claims) are unchecked.

## Repair catalogue ratings (Amine, 2026-10-28)

- Every repair in the catalogue is rated **safe**, **risky** or **dangerous** and handled accordingly. When Nightshift meets something new and it gets solved, the fix is added to the catalogue (and tested before release).
- **Superseded (same day):** risk and authorisation are separate questions, so there is no mapping from ratings to "kinds of fix". Last resort is an execution condition on a fix permitted in advance, not a third kind of fix. An unanswered request or a predicted failure within 30 minutes never grants extra permissions. Prohibited actions can never become permitted through advance approval. The 30-minute threshold is a proposal to validate.
- **For the PRD:** define "dangerous" clearly, and decide whether a dangerous repair can ever be permitted in advance or always needs approval at the time.
- The 30-minute last-resort window is Amine's idea.
