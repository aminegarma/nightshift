# 5.4 Rollout waves, stop conditions and rollback (proposal, 2026-11-05, not decided)

**Status:** AI proposal for Amine. Nothing here is adopted until Amine decides.

## Two kinds of update

| | Nightshift releases, catalogue and policy | Platform updates (FR-47) |
|---|---|---|
| What | Agent, gateway, executor, checker; catalogue and policy versions | OMK or Quornex versions on bare metal; Kubernetes version, nodes and add-ons on EKS |
| Applied by | Flux in each cluster (5.2), pinned by digest | **OMK:** OMK's own update path *(unknown, to confirm with Orvex)*. **EKS:** the EKS update API, run by whoever holds the account rights *(account layout is an assumption)* |
| Rollback | Previous signed release, kept locally | **OMK:** unknown. **EKS:** control plane to the previous minor version **within 7 days**, then only by a new cluster; one minor version at a time; can't be paused once started (AWS docs, checked 2026-11-05) |
| Permission | Maintenance policy (FR-47) | Maintenance policy; rollback policy or approval (FR-47) |

Fleet's rollout controller sequences **both** in the same waves with the same stop conditions. It never applies anything itself: it only says which clusters are eligible for which signed version now.

## R1 Waves and stop conditions

- **Wave 0:** Orvex's own test clusters, one OMK and one EKS at least.
- **Then growing waves** *(sizes and soak times are assumptions, e.g. 1% → 5% → 25% → 100%, with a soak time per wave)*, each containing both platforms; health is judged **per platform**, so an EKS-only fault stops EKS without hiding behind healthy OMK clusters.
- **Never in an early wave, never counted healthy:** clusters whose heartbeat doesn't reach Fleet (FR-46).
- **Within the customer's maintenance window only** (FR-47); a wave is a set of *eligible* clusters, not a time.
- **Automatic stop** (FR-32) when updated clusters, compared with not-yet-updated ones, show: lost or degraded heartbeats; failed post-update self-checks; a new correlated problem; more failed verifications or escalations; signature-check failures. Thresholds are assumptions to tune.
- **Stop beats go:** a stop takes effect at once; restarting needs a person.

## R2 Rollback when the bad update broke the normal path (FR-32)

Three layers, so no single broken part blocks recovery:

1. **Flux is not part of a routine Nightshift release.** It is upgraded only through the separate install path (E3). A bad Nightshift release that breaks the gateway or the agent leaves Flux working, so a signed rollback release can still arrive.
2. **Local probation guard.** After an update, the cluster runs a probation check. If it fails within the probation window, a minimal local component reverts to the **last known-good signed release kept in the cluster**, without Fleet. *(Where it lives is open: inside the independent checker, or a separate tiny guard. The heartbeat path stays report-only and never carries commands.)*
3. **Manual path:** a runbook for Orvex or the customer through the separately authorised install path, for when the local guard is broken too.

**Platform updates:** EKS rollback exists only within 7 days, so EKS waves soak and stop well inside that window. OMK rollback is unknown until Orvex confirms it.

**Permission question (needs Amine's decision):** is reverting a Nightshift update that **failed its own probation** part of that update (covered by the maintenance policy), or an emergency rollback that needs the customer's rollback policy (FR-47)? The proposal: part of the update, because the Nightshift agent never touches customer workloads (NFR-4). Platform rollbacks stay under FR-47 unchanged. This would be a PRD clarification (AP-7).

## R3 Fleet can't push old or stale versions

A compromised rollout controller could assign an old, vulnerable signed release, or keep a cluster on an old version forever.

- The cluster accepts only a release that is **newer than its current one**, or that the release pipeline signed as an **allowed rollback target** for that release.
- Signed release metadata **expires**, so a cluster held back notices and reports it (PRD: a cluster can't stay indefinitely on an old version).
- This follows The Update Framework's ideas *(TUF; as an idea, not yet as a tool choice)*.
