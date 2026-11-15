"""Nightshift cost model (round 8). Reproducible: `python3 cost_model.py > cost-model-results.md`.

Every usage figure is an UNVALIDATED ASSUMPTION (Amine, 2026-11-11). Prices are AWS Frankfurt
(eu-central-1) on-demand list prices checked 2026-11-11, used only as a labelled comparison basis;
they do not establish Fleet's real hosting cost. Sources: ../.working/round8-prices-aws.md,
../.working/round8-prices-messaging-ai.md, ../.working/round4-ai-token-costs.md.
"""

H = 730  # hours per month

# ---------- Verified prices (USD, 2026-11-11) ----------
VCPU_EQ_HR = 0.12075 / 2   # m7i.large: 1 vCPU-equivalent = 1 vCPU + 4 GiB
EBS_GB_MO = 0.0952          # gp3
S3_GB_MO = 0.0245
EGRESS_GB = 0.09            # first 10 TB tier (used flat: slightly high above 10 TB)
EKS_HR = 0.10
NLB_HR, NLCU_HR = 0.027, 0.006
KMS_KEY_MO, KMS_SIGN_10K = 1.0, 0.15
HSM_HR = 1.92
G6_XL_HR = 1.0064           # 1x NVIDIA L4 24 GB
L4_WATTS = 72

# ---------- Scenario assumptions (low / base / high = low / base / high COST) ----------
# Every input says where it comes from. "NO SOURCE" = AI placeholder, to be set by Amine.
S = ["low", "base", "high"]
SRC = {}
def inp(key, values, source):
    SRC[key] = (values, source); return values

