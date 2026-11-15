# Party challenge of 4.3 (hosted provider, call path, local and shared models), 2026-11-04

Requested by Amine. The room: Winston (architecture), Vex (security), Moss (operations). **Nothing here changes the architecture until Amine decides.** The personas' claimed experience is not operational evidence.

## Verified facts (checked 2026-11-04)

| # | Fact | Source |
|---|---|---|
| V1 | Anthropic ZDR: approved via sales, per organisation. Prompts and responses aren't stored at rest after the response. Batch and Files aren't covered. Claude Fable 5/5.1 and Mythos 5/5.1 require 30-day retention unless expressly authorised | [Anthropic](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) |
| V2 | OpenAI: not used for training by default. Abuse logs up to 30 days. ZDR by prior approval. Batches and Files ineligible | [OpenAI](https://developers.openai.com/api/docs/guides/your-data) |
| V3 | Bedrock: a retention mode per account (or project) per Region. `none` writes nothing to durable storage and shares nothing with the provider, and requests to models that need retention are blocked. An organisation policy (SCP) can force `none`. Each model lists its `allowed_modes`, which can be checked through the API | [Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html) |
| V4 | Bedrock inference is limited by per-account, per-Region token quotas. Increases aren't automatic | [Bedrock quotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas.html) |
| V5 | Ollama binds 127.0.0.1:11434 by default. Its FAQ doesn't describe built-in authentication | [Ollama FAQ](https://docs.ollama.com/faq) |
| V6 | llama.cpp server supports `--api-key` (default: none) and listens on 127.0.0.1 by default | [llama.cpp server](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) |
| V7 | A shared vLLM process doesn't isolate tenants (shared scheduling and caches). Its API-key option protects only some routes | research 2026-10-29, verification.md |

## Findings

| # | Topic | Finding |
|---|---|---|
| C1 | Provider | Decide the **required properties** first, then which provider v1 tests first. The required properties: enforceable or verifiable zero retention, no training, region and jurisdiction per customer, a pinned model that is ZDR-eligible, a contract with Orvex |
| C2 | Provider | Bedrock's `none` mode is the only zero retention among the three that Nightshift can **check itself** (V3): read the account mode and the model's `allowed_modes` before use, and refuse otherwise. Anthropic and OpenAI rest on approval and contract (V1, V2) |
| C3 | Sovereignty | Orvex sells "sovereign" private cloud. Some OMK customers may refuse a US hyperscaler or provider even with an EU Region. The consent screen must name the actual provider, Region and jurisdiction (PRIV-8). A customer who refuses gets an in-cluster model or no AI |
| C4 | Scale | Bedrock token quotas are per account and Region, and increases aren't automatic (V4). A bad night (500 problems) concentrates calls. Quotas must be sized and tested. The core loop works without AI anyway |
| C5 | Direct calls | Short-lived per-cluster credentials vended by Fleet: a compromised cluster can spend Orvex's tokens or flood the provider. The gateway must enforce local budgets, report usage counts in Fleet reports, and Fleet stops vending tokens to a cluster over budget. A compromised Fleet can vend tokens but can't see the content |
| C6 | Relay | A relay puts sanitised content through Orvex: one more party that must keep nothing and be audited, and a new channel to assign under PRIV-9. It is also a central hot path at 10,000 clusters (outage means no AI for anyone, though the core loop continues) |
| C7 | Local model | The local endpoint must be reachable only from the agent (network rules) and authenticated (llama.cpp `--api-key`, V6). Ollama's default listening address is local and its auth isn't documented (V5). Model weights are signed and distributed like releases (SEC-5) |
| C8 | Shared GPU | One model server per customer, never one shared process (V7). Not built in v1. The cost model only |

## Decisions for Amine (material to privacy, safety or cost)

- **M1, provider strategy:** the C1 required properties, plus Bedrock as the first adapter (zero retention checked before every use), with Anthropic direct as a second adapter where Bedrock lacks the model or Region. The consent screen names the provider, Region and jurisdiction.
- **M2, call path:** direct from the cluster's gateway, with short-lived per-cluster credentials, local budgets and Fleet stopping over-budget clusters. Or a relay at Orvex.
- **M3, local and shared:** an in-cluster runtime only where the hardware exists and the customer wants it (llama.cpp server with an API key and network rules, one pinned signed model). No shared GPU in v1.

## Disagreements

- **Provider:** Moss wants two providers from day one (quota and outage resilience). Vex wants one (fewer contracts and less to audit). Winston: one adapter interface, Bedrock first, the second adapter when a real gap appears.
- **Call path:** Vex accepts direct only with per-cluster budgets enforced *both* locally and by Fleet's token vending. Moss is fine with local budgets alone.
