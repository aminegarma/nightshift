# PRD Quality Review — Nightshift (third review, after the 2026-11-02 update)

Reviewed: `prd.md` (updated 2026-11-02) and `addendum.md`, diffed against `prd-final-2026-10-31.md` and `addendum-final-2026-10-31.md`. Judged against `prd-validation-checklist.md`. This review covers the changed and new parts and their knock-on effects: FR-21 (the two-row approval table), FR-22, FR-50, FR-51, FR-52, FR-6, FR-12, FR-14, FR-34, FR-42, PRIV-2, PRIV-8, PRIV-9, Section 7 "Without external AI", the Glossary additions and Section 10. Findings already in `review-after-rubric.md` are not repeated unless the update made them worse; when one is repeated, it is marked "carried over". Inline source tags are the author's convention and are not flagged.

Status of the three high findings from the previous review: "Harmful repair" is now defined (Glossary), with SM-2 and SM-3 kept separate, so that one is **fixed**. FR-41's tuning is now inside the authorisation model, so that one is **fixed** too. The settings and permissions journey is **still missing, and the update made it worse** (see Shape fit).

## Overall verdict
The update applies Danny's Exchange 5 faithfully and mostly well. Dangerous repairs becoming manual, approval depending on what a repair changes, explicit external-AI consent, and the heartbeat as a permitted outbound channel are all stated as decisions with their sources. FR-6 is a model of how to state what a decision gives up. The risk is that the new rules move the hard questions somewhere the PRD does not specify. Three gaps matter most. First, the new axis in FR-21 ("can affect customer production") has no owner, no catalogue field and no defined pre-run check, even though it decides whether the customer is asked at all. Second, FR-52's "a person performs the repair" names no person and drops every authorisation guard the old dangerous-repair flow had. Third, PRIV-9's channel list and its stated consequences do not match PRIV-2, FR-14 and FR-15. These need settling before architecture builds the executor and gateway (SEC-8) against them. UX can proceed in parallel.

## Decision-readiness — strong

The update turns several open items into real decisions with traceable reasons. Examples: "I'd leave dangerous repairs manual initially" (FR-52), "There is no hidden exception" (Glossary, Alert-only mode), "A GPU shared across clusters counts as external AI" (PRIV-8), and the closure of Q1 to Q4 with Exchange 5 citations (Section 10, "Answered and decided"). FR-6 states plainly what a customer gives up by refusing the heartbeat: "Fleet cannot detect from outside that the agent is dead … NFR-4's 'Fleet notices the silence' do[es] not hold." The provisional status of the double approval for the customer's own app is stated honestly (FR-21, last-but-one bullet, and Q21), rather than presented as a rule Danny confirmed.

Two of the new decisions are stated without saying what they cost, and Section 10 has a revisit trigger that cannot fire.

### Findings
- **[medium]** Alert-only mode now stops Orvex's own platform repairs, but the PRD does not say who maintains OMK and Quornex on those clusters (Glossary "Alert-only mode", FR-21, FR-51). "It stops every change Nightshift executes, including routine platform repairs under the agreed management policy", and alert-only is "an ongoing option for any customer, not only for trials". Orvex operates OMK and Quornex for these customers and holds a 99.9% working target (SM-7). Nothing says whether Orvex engineers then do those routine repairs by hand, whether the work is simply not done, or how this affects SM-7, SM-8 or the cost model. The decision itself is clear, but what it gives up is not stated. *Fix:* add one sentence to FR-51 naming the consequence, for example "on alert-only clusters, policy repairs become recommendations to the Orvex Nightshift team, who perform them manually; SM-7 is reported separately for alert-only clusters", and let the cost model count the extra work.
- **[medium]** The open questions for Danny include three that were never sent, under a revisit trigger that can never fire (Section 10 triage, Q19, Q20, Q21). The triage says Danny's questions "(5–7b, 19–21) are owned by Danny and revisited when he replies". But Q19 and Q20 are marked "never sent", and Q21 was "not asked directly" in effect, since Exchange 5 "covers platform changes only". Q21 decides whether every risky repair to a customer's app needs an Orvex engineer, which is the largest single lever on SM-8 staffing. The hand-in window is 10 to 14 November. *Fix:* either send Q19 to Q21 to Danny now, or rewrite their trigger as "our proposal stands for the hand-in; flagged in the cover note as unconfirmed".

## Substance over theater — strong

