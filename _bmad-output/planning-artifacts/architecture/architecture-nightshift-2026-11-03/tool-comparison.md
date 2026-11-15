# Nightshift: tool comparison and evidence

The tools Nightshift's architecture compared, what was chosen, what was rejected, and the evidence for each claim. It is a living file, updated as each architecture round chooses tools. Last updated 2026-11-04.

**How to read the status column:**
- **Decided:** chosen by Amine, as a working architecture choice.
- **Provisional default:** chosen for now, open to replacement after measurement.
- **Alternative to evaluate:** kept, but adopted only if a measurement justifies it.
- **Lean, pending:** the AI's proposal, not yet decided.
- **Rejected:** with the reason.

**Evidence labels:**
- **Documented:** the project's own documentation or repository says so (link and access date). This is the maintainer's claim, not an independent test.
- **Estimate:** planning arithmetic, not a measurement.
- **Unverified:** no adequate source or test yet.

Most "Documented" items were retrieved in the open-source research of 2026-10-29 (`research/technical-nightshift-open-source-architecture-2026-10-29/`). Items marked 2026-11-03 or 2026-11-04 were rechecked in this architecture run. **No benchmark, security audit or production deployment of these tools was performed for Nightshift.** Every resource and cost figure is unvalidated.

---

## 1. Repair execution (round 1)

