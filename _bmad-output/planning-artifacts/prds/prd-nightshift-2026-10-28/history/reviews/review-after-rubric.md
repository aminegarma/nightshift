# PRD Quality Review — Nightshift (second review, after fixes)

Reviewed: `prd.md` (updated 2026-10-31) and `addendum.md`. Judged against `prd-validation-checklist.md`. Deferred open questions with an owner and a revisit trigger (Section 10 triage) are treated as acceptable, not as gaps.

## Overall verdict
The authorisation model is the PRD's backbone and holds up well. The risk levels in the Glossary, the approval table in FR-21, FR-22 to FR-24 and the Non-goals in 3.2 are crisp, sourced and consistent with each other, and the open items are triaged honestly. Three gaps remain, and each touches either the thesis or the next step. "Harmful repair" is never defined, yet the Vision's third proof point and SM-3 rest on it. FR-41 lets Nightshift tune cluster settings without saying how that fits the tick/approval rules that SM-4 holds at zero. And no journey shows a customer setting up the permissions the whole model depends on, although UX wireframes come next. Fix those three and the PRD is ready for UX and architecture.

## Decision-readiness — strong

Decisions are stated as decisions, and most come with their reasons. Examples: "Delegation never covers dangerous repairs" (FR-21), "Focus for the first version: the hosted model ... because it should cost much less" (Section 7), the trade-off in FR-43 ("in-cluster only would leave the experiment with very few users"), and "Whether that needs a separate tool is for the architecture" (FR-32 table). The Section 10 triage gives every remaining item an owner and a revisit trigger, and the "Answered and decided" list shows questions that were actually closed. Someone pushing back on the extra Orvex approval step would find their objection already raised as Q2.

Two places still stop short of a decision. The first is staffing. SM-8 does the arithmetic (about 8 hours of human work on an average night, about 17 on a bad one) but never compares it with "One Nightshift engineer is on duty each night" (FR-23, SM-8). The second is the code-fix experiment, which has metrics but no rule for keeping or dropping the feature.

### Findings
- **[medium]** The staffing arithmetic is never compared with the one-engineer decision (SM-8, FR-23, FR-21). At the base case, about 8 hours of hands-on work a night falls on one on-duty engineer, which is close to full utilisation with no slack. On a bad night it is about 17 hours. FR-21 also requires "Orvex technical approval each time" a ticked risky repair runs, which adds to that load. The PRD says "the staffing estimate depends heavily on the automatic share" but never says at what point backups are called in or the model fails. *Fix:* state the automatic share and the minutes per escalation at which one engineer is enough, and name the backup trigger. For example: "backups join when the queue of pending approvals exceeds N or the predicted human work exceeds X hours."
- **[medium]** The code-fix experiment has no rule for keeping or dropping it (FR-45). "Orvex measures the experiment to decide whether code fixes stay" lists seven metrics but gives no threshold, no sample size and no decision owner or date, and Q12 does not list them. Danny asked for this feature as an experiment, so the rule for ending it is the decision that matters. *Fix:* add a decision rule, for example "keep if net cost savings > 0 and fix success rate ≥ X% after N patches", or add it to Q12 with an owner.

## Substance over theater — strong

Very little here is furniture. The Vision is specific to this product (OMK versus EKS coverage, sovereign cloud for small businesses, 10,000 clusters, four testable proof points) and could not be swapped into another PRD. The three user types each drive routing and approval logic (FR-12, FR-21), and the UJs use named roles that map to them. The cost section separates technical cost from total operating cost and adds a "without Nightshift" baseline (COST-4), which is real substance. The example tables (risk levels, FR-8, FR-32 responsibilities) do work in the PRD rather than decorate it.

### Findings
- **[low]** A few NFRs and constraints only restate other sections (NFR-5, NFR-8, SEC-4). NFR-5 repeats the Vision and 5.7, and NFR-8 repeats FR-11. SEC-4, "Nightshift holds only the rights it needs", is boilerplate on its own; SEC-3 carries the real content. *Fix:* make SEC-4 concrete (for example, read-only by default, with write rights limited to the actions in the repair catalogue entries the customer has ticked), and either fold NFR-5 and NFR-8 into their sources or leave them as explicit pointers.

## Strategic coherence — adequate

The thesis is clear, and the success metrics follow it: detect (SM-1), explain (SM-5), repair without harm (SM-2, SM-3, SM-4), and replace engineers at a lower cost (SM-8, SM-9, SM-10, COST-4). Each counter-metric is paired with a specific metric. The MVP is "everything", and the PRD says so openly (3.1: "Nothing has been deferred to a later version yet"). That is a legitimate choice for a design challenge where Danny wants feedback on everything. Two things weaken the arc: the key term behind proof point 3 is undefined, and the new focus on the hosted model in Section 7 is not reconciled with the scope list in 3.1.

