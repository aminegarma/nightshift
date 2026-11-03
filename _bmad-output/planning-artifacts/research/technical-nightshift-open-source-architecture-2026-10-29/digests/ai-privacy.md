# AI investigation, detection, privacy, and inference digest

Evidence retrieved 2026-10-29 from official project documentation and GitHub. Recommendations below are architectural inferences, not upstream guarantees or measured Nightshift capacity. No source establishes safe operation or throughput at 10,000 clusters.

## Recommended boundary

Keep collection, raw logs, event bodies, object manifests, identifiers, and investigation evidence inside the customer cluster. Build a deterministic evidence service that emits a versioned, size-bounded fact schema: approved metric aggregates, normalized failure codes, time windows, pseudonymous object references, and evidence IDs. Hosted inference receives only explicitly allowlisted facts after validation; arbitrary strings, raw log excerpts, labels, annotations, URLs, and model-generated follow-up queries must not bypass this boundary. Local inference may access richer evidence through the same bounded interface, but privacy mode must be enforced by network policy and endpoint configuration, not a prompt.

Treat logs and all tool results as attacker-controlled data. The model proposes hypotheses and references evidence IDs; it cannot run shell commands, kubectl, code, arbitrary HTTP, arbitrary SQL/PromQL, MCP discovery, or remediation. Fixed queries execute in trusted code with scope, time, row, byte, and timeout limits. Validate generated output and display uncertainty. This design is a recommendation prompted by the broad tool surfaces below, not a claim that any compared framework implements it automatically.

## Investigation engines: two direct candidates and one broader alternative

| Candidate | Verified OSS role and license | Nightshift fit and caveat |
| --- | --- | --- |
| HolmesGPT | Apache-2.0 SRE investigation project; integrations and alert investigation are documented. | Stronger candidate for multi-source investigation evaluation. Use only explicitly enabled fixed toolsets behind the evidence boundary; default configuration violates the no-shell requirement. |
| K8sGPT | Apache-2.0 cluster scanning and diagnostic analyzers, with hosted and local model providers. | Better bounded baseline for Kubernetes issue extraction; analyzer results are observations, not proven root causes. Evaluate the non-LLM analyzer path first and control what explanation requests transmit. |
| kagent | Apache-2.0 Kubernetes-native framework for deploying/managing agents. | Broader orchestration platform rather than a drop-in bounded RCA engine. Adds controller, CRD, agent and tool lifecycle responsibilities; defer unless Nightshift needs this platform independently. |

