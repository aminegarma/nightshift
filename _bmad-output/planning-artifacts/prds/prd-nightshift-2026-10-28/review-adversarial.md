# Adversarial review: Nightshift PRD

Reviewed: `prd.md` (updated 2026-10-29/30) and `addendum.md`. Review date: 2026-10-30.
Scope: contradictions, untestable requirements, authorisation loopholes, ignored failure modes, claims resting on estimates. Style and prose are out of scope. Source tags are treated as deliberate.

**Verdict:** the approval model looks strict per repair but has no protection at the level of the whole system. Ticks are not tied to a catalogue version. The last-resort condition removes the human check exactly when stakes peak. Individually "safe" repairs can add up to an outage. Orvex's own fleet actions (releases, Fleet rollbacks, batch approval) sit entirely outside the approval model that SM-4 claims to measure.

## Counts

| Severity | Count |
|---|---|
| Critical | 4 |
| High | 13 |
| Medium | 17 |
| Low | 6 |
| **Total** | **40** |

---

## Critical

### C1. A tick survives any change to the repair it approved, and the release pipeline that changes repairs is outside the threat model
- **Where:** FR-21 "A ticked repair stays permitted until the customer unticks it"; Glossary *Risk level* "Orvex sets each repair's risk level ... customers cannot change it"; FR-38 new entries "distributed through a controlled release"; FR-44; SEC-2 (covers only "the Nightshift agent in one cluster").
- **Problem:** the customer ticks a catalogue entry, but nothing ties the tick to a version of that entry: its action, preconditions, scope, risk level or verification. Every release can change all of these under the same name, and the tick carries over.
- **Failure scenarios:**
  1. Release N+1 widens "disk cleanup" to include a new cache directory, which on one customer's misconfigured host is a symlink into a database volume. The tick from release N authorises the deletion. SM-4 records 0, because a tick exists.
  2. Orvex downgrades "restart one replica" from risky to safe after good results. Every customer who ticked it when it needed the Nightshift team's yes each time now has it run automatically. No customer saw or agreed to the change.
  3. An entry is upgraded from risky to dangerous. Dangerous repairs "cannot be ticked" (FR-20), but the PRD never says what happens to existing ticks.
  4. The update controller, the catalogue signing path or Quornex Fleet is compromised. It ships a changed action under a ticked, safe entry to 10,000 clusters, and the safe entry runs with no human in the loop. SEC-2 lists four containment areas for a compromised *agent* and none for a compromised Fleet, catalogue or release pipeline, which is the single component that can touch every cluster. The portal approvals (FR-14) presumably also go through Orvex-hosted infrastructure, so a compromised portal or Fleet could also forge per-request yeses. SEC-2's rule "the agent cannot forge approvals" does not cover that.
- **Fix:** bind each tick to an entry ID plus a content hash or version. Any change to the action, preconditions, scope or risk level voids the tick and asks the customer again, with a diff in plain language. Define what happens to ticks on reclassification. Add SEC-5, "compromised Fleet, catalogue or update pipeline", with these controls: signed entries, two-person release approval, per-cluster verification of signatures against keys Fleet cannot rotate on its own, and approvals signed end-to-end by the approver's device or session so they can be checked inside the cluster.

### C2. The last-resort condition removes the per-run Orvex check for risky repairs, contradicting "never grants extra permissions"
- **Where:** FR-20, risky ticked: "The Nightshift team's yes **each time** it is about to run"; FR-23 "Orvex's permission given in advance replaces the Nightshift team's yes at that moment"; Glossary *Last-resort condition* and FR-23 "It never grants extra permissions"; FR-21 "There are no timers to manage"; FR-22 "If they do not answer in time".
- **Problems:**
  - **Contradiction.** A risky repair that needs a human yes each time can now run with no human yes. That is an extra permission by any definition, and FR-23 overrides FR-20 without saying so.
  - **Undefined trigger.** "Nobody answers" needs a timeout, but FR-21 says there are no timers. "About 30 minutes" is not testable either. For a *ticked* risky repair the customer is never asked, so "nobody" can only mean the single on-duty engineer (FR-22, SM-8).
  - **Manipulable trigger.** The condition fires on a *prediction* ("failure is predicted within about 30 minutes"). Predictions come from statistics and AI (3.2), which work on logs and metrics that SEC-1 admits can be hostile. SEC-1's rule-based authorisation check only checks that the repair is authorised. Its input, "failure predicted in under 30 minutes", comes from the part that can be manipulated.
  - **Unclear scope.** Can last-resort apply to an *unticked* risky repair? FR-23 says it covers repairs the customer "is allowed to tick", not repairs the customer *has* ticked. If unticked repairs count, last-resort is a tick with no customer yes and no Orvex yes at the time. The statement "safe repairs do not need it" is also false for unticked safe repairs.
