# Appendix A: Outbound flows and channels (PRIV-9)

Part of the architecture hand-in (2026-11-15). Each outbound flow is listed with its path, PRIV-9 channel, what it carries and what happens when the channel is off (spine AD-70). Process history: `.working/round9-outbound-flows.md`. Synced with the PRD update of 2026-11-15 (AP-1 and AP-8 adopted; conflict decisions 1, 6 and 7; remaining points): the **Fleet service channel** is the one required channel and carries exactly flows 1, 6, 6a and 15, with the permitted fields below, disclosed at onboarding (minimal service metadata; no raw logs, secrets or application content). Every flow is checked, including the three paths outside the gateway (PRIV-4, AD-67).

## Flows

| # | Flow | From → to | Through | Channel | Carries | If the channel is off |
|---|---|---|---|---|---|---|
| 1 | Fleet heartbeat with audit checkpoint (AP-1) | Independent checker → Fleet heartbeat watchdog | **Own path (AP-8)**: own identity, fixed destination, rate limit, fixed-schema validator as purpose-specific check | Fleet service channel (required) | Agent ID (mapped to cluster at installation), timestamp, status alive/degraded, `audit_seq`, `chain_head`, `checkpoint_time`, `audit_key_id`, `checkpoint_sig` | Can't be turned off: no strict no-outbound mode in v1 |
| 2 | Sanitised problem reports, correlation fields, coverage report, AI usage counts | Gateway → Fleet report intake | Gateway | Fleet reports | Allowlisted fields only | Left out of fleet correlation; Fleet sees only the heartbeat |
| 3 | Audit checkpoints | Audit service → independent checker (heartbeat) → Fleet checkpoint store | Rides flow 1 (AP-1 adopted 2026-11-15); no longer through the gateway on Fleet reports | Fleet service channel (required) | Sequence, chain head, time, key ID, signature | Missing heartbeat means missing checkpoints; Fleet sees "not reporting" |
| 4 | Decision statements D to the portal; approval requests; receipts; group-approval leaves | Executor → gateway → relay → portal / group-confirmation service | Gateway | Portal | D fields, request status, receipts | No new remote approvals; open requests only on the local dashboard |
| 5 | Inbound decisions, stops, switch-offs fetched from the relay | Gateway → relay (response returns on the cluster's connection) | Gateway | Portal (decisions) | Request identifiers out; signed objects in | Remote decisions don't arrive; local stops still work |
| 6 | Relay status statements, signed key lists, policy and roster updates | Gateway → relay / Fleet | Gateway | Fleet service channel (required) | Out: status statements and key lists: cluster identity, versions, sequence numbers; policy and roster updates: cluster identity and versions requested. In: signed objects; roster updates contain roster data (people, roles, credential public keys) | Interruption follows the offline tiers (AD-24): from 1 h, permissions needing Orvex authority pause; from 24 h they stop; customer-only safe ticks continue within their own validity |
| 6a | Fixed attention notice after the expired tier (AD-24) | Gateway → Fleet | Gateway | Fleet service channel (required) | A fixed "attention needed" marker, no other content | Not separately switchable; if it can't leave, Fleet still sees the heartbeat status |
| 7 | Dashboards and morning summary data | Gateway → portal | Gateway | Portal | Fact-builder fields only | Visible only on the local dashboard |
| 8 | Approval SMS (one-time codes) and post-decision notices ("You approved … Not you? Withdraw") | Gateway → SMS provider | Gateway | **Approval-SMS permission** (own permission naming provider and fields; opt-in at onboarding, not pre-ticked; not part of notifications) | Executor-built text from D and the catalogue template: action, target, and the code (code message only) | Declined: approvals need the enabled passkey-only fallback, else unavailable; turning notifications off never grants it |
| 8a | Alert SMS and post-stop notices (AD-23) | Gateway → SMS provider | Gateway | Notifications | Allowlisted fields (O-11) | No alerts outside the cluster; stops show as unconfirmed until their receipt is seen |
| 9 | Phone calls and Slack messages | Gateway → telephony / Slack provider | Gateway | Notifications | Allowlisted fields (O-11, with AP-2) | No alerts outside the cluster |
| 10 | Signal to Orvex when the customer confirms something (FR-12) | Gateway → Fleet | Gateway | Fleet reports (optional) | Event type and request identifiers | Orvex not told; recorded locally |
| 11 | Hosted AI calls | Gateway → Bedrock (customer-permitted Regions) | Gateway | External AI (consent) | Fact-builder fields only | Templates and rules only; local model if present |
| 12 | AI credential vending | Gateway → Fleet credential vending | Gateway | External AI (only used when consented) | Cluster identity, usage counts | No credentials requested |
| 13 | Source code for code fixes | Gateway → hosted provider | Gateway | External AI + separate source-code consent (AD-38) | Relevant files only, after secret scanning and the PRIV-4 check | Code fixes unavailable |
| 14 | Code-fix engineer access | Orvex engineer ↔ isolated test environment | To be designed (FR-44) | **Open**: needs its own consent and channel decision | — | — |
| 15 | Release, catalogue and model-weight downloads | Flux → registry | **Own path (AP-8)**: Flux identity, registry allowlist, permitted operations and request fields, digest pinning, signature verification | Fleet service channel (required) | Out: cluster identity, requested digests or versions; in: signed packages | Can't be turned off: security updates are required by contract (FR-47) |
| 16 | AWS poller (EKS) | Poller → customer's own AWS account Describe APIs | **Own path (AP-8)**: customer-granted role, read-only, own identity, defined operations and request fields, allowlist, limits | Separately optional, customer-granted | Describe requests; responses stay in the cluster | Reduced EKS coverage, reported |
| 17 | Management-agent links | Workload cluster → customer's control cluster (outbound, own identities) | Gateway of the workload cluster | Inside the customer's estate; sanitised data only (PRIV-5) | Sanitised status and coordination messages | Cross-cluster repairs wait; local repairs continue |
| 18 | Installation-time registrations (first-admin pin, receipt key, audit key, cluster identity) | Installer job → Fleet | Install path | Portal / service setup (one-time) | Public keys and fingerprints only | Installation can't complete |

## Not Nightshift flows
Cluster DNS, time sync and the kubelet's own image pulls belong to the platform, not Nightshift. They are listed so nobody assumes they are covered.

## Purpose-specific controls on the three paths outside the gateway
For flows 1, 15 and 16, the permitted destinations, operations and request fields are defined, plus authentication and limits; read-only access or a destination allowlist alone is not sufficient. These controls are purpose-specific, not automatically equivalent to the gateway's checks; their enforcement is to be verified on OMK and EKS and residual risks documented (PRIV-4, SEC-8, AD-67).

## Open points
- Flow 14, code-fix engineer access, needs its own design and consent (C-14, open).
- The table stays a draft until the enforcement of the three purpose-specific controls is verified.
