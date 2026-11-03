> Second validation, after the review findings and polish were applied (2026-10-31). Compare with validation-report.md (before).

# PRD: Nightshift — Validation Report (after)

- **PRD:** `/home/amine/nightshift/_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/prd.md`
- **Rubric:** `/home/amine/nightshift/.claude/skills/bmad-prd/assets/prd-validation-checklist.md`
- **Run time:** 2026-10-31T15:31:49+00:00
- **Grade:** **Poor**. 4 critical findings across all reviewers (2 adversarial, 2 security), which alone sets Poor. The rubric alone would grade Fair: no thin or broken dimension, but 3 high findings.
- **Reviews:** `review-after-rubric.md` (primary), `review-after-adversarial.md`, `review-after-judge.md`, `review-after-security.md` (all in the PRD folder)
- **Findings:** 4 critical, 36 high, 49 medium, 22 low (111 total)

| Source | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Rubric | 0 | 3 | 10 | 4 | 17 |
| Adversarial | 2 | 16 | 17 | 7 | 42 |
| Judge | 0 | 6 | 11 | 6 | 23 |
| Security | 2 | 11 | 11 | 5 | 29 |
| **All** | **4** | **36** | **49** | **22** | **111** |

## Overall verdict

The authorisation model is the PRD's backbone and holds up well. The risk levels in the Glossary, the approval table in FR-21, FR-22 to FR-24 and the Non-goals in 3.2 are crisp, sourced and consistent with each other, and the open items are triaged honestly. Three gaps remain, and each touches either the thesis or the next step. "Harmful repair" is never defined, yet the Vision's third proof point and SM-3 rest on it. FR-41 lets Nightshift tune cluster settings without saying how that fits the tick/approval rules that SM-4 holds at zero. And no journey shows a customer setting up the permissions the whole model depends on, although UX wireframes come next. Fix those three and the PRD is ready for UX and architecture.

Beyond the rubric, the adversarial and security reviewers each raise 2 critical findings, and those 4 set the grade at Poor; on the rubric alone it would be Fair. Across all four reviews there are 4 critical, 36 high, 49 medium and 22 low findings (111 in total). Both critical pairs land on the same gap: the PRD says the approval check sits outside the agent, but not who holds the rights to act or where the other controls run. The **adversarial** reviewer finds two direct paths to changes in customer production that bypass the approval model: FR-41 tuning, which needs no tick and still runs in alert-only mode (C-1), and a compromised agent that holds its own execution and egress rights, so it never needs to forge an approval (C-2). It adds contradictions an architect cannot resolve without a product decision: local autonomy versus enforcement outside the agent (H-2), one release everywhere versus customer-controlled updates (H-11), and the code-fix review path versus FR-39 and FR-40 (H-7). It also calls the staffing claim that carries the business case unverified, resting on an assumed 90% and leaving out most of the human review work the PRD itself creates (H-13). The **security** reviewer reaches the same core from the threat side: the rights to change things are not separated from the agent that reads untrusted data (SEC-R2-01), and approvals, ticks and policies can be forged centrally through the portal, the Slack integration or Fleet, whose powers are unbounded (SEC-R2-02). Its remedy is two new requirements, SEC-8 (a separate executor and a read-only agent) and SEC-9 (authorisations signed by the person and verified in the cluster), and it notes that none of its findings needs a redesign of the product. The **judge**, reading as Danny, raises no critical findings and calls the PRD disciplined, honest and well traced. Its high findings are design tensions: two humans for every risky repair and customer approval of Orvex's own platform collide with "self-managing", "fully managed by us", the 99.9% target and the cost target; the default mode and default checklist are undefined; and nothing says how Nightshift behaves with no model available. The reviews converge on FR-41 tuning outside the approval model (all four), the compromised agent's rights inside its own cluster (adversarial, judge, security), the staffing arithmetic (rubric, adversarial, judge), code sent to a hosted model despite "secrets never leave" (rubric, adversarial, security), the undefined "harmful repair" (rubric, adversarial), and, between the adversarial and security reviews, Orvex holding both approval keys under delegation, customer code becoming fleet-wide entries, approvals with no expiry, and Orvex alone owning the outbound allowlists.

## Before → after

The grade stays Poor, but for narrower reasons. Criticals halve from 8 to 4, and total findings fall from 122 to 111. On the rubric, Done-ness clarity moves from thin to adequate, three dimensions rise to strong, and rubric high findings drop from 5 to 3, so the rubric-only grade stays Fair.

|  | Before (2026-10-30) | After (2026-10-31) |
|---|---|---|
| Grade | Poor | Poor |
| Rubric-only grade | Fair (one thin dimension, 5 high findings) | Fair (no thin dimension, 3 high findings) |
| Critical | 8 | 4 |
| High | 39 | 36 |
| Medium | 53 | 49 |
| Low | 22 | 22 |
| Total | 122 | 111 |
| Rubric (C / H / M / L) | 0 / 5 / 17 / 5 | 0 / 3 / 10 / 4 |
| Adversarial (C / H / M / L) | 4 / 13 / 17 / 6 | 2 / 16 / 17 / 7 |
| Judge (C / H / M / L) | 0 / 8 / 10 / 7 | 0 / 6 / 11 / 6 |
| Security (C / H / M / L) | 4 / 13 / 9 / 4 | 2 / 11 / 11 / 5 |

| Dimension | Before | After |
|---|---|---|
| Decision-readiness | adequate | strong |
| Substance over theater | adequate | strong |
| Strategic coherence | adequate | adequate |
| Done-ness clarity | thin | adequate |
| Scope honesty | adequate | strong |
| Downstream usability | adequate | adequate |
| Shape fit | adequate | adequate |

Read the counts with care. The second-pass reviewers judged the PRD as it stands and did not read the first reviews, so the after findings are a fresh read, not a list of leftovers. The first-pass criticals (ticks not bound to a catalogue version, last-resort overriding the per-run yes, no limit on combined disruption, Fleet actions outside the approval model, unauthenticated approvals) now come back, if at all, as narrower high or medium findings. The remaining criticals are deeper: who holds the rights to act, and whether central systems can mint authorisations. The adversarial review's own count table says 15 high, but it lists 16 (H-1 to H-16); this report counts the 16 listed.

## Dimension verdicts

| Dimension | Verdict | Critical | High | Medium | Low |
|---|---|---|---|---|---|
| Decision-readiness | strong | 0 | 0 | 2 | 0 |
| Substance over theater | strong | 0 | 0 | 0 | 1 |
| Strategic coherence | adequate | 0 | 1 | 1 | 1 |
| Done-ness clarity | adequate | 0 | 1 | 3 | 1 |
| Scope honesty | strong | 0 | 0 | 1 | 1 |
| Downstream usability | adequate | 0 | 0 | 2 | 0 |
| Shape fit | adequate | 0 | 1 | 1 | 0 |

### Decision-readiness — strong

Decisions are stated as decisions, and most come with their reasons. Examples: "Delegation never covers dangerous repairs" (FR-21), "Focus for the first version: the hosted model ... because it should cost much less" (Section 7), the trade-off in FR-43 ("in-cluster only would leave the experiment with very few users"), and "Whether that needs a separate tool is for the architecture" (FR-32 table). The Section 10 triage gives every remaining item an owner and a revisit trigger, and the "Answered and decided" list shows questions that were actually closed. Someone pushing back on the extra Orvex approval step would find their objection already raised as Q2.

Two places still stop short of a decision. The first is staffing. SM-8 does the arithmetic (about 8 hours of human work on an average night, about 17 on a bad one) but never compares it with "One Nightshift engineer is on duty each night" (FR-23, SM-8). The second is the code-fix experiment, which has metrics but no rule for keeping or dropping the feature.

### Substance over theater — strong

Very little here is furniture. The Vision is specific to this product (OMK versus EKS coverage, sovereign cloud for small businesses, 10,000 clusters, four testable proof points) and could not be swapped into another PRD. The three user types each drive routing and approval logic (FR-12, FR-21), and the UJs use named roles that map to them. The cost section separates technical cost from total operating cost and adds a "without Nightshift" baseline (COST-4), which is real substance. The example tables (risk levels, FR-8, FR-32 responsibilities) do work in the PRD rather than decorate it.

### Strategic coherence — adequate

The thesis is clear, and the success metrics follow it: detect (SM-1), explain (SM-5), repair without harm (SM-2, SM-3, SM-4), and replace engineers at a lower cost (SM-8, SM-9, SM-10, COST-4). Each counter-metric is paired with a specific metric. The MVP is "everything", and the PRD says so openly (3.1: "Nothing has been deferred to a later version yet"). That is a legitimate choice for a design challenge where Danny wants feedback on everything. Two things weaken the arc: the key term behind proof point 3 is undefined, and the new focus on the hosted model in Section 7 is not reconciled with the scope list in 3.1.

### Done-ness clarity — adequate

The authorisation and recording FRs are testable as written. FR-21's table, FR-22's version-tied ticks, FR-34's count of unapproved changes with a target of 0, FR-31's crash recovery and FR-7's four-step installation check all give story writers clear acceptance conditions. Detection scope is tied to the failure catalogue deliverable (FR-1), which is a sound way to bound it. Weaker FRs remain, though: one sits outside the approval model, and several use adjectives where bounds are needed and are not covered by the deferral of timing targets in Q8.

### Scope honesty — strong

This is the PRD's strongest structural feature. Section 3.2's Non-goals do real work: each points to the requirement that enforces it (FR-17, FR-23, PRIV-1, SEC-1), and "Treat silence as permission" is stated with its exception. The scope admits its own instability ("Code fixes might not stay after the first version"). Unconfirmed items are labelled where they appear (for example "[DESIGN ASSUMPTION unless Danny confirms]", "Amine's proposal, to validate" and "our proposal, pending Danny's confirmation" in FR-47), and the Section 10 triage gives every deferral an owner. The number of open items is proportionate for a design PRD whose next steps are UX and architecture rather than a build.

### Downstream usability — adequate

The Glossary is substantial and mostly respected: risk levels, approval, advance permission, last-resort condition and the coordination tiers (Nightshift agent, management agent, Quornex Fleet) are used consistently from FR-6 to FR-48. The IDs are contiguous and unique: FR-1 to FR-49, SM-1 to SM-10 plus SM-C1 to SM-C3, PRIV-1 to PRIV-7, SEC-1 to SEC-7, COST-1 to COST-6, NFR-1 to NFR-8 and UJ-1 to UJ-5. Cross-references resolve. Section 11 tells the architecture, failure catalogue and cost model exactly what to contain, and the addendum routes architecture-depth material cleanly. What remains is a handful of component and surface names that the architecture and wireframes will have to guess at.

### Shape fit — adequate

This is a multi-stakeholder B2B product with real UX, feeding wireframes and then architecture, so the UJs carry weight, and the PRD rightly has them. Five journeys cover the customer warned in advance, approval in a crisis, Orvex technical approval, the morning summary and a fleet-wide failure. The FR sections are a capability-spec shape, which suits the operator-side material. The gap lies in which journeys exist. The model's most distinctive UX surface, the settings checklist, appears in no journey, and one of the three named user types has no journey at all.

## Reviewer verdicts

### Adversarial review

Source: `/home/amine/nightshift/_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/review-after-adversarial.md` — 2 critical, 16 high, 17 medium, 7 low (42 findings).

**Verdict:** The PRD is much tighter on the main approval path (FR-21 to FR-24, SEC-1, SEC-7). It still has two direct paths to changes in customer production that bypass the approval model: FR-41 tuning, and a compromised agent that holds its own execution and egress rights. It also has several contradictions an architect cannot resolve without a product decision: where authorisation is enforced versus local autonomy, one release everywhere versus customer-controlled updates, and the code-fix review path versus FR-39 and FR-40. The staffing claim, which carries the business case, rests on an unverified 90% figure and leaves out most of the human review work the PRD itself creates.

The review's own count table says 15 high; it lists 16 (H-1 to H-16), and this report counts the 16 listed.

### Judge review (Danny, Orvex)

Source: `/home/amine/nightshift/_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/review-after-judge.md` — 0 critical, 6 high, 11 medium, 6 low (23 findings).

**Verdict:** A disciplined, honest, well-traced PRD that answers most of the brief's "must answer" questions at requirement level and hands the rest cleanly to the other deliverables. Its main weaknesses are not missing sections but design tensions it has not confronted yet: the approval model (two humans for every risky repair, customer approval of Orvex's own platform) collides with Danny's "self-managing", "fully managed by us" and "close to public-cloud reliability" goals and with the cost target. And the compromised-agent story covers everything except the cluster the agent sits in.