- **Failure scenario:** a bad night (500 problems, NFR-1) keeps the one engineer saturated. A noisy memory trend in a customer's database pod pushes the forecast under 30 minutes. A false positive is something FR-10 explicitly expects. Last-resort fires a risky restart of a replica that the precondition check counted as healthy because of stale metrics. Nobody at the customer or at Orvex approved it at the time, and SM-4 still reads 0.
- **Fix:** state the exception honestly in FR-20 ("unless the last-resort condition applies"). Restrict it to *ticked* risky repairs. Require the forecast to meet a stated confidence and to be confirmed by a rule-based, non-AI signal. Define the no-answer timeout as an explicit timer (and drop "no timers" from FR-21). Cap it at one last-resort execution per problem per cluster, followed by a mandatory stop. Count last-resort runs as a separate SM line, not inside "approved".

### C3. Repairs that are each "safe" can add up to an outage; nothing limits how much they disrupt in total
- **Where:** FR-26 "moves to the next repair only if that repair is safe"; FR-28 the coordinator only blocks repairs "on the same thing"; FR-21 a ticked repair stays permitted indefinitely, with no rate limit; Glossary *Safe repair* "will not interrupt the customer's service".
- **Problem:** safety is judged one repair at a time, against the state before that repair ran. No requirement limits how many changes run at once, how often, or how much capacity they take in total across a service or a cluster.
- **Failure scenarios:**
  1. Problem P1 on replica A: a ticked safe repair moves traffic off A. Problem P2 (a separate match) on replica B moves traffic off B. These are different "things", so the coordinator allows both. All checkout traffic lands on C, which falls over. Each step was ticked and safe. The customer never approved "run checkout on one replica".
  2. A ticked safe repair flaps: traffic moves away, health recovers, the problem clears, the trend returns, traffic moves again, every few minutes all night. FR-27 needs "worse" to be detected. Oscillation can stay under that threshold while users see repeated errors.
  3. FR-26 chains repairs after a failure: safe repair 2 is checked against a state that repair 1 has already changed and that cannot be undone ("such as a restart").
- **Fix:** add a per-service and per-cluster disruption budget to the coordinator: a minimum healthy capacity, at most N concurrent changes, at most M runs of any repair per problem per window. Exceeding it escalates instead of running. Re-check preconditions against the *combined* effect of in-flight repairs. Add a cool-down and flap detection to FR-21.

### C4. Orvex's fleet-level changes to customer clusters bypass the approval model, and SM-4 cannot see them
- **Where:** Glossary *Customer production*: "anything whose change can affect the customer's live experience ... at any layer ... needs the customer's approval"; FR-44 (Fleet rolls out releases); FR-30 (Fleet "stops the update immediately, and coordinates recovery"; "Roll back a verified, pre-authorised safe update — Independent update controller"; "with customer approval *where required*"); UJ-2 (Josh "approves" one fix for 300 clusters); Glossary *Approval* "a yes ... for one repair"; Section 10 Q1 (who approves risky changes to OMK/Quornex: unanswered).
- **Problems:**
  - By the PRD's own definition, a Nightshift, OMK or Quornex release, rollout or rollback on a customer's cluster can affect customer production. FR-44 and FR-30 give the customer no approval step.
  - "Pre-authorised" (by whom?) and "where required" (by what rule?) are not defined.
  - UJ-2 introduces a batch approval: one engineer, 300 clusters, many customers. Nothing in 3.5 defines that, and it contradicts "for one repair".
  - These changes do not go through the repair catalogue (FR-17), so the prohibited-action guard (catalogue-only, FR-17) does not apply to them.
  - SM-4 compares *Nightshift's* execution records with approvals, so fleet-controller actions are not counted at all.
  - Alert-only customers (FR-20) still receive Fleet rollbacks.
