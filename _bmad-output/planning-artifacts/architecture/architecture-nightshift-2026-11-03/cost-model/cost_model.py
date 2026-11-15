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
# Every input says where it comes from. "PLACEHOLDER" = AI placeholder, to be set by Amine.
S = ["low", "base", "high"]
SRC = {}
def inp(key, values, source):
    SRC[key] = (values, source); return values

A = {
    "nodes": inp("nodes", [3, 10, 30], "Round 8 K3 (Amine accepted as unvalidated); research §9 uses 3 nodes as reference"),
    "problems_day_10k": inp("problems_day_10k", [250, 500, 1000], "Round 4 (Amine): 500 a day starting assumption; PRD NFR-1: about 250 a night, up to 500 on a bad night"),
    "supported_share": inp("supported_share", [0.95, 0.90, 0.80], "Round 4 (Amine): share of problems the catalogue SUPPORTS. Supported is not automatic: a supported problem may still need customer approval, Orvex technical approval or manual work"),
    "tokens_per_cluster_mo": inp("tokens_per_cluster_mo", [0.007, 0.023, 0.125], "Round 4 token costs, Haiku 4.5 regional (Amine accepted)"),
    "approvals_day_10k": inp("approvals_day_10k", [50, 150, 400], "PLACEHOLDER"),
    "approvers_per_approval": inp("approvers_per_approval", [1.2, 1.5, 2.0], "PLACEHOLDER; PRD FR-21: some repairs need two approvals"),
    "resend_factor": inp("resend_factor", [1.1, 1.2, 1.5], "PLACEHOLDER"),
    "alert_sms_day_10k": inp("alert_sms_day_10k", [20, 100, 300], "PLACEHOLDER"),
    "sms_price": inp("sms_price", [0.012, 0.07, 0.11], "Verified prices: US ~$0.012, UK $0.05, FR $0.074, DE $0.107 (round8-prices-messaging-ai.md); country mix PLACEHOLDER"),
    "calls_day_10k": inp("calls_day_10k", [5, 20, 50], "PLACEHOLDER"),
    "call_min": inp("call_min", [1, 2, 3], "PLACEHOLDER"),
    "call_price_min": inp("call_price_min", [0.014, 0.04, 0.38], "Verified Twilio prices US $0.014, DE-from-EEA $0.042, DE standard $0.376"),
    "releases_mo": inp("releases_mo", [1, 2, 4], "PLACEHOLDER"),
    "release_gb": inp("release_gb", [0.5, 1.0, 1.0], "PLACEHOLDER"),
    "reports_gb_mo": inp("reports_gb_mo", [0.02, 0.05, 0.2], "PLACEHOLDER; research §9: 1 KiB heartbeat a minute ≈ 1.5 MB a month"),
    "report_retention_mo": inp("report_retention_mo", [13, 13, 13], "PLACEHOLDER"),
    "fleet_nodes_xl": inp("fleet_nodes_xl", [1.5, 3, 6], "PLACEHOLDER; research §9: shared watchdog + database 0.2-1 core, 0.5-2 GiB initially, 10k capacity unverified"),
    "clusters_per_fleet_vcpu": inp("clusters_per_fleet_vcpu", [500, 250, 125], "PLACEHOLDER"),
    "fleet_db_gb": inp("fleet_db_gb", [200, 500, 1000], "PLACEHOLDER"),
    "status_signs_per_cluster_hr": inp("status_signs_per_cluster_hr", [0.25, 1, 2], "Round 6 D6: fresh tier needs a relay status statement within 1 hour"),
    "kms_key_versions": inp("kms_key_versions", [6, 10, 20], "Round 5.1: five signing keys; versions PLACEHOLDER"),
}
MANUAL_FACTOR = 1.0  # equal handling time with and without Nightshift (Amine)
ENGINEER = {"illustrative": 100_000, "low": 50_000, "high": 130_000}  # Amine, modelling assumptions

