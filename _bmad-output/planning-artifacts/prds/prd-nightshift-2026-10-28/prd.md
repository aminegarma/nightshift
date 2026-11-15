---
title: "PRD: Nightshift"
status: final
created: 2026-10-28
updated: 2026-11-15
---

# PRD: Nightshift

Status: final (2026-10-31), updated and final again on 2026-11-02 with Danny's Exchange 5, the changes from the UX work and the fixes from the review of the update; updated on 2026-11-03. Updated on 2026-11-15 to reconcile the PRD with the final architecture (architecture-nightshift-2026-11-03: proposed changes AP-1 to AP-20 and Amine's decisions on seven conflicts); status draft while this update is in review. Those changes are tagged "(architecture AP-n, Amine, 2026-11-15)"; the change report is `update-notes-2026-11-15.md`. Each section was drafted from Amine's answers and the record, and reviewed by Amine; inline tags give the source of each statement.

## 1. Vision

Nightshift is the operations agent that runs inside every Quornex cluster. It keeps watch over the whole stack, reading logs and metrics. On OMK, it has access from the customer's hardware and the operating system up through Kubernetes and Quornex's platform services. On hosted Kubernetes such as EKS, it works with the signals the provider makes available, plus Kubernetes and Quornex's platform services. If the customer opts in, it also watches the customer's own app. It alerts before the system fails, explains problems in plain words, and carries out the repairs it is authorised to make (Amine, rephrased in places with Codex).

Orvex's ambition is to make affordable sovereign cloud accessible to a million companies, including small businesses without specialist infrastructure teams. Nightshift is central to making that service reliable and economical to operate (Amine, after Danny, Exchange 3). Orvex aims to run its software on 10,000 clusters across customer bare-metal and hosted Kubernetes environments. For Orvex, Nightshift replaces much of the DevOps work that would otherwise be needed, and makes the remaining engineers' work much easier. Each cluster looks after itself when central coordination is unavailable, within bounded offline limits (FR-22), including when it is one of many clusters coordinated by a customer control cluster. Meanwhile, Orvex manages the fleet efficiently. For the customer, Nightshift means they can operate their own cloud at low cost, with a public-cloud-like experience and control over their data and compute. Raw data and secrets never leave the cluster; only approved, sanitised information does, through the channels the customer permits.

The first version must prove four things:
- Nightshift detects problems.
- It provides evidence-based explanations for supported problems and states uncertainty when the cause is unknown.
- It performs authorised repairs without harming the app or the cluster. Zero harm is the goal: every harmful repair is counted and reviewed.
- It shows whether it really replaces engineers, and so whether it costs Orvex less or more than those engineers would.

**How this PRD is organised:**
- Sections 2 and 3: who Nightshift serves, its key journeys and what is in and out of the first version.
- Section 4: the Glossary of terms the requirements use.
- Section 5: the features (FR-1 to FR-52; FR-50 to FR-52 were added on 2026-11-02 and sit in the sections they belong to), from observing a cluster to managing the fleet.
- Sections 6 and 7: privacy, security and cost constraints (PRIV, SEC, COST), and the model options.
- Sections 8 and 9: non-functional requirements and success metrics.
- Sections 10 and 11: open questions, and what the other hand-in documents must contain.

## 2. Users and key journeys

