# Memlog audit: `.memlog.md` against `prd.md` and `addendum.md`

Audit date: 2026-10-30. Read-only audit; no existing file was changed.
Scope: every memlog entry of type decision, override, change or assumption (143 entries). The 12 "event" entries (lines 6, 24, 25, 43, 51, 71, 72, 73, 78, 105, 141, 148) are skipped.
"L" = line number in `.memlog.md`.

## Counts

| Class | Count |
|---|---|
| CAPTURED | 119 |
| SUPERSEDED | 10 |
| CONFLICT | 5 |
| MISSING | 3 |
| N/A (process, or a change to other files; no PRD content expected) | 6 |
| **Total** | **143** |

## Audit table (CONFLICT and MISSING first)

| L | Type | Gist | Class | Where / why |
|---|---|---|---|---|
| 77 | override | Catalogue split is for safety: repair catalogue = tested fixes; incident catalogue = fix not yet tested, still under investigation (replaces L66 rationale) | CONFLICT | Captured in Glossary "Repair catalogue", but Glossary "Incident catalogue" still carries L66 wording: entries "may reference zero or more repairs". Under L68/L77/L79 a problem with known repairs lives in the repair catalogue, and FR-19 says nothing in the incident catalogue is repaired. |
| 82 | decision | Fault / failure / incident defined; incident = user-facing disruption; replaces "one failure, however many alerts" | CONFLICT | Defined in Glossary, but old broad sense of "incident" survives: SM-2 "without causing another incident" (should be problem; a repair can cause a fault or failure users don't see yet) and 3.11 description "incident escalation" (FR-45 itself says fleet-level escalation of problems). |
| 86 | decision | Risk level is per repair; one problem can have several repairs of different risk | CONFLICT | Glossary "Risk level" and FR-25 follow it, but Glossary "Repair catalogue" still says "Every entry defines the action, its safety preconditions, risk level..." (one action, one risk per entry, from L66). Since L74 an entry is per problem and holds several repairs. |
| 88 | decision | Say "supported problem(s)", not "supported incidents" | CONFLICT | Vision and Glossary "Supported problem" follow it, but Glossary "Incident catalogue: the list of supported incidents" was not updated. |
| 160 | override | Never act on silence = silence grants no new permission; an already authorised repair (ticked or last-resort) may still run when nobody answers. Non-goal: never modify/delete customer records, databases, backups | CONFLICT | Applied in 9.2, FR-22 and Glossary "Prohibited action". Not applied in Glossary "Approval" ("No answer is never a yes: Nightshift changes nothing...") or FR-14 (the request "says that, without an answer, Nightshift changes nothing"), which is wrong for a risky repair under the last-resort condition (FR-23). |
| 27 | decision | Danny: Nightshift keeps the whole stack healthy; detects disk/NIC/PSU, L2/L3, misconfig, K8s; assume customers have little infra expertise **and badly configured hardware**; takes over after installation and validation | MISSING (partial) | Detection list in FR-1, take-over in FR-7, low expertise in Users and NFR-8. The design assumption "customer hardware is often badly configured" appears nowhere (no assumption, NFR or open question). |
| 44 | assumption | AI reading: Danny's provider mention is where Quornex Fleet runs, i.e. bare-metal servers under OMK, not hosted K8s like EKS | MISSING | Glossary "Quornex Fleet" only says "on a hosting provider"; the bare-metal-under-OMK reading is not in the PRD, addendum or open questions. Belongs in addendum "For the architecture" as an unconfirmed reading. |
| 136 | assumption | Open points in 3.10; defend point: few customers will have in-cluster GPUs, so the code-fix experiment sample may be small | MISSING (partial) | The two open points were resolved (L137, L138; FR-40, FR-43). The small-sample risk is not mentioned in FR-41, FR-42, Section 9 or Section 10, though it directly limits what FR-42 can conclude. |
| 7 | decision | Stakes high: graded deliverable, Amine must defend every requirement | N/A | Process. Reflected indirectly by source tags and [AI] markers. |
| 13 | decision | After PRD: validate, then bmad-ux, then bmad-architecture | N/A | Process. Consistent with addendum "For the architecture" and FR-30 "to feed the UX wireframes". |
| 35 | change | Inputs updated: danny-qa Exchange 4, extract files, checklist U1, brief correction note | N/A | Changes to other files. |
| 41 | change | Memlog line 28 hand-redacted (provider name) | N/A | Change to the memlog itself. |
| 42 | change | Brief corrected after finalisation (OMK ground rule, control cluster, hardware scope) | N/A | Changes to the brief. PRD wording is consistent with the corrected brief. |
| 107 | decision | Working mode for the rest: mixed (AI drafts some sections, coaching for others) | N/A | Process. Reflected by "[DRAFTED FROM THE RECORD]" markers. |
| 14 | decision | Entry point Vision + Features; AI to propose 3 section orders | SUPERSEDED | By L18/L19 (Order B chosen). |
| 29 | assumption | Possible conflict: Danny's "safe automatic" vs brief advance permission; who approves OMK/Quornex changes; data to control cluster | SUPERSEDED | By L37, L87 (FR-20) and L142 (PRIV-1). Residual "who approves OMK/Quornex changes" kept as Section 10 Q1. |
| 36 | assumption | brief.pdf "our bare metal" vs Exchange 4; logged as open question 6 | SUPERSEDED | By L49; Glossary "Platforms" follows L49; open question removed (Q6 is now about trusted hosted models). |
| 56 | change | Vision rewritten as draft v2 | SUPERSEDED | By L58 (Vision v3). |
| 64 | decision | Advance permission set by contract, not settings; two types of allowed repairs (automatic / Orvex technical approval) | SUPERSEDED | Contract part overridden by L69; two-types part refined by L80/L87. PRD follows the later entries (Glossary "Advance permission", FR-20). |
| 66 | decision | Two catalogues; entries reference zero or more repairs; rationale "separates recognising from permission"; "understood 100% gains a repair" | SUPERSEDED | By L68, L74, L77, L86. PRD follows them, except residue flagged under L77 and L86. |
| 67 | assumption | Possible conflict: Exchange 1 tick list vs contract | SUPERSEDED | Resolved by L69 and L75 (Glossary "Advance permission", "Customer contract"). |
| 83 | assumption | Naming tensions: incident catalogue vs incident definition; 250-a-night meaning; risk per problem vs per repair | SUPERSEDED | Resolved by L84, L85, L86. |
| 104 | assumption | AI additions in 3.2 to confirm | SUPERSEDED | Accepted in L106 (FR-8, FR-9 bullets). |
| 112 | assumption | Contradiction: Nightshift team vs support as Orvex's approver | SUPERSEDED | Resolved by L113 (Nightshift team only). |
| 8 | decision | Coaching path; every decision links to its source | CAPTURED | Source tags throughout the PRD. |
| 9 | decision | Danny input only from recorded exchanges; unanswered follow-ups stay open | CAPTURED | Section 10 "For Danny (not yet asked unless stated)"; danny-qa references in Q1-Q3. |
| 10 | decision | PRD must settle 5 things (risk vs authority; permissions/approval/Orvex review; no answer/failed repair/Nightshift down; privacy and metrics; v1 scope incl. code fixes) | CAPTURED | Glossary risk levels + 3.5; FR-22, FR-26/27, FR-29, NFR-4, FR-6; Section 4, Section 8; Section 9, 3.10. |
| 11 | decision | Careful areas: approval, multi-cluster, privacy, cost | CAPTURED | 3.5, 3.7, 3.11, 4.1, 4.3. |
| 12 | override | Codex verified only some research claims; keep uncertainty markings, verify where it matters | CAPTURED | Section 5 GPU price note; Section 8 header; Section 10 "To test" 13-17; FR-8/9/10 source headers. |
| 15 | decision | Risk scale safe / risky / dangerous; prohibited is a rule, not a level | CAPTURED | Glossary "Risk level", "Prohibited action". |
| 16 | decision | Runs in each cluster; Quornex portal; dashboards per cluster and per 100 clusters | CAPTURED | Vision; FR-15. |
| 17 | decision | Must cover approval boundaries, code fixes, cross-cluster privacy, monitoring blind spots | CAPTURED | 3.5; 3.10; PRIV-1; FR-3, FR-5, FR-7. |
| 18 | change | Order B re-issued with repair catalogue, risk and authorisation explicit | CAPTURED | Sections 3.4 Choose a repair, 3.5 Authorise. |
| 19 | decision | Section order: Order B | CAPTURED | PRD structure, Sections 1-10 (3.11 added per L46/L50). |
| 20 | decision | Fleet learning gate: new fix enters catalogue only once found, tested, well controlled | CAPTURED | FR-19, FR-35, FR-38. |
| 21 | decision | Vision in Amine's words | CAPTURED | Vision. (Wording defect: "replaces much of the DevOps work that would otherwise need," is missing its object.) |
| 22 | decision | v1 must prove four things | CAPTURED | Vision list; item 2 "100% explainable" softened by L58, which the PRD follows. |
| 23 | decision | Grouped 100-cluster dashboards for Orvex; customer combined dashboard, data kept safe | CAPTURED | FR-15; PRIV-4. |
| 26 | decision | Customers own their hardware; OMK manages OS + K8s; on EKS provider owns K8s and infra | CAPTURED | Glossary "Platforms", "Customer hardware", "OMK", "Hosted Kubernetes". No "Orvex's bare metal" wording remains. |
| 28 | decision | Three levels: agent per cluster, management agent on control cluster, Quornex Fleet; each cluster self-sufficient | CAPTURED | Glossary; 3.7; FR-6; NFR-5. |
| 30 | change | Vision scope phrase changed to customer hardware under OMK | CAPTURED | Vision para 1. |
| 31 | decision | Glossary distinguishes Fleet / control cluster / workload clusters | CAPTURED | Glossary. |
| 32 | decision | Danny's model, but every agent keeps working locally if management agent / control cluster / link is down | CAPTURED | 3.7; FR-28; NFR-5. |
| 33 | decision | Hardware detection does not imply physical repair; define mitigate / report uncertainty / escalate | CAPTURED | 3.4 "Hardware faults". |
| 34 | decision | Coordination does not let private data leave its cluster; control-cluster boundary needs decision | CAPTURED | PRIV-1; Section 10 Q3. |
| 37 | decision | "Safe repairs automatic" = runs automatically once permitted in advance | CAPTURED | FR-20 (safe + ticked); Orvex part resolved by L87. |
| 38 | decision | Hardware provider only via the customer | CAPTURED | 3.4 "Escalate to the hardware provider"; 9.2. |
| 39 | decision | Single-cluster customer: no control cluster, agent connects only to Fleet | CAPTURED | 3.7 last bullet, labelled design assumption (per L47). |
| 40 | decision | Public repo: say "a hosting provider" | CAPTURED | Glossary "Quornex Fleet"; addendum. No provider name in PRD. |
| 45 | decision | Amine's reading: customer replaces hardware; OMK on bare metal; Quornex services; Fleet hosting ≠ customer apps; respect EKS provider | CAPTURED | Glossary "Customer hardware", "Quornex", "Quornex Fleet", "Hosted Kubernetes". |
| 46 | decision | 10,000 clusters across customer environments; local autonomy + fleet management (safe updates, escalation, isolation, low cost); 3.11 placeholder | CAPTURED | 3.11 FR-44 to FR-47; Vision. "Not on Orvex's servers" part softened by L58, which the PRD follows. |
| 47 | change | Design-assumption labels: Fleet internals, single-cluster model, cross-cluster data sharing | CAPTURED | Glossary "Quornex Fleet"; 3.7 last bullet; Section 10 Q3 for PRIV-1. |
| 48 | decision | Provider name is Danny's private data; architecture may name it | CAPTURED | Addendum "Hosting provider". |
| 49 | decision | Platforms wording; replaces brief.pdf vs Exchange 4 open question | CAPTURED | Glossary "Platforms" (verbatim). |
| 50 | decision | Keep 3.11 placement | CAPTURED | 3.11. |
| 52 | decision | 3.4 hardware accepted with changes (mitigate on matching evidence; fault open until customer confirms; double-check before closing) | CAPTURED | 3.4 "Hardware faults". |
| 53 | decision | Raw data and secrets never leave; outbound line check | CAPTURED | Vision; PRIV-2; PRIV-3. |
| 54 | decision | Zero harm is a goal, every harmful repair counted and reviewed | CAPTURED | Vision; SM-3; FR-34. |
| 55 | decision | Customers run their own cloud at low cost, public-cloud-like, control over data and compute | CAPTURED | Vision para 2. |
| 57 | decision | Catalogue entry says what evidence is enough; matching is not a guess | CAPTURED | FR-18; 3.4 "Mitigate". |
| 58 | change | Vision v3 (OMK vs EKS access; customer environments; evidence-based explanations, states uncertainty) | CAPTURED | Vision ("supported problems" per L88). |
| 59 | decision | Safe repair: no interruption or data loss; e.g. disk cleanup | CAPTURED | Glossary "Safe repair". |
| 60 | decision | Customer production definition; changes need customer approval | CAPTURED | Glossary "Customer production" ("by contract" replaced by settings checklist per L69). |
| 61 | decision | Supported problem includes unrepairable ones (power, NIC, disk) | CAPTURED | Glossary "Supported problem". |
| 62 | decision | Risky repair definition + memory-creep example | CAPTURED | Glossary "Risky repair". |
| 63 | decision | Dangerous repair definition | CAPTURED | Glossary "Dangerous repair". |
| 65 | decision | Disk cleanup = allowlisted disposable files with limits | CAPTURED | Glossary "Disk cleanup". |
| 68 | override | Fully understood problem moves from incident to repair catalogue | CAPTURED | Glossary "Repair catalogue"; FR-35. |
| 69 | override | Tick list is in the settings for all customers; contract is something else | CAPTURED | Glossary "Advance permission", "Customer production"; UJ-3. No "contract" wording left for the tick list. |
| 70 | decision | Vision keeps local autonomy incl. when control cluster coordinates many clusters | CAPTURED | Vision para 2. |
| 74 | decision | Evidence and explanation live in the repair catalogue entry after the move | CAPTURED | Glossary "Repair catalogue"; FR-35. |
| 75 | decision | Customer contract = price, period, privacy, hardware responsibility, services; not the checklist | CAPTURED | Glossary "Customer contract". |
| 76 | change | Glossary drafted: approval, Orvex technical approval, last resort, incident; "fault" proposed | CAPTURED | Glossary "Approval", "Orvex technical approval", "Last-resort condition"; incident definition replaced per L82. |
| 79 | decision | Known but never-Nightshift-fixable problems go in the repair catalogue; Nightshift suggests the fix | CAPTURED | Glossary "Repair catalogue". |
| 80 | decision | Risky repairs also need Orvex technical approval; safe ones automatic | CAPTURED | Glossary "Orvex technical approval"; FR-20. |
| 81 | decision | Customer ticks once from the catalogue | CAPTURED | Glossary "Advance permission"; FR-20. |
| 84 | decision | Keep catalogue names; fault/failure/incident treated alike; "problem" umbrella term | CAPTURED | Glossary "Problem". |
| 85 | decision | 250 a night = problems of all types; false alerts not counted | CAPTURED | NFR-1. |
| 87 | decision | Authorisation table by risk level and tick | CAPTURED | FR-20. |
| 89 | decision | Last resort only if the customer ticks it; Orvex never applies it alone | CAPTURED | Glossary "Last-resort condition"; FR-23. |
| 90 | decision | Heartbeat first; verify with neighbours; then infrastructure | CAPTURED | FR-2, FR-3. |
| 91 | decision | Self-monitoring: heartbeat, freshness, checker independent of Prometheus, monitoring failure case | CAPTURED | FR-4; addendum (Prometheus). |
| 92 | decision | Invisible resources reported; collect what's possible; detect symptoms | CAPTURED | FR-5. |
| 93 | change | 3.1 drafted; addendum created | CAPTURED | 3.1; addendum. |
| 94 | decision | Fleet as external watchdog | CAPTURED | FR-6. |
| 95 | decision | Three levels of monitoring | CAPTURED | FR-6 table; open point resolved by L100. |
| 96 | decision | Out-of-band management required; installation validates it | CAPTURED | FR-7; Glossary "Out-of-band management". |
| 97 | assumption | OOB credentials are a security risk; belongs in Section 4 | CAPTURED | SEC-2 (hardware credentials row); SEC-3. |
| 98 | decision | No OOB = limited-visibility mode, acknowledgement, coverage report | CAPTURED | FR-7; Glossary. |
| 99 | decision | Hardware credentials not stored in agents | CAPTURED | SEC-3. |
| 100 | decision | Every agent sends its own "I'm alive" to Fleet | CAPTURED | FR-6 bullet. |
| 101 | decision | FR-8 predictable-problems table | CAPTURED | FR-8. |
| 102 | decision | FR-9 four alert factors, actionability final | CAPTURED | FR-9. |
| 103 | decision | FR-10 keeping predictions honest | CAPTURED | FR-10. |
| 106 | decision | 3.2 additions accepted; customer may take full care of own infra | CAPTURED | FR-8 bullets; FR-9 bullets. |
| 108 | change | 3.3 drafted FR-11 to FR-16 | CAPTURED | 3.3. |
| 109 | decision | Visible ≠ notified; team not paged for safe problems | CAPTURED | FR-12. |
| 110 | decision | Orvex's approval given by the Orvex Nightshift team | CAPTURED | FR-12; Section 6 Users. |
| 111 | decision | Routing follows the approval table; Orvex signalled on customer confirmations | CAPTURED | FR-12 routing; FR-34. |
| 113 | decision | Orvex approval from the Nightshift team only; support not involved | CAPTURED | FR-12; FR-26; Users. Loose wording elsewhere: see observations. |
| 114 | change | 3.4 general part FR-17 to FR-19; hardware wording uses repair catalogue | CAPTURED | 3.4. |
| 115 | decision | Always lowest-risk repair expected to work | CAPTURED | FR-18; FR-25. |
| 116 | decision | Orvex approves risky each time; unticked needs yes at the time; last resort only tickable repairs | CAPTURED | FR-20; FR-23. |
| 117 | decision | ~15 Nightshift engineers for 10,000 clusters | CAPTURED | SM-8; Users; Section 10 Q13. |
| 118 | decision | Nobody answers at 3 AM: do nothing unpermitted, keep monitoring; possible call for dangerous | CAPTURED | FR-22 (as amended by L160). |
| 119 | decision | Ticked = valid until unticked; on-request yes = one time | CAPTURED | FR-21. |
| 120 | change | 3.5 drafted FR-20 to FR-23 | CAPTURED | 3.5. |
| 121 | decision | One engineer on duty; repair waits, re-alert, call if critical; re-check preconditions, no timers | CAPTURED | FR-21; FR-22. |
| 122 | decision | Last resort is for risky repairs; Orvex advance permission replaces the team's run-time yes | CAPTURED | FR-23. |
| 123 | decision | Reason for ~15 engineers; share needing a team yes to test | CAPTURED | SM-8; SM-9. |
| 124 | decision | Failed repair: next runs automatically only if safe; else team approval | CAPTURED | FR-26. |
| 125 | decision | Repair coordinator prevents conflicting repairs | CAPTURED | FR-28. |
| 126 | decision | Rank by safety, success, impact; worse = rollback, stop, call a person | CAPTURED | FR-25; FR-27. |
| 127 | change | 3.6 drafted FR-24 to FR-28 | CAPTURED | 3.6. |
| 128 | decision | Crash mid-repair: save progress, keep marks, check real state | CAPTURED | FR-29. |
| 129 | decision | Fleet-wide failure: one consolidated alert; Fleet stops update; risky repairs wait | CAPTURED | FR-30. |
| 130 | change | 3.7, 3.8, 3.9 drafted; fleet-learning pipeline to addendum | CAPTURED | 3.7-3.9; addendum. |
| 131 | decision | FR-30 example consolidated alert | CAPTURED | FR-30 example. |
| 132 | decision | AI additions accepted (per-cluster coordinator, no chained approvals, record reads, append-only record, tested release) | CAPTURED | FR-28; FR-26; FR-31; FR-33; FR-38. |
| 133 | decision | Code fixes follow the repair path | CAPTURED | FR-40. |
| 134 | decision | Code fixes only with in-cluster GPU model | CAPTURED | FR-41; PRIV-5. |
| 135 | decision | Code-fix experiment metrics | CAPTURED | FR-42. |
| 137 | decision | Non-reusable fixes as customer-specific catalogue entries | CAPTURED | FR-40; Glossary "Customer-specific entry". |
| 138 | decision | Code-fix testing in isolated in-cluster environment | CAPTURED | FR-43. |
| 139 | change | 3.10 complete; 3.11 drafted | CAPTURED | 3.10 (FR-43 OPEN; Section 10 Q11); 3.11. |
| 140 | decision | Staged rollout; customer isolation in Fleet | CAPTURED | FR-44; FR-46. |
| 142 | decision | Private data stays in originating cluster even within one customer; placeholders; strict = time and type only | CAPTURED | PRIV-1; PRIV-2; PRIV-4; 9.2. |
| 143 | decision | Log text is evidence, never instruction; rule-based check authorises | CAPTURED | SEC-1. |
| 144 | decision | Compromised agent: four isolation requirements | CAPTURED | SEC-2. |
| 145 | change | 4.1 and 4.2 drafted; FR-15 updated | CAPTURED | 4.1 (now PRIV-1 to PRIV-6); 4.2; FR-15. |
| 146 | decision | Hosted model gets approved, sanitised fields; time-and-type for max privacy | CAPTURED | PRIV-2 bullet. |
| 147 | decision | Proving privacy: inspectable record, planted-secret tests, outside audit | CAPTURED | PRIV-6. |
| 149 | decision | Model data boundary: shared GPU = hosted boundary; not necessarily Orvex-run | CAPTURED | Section 5 table. |
| 150 | decision | Cost: technical vs total operating cost; GPU full cost; who pays | CAPTURED | COST-1; COST-2; COST-3. |
| 151 | change | 4.3 and Section 5 drafted | CAPTURED | 4.3; Section 5. |
| 152 | decision | User journeys UJ-1 to UJ-3 | CAPTURED | Section 6. |
| 153 | change | Section 6 drafted with AI additions | CAPTURED | Section 6 ([AI] markers). |
| 154 | change | UJs accepted; Sections 7 and 8 drafted | CAPTURED | Sections 7, 8. |
| 155 | decision | NFR-4 accepted; NFR-6 measures CPU, RAM, storage, network, AI/GPU | CAPTURED | NFR-4; NFR-6. |
| 156 | decision | "Explained" = three checks | CAPTURED | SM-5. |
| 157 | decision | Night: one engineer + 2-3 remote backups | CAPTURED | SM-8. (Users and FR-22 mention only the one engineer.) |
| 158 | decision | Counter-metrics in Amine's words | CAPTURED | SM-C1 to SM-C3. |
| 159 | change | Sections 9 and 10 drafted; old questions resolved | CAPTURED | Sections 9, 10 (Q3 keeps PRIV-1 to confirm with Danny). |

## Other observations (not tied to a single entry)

- **Who gives Orvex approval (L110, L113):** FR-12, FR-20 and Users say the Orvex Nightshift team, but the FR-30 responsibilities table says "An Orvex engineer", and Glossary "Orvex technical approval" / "Advance permission" say "the Orvex team". Not contradictory, but loose; tighten to "the Orvex Nightshift team".
- **"Contract" (L69, L75):** FR-12 "Orvex support is told when the customer's contract says so". Plausible (support is a service term), but check it is not leftover from the contract/settings mix-up.
- **What leaves a cluster (L53, L142):** FR-36 says "raw logs and secrets never do"; Vision and PRIV-2 say "raw data and secrets". Align FR-36. FR-6 "only liveness information goes to Fleet" is still marked [AI, to confirm].
- **Stale status markers:** frontmatter `updated: 2026-10-29`, though Sections 4-10 are dated 2026-10-30. Glossary header still says "the Glossary section itself is still to be worked through", but it was worked through in L59-L89. 3.3, 3.4, 3.8, 3.9 and 3.11 still say "for Amine's one-pass review", but L113, L116, L132 and L140 record them as complete. No memlog entry records Amine accepting the Vision as a whole (the next step in L72).
- **Numbering:** in 3.10, FR-43 comes before FR-42.
- **Vision sentence defect:** "replaces much of the DevOps work that would otherwise need, and makes..." is missing its object.
- **Unconfirmed [AI] items still in the text:** 3.4 (provider evidence package; EKS escalation) and UJ edge cases.