The new material is substantive. PRIV-9's "per channel" consequences, the FR-21 table's two rows, the zero-retention rule in Section 7 and the consent-screen requirements in PRIV-8 ("nothing preselected", "what leaves the cluster, which provider processes it") each constrain the design in a specific way. The draft consent wording and the status strings in the addendum are useful handoff material, not decoration. No findings.

## Strategic coherence — adequate

The thesis is unchanged, and the update serves it. External AI only with consent, and a working path without any AI (Section 7), strengthen the sovereignty claim in the Vision ("only approved, sanitised information does, through the channels the customer permits"). The update also partly answers the earlier medium on "focus" against "all three options": the in-cluster path must now be built as the fallback for customers who do not consent, not just costed. The shared-GPU question from that finding remains open. The new weakness is proof point 4: the update adds human work in several places but does not revisit the staffing arithmetic.

### Findings
- **[medium]** The update adds human work but leaves the staffing arithmetic unchanged (carried over, made worse; SM-8, SM-9, FR-52, FR-21, FR-22). SM-9 now counts "a manual repair (FR-52)", and the update adds four new sources of human work. Dangerous repairs are now performed by a person, typically hands-on network-card or IP work, not a 20-minute approval. Safe platform repairs that are not in the policy need "Orvex technical approval at the time". Expired approvals mean "Nightshift asks again". Q21's provisional double approval stays in force. Yet SM-8 still uses "90% handled automatically and 20 minutes for each of the rest" and "one engineer is on duty". Proof point 4 ("whether it costs Orvex less or more than those engineers would") rests on these numbers. *Fix:* split SM-9 into "needs an approval" and "needs a manual repair", give the manual case its own time estimate, and re-run the SM-8 arithmetic with both.

## Done-ness clarity — adequate

FR-22's expiry, FR-14's portal-only approval and FR-6's heartbeat contents ("agent ID, a timestamp and a status") are concrete, and the FR-21 table remains readable at a glance. But the update makes the authorisation backbone depend on three things no FR specifies. These are the production-impact classification, the person who performs a dangerous repair, and the lifetime of a rejection. PRIV-9's consequences also contradict the approval surface. These are the conditions story writers will need first.

### Findings
- **[high]** The new approval axis, "can affect customer production", has no owner, no catalogue field and no defined check (FR-21 table and bullets, FR-51 "Limits", Glossary "Customer production", "Platform repair" and "Repair catalogue", FR-22). This axis now decides whether the customer is asked at all. Yet:
  - Risk level has a stated owner ("Orvex sets each repair's risk level … customers cannot change it"), but this axis has none.
  - The repair catalogue entry's fields ("action, its safety preconditions, risk level, expected interruption, authorisation, verification and rollback") do not include it.
  - FR-21 and FR-51 rely on "the pre-run checks show that a platform repair would affect customer production", but FR-22's pre-run checks cover only safety preconditions and authorisation. No production-impact check is defined.
  - The wording shifts between "can affect" (table row, Glossary) and "would affect" / "affects" (FR-21 bullet, FR-51). That is the difference between a design-time classification and a runtime prediction.
  - Quornex "provides databases, queues, storage" to customer apps (Glossary), so the grey zone is large.

  Because Orvex both authors the policy and, implicitly, makes this classification, a misclassified repair would run with no customer say. SM-4 would not catch it, because it compares execution records with "policy decisions". *Fix:* add a catalogue field "affects customer production: yes / no / depends on conditions", set by Orvex at testing and reviewed by the two catalogue reviewers (FR-39). Define the runtime check in FR-22 as a check of that entry's stated conditions. Use "can affect" consistently. Add to SM-4 a review sample of policy repairs that did affect customer production.
- **[high]** FR-52 names no one to perform a dangerous repair and drops every authorisation guard (FR-52, FR-12 "goes to whoever must perform it", FR-42 step 4 "left to a person", Section 2 Users, Glossary "Customer production", SM-4). The old flow required "the customer's approval and Orvex technical approval … plus a recovery plan reviewed before the repair runs". The new flow says only "a person performs the repair". The PRD does not say:
  - who that person is. The customer "chose Quornex so they would not need DevOps staff", and on OMK, Orvex runs the operating system and Kubernetes. So for a dangerous repair to customer production, OMK, a customer-specific code fix, or the customer's hardware configuration, the performer could be Orvex, the customer or the customer's hardware provider.
  - whether a person's manual change to customer production still needs the customer's permission, which the Glossary says any change that can affect customer production does.
  - whether the recovery plan survives.
  - how the change is recorded so that SM-4's cross-check against "Kubernetes audit logs" does not count an Orvex engineer's manual fix as an unapproved change.

  *Fix:* add a "who performs" rule to FR-52, split by what the repair changes: platform → Orvex Nightshift team; customer production → Orvex with the customer's approval; physical hardware → customer, as in FR-20. Keep the customer-approval and recovery-plan requirements for manual changes to customer production. Have Nightshift record the manual repair with the approval behind it (FR-34).