| Criterion | Verdict | One-line reason |
|---|---|---|
| Technology choices | **Adequate for a PRD (handed off)** | Correctly deferred to the architecture (Section 11), but the PRD leaves the requirements that would discriminate between tools (footprint, retention, timing) as "target to set" |
| Architecture clarity (bare metal and EKS) | **Good, with gaps** | The three-level model, out-of-band rules, limited-visibility mode and "each cluster on its own" are clear. EKS is under-described, the case without a BMC on cheap hardware is treated as the exception, and the PRD never says what happens when the model is unavailable |
| Privacy and security | **Good on privacy, one major security gap** | Allowlists on every outbound channel, placeholders, an outbound check, planted-secret tests and honest proof claims are strong. A compromised agent's power inside its own cluster is not addressed, and the PRD does not say whether free-text log lines ever leave the cluster |
| Cost credibility | **Structure good, credibility at risk** | Two numbers per cluster, a without-Nightshift baseline, full GPU cost and who pays are all right. But the PRD's own design choices make human time the dominant cost, it never says so, and the 100-cluster case will not be "a few dollars" |
| AI fluency | **Strong** | Every statement is tagged with its source; AI suggestions are marked as accepted, reworded or unconfirmed; Codex's figures are labelled "partly checked". The volume of provenance tags hurts readability, and some AI-sourced tables are not visibly verified |
| Honest thinking | **Strong** | Uses [OPEN], [To test] and "proposed, not observed" labels; makes no 100%-privacy claim; validates rare events with failure injection; shows staffing sensitivity arithmetic. It falls short on the tensions between its own requirements, which it does not name (approval latency vs 99.9%, one engineer vs its own workload arithmetic) |

**Where the PRD departs from Danny's stated wishes:**

| # | Danny said | PRD does | Status |
|---|---|---|---|
| 1 | "Safe repairs should be automatic" (Ex 4) | Automatic only if the customer ticks them; the default is undefined | Not raised with Danny; see H3 |
| 2 | Customer approves, optionally via Orvex support (Ex 1) | Adds Orvex technical approval for every risky and dangerous repair, even when ticked | Asked in Ex 5 Q1; pending |
| 3 | Quornex "fully managed by us"; "same tested release everywhere" (brief) | Platform updates and repairs need a customer maintenance policy or approval | Asked in Ex 5 Q2; conflict with NFR-3 not acknowledged (H4) |
| 4 | GPUs shared across clusters worth exploring (Ex 3) | PRIV-1 forbids private data moving even between one customer's clusters, so a shared GPU gets only sanitised data | Asked in Ex 5 Q3; stricter than the brief requires, and defensible |
| 5 | Code fixes in the first version, to see them in real use (Ex 2); heavy hosted-AI use (Ex 3) | Hosted model only with separate consent; a mandatory Orvex engineer reads the code, and the patch is rejected if the customer refuses access | Open question 7a; defensible, but limits the experiment's reach |
| 6 | "Make every other cluster ready for it" (brief) | Fully human-gated, release-bound learning, with no speed target | Not raised; see M6 |
| 7 | "Tuning and self-healing" (brief quote) | Tuning reduced to one line | Not raised; see M7 |
| 8 | "Our bare metal" (brief) | Follows Ex 4: customers own the hardware | Correct; Ex 4 overrides |
| 9 | Exchange 5 email: dangerous repairs need "a more thorough recovery review"; privacy boundary named "raw logs and secrets" | FR-21 now has "a recovery plan reviewed before the repair runs"; PRIV-1 covers all private data | Aligned in substance; the broader privacy wording is stricter than the email. Make sure the walkthrough uses the PRD's wording |

### Security and privacy review

Source: `/home/amine/nightshift/_bmad-output/planning-artifacts/prds/prd-nightshift-2026-10-28/review-after-security.md` — 2 critical, 11 high, 11 medium, 5 low (29 findings).

**Verdict.** The PRD now states the right principles: log text is evidence, approvals are single-use and bound to the repair, a compromised agent cannot approve its own repairs, releases are signed, and data leaves only through approved fields. But it still does not say **where** these controls are enforced or **who holds the rights to act**. As written, the Nightshift agent can hold the write rights it is told not to misuse. The central systems that issue approvals, ticks and policies (portal, Slack integration, Quornex Fleet) are trusted without any check inside the cluster. Two critical and eleven high findings remain. All of them can be fixed with requirement-level wording; none needs a redesign of the product.

**What improved and should be kept:**

- The Approval definition binds an approval to "the exact repair, target, catalogue version and evidence shown" and makes it single-use.
- SEC-1 separates rule-based facts from the AI's wording, treats model output as untrusted, and needs more than one signal for an automatic repair.
- SEC-2 has four parts, and its approvals part says that "Enforcement sits outside the agent".
- SEC-3 separates reading from acting and lists allowed actions per machine.
- SEC-5 signs releases, the catalogue and model weights. SEC-7 protects the settings and enforces alert-only mode outside the agent.
- PRIV-2 covers every channel. PRIV-7 keeps honest wording about the planted-secret tests.
- FR-47 says that "An emergency alone grants no permission."
- FR-44 says no AI-written code reaches production unless a person has read it.

**Requirement-level changes, in brief:**

1. Add **SEC-8** (separate executor, read-only agent) and **SEC-9** (authorisations signed by the person and verified in the cluster; Fleet commands limited to a closed list). These fix both critical findings and support most of the high ones.
2. Widen SEC-1 to all untrusted inputs. Define independent signals by trust domain. Render approval requests only from structured, signed data.
3. Define approver roles, MFA and step-up authentication, separation of duties, and approval per cluster for fleet events.
4. Add an exfiltration row to SEC-2 (egress gateway outside the agent) and a management-agent compromise case.
5. Fix code-fix distribution (consent before fleet-wide reuse; customer-specific entries out of the shared release), deployment (pull request with pinned hash), test-environment isolation, and engineer access as a listed channel.
6. FR-47: version floor and revocation, update type in the signed metadata, enforcement components never "routine", signing keys in an HSM with threshold signing.
7. Add PRIV-8 with the hosted-model provider's minimum terms and a data level chosen by each customer.
8. Make PRIV-3, PRIV-4, FR-48, SEC-3 and SEC-4 testable with published inventories, field lists and test corpora.

## Findings by severity

### Critical (4)

**[Adversarial]** — C-1. FR-41 tuning is a change to customer production with no authorisation, even in alert-only mode (§ FR-41; Glossary "Customer production", "Alert-only mode", "Prohibited action"; FR-17; FR-21)

**Text:** FR-41: "Nightshift may tune the cluster's settings only within the limits set by the tested release; anything bigger goes to Orvex as a proposal." Glossary: "A change that can affect customer production needs the customer's advance permission (a tick in the settings checklist) or the customer's approval per action." Alert-only mode: "never executes **repairs**".

**Problem:** tuning is not called a repair, is not said to come from the repair catalogue, and is not linked to FR-21, ticks, modes or FR-34. As written it bypasses every authorisation rule. Alert-only mode only forbids *repairs*, so tuning still runs there. Larger changes go "to Orvex as a proposal", not to the customer, so Orvex alone can approve a larger change to the customer's cluster. FR-17 and the "Prohibited action" definition ("improvised repairs that are not in the repair catalogue") contradict FR-41 unless tuning is in the catalogue, and the PRD never says it is.

**Failure scenario:** a customer in alert-only mode runs a latency-sensitive database. Nightshift "tunes" its CPU limits or HPA minimum replicas within the release limits at 3 AM. Checkout latency doubles. Nothing in FR-34 records who permitted it, and SM-4 cannot count it because no approval record was expected. Repeated small changes, each within the limits, add up to a large one, and FR-30 limits only *repairs*.

Fix: define tuning as a class of repair catalogue entries with risk levels, subject to FR-21, ticks, modes, FR-30 and FR-34. Route "anything bigger" to the customer as an approval request, with Orvex technical approval on top, not to Orvex alone. Add a cumulative-drift limit per setting.

**[Adversarial]** — C-2. SEC-2 contains approvals but not execution or egress: a compromised agent can change production and exfiltrate data without forging anything (§ SEC-2, SEC-3, SEC-4, FR-25, PRIV-4, FR-35, SM-4)

**Text:** SEC-2 "Approvals: The agent cannot approve its own repairs, forge approvals or change its permissions. Enforcement sits outside the agent." FR-25 "Nightshift applies the repair". 3.2 "Nightshift still has permitted diagnostic access". FR-35 "the agent can add to it but cannot change or delete entries."

**Problem:** SEC-3 moves only *hardware* credentials out of the agent. The Kubernetes credentials needed to drain, restart, delete pods, clean node disks (hostPath, which in practice means node root) and read customer databases remain, by implication, in the agent that "applies the repair". A compromised agent does not need to forge an approval; it calls the Kubernetes API directly. Likewise, PRIV-4's outbound check and the PRIV-3 allowlists have no required location, so if they run inside the agent, a compromised agent skips them. FR-35 also lets the agent *add* entries, so it can write plausible execution records. SM-4 compares those with approval records, so the comparison relies on what the attacker wrote. The SEC-2 table has no "customer data / egress" row at all.

**Failure scenario:** a log-parsing bug gives an attacker code execution in the agent. The attacker uses the agent's service account to cordon and drain every node (outage), reads customer tables through "permitted diagnostic access", and sends them out in hosted-model calls disguised as sanitised prompts. No approval was forged, so SEC-2 is met on paper.

Fix: add SEC-2 rows: (a) **Execution:** mutating credentials live in a separate executor outside the agent. The executor accepts only signed catalogue actions, each with a verifiable authorisation token from the approval service, and the agent itself has read-only RBAC. (b) **Egress:** the PRIV-3 allowlist and the PRIV-4 check are enforced at a network egress point outside the agent, and the agent has no other route out. (c) **Records:** approval records come only from the approval service, never from the agent, and SM-4 is computed from executor logs, approval-service logs and Kubernetes or BMC audit logs, not from agent-written records.

**[Security]** — SEC-R2-01. The rights to act are not separated from the agent that reads untrusted data (§ SEC-1, SEC-2 (Approvals row), SEC-4, FR-21, FR-22, Glossary "Risk level")

**Text:** SEC-1: "A separate, rule-based check, not the AI, authorises execution". SEC-2: "The agent cannot approve its own repairs, forge approvals or change its permissions. Enforcement sits outside the agent." SEC-4: "Nightshift holds only the rights it needs". Glossary: "The same action can have different risk levels depending on its conditions".

**Problem:** The PRD moves the **approval** check outside the agent, but nothing says that the **rights to change things** (Kubernetes write rights, node drain, restarts, cleanup, deployments) sit outside the agent. It also does not say where the rule-based check, the precondition re-check (FR-22) and the risk-condition evaluation run. If they run in the agent process, which also reads logs and talks to the model, then "enforcement outside the agent" means nothing in practice.

**Attack:** An attacker gets code execution in the workload-cluster agent, for example through a parser bug triggered by a crafted log line, or through a poisoned dependency. The agent's service account can patch Deployments and delete pods. The attacker never asks for an approval: they use the service account directly to scale checkout to zero, or to roll a Deployment to an attacker-chosen image. A subtler version: the agent evaluates "healthy replicas can carry the traffic" itself and reports it true, so a risky "restart the only replica" is classed as a safe "restart one replica" and runs automatically with no human involved.