# ---------- Staffing inputs ----------
# Work types (Amine, 2026-11-11): approval-only, investigation, manual repair. Only hands-on minutes count;
# waiting (for a customer, for a repair to run) is not workload. Proportions are unknown -> PLACEHOLDER + sensitivity.
W = {
    "self_heal": (0.20, "PLACEHOLDER: share of problems Kubernetes/AWS self-healing resolves with no person; credited equally in BOTH cases"),
    "orvex_scope": (0.70, "PLACEHOLDER: share of remaining problems in Orvex's managed-software scope; the rest is customer/provider work (hardware, customer apps)"),
    "auto_of_supported": (0.70, "PLACEHOLDER: share of supported Orvex-scope problems repaired with no Orvex person (safe ticked repairs, agreed policy, customer-approved)"),
    "manual_of_supported": (0.05, "PLACEHOLDER: share of supported Orvex-scope problems needing manual repair (e.g. FR-52 dangerous repairs)"),
    "manual_of_unsupported": (0.5, "PLACEHOLDER: share of unsupported (unfamiliar) Orvex-scope problems that also need a manual repair after investigation"),
    "approval_min": ((5, 10), "Amine: 5-10 minutes for approval-only work, illustrative"),
    "investigation_min": (30, "PLACEHOLDER: hands-on minutes to diagnose and choose what to do"),
    "manual_min": (30, "PLACEHOLDER: hands-on minutes for a person to perform a repair"),
    "customer_min": (30, "PLACEHOLDER: customer/provider hands-on minutes per problem in their scope"),
    "grouping": (1.0, "PLACEHOLDER: work multiplier for related incidents handled together (1.0 = none; FR-32 grouping justifies <1 only for fleet-wide events); applied to BOTH cases"),
}
PRD_AVG = {"auto": 0.90, "min": 20, "source": "PRD SM-8: 90% handled automatically, 20 minutes each for the rest (Codex arithmetic, brief addendum); unvalidated"}
PRD_STRESS = {"auto": 0.60, "min": 45, "source": "Brief addendum / PRD SM-8: 60% automatic, 45 minutes each; unvalidated"}
PRODUCTIVE_H_YR = 1760   # PLACEHOLDER: 52 weeks x 40 h = 2,080 h, minus about 320 h of leave, holidays and training
NIGHT_SHARE = 0.5        # derived: PRD NFR-1 "about 250 a night" of round 4's 500 a day
NIGHT_SHIFT_H = 12       # PLACEHOLDER: length of the night duty
# Coverage (PRD SM-8): one engineer on duty at night, 2-3 backups on call from home (standby, not staffed hours).
# Daytime: the same team works normal hours. "Someone on duty at all times" = 8,760 h / productive hours.
COVERAGE_FTE = 8760 / PRODUCTIVE_H_YR
CATALOGUE_FTE = {100: [1, 2, 3], 10000: [3, 5, 8]}   # PROVISIONAL: catalogue, two reviewers per entry, releases
BASELINE_TOOLING_FTE = {100: [0.5, 1, 1.5], 10000: [2, 3, 5]}  # PROVISIONAL: runbooks and tooling without Nightshift

# Footprint envelopes (vCPU low-high, GiB low-high) from research §9 (initial benchmark envelopes, 3-node, ~100k series).
# Base = midpoint. Components research doesn't cover are mapped to the nearest envelope, marked "mapped (AI)".
SERVICES = {
    "Prometheus, one replica": ((0.2, 1.0), (0.5, 2.0), "research §9"),
    "Alertmanager + kube-state-metrics + probes": ((0.05, 0.25), (0.15, 0.5), "research §9 (its envelope also covered a checker; the baseline keeps all of it)"),
    "independent checker (Nightshift)": ((0.05, 0.2), (0.125, 0.5), "PLACEHOLDER: mapped (AI) to the controller envelope; v5 moved it out of the baseline row"),
    "executor (controller + policy + outbox)": ((0.05, 0.2), (0.125, 0.5), "research §9"),
    "gateway + outbox": ((0.05, 0.2), (0.125, 0.5), "mapped (AI) to the controller envelope"),
    "agent (reader)": ((0.1, 1.0), (0.25, 1.0), "mapped (AI) to 'optional investigation worker'"),
    "audit service + rollback guard + local dashboard": ((0.05, 0.2), (0.125, 0.5), "PLACEHOLDER: mapped (AI) to one controller envelope"),
    "Flux controllers, if newly needed": ((0.05, 0.25), (0.15, 0.6), "research §9"),
    "BMC exporter (OMK) / AWS poller (EKS)": ((0.01, 0.1), (0.03, 0.15), "research §9 (BMC); AWS poller mapped (AI)"),
    "log storage (VictoriaLogs)": ((0.1, 0.5), (0.25, 1.0), "research §9 'local Loki/service storage' envelope"),
}
PER_NODE = ((0.05, 0.30), (0.15, 0.50), "research §9: node_exporter + NPD + log agent + optional SMART, per node")
MONITORING_ONLY = {"Prometheus, one replica", "Alertmanager + kube-state-metrics + probes",
                   "log storage (VictoriaLogs)"}  # what a manual baseline would still run