- **[high]** PRIV-9's consequences contradict the approval surface, and its channel list does not match PRIV-2 (PRIV-9, PRIV-2, FR-14, FR-15, FR-16, Glossary "Approval").
  - PRIV-9 lists "the portal" as a separately permitted channel. Yet "Without notifications as well: no alert or approval request reaches anyone outside the cluster; only repairs authorised in advance run" holds only if the portal is also blocked. FR-14 makes the portal the place where approval requests appear and are answered.
  - Blocking the portal on its own, which removes the only approval surface, the FR-15 dashboards and possibly the morning summary, has no stated consequence.
  - "Only repairs authorised in advance run" is also imprecise. A ticked risky repair is authorised in advance but still needs Orvex technical approval at the time, and with notifications and the portal blocked, no request can reach Orvex.
  - PRIV-2 counts "dashboards and the morning summary" as outbound ways information leaves, but PRIV-9's closed list ("The channels are: …") omits them.
  - The "in-cluster dashboard" (FR-15, PRIV-9) is a new surface. The PRD does not say whether approvals can be given on it.

  The gateway (SEC-8) will be built against this list. *Fix:* make PRIV-9 a single table with one row per channel (external AI, heartbeat, Fleet reports, notifications, portal including dashboards and morning summary, code to a hosted model): what each carries, its default, and what stops working without it. Rewrite the "without notifications" bullet in terms of the portal. State whether the in-cluster dashboard can take approvals.
- **[high]** FR-50 does not say how long a rejection blocks a repair, or how a blocked problem can move forward (FR-50, FR-22, FR-23, FR-26, FR-27). "Blocks that proposed repair" does not say whether the block covers this problem instance, the repair on this target until conditions change, or the repair for good. "Does not substitute another repair to get around the rejection" conflicts with FR-26 and FR-27's ranked fallback, and it leaves no path if the problem later becomes critical. FR-23 still says Nightshift "calls if the problem becomes critical", but it is not allowed to propose anything. With two approvers, the FR does not say whether one rejection voids an approval the other has already given. It also does not say whether an Orvex engineer's rejection of a ticked risky repair affects the customer's tick for next time. *Fix:* state that a rejection blocks that repair for that problem instance until the evidence changes materially (for example, a rise in criticality or a new time to impact), at which point Nightshift may ask again, saying what changed. State that any one rejection voids the request for all approvers, and that the tick itself is untouched.
- **[medium]** The default for each outbound-channel permission is not stated (PRIV-9, PRIV-8, SEC-7, Glossary "Approval-enabled mode"). External-AI consent has "nothing preselected", and PRIV-9 requires every channel to be permitted "explicitly". If that also means off by default for the heartbeat, notifications and the portal, a new customer "starts in approval-enabled mode with safe repairs ticked by default" but receives no phone call (FR-13) and no approval request. Onboarding and the UX need the defaults. *Fix:* list the default per channel in the PRIV-9 table proposed above, and state whether the customer contract can make the heartbeat mandatory.
- **[medium]** The path without any AI does not say what degrades (Section 7 "Without external AI", FR-11, FR-19, SM-5, Q15). "Explains with templates instead of AI" works for catalogue entries. FR-19, however, requires Nightshift to explain problems "in neither catalogue … with the evidence it has", and templates cannot be written in advance for unknown problems. The in-cluster fallback applies "if their hardware can run it", but whether a 24 GB or 96 GB model is "useful enough" is still [To test] (Q15), and nothing says who decides which path a cluster is on. *Fix:* add two lines. One: without AI, new problems get a structured evidence summary (observed signals, the closest catalogue entries, "cause unknown"). Two: the in-cluster model is used only if it passes the Q15 tests, otherwise the cluster runs without AI. Report SM-5 separately for each path.
- **[low]** "Degraded" in the heartbeat is undefined (FR-6). An agent reporting "degraded" to Fleet is a new status with no trigger and no Fleet response. *Fix:* define it (for example, "independent self-checks in FR-4 failing") and say whether Fleet alerts on it.
- **[low]** "Materially changed" is the only test for asking again (FR-22, fourth bullet). This governs when an approval given becomes invalid, which matters more now that approvals also expire. *Fix:* tie it to the approval's binding in the Glossary ("repair, target, catalogue version and evidence shown"): any change to those invalidates the approval.

