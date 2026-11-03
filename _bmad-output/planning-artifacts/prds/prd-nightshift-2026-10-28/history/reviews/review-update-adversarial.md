# Adversarial review: PRD update of 2026-11-02

Reviewer stance: hostile SRE, security and product reviewer. Scope: the diff from `prd-final-2026-10-31.md` to `prd.md`, how the changed parts interact with the rest of the PRD, and `addendum.md`. Context: `danny-qa.md`, Exchange 5. Source tags and acceptable Section 10 deferrals are out of scope.

## Verdict

Not ready to hand in as it stands. The update follows Danny's direction faithfully, but it adds a new source of authority, the agreed management policy, that Orvex alone writes, signs and classifies. The gate that decides whether that authority applies ("does this affect customer production?") is defined three different ways and assigned to no one. A CTO can game it, and misclassify by accident, without SM-4 ever noticing. The update also moves dangerous repairs, the riskiest category, outside every control the PRD built: the separate executor, the ban on running AI-generated commands, the customer's personal approval and the recovery plan. That leaves them less controlled than safe repairs. SEC-8 and SEC-9 still hold in their own text, but the new gates get around them at the edges. The FR-41 tuning bypass is back, through the platform row. PRIV-9 promises "nothing leaves by any channel unless permitted", but its list of channels leaves out security updates, the delivery of approvals, audit records and engineer access. The PRD also never says what still works when a customer switches every channel off. The privacy and consent work, the heartbeat wording and the "AI redaction alone" rule are real improvements. The blocking problems are the classification gate and FR-52.

| Severity | Count |
|---|---|
| Critical | 3 |
| High | 12 |
| Medium | 10 |
| Low | 6 |
| **Total** | **31** |

Previously fixed critical issues: **SEC-8 is partly reopened** (H3: the executor's new pre-run check of whether a repair affects customer production depends on data from the untrusted agent, and SEC-8's list of authorisations was never updated). **SEC-9 is partly reopened** (C2: a policy repair's only authorisation is now Orvex's own signature, and nothing separates that key from Fleet's or the release pipeline's). **The FR-41 tuning bypass is reopened** (H2).

---

## Critical

### C1. "Affects customer production" is the new approval gate, and it is undefined, inconsistent and decided by the party it benefits

- **Where:** FR-21 table and bullets; FR-51 Limits; Glossary "Customer production", "Platform repair", "Quornex"; Section 10 (missing).
- **Text:**
  - Glossary: "anything whose change can affect the customer's live experience or service, data, availability or security, at any layer" and "A change to OMK or Quornex can affect customer production; when it does, the customer's permission applies as for any other change to customer production".
  - FR-21 table: "Only OMK or Quornex (platform repair), without affecting customer production".
  - FR-21: "If the pre-run checks show that a platform repair would affect customer production, it follows the customer-production row".
  - FR-51: "the policy never contains a change that affects customer production".
  - Glossary "Quornex": "It provides databases, queues, storage and application deployment, fully managed by Orvex".
- **Problem:** The PRD uses three different tests: "*can* affect" (Glossary), "*would* affect, as shown by pre-run checks" (FR-21) and "*affects*" (FR-51). Under the Glossary's own test, almost no OMK or Quornex change is free of customer production. Quornex *is* the customer's databases, queues, storage and deployments, and the definition covers "security, at any layer". So the platform row is either empty, which makes FR-51 pointless, or it is filled under the looser "would, per pre-run checks" test. In that case a change that *can* affect production runs without the customer whenever a check written by Orvex says it won't this time. Nothing says who classifies an entry, when, with how many reviewers, against what evidence, or whether the customer can dispute it. Orvex writes the catalogue entry, sets its risk level, decides whether it touches production, puts it in the policy and signs it. Orvex is also the party that saves staff time by classifying it "platform-only". SM-4 compares executions with "approval records and policy decisions", so a misclassified policy run counts as *approved* and SM-4 stays at 0 by construction. The question is not even in Section 10.
- **Failure scenario:** A policy entry "Reset the Quornex namespace's egress NetworkPolicy to the platform default" is tested on a lab cluster, classified safe and platform-only, and approved by one engineer. On a customer who had tightened egress, it reopens outbound paths that go around the PRIV-9 gateway. That affects "security", but the pre-run check only looks at pod health, finds no interruption, and the repair runs without a tick. It is recorded as "in the agreed management policy", so SM-4 shows 0. Second example: "restart the Quornex queue broker's sidecar" counts as platform-only until the broker drops in-flight messages for the customer's checkout.
- **Fix:**
  1. Use one test, "can affect", as a stored property of each catalogue entry. Set it when the entry is reviewed, with the two reviewers FR-39 requires, and default to customer production.
  2. Tie the classification to the expected-interruption field. Any expected interruption other than "No service interruption expected", and any change to data, network policy, RBAC, secrets, storage or the customer's Quornex services, makes the entry customer production.
  3. Let the runtime check only *escalate* an entry to customer production, never downgrade it.
  4. Give the customer a per-entry view and an opt-out from the policy that does not force alert-only mode.
  5. In SM-4, count as unapproved any policy repair whose before-and-after health checks show an impact on the customer.
  6. Add "how platform-only is decided and audited" to Section 10, owned by Orvex, and to the architecture requirements.

