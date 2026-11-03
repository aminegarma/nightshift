# Security and privacy review (second pass, after fixes): Nightshift PRD

- **Reviewed:** `prd.md` (updated 2026-10-31) and `addendum.md`, judged as they stand. Earlier review files were not read.
- **Reviewer:** security and privacy reviewer (AI)
- **Date:** 2026-10-31
- **Scope:** Section 6 (PRIV-*, SEC-*); every feature in Section 5 that reads untrusted data or changes things; the Glossary terms for approval, advance permission and the modes; FR-47; SEC-3.

## Verdict

The PRD now states the right principles: log text is evidence, approvals are single-use and bound to the repair, a compromised agent cannot approve its own repairs, releases are signed, and data leaves only through approved fields. But it still does not say **where** these controls are enforced or **who holds the rights to act**. As written, the Nightshift agent can hold the write rights it is told not to misuse. The central systems that issue approvals, ticks and policies (portal, Slack integration, Quornex Fleet) are trusted without any check inside the cluster. Two critical and eleven high findings remain. All of them can be fixed with requirement-level wording; none needs a redesign of the product.

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 11 |
| Medium | 11 |
| Low | 5 |

### What improved and should be kept
- The Approval definition binds an approval to "the exact repair, target, catalogue version and evidence shown" and makes it single-use.
- SEC-1 separates rule-based facts from the AI's wording, treats model output as untrusted, and needs more than one signal for an automatic repair.
- SEC-2 has four parts, and its approvals part says that "Enforcement sits outside the agent".
- SEC-3 separates reading from acting and lists allowed actions per machine.
- SEC-5 signs releases, the catalogue and model weights. SEC-7 protects the settings and enforces alert-only mode outside the agent.
- PRIV-2 covers every channel. PRIV-7 keeps honest wording about the planted-secret tests.
- FR-47 says that "An emergency alone grants no permission."
- FR-44 says no AI-written code reaches production unless a person has read it.

---

## Critical

