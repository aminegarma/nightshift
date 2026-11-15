# Party challenge of the 3.3 infrastructure adapters, 2026-11-04

Requested by Amine. The room: Winston (architecture), Vex (security), Moss (operations). Questions: one signal interface across OMK, EKS EC2 and Fargate; missing coverage, misleading diagnoses and adapter failure; minimum privileges, credential isolation and AWS API costs; complexity versus reusing collectors. **Nothing here changes the architecture until Amine decides.** This round supersedes disagreements D1–D3 in `party-check-3.3-2026-11-04.md`.

## Verified facts (primary sources, checked 2026-11-04)

| # | Fact | Source |
|---|---|---|
| F1 | "Currently, the Amazon EC2 Describe* API actions do not support resource-level permissions." A read role can't be limited to one cluster's instances (a Region condition is possible) | [AWS EC2 IAM policies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policies-for-amazon-ec2.html) |
| F2 | The AWS Health API needs a Business Support+, Enterprise or Unified Operations plan (older plans: Business, Enterprise On-Ramp, Enterprise). Without one it returns `SubscriptionRequiredException` | [AWS Health API](https://docs.aws.amazon.com/health/latest/ug/health-api.html) |
| F3 | EC2 throttles API requests per account per Region with token buckets. Non-mutating calls: 100 burst, 20 per second refill. Unfiltered or unpaginated `DescribeInstanceStatus` uses a smaller bucket (50 burst, 10 per second) | [EC2 API throttling](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-throttling.html) |
| F4 | EC2 status checks (system, instance, attached EBS) run every minute and can't be disabled. Scheduled events (retirement, reboot, maintenance) are returned by `DescribeInstanceStatus` | [Status checks](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html), [Scheduled events](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html) |
| F5 | EKS Pod Identity isn't available for pods on Fargate. If IMDS isn't restricted, a pod's containers can reach the node's IAM role. "Containers are not a security boundary" | [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) |
| F6 | The EKS node monitoring agent is Apache-2.0, runs as a DaemonSet and is recommended as an EKS add-on. It reports storage, network, kernel, runtime and accelerator conditions and events. EKS auto repair acts on those conditions when enabled | [eks-node-monitoring-agent](https://github.com/aws/eks-node-monitoring-agent), [node health](https://docs.aws.amazon.com/eks/latest/userguide/node-health-nma.html), [node repair](https://docs.aws.amazon.com/eks/latest/userguide/node-repair.html) |
| F7 | Fargate doesn't support DaemonSets or privileged containers | [Fargate considerations](https://docs.aws.amazon.com/eks/latest/userguide/fargate.html) (research, 2026-10-29) |
| F8 | smartctl_exporter needs root. ipmi_exporter can query remote BMCs | Repositories (checked 2026-11-04) |

## Not verified (assumptions or to check)

- No per-request charge for EC2 `Describe*` calls was found in the docs read *(to confirm)*. CloudWatch metric reads are charged *(price to verify; avoided in v1)*.
- IRSA works for pods on Fargate *(to verify)*.
- Whether Auto Mode includes the node monitoring agent, and whether that agent runs privileged *(to verify)*.
- Whether BMCs enforce read-only accounts *(to test)*.
- How AWS accounts are laid out for Quornex customers (one per customer, or shared) *(to confirm)*.

## Findings

| # | Question | Finding |
|---|---|---|
| A1 | One interface | Works only if every value carries its **source, vantage point, platform, freshness and coverage state** (observed / not observable / not permitted / stale), and "unknown" never defaults to healthy. Catalogue entries state **per platform** which sources count as evidence. Without enough evidence on a platform, the entry becomes "only report" there |
| A2 | Misleading diagnosis | A failing EC2 *system* status check means a problem on AWS's host (power, network, host hardware). It doesn't say *which*, so FR-20's "report uncertainty" applies. A node replaced by EKS auto repair must not be diagnosed as a crash: Nightshift correlates it with AWS's repair markers |
| A3 | Adapter failure | Adapter down: its signals go "unknown", a monitoring failure case opens (FR-4), and disruptive repairs that depend on them are blocked (coordinator point 8) |
| A4 | Missing coverage | Fargate (no node collectors, F7), Hybrid Nodes (the customer's hardware), OMK without a BMC (FR-7), EKS without an AWS role. All visible in the coverage report |
| A5 | Privileges | The AWS read role sees the whole account in its Region (F1). Mitigation: a Region condition, filtered and paginated calls, client-side filtering to its own nodes, no other cluster's data in the evidence (PRIV-1) |
| A6 | Credential isolation | Pod Identity scopes the role to one service account, but **only if IMDS is restricted** (F5). Otherwise any pod, including a compromised agent, could reach the node role. Not on Fargate (F5) |
| A7 | AWS cost | Don't depend on the Health API (F2). `DescribeInstanceStatus` returns status checks and scheduled events (F4). Throttling arithmetic (F3): at 1 filtered call per cluster per minute, one account and Region sustains about 20 × 60 ≈ **1,200 clusters** *(estimate; real calls per poll may be more than 1)* |
| A8 | Complexity | Reuse the existing collectors: node_exporter, smartctl_exporter and node-problem-detector on OMK; the AWS node agent (F6) on EKS. The **credentialed adapter exists only where credentials are needed**: a BMC reader on OMK, an AWS poller on EKS. The "signal interface" is a mapping in the catalogue plus the agent's normalisation, not a new service |

## Recommended practical v1 design

1. **Signal interface:** a catalogue mapping (signal family → sources per platform), consumed by the agent. Every value carries source, vantage point, freshness and coverage state, and "unknown" is never healthy (A1).
2. **Reuse collectors:**
   - OMK: node_exporter, smartctl_exporter, node-problem-detector.
   - EKS EC2: node_exporter plus the AWS node agent, or node-problem-detector where the AWS agent isn't installed. No SMART promise.
   - Fargate: pod status and probes only.
   - Hybrid Nodes: OMK rules, without a BMC unless the customer provides one.
3. **Credentialed adapters only where needed,** each in its own pod and identity:
   - **OMK BMC reader:** credentials fetched just in time, read-only BMC accounts where enforced, network rules to the listed BMCs only.
   - **EKS AWS poller:** Pod Identity (IRSA where Pod Identity isn't available), minimal `Describe` actions with a Region condition, filtered and paginated calls, polling every ≥ 60 s with jitter and backoff [to set], client-side filtering. **Optional:** if it isn't granted, coverage is reduced.
4. **No dependency on the AWS Health API** (F2).
5. **Failure behaviour:** adapter down → "unknown", a monitoring failure case, and dependent disruptive repairs blocked (A3).
6. **Diagnosis keeps uncertainty,** and correlates AWS repairs (A2).
7. **Privileged exporters:** one minimal pod each, read-only filesystem, egress only to the local metrics store, no Kubernetes write rights.

## Decisions for Amine (only those that materially affect coverage, safety or cost)

- **DA:** EKS AWS access. An optional, customer-granted read role, accepting that it sees the account's instance inventory in its Region (F1), or no AWS API in v1 (losing EC2 status checks and scheduled events).
- **DB:** IMDS restriction on EKS. A hard prerequisite for enabling the AWS poller, or only a recorded risk.
- **DC:** AWS polling at scale. A poller per cluster (about 1,200 clusters per account and Region at 1 call a minute, estimate), with a shared poller per account only if accounts are shared, or a shared poller from the start.
- **DD:** Node checkers on EKS. The union of distinct checks from node-problem-detector and the AWS agent, or the AWS agent only (fewer privileged pods, less coverage).