Fix: Add **SEC-8: Separate executor.**
- (a) The Nightshift agent (collection, analysis, model calls) holds read-only rights and no write rights to customer production.
- (b) All changes go through a separate in-cluster executor. It accepts only a signed catalogue action ID plus a verifiable authorisation (a tick, an approval or a policy; see SEC-R2-02). It evaluates the preconditions and the conditions that set the risk level itself, from data it reads directly from the Kubernetes API or the hardware component, not from the agent.
- (c) The executor runs no model and does not parse log text.
- (d) In alert-only mode the executor holds no write rights at all.
- (e) Acceptance test: with the agent fully compromised (simulated by giving an attacker the agent's credentials), no write to customer production succeeds without a valid authorisation. SM-4 measures this.

**[Security]** — SEC-R2-02. Approvals, ticks and policies can be forged centrally, and Fleet's powers are unbounded (§ Glossary "Approval", "Advance permission", "Maintenance policy"; FR-14, FR-21, FR-32, FR-47, SEC-5, SEC-7)

**Text:** "Approval: a yes given by an authenticated person at the time, for one repair, through Slack or the Quornex portal". FR-32: "Quornex Fleet recognises the shared problem, stops the update immediately, and coordinates recovery across all the affected clusters." SEC-5: "so a compromised Quornex Fleet or release pipeline cannot push unapproved changes".

**Problem:** SEC-5 protects **releases and the catalogue** against a compromised Fleet. It does not protect **approvals, ticks, delegations, last-resort permissions, maintenance policies or rollback policies**. All of these are created in the Quornex portal or Slack and pass through Orvex's central, multi-tenant systems before they reach a cluster. SEC-2 only considers a compromised **agent**. The PRD never considers a compromised portal, Slack integration or Fleet, nor any limit on what Fleet may order clusters to do.

**Attack:** An attacker compromises the portal backend or the Slack app's signing secret, or an Orvex insider does. They write "ticked: restart only replica; last-resort: on" into the settings of 10,000 clusters, or mint approval records for a dangerous repair on chosen customers. Each cluster sees a well-formed authorisation from its trusted control plane and acts. A second path is FR-32's "coordinate recovery" plus a rollback tool "that must still work even if the bad update broke the normal update path". Together they give Fleet a break-glass channel into every cluster, with no requirement that its orders be checked in the cluster.

Fix: Add **SEC-9: Authorisations are verifiable in the cluster.**
- (a) Every tick, approval, delegation, last-resort permission and maintenance or rollback policy is signed by the approving person's own credential, for example a WebAuthn or passkey assertion over a hash of the exact repair, target, catalogue version, evidence and expiry. Orvex technical approvals are signed by the engineer's individual key.
- (b) The in-cluster executor verifies the signature, the approver's role for that customer (from a customer-administered roster whose root of trust is set at installation) and single use, before acting.
- (c) Neither Fleet, the portal nor the Slack integration can produce a valid authorisation on its own.
- (d) State Fleet's allowed commands to clusters as a closed list (liveness, pause rollout, signed release or catalogue delivery, SEC-6 switch-off). The break-glass rollback path accepts only signed releases under a customer-signed rollback policy.
- (e) Add a threat case to SEC-2: "Quornex Fleet, the portal or the Slack integration is compromised."

### High (36)

**[Strategic coherence]** — "Harmful repair" is never defined, although a primary metric depends on it (§ Vision, SM-3, FR-36, FR-28)

The Vision's third proof point is "every harmful repair is counted and reviewed", and SM-3 counts harmful repairs "separately from repairs that did not work". The Glossary has no entry for the term. SM-2 ("restore health without causing another problem") and FR-28 ("makes things worse") each describe something close to it, and nothing says where one ends and another begins. Without a definition, SM-3 cannot be measured, and the failure-injection tests (Section 9) cannot label outcomes consistently.

Fix: add a Glossary entry, for example "a repair whose effect worsens service health, data integrity, security or access beyond the state before it ran, whether or not it was rolled back". State that SM-2 failures and SM-3 harms are mutually exclusive, and that FR-28 is the runtime response to a harmful repair.

**[Done-ness clarity]** — FR-41's tuning sits outside the authorisation model (§ FR-41, Glossary "Customer production", SM-4)

"Nightshift may tune the cluster's settings only within the limits set by the tested release" says nothing about ticks, approval, risk level, alert-only mode or recording. The Glossary's "Customer production" says any change that "can affect the customer's live experience or service" needs a tick or an approval, and SM-4 holds unapproved changes at 0. As written, an engineer cannot tell whether tuning goes through FR-21, or whether it may run in alert-only mode.

Fix: state that every tuning action is a repair catalogue entry with a risk level, subject to FR-21 and FR-33, and that alert-only mode disables it. Or, if tuning needs its own permission, make it a settings tick covered by SEC-7.

**[Shape fit]** — No journey shows the customer configuring permissions (§ UJ-3, UJ-4, glossary "Advance permission", FR-21, FR-22, FR-24, SEC-7, FR-43, FR-7)

UJ-3 and UJ-4 both rely on a tick made off-screen ("the customer has ticked it in their settings", "She had permitted this rollback in advance by ticking it"). The settings surface carries a lot of logic:
- alert-only versus approval-enabled mode;
- ticking repairs that show their risk levels, with dangerous ones not tickable;
- re-ticking after a repair version changes;
- the last-resort tick;
- the scope and revocation of delegation to Orvex support;
- the read scope;
- the two consents for code fixes;
- acknowledging limited visibility at installation.

The wireframes come next and have no journey to design this surface from.

Fix: add a UJ with a named business owner who sets up the cluster, including one re-tick prompt after a release changes a repair.

**[Adversarial]** — H-1. Authorisation is not re-checked at execution time: revocation races produce unapproved changes (§ FR-22 third bullet; FR-21 (delegation "can revoke it at any time"); SEC-6; SEC-7)

**Text:** "Right before every run, Nightshift re-checks the repair's **safety preconditions** from the repair catalogue. If they still hold, it runs."

**Problem:** the run-time re-check covers safety preconditions only. It does not cover authorisation state: tick still present, mode still approval-enabled, delegation still in force, catalogue entry not switched off (SEC-6), last-resort still ticked, approver still authorised.

**Failure scenario:** at 02:00 Orvex support, under delegation, approves a risky restart, and Josh gives Orvex technical approval. The repair waits in the coordinator queue (FR-29) behind a drain. At 02:05 the customer revokes the delegation, or switches to alert-only mode, because they are handling it themselves. At 02:10 the restart runs: an unapproved change to customer production that the customer explicitly withdrew.

Fix: FR-22: "Right before every run, the enforcement point re-checks authorisation (mode, tick and tick version, delegation, approval validity, last-resort, kill switch) together with the safety preconditions; any change cancels the run." Make it a testable consequence.

**[Adversarial]** — H-2. Local autonomy contradicts enforcement outside the agent (§ 5.7, NFR-5, Vision ("Each cluster looks after itself when central coordination is unavailable") versus SEC-2 ("Enforcement sits outside the agent") and SEC-7 ("alert-only mode is enforced outside the Nightshift agent"))

**Problem:** if the enforcement point (ticks, mode, approval validity) is central, a disconnected cluster cannot run even ticked safe repairs, which breaks NFR-5. If it is local, it is inside the cluster the agent controls, so "outside the agent" needs a definition. The PRD does not say which, and the answer changes the architecture: a local policy enforcer, cached signed policy, revocation latency and the offline audit buffer.

**Failure scenario:** a network split cuts a cluster off from Fleet and the portal. Either (a) a disk fills and the ticked cleanup does not run, because the external enforcer is unreachable, or (b) the agent enforces from its own cache, a customer's untick made during the split is never seen, and the repair runs after permission was withdrawn.

Fix: state that the enforcement point is a separate in-cluster component outside the agent's trust boundary, enforcing a signed policy snapshot. Define its behaviour when offline: ticked safe repairs run; nothing that needs a fresh approval runs; revocations take effect on reconnect, with a stated maximum staleness. State that offline audit records are buffered by that component, not by the agent.

**[Adversarial]** — H-3. Delegation plus Orvex technical approval means Orvex alone approves risky changes, including its own platform changes (§ FR-21 (delegation), Glossary "Orvex technical approval" ("so the customer cannot damage their own app"), FR-47, Q1)

**Problem:** for a risky repair, the customer's approval can come from Orvex support and the technical approval from the Orvex Nightshift team, so both "keys" belong to Orvex. Nothing requires two different people or prevents one person from holding both roles. Under FR-47 a delegated customer approval also lets Orvex approve changes to Orvex's own software in the customer's production, which is a conflict of interest that the "customer's permissions" framing was meant to prevent.

**Failure scenario:** one Orvex engineer with both support and Nightshift-team roles clicks both approvals for a risky restart of a single-replica service at 3 AM. The customer learns of it from the after-the-fact notification.

Fix: require that the delegated approver and the technical approver are different people with separate roles, enforced by the approval service. State whether delegation can cover FR-47 platform changes; recommend that it cannot by default. Add delegation-scoped approvals to FR-34.

**[Adversarial]** — H-4. Individually safe repairs can run concurrently on different targets and invalidate each other's safety preconditions (§ FR-29 ("on the same target"), Glossary risk table ("Restart an affected replica, when the healthy replicas can carry the traffic ... Safe"), FR-30)

**Problem:** the coordinator serialises only per target. Two safe repairs on *different* replicas or nodes of the same service each check "healthy replicas can carry the traffic" at the same moment, both pass, and together remove too much capacity. FR-30's "rate limits ... based on the impact on workloads" and "checks for conflicting changes" have no definition of impact, scope or threshold, so they cannot be tested.

**Failure scenario:** memory creep on 3 checkout replicas. The rule fires for replicas A and B within the same second. Each restart sees 2 healthy peers and is classified safe. Both run, one replica carries all checkout traffic and falls over. No approval was ever requested because each repair was safe and ticked.

Fix: coordinate at the level of the *safety domain* (the service or PodDisruptionBudget, the node pool), not the target. Re-evaluate preconditions under a lock that covers that domain. Define FR-30's impact measure (for example, capacity removed per service per window) as a testable limit.

**[Adversarial]** — H-5. Stale or failed monitoring still feeds safety-precondition checks (§ FR-4 ("When these checks fail, Nightshift opens a monitoring failure case"), FR-22, Glossary "Safe repair")

**Problem:** FR-4 opens a case but says nothing about what happens to automatic repairs while Nightshift's own data is stale. The checks "healthy replicas can carry the traffic" and "the runtime confirms removal is safe" are only as good as data freshness.

**Failure scenario:** Prometheus stalls at 02:00. At 02:20 a ticked safe restart checks replica health from 02:00 data, which still shows 3 healthy replicas when in fact 2 crashed at 02:10. It restarts the last healthy one.

Fix: add a testable consequence to FR-4 and FR-22: every precondition carries a maximum data age; past it, the precondition fails closed. While a monitoring failure case is open in a cluster, automatic repairs there are suspended.

**[Adversarial]** — H-6. Silent-node mitigation without fencing causes split-brain data corruption (§ FR-20 "Report uncertainty": "it may run only a mitigation that is valid whatever the cause"; FR-3; FR-7 "Node goes silent without out-of-band management")

**Problem:** the standard mitigation for a silent node, rescheduling its pods elsewhere, is *not* valid whatever the cause. In a network partition the node is alive and its stateful pods are still writing. Without fencing (power-off through the BMC, which is dangerous) or a storage-level lock, moving a StatefulSet pod or a ReadWriteOnce volume creates two writers. In limited-visibility mode fencing is impossible by definition.

**Failure scenario:** a top-of-rack switch fault isolates node C, which runs the primary of a Quornex-managed database. Nightshift treats rescheduling as cause-agnostic, force-detaches the volume and starts a new primary on node D. Node C is still serving local clients. The data diverges.

Fix: state that any mitigation that moves stateful workloads off a silent node requires confirmed fencing, and is dangerous otherwise. In limited-visibility mode, stateful failover from a silent node is never automatic. Add this as a must-have entry in the failure catalogue.

**[Adversarial]** — H-7. Code-fix review path contradicts FR-39, FR-40 and NFR-3 (§ FR-44 steps 4 to 6, FR-42 step 3, FR-39, FR-40, NFR-3)

**Text:** FR-44 "An Orvex engineer reviews ... **The engineer** approves or rejects the patch. An approved patch enters the repair catalogue". FR-39 "A new or changed repair catalogue entry needs **two reviewers**." FR-40 "never as one-off changes to single clusters". NFR-3 "differences between customers are only their permissions and settings".

**Problem:** a customer-specific code-fix entry is by definition a one-off change to one customer's clusters, delivered outside the "tested release", so it breaks FR-40 and NFR-3. It is approved by one engineer, which breaks FR-39. The PRD also never says what risk level an AI-written code deployment can have. If Orvex classifies one as "safe", a customer who ticks it gets AI-written code deployed to production automatically.

**Failure scenario:** one engineer approves a patch whose regression tests pass but whose fix changes the rounding in a pricing function. It is marked safe and ticked, deploys automatically at the next occurrence, and silently mis-charges customers.

Fix: apply FR-39's two reviewers to code-fix entries. Add an explicit exception to FR-40 and NFR-3 for customer-specific entries, with their own signing and distribution path (SEC-5). Set a floor of "risky" for any code deployment, so it can never run on a tick alone.

**[Adversarial]** — H-8. A customer's proprietary code can become a fleet-wide catalogue entry for other customers (§ FR-42 step 3 ("as a fleet-wide entry if it is reusable"), FR-38 ("lessons (rules, catalogue entries, fixes)"), PRIV-1, PRIV-6)

**Problem:** a code fix is derived from customer A's source code. Orvex alone decides it is "reusable" and publishes it to the fleet. The patch, together with the code context and test it carries, reaches other customers. Nothing requires customer A's consent, and it breaks the spirit of PRIV-1 and PRIV-6 (code stays in the cluster). It may also break customer A's intellectual-property rights.

**Failure scenario:** a fix to customer A's custom payment-retry module becomes a fleet entry. Customer B, a competitor, sees the entry in their catalogue checklist, including its description and diff.

Fix: a code fix derived from a customer's code is always customer-specific. Promoting it to the fleet requires the originating customer's explicit written consent and an Orvex rewrite that contains none of their code.

**[Adversarial]** — H-9. Orvex unilaterally controls what leaves the cluster and can widen it through a routine update (§ PRIV-3 ("Orvex defines and owns the list of allowed fields, recipients and destinations"), FR-47 routine updates under the maintenance policy, Vision ("only approved, sanitised information" leaves))

**Problem:** "approved" is approved by Orvex alone. A routine Nightshift release can add fields, recipients or destinations, such as a new hosted-model provider or region, and it rolls out under the maintenance policy without the customer seeing that their data boundary changed. For a product sold on *sovereignty*, the customer has no control over its own egress policy.

**Failure scenario:** release 2.5 adds "service name" and "error message template" to the hosted-model allowlist and switches to a model endpoint in another jurisdiction. It deploys under the routine maintenance policy, and the customer's data now leaves under terms they never saw.

Fix: make PRIV-3 lists versioned and visible to the customer. Any widening (new field, recipient, destination, provider or region) needs the customer's explicit consent, like a changed tick (FR-22), and never rides along in a routine update. The customer can choose a stricter list.

**[Adversarial]** — H-10. Code sent to a hosted model contradicts "secrets never leave", and the absolute claim rests on an untested sanitiser (§ Vision ("Raw data and secrets never leave the cluster"), PRIV-2, PRIV-6 ("This is the only exception to PRIV-1"), FR-43, Section 7 (hosted model is the first-version focus), Q16)

**Problem:** (a) Source code commonly contains hard-coded credentials, internal hostnames and customer identifiers. FR-43 sends "the relevant code" raw; nothing applies PRIV-2 or PRIV-4 sanitising to code, so "secrets never leave" is false for every consenting customer. (b) FR-44 step 4 lets an Orvex engineer access customer code remotely, which is a second exception, so "the only exception" is also false. (c) For everything else, the absolute "never" depends on free-text log sanitising that Q16 still lists as *to test*, while Section 7 makes the hosted model the default path for all explanations.

**Failure scenario:** `config.py` in the relevant code holds a Stripe live key. It is sent to the hosted model and stored in the provider's logs.

Fix: require secret scanning and redaction of code before any hosted transfer, with the transfer blocked on a hit. List all exceptions (hosted code transfer, engineer access to the test environment). Restate the Vision claim as a design goal that is tested by PRIV-7, not as a guarantee.

**[Adversarial]** — H-11. One release everywhere (FR-46, NFR-3) contradicts customer-controlled updates (FR-47) (§ FR-46 "Every cluster runs the same tested Nightshift release"; NFR-3; FR-47 "Routine updates run under a maintenance policy the customer has authorised")

**Problem:** if the customer can choose update types and windows, or never authorise a policy, clusters will run different Nightshift, catalogue, OMK and Quornex versions, possibly for a long time. That affects catalogue compatibility, the versions ticks are bound to (FR-22), SEC-6 switch-off across versions, security patching, and the FR-46 canary logic (customer windows decide which clusters can be in the first group).

**Failure scenario:** a customer never authorises a maintenance policy. Their cluster stays on a release with a known sanitiser bug (H-10) and a catalogue entry later found harmful. Their old agent does not recognise the SEC-6 switch-off format.

Fix: pick one: (a) security and safety updates (sanitiser, kill switch, signature roots) are mandatory and outside the customer's policy, stated explicitly, while feature updates are policy-gated; or (b) define a supported version window (N and N-1) and what happens to clusters outside it.

**[Adversarial]** — H-12. A compromised Fleet can still do harm through signed artefacts and orchestration; SEC-5 overclaims (§ SEC-5 ("so a compromised Quornex Fleet or release pipeline cannot push unapproved changes"), FR-32 (Fleet "stops the update ... and coordinates recovery"), FR-47 emergency rollback, SEC-6)

**Problem:** signatures prove origin, not freshness or intent. A compromised Fleet can (a) start "emergency rollbacks" to an older, validly signed release with known vulnerabilities (a downgrade attack) on every cluster with a rollback policy, (b) switch off safety-critical catalogue entries fleet-wide (SEC-6), (c) pause all rollouts, and (d) if the portal or approval service runs in Fleet, which the PRD does not exclude, forge approvals. None of these needs an unsigned artefact.

**Failure scenario:** an attacker in Fleet declares a "correlated failure" on 2,000 clusters and rolls them back to v2.1, which has a known RBAC escalation. Every step uses signed artefacts and authorised rollback policies.

Fix: add anti-rollback (a minimum allowed version per cluster) and signed, time-limited rollback and kill-switch commands from a separate signing authority. State that the approval service is isolated from Fleet. Reword SEC-5 to what signatures actually guarantee.

**[Adversarial]** — H-13. The staffing estimate that carries the business case is unverified, and the arithmetic leaves out most of the human work (§ SM-8, SM-9, Section 2 ("one on night duty"), FR-21 (risky repairs need Orvex technical approval "each time"), FR-39, FR-44, SM-6, Vision bullet 4)

**Problem:** (a) The 90% "handled automatically" figure is assumed. SM-9 measures something else, "the share that needs Orvex technical approval", which is not the same as "handled automatically": problems escalated to customers or approved only by customers are not automatic but do not need Orvex either. (b) The arithmetic counts only incident handling. It leaves out FR-39 two-reviewer catalogue reviews, review of every fleet lesson, FR-44 code-fix reviews, SM-6 labelling of every alert, FR-21 recovery-plan reviews, and the fact that *every* risky repair, ticked or not, needs Orvex approval each time. (c) At the base case one night engineer is already 100% loaded (8.3 hours of work in an 8-hour shift), and during a UJ-5 fleet incident every other approval queues behind them. Seats for 24/7 rotation, holidays and day shifts are not derived.

**Failure scenario:** a bad night (500 problems, 17 hours of work) coincides with a 300-cluster incident. The one engineer is busy for 2 hours. Risky repairs across the fleet wait, last-resort conditions fire unattended, and the "15 engineers" claim fails on day one.

Fix: model human load as the sum of all human-gated activities in the PRD, per role. Derive seats from shift coverage. Make "approval latency at P95 per risky request" a success metric. Present 15 engineers as a hypothesis with its sensitivity range, not as an estimate.

**[Adversarial]** — H-14. Rollback, the flagship repair, has no risk level and no handling of data migrations (§ UJ-2, UJ-4, UJ-5, FR-32, FR-47; 3.2 non-goal (never "modify ... databases"))

**Problem:** rollback is the repair the journeys rely on, but its risk level is never stated, and the risk-level table does not include it. A rollback across a forward-only schema migration either corrupts data (the old code writes in the old format to the new schema) or needs a down-migration, which modifies a database and is a prohibited action. FR-47 emergency rollbacks run "without fresh approval" whenever "safety conditions pass", and those conditions are undefined.

**Failure scenario:** checkout v42 adds a non-null column. UJ-4's pre-ticked rollback to v41 runs at 2:20 AM, inserts fail, and orders are lost, while the morning summary says "Checkout recovered".

Fix: add rollback to the risk-level table with its conditions: no schema or data-format change between versions means safe or risky, and otherwise dangerous or not permitted. Make "no irreversible migration in the diff" a mandatory safety precondition of every rollback catalogue entry, for both application and platform rollbacks.

**[Adversarial]** — H-15. Deferring "which hosted models and regions are trusted" (Q6) is unsafe for the architecture (§ Section 10 Q6 and the triage ("none of the remaining items blocks UX or architecture"); Section 7 (hosted model is the first-version focus); Vision ("sovereign cloud"))

**Problem:** the first version's main AI path is a hosted model, yet whether it may be a US-jurisdiction provider, an EU-hosted provider or a self-hosted Orvex service decides the architecture: endpoints, egress control, data residency, the cost model and contracts. It also decides the core sovereignty promise. Q1 (who approves OMK and Quornex changes) and Q2 (whether Orvex technical approval fits Danny's model) likewise shape the approval UX flows, so the triage claim is wrong for them too.