- **Failure scenario:** the "bad update" at 3 AM is an OMK update. The independent controller rolls 300 clusters back to the previous OMK version, which assumes an older storage driver. A customer cluster with a migrated volume format loses access to persistent volumes. No customer approved it, it does not appear as a Nightshift repair, and SM-4 reads 0.
- **Fix:** make every Orvex-originated change to a customer cluster (releases, platform updates, Fleet rollbacks) its own governed class. Either state explicitly in the customer contract that Orvex may change platform components on its own authority, or route these changes through 3.5. Define batch approval if it exists, at least per customer. Widen SM-4's scope to "all changes to customer clusters by any Orvex component", measured from cluster-side evidence (see H6).

---

## High

### H1. The AI chooses which entry matches; the rule check only authorises the entry it is given
- **Where:** FR-17 the AI helps "match evidence to a catalogue entry"; FR-18 "matching the entry is not a guess"; SEC-1 "A separate, rule-based check, not the AI, authorises execution"; Section 5, hosted model.
- **Problem:** SEC-1 checks that the *selected* entry is ticked or approved. It does not check, independently of the AI, that the entry's evidence conditions actually hold. The hosted model's *output* comes from outside the cluster and is not listed as untrusted. That leaves two ways to steer a repair: log injection, and a compromised or wrong model response.
- **Scenario:** an attacker writes log lines that look like inode exhaustion. The AI matches the ticked safe disk-cleanup entry, the rule check sees "ticked, preconditions OK", and cleanup runs repeatedly, deleting regenerable caches and cached images at peak load.
- **Fix:** every catalogue entry's match criteria must be machine-checkable predicates over metrics and state, not over log text, and the rule engine must evaluate them. The AI may *propose* a match but never be the deciding input. Add "model output is untrusted" to SEC-1.

### H2. Approvals are not authenticated, not tied to the evidence the approver saw, and arrive through a channel that isn't sanctioned
- **Where:** Glossary *Approval* "through Slack or the Quornex portal"; FR-21 a one-time yes has no expiry ("no timers"); UJ-1 "Nightshift reaches him by phone call ... Amine approves".
- **Problems:**
  - No requirement on *who* may approve: role, strong authentication, a named list of approvers. Anyone in a shared Slack channel, a guest or a contractor can approve a dangerous repair.
  - A yes is tied to "one repair", not to the evidence snapshot and description shown. A yes given at 02:00 for "memory runs out in 4 hours, low traffic" can run at 08:30 at peak traffic, because FR-21 re-checks only the catalogue preconditions, not "is this still the situation the person approved?".
  - UJ-1 implies approval by phone, which the Glossary does not allow, and voice is weak authentication.
- **Fix:** add an approver identity requirement (named approvers per customer, SSO/MFA, Slack identity mapped to a portal identity). Bind each yes to a request ID, an evidence hash and an expiry. Re-request if the situation has changed materially. Either remove phone approval from UJ-1 or specify how it is authenticated.

### H3. Delegation lets Orvex alone approve dangerous changes to customer production
- **Where:** FR-20 "Orvex support may give [the customer's yes] instead if the customer has delegated"; dangerous repairs need "the customer's yes and the Nightshift team's yes".
- **Problem:** with delegation, both signatures for a dangerous repair, for example "Force-restart the only production instance", come from Orvex. Nothing requires the two to be different people, nothing defines delegation scope (all repairs? safe only?) or revocation, and nothing tells the customer when Orvex used it. This also undercuts the Glossary claim that the last-resort condition "stays within the customer's knowledge".
- **Fix:** delegation is scoped (by risk level and per cluster), recorded in FR-32, notified to the customer at the time of use, and revocable. Two different people are required. Consider excluding dangerous repairs from delegation by default.

