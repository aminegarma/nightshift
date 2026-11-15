# Party challenge of the hybrid design (C), 2026-11-03

Requested by Amine. The room: Winston (architect), Vex (security) and Moss (operations, an ad-hoc SRE persona). Topics: complexity, crash recovery and Kubernetes outages. **Nothing here changes the architecture until Amine decides.**

## Findings

| # | Finding | Who pushed it | Status |
|---|---|---|---|
| P1 | The honest count of per-cluster deployables is 6–7, not 3: agent, gateway, executor, audit service, independent checker, hardware component (SEC-3), heartbeat path. Proposal: ship one image with a role per pod. Keep separate pods, because a ServiceAccount is set per pod. | Moss, agreed by Vex and Winston | To decide |
| P2 | Executor replicas. **Single** (Recreate rollout): no stale-leader risk, but repairs pause for about 5 minutes if its node dies (default eviction from an unreachable node). **Two with leader election**: faster takeover, but a paused old leader can wake up and act. | Vex single, Moss two, Winston single for v1 | Disagreement |
| P3 | Catalogue rule: every automatic action declares whether it is idempotent and how to check "did it already happen?". An action without that check can't be automatic in v1. Most such actions (power, IP or NIC changes) are already dangerous, so manual (FR-52). | Vex, agreed | To decide |
| P4 | Only the executor may depend on the Kubernetes API for its core loop. The checker, gateway, audit service and heartbeat must keep working without it. | Winston, agreed | To decide |
| P5 | When the API comes back, the executor applies stop decisions (withdrawals, rejections, unticks, alert-only) before it resumes any repair. | Vex, agreed | To decide |
| P6 | Repairs needed *because* the API is down, for example a control-plane disk filling up. **Escalate to a person in v1**, or add a node-level helper that can act without the API. | Moss for the helper, Vex against, Winston: escalate in v1, revisit | Disagreement |

## Assumptions flagged

- A1: the 5-minute pause is acceptable for the executor's own node failing (untested, depends on NFR-7 targets that are still open).
- A2: a disk filling up is a common cause of control-plane outages on OMK. This is the room's experience, not Orvex data.
- A3: 6–7 small processes cost tens to low hundreds of MiB per cluster (unmeasured estimate).
- A4: Kubernetes audit logging gets configured on OMK by Orvex. On EKS it is the customer's account and cost (who enables it is undecided).

Kubernetes facts checked 2026-11-03:
- [ServiceAccount per pod](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [DefaultTolerationSeconds, 5 minutes](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

## Decisions (Amine, 2026-11-03)

- Keep C.
- **P2:** one active executor in v1. This doesn't eliminate duplicate actions, because a partitioned old process may still exist. Action-level duplicate protection stays, and restart and takeover behaviour is defined. Recovery time is to test, not a guaranteed five minutes.
- **P6:** control-plane failures are reported and escalated to a person. The node-level repair helper is deferred, and the reduced automatic-repair coverage is documented.
- **P1:** sensitive roles get distinct security boundaries and identities. A shared image is optional.
- **P3:** every automatic action has safe retry behaviour or reliable evidence that it already happened. Deleting files isn't automatically safe to repeat when its targets can change.
- **P4:** observation, outbound checks, auditing and heartbeats continue through temporary API outages where possible, with the cached dependencies and their limits documented. Running pods may continue, but Kubernetes can't necessarily restart them.
- **P5:** stop decisions are processed before repairs resume. Authorisation, evidence and action state are revalidated.
- The assumptions above stay estimates. The personas' claimed experience is not operational evidence.
