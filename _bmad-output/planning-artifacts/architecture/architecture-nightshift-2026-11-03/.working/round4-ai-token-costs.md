# Round 4.4: AI token costs (working estimate, 2026-11-04)

**AI token costs only.** These are not Nightshift's operating costs: telemetry, Fleet services, SMS, catalogue engineering and human time come in round 8. Every usage number below is an assumption, not a measurement.

## Prices (checked 2026-11-04)

| Model | Global endpoint (input / output per MTok) | Regional endpoint (+10%) | Blended at 80/20, regional |
|---|---|---|---|
| Claude Haiku 4.5 | $1 / $5 | $1.10 / $5.50 | **$1.98 per MTok** |
| Claude Sonnet 4.6 | $3 / $15 | $3.30 / $16.50 | **$5.94 per MTok** |

- **Source:** Anthropic's [pricing page](https://platform.claude.com/docs/en/about-claude/pricing). It lists the base prices, and says that for Haiku 4.5 and later models, Bedrock's **regional endpoints** ("guaranteed data routing through specific geographic regions") carry a **10% premium over global endpoints**.
- **Regional pricing is used,** because global routing can break a customer's region requirement.
- **To confirm:** the exact price for the chosen AWS Region on [AWS's Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) (its price table couldn't be read by the tool); that the model is available in that Region; and that it is ZDR-eligible there (`none` in its allowed modes). AWS says Claude models released before Fable 5 had no retention change ([Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)).
- **The 80/20 input/output split is an assumption** (Amine, from Codex).

## Assumptions

| Input | Low | Baseline | High |
|---|---|---|---|
| Problems per day, fleet of 10,000 (NFR-1: ~250 a night; 500 a day is a starting assumption) | 250 | 500 | 1,000 |
| Supported problems (the rest are unfamiliar, so the two add up to 100%) | 95% | 90% | 80% |
| Supported problems that need AI wording (templates first, per 4.1) | 10% | 30% | 60% |
| AI calls per such problem (about 1.8k tokens each) | 1 | 2 | 4 |
| Unfamiliar problems (FR-19) | 5% | 10% | 20% |
| AI calls per unfamiliar problem (about 9k tokens each) | 2 | 3 | 5 |
| Customers (assumed average of 4 clusters per customer) | 2,500 | 2,500 | 2,500 |
| Morning summaries (one per customer per day) written by AI | 10% | 20% | 50% |
| Tokens per AI summary | 3.5k | 3.5k | 3.5k |
| Retries | +5% | +10% | +25% |
| Customers with external-AI consent | 100% (upper bound; the real share is a cost-model input) | 100% | 100% |

At 100 clusters, the same rates per cluster apply (25 customers, about 5 problems a day). That assumes the same incident rate per cluster, which is an assumption too.

## Results

| Scenario | Tokens per month (10,000 clusters) | Haiku 4.5, 10,000 clusters | Sonnet 4.6, 10,000 clusters | Haiku, 100 clusters | Sonnet, 100 clusters | Per cluster per month (Haiku / Sonnet) |
|---|---|---|---|---|---|---|
| Low | ~36 M | ~$71 | ~$214 | ~$0.71 | ~$2.14 | $0.007 / $0.021 |
| Baseline | ~118 M | ~$234 | ~$703 | ~$2.34 | ~$7.03 | $0.023 / $0.070 |
| High | ~631 M | ~$1,250 | ~$3,749 | ~$12.50 | ~$37.49 | $0.125 / $0.375 |

- **Baseline arithmetic per day:**
  - 135 supported problems × 2 calls × 1.8k tokens;
  - 50 unfamiliar problems × 3 calls × 9k;
  - 500 summaries × 3.5k;
  - in total about 3.59 M tokens, plus 10% retries, ≈ 3.94 M a day, ≈ 118 M a month.
- **Amine's earlier figure:** 35k tokens per cluster per month at global prices gives $0.063 (Haiku) and $0.189 (Sonnet). At regional prices it would be $0.069 and $0.208. The revised baseline is about 11.8k tokens per cluster per month, because templates come first and summaries are counted per customer.

## Code fixes (separate)

- **Per attempt** (assumed 50k input + 5k output tokens on Sonnet 4.6, regional): about $0.25.
- **Per fix** (assumed 3 attempts): about $0.74.
- **Volume:** unknown (opt-in and experimental), so no monthly total is given.

## Corrections (Amine, 2026-11-05)

- **Supported vs unfamiliar.** The supported share is now the complement of the unfamiliar share: 95 / 90 / 80%. Earlier it was 90% in every scenario, so low and high counted problems twice or left some out. The baseline is unchanged.
- **In-cluster GPU.** Local inference is optional, used when a customer has suitable resources. The cost model doesn't assume every cluster needs a newly purchased GPU.
