# Questions to Danny and his answers (summary)

A paraphrased record of what Danny (Orvex AI) has confirmed in his replies. The correspondence itself is kept private, outside this repository; only this summary is published (Amine, 2026-11-03). Anything we interpret is marked as interpretation. Danny presented his answers as his current thinking, open to discussion, not as final requirements.

## Exchange 1: approval authority and cluster sharing

Reply received by 2026-10-27.

**Who approves changes affecting customer production?**
- The customer chooses the mode: alert-only, or Nightshift handling high-confidence repairs.
- A possible design is a list of available repairs, in which the customer ticks the ones Nightshift may run automatically.
- Nightshift can ask for permission to act through Slack and the portal.
- The customer can choose to let Orvex support answer those requests.

*Our interpretation (not confirmed):* the customer is the default approver for changes to their production, and Orvex support approves only if the customer delegates to them.

**Does a cluster serve one customer or several?**
- A cluster belongs to one customer and is not shared.
- A customer can have a multi-cluster deployment: one control cluster and several workload clusters running the customer's applications.

## Exchange 2: fixing bugs in customer code

Reply received by 2026-10-27.

- Code fixes go in the initial scope, as an experiment: not every first-version feature has to stay in the basic product. Orvex wants to see how it works in real use and wants feedback on everything.
- *Our interpretation:* code repair is an experimental first-version feature. Pricing was not addressed, so "an optional paid capability" remains Amine's proposal.

## Exchange 3: cost, and why Nightshift matters

Reply received by 2026-10-28.

- **Vision:** make private cloud cheap, reliable and easy enough to compete with public cloud, so that many companies can run their own cloud with control over their data and compute. Today private cloud is costly and hard to operate, and Quornex has many open-source parts that can go wrong. AI is what makes this realistic now.
- **Business:** Orvex has to make money doing it; a cheap cloud is pointless if it is expensive to maintain.
- **Cost:** no fixed budget. Find the lowest realistic cost at close to public-cloud reliability, modelled at 100 and 10,000 clusters. Small savings per cluster matter at scale.
- **AI:** Danny expects to rely heavily on hosted AI for at least the next three years. Keep inference and token costs low, and don't use AI where rules, monitoring and automation are enough.
- **GPUs:** explore whether a consumer GPU (about $1,000, 24 GB) or a larger one (about $10,000, 96 GB) is enough, and whether GPUs can be shared across clusters.

*Our interpretation:* cheap, unreliable hardware makes hardware failures a central case. Sharing a GPU across clusters moves data outside each cluster; this was explored in the PRD (PRIV-8: a shared GPU counts as external AI).

## Exchange 4: bare metal, approvals, multi-cluster

Reply received by 2026-10-28.

- **Hardware:** customers are responsible for their own hardware. Orvex provides OMK (Orvex Managed Kubernetes), which manages the operating system and Kubernetes, with Quornex on top. For launch, Orvex will likely use a hosting provider (generalised in this repository).
- **Scope:** Nightshift keeps the whole stack healthy, including OMK and Quornex. It must detect disk, network-card and power-supply failures, network problems at layers 2 and 3, misconfigurations and Kubernetes issues. Customers may have little infrastructure expertise and badly configured hardware. Installation and validation happen before Nightshift takes over.
- **Approvals:** safe repairs should be automatic; risky changes need approval.
- **Hosted Kubernetes (EKS):** the provider stays responsible for Kubernetes and the infrastructure.
- **Multi-cluster:** Quornex Fleet is Orvex's central, multi-tenant control plane. A customer may also run a control cluster managing several workload clusters, with a Nightshift management agent on it. Each cluster must still be able to look after itself.
- **Aim:** as close to self-managing as possible, on unreliable hardware, at very low cost.

*Our interpretation (not confirmed):* Nightshift detects hardware faults but can't repair them physically; whether "automatic" still means "if the customer allows it" was unclear; who approves risky platform changes was not yet stated.

**Decisions Amine took (2026-10-28):** customers are responsible for their hardware; Quornex Fleet, the customer's control cluster and the workload clusters are distinct terms; every workload cluster's agent keeps working locally if the management agent is unavailable; detecting a hardware fault doesn't mean repairing it physically; coordination doesn't let private data leave its cluster.

## Exchange 5: approval model, privacy boundary, reliability

Questions sent around 2026-10-30; reply received 2026-11-02.

- **The model:** it broadly fits. The two catalogues make sense, but the incident history should be kept and linked to the validated repair. Not every repair needs both customer and Orvex approval.
- **Platform changes:** Orvex operates OMK and Quornex, so routine, tested repairs should run automatically. Risky platform changes need an authorised Orvex engineer; changes affecting customer production also need the customer's approval. Dangerous repairs stay manual at first.
- **Privacy:** the proposed boundary is a good starting point. External inference is allowed with the customer's consent and zero data retention, or a local model if nothing may leave. AI redaction alone must not be assumed to make data safe to share.
- **Reliability:** 99.9% is a working target, not a promise; what is achievable depends on the customer's hardware and on whether the installation is highly available.
- **For the challenge:** keep it practical and explain assumptions and trade-offs; Orvex is interested in the reasoning, not a finished production design.

*Our interpretation (not confirmed):* approval depends on what a repair changes as well as on its risk; an advance tick may still count as the customer's approval; "manual" means a person performs the repair; external inference needs consent for every use, not only code.

**Decisions Amine took (2026-11-02):** dangerous repairs are manual in version 1; approval depends on what a repair changes; an advance tick covers only its specific tested action and conditions; external AI needs explicit consent, nothing preselected, with source code a separate permission; hosted AI is the focus, with an in-cluster model or rules and templates when there is no consent.

## Follow-ups

- Answered: who approves platform changes (Exchange 5), the privacy boundary (Exchange 5, as a starting point), whether the extra Orvex approval fits (Exchange 5), reliability as a number (Exchange 5), code fixes (Exchange 2), cost (Exchange 3), whose hardware it is (Exchange 4). Hand-in: between 10 and 14 November 2026 (Amine, 2026-10-30).
- **Never sent, still open:** who decides what counts as a "high-confidence" repair; what happens when an approval request gets no answer at night; what monitoring and night cover Orvex has today (PRD Section 10, items 5, 19 and 20). Risky repairs to the customer's own app keep both approvals, as our conservative interpretation of Danny's approval model (FR-21); this is decided and not asked again.
