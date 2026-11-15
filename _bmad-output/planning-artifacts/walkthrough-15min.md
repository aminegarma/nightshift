# Walkthrough: 15 minutes, then questions

Speaker notes for presenting the Nightshift design to Danny and the Orvex team. Each block gives the time, the point to land, what to show, and the one sentence to say if time runs short.

## 0:00–1:00 · What this is

- **Point:** Nightshift is an ops agent in every Quornex cluster, on bare metal (OMK) and EKS, so Orvex can run 10,000 clusters with a small team. It's a design: nothing is built or tested yet.
- **Show:** the bottom line at the top of `architecture-orvex.md`.
- **If short of time:** "Rules do the work, AI only explains; the agent that reads logs can't act; nothing is claimed as tested."

## 1:00–3:00 · One design for bare metal and EKS (criterion: architecture)

- **Point:** the same components per node, per cluster and in Fleet; only the adapters and repair scope change between platforms.
- **Show:** the picture in §1, then the OMK/EKS table in §2.3.
- **Land:** OMK hardware belongs to the customer, and the BMC is read-only in v1. On EKS, Nightshift never fights AWS node repair. Clusters only connect out.

## 3:00–5:00 · How a repair stays safe (criterion: architecture)

- **Point:** the agent proposes, and a separate executor checks everything itself before acting.
- **Show:** §3.3, "one repair with a crash" (sequence diagram).
- **Land:** intent is written first; changes are tied to the exact object; after a crash it applies stops, reconciles and revalidates; ambiguous cases go to a person. A retry needs valid authorisation and verified protection against duplicate runs; "retry once" alone isn't safety.

## 5:00–7:30 · Who can approve, and what happens offline (criterion: privacy and security)

- **Point:** authority comes from people's signatures checked inside the cluster, not from the portal or Fleet.
- **Show:** §4.3 (passkey plus SMS code), §4.7 (validity tiers).
- **Land:**
  - **Stops beat approvals.** Receipts say "Sent — not yet effective in the cluster" until the cluster confirms.
  - **Offline, permissions are judged by the authority they need.** After 1 hour without Fleet, anything needing Orvex's authority pauses. After 24 hours, only the customer's own safe ticks continue, within their validity.
  - **State the limits honestly:** a compromised portal can mislead someone who doesn't read the SMS, and cluster-admin is a documented limit (SEC-10, AD-72).

## 7:30–9:30 · Customer data and the locked-down agent (criterion: privacy and security)

- **Point:** raw logs never leave. Outbound messages are built from typed fields, and every outbound flow is checked.
- **Show:** `privacy-security-review.md`, the three tables: specified design controls, remaining risks, not yet validated.
- **Land:**
  - default-deny networking, with three purpose-specific exceptions;
  - prompt-injection controls (§5.4): an AI taken over by injection still can't act, approve or send data out by itself;
  - the planned injection and planted-secret tests, which haven't been run.

## 9:30–11:30 · Cost (criterion: cost)

- **Point:** hosted AI tokens are tiny (about $0.02 per cluster per month). The in-cluster footprint and people are what cost money.
- **Show:** §12 and `cost-model/cost-model-results.md`.
- **Land:**
  - Orvex cash and the customer's footprint are shown separately.
  - At 10,000 clusters, Nightshift needs far fewer engineers than manual operation under the stated assumptions. At 100 clusters, round-the-clock cover sets the cost on both sides.
  - "About 15 engineers" is a target. The model shows what has to be true to reach it.
  - Every input is either sourced or labelled as a placeholder.

## 11:30–13:00 · Failures (criterion: honest thinking)

- **Point:** the top 20 failures, each *predict*, *fix* or *only report*, for both platforms.
- **Show:** the table in §11 or `failure-catalogue.md`.
- **Land:** many failures are detected and reported, not fixed. Stateful takeover needs a verified fencing procedure, and nothing is called tested before it is.

## 13:00–14:00 · How I steered the AI (criterion: AI fluency)

- **Show:** `AI_LOG.md`, "Five to read first".
- **Tell two stories:**
  1. The AI recommended EU-only AI routing; I overruled it, because customers are worldwide.
  2. The AI's first cost model needed 48 engineers, because it read "supported" as "automatic" and guessed its inputs. I made it use the PRD's figures, separate the types of work, and show the conditions instead of a single number.

## 14:00–15:00 · What I'd test next, and open questions (criterion: honest thinking)

- **Show:** "What I'd test next" and "Open questions" in the README.
- **Ask Danny:**
  - the OMK details (distribution, network plugin, storage, BMC);
  - what the 15-engineer target covers.

## Likely questions, with where to point

| Question | Short answer | Where |
|---|---|---|
| Why not let the AI fix things directly? | AI output is untrusted. Repairs come only from the signed catalogue, checked by the executor | Orvex document §3, §5.4 |
| What if Fleet is compromised? | It can delay or hide decisions, but can't approve, forge a release or connect into a cluster; missing receipts show it | Compromise table §5.3 |
| Why SMS when NIST discourages it? | It's a second channel naming the action, not the main factor; the passkey signature is the protection. The limits are written down | §4.3; privacy review |
| Why Flux and not Argo CD? | Pull-based per cluster, digest pinning and signature checks; central Argo CD would hold credentials to every cluster | `tool-comparison.md` §8 |
| Why Bedrock first? | The zero-retention mode is enforced by AWS rather than resting on a contract; Regions are per customer | §7; tool comparison §9 |
| How credible is the cost model? | Reproducible script; sourced inputs; placeholders labelled; scenarios and sensitivities shown | `cost-model/` |
| What happens at 3 AM with nobody answering? | Nothing that isn't already authorised runs; Nightshift keeps alerting. Last resort needs prior permission from both sides | PRD FR-23, FR-24 |
