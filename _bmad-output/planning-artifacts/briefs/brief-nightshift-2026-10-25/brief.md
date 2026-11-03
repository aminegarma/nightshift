---
title: "Product Brief: Nightshift"
status: final
created: 2026-10-25
updated: 2026-10-28
---

# Product Brief: Nightshift

*Context: this brief is part of the Orvex AI intern design challenge. The challenge delivers a design (PRD, architecture, privacy and security review, failure catalogue, cost model), plus a small prototype on a test VM showing one part of Nightshift. Deeper detail behind this brief is in `addendum.md`.*

## Summary

Orvex wants to provide managed cloud to many companies across 10,000 clusters, on cheap and unreliable bare metal as well as on EKS, without needing a large operations team for every cluster. Nightshift is the operations agent inside every cluster of Quornex, Orvex's cloud platform, and it is what makes this possible. It predicts failures before customers feel them, explains them in plain words, and handles well-understood repairs from a tested catalogue, but only with the approvals the customer and Orvex have given. Customer data stays protected throughout.

Nightshift builds on proven open-source tools, uses AI only where rules and automation can't do the job, and aims for the lowest realistic cost per cluster at close to public-cloud reliability. For the customer, Quornex should feel like a cheap public cloud. For Orvex, it should be a cloud it can run profitably at scale.

## The Problem

**For the customer,** Quornex should be a cheap public cloud. Today, private cloud is a poor alternative to public cloud: it is complicated and expensive to maintain, it needs specialist engineers, and the experience is much worse (Danny, Orvex AI).

**For Orvex,** Quornex is itself "a complex mess of open-source components with a million things that can go wrong" (Danny), running on cheap, unreliable and possibly poorly maintained bare metal. The fleet sees about 250 distinct incidents a night, and up to 500 on a bad night *(planning assumptions, to validate)*. If people have to handle every one, Orvex would need hundreds of engineers *(estimate)*: the customer's DevOps cost simply moves to Orvex, and cheap cloud stops making money.

**An example night.** An online shop runs its app on several Quornex clusters. At 2 AM, one service's memory creeps up until it hits its limit, and the service keeps restarting. Checkouts fail. Shoppers notice first, the owner hears it from them, and Orvex finds out last. The customer loses sales and trust; Orvex loses credibility, and in the end the customer.

## Who This Serves

- **Primary: the Orvex Nightshift team** (working range: one engineer per 350–400 clusters). Orvex can't run Quornex at this scale without Nightshift, so Nightshift serves Orvex first. The team watches over Nightshift itself: its limits, its proposals and the lessons shared across the fleet. They are not paged for every customer incident.
- **Secondary: the customer's business owner** (or another senior person). They chose Quornex so they wouldn't need DevOps staff. Nightshift tells them in plain words what is wrong and what it did. They answer Nightshift's fix requests, choose which fixes it may run on its own, can watch their app's health live, and start the day with a summary of the night.
- **Secondary: Orvex support.** They handle customer incidents, and answer fix requests when a customer delegates approval to Orvex.

## The Solution

Nightshift runs inside every Quornex cluster. Every cluster runs the same Nightshift release; what differs between customers is only the permissions they choose in their cluster settings.

**How fixes are decided.** Every repair comes from a tested catalogue. Two separate questions decide what Nightshift may do:
- **How risky is the repair?** Each repair is rated **safe**, **risky** or **dangerous** *(definitions to settle in the PRD)*.
- **Who has said yes?** A **permitted** fix runs without asking, because the customer and Orvex approved it in advance. Any other fix needs an **approval** at the time, sometimes from both the customer and Orvex.

Risk and approval are kept separate: a low-risk repair may still need approval, for example because it affects the customer's production.

