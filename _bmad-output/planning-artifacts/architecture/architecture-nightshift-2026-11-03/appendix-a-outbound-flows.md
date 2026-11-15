# Appendix A: Outbound flows and channels (PRIV-9)

Part of the architecture hand-in (2026-11-15). Each outbound flow is listed with its path, PRIV-9 channel, what it carries and what happens when the channel is off (spine AD-70). Process history: `.working/round9-outbound-flows.md`.

## Flows

| # | Flow | From → to | Through | Channel | Carries | If the channel is off |
|---|---|---|---|---|---|---|
| 1 | Fleet heartbeat | Independent checker → Fleet heartbeat watchdog | **Own path (AP-8)**: own identity, fixed destination, rate limit, fixed-schema validator | Fleet heartbeat (required service channel) | Agent ID, timestamp, status (AP-1 would add checkpoint fields) | Can't be turned off: no strict no-outbound mode in v1 |
| 2 | Sanitised problem reports, correlation fields, coverage report, AI usage counts | Gateway → Fleet report intake | Gateway | Fleet reports | Allowlisted fields only | Left out of fleet correlation; Fleet sees only the heartbeat |
| 3 | Audit checkpoints (until AP-1 is adopted) | Audit service → gateway → Fleet checkpoint store | Gateway | Fleet reports | Sequence, chain head, time, key ID, signature | Loss of external checkpointing recorded and shown (D11) |
| 4 | Decision statements D to the portal; approval requests; receipts; group-approval leaves | Executor → gateway → relay → portal / group-confirmation service | Gateway | Portal | D fields, request status, receipts | No new remote approvals; open requests only on the local dashboard |
| 5 | Inbound decisions, stops, switch-offs fetched from the relay | Gateway → relay (response returns on the cluster's connection) | Gateway | Portal (decisions) | Request identifiers out; signed objects in | Remote decisions don't arrive; local stops still work |
| 6 | Relay status statements, signed key lists, policy and roster updates | Gateway → relay / Fleet | Gateway | **Proposed: required service traffic, add to AP-8 / PRIV-9 update** (carries only cluster identity and version numbers) | Identity and versions out; signed objects in | Without them the cluster ages through fresh → stale → expired (24 h: automatic repairs suspended) |
| 6a | Fixed attention notice after the expired tier (AD-24) | Gateway → Fleet | Gateway | Fleet heartbeat path or Fleet reports: **to confirm** (carries no data) | A fixed "attention needed" marker, no data | If Fleet reports are off, only the heartbeat shows the cluster is degraded |
| 7 | Dashboards and morning summary data | Gateway → portal | Gateway | Portal | Fact-builder fields only | Visible only on the local dashboard |
| 8 | SMS (one-time codes, alerts, post-decision notices) | Gateway → SMS provider | Gateway | Notifications | Executor-built text from D and templates | No SMS codes: option B approvals can't complete (passkey-only only where policy enables it) |
| 9 | Phone calls and Slack messages | Gateway → telephony / Slack provider | Gateway | Notifications | Allowlisted fields (O-11, with AP-2) | No alerts outside the cluster |
| 10 | Signal to Orvex when the customer confirms something (FR-12) | Gateway → Fleet | Gateway | **Proposed: Fleet reports** (to confirm) | Event type and request identifiers | Orvex not told; recorded locally |
| 11 | Hosted AI calls | Gateway → Bedrock (customer-permitted Regions) | Gateway | External AI (consent) | Fact-builder fields only | Templates and rules only; local model if present |
| 12 | AI credential vending | Gateway → Fleet credential vending | Gateway | External AI (only used when consented) | Cluster identity, usage counts | No credentials requested |
| 13 | Source code for code fixes | Gateway → hosted provider | Gateway | External AI + separate source-code consent (AD-38) | Relevant files only, after secret scanning and the PRIV-4 check | Code fixes unavailable |
| 14 | Code-fix engineer access | Orvex engineer ↔ isolated test environment | To be designed (FR-44) | **Open**: needs its own consent and channel decision | — | — |
| 15 | Release, catalogue and model-weight downloads | Flux → registry | **Own path (AP-8)**: Flux identity, registry allowlist, digest pinning, signature verification | **Proposed: required service traffic (AP-8)**; requests carry no customer data | Package requests out; signed packages in | Can't be turned off: security updates are required by contract (FR-47) |
| 16 | AWS poller | Poller → customer's own AWS account Describe APIs | **Own path (AP-8)**: customer-granted role, read-only, own identity, allowlist | **Proposed: customer-account access, not data leaving to a third party (AP-8)** | Describe requests; responses stay in the cluster | Reduced EKS coverage |
| 17 | Management-agent links | Workload cluster → customer's control cluster (outbound, own identities) | Gateway of the workload cluster | Inside the customer's estate; sanitised data only (PRIV-5) | Sanitised status and coordination messages | Cross-cluster repairs wait; local repairs continue |
| 18 | Installation-time registrations (first-admin pin, receipt key, audit key, cluster identity) | Installer job → Fleet | Install path | Portal / service setup (one-time) | Public keys and fingerprints only | Installation can't complete |

## Not Nightshift flows
Cluster DNS, time sync and the kubelet's own image pulls belong to the platform, not Nightshift. They are listed so nobody assumes they are covered.

## Open points for Amine
- Flows 6, 10, 15 and 16 have no named PRIV-9 channel. Proposed: extend AP-8 so the PRD names "required service traffic" (status statements, key lists, signed package downloads) and the AWS-poller exception.
- Flow 14, code-fix engineer access, needs its own design and consent.