### Findings
- **[high]** "Harmful repair" is never defined, although a primary metric depends on it (Vision, SM-3, FR-36, FR-28). The Vision's third proof point is "every harmful repair is counted and reviewed", and SM-3 counts harmful repairs "separately from repairs that did not work". The Glossary has no entry for the term. SM-2 ("restore health without causing another problem") and FR-28 ("makes things worse") each describe something close to it, and nothing says where one ends and another begins. Without a definition, SM-3 cannot be measured, and the failure-injection tests (Section 9) cannot label outcomes consistently. *Fix:* add a Glossary entry, for example "a repair whose effect worsens service health, data integrity, security or access beyond the state before it ran, whether or not it was rolled back". State that SM-2 failures and SM-3 harms are mutually exclusive, and that FR-28 is the runtime response to a harmful repair.
- **[medium]** The hosted-model "focus" is not reconciled with "all three model options" in scope (Section 7 versus 3.1). Section 3.1 puts "all three model options" in the first version, while Section 7 says "Focus for the first version: the hosted model". The architecture cannot tell whether in-cluster GPU diagnosis is built for the first version or only costed. The shared-GPU option raises the same question. *Fix:* say in one sentence what "focus" means. For example: "first version builds the hosted path for diagnosis and the in-cluster path for code fixes; shared GPU is costed only."
- **[low]** SM-10 does not state the success test for proof point 4 (SM-10, COST-4). Its target is "as low as realistically possible", while the actual test, total operating cost compared with the "without Nightshift" baseline, sits in COST-4. *Fix:* make SM-10's pass condition "total operating cost per cluster below the without-Nightshift baseline at 10,000 clusters".

## Done-ness clarity — adequate

The authorisation and recording FRs are testable as written. FR-21's table, FR-22's version-tied ticks, FR-34's count of unapproved changes with a target of 0, FR-31's crash recovery and FR-7's four-step installation check all give story writers clear acceptance conditions. Detection scope is tied to the failure catalogue deliverable (FR-1), which is a sound way to bound it. Weaker FRs remain, though: one sits outside the approval model, and several use adjectives where bounds are needed and are not covered by the deferral of timing targets in Q8.