| Option | Licence | In plain words | For | Against | Status |
|---|---|---|---|---|---|
| **Hybrid (C):** ordinary services for the agent and gateway, plus a Kubernetes controller for the executor with `RepairRun` objects and one claims ledger | — (design pattern) | Only repairs go on Kubernetes' "shared whiteboard". Everything else talks directly | Persistent repair progress without making every part an operator | Progress alone isn't crash safety (needs intent-before-action, target-ID guards and checking reality on restart). One more Kubernetes object type to version | **Decided** (2026-11-03) |
| A. Operator everywhere | — | Every component is a controller with its own object types | Consistent | 4–6 object types to version and protect, for parts that don't reconcile anything | Rejected |
| B. Plain services with the executor's own database | — | No custom objects. The executor keeps a database on a disk | Simplest to picture | Crash safety, migrations and backups built by hand | Rejected |
| [controller-runtime](https://github.com/kubernetes-sigs/controller-runtime) | Apache-2.0 | The standard Go library for writing Kubernetes controllers | Widely used, so C needs no framework of its own | It's a library, not a safe-repair product. The safety code is ours | Candidate library (decided with the stack) |
| [Argo Workflows](https://github.com/argoproj/argo-workflows) | Apache-2.0 | A workflow engine that runs steps as pods | Good for long multi-step jobs | Templates and parameters need lockdown. Too broad for fixed typed repairs | Rejected for v1 (reuse only if already run locally, locked down) |
| [Temporal](https://github.com/temporalio/temporal) | MIT | A durable workflow service | Strong for long management workflows | Needs its own services and datastore in every cluster | Rejected for clusters. Possible at Orvex central |
| [StackStorm](https://github.com/StackStorm/st2) | Apache-2.0 | Event-driven automation platform | Mature runbook automation | Large dependency footprint | Rejected |

**Evidence used in the round 1 decision (checked 2026-11-03):**
- Operator = custom resources plus controllers following the control loop ([Kubernetes](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)).
- The Eviction API respects disruption budgets and returns 429 when a budget blocks it ([Kubernetes](https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/)).
- Deletes can be guarded by the target's unique ID and version, returning 409 Conflict if they don't match ([Preconditions](https://kubernetes.io/docs/reference/kubernetes-api/definitions/preconditions-v1-meta/), [DeleteOptions](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/delete-options/)), and Eviction accepts them ([Eviction v1](https://kubernetes.io/docs/reference/kubernetes-api/definitions/eviction-v1-policy/)).
- etcd's default limits are 1.5 MiB per request and 2 GiB in total, so no evidence or audit goes into Kubernetes objects ([etcd](https://etcd.io/docs/v3.5/dev-guide/limit/)).
- A ServiceAccount is set per pod, so roles with different rights need separate pods ([Kubernetes](https://kubernetes.io/docs/concepts/security/service-accounts/)).
- Pods on a not-ready or unreachable node are evicted after 5 minutes by default ([Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)). This is not a promise about Nightshift's recovery time.
- On EKS, control-plane audit logs are off by default and charged through CloudWatch ([AWS](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)).

**Unvalidated estimates:** about 6–7 small processes per cluster, each roughly 20–60 MiB of RAM. Not measured.

## 2. Approvals and identity (round 2)

| Option | In plain words | For | Against | Status |
|---|---|---|---|---|
| **Passkey + SMS (B):** passkey sign-in → Approve → SMS from the cluster naming the action with a code → enter the code → a fresh passkey assertion over the decision's fingerprint. The cluster checks that both bind to the same decision | Face ID proves who you are. The SMS shows which action, from a channel the portal doesn't control | The cluster verifies both itself. A hacked portal alone can't forge an approval | Typing the code doesn't prove the person read the task. SMS can be hijacked. A hacked portal can still mislead someone who doesn't read the SMS | **Decided as a working proposal**, pending feasibility and usability testing (2026-11-04) |
| Passkey only (signing the decision fingerprint) | Face ID, no SMS | Simple. Phishing-resistant | The passkey prompt doesn't show the repair | Fallback only where a policy explicitly enables it, shown and recorded as reduced assurance |
| Passkey at sign-in + SMS code only (A) | The cluster checks only the code | One fewer tap | The cluster can't verify identity. Hacked portal + hijacked phone number = forged approval | Rejected |
| Portal signs on the person's behalf | The portal's key signs | Easiest | A hacked portal can approve anything (defeats SEC-9) | Rejected |
| Separate Orvex signing service | A hardened service signs after login | Better than the portal signing | A hack of that service forges approvals | Rejected |
| Approving inside Slack | Click Approve in Slack | Fast | The PRD allows approval only in the authenticated portal (FR-14) | Rejected (product decision) |

**Evidence:**
- A WebAuthn assertion is a signature over the authenticator data plus a SHA-256 hash of the client data, which includes the server's challenge ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAssertionResponse/signature), checked 2026-11-03).
- WebAuthn Level 3 defines no transaction-display extension: the client extensions it defines are appid, appidExclude, credProps, prf and largeBlob ([W3C](https://www.w3.org/TR/webauthn-3/), checked 2026-11-03).
- NIST SP 800-63B-4 sec. 3.1.3.3 treats SMS and voice as a "restricted" authenticator. Changing the registered phone number counts as binding a new authenticator ([NIST](https://pages.nist.gov/800-63-4/sp800-63b.html), checked 2026-11-04).

Identity providers screened in the research (not yet chosen): [Keycloak](https://github.com/keycloak/keycloak) and [Dex](https://github.com/dexidp/dex), both Apache-2.0. The research recommends reusing Quornex's identity provider. Authentication alone never establishes approval.

## 3. Metrics (round 3.1)

| Option | Licence | In plain words | For | Against | Status |
|---|---|---|---|---|---|
| **Existing Quornex monitoring** | — | Use what Quornex already runs | No duplicate collection | Unknown what Quornex ships (open question) | **Decided: reuse first**, when it meets Nightshift's fixed named queries |
| **[Prometheus](https://github.com/prometheus/prometheus)** (local, per cluster) | Apache-2.0 | Collects numbers like CPU, RAM and disk space, stores them inside the customer's cluster, checks rules and trends to spot problems, and keeps working when the connection to Fleet goes down (Amine's reasons) | The standard rules language; widely run; local and autonomous | Local storage isn't clustered or replicated. Memory and disk per cluster are a cost driver (unmeasured) | **Provisional default** (2026-11-04) |
| [VictoriaMetrics](https://docs.victoriametrics.com/victoriametrics/) single-node + [vmalert](https://docs.victoriametrics.com/victoriametrics/vmalert/) | Apache-2.0 core. Some vmalert features are Enterprise-only | A Prometheus-compatible store, with vmalert evaluating alerting and recording rules | The vendor claims lower resource use | MetricsQL is similar to PromQL, not identical. Savings are a vendor claim, not our measurement. One more component (vmalert) | **Alternative to evaluate**, adopted only if measured savings justify the complexity and query differences |
| [Zabbix](https://www.zabbix.com/license) | AGPLv3 (since 7.0) | An integrated monitoring server with proxies | Mature. Good at network and hardware monitoring | Proxies don't evaluate triggers or alert, so a central server breaks local decisions | Rejected as the core (reuse as an evidence source if already deployed) |
| [Netdata Agent](https://github.com/netdata/netdata) | GPLv3+ (agent). UI and Cloud parts are closed | All-in-one collection, storage, ML and alerts | Fewer moving parts | New features (such as Redfish) aren't long-established. Anomaly scores aren't calibrated failures | Rejected for v1 (possible lab challenger) |
| Central raw-metrics store at Orvex | — | Send all metrics to Orvex | One place to query | Raw data must stay in its cluster (PRIV-1, PRIV-2) | **Rejected by design** |

**Rules and constraints decided with 3.1:**
- Raw metrics stay local by default. Only permitted information leaves, through Nightshift's gateway.
- No extra Grafana deployment is required. [Grafana](https://github.com/grafana/grafana) is AGPL-3.0 core. Customer views are in the Quornex portal.
- [Alertmanager](https://github.com/prometheus/alertmanager) (Apache-2.0) is optional, with **internal receivers only**. An external receiver (Slack, email) would bypass the gateway (SEC-8).

**Evidence:**
- Prometheus local storage "is not clustered or replicated". Recent samples are protected by a write-ahead log replayed on restart. It averages "1-2 bytes per sample". Disk ≈ retention seconds × samples per second × bytes per sample, with retention size kept at no more than 80–85% of the disk. Default retention is 15 days ([Prometheus storage](https://prometheus.io/docs/prometheus/latest/storage/), checked 2026-11-04).
- Latest stable Prometheus release: 3.15.1 (2026-10-21); prerelease 3.16.0-rc.4 (2026-11-03) ([releases](https://github.com/prometheus/prometheus/releases), checked 2026-11-04). The version gets pinned at implementation freeze.
- vmalert runs alerting and recording rules against Prometheus-compatible datasources. Alertmanager is needed only for alert notifications. An Enterprise build exists ([vmalert docs](https://docs.victoriametrics.com/victoriametrics/vmalert/), checked 2026-11-04).

**Illustrative arithmetic (estimate, not sizing):** 100,000 active series every 30 seconds ≈ 3,333 samples per second. At 1–2 bytes per sample, 7 days ≈ 2–4 GB per cluster, before index, WAL and compaction overhead (research, 2026-10-29). The real series count per cluster is unknown.

### Representative benchmark plan (described; running it isn't required for the design challenge)

| Step | What |
|---|---|
| Fixtures | Two disposable test clusters: small (3 nodes) and medium (about 20 nodes) [assumption]. Synthetic series at two levels, for example 50,000 and 200,000 active series [assumption], scraped every 30 s |
| Rules | Nightshift's own rule corpus: the FR-8 predictions (disk filling, memory creep, …) and the fixed evidence queries from catalogue entries |
| Measure | Idle and p95 CPU and memory. Disk use per day. WAL size. Query latency of the fixed queries. Restart and WAL-replay time. Behaviour when the disk fills. Behaviour after a 24-hour disconnection |
| Equivalence | Replay the same recorded data through PromQL (Prometheus) and MetricsQL (VictoriaMetrics + vmalert). Every catalogue query must give the same decision |
| Decision rule | Switch to VictoriaMetrics only if savings exceed a threshold [to set] **and** every catalogue query is equivalent **and** recovery is no worse |

---

## 4. Logs (round 3.2)

| Option | Licence | In plain words | For | Against | Status |
|---|---|---|---|---|---|
| **[Fluent Bit](https://github.com/fluent/fluent-bit)** (collector, per node) | Apache-2.0 | Reads container and system logs, turns the log patterns named in catalogue entries into counts and events, and forwards logs to the local store | Small. Bounded memory and filesystem buffers. Reports dropped records as metrics | Some inputs can lose data when the memory limit is hit. A full buffer discards the oldest chunk | **Provisional default** (2026-11-04) |
| **[VictoriaLogs](https://docs.victoriametrics.com/victorialogs/)** single-node (local store, per cluster) | Apache-2.0 (Enterprise features separate) | A small log database inside the cluster for recent evidence | Time-based retention plus a disk-space cap that drops the oldest days | Goes read-only if the disk actually fills. Unmeasured for our load | **Provisional default** (2026-11-04) |
| [Loki](https://github.com/grafana/loki) | AGPL-3.0 | Log store that indexes labels, not log text | Widely used. **Reuse if Quornex already runs it** | Filesystem storage is described as for development or proof of concept. Needs its own authentication layer | **Alternative**, especially if Quornex already uses it |
| [OTel Collector](https://github.com/open-telemetry/opentelemetry-collector) | Apache-2.0 | General telemetry pipeline | Standard for traces and OTLP | More than node logs need. Some components' stability varies | Rejected as the default (only if OTLP is already in use) |
| [Vector](https://github.com/vectordotdev/vector) | MPL-2.0 | Telemetry pipeline | Powerful transforms | About 256 MiB minimum per disk buffer | Rejected as the default |
| [OpenSearch](https://github.com/opensearch-project/OpenSearch) | Apache-2.0 | Full-text search cluster | Strongest search | Too heavy per cluster (JVM, indexes, replicas) | Rejected |
| Full log store / no log store | — | Keep everything, or nothing | — | Full: the biggest storage cost. None: logs rotate away before diagnosis | Rejected (option b chosen) |

**Rules decided with 3.2 (Amine, 2026-11-04):**
- **Bounded by design:**
  - time-based retention;
  - a bounded storage allocation (a dedicated volume, with the cap kept under 80% of it);
  - ingestion limits per source;
  - bounded collector buffers.
- **At capacity:** behaviour is defined, and dropped evidence is reported clearly. Dropped-record counters feed the monitoring coverage report and every affected explanation ("logs from 02:10–02:14 were dropped at capacity; this explanation may be incomplete").
- **Unfamiliar problems:** recent evidence is kept for problems in neither catalogue (FR-19). The case's time window goes to a separately capped local "case evidence" hold until the case closes.
- **Customer-owned originals are protected.** Nightshift only reads the customer's log files and never modifies or deletes them. Retention and caps apply only to Nightshift's own copies.
- **Outbound allowlists are enforced separately, in the gateway.** The log store has no outbound path.
- **Raw logs stay in the cluster.** Only diagnostic messages built from explicitly allowed fields, with validated values and placeholders for identifying details, may leave through the gateway. External AI also requires customer consent and zero-retention terms. **Cleaning raw logs doesn't make them eligible for export.**

**Evidence (checked 2026-11-04):**
- VictoriaLogs keeps 7 days by default (`-retentionPeriod`). `-retention.maxDiskSpaceUsageBytes` or `-retention.maxDiskUsagePercent` (mutually exclusive) drop old per-day partitions, keeping at least the last two days. If the disk actually fills, it switches to read-only mode, so keep at least 20% free. No explicit ingestion rate limit is documented, only a cap on concurrent inserts ([VictoriaLogs docs](https://docs.victoriametrics.com/victorialogs/)). So ingestion limits must come from the collector.
- Fluent Bit's `mem_buf_limit` pauses an input until chunks flush, and some inputs can lose data then. With filesystem buffering, `storage.total_limit_size` discards the oldest chunk when it is reached ([backpressure](https://docs.fluentbit.io/manual/administration/backpressure)). The dropped, retried and failed counters (`fluentbit_output_dropped_records_total`, `…_retries_failed_total`, `…_errors_total`) are exposed at `/api/v2/metrics/prometheus` ([monitoring](https://docs.fluentbit.io/manual/administration/monitoring)).
- Loki indexes labels only, not log content. It can run as a single binary. Filesystem chunk storage is for "development or proof of concept" ([Loki overview](https://grafana.com/docs/loki/latest/get-started/overview/)).
- **Still to verify before the stack is final:** Fluent Bit's per-source rate-limiting mechanism, and the tail input's behaviour (whether it resumes from its file position or loses lines that rotated away during a pause).

**Unmeasured:** resource costs and search performance for both stores.

### Comparative test (described; two implemented prototypes aren't required)

| Step | What |
|---|---|
| Corpus | One recorded test-log corpus: synthetic app, system and Kubernetes logs, with planted catalogue patterns and fake secrets. Replayed at a normal rate and a burst rate [assumption] |
| Queries | Nightshift's fixed evidence queries from the catalogue entries |
| Measure | CPU, memory and disk per day. Query latency. Behaviour at the retention cap and when the disk fills. Restart time. Dropped-record counts as reported |
| Decide | Keep VictoriaLogs unless Loki is already run by Quornex, or Loki is clearly better on the measured queries |

## 5. Hardware and node signals (round 3.3)

**Design (Amine, 2026-11-04):**
- **One signal interface:** a catalogue mapping from each signal family to its sources per platform. The agent tags every value with source, vantage point, freshness and coverage state, and "unknown" is never healthy.
- **The executor verifies repair evidence independently.** It never relies on the agent's labels.
- **Existing collectors are reused.** Credentialed adapters exist only where credentials are needed.

| Platform | Collectors (reused) | Credentialed adapter | Coverage notes |
|---|---|---|---|
| OMK bare metal | [node_exporter](https://github.com/prometheus/node_exporter), [smartctl_exporter](https://github.com/prometheus-community/smartctl_exporter) (needs root), [node-problem-detector](https://github.com/kubernetes/node-problem-detector) | BMC reader (Redfish; [ipmi_exporter](https://github.com/prometheus-community/ipmi_exporter) fallback): own pod and identity, credentials fetched just in time, read-only BMC accounts where enforced, network access only to the listed BMCs | No BMC access means **reduced hardware coverage** (FR-7), not an unsupported cluster |
| EKS on EC2 | node_exporter; [AWS node monitoring agent](https://github.com/aws/eks-node-monitoring-agent) (Apache-2.0) where supported; node-problem-detector **only for a specific named missing check** | Optional AWS poller (customer-granted), **enabled only after credential isolation is verified** (node IMDS credentials restricted, its own least-privilege identity, a check that other Nightshift components can't obtain its credentials; otherwise disabled and coverage reported as reduced): Pod Identity, minimal `Describe` actions, Region condition, filtered and paginated calls, client-side filtering to its own nodes. Status checks and scheduled events through `DescribeInstanceStatus`. **No Health API** (needs a paid support plan) | No SMART promise on virtual disks. Never acts twice on conditions AWS auto repair handles |
| EKS Fargate | Pod status and probes | — (Pod Identity isn't available on Fargate) | No node collectors (no DaemonSets or privileged pods) |
| EKS Hybrid Nodes | Discovered per cluster | Discovered per cluster | **Not OMK:** customer-managed nodes with an AWS-managed control plane. Actual hardware access and management permissions are discovered |

**Rejected:**
- **Running node-problem-detector and AWS's agent side by side by default:** duplicate collection, and more privileged pods.
- **Depending on the AWS Health API:** it needs a paid support plan.
- **A shared AWS poller:** not until the account layout shows a need.
- **A separate "adapter service" for all signals:** too much complexity for what the existing collectors already provide.

**Evidence (checked 2026-11-04):**
- EC2 `Describe*` calls don't support resource-level permissions ([AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-policies-for-amazon-ec2.html)).
- The Health API needs Business Support+ or higher ([AWS](https://docs.aws.amazon.com/health/latest/ug/health-api.html)).
- EC2 throttling is per account and Region: non-mutating calls refill at 20 per second, unfiltered `DescribeInstanceStatus` at 10 ([AWS](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-throttling.html)).
  - *Illustrative arithmetic, not a capacity limit:* at 1 filtered call per cluster per minute, about 1,200 clusters per account and Region. Real limits depend on calls, pagination, polling bursts and other account activity.
- Pod Identity isn't available on Fargate. Unrestricted IMDS exposes the node role to pods ([AWS](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)). So the poller's separate identity alone would not ensure credential isolation.
- Status checks and scheduled events are covered on the [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html) [docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html). Node agent conditions are covered in the [AWS](https://docs.aws.amazon.com/eks/latest/userguide/node-health-nma.html) docs.

**Not verified:**
- a per-request charge for EC2 `Describe*` calls (none found);
- IRSA on Fargate;
- whether Auto Mode includes the node agent, and whether it runs privileged;
- whether BMCs enforce read-only accounts.

## 6. Observation: remaining round 3 decisions

| Layer | Options compared | Lean |
|---|---|---|
| Independent watchdog | A small custom in-cluster checker; [Healthchecks](https://github.com/healthchecks/healthchecks) (BSD-3-Clause) outside the cluster; [blackbox_exporter](https://github.com/prometheus/blackbox_exporter) (Apache-2.0) | **Decided (Amine, 2026-11-04): a small custom checker** that runs without Prometheus or the agent. Lightweight checks only. A failed probe means "unreachable from the checker", not "dead". Fleet is the outside watchdog. Rejected: a blackbox probe that depends on the same Prometheus, because it can't detect that Prometheus has died |
| Heartbeat path (3.4) | Through the main gateway, or its own tiny fixed-schema path | **Decided (Amine, 2026-11-04): its own path**, sent by the independent checker, with authentication, a fixed destination, rate limits and strict field validation. No logs or arbitrary messages. Status says "gateway health check failed", never "gateway down". The AP-1 checkpoint is added only after its schema and PRD changes are accepted. A shared node or network failure can still break both paths |

## 7. Later rounds (candidates from the research, to compare)

| Layer | Candidates (licence) | Round |
|---|---|---|
| Policy evaluation inside the executor (see section 9) | [OPA](https://github.com/open-policy-agent/opa) (Apache-2.0; standalone server authentication off by default), [Cedar](https://github.com/cedar-policy/cedar) (Apache-2.0) | 4 |
| Outbound fact building and redaction | Custom positive-schema builder; [OTel redaction processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor) (Apache-2.0; logs and metrics alpha); [Presidio](https://github.com/data-privacy-stack/presidio) (MIT). AI redaction is only an extra layer (PRIV-2) | 4 |
| Hosted model access | Direct provider adapters; [LiteLLM OSS](https://github.com/BerriAI/litellm) (MIT; some controls Enterprise) | 4 |
| Local or shared inference | [llama.cpp](https://github.com/ggml-org/llama.cpp) (MIT), [Ollama](https://github.com/ollama/ollama) (MIT), [vLLM](https://github.com/vllm-project/vllm) (Apache-2.0; a shared process doesn't isolate tenants) | 4 |
| AI investigation | [K8sGPT](https://github.com/k8sgpt-ai/k8sgpt), [HolmesGPT](https://github.com/HolmesGPT/holmesgpt) (Bash tools on by default, must be disabled), [kagent](https://github.com/kagent-dev/kagent) (all Apache-2.0) | 4 |
| Release and catalogue delivery | Decided, see section 8 | 5 |
| Fleet transport | Decided, see section 8 | 5 |
| Workload identity, PKI and secrets | [SPIRE](https://github.com/spiffe/spire), [cert-manager](https://github.com/cert-manager/cert-manager) (Apache-2.0); [OpenBao](https://github.com/openbao/openbao), [SOPS](https://github.com/getsops/sops) (MPL-2.0) | 5 and the security review |
| Node fencing | [Medik8s NHC + SNR](https://github.com/medik8s/node-healthcheck-operator) (Apache-2.0); provider-native repair; typed Redfish | 6 (v1: detection and escalation first) |

## 8. Fleet delivery and transport (round 5)

| Layer | Options compared | Decision |
|---|---|---|
| Release and catalogue delivery (5.2) | [Flux](https://github.com/fluxcd/flux2), [Argo CD](https://github.com/argoproj/argo-cd), [Rancher Fleet](https://github.com/rancher/fleet) (all Apache-2.0) | **Flux in each cluster (Amine, 2026-11-05).** Pulls from the cluster; pins OCI artifacts by digest; Cosign or Notation check, which is off by default and is made required ([Flux OCIRepository](https://fluxcd.io/flux/components/source/ocirepositories/), checked 2026-11-05). Rancher Fleet kept only if Quornex already runs it: its agents pull ("the fleet controller does not initiate connections to downstream clusters", [architecture](https://fleet.rancher.io/explanations/architecture)), but signature checks and scale aren't described there. **Rejected: central Argo CD**, which stores every cluster's credentials and connects in ([architecture](https://argo-cd.readthedocs.io/en/stable/operator-manual/architecture/)); its source checks cover Git commits only, "not possible when using Helm or OCI application sources" ([source integrity](https://argo-cd.readthedocs.io/en/stable/user-guide/source-integrity-git-gpg/)) |
| Trust | Rely on the delivery tool, or verify separately | **Separately:** Nightshift checks catalogue, policy and people-list signatures itself. Images are verified on their own, because a signed package doesn't verify every image. Tool to verify (Sigstore policy-controller or Kyverno) |
| Delivery rights | Cluster-admin, or restricted | **Restricted** to Nightshift's namespaces and required objects. CRDs, ClusterRoles and admission webhooks go through a separately authorised install and upgrade path. Exact Flux configuration to verify |
| Cluster-to-Fleet transport (5.3) | HTTPS + local outbox; [NATS JetStream](https://github.com/nats-io/nats-server) (Apache-2.0) | **HTTPS + local outbox (Amine, 2026-11-05):** survives restarts, storage limit, stable message IDs with duplicate detection at the receiver, withdrawals and stops first, privacy checks on every message. NATS not used in v1 (AI's reasoning): one more stateful system to run at Orvex for 10,000 clusters, without a need v1 has shown |
| Correlation and alerting (5.5) | Custom correlation service; [Alertmanager](https://github.com/prometheus/alertmanager) (Apache-2.0); commercial correlation products | **Custom correlation service + Alertmanager (Amine, 2026-11-05).** Alertmanager deduplicates, groups, inhibits, silences and routes, and runs as an HA cluster ([docs](https://prometheus.io/docs/alerting/latest/alertmanager/), checked 2026-11-05). The grouping rules are Nightshift-specific, so correlation itself is custom. Notifications pass the permission and outbound checks. Commercial products were not evaluated |
| AI credentials and usage checks (M2) | Direct calls with per-cluster credentials in account cells; a thin metering proxy at Orvex | **Direct, in cells (Amine, 2026-11-05; design level, unvalidated).** One IAM role and one application inference profile per cluster; content-free usage records and delayed billing per profile ([profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html)). Runtime metrics are documented per model only ([metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/monitoring-runtime-metrics.html)); role sessions are revoked by issue time ([IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html)). No hard per-cluster cap. The proxy is the fallback |

## 9. Intelligence and outbound (round 4, completed 2026-11-15)

| Layer | Options compared | Decision |
|---|---|---|
| Rules vs AI (4.1) | AI-led diagnosis; rules first with optional AI | **Rules first (Amine, 2026-11-04).** Rules and statistics detect, predict and verify catalogue matches; authorisation, safety checks, execution and verification are rules only. Explanations are templates first; AI wording is optional and labelled. Without any AI, unfamiliar problems become "evidence collected, cause unknown, escalated" |
| Outbound fact building (4.2) | Custom positive-schema builder; redaction tools ([OTel redaction processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor), [Presidio](https://github.com/data-privacy-stack/presidio)) as the main protection | **Positive-schema builder (Amine, 2026-11-04):** messages built only from typed, allowlisted fields; no log text leaves. **Rejected as primary protection:** redacting real text (PRIV-2) |
| Hosted provider (4.3 M1) | Anthropic API, OpenAI API, Amazon Bedrock | **Bedrock first (Amine; provisional).** Retention mode `none` is an account setting Bedrock enforces itself ([Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)); Anthropic and OpenAI zero retention rest on approval and contract ([Anthropic](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention), [OpenAI](https://developers.openai.com/api/docs/guides/your-data)), checked 2026-11-04. AI-processing Regions are set per customer; global routing only when permitted (D4, 2026-11-11) |
| Models (D5) | Claude Haiku 4.5 / Sonnet 4.6; newer models | **Haiku 4.5 and Sonnet 4.6 for v1** (Amine, 2026-11-11), subject to availability and zero-retention checks per route; quality validated before relying on them. They run on Anthropic's legacy Bedrock integration (pinned SDK) |
| Call path (4.3 M2) | Direct per-cluster credentials; a metering proxy at Orvex | **Direct, in account cells (design level, unvalidated)**; proxy is the fallback (see section 8) |
| Hosted model access library | Direct provider adapters; [LiteLLM OSS](https://github.com/BerriAI/litellm) (MIT; some controls Enterprise) | **Direct adapter** (one provider in v1); LiteLLM not needed |
| Local inference (4.3 M3) | [llama.cpp](https://github.com/ggml-org/llama.cpp) (MIT), [Ollama](https://github.com/ollama/ollama) (MIT), [vLLM](https://github.com/vllm-project/vllm) (Apache-2.0) | **llama.cpp server, provisional:** supports an API key and listens on 127.0.0.1 by default ([README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)). **Not chosen:** Ollama (built-in authentication not documented in its FAQ); a shared vLLM process (doesn't isolate tenants). No shared GPU and no fine-tuned model in v1 (fine-tuning deferred, not shown uneconomic) |
| AI investigation frameworks | [K8sGPT](https://github.com/k8sgpt-ai/k8sgpt), [HolmesGPT](https://github.com/HolmesGPT/holmesgpt), [kagent](https://github.com/kagent-dev/kagent) (Apache-2.0) | **Not adopted in v1:** the agent is read-only and repairs come only from the signed catalogue; HolmesGPT's Bash tools are on by default |
| Policy evaluation in the executor | [OPA](https://github.com/open-policy-agent/opa), [Cedar](https://github.com/cedar-policy/cedar) (Apache-2.0) | **Not decided:** implementation choice at build (executor checks are fixed by the spine) |