**Users** (product brief):
- **Primary: the Orvex Nightshift team.** They watch over Nightshift itself and give Orvex technical approval for risky repairs (Amine; product brief), including risky changes to OMK and Quornex (Danny, Exchange 5), and before manual dangerous repairs (FR-52). About 15 engineers, one on night duty (Amine's estimate, to test).
- **Secondary: the customer's business owner** (or another senior person). Not a technical expert; they chose Quornex so they would not need DevOps staff.
- **Secondary: Orvex support.** They handle customer problems and answer approval requests when a customer delegates approval to them.

**Key journeys** (narrated by Amine and structured by the AI; additions accepted by Amine):

**UJ-1. The shop owner is warned hours before checkout fails.** *(From the example night in Amine's product brief.)*
- **Persona and context:** the owner of an online shop running on several Quornex clusters.
- **Entry:** at night, the checkout service's memory is growing steadily. Once the trend becomes a real risk (FR-9), Nightshift alerts the owner, and Orvex support if the contract says so.
- **Path:** the message says that checkout still works but memory runs out in about 4 hours and that the cause is not confirmed yet; it also proposes a fix. If nobody answers, Nightshift keeps watching and changes nothing that is not already authorised.
- **Climax:** the owner approves; Nightshift applies the fix, checks that it worked, and undoes it if it did not work and can be undone.
- **Resolution:** checkout never fails. Without Nightshift, shoppers would have noticed first, the owner second and Orvex last.
- Realises FR-8 to FR-11, FR-21, FR-25.

**UJ-2. Cris approves a rollback while checkout is failing.**
- **Persona and context:** Cris owns an online shop running on Quornex.
- **Entry:** checkout is failing. Because checkout is critical, Nightshift calls him (FR-13), and he opens the approval request in the portal.
- **Path:** Nightshift explains the problem in plain words and proposes a rollback. Cris approves.
- **Climax:** the rollback is done, and Nightshift confirms the recovery once it has checked that checkout works again.
- **Resolution:** checkout is back; the action and his approval are in the record and the morning summary.
- **Edge case:** if the rollback is a risky repair, Orvex technical approval from the Nightshift team is needed as well as Cris's approval (FR-21, our conservative interpretation of Danny's approval model for the customer's own app), so Cris is told that Orvex technical approval is still needed.
- Realises FR-11, FR-13, FR-14, FR-21, FR-25.

**UJ-3. Josh approves a ticked risky repair.** *(Drafted by the AI from FR-21; accepted by Amine, 2026-10-31.)*
- **Persona and context:** Josh is the Nightshift engineer on night duty.
- **Entry:** a customer's service has memory creep and runs as a single replica. The repair, restarting the only replica, is risky; the customer has ticked it in their settings, so it needs only Orvex technical approval, which Josh gives (FR-21, our conservative interpretation of Danny's approval model for the customer's own app).
- **Path:** Josh is notified in Slack and opens the request in the portal, where he signs in (FR-14). He sees the facts from the rule-based checks (memory trend, time to impact) separately from the AI's explanation, plus the customer's tick and the repair's safety conditions.
- **Climax:** he approves. Nightshift re-checks the conditions, restarts the replica, verifies that the service recovered, and records everything.
- **Resolution:** the customer sees it in the morning summary.
- **Edge case:** if Josh does not answer in time, the repair waits, Nightshift alerts again, and a backup engineer can step in. Nothing runs on silence.
- Realises FR-11, FR-14, FR-21, FR-22, FR-23, FR-25, SEC-1.

**UJ-4. Samira reads the night's summary.**
- **Persona and context:** Samira is a customer's business owner.
- **Entry:** at 9 AM she opens the morning summary.
- **Path and climax:** she reads: "Checkout recovered at 2:25 AM after the rollback you authorised." She had permitted this rollback in advance by ticking it in her settings.
- **Resolution:** she knows what happened overnight without having been woken up.
- Realises FR-16, FR-21, FR-34.

**UJ-5. Josh handles one big problem across 300 clusters.**
- **Persona and context:** Josh is the Orvex Nightshift engineer on night duty.
- **Entry:** he gets one consolidated urgent alert about a single fleet-wide problem affecting 300 clusters (FR-32).
- **Path:** he reviews the evidence and impact, then checks the proposed solution and which approvals it requires.
- **Climax:** he approves.
- **Resolution:** he watches the result as the clusters recover.
- **Edge case:** Josh's approval is the authorised Orvex engineer's approval that a risky platform change needs; because the rollback affects customer production, the customer's approval is needed as well (Danny, Exchange 5). For customers who have authorised a rollback policy in advance, the rollback runs if its safety conditions pass; for the others, it waits for each customer's approval (FR-47; FR-32).
- Realises FR-6, FR-21, FR-32, FR-47.

## 3. Scope and non-goals

### 3.1 In the first version
Everything in Sections 5 to 7 (product brief; Danny wants feedback on everything in real use). That includes:
- watching Kubernetes and the platform services on OMK and EKS, and the customer's hardware on OMK, within what out-of-band management allows;
- the customer's own app, if they opt in;
- prediction and plain-language explanations;
- ticked and approved repairs, including the last-resort condition;
- routine platform repairs under the agreed management policy (FR-51);
- phone calls, alerts, dashboards and the morning summary;
- fleet learning;
- experimental code fixes (a trusted, zero-retention hosted model when the customer separately authorises sending the relevant code; an in-cluster model where the hardware allows and the customer prefers it; FR-43; architecture AP-6, Amine, 2026-11-15);
- all three model options, the external ones only with the customer's consent (PRIV-8), and working without any AI (Section 7).

Deferred: Nightshift does not execute dangerous repairs in the first version; they are manual (FR-52; Danny, Exchange 5). Code fixes might not stay after the first version (Danny, Exchange 2). Kubernetes control-plane failures are reported and escalated to a person in the first version, not repaired automatically (FR-5; architecture AP-5, Amine, 2026-11-15). Nightshift performs no hardware power actions in the first version: its hardware management access is read-only (SEC-3; architecture AP-10, Amine, 2026-11-15).

### 3.2 Non-goals: what Nightshift never does
- Modify or delete customer records, databases or backups, even with approval or in an emergency (product brief Ground Rules). Nightshift still has permitted diagnostic access (Amine).
- Improvise repairs, or run commands or scripts the AI generated (FR-17).
- Execute a dangerous repair in the first version (FR-52).
- Treat silence as permission: no answer grants no new permission. A repair already authorised may still run when nobody answers, if its conditions pass (FR-23; Amine).
- Physically repair hardware, or contact a customer's hardware provider directly (5.4).
- Take over the provider's responsibilities on hosted Kubernetes (Glossary).
- Send anything out of the cluster through a channel the customer has not permitted, other than the required Fleet service channel accepted with the service (PRIV-9; architecture AP-8, Amine, 2026-11-15).
- Offer a strict no-outbound deployment in the first version: managed Nightshift needs the Fleet service channel, including the Fleet heartbeat (FR-6, PRIV-9). This is a documented limitation (Amine, 2026-11-03, review of the update).
- Move private data out of the cluster it came from, even between one customer's clusters (PRIV-1).
- Treat text in logs as instructions (SEC-1).

## 4. Glossary

**Platforms and components.** Nightshift supports OMK on bare metal and hosted Kubernetes such as EKS. According to Danny's latest clarification (Exchange 4), customers are responsible for the hardware, while OMK manages the operating system and Kubernetes. Exact hardware ownership and hosting arrangements may vary (Amine).

- **Out-of-band management**: a separate hardware management interface on a server (BMC/Redfish or equivalent) that still answers when the server's main network or operating system is down, and reports power status and hardware health. Required for full bare-metal management (Amine, with Codex).
- **Limited-visibility mode**: how Nightshift runs on a server without working out-of-band management: reduced hardware coverage, acknowledged by the customer during Orvex's installation process and recorded by Nightshift in the monitoring coverage report (Amine).
- **Monitoring coverage report**: Nightshift's record of what it can and cannot see in each cluster, including limitations such as missing out-of-band management (Amine).
- **Customer hardware**: the physical servers, disks, network cards, power supplies and network equipment a cluster runs on with OMK. It may be badly configured and run by customers who may have very little infrastructure expertise (Danny, Exchange 4). The customer is responsible for it, including replacing broken components (Danny, Exchange 4; "including replacing broken components" is Amine's reading). Nightshift detects problems in it but cannot physically replace broken parts.
- **OMK (Orvex Managed Kubernetes)**: what Orvex provides on bare metal to manage the operating system and Kubernetes on customer hardware (Danny, Exchange 4).
- **Quornex**: Orvex's developer cloud, running on top of OMK or hosted Kubernetes. It provides databases, queues, storage and application deployment, fully managed by Orvex (`brief.pdf`; Danny, Exchange 4).
- **Hosted Kubernetes (such as EKS)**: Kubernetes run by a cloud provider; the provider remains responsible for Kubernetes and the underlying infrastructure (Danny, Exchange 4). Nightshift respects the provider's management responsibilities and works with the monitoring access the provider makes available (Amine).
- **Quornex Fleet**: Orvex's central, multi-tenant management platform, hosted and managed by Orvex on a hosting provider (Danny, Exchange 4). It does not mean customer applications run there (Amine). [DESIGN ASSUMPTION unless Danny confirms: its exact internal components.]
- **Customer control cluster**: an optional cluster a customer runs to manage several of their workload clusters. It hosts the Nightshift management agent (Danny, Exchange 4).
- **Workload cluster**: a cluster that runs a customer's applications. It belongs to one customer and runs its own Nightshift agent (Danny, Exchanges 1 and 4).
- **Nightshift agent**: the Nightshift instance in a workload cluster. It operates locally (Danny, Exchange 4; Amine).
- **Nightshift management agent**: the Nightshift instance on a customer control cluster. It coordinates the Nightshift agents across that customer's workload clusters (Danny, Exchange 4).

**Problems and catalogues.**

- **Fault**: an underlying technical problem, such as a failing hard disk or a broken component (Amine, with Codex).
- **Failure**: a service failing, for example when it cannot read data (Amine, with Codex).
- **Incident**: a service disruption experienced by users, for example when they cannot access the app (Amine, with Codex). This definition replaces the product brief addendum's definition, "one failure, however many alerts it fires".
- **Problem**: any fault, failure or incident Nightshift may face. The catalogues hold problems, and every problem is treated the same way: if it is in the repair catalogue, its known repairs and their risk levels apply, whatever it is called; if it is in neither catalogue, it is handled as new (Amine).
- **Supported problem**: a problem with an entry in the incident catalogue or the repair catalogue, which Nightshift can explain with evidence. This includes problems it cannot repair, most likely power, network-card (NIC) or failing-physical-disk problems (Amine).
- **Incident catalogue**: the list of supported problems whose fix is not yet tested or confirmed. Every entry defines the evidence, explanation, uncertainty and escalation for one problem (Amine).
- **Repair catalogue**: the list of problems whose fix is known. Every entry holds one problem and one or more repairs; each repair defines the action, its safety preconditions, risk level, whether it can affect customer production (FR-21), expected interruption, authorisation, approval validity, verification and rollback (Amine; expected interruption from the UX work, 2026-10-31; approval validity: Amine, 2026-11-03, UX work). It also holds problems Nightshift can never fix itself but whose fix is known, such as replacing a disk or network card or checking a power supply; for these, Nightshift suggests the fix to the customer (Amine).
- **Customer-specific entry**: a repair catalogue entry, such as a code fix, that applies to one customer only; only that customer can access or execute it (Amine).

**Risk.**

- **Risk level**: every repair in the repair catalogue has one of three risk levels, from lowest to highest: safe, risky, dangerous. A problem may have several repairs, each with its own risk level (Amine). Orvex sets each repair's risk level when it tests the repair catalogue entry; customers cannot change it (Amine). Example (from another Claude conversation, pasted by Amine):

  | Repair (for one affected service) | Example risk |
  |---|---|
  | Move traffic to a healthy replica | Safe |
  | Restart an affected replica, when the healthy replicas can carry the traffic and all safety checks pass | Safe |
  | Restart the only replica | Risky |
  | Force-restart the only production instance | Dangerous |

  The same action can have different risk levels depending on its conditions; each catalogue repair states the conditions its risk level assumes (Amine, 2026-10-30).
- **Safe repair**: a repair that will not interrupt the customer's service or lose data (Amine). Example: disk cleanup.
- **Risky repair**: a repair that can interrupt a service or reduce redundancy (Amine). Example: restarting the only replica. (Restarting one replica while healthy replicas carry the traffic and all checks pass is safe; Amine, 2026-10-30.)
- **Dangerous repair**: a repair whose side effects could corrupt data, create an opening for injection or cause loss of access. Most involve network-card problems, IP address changes or anything on a live node that could disconnect it from Nightshift (Amine). In the first version, dangerous repairs are manual: Nightshift never executes them (FR-52; Danny, Exchange 5).
- **Expected interruption**: what the customer's service should experience while a repair runs, stated for every repair. Examples: "No service interruption expected." (clearing disposable temporary files); "The application may be unavailable for approximately 30–60 seconds." (restarting the only application replica); "Connectivity may be interrupted. Duration unknown." (changing network settings) (Amine, UX work, 2026-10-31).
- **Harmful repair**: a repair after which the service or cluster is worse than before it ran (a new or worse problem, less availability, or a risk to data), as shown by the health checks before and after. A repair that simply did not help is counted separately as one that did not work (SM-2, SM-3) (after-review fix, 2026-10-31, approved by Amine).
- **Disk cleanup**: deleting only explicitly allowlisted, disposable files: expired Nightshift temporary files, regenerable caches, and unused container images where the runtime confirms removal is safe. Each cleanup has defined ownership, retention rules, exclusions and deletion limits (Amine).
- **Prohibited action**: not a risk level but a rule: an action Nightshift may never take, with or without approval. It includes modifying or deleting customer records, databases or backups (Nightshift keeps its permitted diagnostic access), and improvised repairs that are not in the repair catalogue (product brief Ground Rules). The difference from a dangerous repair: a dangerous repair risks damage as a side effect and can be approved and then performed by a person (FR-52); a prohibited action deliberately modifies or deletes customer records and can never be approved (review fix, 2026-10-30, approved by Amine).
- **Customer production**: anything whose change can affect the customer's live experience or service, data, availability or security, at any layer. It is not limited to customer data fields such as emails and IDs; customer data may sit in different layers. A change that can affect customer production needs the customer's advance permission (a tick in the settings checklist) or the customer's approval per action (Amine). A change to OMK or Quornex that can affect customer production needs the same permission (Amine, after Danny, Exchange 5).
- **Platform repair**: a repair to OMK or Quornex components, which Orvex operates (Danny, Exchange 5). Who must approve it depends on its risk level and on whether it can affect customer production (FR-21).

**Authorisation and settings.**

- **Customer contract**: the agreement between Orvex and the customer: price, period, privacy, hardware responsibility, the clusters and services Orvex offers, and similar terms. It is not the checklist of allowed repairs (Amine).
- **Alert-only mode**: a mode the customer can choose in which Nightshift informs and recommends, but never executes repairs or asks for approval to execute them (Danny, Exchange 1; Amine). It stops every change Nightshift executes, including routine platform repairs under the agreed management policy and tuning (FR-41); monitoring, predictions and recommendations continue. There is no hidden exception. Kubernetes' own controllers and separately authorised maintenance (FR-47) are not Nightshift changes and are outside this mode. Alert-only is an ongoing option for any customer, not only for trials; trying the product before enabling repairs is one use of it (Amine, 2026-11-02).
- **Approval-enabled mode**: the other mode: the customer's checklist of ticked repairs applies, and Nightshift can ask for approval per repair. An empty checklist in this mode still allows individual approval requests (Amine). A new customer starts in approval-enabled mode with safe repairs ticked by default; the customer can untick any of them (Amine, 2026-10-31).
- **Advance permission**: the customer ticks, in a settings checklist, the repairs Nightshift may run. They do this once, from the repair catalogue, so Nightshift does not disturb them every time (Amine). The checklist is in the settings for all customers (Amine; Danny, Exchange 1). What a tick covers: FR-21.
- **Approval**: a yes given by an authenticated person at the time, for one repair, in the Quornex portal. In the first version Slack, phone calls and text messages only notify (FR-14). The approval is confirmed in the portal with the person's passkey and a one-time code the cluster sends by text message; the code is entered in the portal, never answered by text (FR-14; architecture AP-2, Amine, 2026-11-15). Text-message delivery of the code needs its own opt-in permission, naming the provider and the fields; if the customer declines it, approvals need the separately enabled passkey-only fallback, or are unavailable (PRIV-9; Amine, 2026-11-15). It is single-use, tied to the exact repair, target, catalogue version and evidence shown (review fix, 2026-10-30, approved by Amine). The one exception to "one repair, one target" is the group approval of FR-32 (Amine, 2026-11-03, review of the update). An approval expires if it is not used in time (FR-22). The customer approves, or Orvex support if the customer delegates to them (Danny, Exchange 1); for a platform repair that cannot affect customer production, only Orvex technical approval is needed (FR-21).
- **Orvex technical approval**: a technical check by an authorised engineer of the Orvex Nightshift team. On a risky repair to customer production it comes in addition to the customer's tick or approval, so the customer cannot damage their own app (Amine; product brief). On a risky platform repair, it is the approval Danny requires from "an authorised Orvex engineer" (Exchange 5). The Orvex Nightshift team also gives it before manual dangerous repairs (FR-52). Orvex reviews each repair catalogue entry in advance; safe repairs the customer has ticked then run automatically within the entry's conditions (Amine, 2026-10-30). See 5.5 for which approval each repair needs.
- **Agreed management policy**: the versioned list of routine, tested platform repairs that Nightshift may run without a customer tick. Orvex authorises its content; the customer agrees to its scope as part of the managed-service contract. Changes within that scope (the same repairs, with actions, targets and conditions that are no less restrictive) arrive with Orvex's current approved release; any other change expands permissions, and its new actions stay disabled until the customer explicitly accepts them. A change that can affect customer production leaves the routine policy and follows FR-21. See FR-51.
- **Maintenance policy**: the customer-authorised policy that lets Orvex's routine updates run within permitted update types and maintenance windows; a separate rollback policy covers emergency rollbacks, except the bounded probation rollback included in the authorisation of a routine Nightshift update (FR-47; architecture AP-7, Amine, 2026-11-15). See FR-47. Not to be confused with the agreed management policy above: that one covers routine platform repairs, and Orvex authorises its content.
- **Last-resort condition**: not a kind of repair but a condition. The customer and Orvex may permit a repair in advance, for use only when nobody answers and failure is predicted within about 30 minutes (Amine's proposal, to validate). See FR-24.
- **External AI**: an AI model that runs outside the customer's cluster: a hosted model, or a GPU shared across clusters. "No external AI" means nothing goes to an external AI provider (PRIV-8).
- **No outbound data**: nothing leaves the cluster by any channel. It is broader than "no external AI" (PRIV-9). A strict no-outbound deployment is not offered in the first version (FR-6, 3.2; Amine, 2026-11-03, review of the update).
- **Fleet service channel**: the one required outbound channel of the managed service (PRIV-9). It carries exactly: the Fleet heartbeat with its audit checkpoint (FR-6); requests for the relay's signed status confirmations and signed key lists; downloads of signed releases, catalogue and model weights; requests for signed policy and roster updates; and the fixed "attention needed" notice a cluster sends after its permissions expire (FR-22). PRIV-9 lists the exact permitted fields of each flow, which onboarding discloses. It carries minimal service metadata; no raw logs, secrets or application content. It replaces the earlier rule that the Fleet heartbeat alone was required (architecture AP-8, Amine, 2026-11-15; policy and roster updates and the attention notice: Amine, 2026-11-15, remaining points).

## 5. Features

### 5.1 Observe

**Description.** Nightshift watches the whole stack of every cluster. It notices when a node or a part of its own monitoring goes silent, and it says openly what it cannot see.

#### FR-1: Whole-stack detection
Nightshift detects disk, network-card and power-supply faults, Layer 2/3 networking problems, misconfigurations and Kubernetes problems on OMK; on hosted Kubernetes, it detects what the provider's available signals allow; and, if the customer opts in, problems in the customer's own app (Danny, Exchange 4; product brief). The tested scope is the failure catalogue deliverable (Section 11) and the FR-8 table; anything else is handled as a new problem (FR-19; review fix, 2026-10-30, approved by Amine).

#### FR-2: Node heartbeat
Every node sends a regular node heartbeat to the Nightshift monitoring service or the Kubernetes control plane (Amine).
**Consequences (testable):**
- A missing node heartbeat is noticed first by Kubernetes and the Nightshift monitoring service.
- [OPEN] How long a node heartbeat may be missing before it counts as missing.

#### FR-3: Silent-node diagnosis
When a node's heartbeat is missing, Nightshift verifies with neighbour nodes, then checks the infrastructure (on bare metal, through the server's out-of-band management interface, see FR-7) to determine whether the cause is a failed network card, power loss, a node crash or a network outage (Amine). If it cannot tell, it reports uncertainty (see 5.4).
- **Stateful workloads on a silent node:** Nightshift moves or force-deletes stateful workloads off an unreachable node only when a verified fencing and storage-safety procedure for that workload and platform confirms that the node can no longer write to the data; otherwise it escalates for a manual decision. A powered-off reading is evidence only. A reading from the out-of-band management interface is used only when its reported system ID matches the node's recorded one (architecture AP-10, Amine, 2026-11-15).

#### FR-4: Monitoring of Nightshift itself
Nightshift detects when one of its agents stops collecting metrics and information (Amine).
**Consequences (testable):**
- First checks: the agent's heartbeat, and the freshness of its data.
- A checker independent of the main metrics system detects a missing heartbeat or stale data, then runs independent health checks, such as Kubernetes API connectivity and node reachability.
- When these checks fail, Nightshift opens a **monitoring failure case**.

#### FR-5: Limited visibility
When some resources are invisible to Nightshift (for example, the provider-managed parts of hosted Kubernetes), Nightshift reports openly what it cannot see. It collects what it can from APIs, metrics and logs, looks for symptoms such as the Kubernetes API becoming unreachable or pods not responding, and reports with the evidence it collected (Amine). While the Kubernetes API is unreachable, no automatic repair that needs it runs: the problem shows as "Kubernetes API unreachable: repairs paused" and is escalated to a person. In the first version, Kubernetes control-plane failures are reported and escalated, not repaired automatically; this reduced coverage is documented (architecture AP-5, Amine, 2026-11-15).

#### FR-6: Three levels of monitoring
Each level is watched from outside itself (Amine, reformulated with Codex):

| Component | Monitors |
|---|---|
| Nightshift agent on each workload cluster | Local nodes, workloads and Kubernetes health |
| Nightshift management agent on the customer control cluster | The workload-cluster agents; coordinates investigations. The control cluster also runs its own Nightshift agent for its own health (Amine, 2026-10-31) |
| Quornex Fleet (managed by Orvex, outside the customer's clusters) | Whether every Nightshift agent, including the management agent, is still alive and reporting, acting as an external watchdog |

- Every Nightshift agent, in every workload cluster and on the customer control cluster, sends its own small "I'm alive" signal (the Fleet heartbeat) directly to Quornex Fleet. If the customer control cluster goes down, Fleet still sees which workload clusters are alive (Amine).
- The Fleet heartbeat contains only the agent ID, a timestamp, a status (alive or degraded) (AI draft, accepted by Amine, 2026-11-02) and a minimal audit checkpoint: sequence number (`audit_seq`), chain head (`chain_head`), checkpoint time (`checkpoint_time`), key ID (`audit_key_id`) and signature (`checkpoint_sig`), with a fixed schema and no text. The checkpoint lets Fleet detect that the cluster's audit record (FR-35) was rewritten or destroyed. Limits: destruction is detectable, not recoverable; the checkpoint proves neither that the record is complete nor that it is true; and if the audit service is compromised, the checkpoint fields (about 32 bytes per heartbeat) could be used as a covert channel (architecture AP-1, Amine, 2026-11-15). For correlating problems across clusters (FR-32), Fleet receives only the allowed fields defined in PRIV-3 (review fix, 2026-10-30, approved by Amine).
- The Fleet heartbeat is part of the Fleet service channel, the required channel of the managed service (PRIV-9). Before the customer accepts the service, onboarding explains its purpose and its exact fields, including the audit checkpoint fields (Amine, 2026-11-02; required channel: Amine, 2026-11-03, UX work; Fleet service channel and checkpoint fields: architecture AP-1 and AP-8, Amine, 2026-11-15). It is authenticated and never silently exempt from the outbound check: the independent checker sends it on its own path outside the gateway, to a fixed destination with a rate limit, and a strict fixed-schema validator is that path's purpose-specific outbound check (PRIV-4, SEC-8; architecture AP-8, Amine, 2026-11-15). A shared node or network failure can stop both the heartbeat and the gateway.
- **Strict no-outbound:** a strict no-outbound deployment, where nothing may leave the cluster, is not offered in the first version (3.2): without the Fleet heartbeat, Fleet could not watch the cluster from outside (Amine, 2026-11-03, review of the update).
- **Fleet's views** show "No data since 02:10" when the Fleet heartbeat stops, and "Heartbeat OK · Fleet reports not permitted: not included in fleet-wide correlation" when Fleet reports are not permitted (Amine, 2026-11-03, UX work).

#### FR-7: Out-of-band management required on bare metal
Full bare-metal management requires out-of-band management (BMC/Redfish or equivalent) on each supported server. Before Nightshift takes over, installation validates access to each server's hardware management interface, including credentials, power status and hardware health reporting (Amine, with Codex).

Behaviour by situation (pasted by Amine, 2026-10-29):

| Situation | Nightshift behaviour |
|---|---|
| Out-of-band management available and validated | Full supported hardware monitoring |
| Out-of-band management missing or inaccessible | Limited-visibility mode |
| Node goes silent without out-of-band management | Report the node unreachable; root cause unknown |
| Repair requires hardware access that is unavailable | Recommend manual customer intervention |

**Consequences (testable):** installation and validation happen before Nightshift is deployed (Danny, Exchange 4). Orvex's installation process
1. checks for out-of-band management;
2. tests connectivity and the available hardware telemetry;
3. if out-of-band management is unavailable, displays a warning explaining the limitations;
4. requires the customer to acknowledge the reduced coverage.

Nightshift then receives the result and records the limitation in its monitoring coverage report (Amine).

### 5.2 Predict

**Description.** Nightshift sees slowly developing problems coming, using rules and statistics first and AI only where they cannot do the job (product brief). It alerts only when a prediction is worth acting on, and it keeps each warning up to date.

#### FR-8: Predictable problems
Nightshift forecasts these slowly developing problems (table from another Claude conversation, pasted by Amine):

| Area | Predictable problems | What Nightshift observes |
|---|---|---|
| Storage | Disk filling, inode exhaustion, SSD wear, growing disk latency | Free space, SMART, I/O metrics |
| Memory | Memory leaks, increasing consumption, memory exhaustion | Sustained memory growth, available RAM |
| CPU | Gradual CPU saturation and throttling | Utilisation, load, throttling |
| Hardware | Overheating, fan deterioration, some disk and RAM faults | Temperature, fan speeds, ECC errors, SMART and out-of-band alerts |
| Power | Some degrading power supplies | Power-supply warnings, where out-of-band management supports them |
| Network | Congestion, increasing packet errors, connection exhaustion | Bandwidth, packet loss, retransmissions, connection counts |
| Kubernetes | Node resource pressure, cluster capacity exhaustion, persistent pod instability | Resource trends, restarts, eviction signals |
| Applications | Database saturation, growing latency, connection-pool exhaustion | Response times, database metrics |
| Configuration | Certificate expiration, capacity limits, gradually harmful configuration changes | Expiration dates, quotas, configuration history |

- Hardware and power rows depend on out-of-band management; in limited-visibility mode their coverage is reduced (FR-7). If the customer chooses to take full care of their own infrastructure, that is their right and their responsibility (Amine).
- The customer's own app is covered only if the customer opts in (product brief); Quornex's own services, such as its databases, are always covered.
- Sudden faults with no warning (for example a power supply dying at once) are detected (5.1), not predicted.

#### FR-9: When a prediction becomes an alert
Nightshift weighs four factors; actionability is required for every alert (from Codex, pasted by Amine):

| Factor | Question Nightshift asks |
|---|---|
| Time to impact | How soon might the problem affect the service? |
| Confidence | How reliable is the evidence and forecast? |
| Criticality | Is this a critical production service or a non-critical workload? |
| Actionability | Is there something useful to do before impact? |

- "Something useful to do" includes actions by Nightshift, the customer or Orvex. For example, SSD wear is actionable because the customer can order a replacement disk.
- A prediction with nothing useful to do goes to the dashboard and the morning summary, not to an alert.

#### FR-10: Keeping predictions honest
Example (from Codex, pasted by Amine): Nightshift predicts a disk will be full in six hours, but the application deletes temporary files and usage falls. Nightshift:
1. recalculates the forecast whenever meaningful new data arrives;
2. updates the existing warning if the predicted time or risk changes substantially;
3. automatically withdraws the warning once the risk has decreased enough and stays stable;
4. explains why the warning changed, for example that disk usage fell after temporary files were removed;
5. records the outcome so that Orvex can evaluate the prediction method and reduce future false alerts.

### 5.3 Explain and notify

**Description.** Nightshift says what is wrong, why it matters and what it did, "in a few sentences anyone can follow" (Danny, `brief.pdf`). It explains to the customer and to Orvex. It stays quiet unless something matters: most things go to the dashboard and the morning summary, alerts are kept for decisions, and phone calls for critical problems (product brief).

#### FR-11: Plain-language, evidence-based explanations
Every message Nightshift sends about a problem can be understood by a non-expert business owner (product brief; Amine's correction during the brief). It is based on evidence, and it says so when the cause is unknown (Vision).
**Consequences (testable):** the facts from the rule-based checks are shown separately from the AI's wording (SEC-1); without any AI, the explanation is written from templates (Section 7). Each message is a few sentences anyone can follow (Danny, `brief.pdf`), and states
- the current state, and the impact on the service;
- the time to impact, for a prediction;
- whether the cause is confirmed, and if not, what is known and what is not;
- what Nightshift did, or the fix it proposes, with its expected interruption;
- for a request, what happens if nobody answers.

Example from the brief: *"Your checkout service is using more memory than usual. Purchases still work, but at this rate memory runs out in about 4 hours and checkout may become unavailable. We haven't confirmed the cause yet. We suggest [fix]. Do you approve? If you don't answer, we'll keep watching and won't change anything."*

#### FR-12: Who is told
- Every problem in the customer's clusters is visible to the customer, who has a full view of them (product brief decision log). Visible does not mean notified: a problem triggers a notification only at the levels in FR-13 (Amine).
- Orvex support is told when the customer's contract says so, and answers approval requests when the customer delegates approval to them (product brief; Danny, Exchange 1).
- The Orvex Nightshift team watches over Nightshift itself (its limits, its proposals and the lessons shared across the fleet). They are not called or alerted for problems handled by safe repairs (product brief; Amine). They give Orvex technical approval for risky repairs (Amine; for risky platform changes, Danny, Exchange 5) and before manual dangerous repairs (FR-52).
- **Routing follows the approval table (5.5)** (Amine):
  - A repair that needs only the customer's approval goes only to the customer.
  - A repair that also needs Orvex technical approval goes to the Orvex Nightshift team as well.
  - A platform repair that needs only Orvex technical approval goes only to the Orvex Nightshift team; the customer sees it on the dashboard and in the morning summary (AI draft, accepted by Amine, 2026-11-02).
  - A dangerous repair (manual, FR-52) goes to the approvers it needs and to whoever performs it, with the evidence and the suggested steps (AI draft, accepted by Amine, 2026-11-02).
  - In every case, Orvex receives a signal whenever the customer confirms something. The signal travels on the optional Fleet reports channel (PRIV-9); with Fleet reports off, it is recorded locally and Orvex is not told (architecture AP-8, Amine, 2026-11-15).
  - This replaces Amine's first routing proposal in the product brief addendum.

#### FR-13: Notification levels
| Level | When |
|---|---|
| Phone call | Only for critical problems: an important service such as checkout or a database is failing, or there is strong evidence it is about to fail |
| Alert | A problem becomes a real risk and needs a decision (see FR-9) |
| Dashboard and morning summary | Everything else |

(product brief; product brief addendum)
- A phone call is paired with a text message carrying the portal link; the customer can choose a text message instead of a call (Amine, 2026-11-03, UX work).
- The one-time code that confirms an approval is also sent by text message, under its own permission: it is part of the approval flow, not an alert (FR-14, PRIV-9; architecture AP-2, Amine, 2026-11-15).

#### FR-14: Approval requests
Nightshift asks for approval in the Quornex portal.
- **Channels:** in the first version, Slack, phone calls and text messages only notify: a Slack message links to the authenticated portal, where the approval is given by an authenticated person (Amine, UX work, 2026-10-31; text messages: Amine, 2026-11-03, UX work; narrows Danny's Exchange 1, which allowed approval in Slack; review fix, 2026-10-30, approved by Amine). Notifications follow the outbound rules (PRIV-2 to PRIV-4, PRIV-9).
- Every problem that needs a person first appears on a Nightshift monitoring page (product brief addendum). Requests waiting for approval and running repairs have separate, bounded capacities in each cluster, with capacity reserved for urgent requests. When the capacity for waiting requests is full, the problem is still recorded (within bounded storage), its status shows "approval request blocked: capacity full" and Orvex is alerted; stops stay possible (architecture AP-14, Amine, 2026-11-15).
- **The request** explains the problem as in FR-11 and states the repair, its target, risk level and expected interruption and the approvals still required. It also says what happens without an answer: Nightshift keeps watching, and changes nothing that is not already authorised (product brief; FR-23). It also states the recovery plan: whether the repair can be undone (a rollback is shown only when the rollback is certain) and what happens if it fails (FR-27, FR-28; Amine, 2026-11-03, UX work).
- The request can be read and answered on a phone (Amine, 2026-11-03, UX work).
- The person can approve or reject (FR-50).
- **Confirming an approval** (architecture AP-2, Amine, 2026-11-15; pending feasibility and usability testing): after the person presses Approve and confirms, the cluster sends a text message to the approver's phone number in the signed roster, naming the action, with a one-time code. The person enters the code in the portal (paste and auto-fill are allowed), then confirms with a fresh passkey check over the decision. The cluster accepts the approval only if the code and the passkey both match the same decision, and records the assurance level "passkey + SMS". This applies to customer, delegated and Orvex approvals and to the performer's "Start now" (FR-52). The code is bound to that decision, recipient, request version and expiry, with attempt and resend limits; its lifetime (5 minutes, a starting value) never extends the approval's validity. The cluster builds the text from the decision and the catalogue template, never from AI or log text.
  - **Approval text-message permission** (Amine, 2026-11-15): the approval text message is a separately disclosed part of the approval flow, distinct from alerts. It needs its own explicit permission, which names the SMS provider and the permitted fields (PRIV-3, PRIV-9). Turning notifications off never silently grants it. If the customer declines it, approvals need the separately enabled passkey-only fallback, or are unavailable; the customer is told this when deciding. It is opt-in at onboarding, never pre-ticked, and it also covers the notice sent after each decision (below) (Amine, 2026-11-15, remaining points).
  - **Passkey-only fallback:** only where a signed policy explicitly enables it (a customer administrator for customer approvals, Orvex for Orvex approvals; SEC-7). The person sees "SMS confirmation unavailable: approving with passkey only (reduced assurance)", and the decision, receipt and history record "passkey only". Without an enabled fallback, a failed text message never lowers the requirement: the person sees "Confirmation code could not be sent", the request stays open and escalation continues.
  - **After every decision** confirmed through this flow, the cluster sends the person a short notice ("You approved … Not you? Withdraw") with allowlisted fields only. It falls under the approval text-message permission, not under notifications (Amine, 2026-11-15, remaining points).
  - **Limits:** the passkey signs a fingerprint of the decision, not readable text, and with paste or auto-fill, entering the code does not prove the person read the task. A compromised portal can still obtain approval for a different request that is genuinely pending and valid if the text message is not read. The gateway carries the text message and sees the code, so a compromised gateway can alter or drop the message and the notice; against it the text message gives no independent proof of possession, and the passkey signature over the decision remains the protection. The notice after a decision may reveal some misuse but does not reliably detect gateway tampering. Provider recipient restrictions, templates, rate limits and spending controls are relied on only where verified; alerts and delayed billing checks are not hard caps.
  - **Timing targets to test, not promises:** under 60 seconds from Approve to receiving the code, and under 60 seconds from entering it to the cluster's receipt. The person sees distinct states: sent ("Sent — not yet effective in the cluster"), received by the cluster (not yet effective), applied by the cluster (receipt), expired, unreachable; nothing is shown as effective before the cluster confirms it (FR-22).
  - **Stops** (rejection, withdrawal, untick) need a fresh passkey check over the decision but no text-message code; the notice sent after a stop confirms them (FR-22, Confirming a stop) (Amine, 2026-11-15, remaining points).

#### FR-15: Dashboards
- Each cluster has its own dashboard, reached through the Quornex portal (Amine).
- A customer sees all their clusters and can combine them in one dashboard (Amine); the combined view uses only sanitised information from each cluster (PRIV-5).
- The customer can watch their app's health live (product brief).
- Orvex has grouped dashboards per 100 clusters, because a single view of 10,000 clusters is unreadable (Amine).
- If the customer permits neither notifications nor the portal, their problems are visible only on an in-cluster dashboard (PRIV-9; Amine, 2026-11-03, review of the update). The in-cluster dashboard is reached at a stable internal address and uses separate local passkeys; what can be done there is in PRIV-9 (architecture AP-13, Amine, 2026-11-15).
- Every dashboard, including the customer's, shows how current its data is and never shows stale data as healthy (threshold: Section 10, item 8; Amine, 2026-11-03, UX work).

#### FR-16: Morning summary
Every morning, the customer gets a summary of the night: the problems, the fixes, anything unusual, and Nightshift's and the app's activity. For problems that need a risky repair, it includes the full timeline from the first thing noticed. It also shows recurring patterns, such as a 3 AM traffic peak that needs more resources, and authorised repairs that succeeded (product brief; product brief addendum).

### 5.4 Choose a repair

**Description.** Nightshift only ever chooses a repair from the repair catalogue. When a problem has no tested repair, it explains, reports and escalates instead of improvising.

#### FR-17: Repairs only from the repair catalogue
Nightshift runs only repairs from the repair catalogue, tested before each release (product brief Ground Rules).
**Consequences (testable):**
- The AI never invents a repair, and in particular never generates shell scripts or commands to run (product brief Ground Rules).
- Rules and automation first; AI only where they cannot do the job, for example to help match evidence to a catalogue entry or to write the explanation (product brief; Danny, Exchange 3).
- A prohibited action is never in the repair catalogue (product brief Ground Rules).

#### FR-18: Matching a problem to a repair
Nightshift chooses a repair only when the evidence or symptoms are enough to match a repair catalogue entry, as defined by that entry. Matching an entry is not a guess; acting outside it would be (Amine; AI wording, accepted by Amine: "they are two different cases").
- Ranking: see FR-26.

#### FR-19: Problems without a tested repair
For a problem in the incident catalogue (fix not yet tested or confirmed), or in neither catalogue, Nightshift does not repair. It explains with the evidence it has, states its uncertainty, and escalates (Amine; product brief).

#### FR-20: Hardware and provider-side faults: mitigate, report uncertainty, escalate
(AI proposal, accepted by Amine, 2026-10-28, with the changes noted. Amine's requirement: detecting a hardware fault does not imply physical repair capability; define when Nightshift mitigates, reports uncertainty or escalates.)

Nightshift detects faults in customer hardware but cannot physically repair them. For each hardware fault it does one or more of the following:
- **Mitigate** when the evidence or symptoms are enough to match a repair catalogue entry, that entry includes a repair that works around the fault without touching the hardware (for example, moving workloads off a node whose disk is failing), and the repair is authorised for its risk level. The exact cause is not always needed (Amine). This makes mitigation only as good as the repair catalogue, which must be strong (Amine). A mitigation keeps the service running but does not close the fault: it stays open until the customer confirms the hardware is fixed and Nightshift has checked that the problem is gone (Amine).
- **Report uncertainty** (accepted by Amine) when the evidence does not identify the cause. Example: a node goes silent, and from outside a dead network card, a failed power supply, a cable, a switch or a network partition look the same. Nightshift states what it observed, the possible causes, what it cannot tell, and what would tell them apart. It does not act on a guess; it may run only a mitigation that is valid whatever the cause.
- **Escalate to the customer** (accepted by Amine) whenever physical work, or a change to hardware or hardware configuration the customer is responsible for (cabling, switches, firmware), is needed, or when no authorised mitigation exists. The message says in plain words what failed, the impact, what to ask the hardware provider, and the evidence. After the customer reports the repair, Nightshift double-checks that the problem is gone before closing the fault (Amine).
- **Escalate to the hardware provider**: only through the customer (Amine). Nightshift never contacts the customer's hardware provider itself; it prepares the evidence for the customer to send.
- **On hosted Kubernetes (EKS)**: the provider is responsible for Kubernetes and the infrastructure, so Nightshift reports provider-side problems through the customer, as for hardware providers: it never contacts the provider directly, but prepares the evidence for the customer to send (Amine, 2026-10-31).

### 5.5 Authorise

**Description.** What Nightshift may do depends on three separate things: what the repair changes (only Orvex's platform, or customer production), its risk level (Glossary), and who has said yes. Nightshift never decides on a change on its own.

#### FR-21: Approval by what a repair changes and its risk level
Orvex operates OMK and Quornex, so not every repair needs both the customer's approval and Orvex technical approval (Danny, Exchange 5). Approval depends on what the repair changes as well as on its risk level (Amine, after Danny, Exchange 5):

| What the repair changes | Safe | Risky | Dangerous |
|---|---|---|---|
| Only OMK or Quornex (platform repair), without affecting customer production | Runs automatically under the agreed management policy (FR-51), with no customer tick. A safe platform repair not in the policy needs Orvex technical approval at the time (AI draft, accepted by Amine, 2026-11-02) | Orvex technical approval at the time | Manual (FR-52) |
| Customer production, including a platform repair that can affect it | Ticked: runs automatically, with no Orvex technical approval. Not ticked: the customer's approval at the time | Ticked: Orvex technical approval each time it is about to run, after Nightshift confirms the customer ticked it. Not ticked: the customer's approval and Orvex technical approval, at the time | Manual (FR-52) |

- FR-21 applies in approval-enabled mode. In alert-only mode Nightshift executes nothing, including policy repairs; it only informs and recommends (Amine; Danny, Exchange 1; Amine, 2026-11-02). Switching to alert-only cancels pending execution authorisations: approvals given but not yet used are cancelled and recorded; ticks and the agreed management policy stay recorded, but the repairs they cover do not run (Amine, 2026-11-03).
- **Who decides whether a repair can affect customer production:** each repair catalogue entry states it. Orvex sets it when testing the entry, with the two reviewers of FR-39, and the customer can read it in the portal. The executor re-checks it before every run; if the pre-run checks show that a platform repair can affect customer production, or if the classification is in doubt, the customer-production row applies. The customer can dispute an entry's classification; until Orvex has reviewed it again, a disputed entry follows the customer-production row for that customer (Amine, 2026-11-02, after the review of the update).
- The customer ticks once, from the repair catalogue, so they are not disturbed every time (Amine). A tick counts as the customer's approval only for the specific tested action and conditions it covers (Amine's interpretation of Danny, Exchange 5; not confirmed by Danny).
- Where the table says "the customer's approval", Orvex support may give it instead if the customer has delegated approval to them (Danny, Exchange 1). The customer sets the delegation's scope, can revoke it at any time, and is notified of every approval given on their behalf (review fix, 2026-10-31, approved by Amine). Where both the customer's approval and Orvex technical approval are required, they come from different people, even when Orvex support approves on the customer's behalf (Amine, 2026-11-03, review of the update).
- Risky repairs to the customer's own app (not OMK or Quornex) need Orvex technical approval as well as the customer's. This is our conservative interpretation of Danny's approval model: Exchange 5 speaks about platform changes, and we keep the product brief's rule so the customer cannot damage their own app. It is a decided policy, not an open question (Amine, 2026-11-02; reworded 2026-11-03).
- A prohibited action can never be ticked or approved (product brief).
- A successful history can support a reviewed reclassification of a repair, but never lowers its risk level or removes approvals automatically (Amine, 2026-10-30).

**Reading is not changing.** The customer chooses what Nightshift may read: the infrastructure only, or also their app and its code. Permission to read never means permission to change (product brief).

#### FR-22: How long a yes is valid
- A ticked repair stays permitted until the customer unticks it (Amine). The tick is tied to the repair's version: if a release changes the repair's action, conditions or risk level, the customer must tick it again (review fix, 2026-10-30, approved by Amine).
- **Offline validity** (architecture AP-4, Amine, 2026-11-15). Every signed permission has its own end of validity and is never used beyond it. Long-lived permissions (ticks, the agreed management policy, rosters, delegations, channel permissions) also need a fresh signed status confirmation from Quornex Fleet. Permissions are classified by the authority they require, not by who signed them. By the age of the last confirmation (starting values to test):
  - **Fresh** (under 1 hour): every authorised repair can run.
  - **Stale** (from 1 hour to under 24 hours): repairs whose required authorities are all customer-held continue within their own validity (safe ticked repairs). Permissions that need current Orvex authority pause: policy repairs (FR-51), the Orvex side of the last-resort condition (FR-24) and repairs that need Orvex technical approval. There is no exception for an Orvex technical approval already received in the cluster and still within its own validity: actions that need fresh Orvex authority pause in this tier (Amine, 2026-11-15, remaining points). This moves the cutoff for safe policy repairs from 24 hours to 1 hour.
  - **Expired** (24 hours or more): repairs whose required authorities are all customer-held and still within their own validity continue (safe ticked repairs). Customer delegations stay valid only within their own validity and only for decisions already received in the cluster; new delegated approvals cannot arrive while the cluster is cut off. Repairs that need any Orvex authority stop: the agreed management policy, Orvex technical approval, Orvex's side of the last-resort condition and Orvex's signed list of platform-only repairs. Nightshift keeps observing and reporting.
  - Stops keep working in every tier, against the cached roster. Stated limits: unticks in the portal and fleet-wide catalogue switch-offs (SEC-6) issued while the cluster is cut off reach it only when it reconnects; a Fleet outage of more than 1 hour pauses every repair that needs current Orvex authority (including policy repairs) on every affected cluster, and one of 24 hours or more stops every repair that needs Orvex authority.
  - Restarting never extends validity. If the cluster cannot establish how long it has been cut off, it treats its permissions as expired until a fresh confirmation arrives; a repeated or older confirmation never renews freshness. A cluster whose clock is not synchronised refuses time-limited approvals. After a detected restore or reinstall, permissions count as expired and repairs stay blocked until stops, revocations and switch-offs have been reconciled with Fleet; approvals from before the restore are not revived. A restore made while the cluster is cut off is detected only when it reconnects. Someone holding cluster-admin can still manipulate time and stored state (SEC-10).
  - Losing contact with Fleet is distinct from the customer turning off portal access (PRIV-9): the confirmations travel on the Fleet service channel.
- An approval given on request is valid for that one time only. If the problem happens again, or another problem appears, a new approval is needed (Amine).
- An approval that is not used in time expires, and Nightshift asks again (Amine, UX work, 2026-10-31; replaces the earlier "there are no timers to manage", an AI suggestion Amine had accepted). Each repair catalogue entry states how long an approval given at the time stays valid; Orvex sets the value when testing the entry. An unanswered request does not expire: it stays open, shows current evidence, is re-issued if the evidence or conditions materially change, and is closed as "resolved, no longer needed" only after Nightshift's verification shows the problem is gone; the closure is recorded and notified (Amine, 2026-11-03, UX work; verification before closing: architecture AP-14, Amine, 2026-11-15).
- Right before every run, Nightshift re-checks the repair's safety preconditions from the repair catalogue. If they still hold, it runs. If the repair or its conditions have materially changed, it does not run and Nightshift asks again (AI suggestion, accepted by Amine; UX work, 2026-10-31).
- If a pre-run check fails, the repair does not run, and a fresh approval cannot override it (Amine, 2026-11-03; AI_LOG correction #30). If a check is inconclusive because Nightshift cannot see (for example, a node is unreachable), a manual repair (FR-52) may go ahead only under a defined manual procedure that establishes each required condition with alternative evidence, such as out-of-band access (FR-7) or an onsite inspection. Missing telemetry alone never waives a check. If no safe procedure can be established, the repair stays blocked and Nightshift escalates. An automatic repair with an inconclusive check does not run (Amine, 2026-11-03, review of the update).
- Right before every run, the executor (SEC-8) also re-checks the authorisation: the tick or approval is still valid, including its offline validity (above), has not been revoked or unticked, and the customer's mode still allows the repair. If not, the repair does not run (after-review fix, 2026-10-31, approved by Amine).
- The person who gave an approval can withdraw it until the repair starts. A withdrawal, a switch to alert-only (FR-21) or an untick takes effect when the executor in the cluster receives and applies it (SEC-8, SEC-9). The validity set in the catalogue entry caps how long any approval can live. The record keeps every step (Amine, 2026-11-03, UX work; revocation reaching the cluster: Amine, 2026-11-03, review of the update).
- **Receipts** (architecture AP-3 and AP-20, Amine, 2026-11-15): after applying or refusing any decision, approvals included, the cluster signs a receipt with its own key. Until the receipt arrives, the person sees "Sent — not yet effective in the cluster". Received and applied are kept distinct: a decision the cluster has received has not necessarily taken effect, and the record shows when the decision was sent and when the cluster applied it. The portal's status is a convenience, not proof: a compromised portal and relay could show a false one, and a failed or lying relay can delay or hide a stop; the missing receipt is the visible sign. Receipts reach the portal or appear on the in-cluster dashboard.
- **Confirming a stop:** only after the cluster has applied and recorded a withdrawal, rejection, untick or switch to alert-only does it tell the person who made it, through notifications if permitted, never through the portal or relay. Without that notice the stop counts as unconfirmed, not as failed; a compromised gateway can still block or alter the notice (architecture AP-3, Amine, 2026-11-15). A stop needs a fresh passkey check but no text-message code (FR-14) (Amine, 2026-11-15, remaining points).
- **Stops win:** in the cluster, any valid stop (withdrawal, rejection, untick, switch to alert-only, revocation) beats any approval for the same request version, whatever the order in which they were signed or arrived. The server's order of decisions, including among several customer administrators, is for display and history (architecture AP-3, Amine, 2026-11-15).

#### FR-23: When nobody answers
If nobody answers, on the customer's side or Orvex's, Nightshift does nothing on its own: silence grants no new permission. A repair that is already authorised (ticked in advance, in the agreed management policy, or permitted under the last-resort condition) may still run when nobody answers, if its conditions pass (Amine; FR-51). The AI never acts alone on what is not permitted (Amine; product brief).
- One Nightshift engineer is on duty each night. If they do not answer in time, the repair waits; Nightshift keeps watching, alerts again, and calls if the problem becomes critical (AI suggestion, accepted by Amine).
- [Possible feature, Amine] When a dangerous case needs a manual repair (FR-52), Nightshift calls a member of the Orvex Nightshift team.

#### FR-24: Last-resort condition
The customer must tick the last-resort condition; Orvex never applies it on its own (Amine). It covers only repairs the customer is allowed to tick (safe and risky), never dangerous or prohibited ones (Amine). It applies only when nobody answers and failure is predicted within about 30 minutes (Amine's proposal, to validate). It is a permission given in advance by the customer and Orvex for a specific repair under a specific condition; it never grants anything beyond that (product brief; review fix, 2026-10-30, approved by Amine).
- In practice the last-resort condition is for risky repairs, because safe repairs do not need it (Amine). For a risky repair under the last-resort condition, Orvex's permission given in advance replaces Orvex technical approval at that moment (Amine).
- "Nobody answers" means that no decision has been made on the open request by the time failure is predicted within about 30 minutes. The threshold is an assumption to validate (Section 10, item 14). The condition grants no extra permission and never overrides a rejection (FR-50; Amine, 2026-11-03, review of the update).
- The Orvex side of a last-resort permission needs current Orvex authority: it pauses after 1 hour without a fresh confirmation from Quornex Fleet, and stops at 24 hours (FR-22) (architecture AP-4, Amine, 2026-11-15).

#### FR-50: Rejecting a request
When a person rejects an approval request, Nightshift (Amine, UX work, 2026-10-31, extending the AI's draft):
- blocks that proposed repair and records the decision (5.8);
- notifies the other approvers concerned;
- keeps monitoring the problem.

Nightshift does not resubmit the same request automatically, and does not substitute another repair to get around the rejection. Rejecting one request does not turn off other automatic repairs.
- **Scope:** the rejection blocks that repair for this occurrence of the problem only. The last-resort condition (FR-24) cannot override it (Amine, 2026-11-02, after the review of the update).
- If the problem becomes critical or materially changes, Nightshift may send one new request, which shows the earlier rejection. A later recurrence of the problem is a new problem (Amine, 2026-11-02, after the review of the update).
- The person who rejected can undo the rejection within a short, fixed window: 2 minutes, a starting value to test, timed by the cluster from when it receives the rejection (architecture AP-16, Amine, 2026-11-15); the other approvers are notified when the window ends. Undoing only reopens the request; it approves nothing (Amine, 2026-11-03, UX work; window: Amine, 2026-11-03, review of the update).

#### FR-51: Agreed management policy
The agreed management policy is a versioned list of routine, tested repairs to OMK and Quornex components. Each entry comes from the repair catalogue with its exact action and conditions (AI draft, accepted by Amine, 2026-11-02; Danny, Exchange 5: "routine, tested repairs should happen automatically").
- **Limits:** the policy never contains a repair whose catalogue entry says it can affect customer production, and never a risky or dangerous repair. If the pre-run checks show that a policy repair can affect customer production, it goes to approval instead (FR-21). Policy repairs never run in alert-only mode. Policy repairs need current Orvex authority, so they pause while the cluster has had no fresh confirmation from Quornex Fleet for 1 hour or more (FR-22) (architecture AP-4, Amine, 2026-11-15).
- Installing a new version of OMK or Quornex is an update (FR-47), never a policy repair, and a policy repair never changes the executor, the gateway or the audit path (SEC-8, SEC-2; review fix, 2026-11-02, approved by Amine).
- **Who authorises it:** Orvex authorises the content. Each entry is approved after testing by two reviewers from the Nightshift team, as for any new or changed catalogue entry (FR-39); each policy version, including Orvex's signed list of platform-only repairs, is signed only after testing and two distinct authorised reviewers, enforced by the signing system (architecture AP-18, Amine, 2026-11-15); the policy reaches clusters through the staged release (FR-40, FR-46; Amine, 2026-11-02, after the review of the update). The customer agrees to the policy as part of the managed-service contract and can read it in the portal.
- **Changes:** each new version is signed (SEC-9), recorded and notified. Clusters follow Orvex's current approved release, which carries the policy, through the controlled rollout (FR-46). Customer acceptance governs permissions; it does not let a cluster stay indefinitely on an old software or policy version (Amine, 2026-11-03):
  - A change within the agreed scope keeps the same repairs, with actions, targets and conditions that are no less restrictive. Corrected steps are allowed, and still need testing and review like any catalogue change (FR-39, FR-40). Such a change applies without fresh acceptance (Amine, 2026-11-03, review of the update).
  - Any other change expands permissions and needs the customer's explicit acceptance. Until the customer accepts, those new actions stay disabled for that customer; the rest of the new version applies. The customer can dispute whether a change is within the agreed scope; until Orvex has reviewed it again, a disputed change is treated as expanding permissions (Amine, 2026-11-03, review of the update).
  - A change that can affect customer production leaves the routine policy and follows FR-21 (Amine, 2026-11-03, review of the update).
  - This replaces the rule of 2026-11-02 that a new version applied to a customer only after acceptance, with the last accepted version staying in force (Amine, 2026-11-03).

#### FR-52: Dangerous repairs are manual in the first version
When the matching repair is dangerous, Nightshift does not execute it. It explains the problem, gathers the evidence and suggests the steps; a person performs the repair (Amine, after Danny, Exchange 5: "I'd leave dangerous repairs manual initially"). Only who performs the repair changes: the approvals stay (Amine, 2026-11-02, after the review of the update; this tag also covers the untagged statements below).
- The request is marked "manual repair needed" (Amine, 2026-11-02).
- **The steps** Nightshift suggests come from the repair catalogue entry; they are never written by the AI (FR-17).
- **Before the person performs it:** on customer production, the customer approves personally (never through delegation), Orvex technical approval is given, and a recovery plan is reviewed by the Orvex engineer who gives technical approval. On a platform repair that cannot affect customer production, an authorised Orvex engineer approves and reviews the recovery plan. The approvals cover a stated time window; outside it, the approvers are asked again. Right before starting, the performer re-runs Nightshift's pre-run check of the evidence. If it fails, the work does not start; if it is inconclusive, the work goes ahead only under a defined manual procedure (FR-22; Amine, 2026-11-03, UX work).
- **Approvers and window:** customer approval and Orvex technical approval come from different people where both are required; the Orvex engineer who approves may also perform the work. The window limits when the work may start. Work still in progress when the window ends is finished or recovered under the reviewed recovery plan, never abandoned. A material change, including a recovery plan changed materially in review, needs renewed approval from the relevant approvers, including the customer where their production is affected (Amine, 2026-11-03, review of the update).
- **Who performs it:** an Orvex engineer for OMK and Quornex; the customer, or their hardware provider, for hardware and for the customer's own app. A hardware provider is not in any roster: a named customer representative from the customer roster confirms that the provider is ready before pressing "Start now", and reports completion afterwards ("I've done it"). The record names the representative and, where known, the actual provider and technician. Their confirmation does not replace the required approvals or safety checks (architecture AP-2, Amine, 2026-11-15).
- **"Start now" and "I've done it"** (architecture AP-2, Amine, 2026-11-15): "Start now" is accepted only from the named performer, with valid approvals, inside the approved window and after the pre-run check passes, and it is confirmed like an approval (FR-14). "I've done it" is a completion report, not an approval: it triggers Nightshift's verification and does not close the fault by itself; the case closes only if verification passes. It can still be sent after the window ends, and its text is treated as untrusted evidence (SEC-1). It is authenticated with a fresh passkey check over the report, with no text-message code, and only the named performer or, for a hardware provider, the agreed customer representative may send it (Amine, 2026-11-15, remaining points).
- When the person reports the repair done, Nightshift records who performed it, under which approvals, and checks that the problem is gone before closing it, as for hardware repairs (FR-20; AI draft, accepted by Amine, 2026-11-02). Manual dangerous repairs count in SM-3 and SM-4 like any other change.
- For a manual procedure (FR-22), the record holds who verified each required condition, the evidence, the approvals and the recovery plan. Work performed outside the procedure is recorded honestly. Authorisation and safety-check compliance are reported separately, so an inconclusive check alone does not make a change "unapproved" (SM-4; Amine, 2026-11-03, review of the update).

### 5.6 Act and verify

**Description.** Nightshift applies the chosen repair, checks that it worked, and undoes it if it did not work and can be undone (product brief; FR-25). It ranks repairs so the safest comes first, never lets two repairs fight, and stops and calls a person when a repair makes things worse.

#### FR-25: Apply and verify
Nightshift applies the repair, then checks that it worked using the verification defined in its repair catalogue entry. If the repair did not work and can be undone, Nightshift undoes it (product brief; repair catalogue definition).

#### FR-26: Ranking repairs
For each problem, the repairs in its repair catalogue entry are ranked by safety, estimated success rate and potential impact. Nightshift always tries the safest repair expected to work first (Amine; first suggested in the AI's session-2 feedback). Example: for memory creep, moving traffic to a healthy replica comes before restarting a replica.

#### FR-27: When a repair does not work
If a repair does not work (including one that cannot be undone, such as a restart), Nightshift moves to the next repair only if that repair is safe. If the next repair is risky, Nightshift asks for Orvex technical approval from the Nightshift team (Amine). If it is dangerous, the problem is marked "manual repair needed" (FR-52; review fix, 2026-11-02, approved by Amine). FR-21 still applies: a previous approval never automatically approves the next or any other repair, so an unticked repair also needs the customer's approval (Amine).

#### FR-28: When a repair makes things worse
Ranking should make this rare, but if a repair makes things worse, Nightshift automatically rolls back what it can, stops further automatic repairs on that cluster, and calls a person to approve what to do next (Amine).

#### FR-29: Repair coordinator
A repair coordinator prevents conflicting repairs from running at the same time on the same target. Before starting any repair, Nightshift checks with the coordinator whether another repair is already running on it (Amine). The coordinator also takes into account changes made by Kubernetes' own controllers, the customer's deployments and people, and its marks expire (review fix, 2026-10-30, approved by Amine).
**Example (Codex):** failing disk.
1. Nightshift detects a failing disk on node A, and repair 1 starts draining node A.
2. The coordinator marks node A as unavailable for workload placement.
3. Repair 2 wants to restart a replica. It must not place that replica on node A.
4. Repair 2 can continue on another healthy node if Kubernetes scheduling and availability checks allow it.

- A coordinator runs in each cluster (AI suggestion, accepted by Amine), so local repairs keep working when central coordination is unavailable (5.7). Repairs that affect more than one cluster are coordinated by the management agent, and wait while it is unavailable.

### 5.7 When things go wrong

**Description.** Nightshift follows Danny's coordination model: a Nightshift agent in every workload cluster, a Nightshift management agent on the customer control cluster, and Quornex Fleet at Orvex (Danny, Exchange 4). Every Nightshift agent must keep operating locally when the management agent, the customer control cluster, or the network connection to them is unavailable (Amine; Danny: "each cluster should still be capable of looking after itself independently"). [DESIGN ASSUMPTION unless Danny confirms] A customer with a single cluster has no control cluster; its Nightshift agent works alone, connected only to Quornex Fleet (Amine).

#### FR-30: Limits on repairs adding up
Repairs that are each safe must not add up to an outage (review fix, 2026-10-30, approved by Amine):
- per-cluster rate limits on repairs, based on the impact on workloads, not just the number of repairs (Amine);
- detection of repeated failures, such as the same repair running again and again (Amine);
- checks for conflicting changes before each repair (Amine).

#### FR-31: Recovering from a crash mid-repair
If Nightshift crashes during a repair, it does not go straight back to work when it restarts (Amine).
**Consequences (testable):**
- Repair progress is saved, so Nightshift knows where it stopped.
- The coordinator's marks (for example, "node A unavailable") stay in place.
- After restarting, Nightshift checks the real state. If continuing is safe, it continues; if the state is uncertain, it asks a person.
- **Recovery order** (architecture AP-17, Amine, 2026-11-15): after a crash, Nightshift first applies pending stops, then reconciles every unfinished repair against the real state and re-checks authorisation (including the offline validity of FR-22), evidence and preconditions before any further action. An approval that has expired does not authorise new forward steps; anything still needed after expiry needs a new request with fresh evidence. An external operation already accepted (for example a cloud volume change in progress) is observed and recorded, neither repeated nor cancelled blindly. Safe-stop or rollback steps run only if the catalogue entry pre-authorises them and they are safe in the current state; otherwise the case is escalated. A retry is allowed only while the authorisation is still valid and the action's protections against duplicate and stale execution pass. An automatic action without verified protection against stale or duplicate execution stays manual in the first version. Recovery time is a test result, not a promise.

#### FR-32: Many clusters failing at once
When the same problem hits many clusters at once (for example, a bad update reaching 300 clusters at 3 AM), the on-duty engineer gets **one consolidated urgent alert**, not 300 separate ones. Quornex Fleet recognises the shared problem, stops the update immediately, and coordinates recovery across all the affected clusters. Risky repairs wait (Amine).

Responsibilities (from Codex):

| Action | Who is responsible |
|---|---|
| Detect correlated failures | Quornex Fleet |
| Stop deployment to the remaining clusters | Fleet update controller, automatically |
| Notify the engineer | Fleet alerting system |
| Probation rollback of a Nightshift update, within its update authorisation (FR-47) | A separate rollback guard in each cluster, so the rollback still works when the bad update broke the normal update path (Amine, 2026-10-31; architecture AP-7, Amine, 2026-11-15) |
| Roll back a verified update under a rollback policy the customer authorised in advance (FR-47) | The update path; a rollback must still work even if the bad update broke the normal update path (Amine, 2026-10-31) |
| Approve any other rollback | A Nightshift team engineer, plus the customer's approval (FR-47) |
| Verify recovery | Fleet, plus healthy local monitoring |

- The affected clusters' reports are preserved for the investigation (Amine).
- One Orvex technical approval may cover one problem group across clusters (Amine, 2026-11-03, UX work). A group approval covers one repair at one catalogue version, for a set of clusters that is frozen and shown when the approver approves; clusters that join the problem group later need a new approval. It is recorded per cluster and each cluster is re-checked before it runs. The rollback runs in waves that stop on the stop conditions of FR-46 and FR-47. Each target must hold a valid, unexpired approval before it runs; a later wave cannot reuse an approval that has expired. A group approval never covers a manual dangerous repair (FR-52). Each customer's permission is still needed where customer production is affected (FR-21, FR-47; Amine, 2026-11-03, review of the update).
- **Confirming a group approval** (architecture AP-15, Amine, 2026-11-15): a group approval is an Orvex technical approval only; each cluster still checks its own customer's permission. A Fleet group-confirmation service sends the approver one text message summarising the group, and the approver confirms with a passkey over the group statement. Each cluster checks that its own request is included and matches. The assurance is recorded as "passkey + SMS verification attested by Fleet; not independently verified by the cluster". Limits: the text message confirms a summary, not the full list of targets; the mechanism does not prove what the approver understood; if the portal and the group-confirmation service are both compromised, the text-message step can be skipped without the cluster noticing, though neither can forge the passkey signature or change a cluster's own request.

**Example of the consolidated alert** (illustrative data, pasted by Amine; to feed the UX wireframes):

> **Quornex Fleet: correlated update failure.** Critical.
> 300 affected clusters · 1 fleet-wide problem · suspected update: v2.4
> Fleet action: pause the rollout, preserve the cluster reports, notify the on-duty engineer, and investigate the common cause.

### 5.8 Record

**Description.** "Nothing done in secret" (Danny, `brief.pdf`): Nightshift records what it reads and changes, keeps the record out of its own reach and shows it to the customer.

#### FR-33: Everything recorded, visible to the customer
Everything Nightshift reads and changes is recorded where the customer can see it (Danny, `brief.pdf`).
- "Reads" are recorded as what was accessed, when, why and by whom, without copying customer data into the record (Amine).
- **Stated exception when storage is full** (architecture AP-11, Amine, 2026-11-15): when Nightshift's protected storage is full, new repairs and new repair steps are suspended ("repairs suspended: storage full") and space is reserved for recording stops. If even that space fills, valid, authorised stops are still enforced, and a safe-stop step that is narrowly defined in the catalogue entry, pre-authorised and safe at that moment may run even though it cannot be recorded. This never permits unrecorded forward repairs, which stay blocked. Missing records are reported honestly.
- If the intent of an action cannot be recorded, the action does not run ("blocked: audit unavailable"). Probation rollbacks (FR-47), including false ones, are recorded like any change (architecture AP-7 and AP-20, Amine, 2026-11-15).

#### FR-34: Action history
For every repair, the record holds: the problem and its evidence, the repair and its risk level, who permitted it (ticked, under the last-resort condition, in the agreed management policy with its version, or approved at the time, by whom and when; Amine, 2026-11-03, review of the update), with the assurance level of each approval: "passkey + SMS", "passkey only" or, for a group approval, "passkey + SMS verification attested by Fleet; not independently verified by the cluster" (FR-14, FR-32; architecture AP-2, Amine, 2026-11-15), the result of the verification, and any rollback (product brief; 5.5; 5.6).
- The outcome is one of: worked; did not work and undone; did not work and could not be undone; failed; blocked; cancelled; recovery failed; harmful (Glossary); manual repair reported done (FR-52); exhausted (an action refused, for example by a disruption budget, until its retries ran out; distinct from failed). A blocked repair states why, for example "blocked: disruption budget or rate limit" or "blocked: audit unavailable" (architecture AP-20, Amine, 2026-11-15; wording pending UX review). Rejected requests and expired approvals are recorded too (FR-50, FR-22) (Amine, UX work, 2026-10-31, correcting the AI's "worked / undone" only).
**Consequences (testable):** unapproved changes to customer production can be counted by comparing the execution records with the approval records and policy decisions; the target is 0 (product brief addendum).

#### FR-35: A record Nightshift cannot rewrite
The record is kept out of the Nightshift agent's reach: the agent can add to it but cannot change or delete entries (AI suggestion from session 2, accepted by Amine as important). Quornex Fleet keeps independent checkpoints of the record (FR-6), so a rewritten or destroyed record is detectable, not recoverable (architecture AP-1, Amine, 2026-11-15).

#### FR-36: Other records
- Harmful repairs: every case is recorded and traced (product brief).
- Prediction outcomes, to reduce future false alerts (FR-10).
- The monitoring coverage report (FR-7).
- The signal to Orvex whenever the customer confirms something (FR-12).
- Repair progress, for crash recovery (FR-31).

### 5.9 Learn across the fleet

**Description.** "A new problem in one cluster makes every other cluster ready for it" (Danny, `brief.pdf`), without moving customer data between clusters.

#### FR-37: How a fix joins the repair catalogue
A new fix joins the repair catalogue only once it has been found and tested, and is well controlled. The problem then moves from the incident catalogue to the repair catalogue, with its evidence and explanation (Amine). Its incident history is kept and linked to the validated repair (Danny, Exchange 5).

#### FR-38: What is shared
Only what PRIV-2 allows leaves a cluster. What is shared across the fleet is lessons (rules, catalogue entries, fixes), not customer data (requirements checklist, assumption A2).

#### FR-39: A person reviews every lesson
A person at Orvex reviews each fleet lesson before it is used (Amine, session 2). A new or changed repair catalogue entry needs two reviewers (review fix, 2026-10-30, approved by Amine). Releases, like catalogue entries and the agreed management policy (FR-51), are signed only after testing and two distinct authorised reviewers; the signing system enforces this (architecture AP-18, Amine, 2026-11-15).

#### FR-40: Lessons reach every cluster through the tested release
New repair catalogue entries must pass testing and validation before being distributed through a controlled release, never as one-off changes to single clusters (Amine).

#### FR-41: Tuning within Orvex's limits
Nightshift may tune the cluster's settings only within the limits set by the tested release; anything bigger goes to Orvex as a proposal (Danny, `brief.pdf`: "Nightshift may tune within the limits it sets; anything bigger comes to us as a proposal"; review fix, 2026-10-30, approved by Amine).
- Every tuning action is a repair catalogue entry like any other repair: it has a risk level, follows advance permission and approval (FR-21), is recorded (5.8), and never runs in alert-only mode (after-review fix, 2026-10-31, approved by Amine).
- A proposal that Orvex accepts becomes a tested catalogue entry before it can run; it still needs the customer's permissions like any other repair (after-review fix, 2026-10-31, approved by Amine).

### 5.10 Code fixes (experimental)

**Description.** If the customer opts in, Nightshift can propose a fix for a bug in the customer's own code (product brief). Danny wants it in the first version as an experiment, to learn from real use; it might not stay (Danny, Exchange 2). A code fix follows the same path as every other repair: tested and approved by Orvex, authorised by the existing approval rules, verified and recorded (Amine).

#### FR-42: How a code fix is handled
1. Nightshift proposes a fix for the detected problem.
2. Orvex tests and approves it, to verify that it works and to assess its risks.
3. The fix enters the repair catalogue with its requirements, risk level and rollback procedure: as a fleet-wide entry if it is reusable, otherwise as a **customer-specific entry** that only that customer can access or execute (Amine). Registering every fix keeps Orvex's work traceable (Amine).
4. The customer's authorisation is checked according to FR-21. A code fix changes the customer's own app, so the customer-production row applies: a risky code fix needs the customer's tick or approval and Orvex technical approval (our conservative interpretation of Danny's approval model, see FR-21), and a dangerous code fix is not deployed by Nightshift but left to a person (FR-52).
5. Nightshift deploys the fix if deployment is supported and authorised.
6. Nightshift verifies the outcome and records the result.

(Amine, with Codex.) Nightshift never applies a generated fix on its own (product brief).
- The testing and the engineer's review of the patch (steps 2 and 3; FR-44) check the code itself. They are separate from the approvals FR-21 requires when the fix is about to be deployed, and do not replace them (Amine, 2026-11-02).

#### FR-43: Hosted first, with a separate source-code consent
Code fixes mainly use a trusted, zero-retention hosted model (Section 7), only when the customer separately authorises sending the relevant source code to it. This is a separate, clearly worded consent on top of the code-fix opt-in, separate from external-AI consent (PRIV-8), and off until the customer opts in (Amine, 2026-10-30, after the PRD review). A customer with suitable hardware who wants the code to stay in the cluster can use an in-cluster model instead (architecture AP-6, Amine, 2026-11-15; replaces "in-cluster by default", Amine).
- Only the code relevant to the fix is sent, after secret scanning and the outbound check (PRIV-4), and every transfer is recorded where the customer can inspect it (PRIV-7).
- The customer can withdraw this consent at any time.
- Without this consent or a suitable in-cluster model, code fixes are not available; monitoring and catalogue repairs continue (architecture AP-6, Amine, 2026-11-15).
- Reason: Danny wants code fixes tried in real use and expects to rely heavily on hosted AI for at least the next 3 years; in-cluster only would leave the experiment with very few users (PRD review).

#### FR-44: Testing a code fix
1. Nightshift generates the patch with a trusted hosted model under the separate source-code consent of FR-43, or with the customer's in-cluster model (architecture AP-6, Amine, 2026-11-15).
2. Nightshift creates an isolated test environment within the customer's infrastructure, separate from production.
3. Automated tests run first, checking functionality, security and potential regressions.
4. An Orvex engineer reviews the results and, if the customer authorises it, securely accesses the test environment to inspect the code changes.
5. The engineer approves or rejects the patch.
6. An approved patch enters the repair catalogue as a customer-specific entry, ready for deployment under the existing approval rules (FR-21).

(Amine.)
- If the customer does not authorise the engineer's access, the patch is rejected: no AI-written code reaches production without a person reading it (Amine, 2026-10-31, after the PRD review).
- The engineer's review and the automated tests reduce the risk of a harmful fix but cannot make it certainly safe; a planned validation with planted malicious inputs, including source-code comments, is not yet done and will be reported with its scope, never as proof (architecture AP-6, Amine, 2026-11-15). How the engineer reaches the test environment (step 4), and under which consent and channel, is open (Section 10, item 27).

#### FR-45: Deciding whether to keep the feature
Orvex measures the experiment to decide whether code fixes stay (Amine, with Codex):

| Metric | What we want to know |
|---|---|
| Approval rate | Share of AI-generated patches approved without changes |
| Rework rate | Share needing changes, or rejected |
| Fix success rate | Share that resolve the problem without introducing new bugs |
| Time saved | Engineering hours saved compared with manual fixes |
| AI operating cost | Cost of GPU hours, tokens, electricity and infrastructure |
| Human labour cost saved | Cost of the engineering hours avoided |
| Net cost savings | Labour savings minus AI operating costs and the remaining review, testing and maintenance costs |

### 5.11 Manage the fleet

**Description.** Each cluster looks after itself; Quornex Fleet lets Orvex manage 10,000 of them efficiently: safe updates, escalation of problems, customer isolation and low operating costs (Amine's reading of Danny, Exchange 4). For escalation, Quornex Fleet watches every Nightshift agent (FR-6), groups the same problem across clusters into one alert (FR-32) and gives Orvex grouped views per 100 clusters (FR-15).

#### FR-46: One tested release, rolled out safely
Every cluster runs the same tested Nightshift release (Danny). Quornex Fleet's update controller rolls releases out, and stops the rollout automatically when correlated failures appear (FR-32).
- A release reaches a small group of clusters first, and the rest only once those are healthy (AI suggestion, accepted by Amine). Clusters whose Fleet heartbeat does not reach Fleet (FR-6) are never in that first group and never count as healthy (review fix, 2026-11-02, approved by Amine).
- A paused rollout never resumes on its own: after a set time (assumption to test) it alerts the release owner, and a person must explicitly resume or stop it (architecture AP-19, Amine, 2026-11-15).

#### FR-47: Platform updates and emergency rollbacks
Updating Orvex's own software (Nightshift, Quornex, OMK) changes customer production, so it follows the customer's permissions too (Amine, 2026-10-30; our proposal, pending Danny's confirmation):
- **Routine updates** run under a maintenance policy the customer has authorised, covering the permitted update types and maintenance windows.
- **Security updates** are required by the customer contract: the customer chooses the window, within a short deadline (Amine, 2026-10-31).
- **Probation rollback** (architecture AP-7, Amine, 2026-11-15): a routine update of Nightshift under the maintenance policy includes an exact, bounded rollback in its authorisation: back to the named previous signed release, only within the probation window, only when the probation check fails (including when no fresh healthy signal from the independent checker arrives for that release in time; mechanism to test), and only if the release is marked rollback-safe. It keeps permissions, approvals and safety rules. A release rolled back once is not re-applied automatically. If the release is not rollback-safe or the rollback cannot complete, a person is called. Shared node, network or Kubernetes API failures can still prevent recovery.
- **Rolling back a security update** needs an explicit advance customer policy that covers the recovery version, the known vulnerability it reintroduces and the recovery limits. Without that permission, Nightshift escalates urgently instead of rolling back automatically. Any rollback must be rollback-safe and is recorded; a rolled-back security fix is followed by a plan to restore it (architecture AP-7, Amine, 2026-11-15).
- **Any other emergency rollback** runs without fresh approval only if the customer has explicitly authorised that rollback policy in advance and its safety conditions pass. Otherwise Nightshift asks for approval and escalates. An emergency alone grants no permission.
- Staged rollouts, health checks and stop conditions limit fleet-wide damage (FR-46, FR-32).
- Updates and rollbacks are recorded and visible to the customer like any other change (FR-33), and count towards SM-4: a platform change outside the customer's policy or approval is an unapproved change.

#### FR-48: Customer isolation
A cluster belongs to one customer (Danny). Quornex Fleet is multi-tenant, so one customer's information is never visible to another customer (AI suggestion, accepted by Amine), and what Fleet holds about each cluster is limited to approved, sanitised information (product brief; Section 6).

#### FR-49: Low operating cost
Rules and automation first (FR-17), with every trick to keep model and token costs low (Danny, Exchange 3). Cost targets are in Section 9.

## 6. Constraints: privacy, security and cost

### 6.1 Privacy

**PRIV-1: Private data stays in its cluster.** Private data stays in the cluster it came from, even between clusters of the same customer. Coordination between clusters does not by itself permit private data to move (Amine, 2026-10-28 and 2026-10-30).

**PRIV-2: Only allowed information leaves, by every channel.** Raw data and secrets never leave the cluster; only approved, sanitised information does (product brief). This applies to every way information leaves: a hosted model or shared GPU, Quornex Fleet, notifications (Slack, phone calls and text messages), the portal, dashboards and the morning summary (review fix, 2026-10-30, approved by Amine). Private values are replaced by placeholders such as `<email>` (Amine). Source code sent for a code fix under PRIV-6 is the one deliberate exception to sanitising; it still passes secret scanning and the outbound check (PRIV-4; architecture AP-6, Amine, 2026-11-15).
- **The protection is rule-based.** Allowlisted fields (PRIV-3), placeholders and the mandatory outbound check (PRIV-4) protect what leaves. AI redaction alone never makes data safe to share; it can only be an extra layer (Danny, Exchange 5: "Don't assume AI redaction alone makes data safe to share").
- **What a hosted model receives,** if the customer has consented (PRIV-8): a small message built from approved fields, sanitised with placeholders, so the hosted model has enough to help (Amine). Without consent, nothing is sent to external AI, not even the time and type of a problem; this replaces the earlier "time and type only" rule for the strictest cases (Amine, 2026-11-02).

**PRIV-3: Allowed fields, recipients and destinations.** For each channel, Orvex defines and owns the list of allowed fields, recipients and destinations; anything else is blocked (review fix, 2026-10-30, approved by Amine). For the approval text message, the permitted fields are the action, the target and the one-time code, built from the decision and the catalogue template (FR-14; architecture AP-2, Amine, 2026-11-15).

**PRIV-4: Outbound check.** After everything related to customer data has been removed, a further test runs on every whole line about to leave, by every channel (PRIV-2), to make sure nothing harmful, such as injected instructions, goes out (Amine). The check is mandatory, with no exceptions (Amine, 2026-10-30, after the PRD review); on the three paths outside the gateway it takes the purpose-specific form below, not this line test.
- **Every outbound flow is checked** (architecture AP-8, Amine, 2026-11-15): everything that leaves through the gateway passes this test. Three paths leave outside the gateway (SEC-8): the Fleet heartbeat, downloads of signed packages and, on EKS, the optional read-only calls to the customer's own AWS account. For each, the permitted destinations, operations and request fields are defined, with authentication and limits; read-only access or a destination allowlist alone is not enough. These are purpose-specific controls, not automatically equivalent to the gateway's checks: their enforcement is verified and the remaining risks are documented.

**PRIV-5: Combined views use sanitised information.** The management agent's investigations across clusters and the customer's combined dashboard (FR-15) use only sanitised information from each workload cluster (follows from PRIV-1).

**PRIV-6: Customer code stays in the cluster unless the customer explicitly consents.** The relevant code goes to a trusted, zero-retention hosted model only with the customer's separate, explicit source-code consent (FR-43; Amine, 2026-10-30, after the PRD review; hosted first: architecture AP-6, Amine, 2026-11-15); without it, the code stays in the cluster. This is the only exception to PRIV-1.

**PRIV-8: External AI only with the customer's explicit consent.** Nightshift sends nothing to external AI (Glossary) unless the customer has explicitly consented (Danny, Exchange 5: "external inference with customer consent and zero data retention"; Amine, 2026-11-02).
- Consent is offered during onboarding, with nothing preselected. The consent screen explains what leaves the cluster, which provider processes it, and that the provider must not keep it after processing (zero retention; Section 7).
- Consent covers ongoing use within its stated scope; it is not asked for each request. It is asked again only if the agreed use changes. The customer can change it in the settings (SEC-7).
- Sending source code stays a separate permission (FR-43).
- Without consent, Nightshift uses an AI model inside the customer's cluster if the hardware allows, or works without AI (Section 7).
- A GPU shared across clusters counts as external AI and needs the same consent (AI draft, accepted by Amine, 2026-11-02).
- The rule binds Orvex's own tools too: information from a customer who has not consented is never passed to external AI by Quornex Fleet or by fleet learning (FR-37 to FR-40) (review fix, 2026-11-02, approved by Amine).

**PRIV-9: Every outbound channel is permitted explicitly.** "No outbound data" is broader than "no external AI": nothing leaves the cluster by any channel unless the customer explicitly permits that channel (AI draft, accepted by Amine, 2026-11-02). The Fleet service channel (Glossary), which includes the Quornex Fleet heartbeat (FR-6), is the one required channel of the managed service, accepted with the service; every other channel is permitted explicitly (Amine, 2026-11-03, UX work; Fleet service channel replacing the heartbeat as the required channel: architecture AP-8, Amine, 2026-11-15).
- The channels are: the Fleet service channel (required), external AI (PRIV-8), Fleet reports with sanitised information (FR-32) and the signal of FR-12, notifications (Slack, phone calls and text messages), the approval text message (FR-14), and the portal, which carries the dashboards, the morning summary and approval requests (PRIV-2). The architecture assigns every other outbound flow to one of these channels (review fix, 2026-11-02, approved by Amine; Fleet service channel, approval text message and FR-12 signal: architecture AP-2 and AP-8, Amine, 2026-11-15).
- **Fleet service channel** (architecture AP-8, Amine, 2026-11-15; policy and roster updates, attention notice and field list: Amine, 2026-11-15, remaining points): onboarding discloses its exact flows and the fields each may carry:
  - the Fleet heartbeat (FR-6): agent ID (mapped to the cluster at installation), timestamp, status (alive or degraded) and the audit checkpoint fields `audit_seq`, `chain_head`, `checkpoint_time`, `audit_key_id`, `checkpoint_sig`;
  - requests for the relay's signed status confirmations and signed key lists: cluster identity, versions and sequence numbers;
  - downloads of signed releases, catalogue and model weights: cluster identity and the requested digests or versions;
  - requests for signed policy and roster updates: cluster identity and the versions requested. The signed objects received contain roster data, such as people, roles and credential public keys;
  - the fixed "attention needed" notice after permissions expire (FR-22): a fixed marker, with no other content.

  It carries minimal service metadata; no raw logs, secrets or application content. Authentication, signature verification and the outbound restrictions (PRIV-4, SEC-8) apply. When it is interrupted, the cluster follows the offline rules of FR-22.
- **On EKS, read-only calls to the customer's own AWS account** are separately optional: the customer grants a read-only role, and the responses stay in the cluster. Without it, Nightshift's EKS coverage is reduced and this is reported (architecture AP-8, Amine, 2026-11-15).
- Each permitted channel sends only its allowlisted fields (PRIV-3) and passes the outbound check (PRIV-4). No channel, including the Fleet service channel, is silently exempt; on the three paths outside the gateway, the check is the purpose-specific control of PRIV-4 (architecture AP-8, Amine, 2026-11-15).
- **At onboarding,** Fleet reports, notifications and the portal start ticked (Amine, 2026-11-03, UX work). These are service settings, not consent, and their basis is the service contract: an authenticated customer administrator reviews and confirms them, never the installer. External AI is consent: opt-in, with nothing preselected (PRIV-8). The customer can untick any optional channel (Amine, 2026-11-03, review of the update). [OPEN] Legal basis for the pre-ticked service settings, for a legal review (Section 10, item 23). The approval text message is a separate permission that names the SMS provider and the permitted fields (FR-14); it is opt-in, never pre-ticked, and it also covers the notice sent after each decision (Amine, 2026-11-15, remaining points). Before any administrator exists, the first installation is authorised by the customer's independently verified contract contact, and the first administrator enrols as described in SEC-7 (architecture AP-2 and AP-9, Amine, 2026-11-15).
- **Without the Fleet service channel:** no managed Fleet, so a strict no-outbound deployment is not offered in the first version (FR-6, 3.2).
- **Without Fleet reports:** the cluster is left out of fleet-wide correlation (FR-32) and of the cross-fleet view of problems it would otherwise feed (AI draft, accepted by Amine, 2026-11-02). Blocking Fleet reports does not block the Fleet heartbeat: Fleet still sees whether the agent is reachable, but receives no diagnostic reports (Amine, 2026-11-02). Orvex is also not told when the customer confirms something (FR-12); the cluster records it locally (architecture AP-8, Amine, 2026-11-15).
- **Without the portal:** no approval can be given, because approvals are given only in the portal (FR-14). Only repairs that need no new approval can run: safe ticked repairs, policy repairs (FR-51) and repairs under the last-resort condition (FR-24) (review fix, 2026-11-02, approved by Amine).
  - Turning off portal access blocks new remote approvals. It does not revoke ticks, the agreed management policy or last-resort permissions. Approvals already given stay valid until their validity ends or the repair runs, because the executor verifies them in the cluster (SEC-9). Turning off portal access is distinct from losing contact with Quornex Fleet: the offline limits of FR-22 depend on the Fleet service channel, not on the portal (architecture AP-4, Amine, 2026-11-15). Open requests can then be seen only on the in-cluster dashboard (Amine, 2026-11-03, confirming the UX proposal).
  - Withdrawals, rejections, unticks, the switch to alert-only and authorised settings changes, including ticks, stay possible on the in-cluster dashboard (FR-22; Amine, 2026-11-03, review of the update). The dashboard has a stable internal address and uses separate local passkeys, enrolled in advance through the customer roster. It gives no per-repair approvals; any additional permission a settings change needs still applies there. Each change is recorded and answered with a receipt, which the dashboard shows (architecture AP-13, Amine, 2026-11-15).
- **Without notifications:** no alerts or calls reach anyone, and stops are not confirmed by a separate notice (FR-22): they show as unconfirmed until their receipt is seen. The approval text message, including the notice after each decision, keeps its own permission (FR-14) (architecture AP-2, Amine, 2026-11-15; notice: Amine, 2026-11-15, remaining points).
- **Without notifications as well:** no alert or approval request reaches anyone outside the cluster; only those repairs run; problems are visible only on an in-cluster dashboard.

**PRIV-7: Proving privacy to a customer.** Nightshift gives the customer three layers of evidence (Amine):
1. a record of exactly what left the cluster, which the customer can inspect;
2. regular tests with planted fake secrets, reported honestly as "no planted secrets escaped in these tests", with the test scope stated, never as proof of 100% privacy (product brief addendum);
3. an outside audit.

### 6.2 Security

**SEC-1: Log text is evidence, never an instruction.** A malicious log line could trick the AI into choosing a repair at the wrong time. A separate, rule-based check, not the AI, authorises execution; text in logs is only evidence to investigate (Amine). Further (review fix, 2026-10-30, approved by Amine):
- The AI may suggest which catalogue entry matches, but rule-based checks verify the evidence against the entry's definition.
- An automatic repair needs evidence from more than one independent signal, never a log line alone.
- Approval requests show the facts from the rule-based checks separately from the AI's wording.
- Model responses are treated as untrusted, like log text.

**SEC-2: A compromised agent is contained.** If an attacker takes over the Nightshift agent in one cluster, isolation limits the damage. All four of these are required (Amine; table written with Codex to make Amine's answer clearer):

| Area | Requirement |
|---|---|
| Other clusters and customers | No unauthorised access. Any permitted coordination uses a separate, narrowly scoped identity. |
| Audit records | The agent cannot alter or delete records already accepted by an independently protected audit service. Missing or interrupted reporting must be detectable. |
| Approvals | The agent cannot approve its own repairs, forge approvals or change its permissions. Enforcement sits outside the agent. |
| Hardware credentials | No unrestricted access: limited as in SEC-3. |

**SEC-3: Hardware credentials.** Powerful hardware credentials, such as out-of-band management credentials, are not stored in the agents. They are kept securely and accessed only when needed, with limited permissions (Amine, 2026-10-29). Hardware operations, where needed, go through a separate component whose credentials are limited to specific actions and machines (Amine). Reading (health, power status) is separate from acting (for example a power cycle), and the allowed actions are listed per machine (review fix, 2026-10-30, approved by Amine). In the first version, hardware management access is read-only: Nightshift reads health and power status but never performs hardware power actions; power actions are manual and follow FR-52. This narrows the acting part of this requirement for the first version (architecture AP-10, Amine, 2026-11-15).

**SEC-4: Least privilege.** Nightshift holds only the rights it needs (Danny, `brief.pdf`).

**SEC-5: Signed releases and catalogue.** Nightshift releases, catalogue entries and model weights are signed, and each cluster verifies the signatures before using anything new, so a compromised Quornex Fleet or release pipeline cannot push unapproved changes (review fix, 2026-10-30, approved by Amine).

**SEC-6: Fleet-wide switch-off.** Orvex can switch off one repair catalogue entry across the whole fleet at once (review fix, 2026-10-30, approved by Amine).

**SEC-7: Settings changes.** Only authenticated customer administrators can change modes, ticks, the last-resort condition, delegation, read scope, external-AI consent (PRIV-8), outbound channel permissions (PRIV-9) and source-code consent (FR-43), accept a management-policy change (FR-51) and dispute a classification (FR-21, FR-51); changes are recorded and notified, and alert-only mode is enforced outside the Nightshift agent (review fix, 2026-10-30, approved by Amine; extended 2026-11-02 and 2026-11-03, review of the update). Administrators also grant or decline the approval text message and enable the passkey-only approval fallback for customer approvals; Orvex enables it for Orvex approvals (FR-14; architecture AP-2, Amine, 2026-11-15).
- **First installation and first administrator** (architecture AP-9, Amine, 2026-11-15; provisional): the first installation only is authorised by the customer's contract contact, whose identity and contact details Orvex verifies independently of the installation; this is recorded. All later privileged work needs an enrolled, authorised customer administrator. The first administrator enrols with a one-time code split in two: one half shown through protected local access the customer controls (mechanism to verify per platform), the other sent by Fleet to the contract contact; both halves are bound to that cluster, short-lived and single-use. The contract contact is notified before the enrolment is registered with Fleet. If the enrolment is disputed, it is not trusted, the delayed recovery procedure applies, and Orvex and the customer are alerted. The installer never enrols an administrator. Someone with cluster-admin at installation can still interfere (SEC-10).
- **Local passkeys:** on the in-cluster dashboard, administrators use separate local passkeys enrolled in advance through the roster (PRIV-9) (architecture AP-13, Amine, 2026-11-15).

**SEC-8: A separate executor.** The Nightshift agent that reads logs and other untrusted data is read-only. A separate executor in each cluster holds the rights to change things, and runs a repair only after it has checked the authorisation (tick, approval, agreed management policy or last-resort permission), the safety preconditions and the risk-level conditions itself. All data leaving the cluster passes through a separate gateway, which sends it only through the channels the customer permits (PRIV-9) and enforces the allowed fields (PRIV-3) and the outbound check (PRIV-4), with exactly three exceptions, each with its own identity, destination allowlist and restrictions (PRIV-4): the Fleet heartbeat sent by the independent checker (FR-6), downloads of signed packages from Orvex's registry, and, on EKS, the optional read-only calls to the customer's own AWS account (PRIV-9). Every Nightshift component denies network traffic by default except what it needs; the rules are tested on OMK and EKS, and gaps in enforcement (for example a network plugin that does not enforce outbound rules) are documented (architecture AP-8, Amine, 2026-11-15). Because the executor and the gateway run inside the cluster, enforcement keeps working when the cluster is cut off, within the offline limits of FR-22 (NFR-5) (after-review fix, 2026-10-31, approved by Amine; extended 2026-11-02).

**SEC-9: Authorisations verified in the cluster; Fleet limited.** Approvals, ticks, delegations, last-resort permissions, the agreed management policy (FR-51), and maintenance and rollback policies are signed, and the executor verifies them in the cluster before use, so a compromised portal, Slack integration or Quornex Fleet cannot forge them. Quornex Fleet can send only explicitly permitted commands, such as pausing a rollout, delivering a signed release or switching off a catalogue entry (SEC-6). Unauthorised downgrades are blocked; a controlled, explicitly authorised rollback to an approved recovery version is allowed (FR-47) (after-review fix, 2026-10-31, approved by Amine; extended 2026-11-02). Its limits towards someone holding cluster-admin are in SEC-10.

**SEC-10: Cluster-admin is a documented limit.** Whoever holds cluster-admin or root on a node (Orvex on OMK; the account operator on EKS) can read Nightshift's secrets, rewrite its state in the cluster, remove its admission rules and use any signing access the cluster holds. They cannot forge Orvex-signed objects or a person's passkey signature. Normal work uses limited roles; full Orvex admin access is temporary, approved and recorded. Kubernetes audit logs and Fleet's external checkpoints (FR-6) give partial tamper detection, not protection against a compromised administrator (architecture AP-12, Amine, 2026-11-15).

### 6.3 Cost

The numbers themselves belong in the separate cost-model deliverable.

**COST-1: Two numbers per cluster per month, at 100 and 10,000 clusters** (Danny, Exchange 3; Amine):
- **Technical cost per cluster:** AI tokens or GPU allocation, monitoring compute and storage, network traffic, and Nightshift's share of Quornex Fleet.
- **Total operating cost per cluster:** the technical cost plus human time: Nightshift engineers, support, escalations and ongoing maintenance.

**COST-2: Full GPU costs.** Where a GPU is used, its electricity, hosting, maintenance and replacement costs are included (Amine).

**COST-3: Who pays.** Resources Nightshift uses on customer hardware are counted too, with a clear distinction between what the customer pays and what Orvex pays (Amine).

**COST-4: Proving the business case.** The total operating cost is what the first version compares with the cost of the engineers Nightshift replaces (Vision). The cost model includes a "without Nightshift" baseline: the engineers and cost Orvex would need to run the same clusters by hand (review fix, 2026-10-30, approved by Amine).

**COST-5: Target.** As low as realistically possible while staying close to public-cloud reliability; "even a few dollars per cluster makes a huge difference at scale" (Danny, Exchange 3).

**COST-6: Cheaper must stay reliable.** A cheaper option must not mean slower responses or less capacity (product brief addendum).

## 7. Model options

Nightshift uses AI only where rules and automation cannot do the job (product brief; Danny). **Focus for the first version: the hosted model** (Amine, 2026-10-31), because it should cost much less until in-cluster GPU models become cheaper and more affordable. Exchange 5 keeps this focus possible: Danny allows external inference with the customer's consent and zero data retention. The cost model must show this with numbers (6.3). The in-cluster GPU stays an option, including for code fixes where the customer wants the code kept in the cluster (FR-43; architecture AP-6, Amine, 2026-11-15). Three ways to run the model are compared (Amine, building on Danny's two ways and his question about GPU sharing):

| Option | What it may receive | Notes |
|---|---|---|
| Hosted model | Only with the customer's consent (PRIV-8), and only approved, sanitised data (PRIV-2) | Danny expects to rely heavily on hosted AI for at least the next 3 years (Exchange 3) |
| Shared GPU (across clusters) | The same as a hosted model: only with consent, and only approved, sanitised data | Different costs, control and operating responsibilities from a hosted model. Sharing does not automatically mean Orvex owns or operates it (Amine) |
| In-cluster GPU | Private diagnostic data, within the local permissions | The only option that keeps private data inside the cluster (Danny); used for code fixes where the customer wants the code kept in the cluster (FR-43). GPUs of about 24 GB (~$1,000) and 96 GB (~$10,000 in Danny's figure; Codex found listings of about $14,000–$16,000) are to be explored |

**A trusted hosted model** meets at least these rules: it keeps no customer data after the request (zero retention, required by Danny, Exchange 5), does not train on it, runs in a region and jurisdiction set per customer, uses a pinned model version, and is covered by a contract with Orvex (Amine, 2026-10-31). The rules other than zero retention are our proposal, pending Danny's confirmation.

**Without external AI.** If the customer does not consent to external AI (PRIV-8), Nightshift uses an AI model inside the customer's cluster if their hardware can run it. Without any AI, Nightshift still monitors, detects problems with rules, runs authorised repairs and verifies them, and explains with templates instead of AI (Amine, 2026-11-02; Danny, Exchange 5: "or a local model if nothing can leave").

- [To test] Whether a model on a 24 GB or 96 GB GPU is useful enough, not just whether it fits in GPU memory (product brief).
- [To test] Whether GPU sharing saves money (product brief).
- [To test] Compare local and hosted models on the same problem cases: diagnosis accuracy, unsupported claims, tool-call correctness, response time, and handling of simultaneous problems (product brief addendum).
- GPU price figures and the 36-month cost spreading are in the product brief addendum (partly checked by Codex) and feed the cost model.

## 8. Non-functional requirements

- **NFR-1: Scale.** Designed for 10,000 clusters and about 250 problems a night across the fleet, up to 500 on a bad night (estimates to validate against operational records; product brief). False alerts are not counted as problems (Amine).
- **NFR-2: One design for both platforms.** One Nightshift for OMK on bare metal and for hosted Kubernetes such as EKS (Danny, `brief.pdf`).
- **NFR-3: The same release and configuration everywhere.** Every cluster runs the same tested Nightshift release; differences between customers are only their permissions and settings (Danny; product brief).
- **NFR-4: Nightshift failing never harms the customer.** If Nightshift stops, the customer's workloads keep running; no repair is left half-done without being recorded (FR-31), except the stated exception for stops when storage is full (FR-33), and Quornex Fleet notices the silence through the required Fleet heartbeat (FR-6, PRIV-9; AI suggestion, accepted by Amine; required heartbeat: Amine, 2026-11-03, UX work). Through the audit checkpoint the heartbeat carries, Fleet can also detect a rewritten or destroyed audit record (FR-35; architecture AP-1 and AP-11, Amine, 2026-11-15).
- **NFR-5: Local autonomy.** Each cluster keeps working on its own when central coordination is unavailable (Vision; 5.7). It does so within the offline limits of FR-22: monitoring, stops, recording and repairs whose required authorities are all customer-held continue; repairs that need Orvex authority pause after 1 hour and stop after 24 hours without a fresh confirmation from Quornex Fleet (architecture AP-4, Amine, 2026-11-15).
- **NFR-6: Small, measured footprint.** Nightshift's own use of the customer cluster's CPU, RAM, storage, network and AI or GPU is measured and reported, and counted in the cost (COST-3; AI suggestion, accepted and detailed by Amine). Target to set.
- **NFR-7: Timely warnings.** Predictions and alerts arrive early enough to act before impact (FR-9). [OPEN] Numeric targets, for example the maximum delay between a node heartbeat going missing and the alert.
- **NFR-8: Understandable by non-experts.** Every message to the customer can be understood by a business owner without infrastructure expertise (FR-11; Danny, Exchange 4).

## 9. Success metrics

All targets are proposed acceptance targets, not observed performance (product brief addendum, Codex-checked). They are checked first in controlled tests with failure injection, then on the first 100 clusters (product brief). The first 100 clusters see only about 2.5 problems a night, too few to validate rare events such as harmful repairs, so those are validated mainly with failure injection (review fix, 2026-10-30, approved by Amine).

**Primary**
- **SM-1: Early detection.** At least 80% of supported, slowly developing problems are detected before the customer feels them. Measured by comparing alert times with failure-injection records and app health checks (product brief addendum). Validates FR-8 to FR-10.
- **SM-2: Repair success.** At least 95% of authorised repairs restore health without causing another problem. Measured from action records, before-and-after health checks and incident reviews (product brief addendum). Validates FR-25 to FR-28.
- **SM-3: Harmful repairs.** Counted separately from repairs that did not work. Zero harm is the goal; every case is recorded and reviewed (Vision; product brief). Validates FR-28.
- **SM-4: Unapproved changes to customer production: 0.** Measured by comparing execution records with approval records and policy decisions (product brief addendum), cross-checked against independent sources such as Kubernetes audit logs, not only Nightshift's own records (review fix, 2026-10-30, approved by Amine); these give partial tamper detection, not protection against someone holding cluster-admin (SEC-10). A policy repair that turns out to have affected customer production counts as an unapproved change (Amine, 2026-11-02, after the review of the update). Validates FR-21, FR-34, SEC-2.
- **SM-5: Explanations.** Nightshift provides an evidence-based explanation for supported problems and states uncertainty when the cause is unknown (Vision). Customer feedback on clarity and usefulness is measured separately; target to set (product brief). "Explained" is measured with a mix of three checks (Amine): every message contains the FR-11 parts; when the cause is later confirmed, Nightshift's explanation was right; and the customer found it clear. Validates FR-11.

**Secondary**
- **SM-6: Alert quality.** At least 90% of alerts are confirmed by Orvex support and the Nightshift team as needing attention; each alert is labelled actionable, duplicate or false alarm (product brief addendum). Validates FR-9, FR-13.
- **SM-7: Availability.** At least 99.9% monthly availability of customer-facing platform services, about 43 minutes of downtime a month. This is a working target, not a promise: what is achievable depends on the customer's hardware and on whether the installation is highly available (Danny, Exchange 5).
- **SM-8: Engineers.** About 15 Nightshift engineers for 10,000 clusters, about 670 clusters each (Amine's estimate, to test; the product brief's earlier range was 350–400). Reason: most problems do not need a risky or dangerous repair, and safe ticked repairs run on their own (Amine). At night, one engineer is on duty, with 2 or 3 backup engineers who help remotely from home only when needed, for example on a bad night (Amine). Measured on the first 100 clusters, then extrapolated (product brief addendum). For scale: at 250 problems a night with 90% handled automatically and 20 minutes for each of the rest, the human work is about 8 hours a night; at 500, about 17 hours. If only 60% were handled automatically at 45 minutes each, it would be about 75 hours a night at 250 problems: the staffing estimate depends heavily on the automatic share (Codex's arithmetic in the product brief addendum).
- **SM-9: Share of problems needing a person.** The share of problems that need Orvex technical approval or a manual repair (FR-52). It drives SM-8. Target to set; the staffing arithmetic above assumes 90% are handled automatically.
- **SM-10: Cost per cluster.** Technical and total operating cost per cluster per month, at 100 and 10,000 clusters (COST-1). Target: as low as realistically possible (Danny).
- **Code-fix experiment:** the metrics in FR-45.

**Counter-metrics (do not optimise)** (AI suggestion; wording by Amine)
- **SM-C1: Missed problems.** Fewer false alerts is good, but not if Nightshift stays silent about real problems: track problems that reached the customer without a warning. Counterbalances SM-6.
- **SM-C2: Harm from automation.** More automatic repairs is good, but not if those repairs cause damage. Counterbalances SM-9 with SM-3.
- **SM-C3: Privacy for cost.** Lower AI cost is good, but not if Nightshift sends private data outside to achieve it: track failures of the planted-secret tests (PRIV-7). Counterbalances SM-10.

## 10. Open questions

Triage (Amine, 2026-10-31; updated 2026-11-02 after Danny's Exchange 5 and 2026-11-03 after the UX work): none of the remaining items blocks UX or architecture. Danny's open questions (5–7b, 19, 20) are owned by Danny and revisited when he replies; our proposals stand meanwhile. Questions 19 and 20 have not been sent yet; Amine decides whether to send them. Item 21 is decided (Amine, 2026-11-03). Timing targets (8) go to the architecture and UX to propose and test. Approval validity (18) and channel defaults (22) were decided in the UX work (Amine, 2026-11-03). Targets still to set (12) and the items to test (13–17) are owned by Orvex and revisited in the controlled tests and on the first 100 clusters. Item 23 (legal basis for the pre-ticked service settings) goes to a legal review, owned by Orvex. Updated 2026-11-15 with the architecture reconciliation: item 7a and the undo-reject window are decided; items 24 to 30 were new open design items and items 31 to 33 new items to test. Items 24, 25, 26, 28, 29 and 30 were decided later the same day (Amine, 2026-11-15, remaining points); item 27 stays open.

**For Danny** (not yet asked unless stated):
- **5.** What monitoring and night cover does Orvex have today?
- **6.** Which hosted models and regions count as "trusted"? Partly answered in Exchange 5: consent and zero retention are required. Our proposal for the rest is the minimum rules in Section 7.
- **7b.** How should code fixes be priced? (Amine's proposal: by tokens or difficulty; Danny has not addressed it.)
- **19.** Who decides what counts as a "high-confidence" repair: Orvex, the customer, or both? (danny-qa #3, never sent.) Our current answer: the repair catalogue entry defines the evidence needed to match it (FR-18).
- **20.** What happens when an approval request gets no answer, for example at 3 AM? (danny-qa #4, never sent.) Our proposal is FR-23.

**Design decisions still open:**
- **8.** How long a node heartbeat may be missing before it counts as missing, and other timing targets (FR-2, FR-15, NFR-7).
- **12.** Targets still to set: harmful repairs, explanation feedback, Nightshift's footprint, share of problems needing a person, and the success record needed before a repair can be reviewed for reclassification.
- **23.** Legal basis for the pre-ticked service settings at onboarding (PRIV-9): for a legal review. Owner: Orvex (Amine, 2026-11-03, review of the update).
- **27.** Code-fix engineer access to the isolated test environment (FR-44 step 4): needs its own consent and channel design (architecture outbound flow 14).

**To test:**
- **13.** Every estimate: 250 problems a night (500 on a bad night), about 15 engineers, the success targets.
- **14.** The 30-minute last-resort threshold (Amine's proposal).
- **15.** Whether a model on a 24 GB or 96 GB GPU is useful enough, not just whether it fits; whether GPU sharing saves money.
- **16.** Whether sanitising keeps private data inside the cluster (planted-secret tests, PRIV-7).
- **17.** How well the signals in FR-8 actually predict failures.
- **31.** The offline validity tiers (1 hour, 24 hours) and the 2-minute undo-reject window (FR-22, FR-50).
- **32.** Approval confirmation (FR-14): feasibility and usability, the 60-second targets and the 5-minute code lifetime.
- **33.** Enforcement of the three purpose-specific outbound controls and the default-deny network rules on OMK and EKS (PRIV-4, SEC-8), and the probation rollback's healthy-signal mechanism (FR-47).

**Answered and decided:**
- **1.** Who approves risky changes to OMK and Quornex: answered in Exchange 5, an authorised Orvex engineer, plus the customer when customer production is affected; routine, tested platform repairs run under the agreed management policy (FR-21, FR-51).
- **2.** Whether Orvex technical approval on top of the customer's fits Danny's model: answered in Exchange 5, "broadly fits", but not every repair needs both (FR-21).
- **3.** Whether private data may never move between a customer's own clusters (PRIV-1): Danny called the privacy boundary "a good starting point" (Exchange 5). PRIV-1 stands.
- **4.** "Close to public-cloud reliability" as a number: 99.9% a month, as a working target, not a promise (Exchange 5; SM-7).
- **7.** The exact hand-in date: answered, between 10 and 14 November 2026 (Amine, 2026-10-30).
- **7a.** Where code fixes run: decided, hosted first under a separate source-code consent, with an in-cluster model where the customer prefers it (FR-43; architecture AP-6, Amine, 2026-11-15; follows Danny's Exchange 3 and the consent rule of Exchange 5). Was: in-cluster by default.
- **9.** Through whom Nightshift escalates provider-side problems on hosted Kubernetes: decided, through the customer (5.4).
- **10.** Whether a customer control cluster runs its own Nightshift agent: decided, yes; Fleet watches it like any other (FR-6).
- **11.** Whether a code fix can be approved on automated test results alone: decided, no, the patch is rejected (FR-44).
- **18.** How long an approval stays valid before it expires: decided, each repair catalogue entry states it; Orvex sets the value when testing the entry (FR-22; Amine, 2026-11-03, UX work).
- **21.** Whether risky repairs to the customer's own app need Orvex technical approval as well as the customer's: decided, yes, as our conservative interpretation of Danny's approval model; not asked again, since it does not change the architecture (FR-21; Amine, 2026-11-03).
- **22.** The default state of each outbound channel at onboarding: decided, the Fleet service channel (including the Fleet heartbeat) is required with the managed service (architecture AP-8, Amine, 2026-11-15); Fleet reports, notifications and the portal start ticked; external AI starts with nothing preselected (PRIV-9; Amine, 2026-11-03, UX work). The approval text message is opt-in (item 24).
- **24.** The default of the approval text-message permission: decided, opt-in at onboarding, not pre-ticked (FR-14, PRIV-9) (Amine, 2026-11-15, remaining points).
- **25.** How "I've done it" is authenticated: decided, a fresh passkey check, no text-message code; only the named performer or the agreed customer representative may report it (FR-52; UX O-8) (Amine, 2026-11-15, remaining points).
- **26.** How stops are confirmed: decided, a rejection, withdrawal or untick needs a fresh passkey check but no text-message code; the notice after a stop confirms it (FR-14, FR-22) (Amine, 2026-11-15, remaining points).
- **28.** The attention notice and policy and roster updates: decided, both belong to the Fleet service channel, with the exact permitted fields listed in PRIV-9; roster updates carry roster data in the signed objects received (Amine, 2026-11-15, remaining points).
- **29.** An Orvex technical approval already received, in the stale tier: decided, no exception; actions that need fresh Orvex authority pause (FR-22) (Amine, 2026-11-15, remaining points).
- **30.** The permission for the notice after every decision: decided, the approval text-message permission (FR-14, PRIV-9) (Amine, 2026-11-15, remaining points).
- **Undo-reject window:** decided, 2 minutes as a starting value to test, timed by the cluster (FR-50; architecture AP-16, Amine, 2026-11-15; test: item 31).

## 11. Requirements for the other deliverables

The PRD sets what the other hand-in documents must contain:
- **All deliverables:** keep it practical and explain the assumptions and trade-offs; Orvex wants the reasoning, "not a finished production design" (Danny, Exchange 5).
- **Architecture:** names the open-source projects used to collect, store, detect and act, the alternatives rejected and why; shows what runs per node, per cluster and centrally at Orvex; explains what changes between bare metal and EKS, and what happens if Nightshift fails (`brief.pdf`).
- **Failure catalogue:** the 20 most important failures, ranked, each tagged *predict*, *fix* or *only report*, per platform (OMK and EKS; `brief.pdf`).
- **Cost model:** technical and total operating cost per cluster per month (COST-1) for each model option in Section 7 and for working without any AI, with the share of customers who consent to external AI as an input (PRIV-8), at 100 and 10,000 clusters, and what moves the cost most (main drivers and sensitivity; `brief.pdf`).
- **Privacy and security review:** covers Section 6, including untrusted log text and a compromised agent (`brief.pdf`).
- **Intelligence:** the architecture says what is done with rules and statistics and what needs a language model, how Nightshift works with and without an in-cluster GPU, without external-AI consent and without any AI (Section 7), and the expected number of model calls, which the cost model needs (`brief.pdf`; review fix, 2026-10-30, approved by Amine).