# Disk per cluster (GB): research §9: Prometheus samples 2-4 GB for 7 days (index/WAL extra); logs 1 GB/day raw x 7 days;
# per-node log spool 0.5-2 GB. Audit and outbox: PLACEHOLDER (AI placeholder 1/2/5 GB).
def disk_gb(i, baseline=False):
    prom = [2, 3, 4][i]; logs = 7; spool = [0.5, 1.25, 2][i] * A["nodes"][i]; own = 0 if baseline else [1, 2, 5][i]
    return prom + logs + spool + own
EXTRA_LOAD_ON_EXISTING_MONITORING = 0.2  # PLACEHOLDER


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
    """Customer incremental footprint (v5): the cluster runs ONE monitoring stack either way (baseline), so only
    Nightshift's own components are added, plus an assumed extra load (PLACEHOLDER 20%) on the three shared
    monitoring components Nightshift queries and alerts through: Prometheus, Alertmanager + kube-state-metrics +
    probes, and log storage. Per-node collectors are not loaded extra. Existing monitoring is not counted again."""
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


def wv(k, w):
    return w.get(k, W[k][0])


def human_hours(i, n, baseline=False, w=None, simple=None):
    """Hands-on hours a day. Returns (orvex_hours, customer_hours, breakdown).
    simple = {"auto":..., "min":...} reproduces the PRD single-average scenarios (no work-type split)."""
    w = w or {}
    probs = A["problems_day_10k"][i] * n / 10_000
    g = wv("grouping", w)
    if simple:
        need = probs if baseline else probs * (1 - simple["auto"])
        h = need * simple["min"] * MANUAL_FACTOR / 60 * g
        return h, 0.0, {"PRD single average": h}
    rem = probs * (1 - wv("self_heal", w))
    orv, cust = rem * wv("orvex_scope", w), rem * (1 - wv("orvex_scope", w))
    sup = A["supported_share"][i]
    appr = wv("approval_min", w); appr = appr if isinstance(appr, (int, float)) else sum(appr) / 2
    inv, man = wv("investigation_min", w), wv("manual_min", w)
    # BASELINE RULE (equal handling time): without Nightshift there is no prepared repair, so every Orvex-scope
    # problem is investigated (investigation_min) and supported ones are also repaired by hand (manual_min).
    if baseline:  # no prepared repair: every Orvex-scope problem is investigated; supported ones also repaired by hand
        bd = {"investigation": orv * inv, "manual repair": orv * sup * man}
    else:
        s_orv = orv * sup
        auto, manual = wv("auto_of_supported", w), wv("manual_of_supported", w)
        bd = {"approval-only": s_orv * (1 - auto - manual) * appr,
              "manual repair": s_orv * manual * man + orv * (1 - sup) * wv("manual_of_unsupported", w) * man,
              "investigation": orv * (1 - sup) * inv}
    bd = {k: v / 60 * g * (MANUAL_FACTOR if baseline else 1) for k, v in bd.items()}
    return sum(bd.values()), cust * wv("customer_min", w) / 60 * g, bd


def staffing(i, n, eng, baseline=False, w=None, simple=None):
    """FTE = max(cover, work). Work = incident hands-on hours + catalogue/release (or tooling) hours, done by the
    SAME engineers (no double counting). Cover = someone on duty at all hours (PRD SM-8)."""
    oh, ch, bd = human_hours(i, n, baseline, w, simple)
    other = (BASELINE_TOOLING_FTE if baseline else CATALOGUE_FTE)[n][i]
    work_fte = oh * 365 / PRODUCTIVE_H_YR + other
    fte = max(COVERAGE_FTE, work_fte)
    night_h = oh * NIGHT_SHARE
    return {"fte": fte, "work_fte": work_fte, "incident_fte": oh * 365 / PRODUCTIVE_H_YR, "other_fte": other,
            "orvex_hours_day": oh, "customer_hours_day": ch, "breakdown": bd,
            "night_hours": night_h, "night_people": max(1.0, night_h / NIGHT_SHIFT_H),
            "orvex_mo": fte * eng / 12}


def messaging(i, n, baseline=False):
    f = n / 10_000
    approvals = 0 if baseline else A["approvals_day_10k"][i] * A["approvers_per_approval"][i] * A["resend_factor"][i]
    sms = (approvals + A["alert_sms_day_10k"][i]) * f * 30
    calls = A["calls_day_10k"][i] * f * 30 * A["call_min"][i] * A["call_price_min"][i]
    return sms * A["sms_price"][i] + calls, sms