### H4. Code fixes contradict FR-17, FR-38, NFR-3 and PRIV-5
- **Where:** FR-17 "The AI never invents a repair, and in particular never generates shell scripts or commands to run"; FR-40 "Nightshift proposes a fix" and it "enters the repair catalogue"; FR-38 "never as one-off changes to single clusters"; NFR-3 "same release and configuration everywhere"; FR-40/Glossary *customer-specific entry*; PRIV-5 "Customer code stays in the cluster"; FR-42 [OPEN].
- **Problems:**
  - An AI-generated patch is AI-generated code that runs in production, so FR-17 is broken unless reworded.
  - A customer-specific entry *is* a one-off change for one customer, which contradicts FR-38 and NFR-3.
  - The repair catalogue is distributed through the one release to every cluster (FR-38, FR-44). A customer-specific entry containing the patch therefore either ships to all 10,000 clusters, leaking the customer's code against PRIV-5 and PRIV-1, or needs a separate per-customer distribution path that the PRD never defines.
  - FR-42's open question allows approval "on the automated test results alone", meaning AI-written code reaches production without a human reading it.
  - FR-42 step 4 has an Orvex engineer viewing customer code remotely, which is a human egress path that PRIV-5 does not acknowledge.
- **Fix:** reword FR-17 as "never executes AI-generated changes without human review and catalogue registration". Define a per-customer catalogue partition with its own distribution path that never leaves the customer's clusters. Close FR-42: no human code review means rejection. List engineer access in the PRIV-6 egress record.

### H5. The line between prohibited and dangerous actions is incoherent, and enforced only by catalogue review
- **Where:** Glossary *Prohibited action* "modifying or deleting customer records, databases or backups"; *Dangerous repair* "a repair that could corrupt data"; Quornex "provides databases ... fully managed by Orvex"; FR-17 "A prohibited action is never in the repair catalogue".
- **Problems:**
  - A dangerous repair may "corrupt data" and can be approved, yet modifying a database is prohibited even with approval. Force-restarting a single-instance database mid-transaction, failing over a managed database, deploying a code fix that contains a schema migration, and rolling back an app version against a migrated schema (UJ-1, UJ-3) all modify databases in effect.
  - Managing Quornex databases (failover, scaling) is presumably exactly what Nightshift should do, but is it prohibited?
  - Enforcement exists only as "never in the catalogue". No runtime guard (for example, no write or delete rights on database volumes, backup buckets or snapshots) is required.
- **Fix:** define prohibited actions by *effect on data* (logical writes or deletes of records, backups or snapshots), separately from availability actions such as restart or failover. Say which managed-database operations are allowed. Add a runtime control: Nightshift's identities hold no delete or write rights on backup stores or database volumes (ties to SEC-4). Treat schema migrations in code fixes and app rollbacks across schema changes as prohibited, or require special handling for them.

### H6. SM-4 ("0 unapproved changes") is measured from records the acting agent writes itself
- **Where:** SM-4 "comparing execution records with approval records"; FR-32; FR-33 "the agent can add to it but cannot change or delete"; SEC-2 "Missing or interrupted reporting must be detectable"; 3.7 local autonomy during partitions.
- **Problem:** an append-only log stops rewrites, not *omissions*. A compromised or buggy agent, or one acting during a legitimate partition when records are buffered locally inside the agent's reach, can make a change and never log it. SM-4 then shows 0. "Detectable" missing reporting cannot be told apart from a legitimate partition.
- **Fix:** measure SM-4 from evidence the agent does not control: the Kubernetes API audit log, the cloud provider's audit trail (CloudTrail on EKS), BMC event logs, and the coordinator's lock log. Each is shipped by a separate identity and reconciled against Nightshift's records. Define a maximum buffering window and treat an agent that executes while it cannot report as a separate countable class.

### H7. Every notification channel sends data out of the cluster, and PRIV-2 and PRIV-6 do not cover them
- **Where:** FR-14 Slack and portal; FR-13 phone calls; FR-15 dashboards "reached through the Quornex portal"; FR-16 morning summary; FR-12 "Orvex receives a signal whenever the customer confirms"; FR-31 audit records visible to the customer; PRIV-6 "a record of exactly what left the cluster".
- **Problem:** FR-11 messages must explain the evidence in plain words: service names, error text, sometimes identifiers. They go to Slack (a third party), a telephony or text-to-speech provider, and a central portal. A per-cluster dashboard served through a central portal sends raw data out unless it proxies live to the cluster. None of these paths appears in the sanitisation boundary or the egress record, and the planted-secret tests (PRIV-6) only target the model path.
- **Fix:** list every outbound channel in Section 4, apply PRIV-2 sanitisation and PRIV-6 recording to each, run planted-secret tests on notifications too, and state whether the portal holds data or proxies it.