### C2. The agreed management policy is an Orvex-only authority: one engineer, one Orvex signature, and consent given through the contract that the PRD says is not a repair checklist

- **Where:** FR-51; Glossary "Customer contract" and "Agreed management policy"; SEC-9; FR-22; FR-39; FR-40 and FR-46.
- **Text:**
  - FR-51: "Orvex authorises the content. An authorised Orvex engineer from the Nightshift team approves each entry after testing. The customer agrees to the policy as part of the managed-service contract and can read it in the portal." and "each new version is signed (SEC-9), recorded and notified to the customer."
  - Glossary: "Customer contract … It is not the checklist of allowed repairs".
  - FR-22: "if a release changes the repair's action, conditions or risk level, the customer must tick it again".
  - FR-39: "A new or changed repair catalogue entry needs two reviewers".
- **Problems:**
  - **The customer's consent covers versions they never saw.** The customer accepts version N when signing the contract. Every later version is only *notified*. A tick, by contrast, must be renewed when the repair changes (FR-22). So the authority with the least customer control has the weakest re-consent rule.
  - **The PRD contradicts itself.** The Glossary says the contract is not a repair checklist; FR-51 turns it into exactly that.
  - **One engineer can add an entry.** Each entry needs one engineer's approval, while FR-39 needs two reviewers for any catalogue change. Moving an existing entry into the policy, which turns "Orvex approval at the time" into "runs automatically everywhere", gets the weaker rule.
  - **SEC-9's protection becomes circular.** SEC-9 exists so that "a compromised portal, Slack integration or Quornex Fleet cannot forge" authorisations. For policy repairs the only authorisation is Orvex's own signature. Nothing requires a key separate from the release key or from what Fleet delivers, and nothing requires several signers.
  - **A policy change can reach the whole fleet at once.** Nothing says a new policy version goes through the staged, health-gated release (FR-40, FR-46).
- **Failure scenario:** An Orvex insider, or an attacker holding the release-signing pipeline (which the addendum lists as an open item, "signing-key custody"), publishes policy v17 with one new entry. Every cluster's executor verifies a valid Orvex signature, and the entry runs automatically on 10,000 clusters with no customer tick and no per-run approval. Customers receive a notification after the fact.
- **Fix:**
  1. Policy entries need the two reviewers of FR-39.
  2. Policy versions ship only inside the signed, staged release (FR-40, FR-46). The policy signing key is separate from Fleet and release keys and needs more than one signer.
  3. New or changed entries take effect only after a notice period, during which the customer can opt out per entry.
  4. Write explicitly that the contract consents to a *process* and a scope, not to future content, and remove the conflict with the "Customer contract" definition.
  5. SEC-9 states which key signs policies and that Fleet cannot deliver policy versions outside a release.

### C3. FR-52 "manual" removes every control from the most dangerous repairs

- **Where:** FR-52; FR-12 routing; FR-21 (deleted text); FR-42 step 4; FR-17; Section 3.2; SEC-1; SEC-8; SM-4.
- **Text:**
  - FR-52: "It explains the problem, gathers the evidence and suggests the steps; a person performs the repair" and "When the person reports the repair done, Nightshift records it".
  - FR-12: "A dangerous repair (manual, FR-52) goes to whoever must perform it, with the evidence and suggested steps".
  - Deleted from FR-21: "Delegation never covers dangerous repairs: the customer always approves those personally" and "plus a recovery plan reviewed before the repair runs".
  - FR-42: "a dangerous code fix is not deployed by Nightshift but left to a person".
- **Problems:**
  - **Approvals are gone.** Before the update, a dangerous repair needed the customer's personal approval (delegation excluded), Orvex technical approval and a reviewed recovery plan. Now FR-21 just says "Manual (FR-52)", and FR-52 sets no approval requirement at all. Who may perform it ("whoever must perform it") is undefined: the customer's non-expert business owner, Orvex support under delegation, or a Nightshift engineer. Nothing says whether the customer must approve an Orvex engineer manually changing their production.
  - **AI suggestions reach production through a person.** "Suggests the steps" does not say the steps come from the catalogue entry. If the AI writes them, a person pasting them at 3 AM is exactly what FR-17 and Section 3.2 forbid ("run commands or scripts the AI generated"). A malicious log line (SEC-1) can then shape the steps.
  - **The person acts outside the executor (SEC-8), with no recovery plan.**
  - **The record depends on the person.** It is kept only "when the person reports the repair done", so SM-4 and SM-3 never see manual changes, including a harmful one.
  - **FR-42 lets a person deploy AI-written code to production outside every Nightshift gate.**