def network(i, n):
    gb = A["releases_mo"][i] * A["release_gb"][i]
    return n * (gb + 0.05) * EGRESS_GB, gb + A["reports_gb_mo"][i] + 0.05


def model(n, i, eng=ENGINEER["illustrative"], baseline=False, w=None, simple=None):
    vc, gb, disk, t1 = footprint(i, baseline)
    t2 = 0 if baseline else A["tokens_per_cluster_mo"][i]
    t3 = fleet_monthly(i, n, baseline) / n
    t4_orvex, cust_gb = network(i, n)
    t4 = t4_orvex / n
    t5_total, sms_count = messaging(i, n, baseline)
    t5 = t5_total / n
    st = staffing(i, n, eng, baseline, w, simple)
    h = st["orvex_mo"] / n
    tech = t1 + t2 + t3 + t4 + t5
    return dict(vc=vc, gb=gb, disk=disk, t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, tech=tech,
                h=h, total=tech + h, cust_gb=cust_gb, sms=sms_count,
                st=st)


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


def customer_increment(i):
    vc, gb, disk, value = footprint_reuse(i)
    return {"vcpu": vc, "gib": gb, "disk_gb": disk, "value": value}


def node_steps(vcpu, gib, node_vcpu=2, node_gib=8, node_price=0.12075 * H):
    """Example only: whole m7i.large nodes needed if NO spare capacity exists (ignores allocatable overhead)."""
    import math
    nodes = max(math.ceil(vcpu / node_vcpu), math.ceil(gib / node_gib))
    return nodes, nodes * node_price


def money(x):
    sign = "-" if x < 0 else ""
    x = abs(x)
    return sign + (f"${x:,.2f}" if x < 100 else f"${x:,.0f}")


def orvex_cash(r):
    return r["t2"] + r["t3"] + r["t4"] + r["t5"] + r["h"]


def print_sources():
    print("## Where every input comes from\n")
    print("| Input | low / base / high | Source |\n|---|---|---|")
    for k, (v, src) in SRC.items():
        print(f"| {k} | {v} | {src} |")
    for k, (v, src) in W.items():
        print(f"| staffing: {k} | {v} | {src} |")
    print(f"| PRD average scenario | {PRD_AVG['auto']:.0%} automatic, {PRD_AVG['min']} min | {PRD_AVG['source']} |")
    print("| baseline rule | without Nightshift: every Orvex-scope problem investigated; supported ones also repaired by hand; same minutes as with Nightshift | Amine: equal handling time |")
    print(f"| PRD stress scenario | {PRD_STRESS['auto']:.0%} automatic, {PRD_STRESS['min']} min | {PRD_STRESS['source']} |")
    print(f"| productive hours a year | {PRODUCTIVE_H_YR} | PLACEHOLDER: 2,080 h minus about 320 h leave, holidays, training |")
    print(f"| night share of problems | {NIGHT_SHARE:.0%} | derived: PRD NFR-1 250 a night / round 4 500 a day |")
    print(f"| night duty length | {NIGHT_SHIFT_H} h | PLACEHOLDER |")
    print(f"| cover: someone on duty at all hours | {COVERAGE_FTE:.1f} FTE | PRD SM-8 (one on night duty; backups on call from home are standby, not staffed hours); 8,760 h / productive hours |")
    print(f"| catalogue and release work | {CATALOGUE_FTE} FTE | PROVISIONAL; done by the same engineers as incident work |")
    print(f"| baseline tooling work | {BASELINE_TOOLING_FTE} FTE | PROVISIONAL |")
    for k, (c, g, src) in SERVICES.items():
        print(f"| footprint: {k} | {c[0]}-{c[1]} vCPU, {g[0]}-{g[1]} GiB | {src} |")
    print(f"| footprint per node | {PER_NODE[0][0]}-{PER_NODE[0][1]} vCPU, {PER_NODE[1][0]}-{PER_NODE[1][1]} GiB | {PER_NODE[2]} |")
    print("| disk | Prometheus 2/3/4 GB + logs 7 GB + spool 0.5/1.25/2 GB per node + audit/outbox 1/2/5 GB | research §9; audit/outbox PLACEHOLDER |")
    print("| engineer cost | $100k (50k / 130k) | Amine, modelling assumption |")
    print("| reuse extra load | 20% | PLACEHOLDER |")
    print()