**Last resort is a condition, not a kind of fix.** The customer and Orvex can permit a fix in advance only for the case where nobody answers and failure is predicted within about 30 minutes *(Amine's proposal, to validate; not a proven safe boundary)*. An unanswered request or a near failure never grants extra permissions, and an action that Ground Rules prohibit can never be permitted, in advance or otherwise.

**The same night, with Nightshift.**
- **Hours before trouble,** Nightshift sees the checkout service's memory growing steadily. Once the trend becomes a real risk, it alerts the owner, and Orvex support if the contract says so:
  > "Your checkout service is using more memory than usual. Purchases still work, but at this rate memory runs out in about 4 hours and checkout may become unavailable. We haven't confirmed the cause yet. We suggest [fix]. Do you approve? If you don't answer, we'll keep watching and won't change anything."
- **If the owner approves,** Nightshift applies the fix, checks that it worked, and undoes it if it didn't.
- **If nobody answers,** Nightshift changes nothing. It keeps watching and alerting. The only exception is a fix permitted in advance for exactly this last-resort situation.
- **When something fails with no warning,** Nightshift applies a permitted fix if one exists; otherwise it reports the incident and calls for help.
- **In the morning,** the owner gets a summary: what happened, what was fixed, and the full timeline of anything risky.

**Quiet unless it matters.** A **phone call** only for critical problems, such as checkout failing. An **alert** when a problem becomes risky and needs a decision. Everything else goes on the **dashboard** and into the **morning summary**.

**The customer stays in control, within Orvex's safety limits.** The customer chooses what Nightshift may read, which fixes are permitted, and who answers fix requests. Permission to read never means permission to change. Some risky fixes also need Orvex's approval after the customer's, so a customer's settings can't damage their own app. Nightshift explains what it sees and does to both the customer and Orvex.

**Code fixes (experimental).** If the customer opts in, Nightshift can generate a fix for a bug in their code. An Orvex engineer must test and approve it; Nightshift never applies it alone. Danny wants this in the first version so Orvex can learn from real use.

## What Makes This Different

Nightshift is not better than existing tools at any single task. Like K8sGPT and HolmesGPT, it uses existing language models and monitoring tools; like HolmesGPT, Datadog or Azure's SRE Agent, it can ask for approval for fixes and run pre-approved ones. What matters is how these are combined and how well they fit Quornex, building on proven open-source tools such as Prometheus rather than rebuilding them. Whether the combination is unique is a claim to demonstrate, not a fact *(see `research-landscape.md`)*.

- **Built for one platform.** Hardware, capacity and workloads differ between clusters, but Orvex can test a repair once and use it across the fleet, on bare metal and EKS alike. What Nightshift learns from a problem in one cluster prepares the others.
- **Privacy by design** (see Ground Rules). Some commercial agents offer private options too, so this is a design commitment, not a claim that nobody else offers it.

## Success Criteria

All targets are estimates, to be checked first in controlled tests and then on the first 100 clusters. How each one is measured is in `addendum.md`.

| Signal | Target |
|---|---|
| Slowly developing failures detected before they affect the customer | ≥ 80% |
| Authorised repairs that restore health without causing another incident | ≥ 95% |
| Repairs that caused damage, counted separately from repairs that didn't work | Target to set; every case reviewed |
| Alerts that Orvex support and the Nightshift team confirm needed attention | ≥ 90% |
| Customer feedback on how clear and useful Nightshift's explanations are (measured separately) | Target to set |
| Clusters per engineer | 350–400 *(range to test)* |
| Monthly availability of customer-facing platform services | ≥ 99.9% *(assumption)* |
| Unapproved changes to customer production | **0** (see Ground Rules) |
| Monthly Nightshift cost per cluster, at 100 and 10,000 clusters | As low as realistically possible at close to public-cloud reliability (Danny) |

## Scope

**In the first version:** watching Kubernetes and the platform services on OMK and EKS, and, on OMK, the customer's hardware (detecting faults, not repairing them physically); the customer's own app if they opt in; prediction and plain-language explanations; permitted and approved fixes, including fixes permitted only as a last resort; phone calls, alerts, a dashboard and a morning summary; fleet learning; experimental code fixes; both model options (a hosted model, and a model on a GPU in the cluster).

**Out of the first version:** nothing is deferred yet. The things Nightshift must never do are permanent, so they are in Ground Rules.

## Ground Rules

From Orvex's brief:
- **A person approves risky changes, and any change to a customer's production.** Permitted fixes, including last-resort ones, don't break this rule: they run only after the customer and Orvex have both approved them in advance. Nightshift never decides on a change on its own.
- **One tool for two kinds of cluster:** OMK (Orvex Managed Kubernetes), which manages the operating system and Kubernetes on bare metal that the customer is responsible for, with Nightshift also watching that hardware; and hosted Kubernetes such as EKS, where the provider is responsible for Kubernetes and the underlying infrastructure, and Nightshift monitors what AWS and the chosen node setup expose.
- **Two ways to run the model.** Only a model on a GPU inside the cluster keeps private data inside the cluster. Otherwise, a trusted hosted model sees only what it must.
- **The same configuration everywhere.** Nightshift tunes its settings only within limits Orvex sets; anything bigger goes to Orvex as a proposal.
- **Nothing done in secret.** Everything Nightshift reads and changes is recorded where the customer can see it, and it holds only the permissions it needs.

Added from Danny's answers and our decisions:
- **A cluster belongs to one customer; a customer may have several clusters** (Danny). A customer may run their own control cluster that coordinates their workload clusters, but each cluster must still look after itself (Danny).
- **Rules and automation first;** AI only where they can't do the job.
- **Only approved, sanitised information leaves a cluster.** Raw logs and secrets stay inside.
- **Customer data, databases and backups are never changed or deleted** by Nightshift, not even with approval or in an emergency.
- **No improvised repairs.** Nightshift runs only repairs from its catalogue, tested before each release. Each repair is rated safe, risky or dangerous and handled accordingly. The AI may not invent repairs, especially generated shell scripts or commands. When a new problem is solved, its fix is added to the catalogue.

## Open Questions and Unknowns

**For Danny:**
- What does "close to public cloud reliability" mean as a number? *(Assumption: 99.9% a month.)*
- For some risky fixes, does requiring Orvex's approval after the customer's fit his approval model?
- How is a night like the example handled today: what monitoring and night cover does Orvex have?

**To test:** every estimate in this brief, starting with 250 incidents a night; whether a model on a 24 GB or 96 GB GPU is useful enough, not just whether it fits in GPU memory; whether GPU sharing meets the privacy rule and saves money; and whether filtering keeps private data inside the cluster. Details are in `addendum.md`.

## Vision

If Nightshift succeeds, Orvex's platform becomes the ultimate DevOps platform: it runs, monitors and heals the cloud for its customers. Nightshift is not a side product. Orvex's main goal needs it.

That goal is Danny's: let a million companies operate their own cloud at low cost, so that "a small underfunded startup in Tunisia" can have the same powerful setup as a well-funded enterprise, and private cloud can genuinely compete with public cloud.

For at least the next 3 years, Nightshift will rely heavily on hosted AI. As GPUs get cheaper and open-source models improve, more of it can run inside the cluster (Danny). The first version is also a way to learn: features such as code fixes may or may not stay.

## Corrections after finalisation

*2026-10-28, after Danny's reply (danny-qa Exchange 4).* The brief was approved before this reply, and three passages were corrected:
- **Ground Rules, one tool for two kinds of cluster.** Was: "OMK (Orvex Managed Kubernetes) on Orvex's bare metal, including the hardware". Customers are responsible for their own hardware; OMK manages the operating system and Kubernetes. On EKS, the provider is responsible for Kubernetes and the infrastructure.
- **Ground Rules, one customer per cluster.** Added the customer control cluster, and that each cluster must still look after itself.
- **Scope.** "The hardware on OMK" now says it is the customer's hardware, and that Nightshift detects faults there but does not repair them physically.