**Failure scenario:** the architecture and cost model are built on a US hyperscaler model API. Danny later answers "EU-sovereign only", and the cost model, latency figures and egress design have to be redone after hand-in.

Fix: make a working assumption now, for example "hosted = EU-jurisdiction provider with zero retention, or Orvex-operated shared GPU", label it a design assumption, and have the cost model show the alternative as a sensitivity case.

**[Adversarial]** — H-16. No validation that the BMC endpoint belongs to the node it is said to manage (§ FR-7 (installation validates "credentials, power status and hardware health reporting"), SEC-3 ("allowed actions are listed per machine"), Glossary "Customer hardware" ("may be badly configured"))

**Problem:** installation checks that each BMC answers, not that BMC X is node Y. With customer hardware the PRD itself expects to be badly configured, a swapped inventory entry is likely. The approver sees "power-cycle node-7", while the action goes to node-3's BMC. The allowlist "per machine" applies the wrong mapping faithfully.

**Failure scenario:** node-7 goes silent and a dangerous power cycle is approved. The BMC mapped to node-7 is actually node-3, the healthy database primary. Power-cycling it causes an outage and possible data loss, and node-7 stays down.

Fix: FR-7 consequence: installation proves the identity binding between node and BMC (serial, system UUID or MAC match, or a controlled LED or identity test), and Nightshift re-verifies the binding right before any BMC action. A mismatch blocks the action.

**[Judge]** — H1. A compromised agent's blast radius inside its own cluster is not covered (§ SEC-2, SEC-4)

SEC-2's table covers other clusters, audit records, approvals and hardware credentials, but not the cluster the agent runs in. If the Nightshift agent holds standing Kubernetes write rights (drain, restart, scale, roll back) and read access to Secrets, then a compromised agent can do all of that directly. "Enforcement sits outside the agent" cannot work if the agent holds the credentials that carry out repairs. This is exactly the brief's question: "How do you stop … a compromised agent from doing harm?"

Fix: add SEC-8. The observing and reasoning agent has read-only rights and no access to Secrets by default. Repairs run through a separate executor that receives a short-lived credential for one catalogue action on one target, only after the rule-based policy check and approval verification, which sit outside the agent (for example an admission or policy controller). List what a compromised agent can still do (read diagnostics, send false evidence, refuse to act) and how each is limited or detected.

**[Judge]** — H2. The approval model conflicts with the 99.9% availability target, and the PRD does not say so (§ FR-21, FR-23, FR-24, SM-7)

An unticked risky repair needs the customer (a non-expert business owner, possibly asleep) and an Orvex engineer at the same moment. The last-resort condition covers only failure *predicted* within 30 minutes, not failure already in progress (UJ-2: checkout is down). One unanswered night uses up the 43-minute monthly budget. Danny said "safe repairs should be automatic" and wants it "as close to self-managing as possible".

Fix: add a requirement or metric for approval latency (time from request to decision, by hour of day). Extend the last-resort condition to cover outages in progress for ticked repairs. State explicitly in Section 10 that the availability target depends on approval latency and on how many risky repairs customers tick, and make it something to test.

**[Judge]** — H3. The default mode and the default checklist are undefined, so it is unclear whether safe repairs are automatic out of the box (§ Glossary, FR-21)

Danny (Exchange 4): "Safe repairs should be automatic, while risky changes require approval." The PRD makes safe repairs automatic only if ticked. It never says whether a new customer starts in alert-only or approval-enabled mode, or with an empty or pre-ticked checklist. If the checklist starts empty, a non-expert owner is asked to approve disk cleanups at 3 AM. That defeats the persona ("chose Quornex so they would not need DevOps staff") and adds load to SM-8 and SM-9.

Fix: state the defaults. Proposal: approval-enabled mode, with safe repairs pre-ticked and the customer able to untick them; risky repairs unticked. Record it as a proposal and list it among Danny's open questions.

**[Judge]** — H4. Customer approval of Orvex's own platform changes departs from "fully managed by us" and "the same tested release everywhere" (§ FR-47, Glossary "Customer production", NFR-3)

Because "customer production" covers any layer, repairs and updates to Quornex's managed databases and to OMK need the customer's policy or approval. If a customer never authorises a maintenance policy, versions drift apart, which contradicts NFR-3 and the brief's ground rule. Public clouds do not ask before failing over a managed database. The PRD marks this as pending Danny (Exchange 5 Q2), which is honest, but it does not acknowledge the conflict with NFR-3 or offer a fallback.

Fix: name the conflict in FR-47. Propose a contract-level default: Orvex has authority over its own platform components within a maintenance window agreed in the contract, with notice and the right to defer for a bounded period (for example N days), after which the update is mandatory. Per-action customer approval would remain only for changes that touch customer apps or data.

**[Judge]** — H5. Requiring Orvex technical approval for every risky repair, even when ticked, is the largest cost and latency driver, and the PRD does not present it as a trade-off (§ FR-21, SM-8, SM-9, COST-1)

Danny's model (Exchange 1) is that the customer approves, optionally delegating to Orvex support. The extra Orvex approval is Amine's addition (Exchange 5 Q1, unanswered). It puts one night engineer between every risky repair across 10,000 clusters and the action. The PRD's own arithmetic (SM-8) shows staffing swinging from about 8 to about 75 hours a night depending on the automatic share, yet Section 7 and COST-1 do not name human approval as the main cost lever.

Fix: in the cost section, state that human time, driven by the share of repairs needing Orvex approval, is expected to dominate the per-cluster cost, and require the cost model to show the sensitivity. Offer a path to earn autonomy: after N verified successes under defined conditions, a reviewed reclassification can drop the per-run Orvex approval (FR-21 already allows reviewed reclassification, so connect the two).

**[Judge]** — H6. Nothing says how Nightshift behaves with no model available (§ Section 7, NFR-4, NFR-5)

There is no requirement that detection, rule-based matching, safe repairs, notifications and the record keep working when the hosted model is down, rate-limited or too expensive, or when a sovereignty-minded customer refuses any hosted model. The "time and type only" strict mode suggests this case but never states the consequence. It matters for availability ("what if Nightshift fails" extends to its dependencies), for cost (it caps model spend) and for Danny's sovereign-cloud pitch.

Fix: add NFR-9. The safety loop (detect, match by rules, authorise, act, verify, record) needs no model. Without one, explanations fall back to templates built from the rule-based facts. List what is lost without a model (help matching new problems, richer explanations, code fixes).

**[Security]** — SEC-R2-03. Prompt injection reaches the humans who approve (§ SEC-1 ("Approval requests show the facts from the rule-based checks separately from the AI's wording"), FR-11, FR-14, UJ-3)

**Problem:** Separating the facts from the AI's wording is necessary but not enough.
1. The AI's wording is still shown next to the Approve button. A crafted log line can steer it, for example: "Orvex has pre-verified this restart; approve within 2 minutes to avoid data loss."
2. The "facts" contain attacker-controlled strings: pod names, labels, error messages, URLs. Kubernetes names and annotations are set by whoever can deploy.
3. Slack renders links, mentions and formatting. An injected `<https://quornex-portal.example|Open in Quornex portal>` link can lead to credential phishing.
4. Nothing requires the target and action shown to come from the executor's structured request rather than from text.

