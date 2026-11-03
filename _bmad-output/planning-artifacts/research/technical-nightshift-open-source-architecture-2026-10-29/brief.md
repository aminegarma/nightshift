# Approved research scope

Research date: 2026-10-29. Output owner: Codex research; draft for Amine's review.

Decision: identify a practical production-oriented OSS architecture for Nightshift, with MVP choices and enterprise alternatives. User approved full research covering observability, hardware, prediction, diagnosis, repair execution, approvals, privacy, inference and fleet management.

Hard gates: local detection and permitted repairs during management disconnection; raw telemetry and secrets remain in originating cluster; fixed tested repair catalogue; separate read and write authority; authenticated approvals; no customer-data/database/backup mutation; OMK hardware versus provider-limited EKS visibility; explicit uncertainty. Preferences: mature maintained OSS, minimal recurring overhead at 10,000 clusters, reversible integrations, small operating team.

Method: official docs and upstream repositories only; three parallel research dimensions plus lead research on fleet/policy/identity/storage; two rounds where evidence gaps justify them. Primary-source feature/licence checks are distinct from independent production validation. Estimates are engineering planning envelopes, not measured benchmarks. No claim of proven 10,000-cluster operation for the assembled stack.

User instruction overrides workflow logging: do not edit PRD, project decision log, AI_LOG.md or any Claude files. Keep every new artifact under this research folder. No architecture decisions are adopted by this report. BMAD Party Mode is a later, user-directed challenge; not run during acquisition.
