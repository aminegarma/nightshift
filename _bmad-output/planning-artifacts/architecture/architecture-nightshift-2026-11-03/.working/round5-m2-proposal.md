# M2 Credential vending and independent usage checks (proposal, 2026-11-05, not decided)

AI proposal for Amine. Still unresolved until Amine decides and the open checks are done. Settled earlier (4.3, Amine): direct calls from the cluster's gateway with short-lived per-cluster credentials; local budgets; Fleet stops vending to over-budget clusters; a compromised gateway can lie about usage; stopping renewal is not a hard cap; shared account quotas are not per-cluster spending caps.

## Verified (2026-11-05)

| # | Fact | Source |
|---|---|---|
| F1 | An **application inference profile** tracks usage and costs per profile, and takes cost allocation tags | [Create an application inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html) |
| F2 | Bedrock's CloudWatch runtime metrics (invocations, input and output tokens, throttles) are documented only with `ModelId` (and `ContextWindow`) dimensions. **No per-profile or per-caller dimension is documented** | [Runtime metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html) |
| F3 | IAM revokes role sessions **all at once, by issue time** (a deny on `aws:TokenIssueTime`; about 30 s to take effect). Revoking one session isn't described there | [Revoke role sessions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html) |
| F4 | Bedrock token quotas are per account and Region (4.3, V4) | [Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) |
| — | **Not found:** a per-profile spending cap or rate limit; the quota on how many application inference profiles an account may have | — |

## What this means
- **Independent usage per cluster** is possible through billing (F1: per-profile cost tags), but billing data is **delayed** *(delay to verify)*. Near-real-time CloudWatch metrics don't separate clusters (F2).
- **No hard cap per cluster at AWS.** A compromised cluster with valid credentials can use up to the **shared account quota** until its credentials expire or are revoked, which also starves other clusters in the same account.
- **Per-cluster revocation** needs either one IAM role per cluster (F3 then revokes that cluster only; IAM role count limits to verify for 10,000) or a deny on the cluster's session name *(unverified)*.

## Options

| | **A. Direct, per-cluster profile, in cells** | **B. Thin metering proxy at Orvex** |
|---|---|---|
| How | Fleet vends 15-minute credentials *(STS minimum, verified in 4.3)* scoped to the cluster's own inference profile. Accounts are split into **cells** (e.g. per Region and a few hundred clusters), so a misbehaving cluster can only exhaust its cell's quota | Clusters call an Orvex proxy that forwards to Bedrock without storing anything, counts tokens from each response, and enforces per-cluster rate limits and hard caps |
| Independent count | Billing per profile (delayed), compared with the gateway's reported usage | The proxy's own count, in real time |
| Hard cap | No: exposure is about one credential lifetime × the cell's quota | Yes |
| Privacy | Content goes only cluster → provider | Content passes through Orvex (not stored, but a new party in the path; PRIV-9 channel; audit) |
| Operations | Many accounts and profiles to manage | A central hot path for 10,000 clusters; its outage means no AI (core loop continues) |

**AI recommendation:** A, with cells, because it keeps content off Orvex's path, which the privacy design (4.3) relied on. Accept the bounded exposure and say so plainly. Keep B as the fallback if testing shows that billing data is too slow or that the exposure per cell is too large.

## To verify before M2 can close
1. Quota on application inference profiles per account and Region (10,000 clusters, or per cell).
2. IAM role quota per account, or whether a deny on session name can revoke one cluster.
3. Delay of per-profile billing data (Cost and Usage Report / Cost Explorer) with cost allocation tags.
4. Whether invocation logging can record token counts **without** prompt or response text (it would add a near-real-time independent count, but must not store content: PRIV-2, ZDR).
5. Whether IAM policy can restrict a session to one inference profile ARN (resource-level permission on `bedrock:InvokeModel`).