- **Failure scenario:** A NIC or IP change on a live node is classified dangerous. FR-52 routes "suggested steps" to the customer, a small-business owner who is "not a technical expert", or to Orvex support acting under delegation. The steps were rendered from model output that a poisoned log influenced. The person runs them, the node drops off the network, and there is no recovery plan, no customer approval on record and no execution record. SM-3 and SM-4 both report zero.
- **Fix:**
  1. Suggested steps come only from the catalogue entry's reviewed runbook, never from the AI. Show them separately from the AI's wording (SEC-1).
  2. Name who performs dangerous repairs, per platform and layer.
  3. Keep, for manual repairs on customer production: the customer's personal approval (delegation excluded), Orvex technical approval and the reviewed recovery plan.
  4. Record the start of the manual work and the approvals, not only the completion.
  5. Cross-check manual changes against Kubernetes and host audit logs, and count them in SM-3 and SM-4.
  6. For code fixes: a person deploys only through the normal deployment pipeline, with the same approvals.

---

## High

### H1. The line between a repair and an update is a way around FR-47

- **Where:** FR-47 against FR-21 and FR-51.
- **Text:** FR-47: "Updating Orvex's own software (Nightshift, Quornex, OMK) changes customer production, so it follows the customer's permissions too". FR-21: "Only OMK or Quornex (platform repair), without affecting customer production".
- **Problem:** By FR-47, *every* update to OMK or Quornex changes customer production. By FR-21 and FR-51, a *repair* to the same components may not. Pinning an image tag, rolling a component back, changing a config map or replacing a sidecar can be labelled either way. Labelled "repair", it goes into the Orvex-only policy and skips the maintenance policy and its windows. The addendum already lists "who may label an update 'routine'" as unresolved.
- **Failure scenario:** To meet a deadline, Orvex ships a Quornex config change as a catalogue repair ("raise broker memory limit") in the management policy. It runs outside the customer's maintenance window and without the maintenance policy, and it restarts the broker.
- **Fix:** Define the boundary: any change to a component's version, image, configuration or manifest is an update under FR-47, unless it is a catalogue repair whose expected interruption is "none" and which C1's classification puts outside customer production. Explain why FR-47 and FR-21 treat the same components differently, or make them consistent.

### H2. The FR-41 tuning bypass is reopened through the platform row

