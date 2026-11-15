# Round 8 Cost model: structure and assumptions (proposal, 2026-11-11, not decided)

AI proposal for Amine. Prices are being verified against primary sources; no totals until they are in. Every usage number is an assumption.

## What the PRD requires
- **COST-1:** two numbers per cluster per month, at 100 and 10,000 clusters: **technical cost** (AI or GPU, monitoring compute and storage, network, Nightshift's share of Fleet) and **total operating cost** (plus human time).
- **COST-2:** full GPU costs (electricity, hosting, maintenance, replacement).
- **COST-3:** count resources on customer hardware, and separate what the customer pays from what Orvex pays.
- **COST-4:** a "without Nightshift" baseline.
- **COST-5/6:** as low as realistic, without becoming slower or less reliable.

## K1 Cost lines and who pays

| Line | What | Paid by | Scales with |
|---|---|---|---|
| T1 In-cluster footprint | Agent, gateway, executor, checker, audit, rollback guard; Prometheus, VictoriaLogs, Fluent Bit; node_exporter on each node | **Customer** (their cluster) | Clusters, nodes per cluster |
| T2 AI | Hosted tokens (round 4), **or** an in-cluster GPU, **or** one model server per customer, **or** none | Orvex (hosted); customer (their GPU) | Problems, customers |
| T3 Fleet | Fleet services compute, storage (reports, audit checkpoints), Alertmanager, registry, relay, signing system | **Orvex** | Partly fixed, partly per cluster |
| T4 Network | Heartbeats, reports, release and catalogue downloads | Orvex (egress) | Clusters × releases |
| T5 Notifications | SMS for option B approvals and alerts; phone calls for urgent alerts | Orvex | Approvals, urgent incidents |
| H1 Nightshift team | Catalogue work, reviews (two per entry), releases, on-call | Orvex | Mostly fixed, steps with scale |
| H2 Escalations | Incidents Nightshift doesn't resolve, × minutes per incident × engineer cost | Orvex | **The uncertain share** (K3) |
| B Baseline | Engineers needed to run the same clusters by hand | — | Clusters per engineer without Nightshift |

## K2 Reference prices
- **EKS and Fleet:** AWS list prices in one reference Region (eu-central-1, on-demand). Discounts (Savings Plans) are noted, not assumed.
- **OMK:** the customer's own hardware. T1 is shown **in resources** (vCPU, GB RAM, GB disk) plus an **indicative** dollar figure at cloud-equivalent prices, labelled as such.
- **Fleet hosting:** Orvex's real provider is an assumption; AWS prices are a stand-in.

## K3 Scenario assumptions (low / baseline / high)

| Input | Low | Baseline | High |
|---|---|---|---|
| Nodes per cluster | 3 | 10 | 30 |
| Problems per day, fleet of 10,000 (round 4) | 250 | 500 | 1,000 |
| **Share of incidents resolved without a person** *(unknown: failure types ≠ incidents, Amine 2026-11-11)* | 60% | 40% | 20% |
| Engineer minutes per escalated incident | 15 | 30 | 60 |
| Fully loaded engineer cost per year | to set with Amine | | |
| Approvals per day needing SMS (fleet of 10,000) | 50 | 150 | 400 |
| Releases per month (download size about 1 GB each) | 1 | 2 | 4 |

The "high" column means high **cost**: so the share resolved is lowest there.

## K4 AI variants to price
1. **Hosted** (main approach): round 4 token cost (+ SMS and Fleet unchanged).
2. **In-cluster GPU, customer-owned** (only where the customer wants it): an L4-class card amortised over 3 years + power + hosting + maintenance (COST-2). Not every cluster: shown per cluster that uses one.
3. **In-cluster GPU on EKS:** a GPU instance running all the time (g6.xlarge or g5.xlarge), or only during working hours (cheaper, but slower answers at night, which COST-6 forbids).
4. **Shared GPU:** one model server per customer (never one shared process), shared by that customer's clusters.
5. **No AI:** tokens zero; same everything else.
6. **Fine-tuned small model** (round 4 follow-up): training once + always-on serving; rejected for v1, shown for comparison.

## Output
For each AI variant: a table with **technical** and **total operating** cost per cluster per month at 100 and 10,000 clusters, split customer-paid vs Orvex-paid, plus the without-Nightshift baseline and the main cost drivers.
