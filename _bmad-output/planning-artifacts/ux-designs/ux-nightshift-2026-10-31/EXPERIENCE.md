---
name: Nightshift
status: final
sources:
  - '{planning_artifacts}/prds/prd-nightshift-2026-10-28/prd.md'
  - '{planning_artifacts}/prds/prd-nightshift-2026-10-28/addendum.md'
  - '{planning_artifacts}/danny-qa-summary.md'
  - ./.memlog.md
  - ./.working/stale-decisions-2026-11-03.md
  - ./.working/open-items-2026-11-03.md
  - ./.working/triage-reviews-2026-11-03.md
  - ./.working/ia-proposal-v3.md
  - ./wireframes/flow-orvex-console-2026-11-03.excalidraw
  - ./wireframes/flow-customer-view-2026-11-03.excalidraw
  - ./mockups/color-themes-1.html
created: 2026-10-31
updated: 2026-11-03
---

# Nightshift: Experience Spine

> How Nightshift behaves for the people who watch it and the people who approve it. Visual specs live in [DESIGN.md](DESIGN.md). PRD content is cited by ID, not restated.

## Foundation

Two experiences, one product:

| Experience | Platform | Who | Density |
|---|---|---|---|
| **Orvex console** | Desktop web only, wide screens | The Orvex Nightshift engineer on duty (Josh); Orvex support in its own restricted role | Dense: compact tables, many rows |
| **Customer view** | Inside the Quornex portal (FR-15). Responsive: desktop for browsing, **phone-first for approvals** | The customer's business owner (shop owner, Cris, Samira); only authenticated customer administrators change settings (SEC-7) | Calm: large type, one thing at a time |