A = {
    "nodes": inp("nodes", [3, 10, 30], "Round 8 K3 (Amine accepted as unvalidated); research §9 uses 3 nodes as reference"),
    "problems_day_10k": inp("problems_day_10k", [250, 500, 1000], "Round 4 (Amine): 500 a day starting assumption; PRD NFR-1: about 250 a night, up to 500 on a bad night"),
    "auto_share": inp("auto_share", [0.95, 0.90, 0.80], "Round 4 supported share 95/90/80% (Amine), read as 'handled automatically'; PRD SM-8/SM-9 staffing arithmetic assumes 90%"),
    "min_per_person_problem": inp("min_per_person_problem", [20, 20, 20], "PRD SM-8: 20 minutes for each problem needing a person (Codex arithmetic, brief addendum)"),
    "tokens_per_cluster_mo": inp("tokens_per_cluster_mo", [0.007, 0.023, 0.125], "Round 4 token costs, Haiku 4.5 regional (Amine accepted)"),
    "approvals_day_10k": inp("approvals_day_10k", [50, 150, 400], "NO SOURCE (AI placeholder)"),
    "approvers_per_approval": inp("approvers_per_approval", [1.2, 1.5, 2.0], "NO SOURCE (AI placeholder); PRD FR-21: some repairs need two approvals"),
    "resend_factor": inp("resend_factor", [1.1, 1.2, 1.5], "NO SOURCE (AI placeholder)"),
    "alert_sms_day_10k": inp("alert_sms_day_10k", [20, 100, 300], "NO SOURCE (AI placeholder)"),
    "sms_price": inp("sms_price", [0.012, 0.07, 0.11], "Verified prices: US ~$0.012, UK $0.05, FR $0.074, DE $0.107 (round8-prices-messaging-ai.md); country mix NO SOURCE"),
    "calls_day_10k": inp("calls_day_10k", [5, 20, 50], "NO SOURCE (AI placeholder)"),
    "call_min": inp("call_min", [1, 2, 3], "NO SOURCE (AI placeholder)"),
    "call_price_min": inp("call_price_min", [0.014, 0.04, 0.38], "Verified Twilio prices US $0.014, DE-from-EEA $0.042, DE standard $0.376"),
    "releases_mo": inp("releases_mo", [1, 2, 4], "NO SOURCE (AI placeholder)"),
    "release_gb": inp("release_gb", [0.5, 1.0, 1.0], "NO SOURCE (AI placeholder)"),
    "reports_gb_mo": inp("reports_gb_mo", [0.02, 0.05, 0.2], "NO SOURCE (AI placeholder); research §9: 1 KiB heartbeat a minute ≈ 1.5 MB a month"),
    "report_retention_mo": inp("report_retention_mo", [13, 13, 13], "NO SOURCE (AI placeholder)"),
    "fleet_nodes_xl": inp("fleet_nodes_xl", [1.5, 3, 6], "NO SOURCE (AI placeholder); research §9: shared watchdog + database 0.2-1 core, 0.5-2 GiB initially, 10k capacity unverified"),
    "clusters_per_fleet_vcpu": inp("clusters_per_fleet_vcpu", [500, 250, 125], "NO SOURCE (AI placeholder)"),
    "fleet_db_gb": inp("fleet_db_gb", [200, 500, 1000], "NO SOURCE (AI placeholder)"),
    "status_signs_per_cluster_hr": inp("status_signs_per_cluster_hr", [0.25, 1, 2], "Round 6 D6: fresh tier needs a relay status statement within 1 hour"),
    "kms_key_versions": inp("kms_key_versions", [6, 10, 20], "Round 5.1: five signing keys; versions NO SOURCE"),
    "nightshift_team_fte": inp("nightshift_team_fte", {100: [1, 2, 3], 10000: [3, 5, 8]}, "NO SOURCE (AI placeholder): catalogue, two reviewers per entry, releases; brief addendum: estimate Nightshift team and support separately"),
    "baseline_tooling_fte": inp("baseline_tooling_fte", {100: [0.5, 1, 1.5], 10000: [2, 3, 5]}, "NO SOURCE (AI placeholder)"),
}
STRESS = {"auto_share": 0.60, "min": 45, "source": "Brief addendum / PRD SM-8: 60% handled automatically at 45 minutes each"}
MANUAL_FACTOR = 1.0  # main case: equal handling time with and without Nightshift (Amine). 1.5 = unvalidated sensitivity.
ENGINEER = {"illustrative": 100_000, "low": 50_000, "high": 130_000}  # Amine, modelling assumptions
PRODUCTIVE_H_YR = 1760   # NO SOURCE (AI placeholder: about 220 working days x 8 h)
COVERAGE_FTE = 8760 / PRODUCTIVE_H_YR  # PRD SM-8: one engineer on duty at night -> someone on duty around the clock ≈ 5 FTE

# Footprint envelopes (vCPU low-high, GiB low-high) from research §9 (initial benchmark envelopes, 3-node, ~100k series).
# Base = midpoint. Components research doesn't cover are mapped to the nearest envelope, marked "mapped (AI)".
SERVICES = {
    "Prometheus, one replica": ((0.2, 1.0), (0.5, 2.0), "research §9"),
    "Alertmanager + kube-state-metrics + probes/independent checker": ((0.05, 0.25), (0.15, 0.5), "research §9"),
    "executor (controller + policy + outbox)": ((0.05, 0.2), (0.125, 0.5), "research §9"),
    "gateway + outbox": ((0.05, 0.2), (0.125, 0.5), "mapped (AI) to the controller envelope"),
    "agent (reader)": ((0.1, 1.0), (0.25, 1.0), "mapped (AI) to 'optional investigation worker'"),
    "audit service + rollback guard + local dashboard": ((0.05, 0.2), (0.125, 0.5), "NO SOURCE: mapped (AI) to one controller envelope"),
    "Flux controllers, if newly needed": ((0.05, 0.25), (0.15, 0.6), "research §9"),
    "BMC exporter (OMK) / AWS poller (EKS)": ((0.01, 0.1), (0.03, 0.15), "research §9 (BMC); AWS poller mapped (AI)"),
    "log storage (VictoriaLogs)": ((0.1, 0.5), (0.25, 1.0), "research §9 'local Loki/service storage' envelope"),
}
PER_NODE = ((0.05, 0.30), (0.15, 0.50), "research §9: node_exporter + NPD + log agent + optional SMART, per node")
MONITORING_ONLY = {"Prometheus, one replica", "Alertmanager + kube-state-metrics + probes/independent checker",
                   "log storage (VictoriaLogs)"}  # what a manual baseline would still run
