# Addendum: Nightshift PRD

Depth that belongs downstream (mainly in the architecture). Sources in brackets.

## For the architecture

- **Independent self-monitoring (FR-4, Amine's idea):** a monitoring tool inside Nightshift that is independent of Prometheus, so that if Prometheus stops, Nightshift notices that metric collection has stopped (Amine, 2026-10-29).
- **Hosting provider:** the planning files say "a hosting provider"; the architecture is free to name the provider for the prototype (Amine, 2026-10-28).
- **Where Quornex Fleet runs (AI's reading, unconfirmed):** bare-metal servers under OMK, not hosted Kubernetes such as EKS. Basis: Danny names the launch hosting provider both in his bare-metal paragraph and as the place where Quornex Fleet runs (danny-qa Exchange 4).
- **Fleet learning pipeline (FR-37 to FR-40, unverified):** candidate design: sanitised evidence → a person diagnoses → rule and fix → replay test → shadow run across the fleet → gradual rollout with rollback → signed, versioned catalogue (AI's session-2 coaching feedback).

## For the UX (added 2026-11-02)

Open UX work from the 2026-11-02 review is in the "UX" item under "From the review of the 2026-11-02 update".

- **External-AI consent wording (draft by Codex, pasted by Amine; PRIV-8):** "Can Nightshift send limited, checked information about problems to this AI provider? The provider won't keep it after processing." **If Yes:** hosted AI helps automatically within that permission. **If No:** nothing is sent to an AI provider; local tools are used instead. Source code is a separate permission (FR-43). (Adjusted 2026-11-02: Codex's draft said "nothing is sent outside", which mixed up "no external AI" with "no outbound data". Other permitted channels (PRIV-9) are unaffected.)
- **Cluster status when the heartbeat is not permitted (FR-6):** "Heartbeat not permitted by the customer: status unknown", shown differently from the status for a stopped heartbeat, such as "No data since 02:10" (Amine, 2026-11-02).
- **Cluster status when neither the heartbeat nor Fleet reports are permitted (PRIV-9):** "Remote monitoring disabled by policy: status unknown" (Amine, 2026-11-02).
- **Status for dangerous repairs (FR-52):** dangerous repairs now show "Manual repair needed".
- **Statuses from the UX run (2026-10-31), for reference:** incident status Being watched / Needs attention / Waiting for customer / Resolved; repair status Waiting for approval / Running / Verifying / Succeeded / Failed / Rejected / Blocked / Cancelled / Expired; severity Critical / Warning / Informational.

## Input for the privacy and security review and the architecture

High findings from the second PRD validation (2026-10-31) that are design details rather than product requirements. They are handed to those deliverables instead of being added to the PRD (Amine, 2026-10-31). Full text: `review-after-security.md` (SEC-R2-*), `review-after-adversarial.md` (H-*) and `review-after-judge.md` (H*).

- **Approval surface:** render the action and target only from structured data, never from AI text; neutralise links and names an attacker controls; define approver roles, step-up authentication and how portal identities map to customers (in the first version, Slack is used only for notifications); require two different people where two approvals are needed (SEC-R2-03, SEC-R2-05, adversarial H-3).
- **Untrusted inputs beyond logs:** Kubernetes names and annotations, metrics, BMC strings, customer code and model output; define "independent signals" (SEC-R2-04).
- **Exfiltration and diagnostic access:** egress only through the gateway (SEC-8); define what "diagnostic access" to databases and Secrets allows (SEC-R2-06).
- **Code fixes:** pinning patch hashes, test-environment isolation (data, secrets, internet), engineer access as a channel, secret scanning before any hosted-model call, database migrations as prohibited actions, a review rule matching the two reviewers needed for catalogue entries, and keeping customer code out of fleet-wide entries (SEC-R2-07, SEC-R2-08, adversarial H-7, H-8, H-10).
- **Platform updates:** signing-key custody, who may label an update "routine", and protecting the enforcement code from being weakened by updates; version skew under customer-controlled updates (SEC-R2-09, adversarial H-11).
- **Hardware:** BMC credential custody at installation, role separation, risk levels for power actions, the BMC network as a pivot, and checking at installation that each BMC belongs to its node (SEC-R2-10, adversarial H-16).
- **Management agent:** its rights, and containment if it is compromised (SEC-R2-12).
- **Repairs adding up:** capacity-aware limits across different targets; FR-30's testability (adversarial H-4).
- **Stale monitoring:** pause automatic repairs while Nightshift's own data is stale (adversarial H-5).
- **Silent nodes:** fencing before stateful pods move off a node that may still be alive (adversarial H-6).
- **Working without a model:** the core loop (detect, check, act, verify, record) works when no model is available (judge H6). This is now a PRD requirement for customers who have neither external-AI consent nor in-cluster AI (Section 7, "Without external AI"; 2026-11-02).
- **Cost and staffing:** human approval time is likely the dominant cost; count the review and approval work the PRD itself creates (judge H5, adversarial H-13).

## From the review of the 2026-11-02 update

Design details from `review-update-adversarial.md`, `review-update-rubric.md` and `reconcile-exchange5.md` and `reconcile-ux-memlog.md`, handed to the deliverables that own them instead of being added to the PRD (same rule as on 2026-10-31). Finding IDs C* and H* below are from `review-update-adversarial.md`; they are not the H-* IDs from `review-after-adversarial.md` in the section above.

- **Privacy and security review and architecture:**
  - Custody of the key that signs the agreed management policy, kept separate from the Fleet and release keys (adversarial C2; extends "Platform updates" above).
  - Which independent signals the executor uses to check that a repair does not affect customer production, so the check does not rest on the untrusted reading agent (adversarial H3; extends "Untrusted inputs beyond logs", SEC-R2-04).
  - The full list of outbound flows (update and catalogue downloads, approval delivery, the audit service, the signal to Orvex, code-fix engineer access, telephony) assigned to PRIV-9 channels (adversarial H4; extends "Exfiltration and diagnostic access" and the engineer-access channel under "Code fixes").
  - What happens when two approvals are needed and one expires before the other is given (adversarial H9; extends "Approval surface").
- **UX (see also "For the UX" above):** the settings journey is still missing and now carries more: modes, ticks, the last-resort condition, delegation, read scope, external-AI consent, outbound channel permissions and reading the management policy (rubric, carried over). Nine UX decisions from 2026-10-31 are stale after this update (dangerous-repair approvals, a screen for manual repairs, recovery-plan review, settings rows, approval routing that lacks an Orvex-only case, missing statuses "Manual repair needed" and "Waiting for Orvex", history "who permitted it", the "written by AI" label when templates are used, cluster states): see `reconcile-ux-memlog.md`, section 3. The UX run also uses "expires" for an unanswered request, while FR-22 makes an unused approval expire; the UX should follow FR-22 or ask for a PRD change.
- **Cost model and staffing (extends "Cost and staffing" above):** re-run the SM-8 arithmetic with the human work this update adds: manual dangerous repairs, Orvex approvals of safe platform repairs outside the policy and platform work on clusters in alert-only mode (adversarial H12).