## Scope honesty — strong

The deferral is explicit and sourced in two places: "Deferred: Nightshift does not execute dangerous repairs in the first version" (3.1), and the matching Non-goal (3.2). PRIV-9's "Without Fleet reports" spells out what a privacy-maximal customer loses. FR-21's caveat that the double approval for the customer's own app is "not a rule he has confirmed" is the kind of honesty the rubric asks for. The gap is that open items the update itself creates were not logged.

### Findings
- **[medium]** Open items created by the update are not in Section 10. The update creates several decisions it leaves open:
  - who performs a dangerous repair (FR-52);
  - how long a rejection blocks a repair (FR-50);
  - the default channel permissions (PRIV-9);
  - the meaning of "degraded" (FR-6);
  - who maintains the platform on alert-only clusters (FR-51).

  Section 10 adds only items 18 (approval validity) and 21 (double approval). *Fix:* add those that the fixes above do not settle to "Design decisions still open", each with an owner.
- **[low]** A first-version deferral sits under the heading "what Nightshift never does" (3.2, "Execute a dangerous repair in the first version (FR-52)"). Every other Non-goal there is permanent. This one is time-bound and already stated in 3.1. *Fix:* move it out of 3.2, or retitle 3.2 "Non-goals".

## Downstream usability — adequate

The new Glossary entries ("Platform repair", "Agreed management policy", "External AI", "No outbound data", "Expected interruption", "Harmful repair") are good and are used consistently in their home FRs. The distinction between the maintenance policy and the management policy is drawn explicitly in the Glossary, which pre-empts an obvious confusion. Cross-references to the new items resolve (FR-22 → Q18, FR-21 → Q21, PRIV-9 → FR-6, NFR-4 → PRIV-9). The weakness is that the list of ways a repair can be authorised now differs between sections, and several FRs written for the old one-axis table were not updated.

### Findings
- **[medium]** The ways a repair can be authorised are listed differently in each place (FR-21, FR-23, FR-34, SEC-9, FR-47, Glossary "Alert-only mode"). There are now five: tick, agreed management policy, approval at the time, last-resort permission, and maintenance or rollback policy.
  - SEC-9 lists all five.
  - FR-23 omits the maintenance and rollback policy.
  - FR-34's "who permitted it (ticked, in the agreed management policy, or approved at the time…)" omits last-resort and the maintenance and rollback policy.
  - FR-21's table does not show where FR-47's rollback policy sits. UJ-5 has Josh approve and then lets pre-authorised customers' rollbacks run, while FR-21's "risky, ticked" cell would also require Orvex approval each time.
  - The Glossary says FR-47 maintenance is "not [a] Nightshift change", yet FR-32 has the update path roll back and FR-47 counts updates toward SM-4.

  Architecture will model the executor's checks (SEC-8) from this, and FR-34 records will be audited against it. *Fix:* define the set once (Glossary "Authorisation basis", listing all five) and reference it from FR-21, FR-23, FR-34 and SEC-9. Add one line to FR-21 placing FR-47's policies relative to the table.
- **[medium]** Several FRs were not updated to the two-row table (FR-24, FR-27, FR-12, Section 2, Glossary "Orvex technical approval").
  - FR-24 limits last-resort to "repairs the customer is allowed to tick", so it is silent on risky platform repairs, where no customer tick exists and Orvex approval at the time is required.
  - FR-27 still says that if the next repair is not safe, "it asks for Orvex technical approval". If the next repair is dangerous, it is now manual (FR-52), and if it is a safe policy repair it runs without asking.
  - FR-12 and Section 2 say the Nightshift team approves "risky repairs", omitting safe platform repairs that are not in the policy.
  - The Glossary says Orvex technical approval on customer production "comes in addition to the customer's approval". That is false for safe repairs and for ticked risky ones.

  *Fix:* update the four sentences, and state in FR-24 whether Orvex can grant last-resort for risky platform repairs.
- **[medium]** FR-34's outcomes do not match the addendum's statuses or the new flows (FR-34, addendum "For the UX", FR-52, Glossary "Harmful repair").
  - FR-34 lists "worked; did not work and undone; failed; blocked; cancelled; recovery failed; harmful". The addendum's repair statuses are "Succeeded / Failed / Rejected / Blocked / Cancelled / Expired" plus "Manual repair needed".
  - "Failed", "did not work" and "recovery failed" are not distinguished.
  - There is no outcome for a repair that did not work and could not be undone (for example, a restart, which the Glossary and FR-27 both mention), and none for a manual repair that a person reports as done (FR-52).

  UX and the SM-2 and SM-3 counts will read from this list. *Fix:* give one outcome list with a one-line definition each, map it to the UX statuses, and add "did not work, not undoable" and "performed manually".