# Disk per cluster (GB): research §9: Prometheus samples 2-4 GB for 7 days (index/WAL extra); logs 1 GB/day raw x 7 days;
# per-node log spool 0.5-2 GB. Audit and outbox: NO SOURCE (AI placeholder 1/2/5 GB).
def disk_gb(i, baseline=False):
    prom = [2, 3, 4][i]; logs = 7; spool = [0.5, 1.25, 2][i] * A["nodes"][i]; own = 0 if baseline else [1, 2, 5][i]
    return prom + logs + spool + own
EXTRA_LOAD_ON_EXISTING_MONITORING = 0.2  # NO SOURCE (AI placeholder)


def pick(rng, i):
    lo, hi = rng
    return [lo, (lo + hi) / 2, hi][i]


def vcpu_eq_cost(vcpu, gib):
    """Capacity must fit both CPU and memory: price max(vCPU, GiB/4) vCPU-equivalents."""
    return max(vcpu, gib / 4) * VCPU_EQ_HR * H


def footprint(i, baseline=False):
    sv = [v for k, v in SERVICES.items() if not baseline or k in MONITORING_ONLY]
    vc = sum(pick(v[0], i) for v in sv)
    gb = sum(pick(v[1], i) for v in sv)
    n = A["nodes"][i]
    vc += n * pick(PER_NODE[0], i)
    gb += n * pick(PER_NODE[1], i)
    disk = disk_gb(i, baseline)
    return vc, gb, disk, vcpu_eq_cost(vc, gb) + disk * EBS_GB_MO


def footprint_reuse(i):
    """Customer already runs suitable monitoring: add only Nightshift's own components plus extra load."""
    full_vc, full_gb, full_disk, _ = footprint(i)
    base_vc, base_gb, base_disk, _ = footprint(i, baseline=True)
    mon = [v for k, v in SERVICES.items() if k in MONITORING_ONLY]
    extra_vc = sum(pick(v[0], i) for v in mon) * EXTRA_LOAD_ON_EXISTING_MONITORING
    extra_gb = sum(pick(v[1], i) for v in mon) * EXTRA_LOAD_ON_EXISTING_MONITORING
    vc, gb, disk = full_vc - base_vc + extra_vc, full_gb - base_gb + extra_gb, full_disk - base_disk
    return vc, gb, disk, vcpu_eq_cost(vc, gb) + disk * EBS_GB_MO


def fleet_monthly(i, n, baseline=False):
    core = A["fleet_nodes_xl"][i] * 4 * VCPU_EQ_HR * H + EKS_HR * H + NLB_HR * H + 5 * NLCU_HR * H
    if baseline:
        return core + A["fleet_db_gb"][i] * EBS_GB_MO * 0.5
    scale = (n / A["clusters_per_fleet_vcpu"][i]) * VCPU_EQ_HR * H
    storage = A["fleet_db_gb"][i] * EBS_GB_MO + n * A["reports_gb_mo"][i] * A["report_retention_mo"][i] * S3_GB_MO
    signs = n * A["status_signs_per_cluster_hr"][i] * H
    signing = A["kms_key_versions"][i] * KMS_KEY_MO + signs / 10_000 * KMS_SIGN_10K
    return core + scale + storage + signing