### H8. The staffing model is at full capacity on a normal night by the PRD's own arithmetic
- **Where:** SM-8 "one engineer is on duty"; "at 250 problems a night with 90% handled automatically and 20 minutes for each of the rest, the human work is about 8 hours a night; at 500, about 17 hours"; NFR-1 "False alerts are not counted as problems"; FR-20 ticked risky repairs need the team's yes "each time"; FR-22 "the repair waits".
- **Problems:**
  - 8.3 hours of work for one engineer on a roughly 8 to 12 hour night is 70 to 100% utilisation before breaks, phone calls, false alerts (up to 10% allowed by SM-6), escalations of incident-catalogue problems (FR-19), monitoring failure cases (FR-4), hardware escalations and fleet-wide events (FR-30).
  - The 90% automatic share is assumed (SM-9 "target to set"), yet every ticked *risky* repair needs a human each time, so how much is truly automatic depends on how repairs split by risk level, which is unknown.
  - The headcount fell from the brief's 25 to 29 (350 to 400 clusters per engineer) to 15 (670 per engineer), and the PRD gives no new evidence for the change.
  - One engineer is a single point of failure. When they are busy, FR-22 makes every risky repair across 10,000 clusters wait, which is exactly the condition that triggers last-resort (C2).
- **Fix:** model night load as a queue (arrival rate, service time, target wait time to approval) including false alerts and escalations. Set an approval-latency SLO. Define automatic paging of backups by queue depth, not "when needed". Present 15 engineers as a hypothesis with the staffing figure at 60%, 75% and 90% automation shown side by side.

### H9. The validation plan cannot statistically validate the targets it sets
- **Where:** Section 8 preamble "checked first in controlled tests ... then on the first 100 clusters"; SM-8 "Measured on the first 100 clusters, then extrapolated"; NFR-1 250 problems a night across 10,000 clusters.
- **Problem:** 250 / 10,000 × 100 ≈ 2.5 problems a night on 100 clusters, about 75 a month. After 90% automation that is about 7 human-handled problems a month, and very few risky or dangerous repairs. That is far too small a sample to show 95% repair success (SM-2), 0 harm (SM-3), 0 unapproved changes (SM-4) with any confidence, or staffing at 100× the scale. Correlated fleet failures (FR-30) and bad nights effectively never happen at 100 clusters.
- **Fix:** state confidence intervals and minimum sample sizes per metric. Rely mainly on failure injection at scale for the low-frequency classes. Name the scale steps between 100 and 10,000 (for example 1,000) with go/no-go criteria.

### H10. The fourth proof in the Vision (does it replace engineers, at lower cost?) has no baseline
- **Where:** Vision "It shows whether it really replaces engineers, and so whether it costs Orvex less or more than they would"; COST-5; SM-8; Section 10 Q5 "What monitoring and night cover does Orvex have today?" (not asked).
- **Problem:** there is no definition of how many engineers 10,000 clusters would need without Nightshift, or at what cost. Without that counterfactual the comparison cannot be made, so version 1 cannot pass or fail this proof. SM-10 and COST-4 ("as low as realistically possible") have no number either.
- **Fix:** define the baseline: clusters per SRE without Nightshift, from industry or Orvex data, with a source. State the break-even cost per cluster. Make COST-5 a pass/fail comparison.

### H11. The repair coordinator only sees Nightshift's own repairs
- **Where:** FR-28 "prevents conflicting repairs ... Before starting any repair, Nightshift checks with the coordinator"; FR-30 independent update controller; FR-29 marks "stay in place".
- **Problem:** the coordinator knows nothing about the Fleet update controller (FR-30), the Kubernetes controllers (HPA, cluster autoscaler, PodDisruptionBudgets, operators), the customer's CI/CD, EKS managed-node-group replacement, or human operators. Nightshift drains node A while the autoscaler scales down node B and a customer deploy rolls out, leaving the service under capacity. The coordinator's marks have no expiry or lease, so a mark left by a crash (FR-29) keeps node A out of scheduling indefinitely.
- **Fix:** the coordinator must read external change signals: in-flight rollouts, PDBs, autoscaler state, Fleet rollout state, change freezes. Fleet actions must take the local coordinator's locks. Marks carry leases with expiry and reconciliation.

