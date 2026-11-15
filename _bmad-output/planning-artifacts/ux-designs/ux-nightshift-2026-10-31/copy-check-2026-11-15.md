# Copy check of EXPERIENCE.md against the final PRD (2026-11-15)

Scope: the 24 places marked "(pending UX review)" after the PRD Update of 2026-11-15, checked against the final `prd.md` (FR-14, FR-22, FR-33, FR-43, FR-47, PRIV-6, PRIV-9, SEC-7) and the 2026-11-15 decisions in `.memlog.md`. Backup before editing: `/tmp/claude-1000/-home-amine-nightshift/4c1d45da-342e-4062-9ddd-1d25a6f0e645/scratchpad/experience-before-copy-check.md`.

Result: **20 consistent** (marker removed; the closing paragraph now says the wording was checked on 2026-11-15), **4 issues** (marker left, not edited).

## Issues

| Place | Conflict | Proposed copy |
|---|---|---|
| History row (assurance level) | FR-34 has a third level for group approvals; showing only "(passkey + SMS)" or "(passkey only)" would overclaim for a group Orvex approval. | Add: "or, for a group approval, '(passkey + SMS verification attested by Fleet; not independently verified by the cluster)'". |
| Probation rollback | FR-47 / conflict 5: security-update rollback needs an explicit advance policy, otherwise urgent escalation, and a plan to restore the fix. The copy covers routine updates only. | Label the existing copy "routine update". Add: "Security update v2.5 didn't pass its checks; Nightshift returned to v2.4 under your advance rollback policy. This reopens a known vulnerability; a plan to restore the fix follows." Without the policy: "Security update v2.5 didn't pass its checks. Your settings don't allow an automatic rollback, so Nightshift has called for urgent help." |
| Permission tier: expired | FR-22 classifies by required authority, not signer; "repairs you alone authorised" is unclear for delegated decisions and says nothing about Orvex-authority repairs stopping; the restart case (unknown time) is not covered by "for 24 h". | "No confirmation from Orvex for 24 h or more · only repairs that need no permission from Orvex run, within their own validity; repairs that need Orvex's permission are stopped; Nightshift keeps watching and reporting". After a restart: "No confirmation from Orvex since the restart: treated as 24 h or more". |
| AWS read access (EKS) | PRIV-9 says only that responses stay in the cluster and reduced coverage is reported. "Nothing is sent to Orvex from it" overclaims: findings may reach Orvex through permitted channels such as Fleet reports. | "Nightshift sees less of your AWS infrastructure, and this is reported." With access: "Read-only calls go only to your own AWS account; the responses stay in your cluster." |

## Notes on the places you asked about (consistent)

- Code-fix row: consistent. FR-43/PRIV-6: the source-code consent covers only sending code to the hosted model; an in-cluster model keeps code in the cluster and needs no source-code consent (the code-fix opt-in still applies).
- Approval text-message rows, permission tier "limited", capacity full, storage full, Fleet service channel (flows and fields match PRIV-9; roster updates described as carrying roster data): consistent.

## Resolution (2026-11-15)

The four issues above were corrected in EXPERIENCE.md to match the PRD (group-approval assurance label, security-update rollback copy, expired tier by required authority, AWS read access wording). All 24 places are now consistent, and EXPERIENCE.md stays final.