def staffing_rows(label, n, i, w=None, simple=None):
    x = model(n, i, w=w, simple=simple)["st"]; y = model(n, i, baseline=True, w=w, simple=simple)["st"]
    return (f"| {label} | {x['orvex_hours_day']:.1f} | {x['fte']:.1f} | {y['orvex_hours_day']:.1f} | {y['fte']:.1f} |")


def print_staffing(n):
    print(f"## Staffing at {n:,} clusters (Orvex engineers; hands-on hours a day across the fleet)\n")
    print("FTE = the larger of (a) cover: someone on duty at all hours, and (b) work: incident hands-on hours plus catalogue/release work, done by the same engineers. Waiting time is not workload. Kubernetes/AWS self-healing and grouping are credited equally in both cases. **No time below is measured.**\n")
    print("| Scenario | Orvex hours/day with Nightshift | FTE with Nightshift | Orvex hours/day without | FTE without |\n|---|---|---|---|---|")
    for i, sname in enumerate(S):
        print(staffing_rows(f"Work-type split, {sname} (supported {A['supported_share'][i]:.0%})", n, i))
    print(staffing_rows("PRD average: 90% automatic, 20 min (single average)", n, 1, simple=PRD_AVG))
    print(staffing_rows("PRD stress: 60% automatic, 45 min (single average)", n, 1, simple=PRD_STRESS))
    print()
    x = model(n, 1)["st"]
    print("Base work-type breakdown with Nightshift (Orvex hands-on hours a day): " + ", ".join(f"{k} {v:.1f}" for k, v in x["breakdown"].items())
          + f"; customer/provider hands-on {x['customer_hours_day']:.1f} h a day (not Orvex). Night: {x['night_hours']:.1f} h of hands-on work → {x['night_people']:.1f} person(s) on a {NIGHT_SHIFT_H} h night duty.\n")
    if n < 1000:
        print("Sensitivity is not shown at this scale: round-the-clock cover sets the FTE in every case.\n")
        return
    print("**Sensitivity (base, one input at a time; FTE with / without Nightshift):**\n")
    print("| Input changed | Value | FTE with | FTE without |\n|---|---|---|---|")
    for k, vals in [("auto_of_supported", [0.5, 0.9]), ("manual_of_supported", [0.0, 0.15]), ("orvex_scope", [0.5, 0.9]),
                    ("self_heal", [0.0, 0.4]), ("approval_min", [5, 10]), ("investigation_min", [20, 45]),
                    ("manual_min", [15, 60]), ("grouping", [0.8])]:
        for v in vals:
            a = model(n, 1, w={k: v})["st"]["fte"]; b = model(n, 1, baseline=True, w={k: v})["st"]["fte"]
            print(f"| {k} | {v} | {a:.1f} | {b:.1f} |")
    print()


def print_scale(n):
    print(f"## Costs at {n:,} clusters, hosted AI (main approach), engineer ${ENGINEER['illustrative']:,}/yr, work-type split, equal handling time\n")
    print("| Per cluster per month | " + " | ".join(S) + " |\n|---|---|---|---|")
    r = [model(n, i) for i in range(3)]
    b = [model(n, i, baseline=True) for i in range(3)]
    for label, k in [("T1 in-cluster footprint, standalone (customer)", "t1"), ("T2 hosted AI tokens (Orvex)", "t2"),
                     ("T3 Nightshift share of Fleet (Orvex)", "t3"), ("T4 network egress (Orvex)", "t4"),
                     ("T5 SMS and calls (Orvex)", "t5"), ("H Orvex engineers", "h")]:
        print(f"| {label} | " + " | ".join(money(x[k]) for x in r) + " |")
    print("| **Orvex cash: Nightshift** | " + " | ".join(money(orvex_cash(x)) for x in r) + " |")
    print("| **Orvex cash: baseline** | " + " | ".join(money(orvex_cash(x)) for x in b) + " |")
    print("| **Customer footprint: Nightshift standalone** (EKS: cash; OMK: allocated value of existing hardware) | " + " | ".join(money(x['t1']) for x in r) + " |")
    print("| **Customer footprint: baseline monitoring** | " + " | ".join(money(x['t1']) for x in b) + " |")
    print("| **Customer footprint: Nightshift reusing existing monitoring** (incremental) | " + " | ".join(money(footprint_reuse(i)[3]) for i in range(3)) + " |")
    print("| Customer/provider hands-on hours a day (fleet, same in both) | " + " | ".join(f"{x['st']['customer_hours_day']:.1f}" for x in r) + " |")
    print("| Orvex FTE with / without Nightshift | " + " | ".join(f"{x['st']['fte']:.1f} / {y['st']['fte']:.1f}" for x, y in zip(r, b)) + " |")
    print("| Footprint resources standalone (vCPU / GiB / GB disk) | " + " | ".join(f"{x['vc']:.2f} / {x['gb']:.1f} / {x['disk']:.0f}" for x in r) + " |")
    print("| Customer-side traffic (GB/month) | " + " | ".join(f"{x['cust_gb']:.2f}" for x in r) + " |")
    print("| SMS messages per month (whole fleet) | " + " | ".join(f"{x['sms']:,.0f}" for x in r) + " |")
    print()
    print("Engineer-cost sensitivity (base, Orvex cash with / without): " + ", ".join(
        f"${e:,}/yr → {money(orvex_cash(model(n, 1, e)))} / {money(orvex_cash(model(n, 1, e, True)))}" for e in (ENGINEER['low'], ENGINEER['high'])) + "\n")