### H12. Fleet is said to receive only liveness, yet it detects correlated failures and keeps reports
- **Where:** FR-6 "Only liveness information (alive, reporting) goes to Quornex Fleet ... it carries no private data [AI, to confirm]"; FR-30 Fleet "recognises the shared problem", "preserve the cluster reports", "suspected update: v2.4"; FR-15 and FR-45 grouped dashboards per 100 clusters; FR-46.
- **Problem:** correlation needs problem types, versions and timings from every cluster. Preserving cluster reports means storing them somewhere. The PRD never says what problem data flows to the multi-tenant Fleet, under what sanitisation, or where the "preserved reports" live. Customers who choose "time and type only" (PRIV-2) may starve the correlation. Cross-customer correlation in a multi-tenant store is also exactly what FR-46 has to isolate.
- **Fix:** define a Fleet telemetry schema (fields, sanitisation, retention, tenant isolation), separate from liveness. State where preserved reports are stored (in the cluster, with Fleet holding only references). Define the minimum fields correlation needs and what happens for strict-privacy customers.

### H13. Nothing stops a bad repair entry fleet-wide
- **Where:** FR-27 "stops further automatic repairs on *that cluster*"; FR-44 canary "the rest only once those are healthy"; FR-38.
- **Problem:** a canary checks release health shortly after rollout. A catalogue entry that misbehaves only under a rare trigger (a date, a certificate expiry, a disk-size boundary) passes the canary and later fires on thousands of clusters at once. FR-27 stops it one cluster at a time, after harm. FR-30 handles bad *updates*, not bad *repairs*.
- **Fix:** have Fleet monitor harm and rollback rates per repair entry, with an automatic fleet-wide kill switch per entry (a local flag that still works when the cluster is partitioned). Cap concurrency per repair entry across the fleet.

---

## Medium

### M1. Dangerous repairs that can disconnect a node have no way to undo or verify them
- **Where:** Glossary *Dangerous repair* "anything on a live node that could disconnect it from Nightshift"; FR-24 verify and undo.
- **Problem:** if a network-card or IP change cuts the node off, FR-24 can neither verify nor undo it.
- **Fix:** require out-of-band rollback or an on-node dead-man's switch (auto-revert unless confirmed within N minutes) for any repair that can disconnect a node. If neither exists, ban the repair.

### M2. Network partitions and split brain are unhandled; hardware credentials are unreachable when they are needed
- **Where:** FR-3 checks neighbour nodes; 3.4 "only a mitigation that is valid whatever the cause may run"; SEC-3 credentials "kept securely and accessed only when needed"; 3.7.
- **Problems:**
  - An agent stuck in a minority partition sees most nodes as silent. A cause-agnostic mitigation such as "move workloads off silent nodes" is valid whatever the cause, and can drain healthy capacity.
  - If the credential vault is central, a cluster cut off from Orvex cannot reach out-of-band management just when FR-3 needs it.
  - The out-of-band network is often not reachable from pods at all.