- **Slack, phone calls and text messages only notify in v1.** Every approval is given in the authenticated portal (FR-14). Every phone call is paired with a text message carrying the portal link, and customers can choose a text instead of a call (in the PRD, 2026-11-03).
- **No UI system is named.** Nightshift's tokens are neutral and get mapped onto the Quornex portal's design system later [OPEN: Orvex, O-12]. DESIGN.md is the visual reference.
- Light and dark modes exist for both experiences; the person or their device chooses.
- **Times carry their time zone** on screen ("Valid until 02:44 CET") [ASSUMPTION: shown in the viewer's own zone].
- **Wireframes** (low fidelity, Excalidraw): [Orvex console](wireframes/flow-orvex-console-2026-11-03.excalidraw) (A1–A5, A3-M) and [customer view](wireframes/flow-customer-view-2026-11-03.excalidraw) (Slack, B1–B6, B6b, B3-M). Each surface ID below matches its frame title. The 2026-10-31 files in `.working/` are superseded. Newer than the wireframes: the confirmation sheet, the "What we're asking" summary, collapsible sections, the new manual statuses and the role-labelled console actions.
- **Key-screen mocks** (Graphite Ledger, light and dark): [A1 fleet overview](mockups/key-a1-fleet-overview.html) (the console home: summary tiles, attention queue, health grid), [B3 approval](mockups/key-b3-approval.html) (phone approval, request open and after Approve) and [B3-M manual repair](mockups/key-b3m-manual-repair.html) (phone manual-repair approval, request open and after Approve). Colours come from the [palette sheet](mockups/color-themes-1.html); contrast measured on the mocks is in the [contrast report](mockups/contrast-measured.md).
- **The spines win on any conflict with a wireframe or mock**; names, times and IDs in wireframes and mocks are placeholders.
- **Wireframe strings superseded on 2026-11-03:** A5 "Blocked — no data from cluster since 02:10" (now "Current repair status unknown; last reported [status] at [time]", State Patterns › Freshness and cluster connection); the B6b note "strict no-outbound deployments can't use managed Fleet" (strict no-outbound is not offered in version 1); A3-M "pre-start check" (now "pre-run check").

## Information Architecture

### Orvex console (desktop)

Top navigation: **Fleet overview · Action history**, plus "Signed in: Josh (Nightshift engineer on duty)".

| Surface | Reached from | Purpose and content order |
|---|---|---|
| **A1 Fleet overview** (home) | Sign-in; nav | What needs attention in the first five seconds. **Summary tiles:** Approvals waiting for Orvex (count, oldest wait) · Critical problems · Fleet-wide problems (FR-32) · Clusters with no data or stale data. **Attention queue**, sorted by customer impact then time to impact; columns: Customer impact · Severity · Customer · Cluster(s) · Incident status · Time to impact · Approvals still needed · Updated. A customer in alert-only mode carries an "Alert-only" label. **Cluster health grid** in groups of 100 (a viewing option, not a limit on fleet size). **Pause live updates** control. Queue before grid: the engineer acts on problems, not clusters. |
| **A2 Problem detail** | Queue row | Header: problem, customer, cluster, customer impact, severity, incident status, mode ("Alert-only" when it applies), freshness. **Verified facts \| Nightshift's explanation** side by side. Timeline. What Nightshift cannot see (FR-5). Proposed repair (repair, risk level, expected interruption, what this changes) with **Review approval →**, or the "No tested repair" state (FR-19). Links the incident history to the validated repair (Danny, Exchange 5). |
| **A3 Approval review** | A2; Slack link | One repair. Same order as B3 plus technical depth: catalogue entry and version, safety preconditions (re-checked before it runs), the customer's permission, delegation, approval validity, the cluster's mode. **Role-labelled actions:** **Give Orvex technical approval** and, only for Orvex support where the customer has delegated, **Approve on the customer's behalf (delegated)**; plus **Reject**. The same person is never offered both approvals for one repair. In alert-only mode no approve action is offered. |
| **A3-M Manual repair needed** | A2; queue row; notification | A dangerous repair a person performs (FR-52). Technical depth: catalogue entry, pre-run check, the customer's personal approval, recovery-plan review, time window. **Give Orvex technical approval** · **Reject**. Then, for the performer only: the pre-run check, **Start now** and later **I've done it: check now**. |
| **A4 Fleet-wide problem** | "Fleet-wide problems" tile or its queue row | One problem in one problem group across many clusters (UJ-5). Step 1: the frozen set of clusters, with counts and each cluster's customer permission, safety checks and repair status (a check table). Step 2: the proposed rollback and **Approve rollback for these 288 clusters**, with the breakdown beside it. Step 3: gradual rollout by waves. See Authorisation & approvals › Fleet-wide. |
| **A5 Action history** | Nav | Filters: Time · Customer · Cluster · Risk level · Result · Who permitted it. Columns: Time · Customer · Cluster · Repair · Risk level · Who permitted it · Progress (repair status) · Result. Each row opens the full record (FR-34) as timeline entries. |
| **Orvex support** (restricted role) | Sign-in | Same console, restricted. Approves on a customer's behalf only where delegated; never manual dangerous repairs (FR-21, FR-52). Exact permissions [OPEN: architecture, O-9]. |

### Customer view (Quornex portal)

| Surface | Reached from | Purpose and content order |
|---|---|---|
| **Notifications**: Slack message; phone call with a text message | Outbound, per FR-13 | Notify only. Severity, cluster, one-sentence risk, "Nightshift proposes a repair that needs your approval", **Open in Quornex portal to review** (signs in). The text message carries the same portal link. No raw logs, secrets or customer data (PRIV-2–PRIV-4); allowed fields [OPEN: architecture, O-11]. |
| **B1 Home: my clusters** | Portal; sign-in | "Needs your decision (n)" first; Orvex-only info cards; then one cluster card per cluster. Combined across clusters (FR-15, PRIV-5). |
| **B2 Problem page** | Cluster card | FR-11 message first; Verified facts; Nightshift's explanation; What Nightshift cannot see; the proposed repair with **Review the proposed repair**, or the "No tested repair" state (FR-19); the no-answer line. |
| **B3 Approval** | "Needs your decision" card; B2; notification link | Phone, one column: the "What we're asking" summary, then sections 1–10 (Component Patterns › Approval card). |
| **B3-M Manual repair needed** | Same as B3 | Phone, one column: the "What we're asking" summary, then sections 1–11 (Component Patterns › Manual-repair panel). |
| **B4 Activity** | Portal nav; after an approval; "See full activity" | Timeline entries, newest first, all clusters (PagerDuty-style). Each repair: progress steps and "Who permitted it" (FR-33, FR-34). |
| **B5 Morning summary** | Portal, morning (FR-16) | "What happened · What Nightshift fixed · What Nightshift is still watching"; **See full activity**. |
| **B6 Settings: what Nightshift may do** | Portal settings; any "Ticked in your settings on 12 Oct" link | Mode; what Nightshift may read; repair checklist by risk level; last-resort condition; delegation to Orvex support; link to B6b. |
| **B6b Settings: data leaving your cluster & management policy** | B6 ("Data leaving your cluster and management policy ›") | Fleet heartbeat (required); other channels; external AI; source code; agreed management policy. |
| **Onboarding channel screen** | Starting the service | Same content as B6b, with onboarding defaults: an authenticated customer administrator reviews and confirms the pre-ticked service settings (never the installer); external AI is a separate opt-in consent (see Privacy & outbound channels). Not separately wireframed. |
| **In-cluster-only dashboard** | Inside the cluster [OPEN: architecture, O-7] | Shows problems when neither the portal nor notifications are permitted, and open requests when the portal is off. No approvals there; withdrawals, the switch to alert-only and settings stay possible (FR-15, PRIV-9). |

### Surface → journey closure

| Surface | Journeys that land there |
|---|---|
| Notifications (Slack, call with text) | UJ-1, UJ-2 (call), UJ-3, UJ-5, Flow 7 (call) |
| A1 | UJ-3, UJ-5 |
| A2 | UJ-3 |
| A3 | UJ-3, UJ-1 and UJ-2 (Orvex side) |
| A3-M | Flow 7 |
| A4 | UJ-5 |
| A5 | UJ-3, UJ-5, Flow 7 |
| Orvex support role | **None** (gap) |
| B1 | UJ-1 |
| B2 | UJ-1 |
| B3 | UJ-1, UJ-2 |
| B3-M | Flow 7 |
| B4 | UJ-1, UJ-2, UJ-4, Flow 7 |
| B5 | UJ-4 |
| B6 | Flow 6, UJ-4 (tick link) |
| B6b and onboarding channel screen | Flow 6 |
| In-cluster-only dashboard | **None** (gap; surface itself open) |

Gaps:

- **No journey exercises:** the Orvex support role; the in-cluster-only dashboard; **Dispute**, **Revoke delegation** and **Tick again** in B6; a manual repair performed by the customer or their hardware provider; handing the evidence to that provider (FR-20, FR-52).
- **Not wireframed or designed:** Flow 6's climax (the onboarding recap) has no wireframe. Phone-call and text-message content is not designed [OPEN: architecture, O-11].
- **Stated needs with no dedicated surface:** FR-15's per-cluster dashboard and live app health (only B1 cards and B2 today) and the alert-only presentation of a recommended repair.

## Voice and Tone

Plain words for a business owner who is not an infrastructure expert (FR-11). Every problem message follows FR-11's shape: current state and impact · time to impact · whether the cause is confirmed · what Nightshift did or proposes, with its expected interruption · for a request, what happens if nobody answers. The console uses the same words, with technical depth added below.

- **Templates, not AI, for unlabelled lines.** Lead sentences, card impact lines, notification lines and summary lines are built from templates over structured fields (impact, time to impact, repair, target). AI wording appears only inside the labelled explanation block. This is our version-1 design choice, not a SEC-1 requirement.
- **Plain explanations on tap.** On customer screens, technical words (for example replica, rollback, node, repair catalogue, Orvex technical approval) carry a short plain explanation that opens on tap, such as "Replica: a running copy of your program. You have only one, so restarting it pauses checkout briefly."

| Do | Don't |
|---|---|
| "Your checkout service is using more memory than usual. Purchases still work, but at this rate memory runs out in about 4 hours and checkout may become unavailable. We haven't confirmed the cause yet." | Error codes or Kubernetes terms as the message ("checkout-api OOMKilled") |
| "This is a likely explanation, not a confirmed cause." | Presenting the explanation as fact |
| "Approve this repair" · "Reject" · "Give Orvex technical approval" | "OK", "Confirm", "Submit" or one "Approve" that could stand for either of two approvals |
| "You approved at 02:14 CET. Waiting for Orvex technical approval." | "Pending" with no names; "Orvex is checking it" before anyone has looked |
| "Asked 02:13 CET · this request stays open until you decide or the problem goes away." | "Expires at 02:44" on an unanswered request (the wireframes still show it) |
| "1 new repair widens what Nightshift may do … It stays off until you accept it." | "Accept version 4" or "Until you accept it, version 3 stays in force" |
| "Out of date: last data 02:10 CET" | "Checkout works normally" on data that is out of date |

**Exact labels.**

| Where | Text |
|---|---|
| Customer approval buttons | **Approve this repair** · **Reject** |
| Console approval actions | **Give Orvex technical approval** · **Approve on the customer's behalf (delegated)** (Orvex support with delegation only) · **Reject** |
| Manual repair buttons | Customer: **Approve this manual repair** · **Reject**. Orvex: **Give Orvex technical approval** · **Reject**. Performer only: **Start now** (after the pre-run check passes, or the manual procedure has established its conditions), then **I've done it: check now** |
| Manual repair progress | "Work in progress" → "Nightshift is checking" (Verifying) → "Succeeded", "Mitigated" or "Problem still there" |
| Mitigated (manual, hardware) | "Connection stable on the standby interface. The network card still needs replacing; the problem stays open until it is replaced and Nightshift has checked that the cluster is healthy." |
| Fleet-wide | **Approve rollback for these 288 clusters**, beside "300 affected · 12 not included · 288 in this approval: 176 ready · 112 waiting for their customer's permission" |
| Fleet exclusion | "12 clusters aren't included: their Fleet reports are off, so Fleet can't confirm they have this problem. Their own Nightshift keeps watching them, and their local permissions still apply." |
| "What we're asking" summary | Three lines: the problem · the repair · what it means for you |
| Confirmation sheet | Restates the decision: "Approve the restart of checkout-api on shop-eu-1? Checkout may be unavailable for 30–60 seconds." Confirm button repeats the decision ("Approve this repair"); **Cancel** |
| After Approve | "You approved at 02:14 CET. Waiting for Orvex technical approval." "Your approval is valid until 02:44 CET. If Orvex hasn't approved by then, we'll ask you again." **Withdraw my approval** (until the repair starts) |
| Sent, not yet in effect | After a withdrawal, a switch to alert-only or an untick: "Sent; not yet confirmed by the cluster" until the executor in the cluster receives it |
| After manual Approve | "You approved this manual repair for tonight 01:00–03:00 CET. Waiting for Orvex technical approval." Console, once all approvals are in: "Approved for 01:00–03:00 CET. Ready for Marc (Orvex engineer)." |
| Request changed | Banner "This request has changed." with a way to open the new version; or "This request is no longer needed." Buttons disabled |
| Expected interruption | "No service interruption expected." (clear disposable temporary files) · "The application may be unavailable for approximately 30–60 seconds." (restart the only application replica) · "Connectivity may be interrupted. Duration unknown." (change network settings) |
| Recovery plan | A rollback is named only when it is certain. Otherwise: "This repair can't be undone (it's a restart). If it doesn't work, Nightshift tries the next safe repair or asks for approval; if it makes things worse, it stops repairs on this cluster and calls the Orvex engineer on duty." (FR-27, FR-28). Manual: "Review needed: Orvex reviews this plan before work starts" until reviewed, then "Reviewed by Josh (Orvex) at 00:20 CET" |
| No answer (customer) | "If you don't answer: we keep watching and change nothing that isn't already authorised." Last-resort variant (see Authorisation & approvals): "If you don't answer: we keep watching. Because you allowed it as a last resort, this repair may run on its own if failure is about 30 minutes away." Manual: "Nothing is changed. We keep watching and call you if it gets worse." |
| No answer (console) | "The repair waits. Nightshift alerts again and a backup engineer can step in. Nothing runs on silence." |
| Reject result (B3 after Reject) | "You rejected the restart of checkout-api at 02:15 CET." • This repair is blocked. • Your decision is recorded. • The other approvers (Orvex) will be told when the undo window ends. • Nightshift keeps watching shop-eu-1. • It won't ask for this repair again on its own, or swap in another repair to get around your decision. If the problem becomes critical or changes, it may ask you once more, showing that you rejected it. "Other automatic repairs keep working." **Undo reject** (for a short fixed window; the other approvers are told when it ends) · **Back to my clusters** |
| History | "Rejected by Cris at 02:15 CET" · "Approved on your behalf by Lea (Orvex support) at 01:03 CET" · "Approval withdrawn by Cris at 02:16 CET · confirmed by the cluster at 02:17 CET" · "Orvex technical approval not given before Cris's approval ran out at 23:10 CET; Cris was asked again" · manual: "Started 01:10 · reported done by Marc 01:22 · checked by Nightshift" |
| Freshness | "Updated 40 s ago" · "No data from cluster eu-2 since 02:10 CET. What you see may be out of date." · paused: "Live updates paused at 02:14 CET. Safety checks keep running on the server." |
| Repair status on stale data | "Current repair status unknown; last reported Waiting for approval at 02:10 CET" |
| Empty | "Nothing needs your decision right now." |
| Orvex-only info card | "For your information · shop-us-1 · Orvex is repairing a platform component. No effect on your service expected. No action needed." |

## Component Patterns

Behavioural. Visual specs in DESIGN.md › Components; names match.

| Component | Use | Behavioural rules |
|---|---|---|
| Status chips (severity, incident status, repair status, risk level, freshness) | Everywhere | Five separate fields, never merged. Each chip states its word; customer screens prefix the field ("Severity: Warning", "Status: Waiting for customer", "Repair status: Waiting for approval"). |
| Verified facts block | A2, A3, A3-M, B2, B3 | Only facts from the rule-based checks (SEC-1). Ends with its freshness line. Always separate from the explanation block. |
| Explanation block | A2, A3, B2, B3 | AI or template text; the label names the writer. Never contains the repair's action, target or steps: those render from structured catalogue fields only [OPEN: architecture, O-6]. |
| What Nightshift cannot see | A2, B2 | Lists the limits of visibility in words (FR-5), for example "Your application code (you allowed infrastructure only)." Neither fact nor explanation. |
| "What we're asking" summary | Top of B3 and B3-M | Exactly three lines: the problem, the repair, what it means for you, built from templates over structured fields. It summarises; the numbered sections below still hold everything decided. |
| Approval card | B3 (and B1's compact "Needs your decision" card) | One repair per approval; unrelated actions are never bundled. **B3 order:** "What we're asking" summary · 1 The problem (one sentence) · 2 Customer impact (now, and time to impact) · 3 The repair: exact action and target, with "What this changes" · 4 Risk level, in words · 5 Expected interruption · 6 Recovery plan · 7 Evidence: Verified facts, then Nightshift's explanation · 8 Approvals still required · 9 If you don't answer · 10 **Approve this repair** · **Reject**. Evidence and Recovery plan are collapsible, each with a one-line summary while closed [ASSUMPTION: they start closed]. Technical words open a plain explanation on tap. The repair and target come from structured data. **The card is bound to the version it shows** (see State Patterns › Decisions). |
| Manual-repair panel | B3-M, A3-M | **B3-M order:** "What we're asking" summary · 1 The problem · 2 Customer impact · 3 What this changes · 4 What will be done (catalogue steps, "Steps from Orvex's tested repair catalogue, not written by AI") · 5 Who will do it, and when (performer; time window) · 6 Risk level ("Dangerous: always done by a person, never automatically.") · 7 Expected interruption · 8 Recovery plan ("Review needed" until reviewed) · 9 Approvals still required · 10 If you don't answer · 11 **Approve this manual repair** · **Reject**. Recovery plan collapsible as in B3; its closed line keeps the review state. A3-M adds the pre-run check, the recovery-plan review and the time window as its own row (9) before approvals (10). Performer: an Orvex engineer for OMK/Quornex; the customer or their hardware provider for hardware and the customer's own app (FR-52). **Lifecycle:** all approvals in → the performer re-runs the pre-run check → **Start now** (Work in progress) → **I've done it: check now** (Verifying, "Nightshift is checking") → Succeeded, Mitigated or Problem still there. Only the named performer sees the performer actions [OPEN: architecture, O-8]. |
| Confirmation sheet | Approve (all kinds, including manual, Orvex technical and delegated), Reject, the fleet batch approval, Accept this change | The decision button opens the sheet; nothing is sent until the person confirms. The sheet restates the decision: action, target and expected interruption (fleet: the counts; policy: what the change widens). Confirm sends the decision with the version shown; **Cancel** returns with nothing sent. After an approval, **Withdraw my approval** stays available until the repair starts (fleet: for clusters whose rollback hasn't started); it takes effect when the executor in the cluster receives it (State Patterns › Decisions). After a rejection, **Undo reject** stays available for a short fixed window [OPEN: architecture, O-13]; undoing only reopens the request. The history keeps every step. |
| Primary button | Decision points | One per decision. Opens the confirmation sheet where one applies. Never sends a decision from Slack, a call or a text message. |
| Secondary button | Reject, Withdraw, Undo, Cancel, navigation actions | Reject opens the confirmation sheet like Approve. |
| Link | Navigation inside text | Navigates only; never commits a decision. "Ticked in your settings on 12 Oct" opens B6 wherever it appears. |
| Cluster card | B1 | One per cluster; the whole card opens B2. Shows the cluster name, severity and status chips when a problem is open, the impact line in words and the freshness line. The impact line comes from a template ("Checkout works normally"). **Out of date:** the impact line becomes "Out of date: last data 02:10 CET"; it never keeps healthy words. **Alert-only:** an "Alert-only" label beside the name. |
| Timeline entry | B4, A2 timeline, A5 full record | One entry per event or repair, newest first, time with zone. A repair entry shows its progress steps and "Who permitted it", naming the person for every approval (and "on your behalf" for delegated ones). Withdrawals and undone rejections stay as their own entries; a withdrawal, a switch to alert-only or an untick shows when it was sent and when the cluster confirmed it. [ASSUMPTION] An entry opens its full record. |
| Attention-queue row | A1 | Click opens A2 (or A4 for a fleet-wide row). Sort: customer impact, then time to impact. A refresh never moves the row in focus or the person's place in the list. A row whose cluster is out of date keeps its place; its impact reads "Out of date: last data 02:10 CET", time to impact "Unknown", Updated "Out of date (02:10 CET)". "Approvals still needed" reads in words: "Orvex technical approval", "Orvex technical approval only (platform repair)", "Customer: needed", "Manual repair needed: customer (personally) + Orvex, then a person performs it". |
| Summary tile | A1 top strip | Count plus one sub-line ("Oldest wait: 12 min"). Click filters to or opens the matching items; Fleet-wide problems opens A4. |
| Health-grid tile | A1 | One tile per cluster, group selector "Group: clusters 201–300 ▾". Tiles: Critical problem · Warning · No open problem · No data / stale · "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation". All labelled in the legend. [ASSUMPTION] Clicking a tile with a problem opens its A2. |
| Freshness line | Every panel and card | Shows the age of the data, not of the page. Past the threshold the panel becomes a stale panel. In the console, **Pause live updates** freezes the screen with a visible paused state until **Resume live updates**; server-side safety checks stay live. |
| Stale panel | Any panel past threshold | Replaces health colour with hatch and words. Keeps the last known values and says they may be out of date; never healthy words as the headline. |
| Info card | B1 | Orvex-only platform repair shown as information, not a request. No buttons. |
| Check table | A3, A3-M, A4 | Lists each safety precondition or pre-run check with Pass / Fail. Re-run right before the repair runs (FR-22); for a manual repair, the performer re-runs it just before starting. **A failed check blocks the work, and a fresh approval can't override it** (FR-22, SEC-8). An inconclusive check blocks too; for a manual repair only, the defined manual procedure may establish the conditions (State Patterns › Surface states). In A4 it is the per-cluster table, with a repair-status column. |
| Progress steps | B3 after Approve, B4, A5, A4 waves | Repair-status words with arrows. Ticked repairs skip "Waiting for approval". Manual: "Manual repair needed → Work in progress → Verifying → Succeeded / Mitigated / Problem still there", with who reported it done and that Nightshift checked it. Notes such as "undone" or "made things worse" sit next to Failed. A4 wave labels ("Waiting for later waves") are progress counts, not repair statuses. |
| Settings row | B6, B6b, onboarding | Changes are recorded and notified; only administrators can change them (SEC-7). An untick or a switch to alert-only shows "Sent; not yet confirmed by the cluster" until the executor receives it. Each channel row says what "No" means. A tick row says "A tick covers only this tested action under these conditions." **Accept this change** opens the confirmation sheet. |

## State Patterns

### Severity, statuses and risk

| Field | Values | FR-13 notification level (severity only) |
|---|---|---|
| **Severity** | Critical | Phone call, paired with a text message carrying the portal link (or a text only, if the customer chose it). Only when failure is happening or imminent |
| | Warning | Alert when a decision is needed; otherwise dashboard. A prediction like UJ-1's (checkout works; memory runs out in about 4 hours) is Warning; it becomes Critical, and Nightshift calls, only when failure is imminent |
| | Informational | Dashboard and morning summary |
| **Incident status** (problems) | Being watched · Needs attention · Waiting for customer · Waiting for Orvex · Resolved | |
| **Repair status** (repairs) | Waiting for approval · Manual repair needed · Work in progress · Running · Verifying · Succeeded · Mitigated · Problem still there · Failed · Rejected · Blocked · Cancelled · Expired | |
| **Risk level** | Safe · Risky · Dangerous | |
| **Freshness** | Current ("Updated 40 s ago") · Out of date | |

Freshness is not a repair status. Colours per DESIGN.md: `{colors.critical-fill}`, `{colors.warning-fill}`, `{colors.info-fill}`, `{colors.waiting-fill}`, `{colors.success-fill}`, `{colors.neutral-fill}`, stale hatch `{colors.stale-hatch-base}` / `{colors.stale-hatch-stripe}`.

### Repair status → FR-34 outcome

| Final repair status | FR-34 outcome |
|---|---|
| Succeeded | worked |
| Failed, undone | did not work and undone |
| Failed, can't be undone | did not work and could not be undone |
| Failed (error while running) | failed |
| Failed, recovery failed | recovery failed |
| Failed, made things worse | harmful |
| Blocked (including a manual repair whose pre-run check failed) | blocked |
| Cancelled | cancelled |
| Manual: Succeeded after Nightshift's check | manual repair reported done; verification: problem gone |
| Manual: Mitigated | manual repair reported done; verification: workaround holds, fault still open (FR-20) |
| Manual: Problem still there | manual repair reported done; verification: problem still there |
| Rejected · Expired | recorded requests (FR-50, FR-22) |

Manual repair needed and Work in progress are not final. "Who permitted it" sources: ticked in your settings · agreed management policy (version) · approved at the time (by whom, when, on whose behalf) · last-resort condition.

### Freshness and cluster connection

| State | Treatment |
|---|---|
| Current | "Updated 40 s ago" on every panel (FR-15, in the PRD 2026-11-03) |
| Out of date (past the threshold) [OPEN: architecture, O-1] | Grey hatch and words: "No data from cluster eu-2 since 02:10 CET. What you see may be out of date." Queue and customer card: the impact line becomes "Out of date: last data 02:10 CET"; time to impact "Unknown". **Never a stale green, never healthy words on stale data.** |
| Repairs on an out-of-date cluster | "Current repair status unknown; last reported Waiting for approval at 02:10 CET" (A5, B4), with the stale hatch. Local enforcement keeps running in the cluster (NFR-5, SEC-8), so the screen never implies that a repair blocked locally has become unblocked. |
| Fleet reports off | "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation". A4 explains the exclusion (Voice and Tone › Fleet exclusion). |
| Heartbeat not permitted / remote monitoring disabled | **Never shown.** The heartbeat is required (Privacy & outbound channels; in the PRD, 2026-11-03) |
| Limited visibility | What Nightshift cannot see (FR-5) |
| Live updates paused (console) | Visible paused state and time; the screen stops changing until resumed; server-side safety checks stay live |

### Approval validity

- **Only a given approval expires** (FR-22). How long it stays valid is a field of each repair catalogue entry; the UX only displays it: "Valid until 02:44 CET" [OPEN: architecture, O-2]. A material change cancels it sooner. If it runs out unused, Nightshift asks again and the history records it.
- **An unanswered request never expires.** It stays open, always shows current evidence ("Asked 02:13 CET · this request stays open until you decide or the problem goes away"), is re-issued if the evidence or conditions materially change and is withdrawn if the problem resolves (in the PRD, 2026-11-03).
- **Two approvals, one runs out first:** the person whose approval ran out is told "Your approval ran out at 23:10 CET; you were asked again", and the history records it. Who is re-asked and how [OPEN: architecture, O-3].
- **Fleet-wide approval across waves:** recorded per cluster, each cluster re-checked, progress by wave. Each cluster runs only while it holds a valid, unexpired approval; a later wave never reuses an expired one, and Josh is asked again for the remaining clusters. How he is re-asked [OPEN: architecture, O-4].
- **Manual repairs:** approvers approve a stated time window ("tonight 01:00–03:00 CET"). **The window limits when work may start.** If work can't start inside it, the approvers are asked again. Work already in progress when the window ends is finished or recovered under the reviewed recovery plan, never abandoned; the history notes it (an accepted design proposal). A3-M shows the window as "proposed by the performer" [ASSUMPTION: from the wireframe, not the record].
- **Recovery-plan review (manual):** the plan shows "Review needed" until the Orvex engineer who gives technical approval has reviewed it. A review that materially changes it needs renewed approval from the relevant approvers, including the customer where their production is affected (FR-52). That engineer may also perform the work.

### Decisions

- **Bound to the version shown.** The screen freezes the version of the request it shows; content is never swapped in place. If the request is re-issued or withdrawn, a banner says "This request has changed" or "This request is no longer needed", and both buttons stay disabled until the person opens the new version. The decision carries the version ID and is **validated again on the server**, not only by disabling buttons. "Try again" never resends a decision made on an old version.
- **Confirm, withdraw, undo:** see Component Patterns › Confirmation sheet.
- **Several people deciding.** A Reject by any required approver blocks execution (FR-50). Among a customer's administrators the first decision counts and the others see it, with name and time; this never stops an authorised person withdrawing an approval or rejecting before the repair starts. The server orders decisions consistently, and the history keeps every step and names the person for every approval.
- **Revocation takes effect in the cluster.** A withdrawal, a switch to alert-only or an untick takes effect when the executor in the cluster receives it. Until then the screen says "Sent; not yet confirmed by the cluster"; the history shows both times (sent, confirmed). The validity set per catalogue entry caps how long an approval can live. With the portal off, these stay possible on the in-cluster dashboard (PRIV-9).
- **Sign-in on the way to a decision.** After sign-in (from a notification link or a session that ran out), the pending request is preserved (never an unsent approval) and its current version and conditions are revalidated before the buttons are offered. A warning comes before the session times out, with a way to stay signed in. Sign-in accepts password managers, paste and passkeys. Mechanism [OPEN: architecture, O-5].

### Surface states

| State | Surface | Treatment |
|---|---|---|
| Nothing pending | B1 | "Nothing needs your decision right now." |
| No open problems | A1 | [ASSUMPTION] Empty queue says so in words; grid tiles show "No open problem" (never green). |
| Nothing found or nothing yet | A5, B4, B5 | [ASSUMPTION] A5: "No repairs match these filters." B4: "No activity yet." B5 after a quiet night: says in words that nothing needed fixing. |
| Cold load | All | [ASSUMPTION] Neutral placeholders with no status colour until data arrives; the freshness line appears with the first data. |
| Page or data can't load | All | [ASSUMPTION] Says so in words, keeps whatever is already shown marked as possibly out of date and offers to try again. |
| Decision not recorded (network or server error) | B3, B3-M, A3, A3-M, A4 | [ASSUMPTION] The screen stays on the request, says the decision was not recorded and offers to try again. It never shows "approved" before the portal has recorded it. "Try again" re-reads the request and never resends a decision made on an old version. |
| Settings change not saved | B6, B6b, onboarding | [ASSUMPTION] Same rule as a decision not recorded: the screen keeps the person's choice, says it wasn't saved and never shows it as saved. |
| Request withdrawn | B3, B3-M, A3, A3-M | Banner "This request is no longer needed." No buttons remain. |
| Request re-issued | B3, B3-M, A3, A3-M | Banner "This request has changed."; both buttons disabled until the new version is opened. Any approval given on the old version no longer counts (FR-22). |
| Already answered by someone else | B3, B3-M, A3, A3-M | The screen shows each decision already made, with name and time. Any authorised approver can still reject before the repair starts. |
| May not approve | B3, B3-M | [ASSUMPTION] "You can't approve this request", saying who can; no approve button. Approver roles [OPEN: architecture, O-5]. |
| No tested repair (FR-19) | A2, B2 | The proposed-repair section is replaced by: no tested repair exists, so Nightshift changes nothing; what it is unsure about; that it has escalated. [ASSUMPTION] Exact wording and who is told. |
| After Reject, problem gets worse | B3 | One new request at most, showing the earlier rejection (FR-50). |
| Manual: pre-run check fails | A3-M, B3-M | The work doesn't start. Repair status Blocked. A fresh approval can't override a failed check (FR-22, SEC-8). |
| Manual: remote pre-run check inconclusive | A3-M, B3-M | Blocked, unless the defined manual procedure establishes the required conditions with alternative evidence (out-of-band access, an onsite inspection). The record holds who verified each condition, the evidence, the approvals and the recovery plan. Missing telemetry alone never waives a check; if no safe procedure can be established, the repair stays blocked and is escalated (FR-22, FR-52). |
| Manual: work outside the procedure | A3-M, B4, A5 | Recorded as it happened. Authorisation and safety-check compliance are shown as separate lines, so an inconclusive check alone never makes the work read as unapproved. |
| Manual: work in progress | A3-M, B3-M, A1 | "Work in progress", with who started it and when. The repair coordinator (FR-29) blocks conflicting repairs on the target, never necessary recovery actions. |
| Manual: Mitigated | A3-M, B3-M, B1, A1 | The problem stays open (never Resolved). It closes only after the hardware is replaced and Nightshift's own health check passes; the customer's confirmation alone isn't enough. |
| Manual: problem still there | A3-M, B3-M | "Problem still there". [ASSUMPTION] The problem stays open; next step not recorded. |
| Tick out of date | B6 | "Tick again" badge: "A release changed this repair's action, conditions or risk level. Tick it again to keep allowing it." (FR-22) |
| Policy change pending | B6b | The widening action is "Off until you accept it"; the rest of the version already applies (FR-51). |
| Disputed classification | B6 | Follows the customer-production rules until Orvex re-reviews (FR-21). |
| Alert-only mode | B1, B2, B6, A1, A2, A3 | Nightshift informs and recommends; it changes nothing, including Orvex's routine platform repairs. No approval requests. The console shows "Alert-only" on A1, A2 and A3 and offers no approve action. [ASSUMPTION] B2 shows the recommended repair without approval buttons. |
| Switch to alert-only with authorisations pending | Customer, console | Pending Nightshift execution authorisations (approvals given but not used) are cancelled and recorded as Cancelled, and the approvers are told. "Sent; not yet confirmed by the cluster" until the executor receives the switch. |
| Portal access turned off | Customer, console | New remote approvals are blocked. Ticks, the management policy and last-resort permissions are not revoked. Notifications go only through permitted channels. Approvals already given stay valid until their validity ends or the repair runs (the executor verifies them in the cluster, SEC-9); open requests can no longer be answered remotely and stay visible on the in-cluster dashboard, where withdrawals, alert-only and settings stay possible; the change is recorded and told through the channels still permitted (PRIV-9, in the PRD 2026-11-03). |
| Portal not permitted | Customer | No approvals possible; only safe ticked, policy and last-resort repairs run (PRIV-9). |
| Portal and notifications not permitted | Customer | Problems only on the in-cluster dashboard [OPEN: architecture, O-7]. |
| Not an administrator | B6, B6b | [ASSUMPTION] Read-only, with "Only administrators can change these; every change is recorded and you are notified." |
| Orvex support, not delegated | A3, A3-M | [ASSUMPTION] The delegated action is not offered and the screen says why. Exact permissions [OPEN: architecture, O-9]. |

## Interaction Primitives

- **Console:** mouse and keyboard on desktop. Click a queue row → A2; a summary tile → its items; **Review approval →** → A3; a history row → full record. Dropdown filters in A5 and a group selector in A1.
- **Keyboard:** navigation is supported throughout both experiences. No custom keyboard shortcuts (the PRD specifies none).
- **Customer:** tap and scroll in one column on a phone. Notifications deep-link through sign-in to the request (State Patterns › Decisions).
- **Decisions:** through the confirmation sheet (Component Patterns), bound to the version shown (State Patterns › Decisions). Step-up authentication and approver roles [OPEN: architecture, O-5].
- **Live data:** [ASSUMPTION] Panels refresh on their own. A refresh never moves the person's focus or place; the console can pause live updates (Component Patterns › Freshness line).
- **Banned:** approving from Slack, a phone call or a text message (v1) · bundling unrelated actions in one approval · one approve button that could stand for two approvals · rendering the action or target from AI text · sending a decision made on an old version · sending a decision automatically after sign-in · resubmitting a rejected request automatically · substituting a different repair to get around a rejection · treating silence as permission.

## Accessibility Floor

Behavioural. Contrast values live in DESIGN.md › Colors.

- **WCAG 2.2 AA is an untested design target.** Compliance is never claimed.
- Colour is never the only signal: every chip, tile and panel repeats its meaning in words. Out-of-date data is hatched **and** labelled.
- Contrast: token pairs are computed at ≥4.5:1 for text and ≥3:1 for focus rings (DESIGN.md); contrast is to be measured in the rendered result (key-screen mocks: [contrast report](mockups/contrast-measured.md)).
- A visible focus ring on every interactive element. Controls and clickable cards are outlined in `{colors.text-secondary}`, never only by the faint `{colors.border}`.
- Keyboard navigation throughout; auto-refresh keeps the person's focus.
- Consequential decisions are confirmed and reversible within their window (confirmation sheet, withdraw, undo).
- Accessible sign-in and session warnings (State Patterns › Decisions; O-5).
- A person who can't use a phone call can choose a text message instead (in the PRD, 2026-11-03).
- Phone approvals: the three-line summary first, one column, numbered sections, plain explanations on tap, full-width buttons at the end. [ASSUMPTION] Tap targets ≥44px; operable one-handed.
- [ASSUMPTION] Tab order follows the numbered order; status changes ("Verifying" → "Succeeded") are announced to screen readers; text scales to 200% without losing content.

## Key Flows

UJ names mirror the PRD. Screens: see Information Architecture. Times omit the zone here; screens show it.

### UJ-1. The shop owner is warned hours before checkout fails

1. The owner's checkout service on shop-eu-1 is using more and more memory; the trend becomes a real risk (FR-9). Checkout still works and failure is about 4 hours away, so severity is **Warning**: an alert, no phone call (FR-13).
2. Slack: "shop-eu-1: checkout may become unavailable in about 4 hours. Nightshift proposes a repair that needs your approval." He taps **Open in Quornex portal to review** and signs in.
3. B1 shows "Needs your decision (1)". He opens B2: the FR-11 message, Verified facts, Nightshift's explanation (written by AI), what Nightshift cannot see.
4. **Review the proposed repair** opens B3. "What we're asking" tells him in three lines: checkout is running out of memory; Nightshift proposes restarting it; checkout may pause for 30–60 seconds. Below: restart checkout-api (its only replica, with "replica" explained on tap); risky, not ticked, so "You: needed · Orvex technical approval: needed"; the restart can't be undone, and the recovery plan says what happens if it doesn't work.
5. He taps **Approve this repair**; the confirmation sheet restates the restart and its interruption; he confirms. "You approved at 02:14. Waiting for Orvex technical approval." "Your approval is valid until 02:44." **Withdraw my approval** stays available until the repair starts.
6. Josh gives Orvex technical approval in A3 (UJ-3 path).
7. **Climax:** progress moves Running → Verifying → **Succeeded**: Nightshift applied the fix and checked that it worked. Where the repair can be undone and doesn't work, Nightshift undoes it.
8. B4 shows the repair, both approvals by name and the result; it appears in the morning summary.

Failure: no answer → the request stays open, Nightshift keeps watching and changes nothing that isn't already authorised; if failure becomes imminent, severity rises to Critical and Nightshift calls. The request changes while he reads → the banner appears and the buttons stay disabled until he opens the new version. **Reject** → confirmation sheet, then the Reject result, with **Undo reject** for a short fixed window, after which Orvex is told (FR-50). His approval runs out before Orvex approves → he is asked again. The repair doesn't work → "Failed — did not work, undone" or the next step from the recovery plan (FR-27).

### UJ-2. Cris approves a rollback while checkout is failing

1. Checkout on Cris's shop is failing: severity Critical, so Nightshift calls him and sends a text message with the portal link (FR-13).
2. He opens the link and signs in; the request is waiting in B3: "What we're asking", then the problem in plain words and the proposed rollback.
3. The rollback is risky, so "You: needed · Orvex technical approval: needed".
4. He taps **Approve this repair** and confirms in the sheet: "You approved at 21:22. Waiting for Orvex technical approval."
5. The Orvex engineer gives Orvex technical approval in A3.
6. **Climax:** the rollback runs; Nightshift confirms the recovery once it has checked that checkout works again (Verifying → Succeeded).
7. B4: "Who permitted it: Approved by Cris at 21:22 · Orvex technical approval by Josh at 21:25." It also appears in the morning summary.

Failure: Orvex has not approved before Cris's approval runs out → "Orvex technical approval not given before Cris's approval ran out at 23:10; Cris was asked again" ([OPEN: architecture, O-3]). The rollback makes things worse → "Failed — made things worse, repairs stopped on this cluster" (FR-28).

### UJ-3. Josh approves a ticked risky repair

1. Customer C-0142's checkout-api on shop-eu-1 has memory creep and runs as a single replica. The customer ticked "Restart the only replica" on 12 Oct; the tick supplies the customer's permission, but the repair is risky, so it still needs Orvex technical approval. Slack notifies the Orvex team.
2. Josh opens the Orvex console. A1: "Approvals waiting for Orvex"; queue row "Checkout may stop for all shoppers · Critical · Customer C-0142 · shop-eu-1 · Needs attention · About 40 min · Orvex technical approval".
3. A2: Verified facts (memory 71% → 93% in 3 hours; limit in about 40 min; 1 of 1 replicas) beside Nightshift's explanation; what Nightshift cannot see.
4. **Review approval →** A3: catalogue entry restart-only-replica v3; safety preconditions all Pass; customer's permission "Ticked in settings on 12 Oct (risky repair: still needs Orvex technical approval each time)"; delegation not used.
5. **Climax:** he clicks **Give Orvex technical approval** and confirms in the sheet. Nightshift re-checks the conditions, restarts the replica, verifies recovery and records it: A5 "Waiting for approval → Running → Verifying → Succeeded", "Ticked by customer, 12 Oct · Orvex technical approval by Josh at 02:14".
6. The customer sees it in the morning summary.

Failure: Josh doesn't answer → the repair waits, Nightshift alerts again and a backup engineer can step in; nothing runs on silence (FR-23). A precondition fails at run time → Blocked. **Reject** → "Rejected by Josh".

### UJ-4. Samira reads the night's summary

1. At 9 AM Samira opens the portal on her phone: B5, "Good morning, Samira. Last night, 23:00–09:00".
2. **Climax:** she reads "Checkout recovered at 02:25 after the rollback you authorised." She had ticked it in her settings in advance.
3. What happened: "02:05: checkout started failing for some of your customers. 02:25: checkout recovered." What Nightshift fixed: the rollback ("Authorised by you. Worked.") and cleared temporary files ("Ticked in your settings. Worked."). What Nightshift is still watching: image service memory, no impact.
4. **See full activity** opens B4; "Ticked in your settings" opens B6.

She knows what happened overnight without having been woken. Failure path: not applicable; a failed or rejected repair would appear with its FR-34 outcome.

### UJ-5. Josh handles one big problem across 300 clusters

1. Josh gets one consolidated urgent alert: "Quornex Fleet: correlated update failure. Critical. 300 affected clusters · 1 fleet-wide problem · suspected update: v2.4" (FR-32).
2. A1: Fleet-wide problems "Same problem on 300 clusters"; he opens A4.
3. Step 1: the frozen set. "300 affected · 12 not included · 288 in this approval: 176 ready · 112 waiting for their customer's permission", with the reason the 12 are excluded (Voice and Tone › Fleet exclusion). Each of the 288 shows its customer's permission, its own safety checks and its repair status.
4. Step 2: "Roll back the Quornex update v2.4 to the previous version on each affected cluster"; risk level and expected interruption from the catalogue entry.
5. **Climax:** he clicks **Approve rollback for these 288 clusters**; the confirmation sheet restates the counts; he confirms. His approval is recorded separately for each of the 288; it never replaces a customer's required permission or a cluster's own safety checks. Clusters added to the problem later need a new approval, and each cluster runs only while it holds a valid, unexpired approval.
6. Step 3: the rollback runs gradually by waves: "Wave 1 of 6 done. Succeeded 48 · Running 20 · Verifying 5 · Blocked 2 · Waiting for customer permission 112 · Waiting for later waves 101". The 176 ready clusters run as their waves come if their checks pass; the 112 wait for their customer (FR-47).
7. He watches the clusters recover; A5 shows "approved by Josh at 02:05 (fleet approval, recorded for this cluster)".

Failure: a cluster fails its own safety check → Blocked ("Fail: another repair is running"). A cluster's rollback doesn't work → "Failed — undone after it didn't work". Josh's approval runs out mid-rollout → the remaining clusters don't run; a later wave never reuses the expired approval, and Josh is asked again for them ([OPEN: architecture, O-4]).

### Flow 6. Samira sets up what Nightshift may do

1. Samira starts the service. Onboarding opens the channel screen (B6b content). The Fleet heartbeat is shown as required, with its purpose and exact fields.
2. Signed in as an authenticated customer administrator, she reviews the service settings (Fleet diagnostic reports, notifications and portal access, pre-ticked) and keeps them.
3. External AI is opt-in consent and starts with nothing selected; she chooses **No**: nothing is sent to an AI provider; local tools are used instead.
4. The repair checklist (B6 content) starts with safe repairs ticked; she also ticks "Restart the only replica of an application" (risky: still needs Orvex technical approval each time).
5. She lets Orvex support approve risky repairs on her behalf (delegation scope "Risky repairs · all my clusters").
6. **Climax:** she confirms the recap; her confirmation of the service settings is recorded (by her as an administrator, never by the installer). Legal basis [OPEN: legal review, PRD Section 10 item 23].
7. Later: version 4 arrives with the current release. Its changes within what Samira agreed already apply; one new repair widens what Nightshift may do, so it stays off until she reads it and accepts it (confirmation sheet).

Failure: she unticks the portal → she is told that no approvals will be possible. [ASSUMPTION] Onboarding reuses the B6 checklist and delegation rows; the recap is not wireframed.

### Flow 7. Cris approves a manual repair; Marc performs it

1. 23:50: the network card on node n-7 of shop-us-1 is failing. The matching repair is dangerous, so the request is "Manual repair needed" (FR-52). Critical: Nightshift calls Cris and sends a text message with the portal link.
2. Cris opens B3-M: "What we're asking" (the problem, the manual repair, what it means for him), then the problem; impact ("Now: everything works. In about 1 hour: checkout may slow down or stop."); What this changes: your production; the catalogue steps; who: an Orvex engineer, when: tonight 01:00–03:00; Dangerous; "Connectivity may be interrupted. Duration unknown."; recovery plan "Review needed: Orvex reviews this plan before work starts"; "Your own approval is needed: Orvex support can't approve this on your behalf."
3. He taps **Approve this manual repair** and confirms in the sheet (23:58): "You approved this manual repair for tonight 01:00–03:00. Waiting for Orvex technical approval."
4. Josh opens A3-M, reviews the recovery plan without material change and gives Orvex technical approval (00:20): "Approved for 01:00–03:00. Ready for Marc (Orvex engineer)." Had the review materially changed the plan, Cris would have been asked again.
5. 01:10: Marc re-runs Nightshift's pre-run check; the evidence still holds. He presses **Start now**: repair status Work in progress. The coordinator blocks conflicting repairs on n-7, never necessary recovery actions.
6. He performs the catalogue steps and, at 01:22, presses **I've done it: check now**. Repair status: Verifying ("Nightshift is checking").
7. **Climax:** Nightshift's check: the connection is stable on the standby interface. Repair status **Mitigated**: the network card still needs replacing, and the problem stays open until it is replaced and Nightshift's own health check passes.
8. Morning: Cris sees in B4 who did what under which approvals: "Approved by Cris at 23:58 · Orvex technical approval and recovery plan reviewed by Josh at 00:20 · Started 01:10 · reported done by Marc 01:22 · checked by Nightshift: Mitigated".

Failure: Marc can't start inside the window → the approvers are asked again. The pre-run check fails → Blocked; a fresh approval can't override it. It is inconclusive remotely → blocked unless the manual procedure establishes the conditions; otherwise escalated (State Patterns › Surface states). The window ends mid-work → finished or recovered, never abandoned (State Patterns › Approval validity). After the check: "Problem still there".

## Inspiration & Anti-patterns

- **Lifted from Grafana:** monitoring dashboards and grouped fleet views (console).
- **Lifted from Better Stack:** the formal, professional look (console).
- **Lifted from PagerDuty, simplified:** incident status, notifications and action history as a timeline (customer view).
- All three are references for look and feel, not integrations. Nightshift's approval requirements stay explicit in both views.
- **Rejected — approving in Slack (v1):** narrows FR-14's earlier Slack option; Slack links to the portal.
- **Rejected — one status field:** severity, incident status and repair status are separate; the challenge brief's "Fixed on its own / Waiting for a person / Being watched" was replaced.
- **Rejected — the heartbeat as an optional checkbox:** Amine chose none of the AI's four onboarding options.
- **Rejected — one-tap decisions with the result screen as the only confirmation:** replaced by the confirmation sheet with withdraw and undo.
- **Rejected — solid saturated status blocks** (the Clinical Contrast palette).
- **Rejected — AI-written repair steps:** steps come only from the repair catalogue (FR-17, FR-52).

## Responsive & Platform

| Surface | Platform | Behaviour |
|---|---|---|
| Orvex console (A1–A5, A3-M) | Desktop web, wide screens only | Dense tables; tables scroll horizontally rather than drop columns. No phone layout in v1. |
| B3, B3-M, B1, B2, B5 | Phone-first, responsive | One column (≈360px reference in the palette sheet). On desktop the same column, wider. The confirmation sheet is a bottom sheet on a phone, a small dialog on desktop. |
| B4 | Desktop, also responsive on phone | Timeline. |
| B6, B6b, onboarding | Desktop-first | One simple screen each; responsive [ASSUMPTION]. |
| Slack, phone call, text message | Notify only | Link to the portal; no decisions. |

Breakpoints are not decided [ASSUMPTION: the portal's own]. The PRD's journeys say Josh opens requests "in the portal"; here that is the Orvex console [ASSUMPTION: the console is the Orvex-side authenticated portal surface].

## Authorisation & approvals

How the UX shows FR-21. "What this changes" decides who must approve; when classification is in doubt or disputed, the customer-production row applies.

| What this changes | Safe | Risky | Dangerous |
|---|---|---|---|
| **Orvex platform only** | In the agreed management policy: runs; history "Ran under the agreed management policy (v3)". Not in the policy: Orvex technical approval (A3, queue "Orvex technical approval only (platform repair)"). Customer sees an info card. | Orvex technical approval (A3). Customer sees an info card. | Manual (A3-M): an authorised Orvex engineer approves; the recovery plan is reviewed. |
| **Your production** | Ticked: runs; history "Ticked in your settings on 12 Oct". Not ticked: customer approval (B3). | Ticked: the tick supplies the customer's permission; Orvex technical approval each time (A3, UJ-3). Not ticked: customer **and** Orvex (B3 + A3; UJ-1, UJ-2). | Manual (B3-M + A3-M): the customer approves personally, never through delegation; Orvex technical approval; recovery plan reviewed by the Orvex engineer who gives technical approval (in the PRD, 2026-11-03). |

- **One repair per approval**, tied to the exact repair, target, catalogue version and evidence shown (PRD Glossary, "Approval"; State Patterns › Decisions).
- **Separate, role-labelled approvals.** Where both are required, customer approval and Orvex technical approval come from two different people (also when Orvex support approves on the customer's behalf), each through its own labelled action; the same person is never offered both for one repair. The Orvex approver may also perform the manual work. Identity mechanism [OPEN: architecture, O-5].
- **A tick covers only its tested action under its conditions.** A release that changes them shows "Tick again" (FR-22).
- **Delegation:** "Orvex support may approve on my behalf", with a scope, "You're notified of every approval made on your behalf", "You can revoke at any time", "Never covers manual dangerous repairs: you approve those yourself." History names the person: "Approved on your behalf by Lea (Orvex support)".
- **Fleet-wide (A4):** one Orvex approval for clusters with the same problem in the same problem group, recorded per cluster. The targets are frozen at the click and displayed with their counts; clusters added later need a new approval. Orvex approves the candidates, but execution on each cluster waits for its customer's permission and its own checks; rollout is gradual. Each target needs a valid, unexpired approval before it runs; a later wave can't reuse an expired one (Josh is asked again for the remaining clusters). A group approval never covers a manual repair.
- **Last-resort condition** (B6, per repair, safe and risky only; FR-24). Its no-answer line on B3 appears only when every required permission exists and the safety checks pass. It grants no extra permission and never overrides a rejection, alert-only mode or the dangerous / manual restrictions (FR-50, FR-52). The 30-minute threshold is an [ASSUMPTION].
- **Reject** (the one home for these rules): blocks execution of that repair for this occurrence, records it, tells the other approvers, keeps monitoring; no auto-resubmission, no substitute repair; other automatic repairs keep working; at most one new request if the problem becomes critical or materially changes, showing the rejection (FR-50). **Undo reject** within a short fixed window [OPEN: architecture, O-13]; undoing only reopens the request, it approves nothing.
- **Alert-only mode:** nothing is executed, including policy repairs; no approval requests; switching to it cancels pending execution authorisations (State Patterns › Surface states).

## Privacy & outbound channels

Screen: B6b in settings, and the same content at onboarding.

| Channel | At onboarding | What "No" means (shown on screen) |
|---|---|---|
| **Fleet heartbeat** | **Required for the managed service**, not a checkbox. "Tells Orvex this cluster's Nightshift is running. Sends only: agent ID, timestamp, alive/degraded. Authenticated and checked before it leaves. Explained and accepted when you start the service." | Not available: a strict no-outbound deployment is not offered in version 1; managed Nightshift needs the Fleet heartbeat |
| Fleet diagnostic reports | Pre-ticked service setting | "This cluster is left out of fleet-wide problem detection." |
| Notifications (Slack; phone call with a text message, or a text only) | Pre-ticked service setting | "You won't be alerted or called; check the portal." |
| Portal access | Pre-ticked service setting | "No approvals are possible; only safe ticked repairs, policy repairs and last-resort repairs run. With notifications also off, problems show only on a dashboard inside your cluster." Turning it off later: State Patterns › Surface states. |
| External AI | **Nothing selected**: opt-in consent (PRIV-8) | "Nothing is sent to an AI provider; local tools are used instead." |
| Source code (separate permission) | Off until the customer opts in (FR-43) | Code fixes need an in-cluster GPU |

- **Service settings, not consent.** Fleet diagnostic reports, notifications and portal access start pre-ticked on the basis of the service contract. An authenticated customer administrator reviews and confirms them (never the installer) and can untick any. The screen never calls them consent or permission. External AI is the only consent here: opt-in, nothing preselected. Legal basis [OPEN: legal review, PRD Section 10 item 23].
- **Phone calls:** every call comes with a text message carrying the portal link; the customer can choose a text instead of a call (in the PRD, 2026-11-03). Content within the allowed fields [OPEN: architecture, O-11].
- **External-AI consent wording:** "Provider: <name>. Can Nightshift send limited, checked information about problems to this AI provider? The provider won't keep it after processing." Yes / No, nothing preselected.
- **Agreed management policy** (corrected FR-51): "Version 4, installed with the current release on 2 Nov · Scope agreed on 20 Oct". "Version 4 changes within what you agreed already apply." "Within what you agreed" means conditions no less restrictive; corrected steps are still tested and reviewed. Anything else is listed and "stays off until you accept it" (the customer can dispute it, as in FR-21); a repair that can affect customer production leaves the policy and follows FR-21: **Read what changed** · **Accept this change** (confirmation sheet). "Read the policy (13 routine platform repairs)". The UX never says the whole old policy or software version stays in force while acceptance is pending.
- Notifications carry no raw logs, secrets or customer data and go only through permitted channels.
- Only administrators change these; every change is recorded and notified (SEC-7).

## Open items

Behaviour above is fixed; the mechanism or value belongs to architecture or Orvex. IDs are O-n so they don't clash with screen IDs.

| # | Open detail | What the UX already fixes | Owner |
|---|---|---|---|
| O-1 | Freshness threshold | "Updated 40 s ago"; past it, grey hatch and words; never a stale green or healthy words | Architecture (PRD item 8) |
| O-2 | Approval validity values per catalogue entry | "Valid until 02:44 CET" once given; unanswered requests don't expire | Orvex / architecture |
| O-3 | Two approvals needed, one runs out first: who is re-asked and how | "Your approval ran out at 23:10 CET; you were asked again"; recorded | Architecture |
| O-4 | Fleet-wide approval across waves: how Josh is re-asked for the remaining clusters | Recorded per cluster; targets frozen; each re-checked; progress by wave; each target needs a valid, unexpired approval; never reused once expired | Architecture |
| O-5 | Approver roles, step-up authentication, portal identity mapping, enforcing two different people; accessible sign-in | Approval only in the authenticated portal; role-labelled approvals from two different people; sign-in allows password managers, paste and passkeys; a warning before the session times out, with a way to stay signed in; after sign-in the pending request is preserved (never an unsent approval) and revalidated | Architecture |
| O-6 | Rendering action and target only from structured data; neutralising attacker-controlled names and links | Repair, target and steps never come from AI text | Architecture |
| O-7 | In-cluster-only dashboard: where it runs, how it is reached | Shows problems when neither portal nor notifications are permitted, and open requests when the portal is off; no approvals; withdrawals, alert-only and settings possible | Architecture |
| O-8 | Who may press the performer actions (**Start now**, **I've done it: check now**), and how it is authenticated | Only the named performer sees them; Nightshift checks before closing | Architecture |
| O-9 | Orvex support's exact permissions | Same console, restricted; delegated approvals only; never manual dangerous repairs | Architecture |
| O-10 | Signals that decide "can affect customer production" | Displays the catalogue field and Dispute; in doubt, customer-production rules | Architecture |
| O-11 | What a Slack message, phone call or text message may contain | No raw logs, secrets or customer data; links to the portal | Architecture |
| O-12 | Mapping neutral tokens onto the Quornex portal's design system | Neutral tokens in DESIGN.md | Orvex |
| O-13 | Length of the undo-reject window | Short and fixed; the other approvers are told when it ends; undo only reopens the request | Architecture |

**PRD changes from this UX work** (the ten items queued in `.working/open-items-2026-11-03.md`, the portal-off rule and decisions D1–D4) are in the PRD as of 2026-11-03; the record is the PRD's `.memlog.md`.

**Deferred review findings** (product decisions and polish for the next UX Update): [`.working/open-items-2026-11-03.md`](.working/open-items-2026-11-03.md), section 3 "Deferred review findings (next UX Update)".
