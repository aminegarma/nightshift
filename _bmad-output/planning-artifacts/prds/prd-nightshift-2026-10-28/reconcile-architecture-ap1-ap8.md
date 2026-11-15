# Reconcile: architecture AP-1 to AP-8 against the PRD and UX

Read-only extract for the PRD Update started 2026-11-15 (PRD `.memlog.md` last entry). Nothing in the PRD, addendum or UX was changed.

**Sources**
- Proposals: `architecture/architecture-nightshift-2026-11-03/appendix-b-proposed-prd-changes.md` (AP-1..AP-8), `appendix-a-outbound-flows.md` (flows 1-18).
- Final decisions: `ARCHITECTURE-SPINE.md` (status final, AD-1..AD-72) and the architecture `.memlog.md` (later entries amend earlier ones; round 9 D1-D15 of 2026-11-11, review follow-up A1-A20 and edge-case batches of 2026-11-15, consistency-check fixes of 2026-11-15).
- PRD: `prd.md` (status final, updated 2026-11-03), `addendum.md`, PRD `.memlog.md`.
- UX: `ux-designs/ux-nightshift-2026-10-31/EXPERIENCE.md`, `DESIGN.md`, `.working/open-items-2026-11-03.md`.
- Danny: `danny-qa-summary.md`.

**Attribution convention in proposed wording.** "(architecture, 2026-11-xx, AP-n; approved by Amine)" means the architecture decision was adopted by Amine on that date. It does **not** mean Amine has approved the PRD wording; every replacement below is a draft for the Update.

**Line numbers** are from `prd.md` (808 lines), `EXPERIENCE.md` (469 lines), `addendum.md` (59 lines) as read on 2026-11-15.

---

## AP-1: Audit checkpoint in the Fleet heartbeat