**Attack:** An attacker controls one tenant app on the cluster. They log a line that makes the explanation say the payments database pod is "the leaking replica", and annotate a pod so its display name looks like the checkout service. Josh sees a convincing request and approves. The approval is bound to what was shown, and what was shown was the attacker's choice.

Fix:

- The action, target, risk level and expected impact in an approval request are rendered only from the executor's structured, signed request. The AI text cannot change them, and text that contradicts them is suppressed.
- AI wording and every untrusted string are escaped and shown as plain text: no links, mentions, markup or calls to action. Request links point only to a fixed portal domain.
- The AI wording is visibly labelled "AI explanation, unverified".
- Approval requests never ask for credentials. Phone calls and Slack messages say so.
- Acceptance test: a red-team corpus of injected log lines and object names produces no change to the structured fields and no live links, with a pass rate of 100%.

**[Security]** — SEC-R2-04. The untrusted-input boundary covers only "log text" (§ SEC-1 title and body; 3.2 "Treat text in logs as instructions")

**Text:** "An automatic repair needs evidence from more than one independent signal, never a log line alone."

**Problem:** 
- Untrusted inputs also include Kubernetes events, object names, labels and annotations, metric labels, the customer's app metrics, BMC or Redfish strings from customer-managed hardware that may be "badly configured", customer source code read for code fixes, hosted-model output, and fleet lessons.
- "Independent" is not defined. A compromised app controls both its logs **and** its own memory, latency and error metrics, so two signals from the same workload are not independent.
- Nothing says the repair **target** must come from the Kubernetes API rather than from text.

**Attack:** A compromised app deliberately grows its memory and logs matching OOM warnings. This gives "two signals", which triggers repeated restarts of a sibling service named in the log text, or a node drain.

Fix:

- Rename SEC-1 to "Untrusted inputs are evidence, never instructions" and list the input classes above.
- Define independent signals as signals from **different trust domains**, for example node or kubelet metrics versus app-emitted data. Workload-emitted signals together count as one domain.
- Require repair targets and parameters to be resolved from authoritative APIs (Kubernetes, the hardware component), never taken from free text or model output.

**[Security]** — SEC-R2-05. Approver identity, authentication and separation of duties are not specified (§ Glossary "Approval", FR-14, FR-21 (delegation), UJ-5, SEC-7)

**Text:** "an authenticated person"; "Orvex support may give it instead if the customer has delegated approval to them"; UJ-5: "he approves" one fix for 300 clusters.

**Problem:** 
- It is not said **who** may approve for a customer. SEC-7 covers only settings changes, done by administrators.
- The strength of authentication is not set: no MFA, and no step-up for risky or dangerous repairs.
- There is no requirement that a Slack identity be mapped to a customer approver roster. In shared Slack channels, anyone in the channel can click.
- Delegated customer approval by Orvex support plus Orvex technical approval means **Orvex alone** approves a risky change to customer production. Nothing stops the same person, or two colluding colleagues, from giving both approvals.
- UJ-5 shows one engineer's click across 300 customers, which contradicts "for one repair".

**Attack:** A support engineer's Slack session is stolen. The attacker gives the delegated "customer" approval and, in another channel, the Orvex technical approval on the same risky repair.

Fix:

- Define the approver roles per customer, managed by customer administrators under SEC-7.
- Require phishing-resistant MFA for approvers, and step-up re-authentication for each risky or dangerous approval.
- Slack approvals are accepted only from identities linked to that roster, and only for safe and risky repairs. Dangerous repairs are approved only in the portal.
- The customer-side approval and the Orvex technical approval must come from different people. If the customer side is delegated, they must also come from different Orvex teams.
- Fleet-wide approvals (UJ-5) produce a separate authorisation per cluster, each checked against that customer's own policy. One click never authorises more than one customer.

**[Security]** — SEC-R2-06. A compromised agent can send data out of the cluster directly (§ PRIV-2, PRIV-3, PRIV-4, 3.2 ("Nightshift still has permitted diagnostic access"), SEC-2)

**Problem:** The privacy controls describe what a **well-behaved** agent sends. Nothing says:
- that the outbound sanitiser and the PRIV-4 check run outside the agent;
- that the cluster's network blocks any destination not on the PRIV-3 list;
- what "permitted diagnostic access" to customer databases covers;
- whether the agent can read Kubernetes Secrets.

SEC-2 does not list exfiltration among its four containment areas.

**Attack:** The compromised agent uses its diagnostic database credentials to dump customer tables, then sends them over HTTPS to an attacker host, or hides them inside "sanitised" model calls. The sanitiser it skipped was inside its own process.

Fix:

- Add a fifth SEC-2 row, "Data exfiltration". Outbound traffic from Nightshift components passes through an egress gateway outside the agent that enforces the PRIV-3 destinations, sanitisation and the PRIV-4 check.
- A network policy blocks all other egress.
- Define diagnostic access as metadata and health queries only: no reading of table contents and no reading of Kubernetes Secrets, unless a scoped exception is recorded under FR-33.
- Every byte that leaves is logged at the gateway (PRIV-7 layer 1).

**[Security]** — SEC-R2-07. Code fixes leak customer code through the catalogue and the release (§ FR-42 step 3, Glossary "Customer-specific entry", FR-40, NFR-3)

**Text:** "as a fleet-wide entry if it is reusable, otherwise as a customer-specific entry that only that customer can access or execute". FR-40: "distributed through a controlled release, never as one-off changes to single clusters". NFR-3: "Every cluster runs the same tested Nightshift release".

**Problem:** 
1. A patch written against customer A's proprietary code becomes a **fleet-wide** entry because Orvex judges it "reusable". Customer A has not agreed to share it.
2. If customer-specific entries ship inside the single fleet-wide release, every cluster receives customer A's patch. "Only that customer can access or execute it" is then only a promise that a compromised or curious agent can break.

Fix:

- A code fix derived from a customer's code becomes fleet-wide only with that customer's explicit written consent, after review to remove any of their identifiers or code.
- Customer-specific entries are delivered and stored only in that customer's clusters (signed, and encrypted to those clusters), outside the shared release.
- State this as an explicit exception to FR-40 and NFR-3.

**[Security]** — SEC-R2-08. Code-fix deployment rights, the test environment and secrets in code (§ FR-42 step 5, FR-43, FR-44 steps 2 and 4, PRIV-6, 3.2)

**Text:** "Nightshift deploys the fix if deployment is supported and authorised." "Nightshift creates an isolated test environment within the customer's infrastructure". "An Orvex engineer ... securely accesses the test environment". PRIV-6: "This is the only exception to PRIV-1."

**Problem:** 
- (a) Deploying code needs write access to the customer's repository, registry or CI. A compromised agent with that right can push a backdoor into the customer's app.
- (b) Nothing binds the deployed artefact to the reviewed patch, for example by hash.
- (c) The test environment's isolation is undefined: is it fed production data or secrets? Can it reach the internet? AI-written code under test can call out to the internet.
- (d) The engineer's access is a new way **into** customer infrastructure and a new way for data to leave (a human reading code). It is not in the PRIV-2 channel list, and PRIV-6's "only exception" is therefore wrong.
- (e) Code sent to a hosted model may contain hard-coded secrets, which contradicts PRIV-2 "secrets never leave".
- (f) A patch can contain a database migration that modifies records, which is a prohibited action reached indirectly.

Fix:

- Code fixes are delivered as a pull request or change request in the customer's own pipeline. Nightshift never holds push or deploy rights to app code.
- The approved catalogue entry pins the patch hash, and the executor deploys only that hash.
- The test environment uses synthetic or customer-approved data, has no production credentials and no egress except the model endpoint, and is destroyed after use.
- Engineer access is just-in-time, per patch, time-limited, recorded in a session log the customer can see, and listed as a PRIV-2 channel.
- A secret scan and redaction run before any code goes to a hosted model.
- Patches that touch schemas, migrations or data-deletion paths are rejected as prohibited actions.

**[Security]** — SEC-R2-09. Platform updates and rollbacks: downgrade, key custody, update classification (§ FR-47, FR-32, FR-46, SEC-5, Glossary "Maintenance policy")

**Text:** "Routine updates run under a maintenance policy the customer has authorised, covering the permitted update types". FR-32: "a rollback must still work even if the bad update broke the normal update path ... Whether that needs a separate tool is for the architecture".

**Problem:** 
- (a) A rollback installs an **older signed** release. Without a version floor, an attacker or a compromised Fleet can "roll back" clusters to a validly signed version with a known vulnerability (a downgrade attack).
- (b) Signing-key custody is not stated. If the release pipeline holds the key, "a compromised release pipeline cannot push unapproved changes" is false.
- (c) Orvex alone labels an update's "type". Labelling a risky change as "routine security patch" fits it into the maintenance policy (a confused deputy).
- (d) The Nightshift release also contains the executor and the approval checks, so a routine update can weaken the enforcement itself.

Fix:

- Signing keys are held in an HSM outside Fleet and the pipeline. Signing needs the two FR-39 reviewers (threshold signing).
- Each cluster enforces a minimum version and a list of revoked versions. Rollback only to versions not on that list.
- The update type is part of the signed release metadata, and the cluster checks it against the policy. Releases that change the executor, the authorisation checks or the egress gateway are never "routine": they need customer approval.
- The break-glass rollback path is limited to installing a signed, non-revoked release under a customer-signed rollback policy.

**[Security]** — SEC-R2-10. The hardware component acts on request with no authorisation of its own (§ SEC-3, FR-7, FR-3)

**Text:** "Hardware operations, where needed, go through a separate component whose credentials are limited to specific actions and machines." FR-7: installation "validates access ... including credentials".

**Problem:** 
- Limiting the component to "power-cycle node 7" does not stop a compromised agent from **asking** it to power-cycle node 7 at peak time.
- Who holds the BMC credentials during installation, and whether Orvex staff ever see them, is not stated.
- BMC networks are often flat, and customer hardware may use default BMC passwords. The component then becomes a route to every BMC.
- The risk level of power actions is not stated.

Fix:

- The hardware component performs actions (not reads) only on a verified authorisation (SEC-9) for that machine and action.
- Use separate BMC accounts: a read-only one for monitoring and an operator-role one for actions. Never use administrator accounts.
- Credentials are entered by the customer into an in-cluster secret store. Orvex staff and Fleet never receive them.
- Installation flags default or shared BMC passwords, and BMC traffic is limited to the listed machines.
- Power cycle, power off and firmware actions are dangerous by default.

**[Security]** — SEC-R2-11. FR-41 tuning bypasses the authorisation model (§ FR-41, Glossary "Customer production")

**Text:** "Nightshift may tune the cluster's settings only within the limits set by the tested release"; Glossary: "A change that can affect customer production needs the customer's advance permission ... or the customer's approval per action".

**Problem:** Tuning changes customer production, but FR-41 needs no tick, no approval and no rule-based check, and does not say whether the AI chooses the value. Crafted logs can steer the AI to tune resource limits, autoscaler bounds or timeouts to the most harmful value allowed. SM-4 would not count this as unapproved.

Fix: Tuning actions are repair-catalogue entries with risk levels, chosen and bounded by rule-based checks. They are subject to FR-21, executed by the SEC-8 executor, and recorded under FR-34.

**[Security]** — SEC-R2-12. The management agent's rights and its compromise are not covered (§ FR-6, FR-29 ("Repairs that affect more than one cluster are coordinated by the management agent"), PRIV-5, SEC-2)

**Problem:** SEC-2 contains one compromised **workload** agent. The management agent coordinates every workload cluster of a customer, and runs next to the control cluster's own agent. Its rights in the workload clusters (read, coordinate, act?) are not stated. If it is compromised, every workload cluster of that customer is open.

**Attack:** A crafted log on the control cluster leads to compromise of the management agent. It issues "coordinated" repairs, for example a drain, to all of the customer's workload clusters.

Fix:

- The management agent holds no write rights in workload clusters. It can only propose cross-cluster repairs, which each cluster's executor authorises separately.
- The management agent and the control cluster's own agent run under separate identities.
- Add "management agent compromised" as a SEC-2 case with the same four containment areas.

**[Security]** — SEC-R2-13. The hosted model is the main way data leaves, and its terms are not specified (§ Section 7 (hosted model is the focus for version 1), PRIV-2, open question 6)

**Text:** PRIV-2: "a small message built from approved fields, sanitised with placeholders ... 'Time and type only' is kept for the strictest cases".

**Problem:** 
- "Trusted" is undefined (open Q6). Nothing requires zero retention, no training on customer data, no human review by the provider, a region or jurisdiction that matches the sovereignty promise, or a pinned model version.
- The default sends free text after placeholder substitution, and placeholder sanitisers miss what they do not recognise: internal hostnames, customer names in URLs, tokens in non-standard formats.
- Customers cannot turn the hosted model off for diagnostics; they can only choose "maximum privacy".
- The shared-GPU option does not forbid one customer's context or cache being reused for another customer.

Fix:

- Add PRIV-8 with the minimum provider terms: no retention beyond the request, no training, a named region or jurisdiction, a contractual audit right, and a pinned model version.
- Each customer chooses the data level (off, time and type only, or sanitised fields) with a documented default, and that choice is recorded in the coverage report.
- Free text is sent only from allowlisted fields.
- No context, prompt cache or KV cache is shared between customers on hosted or shared GPUs.

