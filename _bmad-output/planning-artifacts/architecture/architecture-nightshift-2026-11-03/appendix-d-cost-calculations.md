# Appendix D: Cost calculations and sources

Part of the architecture hand-in (2026-11-15). This appendix holds the detail behind the cost summary in §12 of the [architecture document](architecture-orvex.md).

- **Generated numbers:** produced by [`cost-model/cost_model.py`](cost-model/cost_model.py), model **v5**, whose full output is [`cost-model/cost-model-results.md`](cost-model/cost-model-results.md). That output includes a table giving the source of every input.
- **Earlier versions:** kept in [`cost-model/history/`](cost-model/history/).
- **Status of the figures:** estimates under labelled assumptions. Nothing is measured.

## D.1 Prices (verified 2026-11-11, AWS Frankfurt list prices: a reference scenario)

| Item | Price | Used for |
|---|---|---|
| m7i.large (2 vCPU, 8 GiB) | $0.12075 an hour | Capacity unit: 1 vCPU with 4 GiB = $0.060375 an hour = **$44.07 a month** (730 h) |
| EBS gp3 | $0.0952 per GB-month | Disk |
| g6.xlarge (1× NVIDIA L4, 24 GB) | $1.0064 an hour | EKS GPU options |
| EKS cluster fee, NLB, S3, data transfer, KMS | see `.working/round8-prices-aws.md` | Fleet costs |
| SMS and voice | see `.working/round8-prices-messaging-ai.md` | Notifications |
| Claude Haiku 4.5 on Bedrock, regional | $1.10 input / $5.50 output per million tokens | Hosted AI (round 4 token model) |

## D.2 How a footprint becomes a dollar figure

1. **Size each component** at the **midpoint** of its research envelope (research §9: initial benchmark envelopes, a 3-node reference cluster with about 100,000 metric series). Components the research doesn't cover are mapped to the nearest envelope and marked as mapped or as a placeholder.
2. **Add up vCPU and GiB.** The capacity needed is the larger of **total vCPU** and **total GiB ÷ 4**, because capacity must fit both CPU and memory. In every scenario here, CPU is the larger.
3. **Price it:** capacity units × $44.07, plus disk GB × $0.0952.
4. **The result is an indicative value**, meaning what the capacity would cost if bought as cloud capacity. It is **not a bill**.

## D.3 The monitoring that runs anyway (baseline, not charged to Nightshift)

The baseline assumes a managed cluster runs one monitoring stack whether or not Nightshift is present. Base scenario: 10 nodes.

| Component | vCPU range (midpoint) | GiB range (midpoint) | Source |
|---|---|---|---|
| Node collectors (node_exporter, NPD, log agent, optional SMART), per node | 0.05–0.30 (0.175) | 0.15–0.50 (0.325) | research §9 |
| Prometheus, one replica | 0.2–1.0 (0.6) | 0.5–2.0 (1.25) | research §9 |
| Alertmanager, kube-state-metrics, probes | 0.05–0.25 (0.15) | 0.15–0.5 (0.325) | research §9. Its envelope also covered a checker; v5 leaves the whole envelope in the baseline |
| Log storage (VictoriaLogs) | 0.1–0.5 (0.3) | 0.25–1.0 (0.625) | research §9, "local Loki/service storage" envelope |
| Disk: Prometheus samples 3 GB + logs 7 GB + spool 1.25 GB per node | 22.5 GB | | research §9 |

**Total:** 2.80 vCPU and 5.45 GiB, which comes to 2.80 units × $44.07 + 22.5 GB × $0.0952 = **$125.55** (indicative).

## D.4 What Nightshift adds (the customer increment)

| Component | vCPU (midpoint) | GiB | Value | Source |
|---|---|---|---|---|
| Agent (reader) | 0.55 | 0.625 | $24.24 | mapped to the research's "optional investigation worker" |
| Flux, **only if not already installed** | 0.15 | 0.375 | $6.61 | research §9 |
| Independent checker | 0.125 | 0.3125 | $5.51 | **PLACEHOLDER**: mapped to the controller envelope. In v4 it sat inside the baseline row; v5 moves it here |
| Executor | 0.125 | 0.3125 | $5.51 | research §9, controller + policy + outbox |
| Gateway and outbox | 0.125 | 0.3125 | $5.51 | mapped to the controller envelope |
| Audit service, rollback guard, local dashboard | 0.125 | 0.3125 | $5.51 | **PLACEHOLDER**: one controller envelope |
| BMC reader (OMK) or AWS poller (EKS) | 0.055 | 0.09 | $2.42 | research §9 (BMC); AWS poller mapped |
| **Extra load on the shared monitoring stack** | 0.21 | 0.44 | $9.26 | **PLACEHOLDER**: 20% of Prometheus, Alertmanager/kube-state-metrics/probes, and log storage |
| Disk for audit and outbox | | | $0.19 (2 GB) | **PLACEHOLDER** |
| **Increment** | **1.465** | **2.78** | **$64.76** | |