### Findings
- **[high]** FR-41's tuning sits outside the authorisation model. "Nightshift may tune the cluster's settings only within the limits set by the tested release" says nothing about ticks, approval, risk level, alert-only mode or recording. The Glossary's "Customer production" says any change that "can affect the customer's live experience or service" needs a tick or an approval, and SM-4 holds unapproved changes at 0. As written, an engineer cannot tell whether tuning goes through FR-21, or whether it may run in alert-only mode. *Fix:* state that every tuning action is a repair catalogue entry with a risk level, subject to FR-21 and FR-33, and that alert-only mode disables it. Or, if tuning needs its own permission, make it a settings tick covered by SEC-7.
- **[medium]** Nobody is assigned to decide which services are critical, or who gets phoned (FR-9, FR-13, UJ-2). Criticality is one of the four alert factors in FR-9 and the trigger for phone calls in FR-13 ("an important service such as checkout or a database"). UJ-2 depends on it ("Because checkout is critical, Nightshift calls him"). Nothing says who marks a service critical (the customer in settings, a default for Quornex databases, or Nightshift inferring it) or which person is called, and in what order. *Fix:* add an FR stating that the customer designates critical services and a call list in settings, with stated defaults for Quornex-managed services.
- **[medium]** FR-28 has no detection criterion and no exit (FR-28). For "If a repair makes things worse", the PRD gives no measure of "worse". "Stops further automatic repairs on that cluster" has no condition for resuming and no one named to re-enable repairs. "Calls a person" does not say whether that is the customer, the on-duty engineer or both. *Fix:* define "worse" against the repair entry's verification (ties to the harmful-repair definition above), and name who is called and who lifts the stop.
- **[medium]** Vague qualifiers remain that the deferral in Q8 does not cover (FR-10, FR-13, FR-23, FR-37). Examples: "if the predicted time or risk changes substantially", "once the risk has decreased enough and stays stable" (FR-10), "strong evidence it is about to fail" (FR-13), "If they do not answer in time" (FR-23) and "well controlled" (FR-37). Q8 defers "timing targets", which arguably covers FR-23 but not the others. *Fix:* either widen Q8 to "thresholds for FR-10, FR-13, FR-23, proposed by the architecture", or replace "well controlled" in FR-37 with what FR-39 and FR-40 already require (two reviewers, a tested release).
- **[low]** The morning summary has no time basis or delivery channel (FR-16, UJ-4). "Every morning" does not say whose morning (the customer's time zone? per cluster?), and UJ-4's "she opens the morning summary" does not say where (the portal, email or Slack). The wireframes need both. *Fix:* add one line covering timing and channel.

## Scope honesty — strong

This is the PRD's strongest structural feature. Section 3.2's Non-goals do real work: each points to the requirement that enforces it (FR-17, FR-23, PRIV-1, SEC-1), and "Treat silence as permission" is stated with its exception. The scope admits its own instability ("Code fixes might not stay after the first version"). Unconfirmed items are labelled where they appear (for example "[DESIGN ASSUMPTION unless Danny confirms]", "Amine's proposal, to validate" and "our proposal, pending Danny's confirmation" in FR-47), and the Section 10 triage gives every deferral an owner. The number of open items is proportionate for a design PRD whose next steps are UX and architecture rather than a build.

### Findings
- **[medium]** The exception for sending code to a hosted model is not reflected in the Vision's absolute privacy statement, and secrets in code are not addressed (Vision, PRIV-2, PRIV-6, FR-43). The Vision says "Raw data and secrets never leave the cluster", and PRIV-2 repeats it. PRIV-6 calls FR-43 "the only exception to PRIV-1" but not to PRIV-2. Source code is not sanitised data, and code often contains hard-coded credentials. Nothing says whether the code sent goes through PRIV-4's outbound check or a secret scan first. The privacy and security review deliverable will run into this directly. *Fix:* qualify the Vision sentence ("…except code a customer explicitly consents to send for a code fix"), and require a secret scan, with blocking, on any code before it is sent.
- **[low]** FR-23 contains an undecided feature: "[Possible feature, Amine] For dangerous cases, Nightshift calls a member of the Orvex Nightshift team." Inside an FR it reads as either in scope or out, and it is not listed in Section 10. *Fix:* decide it, or move it to Section 10 with an owner.

## Downstream usability — adequate

The Glossary is substantial and mostly respected: risk levels, approval, advance permission, last-resort condition and the coordination tiers (Nightshift agent, management agent, Quornex Fleet) are used consistently from FR-6 to FR-48. The IDs are contiguous and unique: FR-1 to FR-49, SM-1 to SM-10 plus SM-C1 to SM-C3, PRIV-1 to PRIV-7, SEC-1 to SEC-7, COST-1 to COST-6, NFR-1 to NFR-8 and UJ-1 to UJ-5. Cross-references resolve. Section 11 tells the architecture, failure catalogue and cost model exactly what to contain, and the addendum routes architecture-depth material cleanly. What remains is a handful of component and surface names that the architecture and wireframes will have to guess at.

### Findings
- **[medium]** Several component and surface terms are undefined (FR-1, FR-2, FR-4, FR-14, Section 11).
  - "Nightshift monitoring service" (FR-2) is not one of the Glossary's agent tiers.
  - "monitoring failure case" (FR-4) is bolded as if it were a defined term.
  - "a Nightshift monitoring page" (FR-14) has no stated relation to the FR-15 dashboards.
  - "failure catalogue" (FR-1, Section 11) sits beside the Glossary's incident catalogue and repair catalogue, even though "failure" has a narrower Glossary meaning ("a service failing").

  The architecture and the wireframes will each map these differently. *Fix:* add Glossary entries, or replace the terms with defined ones. For example, call the Section 11 deliverable "the failure catalogue deliverable (seeds the incident and repair catalogues)".
- **[medium]** Orvex's side of the last-resort permission has no actor and no screen (FR-24, Glossary "Last-resort condition", SEC-7). FR-24 says the permission is "given in advance by the customer and Orvex" and "replaces Orvex technical approval at that moment". SEC-7 covers only the customer's settings changes. Nothing says who at Orvex grants it, whether per customer or per catalogue entry, or where it is recorded. *Fix:* add one sentence naming the Orvex role, the scope (per customer and per repair), and that the grant is recorded under FR-33 and enforced outside the agent (SEC-2).

## Shape fit — adequate

This is a multi-stakeholder B2B product with real UX, feeding wireframes and then architecture, so the UJs carry weight, and the PRD rightly has them. Five journeys cover the customer warned in advance, approval in a crisis, Orvex technical approval, the morning summary and a fleet-wide failure. The FR sections are a capability-spec shape, which suits the operator-side material. The gap lies in which journeys exist. The model's most distinctive UX surface, the settings checklist, appears in no journey, and one of the three named user types has no journey at all.

### Findings
- **[high]** No journey shows the customer configuring permissions (UJ-3, UJ-4, glossary "Advance permission", FR-21, FR-22, FR-24, SEC-7, FR-43, FR-7). UJ-3 and UJ-4 both rely on a tick made off-screen ("the customer has ticked it in their settings", "She had permitted this rollback in advance by ticking it"). The settings surface carries a lot of logic:
  - alert-only versus approval-enabled mode;
  - ticking repairs that show their risk levels, with dangerous ones not tickable;
  - re-ticking after a repair version changes;
  - the last-resort tick;
  - the scope and revocation of delegation to Orvex support;
  - the read scope;
  - the two consents for code fixes;
  - acknowledging limited visibility at installation.

  The wireframes come next and have no journey to design this surface from. *Fix:* add a UJ with a named business owner who sets up the cluster, including one re-tick prompt after a release changes a repair.
- **[medium]** Orvex support has no journey, and delegated approval is never exercised (Section 2 Users, FR-12, FR-21). Orvex support is one of three named users, and FR-21 gives delegation real rules: a customer-set scope, revocation at any time, notification of every approval given, and no dangerous repairs. No UJ shows support receiving and answering a delegated request, or being refused one outside its scope. *Fix:* add a short UJ, or an edge case on UJ-1 ("the owner has delegated to Orvex support; support approves; the owner is notified").

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