### Medium (49)

**[Decision-readiness]** — The staffing arithmetic is never compared with the one-engineer decision (§ SM-8, FR-23, FR-21)

At the base case, about 8 hours of hands-on work a night falls on one on-duty engineer, which is close to full utilisation with no slack. On a bad night it is about 17 hours. FR-21 also requires "Orvex technical approval each time" a ticked risky repair runs, which adds to that load. The PRD says "the staffing estimate depends heavily on the automatic share" but never says at what point backups are called in or the model fails.

Fix: state the automatic share and the minutes per escalation at which one engineer is enough, and name the backup trigger. For example: "backups join when the queue of pending approvals exceeds N or the predicted human work exceeds X hours."

**[Decision-readiness]** — The code-fix experiment has no rule for keeping or dropping it (§ FR-45)

"Orvex measures the experiment to decide whether code fixes stay" lists seven metrics but gives no threshold, no sample size and no decision owner or date, and Q12 does not list them. Danny asked for this feature as an experiment, so the rule for ending it is the decision that matters.

Fix: add a decision rule, for example "keep if net cost savings > 0 and fix success rate ≥ X% after N patches", or add it to Q12 with an owner.

**[Strategic coherence]** — The hosted-model "focus" is not reconciled with "all three model options" in scope (§ Section 7 versus 3.1)

Section 3.1 puts "all three model options" in the first version, while Section 7 says "Focus for the first version: the hosted model". The architecture cannot tell whether in-cluster GPU diagnosis is built for the first version or only costed. The shared-GPU option raises the same question.

Fix: say in one sentence what "focus" means. For example: "first version builds the hosted path for diagnosis and the in-cluster path for code fixes; shared GPU is costed only."

**[Done-ness clarity]** — Nobody is assigned to decide which services are critical, or who gets phoned (§ FR-9, FR-13, UJ-2)

Criticality is one of the four alert factors in FR-9 and the trigger for phone calls in FR-13 ("an important service such as checkout or a database"). UJ-2 depends on it ("Because checkout is critical, Nightshift calls him"). Nothing says who marks a service critical (the customer in settings, a default for Quornex databases, or Nightshift inferring it) or which person is called, and in what order.

Fix: add an FR stating that the customer designates critical services and a call list in settings, with stated defaults for Quornex-managed services.

**[Done-ness clarity]** — FR-28 has no detection criterion and no exit (§ FR-28)

For "If a repair makes things worse", the PRD gives no measure of "worse". "Stops further automatic repairs on that cluster" has no condition for resuming and no one named to re-enable repairs. "Calls a person" does not say whether that is the customer, the on-duty engineer or both.

Fix: define "worse" against the repair entry's verification (ties to the harmful-repair definition above), and name who is called and who lifts the stop.

**[Done-ness clarity]** — Vague qualifiers remain that the deferral in Q8 does not cover (§ FR-10, FR-13, FR-23, FR-37)

Examples: "if the predicted time or risk changes substantially", "once the risk has decreased enough and stays stable" (FR-10), "strong evidence it is about to fail" (FR-13), "If they do not answer in time" (FR-23) and "well controlled" (FR-37). Q8 defers "timing targets", which arguably covers FR-23 but not the others.

Fix: either widen Q8 to "thresholds for FR-10, FR-13, FR-23, proposed by the architecture", or replace "well controlled" in FR-37 with what FR-39 and FR-40 already require (two reviewers, a tested release).

**[Scope honesty]** — The exception for sending code to a hosted model is not reflected in the Vision's absolute privacy statement, and secrets in code are not addressed (§ Vision, PRIV-2, PRIV-6, FR-43)

The Vision says "Raw data and secrets never leave the cluster", and PRIV-2 repeats it. PRIV-6 calls FR-43 "the only exception to PRIV-1" but not to PRIV-2. Source code is not sanitised data, and code often contains hard-coded credentials. Nothing says whether the code sent goes through PRIV-4's outbound check or a secret scan first. The privacy and security review deliverable will run into this directly.

Fix: qualify the Vision sentence ("…except code a customer explicitly consents to send for a code fix"), and require a secret scan, with blocking, on any code before it is sent.

**[Downstream usability]** — Several component and surface terms are undefined (§ FR-1, FR-2, FR-4, FR-14, Section 11)

- "Nightshift monitoring service" (FR-2) is not one of the Glossary's agent tiers.
- "monitoring failure case" (FR-4) is bolded as if it were a defined term.
- "a Nightshift monitoring page" (FR-14) has no stated relation to the FR-15 dashboards.
- "failure catalogue" (FR-1, Section 11) sits beside the Glossary's incident catalogue and repair catalogue, even though "failure" has a narrower Glossary meaning ("a service failing").

The architecture and the wireframes will each map these differently.

Fix: add Glossary entries, or replace the terms with defined ones. For example, call the Section 11 deliverable "the failure catalogue deliverable (seeds the incident and repair catalogues)".

**[Downstream usability]** — Orvex's side of the last-resort permission has no actor and no screen (§ FR-24, Glossary "Last-resort condition", SEC-7)

FR-24 says the permission is "given in advance by the customer and Orvex" and "replaces Orvex technical approval at that moment". SEC-7 covers only the customer's settings changes. Nothing says who at Orvex grants it, whether per customer or per catalogue entry, or where it is recorded.

Fix: add one sentence naming the Orvex role, the scope (per customer and per repair), and that the grant is recorded under FR-33 and enforced outside the agent (SEC-2).

**[Shape fit]** — Orvex support has no journey, and delegated approval is never exercised (§ Section 2 Users, FR-12, FR-21)

Orvex support is one of three named users, and FR-21 gives delegation real rules: a customer-set scope, revocation at any time, notification of every approval given, and no dangerous repairs. No UJ shows support receiving and answering a delegated request, or being refused one outside its scope.

Fix: add a short UJ, or an edge case on UJ-1 ("the owner has delegated to Orvex support; support approves; the owner is notified").

**[Adversarial]** — M-1. FR-34 cannot record half of the PRD's permission sources, which breaks the SM-4 measurement (§ FR-34 ("who permitted it (ticked, or approved at the time, by whom and when)"), FR-24, FR-47, FR-21 delegation, SEC-7)

**Problem:** the record has no field for the last-resort condition, the maintenance policy, the rollback policy, a delegated approval ("on behalf of"), or Orvex's half of the last-resort advance permission. SEC-7 says only *customer* administrators change the last-resort condition, so who at Orvex grants Orvex's advance permission, and how it is recorded, is undefined. SM-4 compares executions against approval records and "policy decisions", so every legitimate policy-driven change is either counted as unapproved or excluded by hand.

Fix: list all permission sources in FR-34, each with an identifier, version and signer. Define Orvex's last-resort grant: who grants it, its scope, its expiry and how it is recorded.

**[Adversarial]** — M-2. The last-resort condition is untestable and gameable (§ FR-24, FR-23 ("If they do not answer in time"), FR-22 ("There are no timers to manage"))

**Problem:** (a) "Nobody answers" has no timeout, yet FR-22 says there are no timers; the PRD contradicts itself, and FR-24 cannot be tested. (b) Non-answer is not distinguished from non-delivery: a Slack or telephony outage, or a cluster cut off from the network, satisfies "nobody answers", so an outage or attacker that blocks egress turns a request into an execution. (c) It applies only when failure is *predicted* within 30 minutes. Once checkout has already failed, nothing is "predicted", so the worst case, an outage in progress, gets *less* automation than an imminent one.

Fix: define a response timeout per request (shorter than time to impact), require proof of delivery to at least one approver channel before silence counts as no answer, and decide explicitly whether last-resort applies to failures already in progress.

**[Adversarial]** — M-3. A fleet-wide approval (UJ-5) contradicts the definition of a single-use approval (§ UJ-5 ("he approves"), Glossary "Approval" ("single-use and tied to the exact repair, target ..."), FR-32)

**Problem:** does Josh approve once for 300 targets, or 300 times? The first breaks the definition; the second makes UJ-5 impossible at 3 AM. Each customer's own approval (FR-47) is also needed, so the per-customer approval UX at scale is undefined.

Fix: define a batch approval: one signed approval naming an explicit list of targets, each target checked individually against its customer's authorisation at run time (H-1).

**[Adversarial]** — M-4. An approval has no expiry, and binding it to the "evidence shown" is either ignored or causes endless re-asking (§ Glossary "Approval" ("tied to ... evidence shown"), FR-22 ("no timers"))

**Problem:** in a fast-moving incident the evidence changes every scrape, so binding it strictly forces a new request each time and an approver never catches up. With loose binding, an approval clicked six hours late on an old Slack message still executes if the preconditions hold, even though the request said "if you don't answer, we won't change anything".

Fix: give approvals a maximum age, set per risk level, and define which evidence fields are binding (problem ID, target, repair version, severity band) and which may drift.

**[Adversarial]** — M-5. Who coordinates multi-cluster recovery: Fleet or the management agent? (§ FR-29 ("Repairs that affect more than one cluster are coordinated by the management agent, and wait while it is unavailable") versus FR-32 ("Quornex Fleet ... coordinates recovery across all the affected clusters"); Glossary (control cluster "optional"))

**Problem:** the 300 clusters in FR-32 belong to many customers, and the management agent is per customer. A customer with several workload clusters but no control cluster has no management agent, so under FR-29 their multi-cluster repairs wait forever.

Fix: state that Fleet coordinates only Orvex platform rollouts and rollbacks, and management agents coordinate customer-scope repairs. Define the fallback for multi-cluster customers without a control cluster.

**[Adversarial]** — M-6. Coordinator marks both expire (FR-29) and persist (FR-31); NFR-4 overclaims (§ FR-29 ("its marks expire"), FR-31 ("The coordinator's marks ... stay in place"), NFR-4 ("Nightshift failing never harms the customer"))

**Problem:** if the agent is down longer than the mark lifetime, the marks expire mid-repair and Kubernetes or a person acts on a half-drained node. If marks never expire, a dead Nightshift leaves nodes cordoned and capacity reduced indefinitely, which is harm caused by Nightshift failing.

Fix: marks expire only if the owning repair is confirmed dead, with Fleet alerting on orphaned marks. Restate NFR-4 as a testable bound, for example "no Nightshift-held cordon or lock outlives the agent by more than X without a person being notified".

**[Adversarial]** — M-7. Dangerous repairs that disconnect the node cannot be verified or rolled back; the recovery plan may be improvised (§ Glossary "Dangerous repair" ("anything on a live node that could disconnect it from Nightshift"), FR-21 ("plus a recovery plan reviewed before the repair runs"), FR-25, FR-17)

**Problem:** FR-25 assumes Nightshift can check the result and undo the repair. After a NIC or IP change cuts the link, it can do neither. The PRD does not say who writes the "recovery plan" or who reviews it. If the AI writes it, or the engineer writes it ad hoc, it is an improvised repair that FR-17 forbids.

Fix: each dangerous catalogue entry includes a pre-tested recovery plan and an automatic node-local revert (a dead-man switch: revert unless confirmed within N minutes). "Reviewed" means confirmed by the approver against the catalogue, not written at the time.

**[Adversarial]** — M-8. The blast radius of a compromised management agent is not covered (§ SEC-2 (only "the Nightshift agent in one cluster"), FR-6, FR-29, PRIV-5)

**Problem:** the management agent coordinates every workload cluster of a customer, runs cross-cluster investigations and coordinates multi-cluster repairs. If it is compromised, every cluster that customer owns is exposed, and PRIV-5's "only sanitised information" has no enforcement point outside it.

Fix: extend SEC-2 to the management agent. Workload agents accept only signed, policy-checked coordination requests, and sanitising happens at the workload cluster's egress before data reaches the management agent.

**[Adversarial]** — M-9. Diagnostics can change production; "reading is not changing" is not true by the PRD's own definition (§ FR-21 ("Permission to read never means permission to change"), 3.2 ("permitted diagnostic access"), Glossary "Customer production" (defined by *effect*))

**Problem:** heap dumps pause the JVM, profilers add load, `EXPLAIN ANALYZE` executes the query, and log-level changes alter behaviour. During an incident, diagnostic queries against a saturated database make it worse. Heap dumps also contain customer data in raw form.

Fix: classify diagnostic actions as catalogue entries with risk levels. Only passive reads (metrics, logs, the Kubernetes API) are "reading". Ban artefacts that contain raw data, such as heap dumps, unless the customer explicitly permits them, and never send them out of the cluster.

**[Adversarial]** — M-10. Prompt injection can still reach the decision through the human approver and through induced signals (§ SEC-1, FR-11, Section 2 (the approver is a "non-expert business owner"))

**Problem:** (a) Facts are shown "separately" from the AI's wording, but the non-expert customer reads the plain-language AI text, which is exactly where an injected log line can steer ("this is a routine, safe fix, please approve"). (b) "More than one independent signal" is undefined: two log streams from two attacker-controlled pods are not independent. (c) A malicious tenant workload can create real signals, such as filling a disk or allocating memory, to trigger ticked repairs (evictions, drains) on demand.

Fix: generate the approval text that describes the action from the catalogue template, never from the model. Define independence (different source and collection path, at least one not under workload control). Add a rate limit per workload on repairs that workload's signals triggered.