def print_target():
    print("## The 15-engineer target (PRD SM-8): what would make it feasible\n")
    print("About 15 engineers at 10,000 clusters is a **target, not a proven capacity**. Under the base work-type split, combinations that reach 15 FTE or fewer (catalogue work PROVISIONAL at 5 FTE):\n")
    print("| auto_of_supported | orvex_scope | investigation_min | FTE with Nightshift |\n|---|---|---|---|")
    for a in (0.5, 0.7, 0.9):
        for o in (0.5, 0.7, 0.9):
            for inv in (20, 30, 45):
                f = model(10_000, 1, w={"auto_of_supported": a, "orvex_scope": o, "investigation_min": inv})["st"]["fte"]
                print(f"| {a:.0%} | {o:.0%} | {inv} | {f:.1f}{' ✓' if f <= 15 else ''} |")
    print()


def print_danny():
    """Answer: cost per cluster per month at 100 and 10,000 clusters, hosted vs in-cluster AI; what moves it most."""
    ci = customer_increment(1)
    gv = dict(gpu_variants())["base"]
    print("## Answer: cost per cluster per month (base scenario, v5)\n")
    print("All figures are estimates under labelled assumptions; nothing is measured. Orvex figures are cash. Customer figures are resources first, then an *indicative* value at AWS Frankfurt on-demand prices, which is not a bill. Hosted and in-cluster AI are not assumed to give equal quality.\n")
    print("| Case | Orvex cost per cluster | Customer: extra resources | Customer: indicative value of those resources | Customer: AI hardware | Without Nightshift (Orvex cost) | Orvex saving (+) or extra cost (-) |")
    print("|---|---|---|---|---|---|---|")
    res = f"{ci['vcpu']:.2f} vCPU, {ci['gib']:.1f} GiB RAM, {ci['disk_gb']:.0f} GB disk"
    for n in (100, 10_000):
        w = model(n, 1); b = model(n, 1, baseline=True)
        hosted = orvex_cash(w); local = hosted - w["t2"]; base = orvex_cash(b)
        print(f"| Hosted AI, {n:,} clusters | {money(hosted)} | {res} | {money(ci['value'])} | none (Orvex pays tokens: {money(w['t2'])}) | {money(base)} | {money(base - hosted)} |")
        print(f"| In-cluster AI, {n:,} clusters | {money(local)} | {res}, plus the model's own GPU and host resources (not sized) | {money(ci['value'])} | per option below | {money(base)} | {money(base - local)} |")
    print()
    print("**In-cluster AI hardware, per cluster that uses it, per month** (only where the customer wants it; most customers are not assumed to buy a GPU):\n")
    print("| Option | Cost per month | What it is |\n|---|---|---|")
    rows = [("Existing spare 24 GB datacenter GPU (L4-class)", "existing spare 24 GB datacenter GPU (L4-class, 72 W): power only", "already owned: power only; no purchase"),
            ("Existing spare 24 GB consumer GPU", "existing spare 24 GB consumer GPU (~350 W, assumption): power only", "already owned: power only"),
            ("New 24 GB GPU (Danny's ~$1,000 option)", "new 24 GB consumer GPU (~$1,000, Danny): 36-month amortisation + power + host share $20 + maintenance 10%/yr", "purchase spread over 36 months + power + host share + maintenance"),
            ("New 96 GB GPU (Danny's ~$10,000 option; listings ~$14-16k)", "new 96 GB GPU ($10,000 Danny / $15,000 Codex listing): amortisation + power (~600 W, assumption) + host share $40 + maintenance", "purchase spread over 36 months + power + host share + maintenance"),
            ("EKS GPU instance g6.xlarge, always on", "EKS g6.xlarge (L4) always on", "rented, list price"),
            ("EKS GPU instance started on demand", "EKS g6.xlarge started on demand (0.15 unfamiliar problems/month x 0.5 h, plus 1 h/day warm window)", "rented by the hour; warm window and start-up delay are PLACEHOLDERS")]
    for label, key, what in rows:
        print(f"| {label} | {money(gv[key])} | {what} |")
    print("\nBoundary: hardware or instance, power, hosting share and maintenance. Excluded: staff time to run models, evaluation, spares. Wattages, load, PUE, electricity prices, host shares and maintenance rates are PLACEHOLDERS (see the source table).\n")
    nodes, step = node_steps(ci["vcpu"], ci["gib"])
    print("**Actual extra spending for the customer vs indicative value:**\n")
    print(f"- **Resources (estimate):** {res} per cluster (research §9 envelope midpoints; 10 nodes).")
    print(f"- **Indicative value:** {money(ci['value'])} a month at Frankfurt on-demand prices. This is what the capacity would cost if bought as cloud capacity, not what the customer pays.")
    print("- **If spare capacity exists:** no new server or node is bought. Power, cooling, storage and network for that load are still real costs; they are **not estimated** (missing: measured power per vCPU on customer hardware, and the customer's network prices).")
    print(f"- **If no spare capacity exists:** capacity is added in whole steps, for example {nodes} m7i.large node{"s" if nodes != 1 else ""} ≈ {money(step)} a month on EKS list price; bigger clusters or the high scenario can need more than one. On OMK it means buying or reallocating hardware (price unknown).")
    print("- **Disk on EKS** (Nightshift's audit and outbox volume) is real spending even with spare compute.\n")
    print("**Orvex saving (base scenario):**\n")
    print("| Scale | Per cluster per month | Fleet per month | Fleet per year | With $50k / $130k engineer-year |\n|---|---|---|---|---|")
    for n in (100, 10_000):
        sv = orvex_cash(model(n, 1, baseline=True)) - orvex_cash(model(n, 1))
        lo = orvex_cash(model(n, 1, ENGINEER["low"], True)) - orvex_cash(model(n, 1, ENGINEER["low"]))
        hi = orvex_cash(model(n, 1, ENGINEER["high"], True)) - orvex_cash(model(n, 1, ENGINEER["high"]))
        print(f"| {n:,} clusters | {money(sv)} | {money(sv * n)} | {money(sv * n * 12)} | {money(lo)} / {money(hi)} per cluster |")
    print()
    print("Scenario range at 10,000 clusters (Orvex saving per cluster per month): " + ", ".join(
        f"{S[i]} {money(orvex_cash(model(10_000, i, baseline=True)) - orvex_cash(model(10_000, i)))}" for i in range(3)) + ".\n")