### SEC-R2-01: The rights to act are not separated from the agent that reads untrusted data
- **Where:** SEC-1, SEC-2 (Approvals row), SEC-4, FR-21, FR-22, Glossary "Risk level"
- **Text:** SEC-1: "A separate, rule-based check, not the AI, authorises execution". SEC-2: "The agent cannot approve its own repairs, forge approvals or change its permissions. Enforcement sits outside the agent." SEC-4: "Nightshift holds only the rights it needs". Glossary: "The same action can have different risk levels depending on its conditions".
- **Problem:** The PRD moves the **approval** check outside the agent, but nothing says that the **rights to change things** (Kubernetes write rights, node drain, restarts, cleanup, deployments) sit outside the agent. It also does not say where the rule-based check, the precondition re-check (FR-22) and the risk-condition evaluation run. If they run in the agent process, which also reads logs and talks to the model, then "enforcement outside the agent" means nothing in practice.
- **Attack:** An attacker gets code execution in the workload-cluster agent, for example through a parser bug triggered by a crafted log line, or through a poisoned dependency. The agent's service account can patch Deployments and delete pods. The attacker never asks for an approval: they use the service account directly to scale checkout to zero, or to roll a Deployment to an attacker-chosen image. A subtler version: the agent evaluates "healthy replicas can carry the traffic" itself and reports it true, so a risky "restart the only replica" is classed as a safe "restart one replica" and runs automatically with no human involved.
- **Fix (requirement):** Add **SEC-8: Separate executor.**
  - (a) The Nightshift agent (collection, analysis, model calls) holds read-only rights and no write rights to customer production.
  - (b) All changes go through a separate in-cluster executor. It accepts only a signed catalogue action ID plus a verifiable authorisation (a tick, an approval or a policy; see SEC-R2-02). It evaluates the preconditions and the conditions that set the risk level itself, from data it reads directly from the Kubernetes API or the hardware component, not from the agent.
  - (c) The executor runs no model and does not parse log text.
  - (d) In alert-only mode the executor holds no write rights at all.
  - (e) Acceptance test: with the agent fully compromised (simulated by giving an attacker the agent's credentials), no write to customer production succeeds without a valid authorisation. SM-4 measures this.

### SEC-R2-02: Approvals, ticks and policies can be forged centrally, and Fleet's powers are unbounded
- **Where:** Glossary "Approval", "Advance permission", "Maintenance policy"; FR-14, FR-21, FR-32, FR-47, SEC-5, SEC-7
- **Text:** "Approval: a yes given by an authenticated person at the time, for one repair, through Slack or the Quornex portal". FR-32: "Quornex Fleet recognises the shared problem, stops the update immediately, and coordinates recovery across all the affected clusters." SEC-5: "so a compromised Quornex Fleet or release pipeline cannot push unapproved changes".
- **Problem:** SEC-5 protects **releases and the catalogue** against a compromised Fleet. It does not protect **approvals, ticks, delegations, last-resort permissions, maintenance policies or rollback policies**. All of these are created in the Quornex portal or Slack and pass through Orvex's central, multi-tenant systems before they reach a cluster. SEC-2 only considers a compromised **agent**. The PRD never considers a compromised portal, Slack integration or Fleet, nor any limit on what Fleet may order clusters to do.
- **Attack:** An attacker compromises the portal backend or the Slack app's signing secret, or an Orvex insider does. They write "ticked: restart only replica; last-resort: on" into the settings of 10,000 clusters, or mint approval records for a dangerous repair on chosen customers. Each cluster sees a well-formed authorisation from its trusted control plane and acts. A second path is FR-32's "coordinate recovery" plus a rollback tool "that must still work even if the bad update broke the normal update path". Together they give Fleet a break-glass channel into every cluster, with no requirement that its orders be checked in the cluster.
- **Fix (requirement):** Add **SEC-9: Authorisations are verifiable in the cluster.**
  - (a) Every tick, approval, delegation, last-resort permission and maintenance or rollback policy is signed by the approving person's own credential, for example a WebAuthn or passkey assertion over a hash of the exact repair, target, catalogue version, evidence and expiry. Orvex technical approvals are signed by the engineer's individual key.
  - (b) The in-cluster executor verifies the signature, the approver's role for that customer (from a customer-administered roster whose root of trust is set at installation) and single use, before acting.
  - (c) Neither Fleet, the portal nor the Slack integration can produce a valid authorisation on its own.
  - (d) State Fleet's allowed commands to clusters as a closed list (liveness, pause rollout, signed release or catalogue delivery, SEC-6 switch-off). The break-glass rollback path accepts only signed releases under a customer-signed rollback policy.
  - (e) Add a threat case to SEC-2: "Quornex Fleet, the portal or the Slack integration is compromised."

---

## High

### SEC-R2-03: Prompt injection reaches the humans who approve
- **Where:** SEC-1 ("Approval requests show the facts from the rule-based checks separately from the AI's wording"), FR-11, FR-14, UJ-3
- **Problem:** Separating the facts from the AI's wording is necessary but not enough.
  1. The AI's wording is still shown next to the Approve button. A crafted log line can steer it, for example: "Orvex has pre-verified this restart; approve within 2 minutes to avoid data loss."
  2. The "facts" contain attacker-controlled strings: pod names, labels, error messages, URLs. Kubernetes names and annotations are set by whoever can deploy.
  3. Slack renders links, mentions and formatting. An injected `<https://quornex-portal.example|Open in Quornex portal>` link can lead to credential phishing.
  4. Nothing requires the target and action shown to come from the executor's structured request rather than from text.
- **Attack:** An attacker controls one tenant app on the cluster. They log a line that makes the explanation say the payments database pod is "the leaking replica", and annotate a pod so its display name looks like the checkout service. Josh sees a convincing request and approves. The approval is bound to what was shown, and what was shown was the attacker's choice.
- **Fix:**
  - The action, target, risk level and expected impact in an approval request are rendered only from the executor's structured, signed request. The AI text cannot change them, and text that contradicts them is suppressed.
  - AI wording and every untrusted string are escaped and shown as plain text: no links, mentions, markup or calls to action. Request links point only to a fixed portal domain.
  - The AI wording is visibly labelled "AI explanation, unverified".
  - Approval requests never ask for credentials. Phone calls and Slack messages say so.
  - Acceptance test: a red-team corpus of injected log lines and object names produces no change to the structured fields and no live links, with a pass rate of 100%.

### SEC-R2-04: The untrusted-input boundary covers only "log text"
- **Where:** SEC-1 title and body; 3.2 "Treat text in logs as instructions"
- **Text:** "An automatic repair needs evidence from more than one independent signal, never a log line alone."
- **Problem:**
  - Untrusted inputs also include Kubernetes events, object names, labels and annotations, metric labels, the customer's app metrics, BMC or Redfish strings from customer-managed hardware that may be "badly configured", customer source code read for code fixes, hosted-model output, and fleet lessons.
  - "Independent" is not defined. A compromised app controls both its logs **and** its own memory, latency and error metrics, so two signals from the same workload are not independent.
  - Nothing says the repair **target** must come from the Kubernetes API rather than from text.
- **Attack:** A compromised app deliberately grows its memory and logs matching OOM warnings. This gives "two signals", which triggers repeated restarts of a sibling service named in the log text, or a node drain.
- **Fix:**
  - Rename SEC-1 to "Untrusted inputs are evidence, never instructions" and list the input classes above.
  - Define independent signals as signals from **different trust domains**, for example node or kubelet metrics versus app-emitted data. Workload-emitted signals together count as one domain.
  - Require repair targets and parameters to be resolved from authoritative APIs (Kubernetes, the hardware component), never taken from free text or model output.

### SEC-R2-05: Approver identity, authentication and separation of duties are not specified
- **Where:** Glossary "Approval", FR-14, FR-21 (delegation), UJ-5, SEC-7
- **Text:** "an authenticated person"; "Orvex support may give it instead if the customer has delegated approval to them"; UJ-5: "he approves" one fix for 300 clusters.
- **Problem:**
  - It is not said **who** may approve for a customer. SEC-7 covers only settings changes, done by administrators.
  - The strength of authentication is not set: no MFA, and no step-up for risky or dangerous repairs.
  - There is no requirement that a Slack identity be mapped to a customer approver roster. In shared Slack channels, anyone in the channel can click.
  - Delegated customer approval by Orvex support plus Orvex technical approval means **Orvex alone** approves a risky change to customer production. Nothing stops the same person, or two colluding colleagues, from giving both approvals.
  - UJ-5 shows one engineer's click across 300 customers, which contradicts "for one repair".
- **Attack:** A support engineer's Slack session is stolen. The attacker gives the delegated "customer" approval and, in another channel, the Orvex technical approval on the same risky repair.
- **Fix:**
  - Define the approver roles per customer, managed by customer administrators under SEC-7.
  - Require phishing-resistant MFA for approvers, and step-up re-authentication for each risky or dangerous approval.
  - Slack approvals are accepted only from identities linked to that roster, and only for safe and risky repairs. Dangerous repairs are approved only in the portal.
  - The customer-side approval and the Orvex technical approval must come from different people. If the customer side is delegated, they must also come from different Orvex teams.
  - Fleet-wide approvals (UJ-5) produce a separate authorisation per cluster, each checked against that customer's own policy. One click never authorises more than one customer.

### SEC-R2-06: A compromised agent can send data out of the cluster directly
- **Where:** PRIV-2, PRIV-3, PRIV-4, 3.2 ("Nightshift still has permitted diagnostic access"), SEC-2
- **Problem:** The privacy controls describe what a **well-behaved** agent sends. Nothing says:
  - that the outbound sanitiser and the PRIV-4 check run outside the agent;
  - that the cluster's network blocks any destination not on the PRIV-3 list;
  - what "permitted diagnostic access" to customer databases covers;
  - whether the agent can read Kubernetes Secrets.

  SEC-2 does not list exfiltration among its four containment areas.
- **Attack:** The compromised agent uses its diagnostic database credentials to dump customer tables, then sends them over HTTPS to an attacker host, or hides them inside "sanitised" model calls. The sanitiser it skipped was inside its own process.
- **Fix:**
  - Add a fifth SEC-2 row, "Data exfiltration". Outbound traffic from Nightshift components passes through an egress gateway outside the agent that enforces the PRIV-3 destinations, sanitisation and the PRIV-4 check.
  - A network policy blocks all other egress.
  - Define diagnostic access as metadata and health queries only: no reading of table contents and no reading of Kubernetes Secrets, unless a scoped exception is recorded under FR-33.
  - Every byte that leaves is logged at the gateway (PRIV-7 layer 1).

### SEC-R2-07: Code fixes leak customer code through the catalogue and the release
- **Where:** FR-42 step 3, Glossary "Customer-specific entry", FR-40, NFR-3
- **Text:** "as a fleet-wide entry if it is reusable, otherwise as a customer-specific entry that only that customer can access or execute". FR-40: "distributed through a controlled release, never as one-off changes to single clusters". NFR-3: "Every cluster runs the same tested Nightshift release".
- **Problem:**
  1. A patch written against customer A's proprietary code becomes a **fleet-wide** entry because Orvex judges it "reusable". Customer A has not agreed to share it.
  2. If customer-specific entries ship inside the single fleet-wide release, every cluster receives customer A's patch. "Only that customer can access or execute it" is then only a promise that a compromised or curious agent can break.
- **Fix:**
  - A code fix derived from a customer's code becomes fleet-wide only with that customer's explicit written consent, after review to remove any of their identifiers or code.
  - Customer-specific entries are delivered and stored only in that customer's clusters (signed, and encrypted to those clusters), outside the shared release.
  - State this as an explicit exception to FR-40 and NFR-3.

### SEC-R2-08: Code-fix deployment rights, the test environment and secrets in code
- **Where:** FR-42 step 5, FR-43, FR-44 steps 2 and 4, PRIV-6, 3.2
- **Text:** "Nightshift deploys the fix if deployment is supported and authorised." "Nightshift creates an isolated test environment within the customer's infrastructure". "An Orvex engineer ... securely accesses the test environment". PRIV-6: "This is the only exception to PRIV-1."
- **Problem:**
  - (a) Deploying code needs write access to the customer's repository, registry or CI. A compromised agent with that right can push a backdoor into the customer's app.
  - (b) Nothing binds the deployed artefact to the reviewed patch, for example by hash.
  - (c) The test environment's isolation is undefined: is it fed production data or secrets? Can it reach the internet? AI-written code under test can call out to the internet.
  - (d) The engineer's access is a new way **into** customer infrastructure and a new way for data to leave (a human reading code). It is not in the PRIV-2 channel list, and PRIV-6's "only exception" is therefore wrong.
  - (e) Code sent to a hosted model may contain hard-coded secrets, which contradicts PRIV-2 "secrets never leave".
  - (f) A patch can contain a database migration that modifies records, which is a prohibited action reached indirectly.
- **Fix:**
  - Code fixes are delivered as a pull request or change request in the customer's own pipeline. Nightshift never holds push or deploy rights to app code.
  - The approved catalogue entry pins the patch hash, and the executor deploys only that hash.
  - The test environment uses synthetic or customer-approved data, has no production credentials and no egress except the model endpoint, and is destroyed after use.
  - Engineer access is just-in-time, per patch, time-limited, recorded in a session log the customer can see, and listed as a PRIV-2 channel.
  - A secret scan and redaction run before any code goes to a hosted model.
  - Patches that touch schemas, migrations or data-deletion paths are rejected as prohibited actions.

### SEC-R2-09: Platform updates and rollbacks: downgrade, key custody, update classification
- **Where:** FR-47, FR-32, FR-46, SEC-5, Glossary "Maintenance policy"
- **Text:** "Routine updates run under a maintenance policy the customer has authorised, covering the permitted update types". FR-32: "a rollback must still work even if the bad update broke the normal update path ... Whether that needs a separate tool is for the architecture".
- **Problem:**
  - (a) A rollback installs an **older signed** release. Without a version floor, an attacker or a compromised Fleet can "roll back" clusters to a validly signed version with a known vulnerability (a downgrade attack).
  - (b) Signing-key custody is not stated. If the release pipeline holds the key, "a compromised release pipeline cannot push unapproved changes" is false.
  - (c) Orvex alone labels an update's "type". Labelling a risky change as "routine security patch" fits it into the maintenance policy (a confused deputy).
  - (d) The Nightshift release also contains the executor and the approval checks, so a routine update can weaken the enforcement itself.
- **Fix:**
  - Signing keys are held in an HSM outside Fleet and the pipeline. Signing needs the two FR-39 reviewers (threshold signing).
  - Each cluster enforces a minimum version and a list of revoked versions. Rollback only to versions not on that list.
  - The update type is part of the signed release metadata, and the cluster checks it against the policy. Releases that change the executor, the authorisation checks or the egress gateway are never "routine": they need customer approval.
  - The break-glass rollback path is limited to installing a signed, non-revoked release under a customer-signed rollback policy.

### SEC-R2-10: The hardware component acts on request with no authorisation of its own
- **Where:** SEC-3, FR-7, FR-3
- **Text:** "Hardware operations, where needed, go through a separate component whose credentials are limited to specific actions and machines." FR-7: installation "validates access ... including credentials".
- **Problem:**
  - Limiting the component to "power-cycle node 7" does not stop a compromised agent from **asking** it to power-cycle node 7 at peak time.
  - Who holds the BMC credentials during installation, and whether Orvex staff ever see them, is not stated.
  - BMC networks are often flat, and customer hardware may use default BMC passwords. The component then becomes a route to every BMC.
  - The risk level of power actions is not stated.
- **Fix:**
  - The hardware component performs actions (not reads) only on a verified authorisation (SEC-9) for that machine and action.
  - Use separate BMC accounts: a read-only one for monitoring and an operator-role one for actions. Never use administrator accounts.
  - Credentials are entered by the customer into an in-cluster secret store. Orvex staff and Fleet never receive them.
  - Installation flags default or shared BMC passwords, and BMC traffic is limited to the listed machines.
  - Power cycle, power off and firmware actions are dangerous by default.

### SEC-R2-11: FR-41 tuning bypasses the authorisation model
- **Where:** FR-41, Glossary "Customer production"
- **Text:** "Nightshift may tune the cluster's settings only within the limits set by the tested release"; Glossary: "A change that can affect customer production needs the customer's advance permission ... or the customer's approval per action".
- **Problem:** Tuning changes customer production, but FR-41 needs no tick, no approval and no rule-based check, and does not say whether the AI chooses the value. Crafted logs can steer the AI to tune resource limits, autoscaler bounds or timeouts to the most harmful value allowed. SM-4 would not count this as unapproved.
- **Fix:** Tuning actions are repair-catalogue entries with risk levels, chosen and bounded by rule-based checks. They are subject to FR-21, executed by the SEC-8 executor, and recorded under FR-34.

### SEC-R2-12: The management agent's rights and its compromise are not covered
- **Where:** FR-6, FR-29 ("Repairs that affect more than one cluster are coordinated by the management agent"), PRIV-5, SEC-2
- **Problem:** SEC-2 contains one compromised **workload** agent. The management agent coordinates every workload cluster of a customer, and runs next to the control cluster's own agent. Its rights in the workload clusters (read, coordinate, act?) are not stated. If it is compromised, every workload cluster of that customer is open.
- **Attack:** A crafted log on the control cluster leads to compromise of the management agent. It issues "coordinated" repairs, for example a drain, to all of the customer's workload clusters.
- **Fix:**
  - The management agent holds no write rights in workload clusters. It can only propose cross-cluster repairs, which each cluster's executor authorises separately.
  - The management agent and the control cluster's own agent run under separate identities.
  - Add "management agent compromised" as a SEC-2 case with the same four containment areas.

### SEC-R2-13: The hosted model is the main way data leaves, and its terms are not specified
- **Where:** Section 7 (hosted model is the focus for version 1), PRIV-2, open question 6
- **Text:** PRIV-2: "a small message built from approved fields, sanitised with placeholders ... 'Time and type only' is kept for the strictest cases".
- **Problem:**
  - "Trusted" is undefined (open Q6). Nothing requires zero retention, no training on customer data, no human review by the provider, a region or jurisdiction that matches the sovereignty promise, or a pinned model version.
  - The default sends free text after placeholder substitution, and placeholder sanitisers miss what they do not recognise: internal hostnames, customer names in URLs, tokens in non-standard formats.
  - Customers cannot turn the hosted model off for diagnostics; they can only choose "maximum privacy".
  - The shared-GPU option does not forbid one customer's context or cache being reused for another customer.
- **Fix:**
  - Add PRIV-8 with the minimum provider terms: no retention beyond the request, no training, a named region or jurisdiction, a contractual audit right, and a pinned model version.
  - Each customer chooses the data level (off, time and type only, or sanitised fields) with a documented default, and that choice is recorded in the coverage report.
  - Free text is sent only from allowlisted fields.
  - No context, prompt cache or KV cache is shared between customers on hosted or shared GPUs.

---

## Medium

### SEC-R2-14: The PRIV-4 outbound check cannot be tested as written
- **Where:** PRIV-4, "a further test runs on every whole line about to leave ... to make sure nothing harmful, such as injected instructions, goes out"
- **Problem:** "Harmful" is undefined. There is no detection target, and nothing says what happens on a match (block, redact or alert). The test checks for injected instructions, not secrets, so secret detection rests on the sanitiser alone.
- **Fix:** Specify what PRIV-4 checks: secret patterns, high-entropy strings, placeholder leaks and instruction-like content. Set the action on a match to block and record. Run it in the egress gateway (SEC-R2-06). Set a measurable target against a labelled test corpus, and report misses under PRIV-7.

### SEC-R2-15: The allowed-field lists belong only to Orvex
- **Where:** PRIV-3 "Orvex defines and owns the list of allowed fields, recipients and destinations"
- **Problem:** Customers cannot see or narrow what leaves, and Orvex can widen a list without the customer knowing. That undermines PRIV-7 ("proving privacy").
- **Fix:** The lists are versioned, signed and published to each customer. Customers can narrow them. Any widening is notified in advance and needs the customer's acceptance for that customer's clusters.

### SEC-R2-16: Fleet-learning integrity and poisoning
- **Where:** FR-37 to FR-40; addendum ("sanitised evidence → a person diagnoses → ... shadow run across the fleet")
- **Problem:**
  - Only new or changed **repair** entries need two reviewers. Detection rules and incident-catalogue entries need one, yet rules decide matching, and matching triggers ticked repairs.
  - Sanitised evidence going to the learning pipeline is a channel not listed in PRIV-2.
  - An attacker running apps on several clusters can produce coordinated crafted evidence that shapes a "lesson".
  - A "shadow run across the fleet" executes new logic in every cluster before release.
- **Fix:**
  - Two reviewers for any rule or entry that can lead to a repair, including any change to a risk level.
  - Add the learning pipeline to the PRIV-2 channel list.
  - Lessons cite the number of distinct customers behind them, and evidence from a single tenant cannot alone produce a fleet rule.
  - Shadow runs are read-only and signed like releases.

### SEC-R2-17: The audit record can be polluted and may hold raw evidence outside the cluster
- **Where:** FR-33, FR-34, FR-35, SEC-2 (Audit records), SM-4
- **Text:** "the agent can add to it but cannot change or delete entries"; FR-34 records "the problem and its evidence".
- **Problem:**
  - A compromised agent can **append** false entries, for example "approved by Samira", or flood the record.
  - SM-4's cross-check with Kubernetes audit logs fails if the agent can change the audit policy.
  - Where the "independently protected audit service" runs is unspecified. If it is central, the evidence in FR-34 (log excerpts) leaves the cluster.
  - Reads by Orvex **people** (support, engineers, Fleet operators) are not recorded where the customer can see them.
- **Fix:**
  - Authorisation entries are written by the executor and verified against the SEC-9 signatures, not taken from the agent.
  - The agent has no rights over the Kubernetes audit policy.
  - The audit service location follows PRIV-1, with evidence stored by reference in the cluster.
  - FR-33 covers Orvex staff access to customer data and clusters.

### SEC-R2-18: An attacker can trigger the last-resort condition
- **Where:** FR-24, FR-23, FR-30
- **Text:** "applies only when nobody answers and failure is predicted within about 30 minutes".
- **Problem:** Both conditions can be engineered. The prediction comes from signals a compromised app controls, and "nobody answers" is likely at 3 AM. This turns a ticked risky repair into an outage on demand, repeated within the FR-30 rate limits.
- **Fix:** The last-resort prediction must come from signals in at least two trust domains (SEC-R2-04). The condition fires at most once per target per window, then needs a human. FR-30 limits count last-resort runs separately, and each run is reported at once.

### SEC-R2-19: Approvals have no expiry
- **Where:** FR-22, "There are no timers to manage"; FR-31
- **Problem:** An approval nobody has used stays open indefinitely. If its preconditions happen to hold days later, possibly arranged by an attacker, it runs. FR-31 can also resume a repair on an approval given before the crash, against a changed state.
- **Fix:** Every approval has an expiry (proposed: minutes, set per risk level) and is void once the evidence is superseded. An approval used before a crash is not reused if the re-checked evidence differs from the evidence shown.

### SEC-R2-20: The scope of advance permission is undefined
- **Where:** Glossary "Advance permission", FR-21
- **Problem:** It is unclear whether a tick on "restart the only replica" applies to every service and cluster, including a database. A customer who meant to allow it for a stateless frontend has authorised it everywhere.
- **Fix:** Each tick names its scope (clusters, namespaces or services, with excluded critical services). The executor enforces the scope.

### SEC-R2-21: Disk cleanup can be turned into a prohibited deletion
- **Where:** Glossary "Disk cleanup", 3.2
- **Problem:** A tenant pod writes a symbolic link in an allowlisted cache or temporary path that points at database files. A cleanup that follows the link deletes customer data, which is a prohibited action.
- **Fix:** Cleanup never follows symbolic links or crosses mount points, and checks ownership before deleting. Allowlisted paths are on Nightshift-owned or runtime-owned volumes only. Cleanup runs in the executor with per-run byte and file limits.

### SEC-R2-22: Supply chain beyond signatures
- **Where:** SEC-5, SEC-6
- **Problem:**
  - No software bill of materials (SBOM) or build provenance is required for open-source dependencies.
  - The installation trust root and how the verifier itself is protected are not stated.
  - There is no revocation.
  - The hosted model cannot be signed, so its behaviour can change silently.
  - SEC-6 switch-off messages are not required to be authenticated, so a forged switch-off disables repairs across the fleet.
- **Fix:**
  - Require an SBOM and signed build provenance per release.
  - Pin the trust root at installation, with customer-visible key rotation and a signed revocation list.
  - Pin hosted model versions and re-run the SEC-1 injection corpus on each model change.
  - SEC-6 commands are signed by the release keys and logged in the customer's record.

### SEC-R2-23: Fleet multi-tenant isolation is not testable
- **Where:** FR-48 "one customer's information is never visible to another customer (AI suggestion, accepted by Amine)"; FR-15 grouped views; FR-32 "The affected clusters' reports are preserved"
- **Problem:**
  - There is no isolation mechanism or test.
  - Orvex's grouped views of 100 clusters mix customers.
  - The preserved cluster reports in FR-32 may be gathered centrally, which would bring raw data to Fleet.
- **Fix:**
  - Each cluster gets its own identity tied to its tenant, and Fleet APIs enforce authorisation per tenant.
  - Run automated cross-tenant access tests in CI and an annual penetration test.
  - Grouped views show only PRIV-3 fields.
  - FR-32 reports are preserved in each cluster and referenced from Fleet, not copied to it.

### SEC-R2-24: Rights inventories are missing, so SEC-3 and SEC-4 cannot be tested
- **Where:** SEC-3 "kept securely", SEC-4 "holds only the rights it needs"
- **Fix:** Require a published rights inventory per component: agent, executor, hardware component, management agent, Fleet, test environment. It lists each Kubernetes verb and resource, BMC role and network destination. An automated test fails the release if the deployed rights go beyond the inventory.

---

## Low

### SEC-R2-25: Phone-call impersonation
- **Where:** FR-13, FR-14
- **Problem:** Attackers who call customers pretending to be Nightshift can push them towards a fake portal.
- **Fix:** Nightshift calls and messages never ask for credentials or approval by voice. Customers are told this during onboarding. The call content counts as a PRIV-2 channel to the telephony provider.

### SEC-R2-26: Liveness is not integrity
- **Where:** FR-6
- **Problem:** A compromised agent can keep sending "I'm alive" while its monitoring is disabled.
- **Fix:** Heartbeats include a signed attestation of the release version and of whether the executor and egress gateway are healthy.

### SEC-R2-27: The reviewer of the recovery plan, and Orvex's advance permission, are unspecified
- **Where:** FR-21 (dangerous: "recovery plan reviewed"), FR-24 ("Orvex's permission given in advance")
- **Fix:** Name the reviewing role, which must differ from the approver. Orvex's advance permission is signed per repair and per customer, like an approval (SEC-9).

### SEC-R2-28: Where the placeholder mapping lives
- **Where:** PRIV-2
- **Fix:** The table mapping placeholders back to real values never leaves the cluster. Model responses are filled back in only inside the cluster.

### SEC-R2-29: Coordinator marks can block all repairs
- **Where:** FR-29, FR-31
- **Problem:** A compromised agent can mark every target "unavailable", which quietly blocks all repairs.
- **Fix:** Only the executor sets marks. A mark longer than a set duration raises an alert.

---

## Requirement-level changes, in brief
1. Add **SEC-8** (separate executor, read-only agent) and **SEC-9** (authorisations signed by the person and verified in the cluster; Fleet commands limited to a closed list). These fix both critical findings and support most of the high ones.
2. Widen SEC-1 to all untrusted inputs. Define independent signals by trust domain. Render approval requests only from structured, signed data.
3. Define approver roles, MFA and step-up authentication, separation of duties, and approval per cluster for fleet events.
4. Add an exfiltration row to SEC-2 (egress gateway outside the agent) and a management-agent compromise case.
5. Fix code-fix distribution (consent before fleet-wide reuse; customer-specific entries out of the shared release), deployment (pull request with pinned hash), test-environment isolation, and engineer access as a listed channel.
6. FR-47: version floor and revocation, update type in the signed metadata, enforcement components never "routine", signing keys in an HSM with threshold signing.
7. Add PRIV-8 with the hosted-model provider's minimum terms and a data level chosen by each customer.
8. Make PRIV-3, PRIV-4, FR-48, SEC-3 and SEC-4 testable with published inventories, field lists and test corpora.