def staffing(i, n, eng, baseline=False, auto=None, minutes=None):
    """Human hours = problems needing a person x minutes (PRD SM-8 arithmetic). FTE = max(round-the-clock
    duty cover, hours / productive hours). Customer/provider hardware work: not estimated (no source)."""
    auto = A["auto_share"][i] if auto is None else auto
    minutes = A["min_per_person_problem"][i] if minutes is None else minutes
    probs = A["problems_day_10k"][i] * n / 10_000
    if baseline:
        hours = probs * minutes * MANUAL_FACTOR / 60
        other_fte = A["baseline_tooling_fte"][n][i]
    else:
        hours = probs * (1 - auto) * minutes / 60
        other_fte = A["nightshift_team_fte"][n][i]
    incident_fte = max(COVERAGE_FTE, hours * 365 / PRODUCTIVE_H_YR)
    return {"incident_fte": incident_fte, "other_fte": other_fte, "hours_day": hours,
            "orvex_mo": (incident_fte + other_fte) * eng / 12}


def messaging(i, n, baseline=False):
    f = n / 10_000
    approvals = 0 if baseline else A["approvals_day_10k"][i] * A["approvers_per_approval"][i] * A["resend_factor"][i]
    sms = (approvals + A["alert_sms_day_10k"][i]) * f * 30
    calls = A["calls_day_10k"][i] * f * 30 * A["call_min"][i] * A["call_price_min"][i]
    return sms * A["sms_price"][i] + calls, sms


def network(i, n):
    gb = A["releases_mo"][i] * A["release_gb"][i]
    return n * (gb + 0.05) * EGRESS_GB, gb + A["reports_gb_mo"][i] + 0.05


def model(n, i, eng=ENGINEER["illustrative"], baseline=False, auto=None, minutes=None):
    vc, gb, disk, t1 = footprint(i, baseline)
    t2 = 0 if baseline else A["tokens_per_cluster_mo"][i]
    t3 = fleet_monthly(i, n, baseline) / n
    t4_orvex, cust_gb = network(i, n)
    t4 = t4_orvex / n
    t5_total, sms_count = messaging(i, n, baseline)
    t5 = t5_total / n
    st = staffing(i, n, eng, baseline, auto, minutes)
    h = st["orvex_mo"] / n
    tech = t1 + t2 + t3 + t4 + t5
    return dict(vc=vc, gb=gb, disk=disk, t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, tech=tech,
                h=h, total=tech + h, cust_gb=cust_gb, sms=sms_count,
                hours_day=st["hours_day"],
                inc_fte=st["incident_fte"], other_fte=st["other_fte"])


# ---------- GPU variants (per cluster that uses one, per month; T2 replacement) ----------
def gpu_variants():
    kwh = [0.15, 0.25, 0.35]; pue = 1.5; avg_load = 0.4; months = 36
    out = []
    for i, s in enumerate(S):
        def power(w):
            return w * avg_load * H / 1000 * pue * kwh[i]
        out.append((s, {
            "existing spare 24 GB datacenter GPU (L4-class, 72 W): power only": power(L4_WATTS),
            "existing spare 24 GB consumer GPU (~350 W, assumption): power only": power(350),
            "new 24 GB consumer GPU (~$1,000, Danny): 36-month amortisation + power + host share $20 + maintenance 10%/yr":
                1000 / months + power(350) + 20 + 1000 * 0.10 / 12,
            "new 96 GB GPU ($10,000 Danny / $15,000 Codex listing): amortisation + power (~600 W, assumption) + host share $40 + maintenance":
                [10_000, 12_500, 15_000][i] / months + power(600) + 40 + [10_000, 12_500, 15_000][i] * 0.10 / 12,
            "EKS g6.xlarge (L4) always on": G6_XL_HR * H,
            "EKS g6.xlarge started on demand (0.15 unfamiliar problems/month x 0.5 h, plus 1 h/day warm window)":
                G6_XL_HR * (0.075 + [0, 30, 60][i]),
            "one model server per customer (g6.xlarge always on / 4 clusters per customer)": G6_XL_HR * H / 4,
        }))
    return out


