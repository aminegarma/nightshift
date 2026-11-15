# Review: reality check of the architecture spine

- **Reviewed:** `ARCHITECTURE-SPINE.md` (updated 2026-11-11), with `.memlog.md` (type "version" entries), `tool-comparison.md` and the round-7 and round-8 working files where the memlog points to them.
- **Reviewer task:** check that each committed decision rests on web-checked or memlog-verified facts rather than training data. Check that named technologies still exist and fit, and that the platform features the spine relies on behave as claimed today.
- **Review date:** 2026-11-11. Sources were fetched on that date.
- **Method:** I re-fetched the primary sources (vendor docs, project repos, W3C) for the highest-risk claims. Each claim was compared with the spine and with the memlog's verified entries.

## Verdict

Most platform facts the spine relies on are verified, and they still hold today. This covers Kubernetes Eviction preconditions, the EKS rollback window, EKS node auto repair, the EBS modification limit, IAM session revocation, Flux verification and impersonation, the VictoriaLogs retention behaviour and the kubelet image GC guidance.

The weak area is Amazon Bedrock. AD-35 and AD-36 combine three mechanisms:

- the per-model `allowed_modes` check;
- one application inference profile per cluster;
- a per-Region `none` setting with a Region named on the consent screen.

Today these live on different Bedrock endpoints or behave differently from what the spine assumes, and the cost-basis models sit on Anthropic's legacy Bedrock integration. Separately, AD-43 states a Flux enforcement ("a cluster refuses to start without it") that Flux does not provide.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 3 |
| Medium | 4 |
| Low | 8 |

---

## High

### H1 — AD-35 / AD-36: the Bedrock checks and the isolation design rely on two different endpoints, and the spine names neither