**[Adversarial]** — M-11. PRIV-4's outbound check is untestable and has no failure behaviour (§ PRIV-4 ("a further test runs on every whole line ... to make sure nothing harmful, such as injected instructions, goes out"))

**Problem:** the PRD does not say what the test is, what counts as "harmful", what happens on a hit (block, quarantine, alert, or degrade to "time and type only"), or where the check runs (see C-2). "To make sure" is a guarantee the check cannot give.

Fix: define the check's classes (secret patterns, PII detectors, instruction-like text), the fail-closed behaviour, the location of the check outside the agent, and measurable detection rates in PRIV-7's planted tests.

**[Adversarial]** — M-12. Engineer access to the code-fix test environment is a new privileged path with no security requirement (§ FR-44 steps 2 and 4)

**Problem:** an Orvex engineer "securely accesses" an environment "within the customer's infrastructure". To run the app, that environment usually needs configuration, credentials and often data copies. Neither SEC nor PRIV says anything about data copies in the test environment, the engineer's access scope, session recording or credential isolation.

Fix: the test environment uses synthetic or masked data and no production credentials. Engineer access is time-limited, recorded (FR-33) and read-only to the diff and test results.

**[Adversarial]** — M-13. Deploying a code fix leaves the customer's source repository out of step with production (§ FR-42 step 5 ("Nightshift deploys the fix if deployment is supported"))

**Problem:** if Nightshift patches the running image or deployment, the customer's next ordinary deploy from their own repository silently reverts the fix, or production runs code that is in no repository. If Nightshift writes to the repository, it is changing customer assets with no stated scope.

Fix: the deliverable of a code fix is a pull request or patch in the customer's source control, to be deployed through their pipeline. Nightshift does not deploy directly, or does so only as a temporary hotfix marked to expire.

**[Adversarial]** — M-14. "Harmful", "makes things worse" and "worth alerting" have no definitions, so SM-2, SM-3 and SM-6 cannot be measured consistently (§ FR-9 ("weighs four factors"), FR-28 ("if a repair makes things worse"), SM-2 ("without causing another problem"), SM-3)

**Problem:** FR-28's automatic stop trigger, the vision's "zero harm" count and the alert decision have no operational definition. Two reviewers will classify the same event differently, and the agent cannot run FR-28 without a rule.

Fix: define a harmful repair (for example, a worsened health signal or a new incident on the same target or safety domain within T after the repair). Make FR-28's trigger a catalogue-defined guard. Give FR-9 a decision rule or scoring rule, even if its thresholds are deferred.

**[Adversarial]** — M-15. Ticks lapse silently on release, and implementation changes skip re-consent (§ FR-22 ("if a release changes the repair's action, conditions or risk level, the customer must tick it again"))

**Problem:** (a) After a release, the customer's expected automatic repairs quietly stop running until they tick again. The PRD does not say they are told, so the 3 AM cleanup they relied on does not run. (b) Changes to the *implementation* (how the action is executed) that keep the same declared action, conditions and risk level carry the old tick over, so changed behaviour runs on a tick given for the old version.

Fix: notify the customer of every tick invalidated by a release, before it deploys, and show the lapse on the dashboard. Bind ticks to a hash of the whole signed entry, or define which implementation changes count as material.

**[Adversarial]** — M-16. Maximum-privacy customers get no AI explanations, but FR-11 still promises them (§ PRIV-2 ("In strict cases, only the time and type of a problem leave"), FR-11, Section 7)

**Problem:** with no in-cluster GPU and a hosted model that receives only time and type, nothing can write a contextual plain-language explanation. FR-11 and SM-5 still apply.

Fix: require template-based explanations from catalogue entries as the baseline for every supported problem. AI wording is an enhancement, and the morning summary states which mode produced each message.

**[Adversarial]** — M-17. Nothing watches Fleet, and a Fleet outage looks like a fleet-wide failure (§ FR-6 (Fleet is the external watchdog), FR-32)

**Problem:** if Fleet's ingestion fails or Fleet loses network reach to a region, thousands of agents look silent. FR-32's correlation logic may raise a false "300 clusters failing" alert, or pause rollouts. Nothing monitors Fleet itself.

Fix: require an independent watchdog for Fleet. Before declaring agents silent across many clusters, check a sample through a second path.

**[Judge]** — M1. It is unclear whether free-text log excerpts ever leave the cluster (§ PRIV-2 to PRIV-4)

PRIV-2 describes "a small message built from approved fields", while PRIV-4 checks "every whole line about to leave", which implies log lines do leave. That is the heart of the brief's question "strip private data first".

Fix: say explicitly which applies. Either only structured, allowlisted fields leave, or sanitised log excerpts may leave under these conditions. Give one worked example (the memory-leak case) of exactly what the hosted model receives.

**[Judge]** — M2. The outbound check (PRIV-4) checks for injected instructions but does not explicitly check for leftover private data (§ PRIV-4)

PRIV-4 describes the check on every whole line about to leave as a guard against injected instructions; leftover secrets and personal data are not named as something it looks for.

Fix: the check also scans for leftover secrets and personal data (patterns, entropy, known customer identifiers) and blocks the message if any are found. Planted-secret tests (PRIV-7) then measure how well this works.

**[Judge]** — M3. "Private data" is not defined (§ Glossary, PRIV-3)

Is it only PII and secrets, or also hostnames, IP addresses, service and table names, and business data in queries? For a sovereign-cloud customer, the names in their architecture may be sensitive.

Fix: add a Glossary entry with categories, and state that the allowlist (PRIV-3) is the operative control, not the definition.

**[Judge]** — M4. EKS is described only as "the signals the provider makes available" (§ Section 7, Section 11)

On EKS with managed node groups, worker nodes are EC2 instances in the customer's account, so node OS, disk and memory signals are fully visible. Only the control plane is the provider's. Node replacement through the Auto Scaling group is a possible (risky) repair. A hosted model in the customer's own cloud account (for example Bedrock in the same region) is a privacy option Section 7 does not consider.

Fix: add a short OMK vs EKS comparison table (visible layers, repair levers, hardware path, model options) or require it of the architecture in Section 11.

**[Judge]** — M5. Without out-of-band management, limited-visibility mode is likely the common case on cheap hardware, but it is treated as the exception (§ FR-7, FR-8)

Danny describes "cheap, unreliable and potentially poorly maintained bare metal".

Fix: define the in-band hardware baseline (SMART, ECC/EDAC, NIC counters and link state, kernel logs, temperature sensors) as always present, and the BMC as an enhancement. Ask the failure catalogue to tag each failure as visible in-band, needs a BMC, or invisible.

**[Judge]** — M6. Fleet learning has no speed target and only one, slow path (§ FR-37 to FR-40)

Every lesson goes through a person, two reviewers and a full tested release. The brief asks that a new problem "make every other cluster ready for it".

Fix: split the paths. Detection and explanation rules, which only alert, can ship faster through a lighter signed channel. New repairs go through the full release. Add a metric: time from first occurrence to fleet readiness.

**[Judge]** — M7. Tuning is one line (§ FR-41)

The brief's opening quote is "tuning and self-healing". It is unclear whether a tuning change is a repair (risk level, tick, verification, rollback) or a separate mechanism, and what "limits" look like.

Fix: state that every tuning change is a catalogue repair with bounds set by the release, a risk level, verification and rollback. Give one or two examples (requests and limits, autoscaler bounds, disk-pressure eviction thresholds).

**[Judge]** — M8. There is no requirement for detecting problems that are not in any catalogue (§ FR-19)

FR-19 handles new problems once found, but nothing requires generic symptom-based detection (service-level-objective burn, error-rate and latency anomalies, log-pattern changes) to catch them.

Fix: add an FR for symptom-based detection that is independent of the catalogue.

**[Judge]** — M9. The workload estimates look optimistic against Danny's framing, and the staffing claim contradicts its own arithmetic (§ NFR-1, SM-8)

250 problems a night across 10,000 clusters is one problem per cluster every 40 nights, on hardware Danny calls unreliable, under a platform he calls "a complex mess … a million things can go wrong". And "one engineer on duty" faces about 8 hours of work at 250 problems and about 17 at 500, under the PRD's own best case.

Fix: give the source or reasoning behind 250, run the cost model over a range (for example 250 to 2,500), and make the night staffing a function of the automatic share instead of a fixed headcount.

**[Judge]** — M10. Model call volume is not bounded in the PRD (§ Section 7, Section 11)

Section 11 asks the architecture for it, but the PRD never states whether the model reads logs continuously ("constantly looking at logs") or is called only per problem. That decides whether model cost is negligible or dominant.

Fix: state the intended mode: called per problem, with rules and statistics on the continuous stream. Ask the cost model to test both.

**[Judge]** — M11. Section 11 under-specifies the failure catalogue and the privacy and security review (§ Section 11)

Section 11 says what the failure catalogue and the privacy and security review must contain, but not the failure catalogue's ranking criteria and per-failure fields, nor the data flows and threat model the review must produce.

Fix: the failure catalogue gives its ranking criteria (frequency × impact × whether it can be detected), plus per failure the detection signals, time to impact, catalogue repair with risk level and approval path, and in-band vs BMC visibility. The privacy and security review includes a data-flow diagram per outbound channel, the first allowlist, a threat model (STRIDE or similar) and the compromised-agent analysis from H1.

**[Security]** — SEC-R2-14. The PRIV-4 outbound check cannot be tested as written (§ PRIV-4, "a further test runs on every whole line about to leave ... to make sure nothing harmful, such as injected instructions, goes out")

**Problem:** "Harmful" is undefined. There is no detection target, and nothing says what happens on a match (block, redact or alert). The test checks for injected instructions, not secrets, so secret detection rests on the sanitiser alone.

Fix: Specify what PRIV-4 checks: secret patterns, high-entropy strings, placeholder leaks and instruction-like content. Set the action on a match to block and record. Run it in the egress gateway (SEC-R2-06). Set a measurable target against a labelled test corpus, and report misses under PRIV-7.

**[Security]** — SEC-R2-15. The allowed-field lists belong only to Orvex (§ PRIV-3 "Orvex defines and owns the list of allowed fields, recipients and destinations")

**Problem:** Customers cannot see or narrow what leaves, and Orvex can widen a list without the customer knowing. That undermines PRIV-7 ("proving privacy").

Fix: The lists are versioned, signed and published to each customer. Customers can narrow them. Any widening is notified in advance and needs the customer's acceptance for that customer's clusters.

**[Security]** — SEC-R2-16. Fleet-learning integrity and poisoning (§ FR-37 to FR-40; addendum ("sanitised evidence → a person diagnoses → ... shadow run across the fleet"))

**Problem:** 
- Only new or changed **repair** entries need two reviewers. Detection rules and incident-catalogue entries need one, yet rules decide matching, and matching triggers ticked repairs.
- Sanitised evidence going to the learning pipeline is a channel not listed in PRIV-2.
- An attacker running apps on several clusters can produce coordinated crafted evidence that shapes a "lesson".
- A "shadow run across the fleet" executes new logic in every cluster before release.

Fix:

- Two reviewers for any rule or entry that can lead to a repair, including any change to a risk level.
- Add the learning pipeline to the PRIV-2 channel list.
- Lessons cite the number of distinct customers behind them, and evidence from a single tenant cannot alone produce a fleet rule.
- Shadow runs are read-only and signed like releases.

**[Security]** — SEC-R2-17. The audit record can be polluted and may hold raw evidence outside the cluster (§ FR-33, FR-34, FR-35, SEC-2 (Audit records), SM-4)

**Text:** "the agent can add to it but cannot change or delete entries"; FR-34 records "the problem and its evidence".

**Problem:** 
- A compromised agent can **append** false entries, for example "approved by Samira", or flood the record.
- SM-4's cross-check with Kubernetes audit logs fails if the agent can change the audit policy.
- Where the "independently protected audit service" runs is unspecified. If it is central, the evidence in FR-34 (log excerpts) leaves the cluster.
- Reads by Orvex **people** (support, engineers, Fleet operators) are not recorded where the customer can see them.

Fix:

- Authorisation entries are written by the executor and verified against the SEC-9 signatures, not taken from the agent.
- The agent has no rights over the Kubernetes audit policy.
- The audit service location follows PRIV-1, with evidence stored by reference in the cluster.
- FR-33 covers Orvex staff access to customer data and clusters.

**[Security]** — SEC-R2-18. An attacker can trigger the last-resort condition (§ FR-24, FR-23, FR-30)

**Text:** "applies only when nobody answers and failure is predicted within about 30 minutes".

**Problem:** Both conditions can be engineered. The prediction comes from signals a compromised app controls, and "nobody answers" is likely at 3 AM. This turns a ticked risky repair into an outage on demand, repeated within the FR-30 rate limits.

Fix: The last-resort prediction must come from signals in at least two trust domains (SEC-R2-04). The condition fires at most once per target per window, then needs a human. FR-30 limits count last-resort runs separately, and each run is reported at once.

**[Security]** — SEC-R2-19. Approvals have no expiry (§ FR-22, "There are no timers to manage"; FR-31)

**Problem:** An approval nobody has used stays open indefinitely. If its preconditions happen to hold days later, possibly arranged by an attacker, it runs. FR-31 can also resume a repair on an approval given before the crash, against a changed state.

Fix: Every approval has an expiry (proposed: minutes, set per risk level) and is void once the evidence is superseded. An approval used before a crash is not reused if the re-checked evidence differs from the evidence shown.