def money(x):
    return f"${x:,.2f}" if x < 100 else f"${x:,.0f}"


def cash_split(n, i, eng=ENGINEER["illustrative"], baseline=False):
    r = model(n, i, eng, baseline)
    orvex = r["t2"] + r["t3"] + r["t4"] + r["t5"] + r["h"]
    return r, orvex


def cash_split_args(n, baseline):
    r = model(n, 1, baseline=baseline, auto=STRESS["auto_share"], minutes=STRESS["min"])
    return r["t2"] + r["t3"] + r["t4"] + r["t5"] + r["h"]


def print_sources():
    print("## Where every input comes from\n")
    print("| Input | low / base / high | Source |\n|---|---|---|")
    for k, (v, src) in SRC.items():
        print(f"| {k} | {v} | {src} |")
    for k, (c, g, src) in SERVICES.items():
        print(f"| footprint: {k} | {c[0]}-{c[1]} vCPU, {g[0]}-{g[1]} GiB | {src} |")
    print(f"| footprint per node | {PER_NODE[0][0]}-{PER_NODE[0][1]} vCPU, {PER_NODE[1][0]}-{PER_NODE[1][1]} GiB | {PER_NODE[2]} |")
    print("| disk | Prometheus 2/3/4 GB + logs 7 GB + spool 0.5/1.25/2 GB per node + audit/outbox 1/2/5 GB | research §9; audit/outbox NO SOURCE |")
    print(f"| productive hours a year | {PRODUCTIVE_H_YR} | NO SOURCE (AI placeholder) |")
    print(f"| round-the-clock duty cover | {COVERAGE_FTE:.1f} FTE | PRD SM-8 (one on night duty), arithmetic 8,760 / {PRODUCTIVE_H_YR} |")
    print("| engineer cost | $100k (50k / 130k) | Amine, modelling assumption |")
    print("| reuse extra load | 20% | NO SOURCE (AI placeholder) |")
    print()


def print_scale(n):
    print(f"## {n:,} clusters, hosted AI (main approach), engineer ${ENGINEER['illustrative']:,}/yr, equal handling time\n")
    print("| Per cluster per month | " + " | ".join(S) + " |\n|---|---|---|---|")
    r = [model(n, i) for i in range(3)]
    b = [model(n, i, baseline=True) for i in range(3)]
    rows = [("T1 in-cluster footprint, standalone (customer)", "t1"), ("T2 hosted AI tokens (Orvex)", "t2"),
            ("T3 Nightshift share of Fleet (Orvex)", "t3"), ("T4 network egress (Orvex)", "t4"),
            ("T5 SMS and calls (Orvex)", "t5"), ("H Orvex engineers", "h")]
    for label, k in rows:
        print(f"| {label} | " + " | ".join(money(x[k]) for x in r) + " |")
    print("| **Orvex cash: Nightshift** | " + " | ".join(money(x['t2']+x['t3']+x['t4']+x['t5']+x['h']) for x in r) + " |")
    print("| **Orvex cash: baseline** | " + " | ".join(money(x['t2']+x['t3']+x['t4']+x['t5']+x['h']) for x in b) + " |")
    print("| **Customer footprint: Nightshift standalone** (EKS: cash for capacity; OMK: allocated value of existing hardware) | " + " | ".join(money(x['t1']) for x in r) + " |")
    print("| **Customer footprint: baseline monitoring** | " + " | ".join(money(x['t1']) for x in b) + " |")
    print("| **Customer footprint: Nightshift reusing existing monitoring** (incremental) | " + " | ".join(money(footprint_reuse(i)[3]) for i in range(3)) + " |")
    print("| Customer/provider hardware work | not estimated (no source) | | |")
    print("| Human hours a day needing a person (fleet): Nightshift / baseline | " + " | ".join(f"{x['hours_day']:.1f} / {y['hours_day']:.1f}" for x, y in zip(r, b)) + " |")
    print("| Orvex FTE: incident seats + Nightshift team | " + " | ".join(f"{x['inc_fte']:.1f} + {x['other_fte']:.1f}" for x in r) + " |")
    print("| Orvex FTE baseline: incident seats + tooling | " + " | ".join(f"{x['inc_fte']:.1f} + {x['other_fte']:.1f}" for x in b) + " |")
    print("| Footprint resources standalone (vCPU / GiB / GB disk) | " + " | ".join(f"{x['vc']:.2f} / {x['gb']:.1f} / {x['disk']:.0f}" for x in r) + " |")
    print("| Customer-side traffic (GB/month) | " + " | ".join(f"{x['cust_gb']:.2f}" for x in r) + " |")
    print("| SMS messages per month (whole fleet) | " + " | ".join(f"{x['sms']:,.0f}" for x in r) + " |")
    print()