## Shape fit — adequate

The UJs were updated where the new rules touch them. UJ-2 and UJ-3 now go through the portal, and UJ-5's edge case now cites Exchange 5. But the shape gap from the last review has grown, and none of the new flows appear in any journey.

### Findings
- **[high]** No journey shows the customer setting permissions (carried over, made worse; Glossary "Advance permission", PRIV-8, PRIV-9, FR-51, SEC-7). The settings surface the previous review listed now also holds:
  - external-AI consent with nothing preselected and a provider disclosure (PRIV-8);
  - a permission per outbound channel, with consequences the UX must explain (PRIV-9, FR-6);
  - the agreed management policy, which the customer "can read … in the portal" (FR-51).

  The addendum gives draft wording for the consent screen, but no journey tells the wireframes when a customer meets these choices or what they see after refusing them. *Fix:* as before, add a UJ with a named business owner onboarding a cluster. Include the consent screen, one channel refused (with the resulting "Heartbeat not permitted by the customer: status unknown" in Fleet), and one re-tick after a release.
- **[medium]** None of the new flows appears in a journey (FR-50, FR-51, FR-52, FR-22). No UJ "Realises" FR-50, FR-51 or FR-52, and none shows an expired approval. Rejection, a manual dangerous repair handed to a person, and a platform-only repair the customer sees only in the morning summary are each new screens or messages for the wireframes. *Fix:* add edge cases to existing UJs instead of new UJs. For example, UJ-2: Cris rejects, and the request is blocked and the Orvex team notified. UJ-3: the approval expires and Nightshift asks again. UJ-4: Samira's summary lists a policy repair and a "manual repair needed" item.

## Mechanical notes

- **ID continuity:** the FR IDs are unique and the set FR-1 to FR-52 is complete. Section 1's "FR-1 to FR-52" is accurate. The new IDs are out of document order, though: FR-52 sits in 5.4 between FR-20 and FR-21, and FR-50 and FR-51 sit in 5.5 after FR-24. Likewise PRIV-8 and PRIV-9 come before PRIV-7. Keeping IDs stable is the right call. Consider a one-line note under "How this PRD is organised" saying that IDs are stable, not sequential.
- **FR-42 list broken:** the new paragraph "The testing and the engineer's review of the patch …" is inserted between steps 5 and 6. Markdown restarts the list, so the paragraph also reads as a separate rule rather than a note on steps 2 and 3. Move it below step 6.
- **FR-12 stale phrase:** "Either way, Orvex receives a signal…" followed the old two-case routing. It now follows four cases. Say "In every case".
- **Glossary drift:**
  - "Orvex approval" (Glossary "Approval": "only Orvex approves"; FR-12: "needs only Orvex approval") and "Orvex technical approval" (FR-21 table) refer to the same thing. Use the defined term.
  - "managed-service contract" (FR-51, Glossary "Agreed management policy") is not the Glossary's "Customer contract". Use "customer contract", or define the relation.
  - "a mode without any AI" (3.1) suggests a third mode beside alert-only and approval-enabled. Section 7 treats it as a fallback, so say "working without any AI".
  - "in-cluster dashboard" (FR-15, PRIV-9) is a new surface with no Glossary entry and no stated relation to the FR-15 dashboards reached through the portal.
- **Assumptions:** SM-7's assumption and Q4 are now resolved by Exchange 5, so two inline assumptions are gone. The two "[DESIGN ASSUMPTION unless Danny confirms]" tags are unchanged and still not indexed (not worse). The new "provisional design" tag in FR-21 is correctly mirrored as Q21.
- **UJ realisation lists:** UJ-5 still "Realises FR-6, FR-32", although its edge case now leans on FR-21 and FR-47 (from the previous review; slightly worse, since the edge case grew). UJ-2's edge case cites FR-21, but its list does not include Q21's provisional status.
- **Addendum:** the "For the UX" section is accurate against FR-6, PRIV-8 and PRIV-9, but its repair status list conflicts with FR-34 (see Downstream usability). The note "Now a PRD requirement" on "Working without a model" correctly points to Section 7.
- **Required sections:** all still present.
