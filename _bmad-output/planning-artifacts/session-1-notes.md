# Session 1 Notes and Understanding Check

Date: 2026-10-25. Status: paused. Amine will read and research before the next session.
Goal for the next 1-3 days: **understand** the problem and the architecture before producing any documents. Prototype or test cluster comes later, and the brief says prototypes are optional.

## Where we stopped

- Requirements checklist saved: `requirements-checklist.md` (same folder).
- Product brief started (create, coaching path): `briefs/brief-nightshift-2026-10-25/brief.md` (status: draft). Only "Who This Serves" has a first draft. Decision log: `.memlog.md` in that folder.
- `AI_LOG.md` at the repo root records what actually happened. The "overruled the AI" section is still empty.
- Nothing installed, no cloud resources, no code.

## Important points so far

1. Nightshift is an ops agent inside every Quornex cluster. It watches, fixes what is safe, and warns before things break.
2. The task is a **design** (PRD plus architecture), defended in 15 minutes. Understanding and honest reasoning are judged, not a working product.
3. Firm rule: human approval before any change to customer production.
4. Privacy rule: logs hold customer data and stay in the cluster. A hosted model sees only what it must.
5. Every cluster runs the same tested release. Nightshift tunes only within limits Orvex sets, and bigger changes are proposals.
6. Everything Nightshift reads or changes is recorded where the customer can see it, with least-privilege rights.
7. Your answer so far: primary users are the Orvex ops team. Customers see only what relates to them, especially changes that may touch their data.

## Questions for you (answer when ready, "I don't know" is a good answer)

Part A: the product (open from last message)
1. Which ops person is Nightshift mainly for (on-call engineer at 3am, platform engineer, manager)? What are they doing when it reaches them?
2. What does the customer see: everything or a subset? Who approves a change to customer production: the customer, Orvex, or both? What does "his data" mean?
3. How do things go wrong today without Nightshift? A real example, or a marked guess.

Part B: understanding check (explain each in your own words, 2-3 sentences, no looking it up first)
4. What is a Kubernetes cluster, a node and a pod? What is the difference between bare metal and EKS from an operator's point of view?
5. What are logs, metrics and traces, and why do the brief's "logs carry customer data" and "slow build-ups" matter for each?
6. Why can't you just send all logs to a hosted LLM? What is the risk if you do?
7. What is a "crafted log line" attack (prompt injection)? Why is an agent that reads untrusted text *and* holds powerful rights dangerous?
8. What does "safe repair" mean? Name one repair you think is safe and one that is not, and say why.
9. What is the difference between predicting, fixing and only reporting a failure? Give one example of each.
10. Why would the same configuration on every cluster make Nightshift's job easier?

Part C: before next session, find out (and note your sources)
- What OMK-like tooling and EKS monitoring look like in practice (names of the common open-source observability tools).
- What a GPU inside a cluster implies (cost, who runs the model).
- Anything that surprised you or that you could not explain.

## Questions for Danny (not sent yet; edit before sending)

1. What do Quornex clusters run today, and what monitoring or alerting already exists?
2. Is the approver Orvex staff, the customer, or configurable?
3. Which hosted models and regions count as trusted? Is an in-cluster GPU optional per cluster?
4. Is there a target price or margin per cluster for the cost model?
5. (New) What does the customer see of Nightshift's activity, and what does "customer's production" cover in a managed service?

## Suggested pace

- **Day 1 (next session):** read-back of Part A and B answers. I explain gaps. Resume the product brief.
- **Day 2:** failures, signals and "rules vs LLM" concepts, in simple terms. Finish the brief.
- **Day 3:** architecture concepts (per node, per cluster, central), privacy and cost basics. Then PRD.
- Prices and technical claims will be checked against primary sources, with dates, before they go into any document.