### 1. Final decision to carry into the PRD
Status in the architecture: **still a proposal**. Amine adopted it as the architecture's design in round 2.3 (2026-11-03), but D11 (2026-11-11) and AD-16/AD-27 make the current design work **without** it:
- Until AP-1 is explicitly accepted in the PRD, the heartbeat carries only the FR-6 fields (agent ID, timestamp, status alive/degraded). Audit checkpoints leave through the gateway on the **Fleet reports** channel (appendix A flow 3). If the customer turns Fleet reports off, the loss of external checkpointing is recorded and shown (D11).
- If accepted: the heartbeat adds exactly five fixed-schema fields, no text: `audit_seq` (u64), `chain_head` (32 bytes), `checkpoint_time`, `audit_key_id`, `checkpoint_sig`. Purpose: external, independently stored evidence that the in-cluster audit chain was not rewritten or destroyed. Onboarding explains the added fields and their purpose before the customer accepts the service.
- Limits to carry (AD-16, AD-72): checkpoints make destruction **detectable, not recoverable**; they prove no completeness or truth of the records; together with Kubernetes audit logs they give **partial** tamper detection, not a guarantee against a compromised cluster-admin. The heartbeat's outbound check is its strict fixed-schema validator on its own path (AD-27; see AP-8). A shared node or network failure can break both the heartbeat and the gateway path.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| FR-6, line 213 | "The Fleet heartbeat contains only the agent ID, a timestamp and a status (alive or degraded)" | "The Fleet heartbeat contains only the agent ID, a timestamp, a status (alive or degraded) and a minimal audit checkpoint: sequence number, chain head, checkpoint time, key ID and signature, with a fixed schema and no text. The checkpoint lets Fleet detect if the cluster's audit record is rewritten or destroyed; it cannot restore it or prove the record complete (architecture, 2026-11-03, AP-1; approved by Amine)." |
| FR-6, line 214 | "onboarding explains its purpose and its exact fields. It is authenticated and passes the outbound check like any other channel (PRIV-4, PRIV-9)" | Keep; add "including the audit checkpoint fields". Outbound-check wording: see AP-8 (the heartbeat's check is a strict fixed-schema validator on its own path). |
| NFR-4, line 732 | "Quornex Fleet notices the silence through the required Fleet heartbeat" | Add: "and, through the audit checkpoint it carries, a rewritten or destroyed audit record (FR-35)". |
| PRIV-9, line 644 / 647 | heartbeat listed as required channel | No change to the channel; the list of its fields follows FR-6. |
| FR-35, line 518-519 (context) | "the agent can add to it but cannot change or delete entries" | Optional cross-reference: "Fleet keeps independent checkpoints of the record (FR-6); destruction is detectable, not recoverable." |
| If AP-1 is **not** accepted | — | PRIV-9 "Without Fleet reports" (line 648) should add: "and audit checkpoints are no longer stored outside the cluster; this loss is recorded and shown" (D11). This sentence is needed either way until AP-1 is decided. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 433 (Privacy & outbound channels, Fleet heartbeat row) | "Sends only: agent ID, timestamp, alive/degraded." | "Sends only: agent ID, timestamp, alive/degraded, and a fixed audit checkpoint (sequence number, fingerprint of the record, time, key, signature) so Orvex can tell if this cluster's record is altered." |
| EXPERIENCE.md 361 (UJ onboarding step 1) | "The Fleet heartbeat is shown as required, with its purpose and exact fields." | No text change; the shown fields follow the row above. |
| EXPERIENCE.md 434 (Fleet diagnostic reports row) | "This cluster is left out of fleet-wide problem detection." | If AP-1 is not accepted: add "and its audit record is no longer checkpointed outside the cluster". |

### 4. Conflicts
- **Wording update, not a conflict:** the heartbeat's "only agent ID, timestamp, status" was a settled decision (AI draft accepted by Amine, 2026-11-02). AP-1 widens a channel the customer **cannot** turn off (required service channel). The added fields carry no customer data, but the onboarding explanation and the "exact fields" promise change; Amine decides explicitly.
- **Dependency:** if AP-1 is rejected, the Fleet-reports channel becomes the checkpoint path, and turning it off loses external checkpointing (needs the PRIV-9 sentence above).

---

## AP-2: Approval confirmation (option B)

### 1. Final decision to carry into the PRD
Status: **adopted, pending feasibility and usability testing** (AD-18; refined by D9, A6, A14, A15, D1; AD-21; AD-17).
- **Flow:** portal sign-in with passkey (portal-verified only) → Approve (confirmation sheet) → the cluster builds and stores the decision statement and sends, through the gateway, an SMS to the approver's phone number in the signed roster, naming the action, with a one-time code → the person enters the code (paste and auto-fill allowed) → a fresh passkey assertion with user verification over the decision's fingerprint → the cluster accepts only if code and assertion resolve to the same decision; assurance recorded as "passkey + SMS".
- **Applies to:** customer, delegated and Orvex approvals, and the performer's "Start now".
- **Fallback:** passkey-only only where a signed policy explicitly enables it (customer-admin-signed for customer approvals, Orvex-signed for Orvex approvals); shown to the person ("SMS confirmation unavailable: approving with passkey only (reduced assurance)") and recorded as "passkey only" in decision, receipt and history. Without an enabled fallback, an SMS failure never downgrades: the request stays open and escalation continues ("Confirmation code could not be sent").
- **SMS content and code:** generated by the executor from the decision and the catalogue template (never AI or log text; target names untrusted); code bound to the exact decision, recipient, request version and expiry; attempt and resend limits; starting code lifetime 5 minutes, which never extends the repair approval's validity; separately scoped SMS credentials per cluster, subject to provider support.
- **Post-decision notice:** after every decision the cluster sends "You approved … Not you? Withdraw" through the gateway (notifications channel), allowlisted fields only.
- **Stated limits (must be carried):**
  - the passkey signs a **fingerprint** of the decision, not readable text; paste or auto-fill means entering the code does not prove the person read the task;
  - a compromised portal can still obtain approval for a different, genuinely pending and valid request if the SMS is not read;
  - the gateway carries the SMS: a compromised gateway can alter or drop the SMS and the notice, and, since it sees the code, **the SMS gives no independent proof of possession against a compromised gateway**; the passkey signature over the decision remains the protection; the risk of a misleading message is documented (A6);
  - the post-decision notice may reveal some cases but **does not reliably detect** gateway tampering (D9);
  - provider recipient restrictions, templates, rate limits and spending controls are used only where verified; alerts and delayed billing checks are not hard caps (A6).
- **Latency (A14):** targets to test, not guarantees: under 60 s from Approve to receiving the code, under 60 s from submit to the cluster's receipt; distinct states "sent" (shown as AP-3 wording), "received/applied by cluster", "expired", "unreachable"; nothing shown effective before the cluster confirms.
- **"I've done it":** an authenticated completion report, **not an approval**; triggers Nightshift's verification; the case closes only if verification passes; stays reportable after the window ends; report text is untrusted evidence. **Its sign-in level is NOT adopted**: the AI proposal "fresh passkey assertion over the report, no SMS step" was never adopted (appendix B note). The PRD must leave the level open (UX O-8 stays partly open).
- **Group approvals (FR-32):** not option B per cluster; a Fleet group-confirmation service sends one SMS and signs an attestation; assurance label "passkey + SMS verification attested by Fleet; not independently verified by the cluster" (A15); the SMS confirms a summary, not the full target list; no claim that the mechanism proves what the approver understood (D1). See candidate AP-9.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| Glossary "Approval", line 167 | "a yes given by an authenticated person at the time, for one repair, in the Quornex portal. In the first version Slack, phone calls and text messages only notify" | Add: "It is confirmed with the person's passkey and a one-time code sent by the cluster by text message (FR-14)." Keep "only notify": the code is entered in the portal, never answered by text. |
| FR-13, line 317 | "A phone call is paired with a text message carrying the portal link" | Add a bullet: "Text messages also carry the one-time confirmation code for an approval (FR-14) and a notice after every decision. They contain only allowlisted fields (PRIV-3) built from the repair catalogue, never AI or log text (architecture, 2026-11-04, AP-2; approved by Amine)." |
| FR-14, line 321 | "Slack, phone calls and text messages only notify" | Keep. Add after line 325 a new bullet **"Confirming an approval"**: the flow above, the fallback rule, "SMS failure never lowers the requirement", the post-decision notice, and the limits list (fingerprint not text; paste/auto-fill; compromised portal; gateway sees the code, so no possession proof against a compromised gateway; notice detects nothing reliably). Mark "pending feasibility and usability testing". |
| FR-14, line 325 | "The person can approve or reject (FR-50)." | Unchanged; rejection does not need the SMS step (stop decisions; AD-17/AD-22). Confirm with Amine whether rejects keep only the passkey (architecture conventions: stops use the request-version nonce, no SMS). |
| FR-52, lines 433-436 | "Right before starting, the performer re-runs Nightshift's pre-run check" / "When the person reports the repair done" | Add: "'Start now' is confirmed like an approval (FR-14). 'I've done it' is a completion report, not an approval: it triggers Nightshift's check, the case closes only if the check passes, and it can be sent after the window ends. How the report is authenticated is open." |
| PRIV-3, line 627 | "For each channel, Orvex defines … the list of allowed fields" | Add: "For text messages, this includes the action, target and code of an approval confirmation and the post-decision notice." |
| PRIV-9, line 644 / 652 | notifications channel; "Without notifications as well: no alert or approval request reaches anyone outside the cluster" | Add to the notifications consequences: "Without notifications, the confirmation code cannot be sent: approvals in the portal are possible only where the passkey-only fallback is enabled (reduced assurance)." See Conflicts. |
| SEC-7, line 684 | list of settings only administrators change | Add "the passkey-only approval fallback (customer-admin-signed for customer approvals; Orvex-signed for Orvex approvals)". |
| FR-34, lines 513-516 | "who permitted it … by whom and when" | Add "and the assurance level of each approval (passkey + SMS, or passkey only)". |
| Addendum line 30 ("Approval surface … step-up authentication") | open design item | Mark as answered by the architecture (AD-17, AD-18), pending tests. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 131 (Voice: Confirmation sheet) | "Confirm button repeats the decision ('Approve this repair'); Cancel" | After Confirm: code step "We've sent a code to your phone ending 42 for: restart checkout-api on shop-eu-1. Enter it to continue" (paste and auto-fill allowed), then passkey. Add "Confirmation code could not be sent" and the reduced-assurance string. |
| EXPERIENCE.md 160 (Component: Confirmation sheet) | "Confirm sends the decision with the version shown" | Confirm starts the code + passkey steps; states "sent" / "received/applied by cluster" / "expired" / "unreachable" (A14). Fleet batch approval uses the group path (one SMS from Fleet, label per A15). |
| EXPERIENCE.md 132 (After Approve) | "You approved at 02:14 CET." | Add the post-decision notice: text message "You approved … Not you? Withdraw". |
| EXPERIENCE.md 125, 377-378 (Start now / I've done it) | performer buttons | "Start now" opens the same confirmation steps. "I've done it: check now" stays a report; its authentication stays [OPEN: architecture, O-8] (level not adopted). |
| EXPERIENCE.md 279, 457 (O-5 step-up) | "Step-up authentication and approver roles [OPEN: architecture, O-5]"; sign-in "allows password managers, paste and passkeys" | Close O-5 with option B (pending tests); keep paste allowed. |
| EXPERIENCE.md 62, 435, 441 (Notifications; Phone calls) | text message carries the portal link | Add: approval codes and post-decision notices travel by text message; content within O-11 allowlist. |
| EXPERIENCE.md 141 (History) | "Approved on your behalf by Lea…" | Show assurance level ("passkey + SMS" / "passkey only"). |
| open-items-2026-11-03.md, section 3 "A request code against phishing" | deferred finding | Replaced by option B (appendix B). |
| DESIGN.md | confirmation sheet uses `{rounded.container}` (line 531) | No token change required; a code-entry field and "reduced assurance" warning style may need tokens [new]. |

### 4. Conflicts
- **REAL: notifications off vs approvals.** PRIV-9 (line 644, 652) makes notifications an optional channel whose loss only stops alerts; UX 435 "You won't be alerted or called; check the portal." Option B needs the SMS (notifications channel, appendix A flow 8): with notifications off, portal approvals cannot complete unless the passkey-only fallback is enabled. Either the confirmation SMS becomes part of the portal/approval channel or PRIV-9 and the UX "No" text must state the consequence.
- **Wording, not conflict:** FR-14 "text messages only notify" stays true (code entered in the portal), but the PRD must say a text message now carries a code, and UX banned list (281) "approving from … a text message" stays.
- **Danny Exchange 1** ("Nightshift can ask for permission … through Slack and the portal"): already narrowed to portal by the PRD; option B does not reopen it. No contradiction.
- **FR-52 "the customer, or their hardware provider" performs (line 435)** vs AD-21: "A hardware provider is not in any roster; a named customer person reports for them". A provider cannot press "Start now" under option B. Real gap; see candidate AP-9.
- **"I've done it" level:** the PRD must not adopt the AI's "fresh passkey, no SMS" level.

---

## AP-3: "Sent — not yet effective in the cluster"

### 1. Final decision to carry into the PRD
(AD-23, A2, A14; Receipt convention.)
- After applying, or refusing, any decision the cluster signs a receipt with its own key (effect: applied, refused as invalid, arrived too late). Until the receipt arrives the person sees **"Sent — not yet effective in the cluster"** (replaces "Sent; not yet confirmed by the cluster"). Applies to every decision, not only revocations; the A14 approval-progress states are "sent" (shown with this wording), "received/applied by cluster", "expired", "unreachable"; nothing is shown as effective before the cluster confirms.
- Receipts travel through the portal channel or appear on the in-cluster dashboard; the relay never signs them; the relay keeps each decision until its receipt arrives.
- **Limits:** a lying or failed relay can delay or hide a stop; the missing receipt is the visible sign. The portal's "effective" status is a convenience, **not proof**: a compromised portal and relay could show a false one.
- **Stop confirmation (A2):** only after the cluster has applied and recorded a stop, it notifies the person who made it on the notifications channel (if enabled), through the gateway, never through the portal or relay; the signed receipt stays visible on the local dashboard. **No notification means "unconfirmed", not proof of failure.** A compromised gateway can still block or alter the notice.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| FR-22, line 395 | "Until then, the person sees that it was sent but not yet confirmed by the cluster, and the record shows when it was sent and when the cluster confirmed it." | "Until the cluster's signed receipt arrives, the person sees 'Sent — not yet effective in the cluster'; the record shows when it was sent and when the cluster applied it. This applies to every decision. The portal's status is a convenience, not proof. After applying a withdrawal, rejection, untick or switch to alert-only, the cluster also tells the person directly through notifications, if permitted; without that notice the stop counts as unconfirmed, not failed (architecture, 2026-11-03 and 2026-11-15, AP-3; approved by Amine)." |
| FR-22, line 395 (end) | "The server orders decisions consistently … a later withdrawal or rejection before execution still counts" | Align with AD-22: in the cluster any valid stop beats any approval regardless of order; the server order is for display and history. (Wording update.) |
| PRIV-9, line 651 | "Withdrawals, the switch to alert-only and settings changes stay possible on the in-cluster dashboard" | Add "and the cluster's receipts are shown there". |
| PRD `.memlog.md` line 251 (D1) | records "Sent; not yet confirmed by the cluster" | History; leave, superseded by the new entry. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 133 (Voice: Sent, not yet in effect) | "Sent; not yet confirmed by the cluster" | "Sent — not yet effective in the cluster"; extend to approvals and all decisions. |
| EXPERIENCE.md 174 (Settings row) | "shows 'Sent; not yet confirmed by the cluster'" | Same replacement. |
| EXPERIENCE.md 237 (State: Revocation takes effect) | "Until then the screen says 'Sent; not yet confirmed by the cluster'; the history shows both times (sent, confirmed)" | New wording; history "sent / applied by the cluster (receipt)"; add "Stop unconfirmed" state when no notice arrives. |
| EXPERIENCE.md 267 (Switch to alert-only) | "'Sent; not yet confirmed by the cluster' until the executor receives the switch" | Same replacement. |
| EXPERIENCE.md 141 (History) | "Approval withdrawn by Cris at 02:16 CET · confirmed by the cluster at 02:17 CET" | "… · applied by the cluster at 02:17 CET (receipt)". |
| EXPERIENCE.md 132 (After Approve) | "You approved at 02:14 CET." | Add the A14 states before "Waiting for Orvex technical approval". |
| DESIGN.md | no status token for "sent/unconfirmed" | May need a chip/state token for "not yet effective" and "unconfirmed" [new]. |

### 4. Conflicts
- None real. Wording update of a settled UX/PRD string (PRD memlog D1, 2026-11-03). Note the new "unconfirmed" outcome depends on the notifications channel (same dependency as AP-2).

---

## AP-4: Bounded offline validity (fresh / stale / expired)

### 1. Final decision to carry into the PRD
(AD-24 with A5/E13/E14 clock, E18 restore, consistency-check fix 1; AD-25; D12/AD-71.)
- Every signed authorisation object carries a validity end. Long-lived ones (ticks, policies, rosters, delegations, channel permissions) also need a fresh status statement signed by the relay.
- **Tiers by age of the last status statement:** **fresh** under 1 h (all authorised repairs); **stale** 1 h to under 24 h (only safe ticked repairs and safe policy repairs); **expired** at 24 h or more (no automatic repairs; observe and report). Values are starting assumptions to test.
- Local stops keep working against the cached roster. Cached outbound policies apply until expiry and are never widened on a failed refresh; after expiry only the heartbeat, a fixed data-free attention notice and recovery fetches (status statements, key lists) leave.
- **Clock and restart (A5):** statements carry an increasing signed sequence number; a repeated or older one never resets freshness. Age is measured with **local monotonic timing** while disconnected; **a reboot never extends validity**; if the age cannot be established after a restart, permissions count as **expired** until fresh confirmation. Future-dated statements beyond the allowed skew are refused; backward clock jumps alarm; an unsynchronised clock refuses time-limited approvals.
- **Restore (E18, consistency fix 1):** after a detected or known restore or reinstall, ordinary actions stay blocked and permissions count as expired; only authenticated recovery messages are processed; stops, revocations and switch-offs are reconciled with the relay before repairs resume; approvals from before the restore are not revived. A restore made while disconnected is detected only on reconnect.
- **Fleet outage (D12):** workloads are never stopped; Nightshift continues locally within these limits, so a Fleet outage longer than 24 h suspends automatic repairs on every affected cluster.
- **Limit:** a compromised host or cluster-admin can still manipulate time and stored state (AD-72).

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| FR-22, line 389 | "A ticked repair stays permitted until the customer unticks it (Amine)." | Add: "While the cluster cannot get a fresh confirmation from Quornex Fleet, permissions age: under 1 hour all authorised repairs run; from 1 to 24 hours only safe ticked and safe policy repairs run; from 24 hours no automatic repair runs and Nightshift only observes and reports. Restarting never extends this; if the cluster cannot tell how long it has been cut off, it treats its permissions as expired. Stops keep working (architecture, 2026-11-03 and 2026-11-15, AP-4; approved by Amine)." |
| FR-22, line 394 | "the executor … re-checks the authorisation: the tick or approval is still valid" | Add "and within its offline validity". |
| FR-51, lines 418-428 | policy repairs "never run in alert-only mode" | Add: "Policy repairs follow the offline limits of FR-22: in the stale tier only safe policy repairs; after 24 hours none." |
| FR-24, lines 402-406 | last-resort permission | Add: "The last-resort condition applies only while the cluster's permissions are fresh (FR-22)." (consequence of the tier rule; risky repairs are excluded from stale). |
| NFR-5, line 733 | "Each cluster keeps working on its own when central coordination is unavailable" | "… within bounded offline validity (FR-22): monitoring, stops, recording and already-authorised repairs continue; after 24 hours without confirmation, automatic repairs are suspended and the cluster only observes and reports." See Conflicts. |
| PRIV-9, lines 649-650 | "Only repairs that need no new approval can run: safe ticked repairs, policy repairs (FR-51) and … last-resort"; "Approvals already given stay valid until their validity ends" | Add "within the offline limits of FR-22". |
| SEC-8, line 686 | "enforcement keeps working when the cluster is cut off (NFR-5)" | Keep; add "including the offline limits (FR-22)". |
| FR-31, line 480 | "After restarting, Nightshift checks the real state." | Add "and its permission age (FR-22); a restored or reinstalled cluster blocks repairs until its permissions are re-established." |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 216-217 (Out of date; Repairs on an out-of-date cluster) | data-freshness states [O-1] | Add separate **permission-tier** states (not data freshness): "Limited: no confirmation from Orvex for 3 h · only safe repairs run" and "Automatic repairs suspended: no confirmation from Orvex for 24 h · watching and reporting only". Keep distinct from "Out of date" (data, about 2 min). |
| EXPERIENCE.md 168 (Health-grid tile), 50 (A1 tiles) | "No data / stale" | Add a tile/marker for the permission tier; "Clusters with no data or stale data" summary may add "repairs suspended". |
| EXPERIENCE.md 174 / 70 (Settings, B6b) | tick rows | Add one line: "Ticks stay valid while the cluster can reach Orvex; cut off for 24 h, automatic repairs pause." |
| open-items-2026-11-03.md O-1 | freshness threshold | Note: O-1 (data freshness) is not the permission tier; both now have starting values (about 2 min; 1 h / 24 h). |
| DESIGN.md 455-456 ("Green means verified") | stale hatch tokens | Suspended tier needs a non-green, worded state; may reuse `chip-stale` or a new token [new]. |

### 4. Conflicts
- **REAL: local autonomy vs 24 h suspension.** NFR-5 (line 733) "Each cluster keeps working on its own when central coordination is unavailable", Danny Exchange 4 ("Each cluster must still be able to look after itself"; "safe repairs should be automatic") and FR-22 line 389 ("A ticked repair stays permitted until the customer unticks it") vs AD-24/D12: after 24 h without Fleet status statements no automatic repair runs, including safe ticked repairs; a Fleet outage > 24 h suspends automatic repairs fleet-wide. This weakens a settled requirement (safety trade-off); needs Amine's explicit decision and probably a note to Danny.
- **REAL (smaller): last-resort while stale.** FR-24 has no connectivity condition; the stale tier allows only safe repairs, so a risky last-resort repair (the main use, FR-24 line 404) cannot run from 1 h offline.
- **REAL (smaller): PRIV-9 portal-off promise.** Lines 649-650 promise safe ticked, policy and last-resort repairs keep running and given approvals stay valid until their validity ends; the tiers cap this. Note: the relay status statements (flow 6) are proposed as required traffic (AP-8), so the portal channel being off does not by itself age the cluster; only lost Fleet contact does.

---

## AP-5: Documented reduced coverage for control-plane failures

### 1. Final decision to carry into the PRD
(P6, Amine 2026-11-03; AD-14; AD-49; failure catalogue.)
- No automatic repair that needs the Kubernetes API runs while the API is down. Kubernetes control-plane failures are reported and escalated to a person in v1. No API-independent repair helper ships in v1 (deferred; revisit when outage data shows how often such failures happen). The reduced coverage is documented.
- While the API is down: running pods, the checker, heartbeat, audit and outbox keep working; status "Kubernetes API unreachable: repairs paused", escalated (AD-49).
- Related catalogue limits (round 7): OMK control-plane certificate renewal is reported, not automated in v1; CoreDNS restart only as a tested risky repair.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| 3.1, line 97 ("Deferred:") | "Nightshift does not execute dangerous repairs in the first version" | Add: "Kubernetes control-plane failures are reported and escalated to a person in the first version: no automatic repair that needs the Kubernetes API runs while the API is down (architecture, 2026-11-03, AP-5; approved by Amine)." |
| FR-5, line 201 | "looks for symptoms such as the Kubernetes API becoming unreachable … and reports with the evidence" | Add: "While the Kubernetes API is unreachable, repairs that need it pause and the problem is escalated to a person." |
| FR-4, line 197 | independent checker runs "Kubernetes API connectivity" checks | No change; optional cross-reference to FR-5. |
| FR-20 | hardware faults | No change needed (AP-5 is about the control plane, not hardware); appendix B offered FR-20 only as an alternative home. |
| SM-9, line 753 | share of problems needing a person | Optional note: control-plane failures count as needing a person in v1. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md (no current string) | — | Add status "Kubernetes API unreachable: repairs paused" with escalation (Surface states table near 216-219, and A1 queue). |
| EXPERIENCE.md 156 ("What Nightshift cannot see") | limits of visibility | Optional line: "While your cluster's Kubernetes API is down, Nightshift can't repair; it tells you and Orvex." |

### 4. Conflicts
- **Scope reduction, not a contradiction:** Danny Exchange 4 ("Nightshift keeps the whole stack healthy, including OMK and Quornex … Kubernetes issues"; aim "as close to self-managing as possible") is a goal; no PRD FR requires automatic control-plane repair. Flag to Amine as a documented coverage limit that may need mentioning to Danny.

---

## AP-6: Code fixes hosted first

### 1. Final decision to carry into the PRD
(Round 4.1, Amine 2026-11-04 after Danny Exchange 3; AD-38; AD-26; prompt-injection decision 2026-11-15; appendix A flows 13-14.)
- Hosted inference is the main v1 approach for code fixes, **when the customer separately authorises** sending the relevant source code to a trusted, zero-retention provider. An in-cluster model is also supported where suitable hardware exists and the customer wants code to stay in the cluster. If neither is available or authorised, code fixes are unavailable; monitoring and catalogue-based repairs continue.
- Source-code consent stays **separate from external-AI consent (PRIV-8)** and **off until the customer opts in**; withdrawable; only relevant files sent, after secret scanning and the PRIV-4 check, with no exception; every transfer recorded (PRIV-7). Code fixes are the only flow that may carry source code (AD-26).
- **Limit:** the engineer's review and automated tests **reduce code-fix risk but do not guarantee safety** (prompt-injection decision); a planned validation with seeded malicious inputs (including source-code comments) is not completed and will be reported with scope, never as proof.
- Open: code-fix engineer access to the test environment (flow 14) needs its own consent and channel design.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| 3.1, line 94 | "experimental code fixes (an in-cluster model by default; a trusted hosted model only with the customer's separate, explicit consent)" | "experimental code fixes (a trusted, zero-retention hosted model when the customer separately authorises sending the relevant code; an in-cluster model where the hardware allows and the customer prefers it)". |
| FR-43 title, line 564 | "In-cluster by default, hosted only with explicit consent" | "Hosted first, with a separate source-code consent". |
| FR-43 body, line 565 | "By default, code fixes use a model on a GPU inside the customer's cluster … A customer without an in-cluster GPU can explicitly opt in…" | "Code fixes mainly use a trusted, zero-retention hosted model, only when the customer separately authorises sending the relevant source code. This consent is separate from external-AI consent (PRIV-8) and stays off until the customer opts in. A customer with suitable hardware who wants the code to stay in the cluster can use an in-cluster model instead (architecture, 2026-11-04, AP-6; approved by Amine)." |
| FR-43, line 566-567 | "Only the code relevant … recorded"; "can withdraw" | Keep; add "after secret scanning and the outbound check (PRIV-4)". |
| FR-43, line 568 | "Without an in-cluster GPU or this consent, code fixes are not available." | "Without this consent or a suitable in-cluster model, code fixes are not available; monitoring and catalogue repairs continue." |
| FR-43, line 569 | "Reason: … in-cluster only would leave the experiment with very few users" | Keep; it now supports hosted-first directly. |
| FR-44 step 1, line 572 | "with the customer's in-cluster model, or with a trusted hosted model if the customer has given the separate consent" | "with a trusted hosted model under the separate source-code consent (FR-43), or with an in-cluster model". |
| FR-44, line 580 | "no AI-written code reaches production without a person reading it" | Add: "The engineer's review and the automated tests reduce the risk of a harmful fix but do not guarantee safety." Engineer access (step 4) as an outbound path: open (flow 14). |
| PRIV-6, line 633 | "Code fixes use an in-cluster model by default; the relevant code goes to a trusted hosted model only with the customer's separate, explicit consent" | "The relevant code goes to a trusted, zero-retention hosted model only with the customer's separate, explicit source-code consent (FR-43); without it, code stays in the cluster. This is the only exception to PRIV-1." |
| PRIV-2, line 623 | "Raw data and secrets never leave the cluster; only approved, sanitised information does" | Add a cross-reference: "Source code under PRIV-6 is the one deliberate exception to 'sanitised', after secret scanning and PRIV-4." |
| PRIV-8, line 638 | "Sending source code stays a separate permission (FR-43)." | Keep. |
| Section 7, line 710 | "The in-cluster GPU stays an option, and it is the default for code fixes (FR-43)." | "The in-cluster GPU stays an option, including for code fixes where the customer wants code kept in the cluster (FR-43)." |
| Section 7 table, line 716 | "the default for code fixes (FR-43)" | Remove "the default for code fixes". |
| Section 10 item 7a, line 769 | "Code fixes use an in-cluster GPU by default…" | Restate as hosted first; "Does this fit Danny's wish…" can move to answered-by-decision (consistent with Exchange 3). |
| Addendum line 33 ("Code fixes: … secret scanning before any hosted-model call … engineer access as a channel") | design items | Secret scanning: answered (AD-26). Engineer access as a channel: still open (flow 14). |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 438 (Privacy table, Source code row) | "Off until the customer opts in (FR-43) \| Code fixes need an in-cluster GPU" | "Off until the customer opts in (FR-43) \| Code fixes aren't available unless you have an in-cluster AI model; monitoring and repairs continue." |
| EXPERIENCE.md 70 (B6b), 71 (Onboarding channel screen) | "source code" row | B6b consent wording for source code: "Can Nightshift send the code relevant to a fix to <provider>? The provider won't keep it after processing. An Orvex engineer reviews every fix before it can run." Separate from the external-AI question; nothing preselected. |
| EXPERIENCE.md 442 (External-AI consent wording) | "Can Nightshift send limited, checked information…" | Unchanged; keep "Source code is a separate permission". |
| Addendum line 20 (consent wording) | "Source code is a separate permission (FR-43)" | Unchanged. |

### 4. Conflicts
- **Settled PRD decision reversed, not a weakening:** PRD memlog 134 and 172 (Decision 2: "in-cluster GPU by default") are replaced. The protection (separate, explicit source-code consent, off by default) is kept, so PRIV-6's principle holds. Aligns with Danny Exchange 3 (hosted AI for 3 years) and PRD's own FR-43 reason. Wording update across 8 locations.
- **Open item, not a conflict:** engineer access to the test environment (FR-44 step 4) has no channel (appendix A flow 14).

---

## AP-7: Bounded probation rollback inside the update authorisation

### 1. Final decision to carry into the PRD
(Round 5.4 R2, Amine 2026-11-05; AD-45 with A8 dead-man switch; AD-68; AD-46.)
- A maintenance-policy update and a security update each include an exact, bounded rollback: back to the **named previous signed release**, only **within the probation window**, only **when the probation check fails**, and only if the release is **marked rollback-safe** (configuration, data and CRD compatibility). Otherwise no automatic rollback; a person is called. It preserves permissions, approvals and safety rules and is recorded like any change (FR-33). Any other rollback stays under the rollback policy or approval (FR-47).
- **Dead-man switch (A8):** a release passes probation only when the independent checker sends a fresh healthy signal tied to the exact release and probation attempt; if it is missing, the separate rollback guard triggers only the pre-authorised, rollback-safe recovery. The checker and guard are updated separately from routine releases. The guard can select only the pre-authorised recovery version (AD-68).
- **Limits:** shared node, network or Kubernetes API failures can still prevent recovery; false rollbacks are recorded; **rollback loops are prevented** (a release rolled back once is not re-applied automatically); escalation if recovery cannot complete. Its authority is the update authorisation, not NFR-4. Platform rollbacks stay under FR-47 (EKS: one minor version within 7 days; OMK: unknown).

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| FR-47, line 605 (Routine updates) and 606 (Security updates) | "run under a maintenance policy…"; "required by the customer contract…" | Add a bullet: "**Probation rollback.** Every routine or security update of Nightshift includes an exact, bounded rollback: back to the named previous signed release, only within the probation window, only when the probation check fails or no fresh healthy signal arrives, and only if the release is marked rollback-safe. It keeps permissions, approvals and safety rules. A release rolled back once is not re-applied automatically. If the rollback is not safe or cannot complete, a person is called. Shared node, network or API failures can still prevent recovery (architecture, 2026-11-05 and 2026-11-15, AP-7; approved by Amine)." |
| FR-47, line 607 | "Emergency rollback runs without fresh approval only if the customer has explicitly authorised that rollback policy in advance" | Add: "Any other rollback (outside the probation rollback above)…". |
| FR-32 table, line 492 | "Roll back a verified update under a rollback policy the customer authorised in advance (FR-47) \| The update path; a rollback must still work even if the bad update broke the normal update path … Whether that needs a separate tool is for the architecture" | Split: "Probation rollback within the update authorisation (FR-47) \| a separate rollback guard in each cluster, which works when the executor is broken"; keep the policy row for other rollbacks. Remove "Whether that needs a separate tool is for the architecture" (answered: yes, the guard). |
| FR-33, line 510 / FR-34 line 515 | "Everything … recorded"; outcomes | Add outcome/record note: probation rollbacks, including false rollbacks, are recorded. |
| Glossary "Maintenance policy", line 170 | "a separate rollback policy covers emergency rollbacks" | Add "except the bounded probation rollback included in each update (FR-47)". |
| SEC-9, line 688 | "a controlled, explicitly authorised rollback to an approved recovery version is allowed (FR-47)" | Keep; cross-reference FR-47 probation rollback. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md (no probation-rollback surface) | — | Customer history/morning summary entry: "Update v2.5 didn't pass its checks; Nightshift returned to v2.4 as your update settings allow." Orvex console (A4/A5): probation rollback and "not re-applied automatically" marker. |
| EXPERIENCE.md 352-357 (UJ fleet-wide rollback) | group rollback approved by Josh | Unaffected (that is an approved rollback, FR-32); optional note that the local probation rollback may already have run. |
| EXPERIENCE.md 443 (Agreed management policy) / B6 maintenance settings | — | If a maintenance-policy screen exists, add "Includes an automatic return to the previous version if the update fails its checks." |

### 4. Conflicts
- **REAL (needs explicit decision): security updates have no customer-authorised rollback policy.** FR-47 line 607 requires explicit advance customer authorisation of the rollback policy for a rollback without fresh approval; FR-47 line 606 makes security updates contractual (customer chooses only the window). AP-7 puts the rollback inside the security update's authorisation, i.e. authorised by contract, not by an explicit customer rollback policy. It is narrower (back to the release the customer already ran), but it changes a settled rule; FR-47 itself is "our proposal, pending Danny's confirmation".
- **Wording:** FR-32 row line 492 left "a separate tool" to the architecture; now answered.

---

## AP-8: Outbound paths that do not pass through the gateway

### 1. Final decision to carry into the PRD
(Round 9 reconcile C-1; D2 → AD-67; AD-27, AD-43, AD-32; AD-70; appendix A.)
- Every Nightshift pod denies ingress and egress by default; required internal connections, cluster DNS and Kubernetes API access are explicitly allowed; services authenticate callers; on EKS pods cannot reach instance metadata. Rules tested on OMK and EKS; enforcement gaps (a network plugin that does not enforce egress policy, host-network or privileged pods) are documented, not assumed away.
- **Exactly three paths bypass the gateway**, each with its own identity, destination allowlist and restrictions:
  1. the **Fleet heartbeat** from the independent checker (own path, fixed destination, rate limit, strict fixed-schema validator, which is that channel's outbound check);
  2. **Flux pulls** of signed releases, catalogue and model weights from the registry (registry allowlist, digest pinning, signature verification; requests carry no customer data);
  3. the optional **EKS AWS poller** calling the customer's own account Describe APIs (customer-granted read-only role; responses stay in the cluster).
- Everything else leaves only through the gateway.
- **Proposed PRIV-9 extension (appendix A, open points):** a named **"required service traffic"** for flows with no PRIV-9 channel: flow 6 (relay status statements, signed key lists, policy and roster updates: only cluster identity and versions out), flow 15 (signed package downloads; cannot be turned off because security updates are contractual), flow 16 (AWS poller, described as customer-account access, not data leaving to a third party), and flow 10 (the FR-12 signal to Orvex when the customer confirms something: proposed Fleet reports, to confirm). Flow 6a (data-free attention notice after the expired tier): channel to confirm. Flow 14 (code-fix engineer access): open.

### 2. PRD locations
| Location | Current text (short) | Proposed replacement |
|---|---|---|
| SEC-8, line 686 | "All data leaving the cluster passes through a separate gateway, which sends it only through the channels the customer permits (PRIV-9)" | "All data leaving the cluster passes through a separate gateway … with exactly three exceptions, each with its own identity, destination allowlist and restrictions: the Fleet heartbeat sent by the independent checker (FR-6), downloads of signed packages from Orvex's registry, and, on EKS, the optional read-only calls to the customer's own AWS account. Every Nightshift component denies network traffic by default except what it needs; gaps in enforcement are documented (architecture, 2026-11-11, AP-8, D2; approved by Amine)." |
| PRIV-9, line 644 | "The channels are: external AI…, the Quornex Fleet heartbeat (FR-6), Fleet reports…, notifications…, and the portal… The architecture assigns every other outbound flow to one of these channels" | Add a channel: "**required service traffic**: the cluster's requests for signed status confirmations, key lists, policies, rosters and signed packages, carrying only the cluster's identity and version numbers; accepted with the service like the heartbeat." Add: "Read-only calls to the customer's own AWS account (EKS) are access the customer grants, not data sent to a third party." Name the FR-12 signal's channel (Fleet reports, to confirm). |
| PRIV-9, line 645 | "Each permitted channel … passes the outbound check (PRIV-4). No channel, including the Fleet heartbeat, is silently exempt." | Add: "On the paths outside the gateway, the check is the path's own fixed schema or allowlist." |
| PRIV-4, line 629 | "a further test runs on every whole line about to leave, by every channel … mandatory, with no exceptions" | State how PRIV-4 applies to the three bypass paths (fixed-schema validator for the heartbeat; package requests and AWS calls carry no customer data). See Conflicts. |
| 3.2, line 106 | "Send anything out of the cluster through a channel the customer has not permitted (PRIV-9)." | Add "except the required service channels accepted with the service (FR-6, PRIV-9)". |
| FR-6, line 214 | "It is authenticated and passes the outbound check like any other channel" | "… on its own path, outside the gateway, checked by a strict fixed-schema validator (SEC-8)". |
| FR-12, line 306 | "Orvex receives a signal whenever the customer confirms something." | Add the channel (Fleet reports, to confirm) and what happens if it is off ("recorded locally; Orvex not told"). |
| Addendum line 32 | "egress only through the gateway (SEC-8)" | "egress only through the gateway, except the three named paths (SEC-8)". |
| Addendum line 50 | "The full list of outbound flows … assigned to PRIV-9 channels" | Mark answered by appendix A (draft), with flows 6a, 10 to confirm and 14 open. |
| NFR-2, line 730 | one design for both platforms | Optional: network rules tested on OMK and EKS with gaps documented. |

### 3. UX references
| File, line | Current | Proposed |
|---|---|---|
| EXPERIENCE.md 431-438 (Privacy & outbound channels table) | channels: heartbeat (required), Fleet reports, notifications, portal, external AI, source code | Add a row "Required service traffic: update and security downloads, status confirmations and key lists. Sends only this cluster's identity and version numbers. Required with the service." and on EKS "AWS read access (optional): read-only checks in your own AWS account; nothing is sent to Orvex from it." |
| EXPERIENCE.md 70-71 (B6b; Onboarding channel screen), 361 (UJ onboarding) | heartbeat as the only required item | Show both required items with purpose and fields. |
| EXPERIENCE.md 444 | "Notifications … go only through permitted channels." | Unchanged. |

### 4. Conflicts
- **REAL: required set beyond the heartbeat.** PRIV-9 (line 643, 646) and PRD item 22 (line 798) settled that **only** the heartbeat is required; everything else is explicitly permitted. Flows 6 and 15 cannot be turned off (appendix A). Adding a second required channel changes a settled decision (UX run, Amine 2026-11-03) and the onboarding screen.
- **REAL: PRIV-4 "no exceptions" vs bypass paths.** PRIV-4 (line 629) requires the test on every line, every channel; the three paths do not pass the gateway's PRIV-4 check (heartbeat: validator only; Flux and AWS: allowlists). The PRD must define the equivalent check or name the exception.
- **Wording:** SEC-8 "all data leaving … passes through a separate gateway" and addendum line 32 are factually superseded.
- **Not a conflict:** flow 15 "can't be turned off" is consistent with FR-47 (security updates required by contract).

---

## Candidate AP-9+ items (architecture decisions changing PRD-level behaviour, not in AP-1..AP-8)

Listed only; no change proposed until Amine decides.

| # | Architecture decision (source) | PRD/UX touched | Nature |
|---|---|---|---|
| C-1 | D15 / AD-51: settings changes on the in-cluster dashboard with **separate local passkeys** enrolled in advance via the roster; dashboard also allows **rejections and unticks**; never approvals; stable internal hostname | PRIV-9 line 651 (lists withdrawals, alert-only, settings), SEC-7 line 684, FR-15 332; UX 72, O-7 | Consistent with PRIV-9; adds rejections/unticks and local passkeys; closes O-7 partly. Not a conflict. |
| C-2 | AD-71 + A7 / consistency fix 3: **first installation authorised by the independently verified contract contact**; first-admin enrolment with split code (one half local, one half to the contract contact); disputed enrolment → pin not trusted, delayed recovery; installer never enrols | PRIV-9 line 646 ("an authenticated customer administrator reviews and confirms them, never the installer"), SEC-7; UX 366 | New PRD-level behaviour; check that "contract contact" vs "authenticated customer administrator" do not clash at onboarding. |
| C-3 | A10 / AD-2: request "closed as 'resolved, no longer needed' only after verification"; **bounded request capacity** with "approval request blocked: capacity full" and Orvex alert | FR-22 line 391 ("withdrawn if the problem resolves"), FR-14 line 322 ("Every problem that needs a person first appears…"), UX 226, 251 ("This request is no longer needed"), O-2 | Refines O-2/FR-22 (verification before closing); capacity-full means a problem can exist without an open request: possible weakening of FR-14; needs decision. |
| C-4 | AD-62 / A20 / D14: **BMC read-only in v1, power actions manual**; stateful takeover only with verified fencing, else manual; BMC-to-node UUID check | SEC-3 line 676 (separate component for hardware operations, "acting (for example a power cycle)"), FR-3 line 190, FR-20, FR-7; addendum "Silent nodes", "Hardware" | Narrows v1 scope (no automated power actions); PRD should say so. |
| C-5 | Status wording (spine conventions; A10, A11, A14, E3, E6, AD-49/50): "Sent — not yet effective in the cluster", "received/applied by cluster", "expired", "unreachable", "approval request blocked: capacity full", "Kubernetes API unreachable: repairs paused", "repairs suspended: storage full", "blocked: audit unavailable", "blocked: disruption budget or rate limit", "exhausted", "Confirmation code could not be sent", "SMS confirmation unavailable: approving with passkey only (reduced assurance)", "unreachable from Fleet", "not reporting", "gateway health check failed", "evidence collected, cause unknown, escalated", "AI explanation unavailable" | Addendum line 24 ("Final statuses, owned by the UX"), EXPERIENCE.md 185-186; FR-34 outcomes line 515 | New states pending UX review (consistency fix 8); "exhausted" vs FR-34 outcome list. |
| C-6 | A11 / AD-50: when storage is full, **stops and narrowly pre-authorised safe-stop steps are enforced even if they cannot be recorded**; missing records reported honestly | FR-33 line 510 ("Everything … recorded"), NFR-4 line 732 ("no repair is left half-done without being recorded"), FR-35 | Real tension with "everything recorded"; deliberate safety trade-off; needs PRD wording. |
| C-7 | AD-21: hardware provider is in no roster; a named customer person reports for them | FR-52 line 435 ("the customer, or their hardware provider" performs) | Real gap: who presses Start now / I've done it for a provider. |
| C-8 | D1 / A15 / AD-48: group approval via Fleet group-confirmation service; label "passkey + SMS verification attested by Fleet; not independently verified by the cluster"; SMS confirms a summary not the target list; customer permissions checked per cluster | FR-32 line 497; UX 128, 353-357, O-4 | Adds assurance limits to the settled group approval. |
| C-9 | A4 / E9 / AD-7: after a crash, an expired approval does not authorise new forward steps; retry only with valid authorisation and duplicate protections; A3: actions without verified fencing protection stay manual in v1 | FR-31 line 480 ("If continuing is safe, it continues") | Refinement; A3 may move some catalogue repairs to manual. |
| C-10 | A1 / AD-72: cluster-admin and node root are a documented security limit (Orvex on OMK, account operator on EKS can rewrite state, remove admission rules) | SEC-2 table, SEC-9, SM-4 line 746 | PRD claims nothing explicit, but SEC-9 "cannot forge" should state this limit. |
| C-11 | D13 / AD-56: two distinct reviewers before signing releases, the management policy and platform map | FR-46, FR-51 line 422 (two reviewers for entries) | Extension of an existing PRD rule. |
| C-12 | AD-25: unsynchronised clock refuses time-limited approvals; undo-reject window 2 min timed by the cluster (starting value) | FR-50 line 416 ("[OPEN] length, proposed by the architecture"), Section 10 last design item; UX O-13 | Closes an open PRD item with a starting value. |
| C-13 | E22 / E21: paused rollout never resumes on its own; last wave compared with each cluster's own pre-update health | FR-46 | Refinement. |
| C-14 | Appendix A flow 14: code-fix engineer access needs its own consent and channel | FR-44 step 4 line 575; addendum line 33 | Open item. |
