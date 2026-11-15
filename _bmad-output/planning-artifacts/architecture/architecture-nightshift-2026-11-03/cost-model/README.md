# Cost model (round 8)

**Status: model v5 (2026-11-15).** v4 is preserved in `history/v4-2026-11-11-work-types/`. Calculations and sources are explained in [Appendix D](../appendix-d-cost-calculations.md).

- `cost_model.py` generates `cost-model-results.md`: run `python3 cost_model.py > cost-model-results.md`. The two always agree: the results file is never edited by hand.
- **Labels:** every input has a source in the results' "Where every input comes from" table. **PLACEHOLDER** means no source; **PROVISIONAL** means a team size to be set later.
- **Status of the numbers:** no handling time or proportion is measured. Savings and break-even hold only under these assumptions.

## Version history

| Version | Date | What changed | Kept as |
|---|---|---|---|
| v1 | 2026-11-11 | First model: invented inputs (70% Orvex scope, 50% seat utilisation, 24/7 staffed seats); escalations 30 min vs 45 by hand in the main case | Not preserved as a file; described in `.memlog.md` and AI_LOG #61–62 |
| v2 | 2026-11-11 | Equal handling time as the main case; cash vs customer footprint split | Not preserved as a file; described in `.memlog.md` and AI_LOG #62 |
| v3 | 2026-11-11 | Inputs taken from the PRD, the research and earlier rounds; source table. Wrongly read round 4's "supported" share as "handled automatically" | `history/v3-2026-11-11-sourced-inputs/` |
| v4 | 2026-11-11 | **Supported ≠ automatic.** Human work split into approval-only (5–10 min, Amine, illustrative), investigation and manual repair; Orvex vs customer/provider work separated; self-healing and grouping credited in both cases; hands-on time only; staffing = max(round-the-clock cover, work), with catalogue work done by the same engineers; PRD average and stress kept as separate scenarios; 15 engineers shown as a target with the conditions that would make it feasible | `history/v4-2026-11-11-work-types/` |
| **v5** | 2026-11-15 | Answers Danny's question directly: Orvex cost, the customer's incremental resources and indicative value, AI hardware options, the without-Nightshift baseline, and Orvex's saving at 100 and 10,000 clusters. The independent checker moves out of the baseline into Nightshift's increment. The customer increment is defined as Nightshift's components plus a 20% PLACEHOLDER extra load on the shared Prometheus, Alertmanager/kube-state-metrics/probes and log storage, so existing monitoring isn't counted twice. Resources come first; dollar values are labelled indicative, not bills. No input was changed to lower the result | current |