if __name__ == "__main__":
    import sys
    print("# Cost model results (round 8, generated by cost_model.py)\n")
    print("All usage numbers are unvalidated assumptions. Prices: AWS Frankfurt list prices, 2026-11-11, a comparison basis only. Savings and break-even hold only **under these assumptions**.\n")
    for n in (100, 10_000):
        print_scale(n)
    print("## Sensitivities (base scenario, Orvex cash per cluster per month)\n")
    print("| Case | 100: Nightshift | 100: baseline | 10,000: Nightshift | 10,000: baseline |\n|---|---|---|---|---|")
    def row(label):
        v = [cash_split(n, 1, baseline=bl)[1] for n in (100, 10_000) for bl in (False, True)]
        print(f"| {label} | " + " | ".join(money(x) for x in v) + " |")
    row("Equal handling time (main case)")
    MANUAL_FACTOR = 1.5; row("Unvalidated: manual handling 1.5x longer (30 vs 20 min)"); MANUAL_FACTOR = 1.0
    for e in (ENGINEER["low"], ENGINEER["high"]):
        v = [cash_split(n, 1, e, bl)[1] for n in (100, 10_000) for bl in (False, True)]
        print(f"| Engineer ${e:,}/yr | " + " | ".join(money(x) for x in v) + " |")
    v = [cash_split_args(n, bl) for n in (100, 10_000) for bl in (False, True)]
    print(f"| PRD stress case: {int(STRESS['auto_share']*100)}% automatic at {STRESS['min']} min (equal time for baseline) | " + " | ".join(money(x) for x in v) + " |")
    print()
    print_sources()
    print("## AI variants: replaces T2 for a cluster that uses it (per cluster per month)\n")
    print("Boundary for every row: hardware or instance, power, hosting share and hardware maintenance. **Excluded everywhere:** staff time to run and update models, evaluation, spares, and the customer's own server. Capability is **not** equivalent: a 24 GB card runs smaller models than hosted Haiku or Sonnet, and quality is untested (PRD: compare local and hosted on the same cases).\n")
    print("Sources: L4 72 W and g6.xlarge $1.0064/h verified; Danny's $1,000 / 24 GB and $10,000 / 96 GB are his hypotheses (a $1,000 24 GB card is not verified); 96 GB cards listed at $14,080-16,000 (brief addendum, Codex). **NO SOURCE (AI placeholders):** consumer card 350 W, 96 GB card 600 W, 40% average load, PUE 1.5, electricity $0.15/0.25/0.35 per kWh, host share $20/$40, maintenance 10% a year, the 1 h/day warm window. GPU start-up delay is unverified.\n")
    print("| Variant | " + " | ".join(S) + " |\n|---|---|---|---|")
    gv = gpu_variants()
    for k in gv[0][1]:
        print(f"| {k} | " + " | ".join(money(v[k]) for _, v in gv) + " |")
    print("| Hosted tokens, Haiku 4.5 regional (round 4) | " + " | ".join(money(x) for x in A["tokens_per_cluster_mo"]) + " |")
    print("| No AI | $0 | $0 | $0 |")
