# PRD Update 2026-11-15: architecture reconciliation (AP-1 to AP-20)

**Inputs.** PRD `.memlog.md` from "PRD Update started (Amine, 2026-11-15)" to the end (conflict decisions 1-7, AP-9 to AP-20); `reconcile-architecture-ap1-ap8.md` (locations and draft wording for AP-1 to AP-8, adjusted where the conflict decisions changed it); `architecture/architecture-nightshift-2026-11-03/ARCHITECTURE-SPINE.md`, `appendix-a-outbound-flows.md`, `appendix-b-proposed-prd-changes.md`.

**AP-1.** Applied (the memlog's last entry says "apply AP-1..AP-20"; confirmed by the coordinator during the update). The architecture spine still describes AP-1 as pending (see "Remaining contradictions", item 7).

**Backups** of every edited file (before this update): `/tmp/claude-1000/-home-amine-nightshift/4c1d45da-342e-4062-9ddd-1d25a6f0e645/scratchpad/prd-update-backup/` (prd.md, addendum.md, EXPERIENCE.md, open-items-2026-11-03.md; DESIGN.md backed up but not edited).

**Not edited:** architecture files, `.memlog.md` files, `AI_LOG.md`, DESIGN.md.

**Attribution.** Every PRD change is tagged "(architecture AP-n, Amine, 2026-11-15)". Untested values are labelled "starting value", "to test" or "mechanism to test". New UX wording is marked "pending UX review".

**Counts.** prd.md: 73 text replacements (frontmatter included), listed as 74 rows below. addendum.md: 11 edits. EXPERIENCE.md: 56 edits. open-items-2026-11-03.md: 1 edit. New requirement ID: **SEC-10**. New Section 10 items: **24 to 33**.

---

## 1. prd.md

| # | Section | Before → after (summary) | AP |
|---|---|---|---|
| 1 | Frontmatter | `status: final`, `updated: 2026-11-03` → `status: draft`, `updated: 2026-11-15` | — |
| 2 | Status line | Adds a sentence on the 2026-11-15 reconciliation, the draft status while in review, the tag convention and this report | — |
| 3 | 1 Vision | "Each cluster looks after itself…" → adds "within bounded offline limits (FR-22)" | 4 |
| 4 | 3.1 scope | Code fixes "in-cluster model by default; hosted only with consent" → hosted first under separate consent; in-cluster model where hardware allows and customer prefers | 6 |
| 5 | 3.1 Deferred | Adds: control-plane failures reported and escalated, not repaired, in v1; no hardware power actions, read-only hardware access | 5, 10 |
| 6 | 3.2 non-goals | "through a channel the customer has not permitted" → adds "other than the required Fleet service channel" | 8 |
| 7 | 3.2 non-goals | Strict no-outbound: "needs the Fleet heartbeat" → "needs the Fleet service channel, including the Fleet heartbeat" | 8 |
| 8 | Glossary, Approval | Adds: confirmed in the portal with passkey plus one-time code by text message; code entered in the portal, never answered by text | 2 |
| 9 | Glossary, Maintenance policy | Rollback policy covers emergency rollbacks → adds "except the bounded probation rollback in a routine Nightshift update's authorisation" | 7 |
| 10 | Glossary | New entry **Fleet service channel**: exact flows, "minimal service metadata; no raw logs, secrets or application content", replaces the heartbeat-only rule | 8 |
| 11 | FR-3 | New bullet: stateful workloads moved off a silent node only with a verified fencing and storage-safety procedure, else manual; powered-off reading is evidence only; BMC system-ID match | 10 |
| 12 | FR-5 | Adds: Kubernetes API unreachable → "Kubernetes API unreachable: repairs paused", escalated; control-plane failures not repaired in v1; reduced coverage documented | 5 |
| 13 | FR-6 heartbeat fields | "only agent ID, timestamp, status" → adds the five fixed-schema checkpoint fields; limits: detectable not recoverable, no completeness or truth, ~32 bytes covert-channel risk if the audit service is compromised | 1 |
| 14 | FR-6 required channel | "required service channel … passes the outbound check like any other channel" → part of the Fleet service channel; onboarding explains checkpoint fields; own path outside the gateway, fixed-schema validator as its purpose-specific check; shared failure limit | 1, 8 |
| 15 | FR-12 | Signal to Orvex → travels on optional Fleet reports; if off, recorded locally and Orvex not told | 8 |
| 16 | FR-13 | New bullet: approval code also by text message, under its own permission; part of the approval flow, not an alert | 2 |
| 17 | FR-14 | "Every problem … first appears on a monitoring page" → adds bounded separate capacities, "approval request blocked: capacity full", Orvex alerted, stops stay possible | 14 |
| 18 | FR-14 | New bullet **Confirming an approval** (pending feasibility and usability testing) with sub-bullets: approval text-message permission (conflict 1), passkey-only fallback and strings, notice after every decision, full limits list, timing targets (60 s, 5 min code; to test), sent/received/applied/expired/unreachable states, rejection confirmation open | 2, 20 |
| 19 | FR-15 | In-cluster dashboard → stable internal address, separate local passkeys, rules in PRIV-9 | 13 |
| 20 | FR-22 | New bullet **Offline validity**: classification by required authority; fresh/stale/expired per conflicts 3 and 4 (stale: customer-held continue, policy and Orvex side of last resort pause, cutoff for safe policy repairs moves from 24 h to 1 h; expired: customer-held continue within own validity, delegations only for decisions already received, all Orvex authorities stop); stated limits (unticks and switch-offs reach on reconnection; fleet-wide outage effects); restart, clock, restore rules; distinct from portal-off. Replaces AP-4's "no automatic repairs" for the expired tier | 4 |
| 21 | FR-22 | "withdrawn if the problem resolves" → closed as "resolved, no longer needed" only after verification; recorded and notified | 14 |
| 22 | FR-22 | Authorisation re-check → adds "including its offline validity" | 4 |
| 23 | FR-22 | "sent but not yet confirmed by the cluster … server orders decisions" → takes effect when received and applied; new bullets **Receipts** ("Sent — not yet effective in the cluster", received ≠ applied, portal status not proof), **Confirming a stop** (unconfirmed, not failed), **Stops win** (server order for display) | 3, 20 |
| 24 | FR-24 | New bullet: Orvex side of last resort pauses after 1 h without fresh confirmation, stops at 24 h | 4 |
| 25 | FR-50 | "[OPEN] length, proposed by the architecture" → 2 minutes, starting value to test, timed by the cluster | 16 |
| 26 | FR-51 limits | Adds: policy repairs need current Orvex authority, pause from 1 h without fresh confirmation | 4 |
| 27 | FR-51 who authorises | Adds: each policy version, including Orvex's signed list of platform-only repairs, signed only after testing and two distinct reviewers, enforced by the signing system | 18 |
| 28 | FR-52 who performs | Adds conflict 2 rule: a named customer representative confirms the provider is ready, presses "Start now", reports "I've done it"; record names representative, provider and technician; no replacement of approvals or checks | 2 |
| 29 | FR-52 | New bullet: "Start now" conditions and confirmed like an approval; "I've done it" is a report, triggers verification, does not close the fault by itself, reportable after the window, untrusted text; authentication open (item 25) | 2 |
| 30 | FR-31 | New bullet **Recovery order**: stops first, reconcile, revalidate; expired approval authorises no new forward step; accepted external operations observed; safe-stop only if pre-authorised and safe; retry rules; unprotected actions manual in v1; recovery time a test result | 17 |
| 31 | FR-32 table | "Roll back … Whether that needs a separate tool is for the architecture" → new row: probation rollback by a separate rollback guard; policy-rollback row kept without the open sentence | 7 |
| 32 | FR-32 | New bullet **Confirming a group approval**: Orvex technical approval only; one Fleet SMS summary; assurance label; limits (summary only, understanding not proven, portal + confirmation service compromise) | 15 |
| 33 | FR-33 | New bullets: stated exception when storage is full (stops and narrowly pre-authorised safe-stop steps may run unrecorded; never forward repairs); "blocked: audit unavailable"; probation rollbacks recorded | 11, 7, 20 |
| 34 | FR-34 | Who permitted it → adds assurance level of each approval (three values) | 2, 15 |
| 35 | FR-34 outcomes | Adds "exhausted"; blocked reasons "blocked: disruption budget or rate limit", "blocked: audit unavailable" (pending UX review) | 20 |
| 36 | FR-35 | Adds: Fleet's independent checkpoints; detectable, not recoverable | 1 |
| 37 | FR-39 | Adds: releases signed only after testing and two distinct reviewers, enforced by the signing system | 18 |
| 38 | FR-43 title | "In-cluster by default, hosted only with explicit consent" → "Hosted first, with a separate source-code consent" | 6 |
| 39 | FR-43 body | In-cluster default → hosted first under separate consent, off until opt-in, separate from PRIV-8; in-cluster alternative | 6 |
| 40 | FR-43 | Relevant code sent → adds "after secret scanning and the outbound check (PRIV-4)" | 6 |
| 41 | FR-43 | "Without an in-cluster GPU or this consent …" → "Without this consent or a suitable in-cluster model …; monitoring and catalogue repairs continue" | 6 |
| 42 | FR-44 step 1 | In-cluster first → hosted under separate consent, or in-cluster | 6 |
| 43 | FR-44 | New bullet: review and tests reduce risk but cannot make a fix certainly safe; planned seeded validation reported with scope, never as proof; engineer access open (item 27) | 6 |
| 44 | FR-46 | New bullet: paused rollout never resumes on its own; alerts release owner after a set time (assumption to test); person resumes or stops | 19 |
| 45 | FR-47 | New bullets: **Probation rollback** for routine Nightshift updates (bounded, rollback-safe, no re-apply, person called, shared-failure limit; healthy-signal mechanism to test); **Rolling back a security update** needs an explicit advance customer policy (recovery version, reintroduced vulnerability, recovery limits), else urgent escalation; rollback-safe, recorded, plan to restore the fix (conflict 5) | 7 |
| 46 | FR-47 | "Emergency rollback runs…" → "Any other emergency rollback runs…" | 7 |
| 47 | PRIV-2 | Adds: source code under PRIV-6 is the one deliberate exception to sanitising; still secret-scanned and checked | 6 |
| 48 | PRIV-3 | Adds: approval text-message fields are action, target, code, from the decision and catalogue template | 2 |
| 49 | PRIV-4 | "The test is mandatory, with no exceptions" → "The check is mandatory, with no exceptions; on the three paths outside the gateway it takes the purpose-specific form below"; new bullet **Every outbound flow is checked** (conflict 7 wording) | 8 |
| 50 | PRIV-6 | "in-cluster model by default" → hosted only with separate source-code consent; otherwise code stays | 6 |
| 51 | PRIV-9 lead | Heartbeat as the required channel → Fleet service channel (includes heartbeat) as the one required channel | 8 |
| 52 | PRIV-9 channels | Channel list → adds Fleet service channel, FR-12 signal under Fleet reports, approval text message; new bullets **Fleet service channel** (exact flows, metadata wording, offline rules) and **EKS AWS read-only calls** (separately optional, customer-granted) | 2, 8 |
| 53 | PRIV-9 | "No channel, including the Fleet heartbeat, is silently exempt" → "including the Fleet service channel …; purpose-specific control of PRIV-4 on the three paths" | 8 |
| 54 | PRIV-9 onboarding | Adds: approval text message is a separate permission naming provider and fields, default open (item 24); first install by verified contract contact, first admin per SEC-7 | 2, 9 |
| 55 | PRIV-9 | "Without the Fleet heartbeat" → "Without the Fleet service channel" | 8 |
| 56 | PRIV-9 Fleet reports off | Adds: Orvex not told of confirmations (FR-12); recorded locally | 8 |
| 57 | PRIV-9 portal off | Adds: portal-off is distinct from losing Fleet contact; tiers depend on the Fleet service channel | 4 |
| 58 | PRIV-9 dashboard | "Withdrawals, alert-only and settings changes" → adds rejections, unticks, authorised settings changes including ticks; stable address, local passkeys, no per-repair approvals, additional permissions preserved, each change audited with a receipt | 13 |
| 59 | PRIV-9 | New bullet **Without notifications**: no alerts; stops unconfirmed until receipt seen; approval text message keeps its own permission | 2, 3 |
| 60 | SEC-3 | Adds: v1 hardware access read-only, no power actions, manual per FR-52; narrows the acting part | 10 |
| 61 | SEC-7 | Adds: admins grant or decline approval text message, enable passkey-only fallback (Orvex for Orvex approvals); new bullets **First installation and first administrator** (provisional; split code, contract contact, dispute handling, installer never enrols, cluster-admin limit) and **Local passkeys** | 2, 9, 13 |
| 62 | SEC-8 | "All data leaving … passes through a separate gateway" → exactly three exceptions with own identity, allowlist, restrictions; default-deny network; tested on OMK and EKS; enforcement gaps documented; cut-off enforcement within FR-22 limits | 8, 4 |
| 63 | SEC-9 | Adds pointer to SEC-10 | 12 |
| 64 | **SEC-10 (new)** | Cluster-admin is a documented limit: what holders can and cannot do; temporary, approved, audited Orvex admin; partial tamper detection only | 12 |
| 65 | 7 Model options | "the default for code fixes" → "including for code fixes where the customer wants the code kept in the cluster" | 6 |
| 66 | 7 table | In-cluster GPU "the default for code fixes" → "used for code fixes where the customer wants the code kept in the cluster" | 6 |
| 67 | NFR-4 | Adds: stated storage-full exception (FR-33); checkpoint lets Fleet detect a rewritten or destroyed record | 1, 11 |
| 68 | NFR-5 | Kept; adds the FR-22 offline limits (customer-held continue; Orvex-authority repairs pause after 1 h, stop after 24 h) | 4 |
| 69 | SM-4 | Adds: audit logs give partial tamper detection, not protection against cluster-admin (SEC-10) | 12 |
| 70 | 10 triage | Adds update note (7a and undo window decided; new items 24-33) | — |
| 71 | 10 For Danny | Item 7a removed from open; moved to Answered as "hosted first" decision | 6 |
| 72 | 10 Design decisions still open | Undo-window line removed; new items 24-30 (approval SMS default, "I've done it" authentication, rejection/stop confirmation, code-fix engineer access (C-14, kept open), attention-notice channel and policy/roster updates, Orvex technical approval in the stale tier, channel of the post-decision notice) | 2, 4, 6, 8 |
| 73 | 10 To test | New items 31-33 (tiers and undo window; approval confirmation; outbound controls, network rules, probation signal) | 2, 4, 7, 8, 16 |
| 74 | 10 Answered | 7a added; item 22 heartbeat → Fleet service channel, approval SMS default open; undo-reject window decided | 6, 8, 16 |

## 2. addendum.md

| # | Section | Before → after (summary) | AP |
|---|---|---|---|
| 1 | For the architecture, Revocation | Open design item → answered (receipts, "Sent — not yet effective in the cluster", stop notice); old text kept as "Was:" | 3 |
| 2 | Undoing a rejection | Open length → answered, 2 minutes starting value, timed by the cluster | 16 |
| 3 | In-cluster dashboard | Open item → answered (address, local passkeys, allowed actions, receipts); per-platform reachability still to verify | 13 |
| 4 | For the UX, Final statuses | Adds the new architecture status strings, pending UX review, received/applied distinct | 20 |
| 5 | Approval surface | Adds: step-up authentication answered by the approval confirmation, pending tests | 2 |
| 6 | Exfiltration | "egress only through the gateway" → "except the three named paths with purpose-specific controls" | 8 |
| 7 | Code fixes | Secret scanning answered; engineer access still open (item 27) | 6 |
| 8 | Hardware | Power-action risk levels → no power actions in v1; BMC read-only with system-ID match | 10 |
| 9 | Silent nodes | Answered: verified fencing, else manual | 10 |
| 10 | Outbound flows list | Answered by appendix A (draft) and the Fleet service channel; open: attention notice, engineer access | 8 |
| 11 | New section "From the architecture reconciliation (2026-11-15)" | Mechanism depth (SMS code storage, polling, credentials; clock protections; rollback guard) and the list of architecture documents needing follow-up wording | 1-8 |

## 3. EXPERIENCE.md (UX)

Frontmatter `updated: 2026-11-03` → `2026-11-15` (status unchanged). No screen redesigned; new copy is marked "pending UX review".

| # | Section | Before → after (summary) | AP |
|---|---|---|---|
| 1 | Foundation | Notify-only bullet → adds: text message also carries the approval code; own permission | 2 |
| 2 | IA, Notifications row | Adds approval codes and post-decision notice by text message | 2 |
| 3 | IA, B6b row | "Fleet heartbeat (required)" → Fleet service channel (required), approval text message, AWS read access (EKS) | 2, 8 |
| 4 | IA, Onboarding channel screen | Adds first-install authorisation by contract contact and split first-admin enrolment; installer never enrols | 9 |
| 5 | IA, In-cluster-only dashboard | "[OPEN: O-7]; withdrawals, alert-only, settings" → stable address, local passkeys, receipts, rejections, unticks, authorised settings incl. ticks; no per-repair approvals | 13 |
| 6 | Voice, Manual repair buttons | Adds: Start now confirmed like an approval; I've done it is a report, auth [OPEN: O-8]; named customer representative for a provider | 2 |
| 7 | Voice, Confirmation sheet | Adds code-step copy, "Confirmation code could not be sent", reduced-assurance string (pending UX review) | 2 |
| 8 | Voice, After Approve | Adds progress states and the "You approved … Not you? Withdraw" text (pending UX review) | 2, 3, 20 |
| 9 | Voice, Sent, not yet in effect | "Sent; not yet confirmed by the cluster" (stops only) → "Sent — not yet effective in the cluster" for every decision until the receipt; received ≠ applied; "Stop unconfirmed" (pending UX review) | 3, 20 |
| 10 | Voice, Request changed | "no longer needed" → only after verification; history "resolved, no longer needed" | 14 |
| 11 | Voice, Reject result | Undo window → 2 minutes, starting value, timed by the cluster | 16 |
| 12 | Voice, History | "confirmed by the cluster" → "applied by the cluster … (receipt)" | 3 |
| 13 | Voice, History | Adds assurance level in history (pending UX review) | 2 |
| 14 | Voice, new row | Probation rollback history/morning-summary string (pending UX review) | 7 |
| 15 | Components, Manual-repair panel | Adds hardware-provider representative rule | 2 |
| 16 | Components, Manual-repair panel | "[OPEN: O-8]" → Start now confirmed like an approval; I've done it auth open | 2 |
| 17 | Components, Confirmation sheet | Confirm → then code and passkey; fleet batch confirmed by one Fleet SMS | 2, 15 |
| 18 | Components, Confirmation sheet | Undo "[OPEN: O-13]" → 2 minutes, starting value | 16 |
| 19 | Components, Timeline entry | Stops show sent/confirmed → every decision shows sent and applied (receipt) | 3, 20 |
| 20 | Components, Health-grid tile | Adds permission-tier markers, separate from freshness (pending UX review) | 4 |
| 21 | Components, Settings row | Old status string → new; tick-row offline line (pending UX review) | 3, 4 |
| 22 | State, Severity/status table | New row "New states from the architecture" (pending UX review) | 20 |
| 23 | State, Repair status → FR-34 | New row Exhausted → exhausted | 20 |
| 24 | State, Freshness and connection | New rows: permission tier limited, permission tier expired (with stated limits), Kubernetes API unreachable | 4, 5 |
| 25 | State, Approval validity | "withdrawn if the problem resolves" → closes only after verification; capacity-full line | 14 |
| 26 | State, Decisions, Revocation | Old string → receipt wording; stop notice; unconfirmed not failed; stop beats approval | 3 |
| 27 | State, Decisions, Revocation | Portal off: adds rejections and local passkeys | 13 |
| 28 | State, Decisions, Sign-in | "Mechanism [OPEN: O-5]" → code plus passkey for approvals, pending tests | 2 |
| 29 | Surface states | New rows: Confirmation code could not be sent; Approval text message not permitted; Approval request blocked: capacity full; Repairs suspended: storage full (pending UX review) | 2, 11, 14 |
| 30 | Surface states, Switch to alert-only | Old string → "Sent — not yet effective in the cluster" until receipt | 3 |
| 31 | Surface states, Portal access turned off | Dashboard actions widened, local passkeys | 13 |
| 32 | Surface states, Portal access turned off | Adds: distinct from losing contact with Orvex | 4 |
| 33 | Surface states, Portal not permitted | Adds "within the permission tiers (FR-22)" | 4 |
| 34 | Surface states, Portal and notifications not permitted | "[OPEN: O-7]" → "O-7, mostly answered" | 13 |
| 35 | Interaction Primitives, Decisions | "Step-up authentication … [OPEN: O-5]" → code plus passkey (pending tests); roles still open | 2 |
| 36 | Flow 6 step 1 | "Fleet heartbeat shown as required, exact fields" → Fleet service channel, exact flows and fields, metadata wording (pending UX review) | 1, 8 |
| 37 | Flow 6 step 2 | Adds first-admin enrolment and the approval text-message decision | 2, 9 |
| 38 | Flow 6 failure | Adds: declining the approval text message → told about fallback or unavailability | 2 |
| 39 | Flow 7 step 5 | Start now → confirmed like an approval | 2 |
| 40 | Flow 7 step 6 | I've done it → a report, not an approval, doesn't close the fault | 2 |
| 41 | Authorisation, Fleet-wide | Adds group SMS confirmation and assurance label | 15 |
| 42 | Authorisation, Last-resort | Adds: Orvex side pauses after 1 h without confirmation | 4 |
| 43 | Authorisation, Reject | Undo "[OPEN: O-13]" → 2 minutes, starting value | 16 |
| 44 | Privacy table, heartbeat row | "Fleet heartbeat … Sends only: agent ID, timestamp, alive/degraded" → **Fleet service channel** row with heartbeat plus checkpoint, status confirmations, key lists, signed downloads, metadata wording; offline behaviour (copy pending UX review) | 1, 8 |
| 45 | Privacy table, Fleet diagnostic reports | "No" text adds: Orvex not told when you confirm something | 8 |
| 46 | Privacy table, Notifications | "No" text adds: stops not confirmed by a separate message | 3 |
| 47 | Privacy table, new row | **Approval text message**: own permission, default open; "No" consequence | 2 |
| 48 | Privacy table, new row | **AWS read access (EKS only)**: optional, customer-granted, responses stay in the cluster | 8 |
| 49 | Privacy table, Source code | "Code fixes need an in-cluster GPU" → unavailable unless in-cluster model; hosted first (pending UX review) | 6 |
| 50 | Privacy, Phone calls bullet | Adds approval codes by text message; post-decision notice channel open (item 30) | 2 |
| 51 | Open items O-5 | Marked answered for approvals (pending tests) | 2 |
| 52 | Open items O-7 | Marked mostly answered | 13 |
| 53 | Open items O-8 | Marked partly answered; "I've done it" auth still open | 2 |
| 54 | Open items O-11 | Adds approval text-message fields | 2 |
| 55 | Open items O-13 | Marked answered (2 minutes, starting value) | 16 |
| 56 | After Open items | New paragraph on the PRD Update of 2026-11-15 and this report | — |

## 4. open-items-2026-11-03.md

| # | Section | Before → after | AP |
|---|---|---|---|
| 1 | 3 Deferred review findings | "A request code against phishing." → marked superseded by the approval confirmation (FR-14) | 2 |

DESIGN.md: not edited. New visual states may need tokens later (UX review): a code-entry field, the "reduced assurance" warning, a "not yet effective" / "unconfirmed" chip, and a permission-tier marker distinct from the stale hatch.

---

## Remaining contradictions

These could not be resolved without a new decision. Each is also listed as an open item in PRD Section 10 or as a follow-up for the architecture documents.

1. **Orvex technical approval in the stale tier** (PRD item 29). Conflict 4: "permissions requiring current Orvex authority pause (agreed management policy repairs, Orvex side of last resort)". Conflict 3 (expired tier) lists "Orvex technical approval" among the authorities that stop. The original AP-4 stale tier allowed "only safe ticked repairs and safe policy repairs". It is undecided whether an Orvex technical approval already received in the cluster, and still within its own validity, counts between 1 h and 24 h.
2. **Which permission carries the notice sent after a decision** (PRD item 30). AD-18: "After every decision the cluster sends a post-decision notice through the gateway"; appendix A flow 8 puts "SMS (one-time codes, alerts, post-decision notices)" under **Notifications**. Conflict 1: "The approval SMS is a separately disclosed part of the approval flow, distinct from alerts. It needs its own explicit permission". It is unclear whether the notice belongs to the approval text-message permission or to notifications.
3. **Default at onboarding of the approval text-message permission** (PRD item 24). Conflict 1 requires "its own explicit permission naming the SMS provider and the permitted fields". PRIV-9: "Fleet reports, notifications and the portal start ticked … These are service settings, not consent". Pre-ticked or opt-in is not decided.
4. **What the Fleet service channel carries** (PRD item 28). Conflict 6 lists: "heartbeat; relay status statements and signed key lists; signed release, catalogue and model downloads". Appendix A flow 6 also includes "policy and roster updates", and flow 6a (the "attention needed" notice after the expired tier) still says "Fleet heartbeat path or Fleet reports: **to confirm**".
5. **How a rejection and the other stops are confirmed** (PRD item 26). AD-18: the code step "Applies to customer, delegated and Orvex approvals and to 'Start now'". The extract: "Confirm with Amine whether rejects keep only the passkey". No decision is in the memlog.
6. **How "I've done it" is authenticated** (PRD item 25; UX O-8). Appendix B: "the authentication level for 'I've done it' (a fresh passkey assertion with no SMS) is an AI proposal that has not been adopted". Conflict 2 settles who reports for a hardware provider, but not the authentication level.
7. **The architecture documents disagree with this update** (not edited here; they need follow-up wording):
   - AD-16: "Until AP-1 is explicitly adopted, checkpoints leave through the gateway on the permitted Fleet-report channel". AD-27: "It carries only agent ID, timestamp and status until AP-1 is accepted". The heartbeat-fields convention and appendix A flows 1 and 3 say the same. The PRD now adopts AP-1.
   - AD-24: "expired (no automatic repairs; observe and report)". AD-71: "including suspending automatic repairs after 24 hours". Conflict 3 now lets customer-held safe ticked repairs continue in the expired tier.
   - Appendix A flow 8: "No SMS codes: option B approvals can't complete" when notifications are off. Conflict 1 now gives the approval text message its own permission, separate from notifications.
   - Appendix B AP-7: "A maintenance-policy update (and a security update) includes an exact, bounded rollback". Conflict 5 now requires an explicit advance customer policy for a security-update rollback.
   - Appendix A and AD-70 still call flows 6, 10, 15 and 16 "proposed". Conflict 6 has now decided them (Fleet service channel; FR-12 under Fleet reports; AWS poller separately optional).
8. **Code-fix engineer access** (PRD item 27, C-14). It stays open by decision. FR-44 step 4 says the engineer "securely accesses the test environment", but no consent or channel is defined for it (appendix A flow 14: "Open").

For information only (decided, but worth telling Danny): NFR-5 and Danny's Exchange 4 ("each cluster should still be capable of looking after itself") and Exchange 5 ("routine, tested repairs should happen automatically") now work within the offline tiers. Policy repairs pause after 1 hour without contact with Fleet, so a Fleet outage longer than 1 hour pauses them fleet-wide.

---

## Second pass (remaining points)

**Inputs.** PRD `.memlog.md`, entry "Remaining points (Amine, 2026-11-15)", decisions (1) to (8). New PRD and UX text is tagged "(Amine, 2026-11-15, remaining points)" or "(in the PRD, 2026-11-15, remaining points)". **Backups** of every file edited in this pass: `/tmp/claude-1000/-home-amine-nightshift/4c1d45da-342e-4062-9ddd-1d25a6f0e645/scratchpad/prd-update-backup-2/`. Not edited: `.memlog.md` files, `AI_LOG.md`, DESIGN.md, open-items file.

### Decisions applied

1. **No exception for Orvex technical approvals already received** (item 29): FR-22 stale tier now pauses repairs that need Orvex technical approval, including one already received and still valid.
2. **Post-decision notice** (item 30): falls under the approval text-message permission (FR-14, PRIV-9), not notifications. The post-stop notice stays on notifications (FR-22).
3. **Approval text-message permission** (item 24): opt-in at onboarding, not pre-ticked (FR-14, PRIV-9, Section 10 item 22).
4. **Fleet service channel** (item 28): adds policy and roster updates and the fixed attention notice; PRIV-9 lists the exact permitted fields of each flow (heartbeat with AP-1 checkpoint fields; cluster identity, versions and sequence numbers; requested digests or versions; versions requested, with the received roster objects containing people, roles and credential public keys; a fixed marker with no other content). Roster updates are not described as data-free.
5. **Stops** (item 26): rejection, withdrawal and untick need a fresh passkey check, no text-message code; the post-stop notice confirms them (FR-14, FR-22).
6. **"I've done it"** (item 25, UX O-8): fresh passkey check, no text-message code; only the named performer or the agreed customer representative (FR-52).
7. **Architecture sync**: see below.
8. **C-14** (item 27, code-fix engineer access) stays open everywhere.

### Edits

| File | Edits | Where |
|---|---|---|
| prd.md | 15 | Glossary Fleet service channel; FR-14 (permission opt-in, notice under the permission, stops); FR-22 (stale tier, confirming a stop); FR-52 ("I've done it"); PRIV-9 (Fleet service channel field list, onboarding, without notifications); Section 10 (triage note; items 24, 25, 26, 28, 29, 30 moved from open to answered; item 22) |
| addendum.md | 2 | Outbound-flows item (attention notice and policy/roster updates placed; engineer access open); follow-up for architecture marked done |
| EXPERIENCE.md | 11 | Manual repair buttons; After Approve; Manual-repair panel; Confirmation sheet (stops: passkey, no code); Revocation; Flow 6 steps 1 and 2; privacy table rows Fleet service channel and Approval text message; Phone calls bullet; O-8 answered (copy still pending UX review) |
| ARCHITECTURE-SPINE.md | 16 | AD-16, AD-27 and heartbeat convention (AP-1 accepted); new convention row "Fleet service channel fields"; AD-18 (approval-SMS permission, stops); AD-21 ("I've done it", hardware provider); AD-24 and AD-71 (tiers by required authority, stated limits, portal-off distinct); AD-38, AD-45, AD-67 headers (adopted); AD-45 security-update rule; AD-67 and AD-70 (every flow checked, purpose-specific controls, channels decided); Deferred (AP queue row replaced by UX review row; "I've done it" row removed; flow table row) |
| appendix-a-outbound-flows.md | 9 | Intro; flows 1, 3 (checkpoint rides the heartbeat), 6, 6a, 15 (Fleet service channel with exact fields), 8 split into 8 (approval-SMS permission) and 8a (notifications), 10 (Fleet reports), 16 (separately optional); purpose-specific controls section; open points (C-14) |
| appendix-b-proposed-prd-changes.md | 16 | Title and intro; AP-1 to AP-8 marked "Adopted into the PRD 2026-11-15" with conflict refinements (AP-2, AP-4, AP-7 security-update rule, AP-8); AP-9 to AP-20 appended; closing note |
| architecture-orvex.md | 24 | Appendix link; 4.3 SMS permission and stops; 4.5 performers; 4.7 tier table and stated limits; 5.1 default-deny and audit/heartbeat; 5.2 channel table; 7.7 AP-6; 8.x recovery (AP-7) and Fleet operations; 9.1 Fleet row; 13.3 open items; 13.5 table (adopted, AP-9..AP-20 row) |

**Lint.** `lint_spine.py` on the architecture workspace: 0 findings.

### Still open
- Code-fix engineer access (C-14; PRD Section 10, item 27; appendix A flow 14).
- New copy and status strings remain "pending UX review"; timing values (1 h, 24 h, 2 minutes, 60 s, 5 minutes) remain starting values to test; enforcement of the three purpose-specific outbound controls remains to verify.