- **Fix:** require quorum or an outside view (Fleet's or out-of-band) before mitigating a mass node loss. Cap mitigation to a fraction of nodes. Specify where hardware credentials live so they survive a partition (an in-cluster broker with narrow scope).

### M3. NFR-4 ("Nightshift failing never harms the customer") rests on an unchecked assumption
- **Where:** NFR-4; FR-28 marks; NFR-6 "Target to set".
- **Problem:** if Nightshift dies mid-repair, cordons, taints, half-moved traffic and coordinator marks remain. If Nightshift uses admission webhooks or an in-cluster GPU model, its failure or its resource use can block deploys or starve workloads. No footprint cap exists.
- **Fix:** list Nightshift's side effects that outlive a crash and require them to expire (TTL) or be reverted by an independent watchdog. Set footprint limits. Require any webhooks to fail open.

### M4. Key requirements have no testable thresholds
- **Where and problem:**
  - FR-9: four factors, no thresholds or combination rule.
  - FR-10: "substantially", "enough", "stays stable".
  - FR-2 and NFR-7: heartbeat timeout is OPEN.
  - FR-23: "about 30 minutes".
  - FR-35: "well controlled".
  - FR-1 and FR-5 on EKS: "what the provider's available signals allow".
  - NFR-6: "Target to set".
  - FR-11: "can be understood by a non-expert", with no test.
- **Fix:** give each one a parameter, an owner and a test method (for example, a readability score or comprehension panel for FR-11, and a per-platform detection matrix for EKS).

### M5. The SM-1 and SM-2 denominators can be gamed
- **Where:** SM-1 "80% of *supported*, slowly developing problems"; SM-2 "95% of authorised repairs".
- **Problem:** Orvex decides what is "supported" and what gets injected, so shrinking the catalogue raises SM-1. SM-2 is dominated by high-volume trivial safe repairs such as disk cleanup, so risky repairs could succeed only half the time and SM-2 still passes.
- **Fix:** report SM-2 per risk level. Report SM-1 alongside SM-C1 against *all* customer-felt incidents. Fix the failure-injection set in advance (for example, the top-20 failure catalogue).

### M6. "Zero harm" has neither a definition nor a threshold
- **Where:** Vision "performs authorised repairs without harming"; SM-3; Section 10 Q12.
- **Problem:** "harmful" is undefined. How is "made things worse" (FR-27) told apart from "did not work"? With no threshold, the third proof cannot fail.
- **Fix:** define harm operationally (for example, a new SLO breach, data loss or capacity loss caused by the repair within T minutes) and set a version 1 threshold.

### M7. Runtime tuning (FR-39) conflicts with "same configuration everywhere" (NFR-3) and with stable preconditions
- **Where:** FR-39 "Nightshift may tune its settings only within limits Orvex sets"; NFR-3.
- **Problem:** if thresholds used in matching or in preconditions can be tuned, automatic repairs change behaviour per cluster without a release or a renewed tick (see C1).
- **Fix:** exclude match criteria and preconditions from self-tuning. Record every tuned value in FR-32.

### M8. FR-25 and FR-18 rank repairs differently
- **Where:** FR-18 "lowest-risk repair expected to work"; FR-25 "ranked by safety, estimated success rate and potential impact. Nightshift always tries the safest repair first".
- **Problem:** a three-factor ranking and "always safest first" give different orders. "Estimated success rate" has no source or data before deployment.
- **Fix:** define one ordering rule, with tie-breaks and the source of the success estimates.

### M9. Recording every read is undefined or unworkable, and the audit metadata itself can leak
- **Where:** FR-31 "Everything Nightshift reads ... is recorded".
- **Problem:** continuous metric and log scraping is millions of reads. File paths, table names and query shapes in the audit can be sensitive, and FR-33 stores them "out of the agent's reach", possibly outside the cluster.
- **Fix:** define what counts as a read event (for example, access sessions per source rather than samples) and keep audit records in the cluster or sanitised.

### M10. The code-fix test environment needs production data and resources
- **Where:** FR-42 step 2 "isolated test environment within the customer's infrastructure".
- **Problem:** realistic tests need data, which means copying production data (privacy, and possibly prohibited database operations), and they use the customer's capacity at their cost.
- **Fix:** specify the source of test data (synthetic or masked), resource limits, cost attribution (COST-3) and customer consent.

### M11. "Disk cleanup" is labelled safe but can break rollbacks
- **Where:** Glossary *Disk cleanup* "unused container images where the runtime confirms removal is safe".
- **Problem:** the runtime only knows that no *running* container uses an image. Deleting the previous release's image, a CronJob image or an air-gapped image breaks the next rollback (UJ-1 and UJ-3 rely on rollbacks) or the next job run, when the registry is unreachable.
- **Fix:** keep images referenced by current and previous ReplicaSets, CronJobs and pinned rollback targets. On air-gapped or sovereign setups, protect any image not available in the registry.

### M12. Out-of-band access is checked only at installation
- **Where:** FR-7.
- **Problem:** a BMC rotated, broken or with firmware updated after installation silently moves the server into limited visibility. Nobody is told, and the customer's acknowledgement is stale. EKS has no equivalent coverage acknowledgement.
- **Fix:** validate out-of-band access continuously. Alert and update the coverage report when coverage changes. Apply the same acknowledgement for EKS.

### M13. Multi-cluster repairs and a compromised management agent are not covered
- **Where:** FR-28 and 3.7 "Repairs that affect more than one cluster are coordinated by the management agent"; SEC-2 "the Nightshift agent in one cluster".
- **Problem:** does one yes cover a repair across N clusters? The management agent holds identities across a customer's clusters, and SEC-2's containment table does not cover it.
- **Fix:** define approvals for multi-cluster repairs (one per cluster, or an explicit multi-cluster scope). Add the management agent to SEC-2.

### M14. Automatic rollback is itself an unapproved change
- **Where:** FR-24 "Nightshift undoes it"; FR-27 "automatically rolls back what it can".
- **Problem:** undoing a risky repair, for example reverting a network change, can be as risky as the repair, yet it needs no approval and has no risk level.
- **Fix:** give each rollback a risk level in the catalogue. Pre-approve it explicitly as part of the repair's approval, and record it.

### M15. The privacy controls are optional or cannot be shown to work
- **Where:** PRIV-3 "If needed, a further test runs"; PRIV-2 placeholders; PRIV-6 "an outside audit".
- **Problem:** who decides when PRIV-3 is "needed"? Placeholder replacement relies on recognising private values in free-text log fields. A card number or token in an unexpected format gets through, and planted-secret tests only find formats someone thought to plant. The outside audit has no scope or frequency.
- **Fix:** make PRIV-3 mandatory. Send the hosted model allowlisted structured fields only, never free text. Define the audit's scope, frequency and auditor independence.

### M16. The approval model rests on stakeholder answers that have not arrived
- **Where:** Section 10 Q1 (who approves OMK/Quornex changes), Q2 (does Danny accept the double yes?), Q4 (reliability number), Q5, Q6, all "not yet asked"; 9.1 "Nothing has been deferred".
- **Problem:** the core of 3.5 and SM-7 depends on unanswered questions, and scope covers everything with no prioritisation, against a hand-in of 10 to 14 November.
- **Fix:** label each 3.5 requirement as confirmed or assumed. State a fallback if Danny rejects the double yes. Name a minimum version 1 cut (for example, defer the shared GPU option and code fixes) in case time or answers run out.

### M17. Crash recovery resumes on an old approval
- **Where:** FR-29 "If continuing is safe, it continues".
- **Problem:** a one-time yes (FR-21) given before the crash is reused after an unknown gap. The progress store's location is not stated: if it sat on the lost node, there is nothing to recover from.
- **Fix:** after a crash, an approval tied to a request (H2) expires unless still valid. Progress is stored off-node, with the coordinator.

---

## Low

### L1. The user journeys contradict the approval table
- **Where:** UJ-3, UJ-4.
- **Problem:** UJ-3 says "after the rollback you approved", but it was a tick. If a rollback is risky, the team's yes is also needed (FR-20), and that is not mentioned. UJ-4 approves a memory-creep fix (a restart, which is risky per the Glossary) with only the owner's yes.
- **Fix:** add the Orvex step or name the repair's risk level.

### L2. Who receives a phone call is unclear
- **Where:** FR-13, FR-22, UJ-1.
- **Problem:** FR-13 does not say whether the call goes to the customer, Orvex, or both, or in what order.
- **Fix:** add a recipient column to FR-13.

### L3. Fleet notices a silent agent but does nothing about it
- **Where:** FR-6.
- **Problem:** no action, owner or SLA after an agent goes silent, and no restart path for Nightshift itself. A "zombie" agent that still sends heartbeats but no longer does work goes unnoticed, because liveness is not correctness.
- **Fix:** define the response to silence, and add a functional health probe beyond liveness.

### L4. Revocation races are unhandled
- **Where:** FR-21.
- **Problem:** if the customer unticks, or delegation is revoked, while a repair is queued or running, it is unclear whether the repair stops.
- **Fix:** check revocation right before execution and at each step.

### L5. The FR-30 example contradicts the canary in FR-44
- **Problem:** "a bad update reaching 300 clusters" means either the canary group is 300 clusters or the canary missed the problem. The type of update (Nightshift, OMK, Quornex, or customer app) is never stated.
- **Fix:** state the canary size and the update type.

### L6. Hardware ownership "may vary", but escalation assumes the customer owns it
- **Where:** Glossary *Platforms*; 3.4 "Escalate ... only through the customer".
- **Problem:** if Orvex or a hosting partner owns the hardware, the escalation path and responsibility do not match.
- **Fix:** add an escalation path for each ownership model.