- **Where:** FR-41; FR-21 platform row; FR-51.
- **Text:** FR-41: "Every tuning action is a repair catalogue entry like any other repair: it has a risk level, follows advance permission and approval (FR-21)" and "it still needs the customer's permissions like any other repair".
- **Problem:** Under the new FR-21, a platform repair that does not affect customer production needs *no* customer permission. Tuning OMK or Quornex settings (Quornex database pool sizes, kubelet eviction thresholds, broker limits) can therefore be classified safe and platform-only, put in the policy, and run with no tick. This is the bypass the 10-31 fix closed. The only thing left between tuning and the customer is C1's undefined classification.
- **Failure scenario:** Tuning entry "lower the kubelet eviction threshold" goes into the policy as platform-only. On a memory-tight customer node it evicts the customer's pods. Nobody was asked.
- **Fix:** FR-41: tuning is always customer production (it changes runtime behaviour), so it can never be in the management policy. Alternatively, let only tuning of components with no customer data plane (for example Nightshift's own collectors) be platform-only, and list them.

### H3. SEC-8: the executor's new pre-run check is fed by the untrusted agent, and SEC-8 was not updated

- **Where:** SEC-8; FR-21 ("pre-run checks"); FR-51; SEC-1.
- **Text:** SEC-8: "runs a repair only after it has checked the authorisation (tick or approval), the safety preconditions and the risk-level conditions itself."
- **Problem:**
  - **The list of authorisations is out of date.** SEC-8 still lists only "tick or approval". It does not mention the management policy, the classification of what a repair changes, alert-only mode or the permitted channels.
  - **The classification relies on data an attacker can shape.** The pre-run check that *decides who must approve* ("would affect customer production") needs observations such as traffic, dependencies and which pods sit behind a component. Those come from the read-only agent, which reads untrusted data. SEC-1 makes the agent's output untrusted, yet the classification now rests on it.
  - **Policy repairs can touch enforcement.** Nothing stops a policy repair from changing the executor, the gateway, the audit forwarder or the egress configuration, all of which are "OMK or Quornex components" in practice.
- **Failure scenario:** A compromised agent reports "no customer pods depend on component X". The executor treats a policy repair on X as platform-only and runs it with no customer approval. Or a policy entry "restart the Nightshift gateway with default config" resets a customer's channel restrictions.
- **Fix:**
  1. Extend SEC-8: the executor verifies policy membership (signed), the entry's stored classification, the mode and the channel permissions.
  2. The executor computes "would affect customer production" only from its own independent sources (the Kubernetes API, its own probes), never from the agent.
  3. Ban policy entries that touch the executor, gateway, audit path, RBAC, network policy or channel settings. Those are always customer production.

### H4. PRIV-9's channel list is incomplete, so "nothing leaves unless permitted" cannot be delivered

- **Where:** PRIV-9; SEC-8 gateway; FR-47; SEC-2; FR-12 and FR-36; FR-44; PRIV-2; SEC-5.
- **Text:** PRIV-9: "The channels are: external AI (PRIV-8), the Quornex Fleet heartbeat (FR-6), Fleet reports with sanitised information (FR-32), notifications (Slack, phone) and the portal." FR-47: "Security updates are required by the customer contract".
- **Problem:** Flows that leave, or that need an outbound connection, but are not on the list:
  - fetching releases, catalogue and policy versions (SEC-5, FR-40), including the *mandatory* security updates;
  - delivering signed approvals and ticks to the executor;
  - the "independently protected audit service" (SEC-2: "Missing or interrupted reporting must be detectable");
  - the "signal to Orvex whenever the customer confirms something" (FR-12, FR-36);
  - the Orvex engineer's access to the code-fix test environment (FR-44; the addendum calls it "engineer access as a channel");
  - code sent to a hosted model (FR-43);
  - the morning summary and dashboards (listed in PRIV-2 but not in PRIV-9);
  - the telephony provider for calls;
  - the outside audit (PRIV-7).

  Either these are hidden exceptions, which PRIV-9's "No channel … is silently exempt" forbids, or a customer who disables everything gets no security updates, contradicting FR-47's contractual requirement.
- **Failure scenario:** A sovereign customer sets every channel off. The CTO asks: "How does the CVE fix reach them? How do you prove they got it? Where does their audit log go?" The PRD has no answer.
- **Fix:** List every outbound and pull channel, including update and catalogue pulls, approval sync, audit, the confirmation signal, engineer access, telephony and the morning summary. For each, state whether the customer can switch it off and what breaks. Name the minimum set the contract requires (for example, pulling signed updates), and state that requirement openly.

### H5. With channels off, the approval model has holes that read as bypasses

- **Where:** PRIV-9 "Without notifications as well"; FR-14; FR-13; FR-21 risky ticked; FR-24; FR-28; FR-31; FR-52; FR-4; FR-15.
- **Text:** PRIV-9: "Without notifications as well: no alert or approval request reaches anyone outside the cluster; only repairs authorised in advance run; problems are visible only on an in-cluster dashboard."
- **Problems:**
  - **"Authorised in advance" is ambiguous, and one reading is a bypass.** A ticked *risky* repair is "authorised in advance" by the customer, but FR-21 still needs Orvex technical approval *each time*. A literal implementer runs ticked risky repairs without Orvex because the channel is off. The PRD must say which reading is right.
  - **Approval exists only in the portal (FR-14), and the portal is a channel the customer can switch off.** No in-cluster place to approve is defined, so with the portal off no repair needing approval can ever run. It is also unclear where SEC-7's administrators change settings, or turn the channels back on.
  - **Several flows reach a dead end.** FR-13 phone calls for critical problems, FR-28 "calls a person", FR-31 "asks a person" and FR-52 "goes to whoever must perform it" all stop silently.
  - **No one watches a dead Nightshift.** FR-4's monitoring failure case is visible only in the cluster, so if Nightshift dies nothing outside notices.
  - **SM-7 does not account for this.** Orvex "operates OMK and Quornex", and its 99.9% target ignores customers who blind it.
- **Failure scenario:** Checkout's database is failing at 3 AM. The customer has turned notifications off. Nightshift cannot call (FR-13), the risky ticked rollback waits forever for an Orvex approval nobody can see, or, under the bypass reading, runs without one. The in-cluster dashboard is served by the Nightshift agent that just crashed.
- **Fix:**
  1. State that "authorised in advance" means a repair needing no approval *at the time*, so risky ticked repairs do not run.
  2. Define an in-cluster approval and settings surface, or state that approval needs the portal channel.
  3. Make the onboarding screen for switching channels off list these consequences (no calls, no Orvex approvals, no outside watchdog) and require the customer to acknowledge them, as FR-7 does for limited visibility.
  4. Exclude such clusters from SM-7, or record the reduced service level in the contract.

### H6. Clusters Fleet cannot see will be treated as healthy by rollout and correlation

- **Where:** FR-6; PRIV-9 "Without Fleet reports"; FR-46; FR-32; FR-47.
- **Text:** FR-46: "A release reaches a small group of clusters first, and the rest only once those are healthy". FR-6: "Fleet cannot detect from outside that the agent is dead, and cannot tell a healthy disconnected cluster from a failed one".
- **Problem:** Staged rollout and automatic stop depend on health signals that customers can now switch off. The PRD does not say how a canary in "status unknown" counts. If unknown counts as healthy, a bad release goes ahead; if it counts as unhealthy, one customer can stall the fleet. A cluster without Fleet reports that receives a bad update is invisible to FR-32 correlation. Without the heartbeat, nobody knows it is broken, and FR-47's emergency rollback is never triggered for it.
- **Failure scenario:** v2.4 bricks the Nightshift agent on clusters with a certain NIC driver. Three of the five canaries do not permit reports. Fleet sees two healthy canaries and three "status unknown", and goes ahead. 300 clusters break, and Fleet cannot see 40 of them.
- **Fix:** In FR-46 and FR-32, clusters in "status unknown" never count as canaries or as healthy evidence. They receive a release only after it has proven itself on visible clusters, and the in-cluster executor rolls back by itself when its local health checks fail after an update. State this for the architecture.

### H7. Alert-only mode against FR-47: "no hidden exception" sits next to an exception, and the exception has no exit

- **Where:** Glossary "Alert-only mode"; FR-47; FR-32; FR-51; FR-21 platform row.
- **Text:** Alert-only: "There is no hidden exception. Kubernetes' own controllers and separately authorised maintenance (FR-47) are not Nightshift changes and are outside this mode." FR-47: "Otherwise Nightshift asks for approval and escalates."
- **Problems:**
  - **Updates still arrive, but rollbacks cannot.** An alert-only customer still receives Orvex updates (maintenance and contract-mandated security updates), so their platform changes. If an update is bad, FR-47's fallback, "Nightshift asks for approval", is suppressed because alert-only "never … asks for approval to execute". They can receive a broken update but cannot be offered its rollback.
  - **The executor of updates is unnamed.** The PRD does not say who executes FR-47 updates. If it is the Nightshift executor, they *are* Nightshift changes.
  - **Orvex cannot operate its own platform in alert-only clusters.** No policy repairs and no risky platform repairs, although Danny says "We operate OMK and Quornex". Fixes then happen by hand, outside Nightshift's record.
- **Failure scenario:** An alert-only customer gets v2.4 in their maintenance window. Checkout fails. Fleet stops the rollout, but the rollback for this customer can neither run (no rollback policy) nor be requested (alert-only), so an Orvex engineer logs in and rolls back by hand, unrecorded.
- **Fix:**
  1. Name the component that executes FR-47 changes.
  2. Let alert-only mode still allow approval requests for rolling back an Orvex update the customer received.
  3. State who repairs OMK and Quornex on alert-only clusters, and that manual changes are recorded (C3). Show the effect on SM-7 and cost.
  4. Drop "no hidden exception", or list the exceptions as exceptions.

### H8. FR-50 Reject contradicts itself and can be worn down by re-asking

- **Where:** FR-50; FR-22; FR-24; FR-26 and FR-27.
- **Text:** "Nightshift does not resubmit the same request automatically, and does not substitute another repair to get around the rejection. Rejecting one request does not turn off other automatic repairs."
- **Problems:**
  - **The two sentences collide.** When the "other automatic repair" is a ticked or last-resort repair that fixes the same problem, sentence 1 forbids it and sentence 2 allows it.
  - **The last-resort condition can run what was just rejected.** FR-24 fires "when nobody answers". If the customer rejected but Orvex never answered, or the reverse, does it count as "nobody answered", and can last-resort then run the rejected repair?
  - **The same request returns under a new name.** FR-22 starts a "new approval" if "the problem happens again", and FR-22 expiry also re-asks. A flapping problem re-raises the rejected repair as a new request every time, until a tired approver clicks yes.
  - **Rejection has no duration and no scope** (this occurrence, this incident, this target).
- **Failure scenario:** Orvex rejects "restart the only replica" because the customer's batch job is running. Memory crosses the 30-minute line, and the customer had ticked last-resort for that repair. The same restart runs under FR-24 two minutes after a person explicitly said no.
- **Fix:** A rejection blocks that repair *and any repair aimed at the same target for the same incident*, including ticked, policy and last-resort runs, until the incident closes or the person who rejected lifts it. Recurrences within N hours inherit the rejection. Define its scope and duration.

### H9. Approval expiry and "materially changed" loosen how an approval is tied to what was shown

- **Where:** FR-22; Glossary "Approval"; FR-21 when two approvals are needed; Section 10 item 18.
- **Text:** FR-22: "An approval that is not used in time expires, and Nightshift asks again" and "If the repair or its conditions have materially changed, it does not run and Nightshift asks again". Glossary: "tied to the exact repair, target, catalogue version and evidence shown".
- **Problems:**
  - **The binding was loosened.** The old rule was "If something has changed, it does not run". The new one tolerates *non-material* change in the evidence, which contradicts "exact … evidence shown". Who decides what is material, and how? If the AI decides, a model judgement now governs whether an approval is still valid.
  - **Two approvals may never be valid together.** The customer approves at 02:10, Orvex at 02:55, and the customer's approval expired at 02:40. The PRD does not say whether expiry runs from the first or the last approval.
  - **Re-asking was never thought through.** "Asks again" means each expiry pages people again: alert fatigue at 3 AM.
- **Failure scenario:** The approval screen showed "memory 92%, 1 replica". The executor runs at 97%, judging it "not material". The restart now lands during peak traffic, which the approver would have refused.
- **Fix:**
  1. Keep the exact binding. Materiality is a rule-based threshold stated in each catalogue entry and checked by the executor, never by the AI.
  2. Expiry runs from the *first* approval, with all approvals for a repair valid together.
  3. Cap how often a request is re-asked.
  4. Section 10 item 18 must at least set a maximum (for example, never longer than the entry's time to impact).

### H10. External AI is off by default while v1 is built around the hosted model, and the market is customers who buy sovereignty

- **Where:** PRIV-8; Section 7 "Focus for the first version: the hosted model"; Section 7 "Without external AI"; FR-11; SM-5; Section 11 cost model; Vision.
- **Text:** PRIV-8: "Consent is offered during onboarding, with nothing preselected." Section 7: "Focus for the first version: the hosted model".
- **Problems:**
  - **The fallback carries the product, not the hosted model.** Orvex sells "affordable sovereign cloud". Those buyers are the most likely to decline an opt-in with nothing preselected, and the cheaper small customers are the least likely to have a GPU. So the template mode carries most of the fleet, while the hosted model gets the v1 focus and the cost case.
  - **Templates cannot meet FR-11 for problems outside the catalogues.** FR-11 asks for evidence-based, plain-language explanations that state what is known and what is not. Templates can do that only for catalogued problems, but FR-19 promises explanations for problems in neither catalogue.
  - **SM-5 is not split by mode.** The cost model has no assumed consent rate.
- **Failure scenario:** The CTO asks what share of customers consents. Answer: unknown. The hosted-focused cost model assumes 100%. If 30% consent, the cheapest-per-cluster story is wrong, and 70% of clusters get template explanations nobody has designed or measured.
- **Fix:**
  1. Add the assumed consent rate to the cost model, with sensitivity at 20%, 50% and 80%.
  2. Split SM-5 and SM-6 by AI mode.
  3. Make templates for every catalogued problem, plus a defined "unknown problem" template, part of the failure-catalogue deliverable.
  4. Either justify the hosted focus under a low consent rate, or make the in-cluster and template modes co-equal for v1.

### H11. PRIV-8 covers only what Nightshift sends, not what Orvex does with Fleet data

- **Where:** PRIV-8; FR-32; FR-37 to FR-40; addendum "Fleet learning pipeline".
- **Text:** PRIV-8: "Nightshift sends nothing to external AI (Glossary) unless the customer has explicitly consented".
- **Problem:** A customer who declines external AI but permits Fleet reports sends sanitised problem data to Quornex Fleet. Nothing stops Orvex's central tooling (correlation, fleet learning, the engineers' assistants, writing the summaries for the consolidated alert) from passing those reports to a hosted model. The consent is then empty in practice. Fleet learning (FR-37) is exactly where that will happen.
- **Failure scenario:** For the 300-cluster incident, the Fleet alert summary is written by a hosted LLM from every affected cluster's reports, including those of customers who said no to external AI.
- **Fix:** PRIV-8 applies to the data wherever it goes. Data from a cluster without consent is tagged, and no Orvex system sends it to external AI. It is excluded from AI-assisted fleet learning, or aggregated before any AI sees it. Test this like PRIV-7.

### H12. Staffing and cost were not updated for manual dangerous repairs, alert-only platform work or non-consenting customers

- **Where:** SM-8; SM-9; COST-1 and COST-4; Section 11; FR-52; FR-21 platform row.
- **Text:** SM-8: "Reason: most problems do not need a risky or dangerous repair, and safe ticked repairs run on their own (Amine)."
- **Problem:** The update adds human work the arithmetic ignores:
  - every dangerous repair is now hands-on: NIC and IP work, often hours, possibly on site;
  - every safe platform repair not in the policy needs Orvex approval at the time;
  - every alert-only cluster's platform repairs are manual;
  - clusters with no heartbeat or Fleet reports need manual triage when the customer calls.

  The "20 minutes each" in SM-8 assumes clicking approve, not performing a repair. Vision #4, "whether it really replaces engineers", is the business case, and it now rests on numbers the update made out of date.
- **Failure scenario:** Asked "who performs manual dangerous repairs across 10,000 clusters at 3 AM, and are they among your 15 engineers?", the PRD has no answer.
- **Fix:** Add to the cost model and SM-8:
  - the share of dangerous repairs and the hours each takes;
  - who performs them (Orvex or the customer, and who pays);
  - Orvex approvals of safe platform repairs outside the policy;
  - the share of alert-only clusters;
  - consent and GPU mix (H10).

  Give SM-9 separate targets for approvals and manual repairs.

---

## Medium

### M1. Default ticks are now treated as "the customer's approval"

- **Where:** Glossary "Approval-enabled mode", "Advance permission"; FR-21.
- **Text:** "A new customer starts in approval-enabled mode with safe repairs ticked by default; the customer can untick any of them" and "A tick counts as the customer's approval only for the specific tested action and conditions it covers".
- **Problem:** Exchange 5 makes customer approval mandatory for anything affecting customer production, and the PRD now counts a tick as that approval. A tick the customer never made is not an approval. External AI gets "nothing preselected", but changes to production arrive pre-ticked. The PRD also never says whether *new* safe catalogue entries arrive pre-ticked for existing customers. If they do, that is another Orvex-granted approval.
- **Fix:** Either require the customer to confirm the default checklist at onboarding (one click, but an act), or state that default ticks are Orvex-granted and not customer approval. Stop new entries from arriving pre-ticked for existing customers.

### M2. FR-47 rollback policy against FR-21: is Orvex approval needed?

- **Where:** FR-47; FR-21 risky ticked; UJ-5; FR-32 table.
- **Text:** FR-47: "Emergency rollback runs without fresh approval only if the customer has explicitly authorised that rollback policy in advance and its safety conditions pass." FR-21: "Ticked: Orvex technical approval each time it is about to run".
- **Problem:** A risky rollback that affects customer production, under a customer-authorised policy, either runs with no Orvex approval (FR-47) or needs Josh each time (FR-21 and UJ-5's "Josh's approval is the authorised Orvex engineer's approval that a risky platform change needs"). These conflict.
- **Fix:** State whether the rollback policy counts as a tick (then Orvex approval each time) or as a separate pre-authorisation that includes Orvex's advance approval, as FR-24 does for last-resort.

### M3. One engineer approves a platform change across 300 clusters

- **Where:** UJ-5; FR-21 platform risky; FR-32.
- **Text:** "Josh's approval is the authorised Orvex engineer's approval that a risky platform change needs".
- **Problem:** A single click by one engineer at 3 AM applies across the fleet. The addendum asks for "two different people where two approvals are needed", but for platform-only risky repairs only one approval is needed. The blast radius is the whole fleet.
- **Fix:** Above a number of clusters (for example 10), a risky platform action needs a second Orvex engineer, or runs in stages with automatic stop.

### M4. The portal is the only approval surface: who signs, and Danny's Slack decision changed without asking him

- **Where:** Glossary "Approval"; FR-14; SEC-9.
- **Text:** "a yes given by an authenticated person at the time, for one repair, in the Quornex portal"; SEC-9: "so a compromised portal, Slack integration or Quornex Fleet cannot forge them".
- **Problem:** With the portal as the only surface, SEC-9 holds only if the signature is made with a credential the approver holds (WebAuthn or similar), not by the portal's backend. The PRD does not say. Also, Exchange 1 had Danny explicitly allow approval in Slack, and the update narrows that on the strength of the UX work without telling him. Expect the question "why did you remove what I asked for?".
- **Fix:** SEC-9: the approval is signed client-side with the approver's own key, and the portal cannot produce one. Give one line of rationale for "Slack notifies only" (identity mapping, phishing) and add it to Danny's list.

### M5. "A GPU shared across clusters" catches the customer's own control-cluster GPU

- **Where:** PRIV-8; Glossary "External AI"; Section 7; FR-43.
- **Text:** "A GPU shared across clusters counts as external AI and needs the same consent".
- **Problems:**
  - **The customer's own shared GPU counts as external.** A customer with a control cluster and one GPU shared across *their own* clusters must give external-AI consent (and with PRIV-1 it may be forbidden entirely), or buy a GPU per cluster. The cost model does not show this.
  - **The two code-fix permissions may conflict.** It is unclear whether FR-43's code consent requires PRIV-8 consent, or whether a customer can grant code-to-hosted-model while refusing external AI for diagnostics.
- **Fix:** Distinguish a GPU shared within one customer from one shared across customers, and decide the first case explicitly against PRIV-1. State that code consent requires PRIV-8 consent, or explain why not.

### M6. Zero retention and the consent's scope cannot be verified as written

- **Where:** PRIV-8; Section 7 "trusted hosted model"; addendum consent wording.
- **Text:** "It is asked again only if the agreed use changes." Addendum wording: "The provider won't keep it after processing."
- **Problems:**
  - **The consent screen promises something Orvex cannot prove.** It states as fact that the provider keeps nothing. Orvex cannot verify that, and many providers keep data for abuse monitoring unless a separate zero-retention agreement applies. PRIV-7 can prove what *left*, not what the provider kept.
  - **Orvex alone decides when the use has changed.** Changing provider, region or model version is not stated to trigger re-consent.
  - **Withdrawal mid-incident is undefined.** Nothing says what happens to requests in flight, or how Nightshift switches to the local or template mode.
- **Fix:** Reword to "contractually required not to keep it". List what triggers re-consent: provider, region, model family, data fields. Define the switch on withdrawal, including that requests already queued are cancelled.

### M7. The in-cluster dashboard and the channel-off states contradict each other

- **Where:** FR-15; PRIV-9; SEC-7.
- **Text:** FR-15: "Each cluster has its own dashboard, reached through the Quornex portal" and "If the customer permits no outbound channel, its problems are visible only on an in-cluster dashboard (PRIV-9)."
- **Problem:** PRIV-9 triggers the "in-cluster only" state when notifications (and the heartbeat) are off. FR-15 triggers it when *no* channel is permitted. With the portal on and notifications off, PRIV-9 says "no … approval request reaches anyone outside the cluster", but the portal would show it. The in-cluster dashboard, its authentication, whether it runs when Nightshift is down, and where SEC-7 administrators sign in are all undefined.
- **Fix:** Make a table of channel combinations and their outcomes: what is visible where, and where approvals and settings happen. Define the in-cluster dashboard and its identity source for the UX and the architecture.

### M8. SM-4 cannot be measured on part of the fleet and does not see misclassified repairs

- **Where:** SM-4; FR-34; PRIV-9.
- **Text:** "cross-checked against independent sources such as Kubernetes audit logs, not only Nightshift's own records".
- **Problem:** For clusters with no outbound channels or no reports, Orvex cannot collect the cross-check. Policy runs count as "policy decisions" (C1), and manual repairs (C3) are not in the execution records. So a fleet-wide "0" is partly unmeasured and partly true by construction.
- **Fix:** Report SM-4 with its denominator (clusters measured). Measure it locally on blind clusters for the customer to inspect. Add to the count: policy runs that affected the customer, and manual changes found in the audit logs.

### M9. No way out when approvers disagree

- **Where:** FR-50; FR-21 provisional bullet; UJ-2.
- **Text:** FR-50: "notifies the other approvers concerned"; FR-21: "Requiring Orvex technical approval as well as the customer's for risky repairs to the customer's own app … is our provisional design".
- **Problem:** Under the provisional design, an Orvex engineer's rejection blocks the customer's own risky change to their own app at 3 AM, while checkout fails, with no override and no escalation. Under a sovereignty pitch, a vendor veto over the customer's app is a hard sell, and Danny has not confirmed it (item 21).
- **Fix:** Define how disagreement is resolved. For example, on the customer's own app the customer may override Orvex's rejection after an explicit acknowledgement of the risk, with the override recorded. Or escalate to a second Orvex engineer within a set time.

### M10. "Platform repair" leaves out Nightshift itself

- **Where:** Glossary "Platform repair"; FR-47; FR-51.
- **Text:** "Platform repair: a repair to OMK or Quornex components".
- **Problem:** FR-47 lists Nightshift as Orvex software, but the platform-repair definition does not. Repairs to Nightshift itself (restarting the agent, executor or gateway, clearing its queues) fall into neither row, and they are the components that enforce everything else (H3).
- **Fix:** Classify Nightshift self-repairs explicitly. Any repair touching the executor, gateway, audit path or settings store needs customer-level authorisation, or is limited to a fixed restart with no change to configuration.

---

## Low

### L1. FR-42's numbered list is broken
- **Where:** FR-42.
- **Text:** "The testing and the engineer's review of the patch (steps 2 and 3; FR-44) check the code itself." This sits between steps 5 and 6.
- **Problem:** The inserted paragraph splits the ordered list, so "6." starts a new list and Markdown will render it out of order.
- **Fix:** Move the paragraph below step 6.

### L2. FR-12 says Orvex is never alerted for safe repairs, but some safe repairs need Orvex
- **Where:** FR-12; FR-21 platform row.
- **Text:** "They are not called or alerted for problems handled by safe repairs".
- **Problem:** A safe platform repair outside the policy needs Orvex technical approval, so the team *is* alerted.
- **Fix:** Add "except safe platform repairs outside the agreed management policy".

### L3. FR-27 ignores FR-52
- **Where:** FR-27.
- **Text:** "Nightshift moves to the next repair only if that repair is safe; otherwise it asks for Orvex technical approval from the Nightshift team".
- **Problem:** If the next repair is dangerous, it is manual (FR-52), not an Orvex approval.
- **Fix:** Add "or, if it is dangerous, marks it manual (FR-52)".

### L4. A stale possible feature in FR-23
- **Where:** FR-23.
- **Text:** "[Possible feature, Amine] For dangerous cases, Nightshift calls a member of the Orvex Nightshift team."
- **Problem:** Dangerous repairs are now manual, and FR-12 routes them to "whoever must perform it". The two overlap with different targets.
- **Fix:** Fold it into FR-52 routing or delete it.

### L5. FR-34 has no outcome for manual repairs
- **Where:** FR-34.
- **Text:** "The outcome is one of: worked; did not work and undone; failed; blocked; cancelled; recovery failed; harmful (Glossary)."
- **Problem:** There is no "manual repair needed", "performed manually" or "reported done, not yet verified".
- **Fix:** Add the manual states, consistent with the addendum's UX statuses.

### L6. The Glossary's "Customer production" lists too few forms of permission
- **Where:** Glossary "Customer production".
- **Text:** "needs the customer's advance permission (a tick in the settings checklist) or the customer's approval per action".
- **Problem:** It leaves out the maintenance and rollback policies (FR-47) and the last-resort condition (FR-24), which also authorise changes to customer production.
- **Fix:** List all the customer-side forms of authorisation, or point to FR-21, FR-24 and FR-47.
