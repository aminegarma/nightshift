# Session 2: Understanding Check

Date: 2026-10-26. Format: 7 rounds, 35 questions, answered by Amine without looking anything up. After each round Claude gave feedback.
Purpose: find what Amine already understands and what to study before writing the product brief, PRD and architecture.

**Caution:** Claude's feedback included technical claims and prices from model knowledge. They have **not** been checked against primary sources. The ones to verify are listed at the end.

## Result per round

| Round | Topic | Overall |
|---|---|---|
| 1 | Big picture, deliverables | Shape right. Missing: why humans don't scale, the judging criteria, AI_LOG overrules |
| 2 | Kubernetes and infra | Basics solid. Gaps: what happens when a node dies, cordon vs drain, DaemonSet vs Deployment |
| 3 | Signals and failures | Strongest round. Leans too much toward "fix". Gap: root cause vs symptoms |
| 4 | AI, privacy, security | Good security instincts. Gaps: allow-list vs deny-list, why prompt injection works |
| 5 | Safety | Tends toward big actions. "Silence = act anyway" breaks the firm rule |
| 6 | Cost | Weakest. Fixed vs variable costs, linear scaling, shared GPU breaking privacy |
| 7 | Process | PRD vs architecture sorting 5/5. Overrules and verification still vague |

## Gaps, most important first

1. **Safety mindset.** Prefer small, reversible actions. When in doubt, hold steady (cordon, watch, escalate) and call a person. Silence is not approval. Never take a *bigger* action because nobody answered.
2. **How things fail.** Disk vs memory. What happens when a node dies (Deployment pods move; StatefulSet or database pods with local disks get stuck). Real hardware failures (disk health, memory errors, network cards, heat). Classics: memory creep and the process being killed, expired certificates, network links. Root cause vs symptoms (timing, location, dependencies, known patterns).
3. **Architecture shape.** Per node: a small collector (DaemonSet). Per cluster: the brain, the executor, the approval queue and the record (Deployment). Central at Orvex: fleet learning, approvals, signed rule releases, and watching for clusters that go silent. A GPU model, if any, runs once per cluster. Nightshift must not go blind when the control plane fails. OMK vs EKS: on bare metal, report hardware faults; on EKS, replace the node. On EKS, AWS runs the control plane.
4. **AI design.** The model explains and suggests; plain code decides and acts. Actions come from a fixed catalogue, checked by plain code and limited by RBAC. Why prompt injection works: instructions and data travel in the same text. Human approval can be fooled too, so show the raw action and the original evidence.
5. **Privacy.** Allow-list fields instead of trying to delete private ones. Replace values with placeholders, keeping the mapping inside the cluster. Assume some data leaks, so send as little as possible. Proof needs a single gateway, an append-only record, and stripping rules customers can test. What a provider does with the data relies on a contract and can't be proven.
6. **Compromised agent.** Keep the record out of the agent's reach. Signed approvals happen outside the cluster. The part that reads untrusted text is separate from the part that holds rights. Fleet lessons are only proposals, reviewed and signed centrally. Kill switch and action limits.
7. **Fleet learning pipeline.** Evidence with private data removed → a person diagnoses → rule plus fix → replay test → watch-only ("shadow") run across the fleet → gradual rollout with rollback → signed, versioned, part of the tested release.
8. **Cost.** Split fixed costs (team, central system) from variable ones (GPU, tokens, storage, network traffic, human time per incident). GPU cost per cluster stays roughly flat because each cluster needs its own GPU. What falls at scale is the *share* of fixed costs. Tokens = calls × tokens per call × price. Use a sensitivity analysis to find what moves the cost most. "Sensible" = compared with human DevOps cost, cluster cost, outage cost, and per-server prices of monitoring products.
9. **Honest-thinking habit.** Label every claim "brief says / I assume / verified (source, date)".

## What Amine got right (keep)

- Kubernetes basics (cluster, node, control plane).
- Logs, metrics and traces, and which ones carry customer data.
- Threshold vs prediction.
- A heartbeat whose absence is itself the alert.
- Read-only diagnosis plus an execution gate plus approval.
- Isolation between clusters plus an outbound firewall.
- A person reviews fleet lessons.
- PRD vs architecture sorting.

## New questions for Danny (add to the list, not sent yet)

6. Does each cluster serve one customer, or do several customers share a cluster? (This affects privacy, customer visibility and approvals.) **Answered: not shared. See `danny-qa.md`.**
7. Confirm the timeline: Amine reports Danny said 2-3 weeks. From which date, and what is the exact hand-in date?

## Study list (short)

- Kubernetes: node failure and pod eviction, StatefulSets with local storage, cordon, drain, PodDisruptionBudgets, DaemonSets, RBAC.
- Signals: Prometheus (and `predict_linear`), a log store (for example Loki), a collector (for example Fluent Bit or OpenTelemetry Collector). Names only for now.
- Security: prompt injection (OWASP Top 10 for LLM applications).
- Cost: current GPU instance prices and hosted-model token prices, with dates.

## Claims from this session still to verify against primary sources

- Kubernetes waits about 5 minutes by default before evicting pods from an unreachable node.
- AWS `g4dn.xlarge` (T4 GPU) costs about $0.50/hour, about $380/month (region and date to confirm).
- The `NETDEV WATCHDOG ... transmit queue timed out` kernel message as a sign of a hung network card.
- Microsoft Presidio as an open-source detector for private data.
- Datadog-style per-server monitoring prices, as a reference point.
