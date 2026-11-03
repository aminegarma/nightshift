# Addendum: Nightshift PRD

Depth that belongs downstream (mainly in the architecture). Sources in brackets.

## For the architecture

- **Independent self-monitoring (FR-4, Amine's idea):** a monitoring tool inside Nightshift that is independent of Prometheus, so that if Prometheus stops, Nightshift notices that metric collection has stopped (Amine, 2026-10-29).
- **Hosting provider:** the planning files say "a hosting provider"; the architecture is free to name the provider for the prototype (Amine, 2026-10-28).
- **Where Quornex Fleet runs (AI's reading, unconfirmed):** bare-metal servers under OMK, not hosted Kubernetes such as EKS. Basis: Danny names the launch hosting provider both in his bare-metal paragraph and as the place where Quornex Fleet runs (danny-qa Exchange 4).
- **Fleet learning pipeline (FR-37 to FR-40, unverified):** candidate design: sanitised evidence → a person diagnoses → rule and fix → replay test → shadow run across the fleet → gradual rollout with rollback → signed, versioned catalogue (AI's session-2 coaching feedback).

## Input for the privacy and security review and the architecture

High findings from the second PRD validation (2026-10-31) that are design details rather than product requirements. They are handed to those deliverables instead of being added to the PRD (Amine, 2026-10-31). Full text: `review-after-security.md` (SEC-R2-*), `review-after-adversarial.md` (H-*) and `review-after-judge.md` (H*).

- **Approval surface:** render the action and target only from structured data, never from AI text; neutralise links and names an attacker controls; define approver roles, step-up authentication and how Slack identities map to customers; require two different people where two approvals are needed (SEC-R2-03, SEC-R2-05, adversarial H-3).
- **Untrusted inputs beyond logs:** Kubernetes names and annotations, metrics, BMC strings, customer code and model output; define "independent signals" (SEC-R2-04).
- **Exfiltration and diagnostic access:** egress only through the gateway (SEC-8); define what "diagnostic access" to databases and Secrets allows (SEC-R2-06).
- **Code fixes:** pinning patch hashes, test-environment isolation (data, secrets, internet), engineer access as a channel, secret scanning before any hosted-model call, database migrations as prohibited actions, a review rule matching the two reviewers needed for catalogue entries, and keeping customer code out of fleet-wide entries (SEC-R2-07, SEC-R2-08, adversarial H-7, H-8, H-10).
- **Platform updates:** signing-key custody, who may label an update "routine", and protecting the enforcement code from being weakened by updates; version skew under customer-controlled updates (SEC-R2-09, adversarial H-11).
- **Hardware:** BMC credential custody at installation, role separation, risk levels for power actions, the BMC network as a pivot, and checking at installation that each BMC belongs to its node (SEC-R2-10, adversarial H-16).
- **Management agent:** its rights, and containment if it is compromised (SEC-R2-12).
- **Repairs adding up:** capacity-aware limits across different targets; FR-30's testability (adversarial H-4).
- **Stale monitoring:** pause automatic repairs while Nightshift's own data is stale (adversarial H-5).
- **Silent nodes:** fencing before stateful pods move off a node that may still be alive (adversarial H-6).
- **Working without a model:** the core loop (detect, check, act, verify, record) works when no model is available (judge H6).
- **Cost and staffing:** human approval time is likely the dominant cost; count the review and approval work the PRD itself creates (judge H5, adversarial H-13).