**The reuse calculation:**
- **No double counting:** the cluster runs one monitoring stack in both cases, so its cost isn't counted again for Nightshift.
- **The extra load:** Nightshift queries Prometheus and the log store, and alerts through Alertmanager. That extra use is assumed to be 20% of those three components' size, a placeholder to measure. The per-node collectors get no extra load.
- **Flux:** if the customer already runs Flux, its $6.61 drops out.

**Across the scenarios:** the increment is $19.05 (low: 0.43 vCPU) and $110.66 (high: 2.50 vCPU).

**v4 compared with v5:**
- **v4:** compared a full Nightshift-plus-monitoring stack ($176) with monitoring alone ($126), and counted the checker inside the baseline.
- **v5:**
  - moves the checker into Nightshift's increment;
  - reports the increment directly ($64.76, up from v4's $59.25 reuse figure);
  - no longer shows the $176 standalone figure as a customer cost.

## D.5 Actual spending versus indicative value

| Situation | What the customer actually pays |
|---|---|
| Spare capacity in existing nodes or servers | No new server or node. Power, cooling, storage and network for the extra load are still real costs and **not estimated** (missing: measured power per vCPU, the customer's network prices). On EKS, Nightshift's disk is real spending |
| No spare capacity, EKS | Whole-node steps. For example, one m7i.large is about $88 a month at list price. Larger clusters or the high scenario may need more |
| No spare capacity, OMK | Buying or reallocating hardware; the price is unknown |

## D.6 Orvex's cost

**Orvex's cost** = engineers + Nightshift's share of Fleet + network egress + SMS and calls + hosted AI tokens. With in-cluster AI there are no tokens.

**Engineers:**
- **How many:** the larger of (a) someone on duty at all hours and (b) incident hands-on hours plus catalogue and release work, done by the same engineers.
- **Productive hours:** 1,760 a year, a placeholder.
- **Engineer cost:** $100,000 a year, illustrative, with $50,000 and $130,000 shown.

**The baseline:**
- **Coverage:** the same coverage, with existing runbooks and automation.
- **Self-healing:** Kubernetes and AWS self-healing credited equally on both sides.
- **Handling time:** the same per task. Without prepared repairs, each Orvex-scope problem is investigated and, if it's a supported one, repaired by hand.
- **Supported is not automatic:** the supported share (95 / 90 / 80%) is kept separate from the share resolved with no Orvex person.

| Base, per cluster per month | 100 clusters | 10,000 clusters |
|---|---|---|
| Orvex cost with Nightshift, hosted AI | $422 | $10.81 |
| Orvex cost without Nightshift | $422 | $48.75 |
| Orvex saving | −$0.62 | $37.94 (fleet: about $379,000 a month, $4.55 million a year) |
| Saving at $50,000 / $130,000 a year | about −$0.62 | $18.83 / $49.41 |

**At 10,000 clusters across the scenarios:** $20.45 (low), $37.94 (base) and $64.76 (high).

**Combined cost** (Orvex plus customer, with the customer at indicative value) at 10,000 clusters, base: $75.57 with Nightshift against $48.75 without.

## D.7 AI hardware options (per cluster that uses one, base)

| Option | Per month | Inputs |
|---|---|---|
| Existing spare L4-class 24 GB | $7.88 | 72 W (verified) × 40% average load × PUE 1.5 × $0.25 per kWh |
| Existing spare consumer 24 GB | $38.33 | 350 W (placeholder), same factors |
| New 24 GB (~$1,000, Danny) | $94.44 | $1,000 / 36 months + power + $20 host share + 10% a year maintenance |
| New 96 GB (~$10,000 Danny; ~$14–16k listings) | $557 | $12,500 (middle of the range) / 36 + 600 W power + $40 host share + maintenance |
| EKS g6.xlarge, always on | $735 | $1.0064 × 730 h |
| EKS g6.xlarge, on demand | $30.27 | 1 hour a day warm (placeholder) + about 0.075 h of work |
| One model server per customer | $184 | g6.xlarge always on ÷ 4 clusters |

The load, PUE, electricity price, host shares and maintenance rate are **placeholders**. The 24 GB and 96 GB prices are Danny's hypotheses; a $1,000 24 GB card has not been verified.

## D.8 The final summary table (§12)

**Combined estimate** = Orvex operating cost (cash) + the customer increment ($64.76, an indicative value) + the AI option's model-host and GPU cost.

**The Orvex cost differs by AI option:**
- **Hosted AI:** Orvex's cost includes the tokens ($0.02).
- **Every in-cluster row:** Orvex's cost excludes them ($422.26 at 100 clusters and $10.79 at 10,000, rounded in the table).

**Avoiding double counting:**
- **EKS GPU instances:** the rental already covers the instance's CPU, RAM and power, so nothing is added for them.
- **Existing-GPU row:** GPU power only (72 W × 40% × PUE 1.5 × $0.25 per kWh), a partial cost; its combined figure is an incomplete subtotal.
- **New-GPU rows:** they include a placeholder host share ($20 or $40) for the host server.

**Arithmetic check:** `cost_model.py` (`final_summary_rows`) builds each combined figure as the sum of its three parts. On 2026-11-15 a separate check confirmed that sum for every row at both scales.