def final_summary_rows(n):
    """Final summary (2026-11-15): Orvex cash + customer indicative increment + AI host/GPU cost, per AI option."""
    w = model(n, 1)
    hosted = orvex_cash(w); local = hosted - w["t2"]
    inc = customer_increment(1)["value"]
    gv = dict(gpu_variants())["base"]
    opts = [
        ("Hosted AI", hosted, 0.0, "tokens are in Orvex's cost", "estimate"),
        ("Existing customer GPU (L4-class, power only)", local, gv["existing spare 24 GB datacenter GPU (L4-class, 72 W): power only"],
         "GPU power only; host CPU/RAM/server not included", "incomplete subtotal"),
        ("New 24 GB GPU (Danny's ~$1,000)", local, gv["new 24 GB consumer GPU (~$1,000, Danny): 36-month amortisation + power + host share $20 + maintenance 10%/yr"],
         "amortisation + GPU power + host-share PLACEHOLDER + maintenance", "estimate"),
        ("New 96 GB GPU (Danny's ~$10,000; listings ~$14-16k)", local, gv["new 96 GB GPU ($10,000 Danny / $15,000 Codex listing): amortisation + power (~600 W, assumption) + host share $40 + maintenance"],
         "amortisation + GPU power + host-share PLACEHOLDER + maintenance", "estimate"),
        ("EKS GPU instance, always on (g6.xlarge)", local, gv["EKS g6.xlarge (L4) always on"],
         "rental includes the instance's CPU, RAM and power", "estimate"),
        ("EKS GPU instance, on demand (g6.xlarge)", local, gv["EKS g6.xlarge started on demand (0.15 unfamiliar problems/month x 0.5 h, plus 1 h/day warm window)"],
         "rental while running; warm window PLACEHOLDER", "estimate"),
    ]
    return [(name, o, inc, ai, o + inc + ai, note, kind) for name, o, ai, note, kind in opts]