These roles and licenses come from [HolmesGPT](https://github.com/HolmesGPT/holmesgpt), [K8sGPT](https://github.com/k8sgpt-ai/k8sgpt), and [kagent](https://github.com/kagent-dev/kagent). HolmesGPT's general README read-only language must not be interpreted as absence of command execution: its current [Bash documentation](https://holmesgpt.dev/latest/data-sources/builtin-toolsets/bash/) explicitly enables shell tooling by default, supports command approval, and persists approved prefixes. Disable bash entirely for Nightshift; allow/deny command prefixes alone do not meet the requested boundary.

Maintenance snapshot: [HolmesGPT releases](https://github.com/HolmesGPT/holmesgpt/releases) show 0.45.0 on October 15; [K8sGPT releases](https://github.com/k8sgpt-ai/k8sgpt/releases) show v0.4.39 on September 14, including anonymization and security dependency fixes. [kagent releases](https://github.com/kagent-dev/kagent/releases) show v1.0.0-alpha17 on October 21 and v0.10.4 the same day; v0.10.4 explicitly lacks CLI artifacts. Release activity supports active maintenance, not maturity equivalence. Pin tested complete releases, never blindly follow the latest tag. HolmesGPT [cross-cluster tools](https://holmesgpt.dev/0.43.0/data-sources/cross-cluster-tools/) require the Robusta platform and matching versions; do not count this as standalone OSS fleet functionality.

## Detection and prediction: rules first; separately evaluate learned signals

| Option | What is actually available | Recommendation and validation gap |
| --- | --- | --- |
| Deterministic alert rules and linear extrapolation | Prometheus `predict_linear` extrapolates float gauges using simple linear regression; it is not a general incident predictor. | Initial production path for explicit conditions such as disk exhaustion. Require suitable windows, minimum history, reset/deployment handling, and alert persistence. |
| PyOD or River worker | PyOD provides anomaly detectors and a fit/predict API; River provides incremental learning plus anomaly, drift, and time-series modules. | Experimental, per-signal service with bounded state, not an autonomous predictor. River fits incremental adaptation; PyOD fits offline detector comparisons. Neither supplies Nightshift's feature pipeline, labels, alert policy, or operational calibration. |

The [Prometheus function reference](https://prometheus.io/docs/prometheus/latest/querying/functions/) restricts `predict_linear` to gauges. [PyOD](https://github.com/yzhao062/pyod) is BSD-2-Clause; [River](https://github.com/online-ml/river) is BSD-3-Clause, with its module inventory in the [River API](https://riverml.xyz/latest/api/overview/). Current releases show [PyOD 3.6.7](https://github.com/yzhao062/pyod/releases) on October 12 (input validation and estimator-contract maintenance) and [River 0.26.1](https://github.com/online-ml/river/releases) on August 21. Both are maintained libraries, not a turnkey fleet prediction system. PyOD's new agent workflow is unnecessary for Nightshift; use explicit estimator code only.

Evaluate against a seasonal naive baseline and deterministic rules using time-ordered replay, incident-level precision/recall, false alerts per cluster-day, lead time, missing data and concept drift. Shadow learned alerts before exposing them. An anomaly score is neither probability of failure nor evidence of causation; forecasting estimates need horizon and error reporting. Do not promise predictive accuracy before representative telemetry and incident labels exist.

## Privacy controls: complementary options, neither a guarantee

| Option | Evidence | Practical boundary |
| --- | --- | --- |
| OpenTelemetry redaction processor | Deletes non-allowlisted attributes and masks blocked values. Current status is beta traces, alpha logs and metrics. | Useful structured telemetry minimization before storage/export; not a general proof that free-text bodies and every sensitive identifier are safe. Test each signal and field. |
| Presidio | MIT SDK for configurable PII detection/anonymization across structured/unstructured data. | Optional in-cluster second pass for free text. Requires domain recognizers, NLP assets, evaluation and operational ownership; false negatives and false positives remain. |

The [OTel processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/redactionprocessor) defines the actual field handling and stability. [Presidio](https://github.com/data-privacy-stack/presidio) now redirects from the Microsoft repository to data-privacy-stack; its [FAQ](https://presidio.dataprivacystack.org/faq/) explicitly disclaims finding all sensitive information. [Presidio releases](https://github.com/data-privacy-stack/presidio/releases) show 2.2.366 on October 27 as a security release with dependency and image changes. Treat ownership movement, runtime/model compatibility, and security updates as deployment checks.

Recommendation: outbound positive-schema selection is mandatory; redaction is defense in depth. Fail closed on schema or policy errors. Keep raw evidence, pseudonym mappings, traces of model prompts/responses, gateway debug logs, and crash reports local; disabling one logging callback is insufficient. Test secret canaries, emails, customer IDs, encoded strings, nested attributes and hostile instructions. Customer-controlled egress destinations and explicit hosted/local configuration must be visible and auditable.

## Provider access: direct adapters versus LiteLLM OSS

Direct adapters minimize dependencies and deployment surface when supporting a small fixed provider set, but Nightshift must own retries, quota enforcement, request normalization, structured-output differences, and compatibility tests. This is an engineering tradeoff, not a separate OSS product claim.

[LiteLLM](https://github.com/BerriAI/litellm) offers broad provider normalization, routing and a self-hosted gateway. Its [license](https://github.com/BerriAI/litellm/blob/main/LICENSE) is MIT outside `enterprise/`, which has separate terms. The [edition matrix](https://docs.litellm.ai/docs/enterprise) lists virtual keys, budgets/rate limits, spend tracking and load balancing in OSS; SSO/SCIM, audit logs and delegated organization administration are Enterprise features, with limited SSO exceptions. Do not make enterprise controls an OSS architecture dependency. A gateway forwarding to a hosted provider still sends request content outside the cluster; self-hosting the gateway does not change that fact.

[Version support](https://docs.litellm.ai/docs/enterprise/version_support) covers only four recent stable minor lines with roughly weekly minors and no separate LTS track. [Releases](https://github.com/BerriAI/litellm/releases) show stable patches such as v1.106.6 alongside v1.108 RC and v1.109 dev tags. This creates a meaningful patch/test burden. Prefer direct adapters initially; add the OSS gateway when multi-provider routing and shared quotas justify its service, datastore, keys, logging configuration and upgrade ownership. Either option sits after fact validation and has no access to raw telemetry or tools.

## Local inference: vLLM versus llama.cpp, with Ollama packaging alternative

| Option | License and deployment role | Resource/security tradeoff |
| --- | --- | --- |
| vLLM | Apache-2.0 serving engine. | Candidate for dedicated accelerator pools and concurrent inference. Hardware, kernels, model architecture, quantization and context support need a tested compatibility matrix. More distributed runtime surface if scaling across nodes. |
| llama.cpp | MIT C/C++ inference/server, quantized GPU and CPU support, compatible APIs and batching. | Candidate for smaller installations or CPU/GPU split; quality, latency and concurrency must be benchmarked on the selected quantization and hardware. It also provides tool-use APIs, which Nightshift must not expose as executable capabilities. |
| Ollama | MIT local runtime and model management. | Convenient operator packaging for local installations; configure local-only mode and pre-provision approved weights. Cloud features are distinct and must be disabled in strict local mode. |

Licenses and roles: [vLLM repository](https://github.com/vllm-project/vllm), [llama.cpp repository](https://github.com/ggml-org/llama.cpp), [Ollama repository](https://github.com/ollama/ollama). Runtime licenses do not license the model weights: separately review each exact model, tokenizer, adapter, redistribution conditions and acceptable-use restrictions.

The [llama.cpp server reference](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) documents quantization, CPU/GPU support, context/cache and batching controls. [Ollama FAQ](https://docs.ollama.com/faq) documents CPU/GPU placement, context settings, model downloads, loopback binding and `OLLAMA_NO_CLOUD=1`. Local inference avoids hosted prompt transfer only when those local endpoints are actually selected and outbound networking is denied; model downloads should be a separate approved provisioning path.

[vLLM security guidance](https://docs.vllm.ai/en/latest/usage/security/) says inter-node communication is insecure by default and that one server process is not a tenant isolation boundary. Isolate networks and tenant deployments, authenticate the API, protect caches, and avoid shared untrusted Ray access. Pin trusted model artifacts and avoid remote model code. Bound request tokens, concurrency and output length; disable unneeded media fetching/endpoints. These are operational requirements, not guarantees from a local runtime.

Maintenance snapshot: [vLLM v0.32.0](https://github.com/vllm-project/vllm/releases) October 18; [llama.cpp](https://github.com/ggml-org/llama.cpp/releases) lists frequent build prereleases including b11982 October 29 and a v0.8.0 tag; [Ollama v0.40.13](https://github.com/ollama/ollama/releases) October 28. Continuous release activity requires pinning and regression tests rather than auto-upgrades.

Capacity remains unverified. Budget weight memory plus KV cache, runtime overhead and concurrent contexts; GPU VRAM alone is not a deployment specification. Measure actual prompt lengths, output limits, concurrent investigations, queue delay, cold starts, OOM behavior, CPU fallback and failure isolation. A small quantized local model may have poorer RCA reasoning or schema fidelity than a hosted model; the evidence contract and evaluation set must be shared across modes. Local GPUs consume power and operations time even when incident demand is bursty. No fixed GPU count or 10,000-cluster claim is defensible from these project pages.