**[Security]** — SEC-R2-20. The scope of advance permission is undefined (§ Glossary "Advance permission", FR-21)

**Problem:** It is unclear whether a tick on "restart the only replica" applies to every service and cluster, including a database. A customer who meant to allow it for a stateless frontend has authorised it everywhere.

Fix: Each tick names its scope (clusters, namespaces or services, with excluded critical services). The executor enforces the scope.

**[Security]** — SEC-R2-21. Disk cleanup can be turned into a prohibited deletion (§ Glossary "Disk cleanup", 3.2)

**Problem:** A tenant pod writes a symbolic link in an allowlisted cache or temporary path that points at database files. A cleanup that follows the link deletes customer data, which is a prohibited action.

Fix: Cleanup never follows symbolic links or crosses mount points, and checks ownership before deleting. Allowlisted paths are on Nightshift-owned or runtime-owned volumes only. Cleanup runs in the executor with per-run byte and file limits.

**[Security]** — SEC-R2-22. Supply chain beyond signatures (§ SEC-5, SEC-6)

**Problem:** 
- No software bill of materials (SBOM) or build provenance is required for open-source dependencies.
- The installation trust root and how the verifier itself is protected are not stated.
- There is no revocation.
- The hosted model cannot be signed, so its behaviour can change silently.
- SEC-6 switch-off messages are not required to be authenticated, so a forged switch-off disables repairs across the fleet.

Fix:

- Require an SBOM and signed build provenance per release.
- Pin the trust root at installation, with customer-visible key rotation and a signed revocation list.
- Pin hosted model versions and re-run the SEC-1 injection corpus on each model change.
- SEC-6 commands are signed by the release keys and logged in the customer's record.

**[Security]** — SEC-R2-23. Fleet multi-tenant isolation is not testable (§ FR-48 "one customer's information is never visible to another customer (AI suggestion, accepted by Amine)"; FR-15 grouped views; FR-32 "The affected clusters' reports are preserved")

**Problem:** 
- There is no isolation mechanism or test.
- Orvex's grouped views of 100 clusters mix customers.
- The preserved cluster reports in FR-32 may be gathered centrally, which would bring raw data to Fleet.

Fix:

- Each cluster gets its own identity tied to its tenant, and Fleet APIs enforce authorisation per tenant.
- Run automated cross-tenant access tests in CI and an annual penetration test.
- Grouped views show only PRIV-3 fields.
- FR-32 reports are preserved in each cluster and referenced from Fleet, not copied to it.

**[Security]** — SEC-R2-24. Rights inventories are missing, so SEC-3 and SEC-4 cannot be tested (§ SEC-3 "kept securely", SEC-4 "holds only the rights it needs")

SEC-3 says credentials are "kept securely" and SEC-4 that "Nightshift holds only the rights it needs", but no inventory of rights exists to test either statement against.

Fix: Require a published rights inventory per component: agent, executor, hardware component, management agent, Fleet, test environment. It lists each Kubernetes verb and resource, BMC role and network destination. An automated test fails the release if the deployed rights go beyond the inventory.

### Low (22)

**[Substance over theater]** — A few NFRs and constraints only restate other sections (§ NFR-5, NFR-8, SEC-4)

NFR-5 repeats the Vision and 5.7, and NFR-8 repeats FR-11. SEC-4, "Nightshift holds only the rights it needs", is boilerplate on its own; SEC-3 carries the real content.

Fix: make SEC-4 concrete (for example, read-only by default, with write rights limited to the actions in the repair catalogue entries the customer has ticked), and either fold NFR-5 and NFR-8 into their sources or leave them as explicit pointers.

**[Strategic coherence]** — SM-10 does not state the success test for proof point 4 (§ SM-10, COST-4)

Its target is "as low as realistically possible", while the actual test, total operating cost compared with the "without Nightshift" baseline, sits in COST-4.

Fix: make SM-10's pass condition "total operating cost per cluster below the without-Nightshift baseline at 10,000 clusters".

**[Done-ness clarity]** — The morning summary has no time basis or delivery channel (§ FR-16, UJ-4)

"Every morning" does not say whose morning (the customer's time zone? per cluster?), and UJ-4's "she opens the morning summary" does not say where (the portal, email or Slack). The wireframes need both.

Fix: add one line covering timing and channel.

**[Scope honesty]** — FR-23 contains an undecided feature (§ FR-23, Section 10)

"[Possible feature, Amine] For dangerous cases, Nightshift calls a member of the Orvex Nightshift team." Inside an FR it reads as either in scope or out, and it is not listed in Section 10.

Fix: decide it, or move it to Section 10 with an owner.

**[Adversarial]** — L-1. Duplicate open-question ID (§ Section 10)

Section 10 uses "7a" and "7b" (for Danny) and also "7" (hand-in date, answered).

Fix: renumber.

**[Adversarial]** — L-2. Three catalogue names, with no mapping between them (§ Section 11, FR-1, FR-8, Glossary, SM-1)

"Failure catalogue" (Section 11, FR-1, tags *predict / fix / only report*), "incident catalogue" and "repair catalogue" (Glossary). FR-1's tested scope is 20 failures, while FR-8 lists about 30 predictable problems, so SM-1's denominator ("supported, slowly developing problems") is ambiguous.

Fix: state that the failure catalogue deliverable is the first-version content of the incident and repair catalogues, and that SM-1 counts only its *predict* entries.

**[Adversarial]** — L-3. The Glossary's "Approval" leaves out the exception for dangerous repairs (§ Glossary "Approval", FR-21)

Glossary: "The customer approves, or Orvex support if the customer delegates to them". FR-21 excludes dangerous repairs from delegation.

Fix: add "except dangerous repairs" in the Glossary.

**[Adversarial]** — L-4. "All three model options" versus "Focus: the hosted model" (§ 3.1, Section 7)

3.1 lists all three options as in scope; Section 7 makes the hosted model the first-version focus.

Fix: say that all three are *costed and compared*, and the hosted model is *built*.

**[Adversarial]** — L-5. SM-1 measured on injected faults is biased towards the faults that were designed for (§ SM-1, SM-C1)

SM-1 validated with failure injection measures recall on the faults the team chose to inject.

Fix: also track SM-C1 (missed problems) on real clusters, and report SM-1 with its injection scope.

**[Adversarial]** — L-6. The coordinator ignores actions taken by the hosted-Kubernetes provider (§ FR-29)

FR-29 considers "Kubernetes' own controllers, the customer's deployments and people", but not EKS node auto-repair, autoscaling-group scale-in or managed node-group upgrades, which drain nodes on their own.

Fix: add provider actions to the coordinator's inputs on hosted Kubernetes.

**[Adversarial]** — L-7. FR-28's stop has no resume path and halts unrelated safe repairs (§ FR-28)

"Stops further automatic repairs on that cluster" does not say who resumes them, and blocks ticked repairs for unrelated problems, such as a disk filling, while the stop lasts.

Fix: scope the stop to the affected safety domain, and name who can lift it.

**[Judge]** — L1. The provenance tags are dense (§ Whole PRD (provenance tags))

The provenance tags are dense: "review fix, 2026-10-30, approved by Amine" appears about 20 times. They are good for AI fluency but slow down a 15-minute read.

Fix: keep short tags, or move them to a trace table, and leave one line explaining the convention.

**[Judge]** — L2. Naming collision (§ Glossary "Incident", incident catalogue)

"Incident" means user-visible disruption, while the "incident catalogue" holds any problem without a tested fix.

Fix: rename it, for example "investigation catalogue" or "known-problem catalogue".

**[Judge]** — L3. App monitoring is either fully opted in or off (§ UJ-1, UJ-2)

Quornex deploys the customer's app, so platform-level health (restarts, golden signals) could be watched without reading app logs or code. UJ-1 and UJ-2 depend on opt-in.

Fix: separate "platform-level health of the customer's app (always)" from "app logs and code (opt-in)".

**[Judge]** — L4. Code fixes do not say where code comes from or goes to (§ FR-42 to FR-44, COST-3)

Code fixes do not say where code comes from or goes to (repository access, pull request vs direct deploy) or who pays for the isolated test environment (COST-3).

Fix: one line each.

**[Judge]** — L5. Sanitised evidence vs judging a repair (§ PRIV-2, FR-21)

An Orvex engineer approving a risky repair sees only sanitised evidence (PRIV-2 covers Slack and the portal).

Fix: Say whether sanitised evidence is enough to judge the repair, and if not, how in-cluster evidence is viewed without exporting it.

**[Judge]** — L6. The success targets (80%, 95%, 90%) have no reasoning behind them (§ Section 8 (success metric targets))

The 80%, 95% and 90% targets are stated without the reasoning behind them.

Fix: one line on why each threshold was chosen, or label them as placeholders.

**[Security]** — SEC-R2-25. Phone-call impersonation (§ FR-13, FR-14)

**Problem:** Attackers who call customers pretending to be Nightshift can push them towards a fake portal.

Fix: Nightshift calls and messages never ask for credentials or approval by voice. Customers are told this during onboarding. The call content counts as a PRIV-2 channel to the telephony provider.

**[Security]** — SEC-R2-26. Liveness is not integrity (§ FR-6)

**Problem:** A compromised agent can keep sending "I'm alive" while its monitoring is disabled.

Fix: Heartbeats include a signed attestation of the release version and of whether the executor and egress gateway are healthy.

**[Security]** — SEC-R2-27. The reviewer of the recovery plan, and Orvex's advance permission, are unspecified (§ FR-21 (dangerous: "recovery plan reviewed"), FR-24 ("Orvex's permission given in advance"))

FR-21 requires a "recovery plan reviewed" for dangerous repairs without naming who reviews it, and FR-24 relies on "Orvex's permission given in advance" without saying how it is given or recorded.

Fix: Name the reviewing role, which must differ from the approver. Orvex's advance permission is signed per repair and per customer, like an approval (SEC-9).

**[Security]** — SEC-R2-28. Where the placeholder mapping lives (§ PRIV-2)

PRIV-2 replaces private values with placeholders but does not say where the table that maps placeholders back to real values is kept.

Fix: The table mapping placeholders back to real values never leaves the cluster. Model responses are filled back in only inside the cluster.

**[Security]** — SEC-R2-29. Coordinator marks can block all repairs (§ FR-29, FR-31)

**Problem:** A compromised agent can mark every target "unavailable", which quietly blocks all repairs.

Fix: Only the executor sets marks. A mark longer than a set duration raises an alert.

## Mechanical notes

- **ID continuity:** FR, SM, PRIV, SEC, COST, NFR and UJ IDs are all contiguous and unique, and Section 1's "FR-1 to FR-49" is accurate. The Section 10 numbering is harder to follow:
  - "7a" and "7b" (for Danny) coexist with "7." (answered: the hand-in date), and the triage note says "Danny's questions (1–7b)".
  - The "Design decisions still open" list jumps from 8 to 12, because 9 to 11 sit under "Answered and decided".

  Rename the answered hand-in-date question (for example A1), or renumber.
- **Assumptions Index roundtrip:** there is no Assumptions Index. Inline assumptions: "[DESIGN ASSUMPTION unless Danny confirms: its exact internal components]" (Glossary, Quornex Fleet); "[DESIGN ASSUMPTION unless Danny confirms] A customer with a single cluster has no control cluster" (5.7 description); "(assumption; Danny's number still open)" (SM-7); and "(Assumption: 99.9% a month.)" (Q4). SM-7 and Q4 are covered by Section 10. The two design assumptions are not listed in Section 10 or anywhere else. Add them to the "For Danny" list or to a short index.
- **Glossary drift:**
  - "incident catalogue" holds faults and failures too, while the Glossary defines "Incident" narrowly as a user-experienced disruption. The name predates the redefinition; consider a note to that effect.
  - "customer administrators" (SEC-7) is the only place an authorised customer role is named. Elsewhere it is "the customer" or "the customer's business owner". Say whether the business owner is the administrator by default.
  - "Nightshift engineer", "Nightshift team engineer" and "Orvex Nightshift team" are used interchangeably. That is fine, but consider one line in the Glossary.
- **UJ protagonists:** UJ-1's protagonist is unnamed ("the owner of an online shop"). UJ-2's protagonist is "Amine", the same name as the author's source tag "(Amine)", which appears throughout. A reader of UJ-2's edge case or the wireframes may confuse the persona with the source. Rename the UJ-2 persona.
- **UJ realisation lists:** UJ-5 lists "Realises FR-6, FR-32" but its edge case relies on FR-47 (rollback policy) and, implicitly, FR-46. Add both. UJ-1's climax ("Nightshift applies the fix") does not say whether the fix is risky; if it is, FR-21 requires Orvex technical approval as well, which UJ-2 handles but UJ-1 does not.
- **Addendum:** its cross-references (FR-4, FR-37 to FR-40) resolve, and its items are correctly labelled as unconfirmed where they are. Nothing in it contradicts the PRD.
- **Required sections:** all are present for this stakes level and product type: Vision, users and journeys, scope and Non-goals, Glossary, FRs, constraints, NFRs, SMs with counter-metrics, open questions and downstream requirements.

---

Rubric: `/home/amine/nightshift/.claude/skills/bmad-prd/assets/prd-validation-checklist.md` · Generated: 2026-10-31T15:31:49+00:00
