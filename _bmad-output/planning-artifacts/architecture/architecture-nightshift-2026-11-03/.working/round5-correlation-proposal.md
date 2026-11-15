# 5.5 Correlation and consolidated alerts (proposal, 2026-11-05; decided, see round5-fleet.md 5.5)

AI proposal for Amine. Nothing here is adopted until Amine decides.

## C1 What is grouped, from allowed fields only
- **Inputs:** sanitised reports (PRIV-3 allowed fields, via intake), heartbeats, and the rollout controller's own state (who got which version when).
- **Group key:** problem type (catalogue entry ID, or for unfamiliar problems a fingerprint built only from allowed fields: signal family, component kind, error class), plus platform, Nightshift release, catalogue version, platform version, rollout wave, and location (EKS Region; OMK site, *if Quornex shares it*).
- No log text, names or customer data are used for matching (PRIV-2, PRIV-3).

## C2 When a group becomes one alert
- Same key on several clusters within a time window, **above that key's normal rate** (thresholds are assumptions to tune).
- **Linked to the rollout:** if the group concentrates on newly updated clusters, the rollout stops (R1) and the alert says so.
- **Silent clusters:** heartbeat loss is grouped by location and network path. Many silent clusters in one Region or site is shown as "N clusters unreachable from Fleet in eu-west-1", a possible shared outage, never "300 agents dead".
- **Gaps are shown, not hidden:** clusters that don't send Fleet reports (PRIV-9), or whose data is stale, are counted as "not reporting", not as healthy.

## C3 Tools
- **Correlation:** a small custom Fleet service (the group keys above are Nightshift-specific).
- **Notification:** Prometheus **Alertmanager** (Apache-2.0) for deduplication, grouping, inhibition, silences and routing to phone/Slack, in its HA cluster mode (checked 2026-11-05).

## C4 Isolation
- Orvex engineers see the group across customers; a customer sees only its own clusters and never another customer's identity or count details (FR-48).
- The group alert carries the frozen cluster list that a group approval (O-4, next item) would cover.