def print_final_summary():
    print("## Final summary: cost per cluster per month, hosted AI or an in-cluster GPU (base scenario)\n")
    print("Columns: **Orvex operating cost** is cash. **Customer increment** is the *indicative* cloud-priced value of Nightshift's extra CPU, RAM and disk (not a bill; see the answer table). **Model host and GPU** is the AI option's own cost (cash or amortised cash); EKS rental already includes the instance's CPU, RAM and power, so nothing is added twice. **Combined estimate** adds the three and therefore mixes cash with indicative value. Figures assume comparable workloads; model quality and the model's resource use are untested.\n")
    print("| AI option | 100: Orvex | 100: customer increment | 100: model host and GPU | 100: combined | 10,000: Orvex | 10,000: customer increment | 10,000: model host and GPU | 10,000: combined |")
    print("|---|---|---|---|---|---|---|---|---|")
    r100 = final_summary_rows(100); r10k = final_summary_rows(10_000)
    for a, b in zip(r100, r10k):
        flag = " (incomplete subtotal)" if a[6] == "incomplete subtotal" else ""
        print(f"| {a[0]} | {money(a[1])} | {money(a[2])} | {money(a[3])} | {money(a[4])}{flag} | {money(b[1])} | {money(b[2])} | {money(b[3])} | {money(b[4])}{flag} |")
    base100 = orvex_cash(model(100, 1, baseline=True)); base10k = orvex_cash(model(10_000, 1, baseline=True))
    print(f"| *Without Nightshift (Orvex only)* | {money(base100)} | – | – | {money(base100)} | {money(base10k)} | – | – | {money(base10k)} |")
    print()
    print("Notes: the existing-GPU row counts GPU power only (a partial cost: host CPU, RAM and server use are missing), so its combined figure is an incomplete subtotal. New-GPU rows include a host share that is a PLACEHOLDER. The customer increment is the same in every row; the model's own host resources are separate. Biggest drivers: Orvex's people (round-the-clock cover at 100 clusters; the share of problems needing a person at 10,000), Nightshift's in-cluster footprint and whether spare capacity absorbs it, and the GPU choice.\n")


if __name__ == "__main__":
    print("# Cost model results (round 8, generated by cost_model.py; model v5, 2026-11-15: checker moved out of the baseline; customer increment defined; answer table added)\n")
    print("All usage numbers are unvalidated assumptions; PLACEHOLDER and PROVISIONAL mark inputs without a source. Prices: AWS Frankfurt list prices, 2026-11-11, a comparison basis only. Savings and break-even hold only **under these assumptions**. Round 4's 95/90/80% is the share of problems the catalogue **supports**, not the share resolved automatically.\n")
    print_final_summary()
    print_danny()
    for n in (100, 10_000):
        print_staffing(n)
    print_target()
    for n in (100, 10_000):
        print_scale(n)
    print_sources()
    print("## AI variants: replaces T2 for a cluster that uses it (per cluster per month)\n")
    print("Boundary for every row: hardware or instance, power, hosting share and hardware maintenance. **Excluded everywhere:** staff time to run and update models, evaluation, spares, and the customer's own server. Capability is **not** equivalent: a 24 GB card runs smaller models than hosted Haiku or Sonnet, and quality is untested (PRD: compare local and hosted on the same cases).\n")
    print("Sources: L4 72 W and g6.xlarge $1.0064/h verified; Danny's $1,000 / 24 GB and $10,000 / 96 GB are his hypotheses (a $1,000 24 GB card is not verified); 96 GB cards listed at $14,080-16,000 (brief addendum, Codex). **PLACEHOLDERS:** consumer card 350 W, 96 GB card 600 W, 40% average load, PUE 1.5, electricity $0.15/0.25/0.35 per kWh, host share $20/$40, maintenance 10% a year, the 1 h/day warm window. GPU start-up delay is unverified.\n")
    print("| Variant | " + " | ".join(S) + " |\n|---|---|---|---|")
    gv = gpu_variants()
    for k in gv[0][1]:
        print(f"| {k} | " + " | ".join(money(v[k]) for _, v in gv) + " |")
    print("| Hosted tokens, Haiku 4.5 regional (round 4) | " + " | ".join(money(x) for x in A["tokens_per_cluster_mo"]) + " |")
    print("| No AI | $0 | $0 | $0 |")