- **Claim:** AD-35: "Limit: the Bedrock control plane exposes no per-model retention signal; the executor checks the account mode and the model's allowed modes before use." AD-36: "One IAM role per cluster, permitted to invoke only that cluster's application inference profile."
- **Where:** AD-35, AD-36, Stack row "Amazon Bedrock model", Deferred "M2 validation".
- **What the sources say:**
  - **`allowed_modes` is visible only on the bedrock-mantle endpoint.** `GET /v1/models/{model}` on `bedrock-mantle` needs the IAM action `bedrock-mantle:GetModel`. The page states: "The Bedrock control plane does not expose a per-model retention signal." On `bedrock-runtime`, a model that needs more retention than the effective mode allows fails with `ValidationException`. The account mode for runtime is read with `GET /data-retention` (`bedrock:GetAccountDataRetention`). Source: [AWS Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html), fetched 2026-11-11.
  - **Application inference profiles are a `bedrock-runtime` (InvokeModel/Converse) mechanism.** On `bedrock-mantle`, AWS directs attribution to **Projects** instead. A project is not tied to one model, and it carries its own data retention mode. Source: [Bedrock Projects cost attribution](https://docs.aws.amazon.com/bedrock/latest/userguide/cost-mgmt-projects.html), fetched 2026-11-11.
  - **Claude Haiku 4.5 and Claude Sonnet 4.6 (the cost basis) are ARN-versioned models on Anthropic's legacy Bedrock integration** (InvokeModel and Converse). Current Anthropic SDKs send API version `2026-10-21`, which these models reject on Bedrock. The SDK must be pinned to the last major version before that release. Source: [Claude on Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy), fetched 2026-11-11.
- **Why this is high:**
  - The per-model check AD-35 promises cannot be run on the path AD-36 builds: runtime endpoint plus application inference profiles. It may not be possible at all for the cost-basis models.
  - The memlog (M1, 2026-11-04) recorded that only bedrock-mantle shows `allowed_modes`. The spine turned that limit into a check that the design cannot perform as written.
- **Fix:** pick the Bedrock endpoint explicitly in AD-35 and AD-36, then align the mechanisms:
  - **Runtime path:** enforce `none` with the documented SCP (deny `bedrock:PutAccountDataRetention` unless the mode is `none`). Read the account mode with `bedrock:GetAccountDataRetention`, and rely on Bedrock rejecting retention-requiring models with `ValidationException`. Drop the "model's allowed modes" check, or mark it unavailable.
  - **Mantle path:** use one Project per cluster, or per cell, with the project retention mode set to `none`. Check `allowed_modes` via `bedrock-mantle:GetModel`, and replace application inference profiles with Projects in AD-36.
  - **Either path:** pin the SDK version that matches the endpoint and model generation.
  - Record the result as a memlog "version" entry.

### H2 — AD-35 "Region and jurisdiction per customer" / consent screen names the Region: Claude on Bedrock runs through cross-Region inference profiles

- **Claim:** AD-35: "The consent screen names provider, Region and jurisdiction. Required provider properties: … Region and jurisdiction per customer." Deployment diagram: "Amazon Bedrock, retention mode none".
- **Where:** AD-35, cost model (regional +10% pricing).
- **What the sources say:**
  - Newer Claude models are offered on Bedrock "through cross-region inference rather than on-demand throughput". They must be called through an inference profile: `global.` for dynamic routing, or a geography prefix (`us.`, `eu.`, `jp.`, `apac.`) for "guaranteed data routing through specific geographic regions".
  - Claude Haiku 4.5 has only `global`, `us` and `eu` profiles; there is no `jp` or `apac`. Source: [Claude on Amazon Bedrock legacy](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy), fetched 2026-11-11.
  - The retention mode "is per-Region: it governs every request in the Region where you set it and does not propagate to other Regions". Where cross-Region inference is used, retained data "are stored in destination Regions". Sources: [data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html) and [abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html), fetched 2026-11-11.
- **Why this is high:**
  - A "regional" (`eu.`) profile spans several AWS Regions inside a geography; it does not pin one Region. So "Region per customer" and a consent screen that names a Region would be inaccurate.
  - Customers outside the US and EU may have no in-geography option for the cost-basis Haiku model.
  - The memlog (round 4) treats "regional" as one Region. That assumption was not checked.
- **Fix:**
  - The consent screen names the geography and the inference profile type, and states that processing may occur in any Region of that geography.
  - Set mode `none`, plus the SCP, in every source Region a cell uses.
  - Verify with AWS whether the source-Region mode governs requests processed in destination Regions.
  - List supported geographies per model in the Deferred row "Bedrock Region prices, model availability per Region".

### H3 — AD-43: "signature verification required; a cluster refuses to start without it" is not a Flux feature, and digest pinning needs an in-cluster updater the spine does not define

- **Claim:** AD-43: "Flux runs in each cluster, pulling OCI packages pinned by digest with signature verification required; a cluster refuses to start without it."
- **Where:** AD-43, diagram "Flux: required signature verification", AD-46.
- **What the sources say:**
  - `.spec.verify` is "an optional field to enable the verification" (Cosign or Notation), off unless set on each OCIRepository. On failure, `SourceVerified=False` and the controller retries.
  - The page describes no way to enforce verification cluster-wide. `.spec.ref.digest` "takes precedence over all other fields". A digest-pinned source therefore never picks up a new release until something rewrites the digest in the cluster.
  - `.spec.ref.semver` is the built-in way to follow new versions.
  - Source: [Flux OCIRepository (v1 API, docs v2.10)](https://fluxcd.io/flux/components/source/ocirepositories/), fetched 2026-11-11. The memlog (2026-11-05) correctly recorded "optional and off by default". The spine's "refuses to start" has no matching verified entry.
- **Why this is high:**
  - SEC-5 delivery trust relies on this sentence.
  - Under AD-42 no Fleet component may write into the cluster, so the spine does not say who updates the pinned digest for each release.
- **Fix:** state the enforcement mechanism as proposed. Two options:
  - an admission policy, such as a ValidatingAdmissionPolicy or Kyverno rule, that rejects any OCIRepository in Nightshift namespaces without `spec.verify`;
  - a startup check by the executor that refuses to run when verification is not configured or `SourceVerified` is not True.

  Define the update path, for example one of these:
  - semver plus required verification, with AD-46 downgrade checks done by the executor;
  - an in-cluster component that writes the digest from a signed release index after the AD-53 policy check.

  Move the rest to Deferred "Exact Flux configuration".

---

## Medium

### M1 — Cost-basis models are now previous-generation; newer, cheaper models exist

- **Claim:** Stack: "cost basis Claude Haiku 4.5 and Claude Sonnet 4.6 (prices verified 2026-11-04)"; AD-35 "pinned ZDR-eligible model".
- **What the sources say:**
  - Anthropic's current model table, cached 2026-11-03 in the Claude API reference, lists **Claude Haiku 5.5** at $0.10 / $0.50 per MTok (prompts ≤100K tokens) and **Claude Sonnet 5.5** and **Claude Sonnet 5** at $2 / $10, as first-party prices. Haiku 4.5 ($1 / $5) and Sonnet 4.6 ($3 / $15) are still served as the previous generation.
  - On Bedrock, Haiku 5.5 and Sonnet 5.x are on the new (non-ARN) integration. Haiku 4.5 and Sonnet 4.6 are on the legacy one. Source: [Claude on Amazon Bedrock legacy](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy), fetched 2026-11-11.
  - The 4.5/4.6 prices themselves are correct: Bedrock eu-central-1 lists $1.10 / $5.50 (Haiku) and $3.30 / $16.50 (Sonnet), per `.working/round8-prices-aws` and messaging-ai, AWS Price List published 2026-11-09.
- **Fix:**
  - Keep 4.5/4.6 as the frozen v4 basis, but add the current generation as a sensitivity row.
  - Before pinning a model, verify on Bedrock its eu-central-1 price, its geography profiles, and whether `allowed_modes` includes `none`. Claude models released from Fable 5 on may require `aws_review`; Fable 5, 5.1 and 5.2 do.
  - Correct the Stack row: the Bedrock prices were verified on 2026-11-11 from the AWS Price List. The 2026-11-04 check covered Anthropic list prices plus the 10% rule only.

### M2 — AD-36 independent usage source: a documented option is missing, and the quota for application inference profiles is still unknown

- **Claim:** AD-36 compares "AWS-recorded, content-free usage records and delayed per-profile billing" based on one application inference profile per cluster.
- **What the sources say:**
  - Since April 2026 Bedrock supports **cost allocation by IAM principal**: caller identity in CUR 2.0, and IAM role tags in Cost Explorer. In August 2026 this was extended to `bedrock-mantle`. Sources: [AWS What's New, 2026-04](https://aws.amazon.com/about-aws/whats-new/2026/04/bedrock-iam-cost-allocation) and [AWS What's New, 2026-08-11](https://aws.amazon.com/about-aws/whats-new/2026/08/amazon-bedrock-expands-iam-principal-cost-allocation-bedrock-mantle/), found by search on 2026-11-11.
  - With "one IAM role per cluster", this gives per-cluster billed usage without creating 10,000 profiles. It is billing-grain, daily and delayed.
  - I found no documented quota on the number of application inference profiles per account. The memlog (round5-m2, open question 1) also left it unresolved.
- **Fix:**
  - Add IAM-principal cost allocation as the candidate independent usage source, or as a second source, in AD-36 and the M2 validation plan. It works on either endpoint.
  - Keep "profile count quota at 10,000 clusters" as an explicit blocker if profiles stay.
  - Verify in CUR 2.0 that `bedrock-runtime` InvokeModel calls carry the principal. The search results did not name runtime explicitly.

### M3 — AD-30 states per-source ingestion limits as a rule; the only Fluent Bit mechanism found drops data and does not document per-source scope or drop counters

- **Claim:** AD-30: "per-source ingestion limits from the collector … Dropped records are counted into the coverage report."
- **What the sources say:**
  - The Fluent Bit `throttle` filter averages a rate over a window, and "when the average over window is more than Rate, Fluent Bit starts dropping messages".
  - The page does not say whether the limit applies per tag or source, or whether drops are counted in metrics. Source: [Fluent Bit throttle filter](https://docs.fluentbit.io/manual/pipeline/filters/throttle), fetched 2026-11-11.
  - VictoriaLogs has no per-stream rate limit, only `-maxConcurrentInserts`, `-insert.maxQueueDuration` and line-size and field caps. Source: [VictoriaLogs docs](https://docs.victoriametrics.com/victorialogs/), fetched 2026-11-11.
  - The memlog (2026-11-04) lists "Fluent Bit per-source rate limiting" as still to verify. The spine lists it under Deferred but states the rule as settled.
- **Fix:**
  - Mark the per-source limit and the drop-counting in AD-30 as "mechanism to verify".
  - Name the candidate: one throttle filter instance per source tag. Check whether its drops appear in `fluentbit_filter_*` metrics, or add a counting step.
  - Until verified, the coverage report must not claim exact drop counts for throttled sources.

### M4 — AD-35 assigns the Bedrock retention check to the executor, which would need AWS Bedrock read permissions

- **Claim:** AD-35: "the executor checks the account mode and the model's allowed modes before use."
- **What the sources say:** the checks need these IAM permissions:
  - `bedrock:GetAccountDataRetention` (control plane);
  - `bedrock-mantle:GetAccountDataRetention` and `bedrock-mantle:GetModel` (mantle).

  Source: the IAM actions table on [data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html), fetched 2026-11-11.
- **Why it matters:** AD-36 gives AWS credentials only to the gateway, through credential vending, and AD-3 separates identities. An executor that holds AWS credentials conflicts with both. The executor also never calls Bedrock.
- **Fix:** move the check to the gateway, which makes the call, or to Fleet credential vending, which owns the cell accounts. Back it with the SCP from H1. Record the result in the audit trail.

---

## Low

### L1 — Prometheus version note is already outdated
- **Claim:** Stack: "3.15.1 was latest stable when checked 2026-11-04".
- **Source:** [Prometheus releases](https://github.com/prometheus/prometheus/releases), fetched 2026-11-11. 3.16.0 is marked latest (dated 2026-11-04, published 2026-11-05).
- **Fix:** keep "pin at implementation freeze", and update the note or drop the version.

### L2 — WebAuthn Level 3 is now a W3C Recommendation; the spine's challenge design should state the nonce entropy
- **Claim:** Stack: "W3C Web Authentication Level 3". AD-17 sets challenge = SHA-256(tag ‖ canonical(D)).
- **Source:** [W3C WebAuthn L3](https://www.w3.org/TR/webauthn-3/), fetched 2026-11-11: "W3C Recommendation, 25 August 2026".
- **Gaps:**
  - The memlog verified assertion behaviour through MDN only, not the spec's §7.2 (Verifying an Authentication Assertion) or §13.4.3 (Cryptographic Challenges).
  - The challenge's randomness comes only from `cluster_nonce`, and the spine gives no size for it.
- **Fix:**
  - Cite the Recommendation (2026-08-25).
  - Check the AD-17 verification list against §7.2. That includes the `rpIdHash`, UP and UV flags, `type`, `origin`, and how `crossOrigin` and `topOrigin` are handled.
  - Set a minimum on `cluster_nonce`, for example at least 16 random bytes, per §13.4.3.

### L3 — AD-51 local dashboard RP ID on internal DNS is unverified per browser and passkey provider
- **Claim:** "the relying-party ID is that hostname" on the customer's internal DNS.
- **Status:** the memlog verified only the rpId and origin suffix rule, via MDN on 2026-11-05. It did not check behaviour with internal-only names: these must be valid domains (not IP addresses), served over HTTPS with a certificate the admin's browser trusts. It also did not check synced passkey providers.
- **Fix:** add these points to the Deferred row "Local dashboard DNS, certificates and routing", as a WebAuthn-specific test.

### L4 — AD-13 / AD-10 could use verified EKS repair details
- **What the source says:** [EKS node repair](https://docs.aws.amazon.com/eks/latest/userguide/node-repair.html), fetched 2026-11-11, confirms the memlog entry. It adds detail that matters to AD-10 and AD-13:
  - `karpenter.sh/do-not-disrupt` does not exclude a node from repair on any compute type.
  - Karpenter v1.15+ honours `karpenter.sh/do-not-repair`. It also has an optional `RebootForRepair` gate, and in Auto Mode a Reboot action is carried out as a Replace.
  - Managed node groups pause repair only when the group has more than five nodes and more than 20% are unhealthy, or on an ARC zonal shift.
- **Fix:** record these in the AD-13 per-mode notes. The executor's "is AWS or Karpenter repairing this node" check can then read the `karpenter.sh/disrupted` taint and `NodeRepairBlocked` events.

### L5 — AD-37 llama.cpp hardening details
- **Source:** [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md), fetched 2026-11-11. It confirms `--api-key` and the `127.0.0.1` default, as the memlog says. It also states:
  - `/health` is exempt from the key.
  - CORS by default reflects any origin with credentials allowed.
  - `--tools`, `--agent`, MCP and `--props` widen what the server can do.
- **Fix:** AD-37 adds `--cors-origins` restricted, and keeps tools, agent, MCP and props disabled. Network policy stays the main control.

### L6 — "Zero retention" wording on the consent screen
- **Source:** [Bedrock abuse detection](https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html), fetched 2026-11-11. Bedrock "may store and review" flagged CSAM in image inputs and outputs, regardless of mode. Nightshift sends text only, so the practical effect is nil, but the consent screen should not over-claim.
- **Fix:** word it as "Bedrock data retention mode `none` (no durable storage of prompts and responses)", not as an absolute.

### L7 — EKS node monitoring agent installation and Auto Mode inclusion are still unverified
- **Status:** the [NMA page](https://docs.aws.amazon.com/eks/latest/userguide/node-health-nma.html), fetched 2026-11-11, lists conditions and events, but does not say whether Auto Mode bundles the agent or how it is privileged.
- **Assessment:** the spine labels this correctly in Deferred. No change is needed beyond keeping AD-31's "where supported".

### L8 — etcd limits are generic
- **Claim:** AD-2 cites the etcd v3.5 defaults (1.5 MiB request, 2 GiB quota).
- **Status:** I did not re-check these. The round-7 file notes a suggested maximum of 8 GiB, and EKS and OMK may set other values.
- **Assessment:** the rule ("no evidence in Kubernetes objects") is conservative and stands. Write the numbers as "etcd defaults" rather than as platform limits.

---

## Confirmed against primary sources today (no change needed)

| Claim (spine location) | Source, fetched 2026-11-11 | Result |
| --- | --- | --- |
| Eviction honours `deleteOptions` UID and resourceVersion preconditions, returning 409 on mismatch, and 429 when a PDB blocks (AD-6) | [kubernetes eviction.go](https://github.com/kubernetes/kubernetes/blob/master/pkg/registry/core/pod/storage/eviction.go) | Confirmed. With a caller-supplied resourceVersion, a conflict is returned as-is and not retried. Without one, an unhealthy-pod conflict becomes a 429. |
| EBS: 4 modifications per rolling 24 h, each must complete first; cannot cancel or decrease (AD-52) | [EBS modify volume](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html) | Confirmed. |
| EKS control-plane rollback to the previous minor version within 7 days; an upgrade cannot be paused once started (AD-45, AD-44) | [EKS update-cluster](https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html) | Confirmed. Auto Mode rolls back worker nodes before the control plane. |
| EKS node auto repair: on and not configurable in Auto Mode; PDB bypass on Auto Mode and Karpenter < 1.15; 20% pause (AD-13, AD-10) | [EKS node repair](https://docs.aws.amazon.com/eks/latest/userguide/node-repair.html) | Confirmed; details in L4. |
| IAM revocation by `aws:TokenIssueTime`, whole role, about 30 s (AD-36) | [IAM revoke sessions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html) | Confirmed: all sessions of the role issued before the time. No single-session revocation is documented. |
| Flux `serviceAccountName` impersonation, `--default-service-account`, `spec.suspend` (AD-43, AD-45) | [Flux Kustomization](https://fluxcd.io/flux/components/kustomize/kustomizations/) (docs v2.10) | Confirmed. `--no-cross-namespace-refs` is also available. |
| Flux OCIRepository digest pinning; verification optional; `SourceVerified` (AD-43) | [Flux OCIRepository](https://fluxcd.io/flux/components/source/ocirepositories/) | Confirmed (API v1). Enforcement is not provided by Flux; see H3. |
| Argo CD has no native OCI source signature verification (rejection rationale) | Argo CD docs search; third-party 2026 guide | Consistent: nothing found in the official docs. The rejection rests mainly on credentials and inbound connections anyway. |
| Bedrock modes `none`, `default`, `aws_review` (and legacy `provider_data_share`); Bedrock blocks models that need retention; SCP can force `none` (AD-35) | [Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html) | Confirmed. Models released before Claude Fable 5 are unchanged. The memlog's "Fable 5 requires aws_review" is confirmed. Endpoint issues are in H1 and H2. |
| VictoriaLogs: 7-day default retention; mutually exclusive disk caps; read-only when full; keep 20% free; no per-stream rate limit (AD-30) | [VictoriaLogs](https://docs.victoriametrics.com/victorialogs/) | Confirmed. |
| Kubelet GC owns image cleanup; avoid external GC tools (AD-52) | [Kubernetes garbage collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/) | Confirmed. |
| llama.cpp `--api-key`, default bind `127.0.0.1` (AD-37) | [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) | Confirmed; additions in L5. |
| Haiku 4.5 $1 / $5, Sonnet 4.6 $3 / $15, Bedrock regional +10% (cost basis) | Anthropic model table (cached 2026-11-03); [Bedrock legacy page](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) | Confirmed; currency issues in M1. |

## Not re-checked today (relying on memlog entries)

These rely on the memlog's dated entries and were not re-fetched:

- Alertmanager features (2026-11-05)
- the non-graceful node shutdown `out-of-service` taint and PVC expansion behaviour (round 7, 2026-11-11)
- NIST SP 800-63B-4 on SMS
- EC2 throttling and Health API plan requirements (2026-11-04)
- Pod Identity on Fargate
- DefaultTolerationSeconds

None is new enough or volatile enough to raise beyond Low. Re-check them at build when the Stack versions are pinned.

## Stack rows marked "unverified"

The Stack labels Kubernetes, Alertmanager, Fluent Bit, VictoriaLogs, the exporters, the node monitoring agent, Flux and llama.cpp as "version to pin at build (unverified)". All of these projects still exist and are maintained. Current markers: Prometheus 3.16.0, Flux docs v2.10, and EKS docs citing Kubernetes 1.36 and 1.37. The labels are accurate and acceptable for a design spine.
