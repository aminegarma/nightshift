# Triage of the 2026-11-03 Update reviews

Sources: `review-update2-rubric.md` (0 critical, 3 high, 7 medium, 5 low), `review-update2-adversarial.md` (1 critical, 7 high, 11 medium, 7 low), `reconcile-ux-2026-11-03.md` (6 missing, 5 contradicted). None of them blocks the UX, which is already final.

## Part 1: decisions for Amine (asked separately)

- **D1. Revocations versus enforcement in the cluster** (adversarial critical; high on portal-off). A withdrawal, a switch to alert-only or an untick is made in the portal, but the executor in the cluster enforces approvals. A cluster that is cut off could still run a repair whose approval was withdrawn.
- **D2. Pre-ticked onboarding channels called "explicit" permission** (adversarial high). The reviewer cites the EU court's Planet49 ruling (C-673/17, 2019): a pre-ticked box is not valid consent. The onboarding confirmation could also be made by an installer rather than the customer.
- **D3. Strict no-outbound deployment** (adversarial high; rubric medium). The PRD names it but never defines it: how it gets releases, the catalogue, the fleet-wide switch-off and policy versions.
- **D4. An inconclusive pre-start check** (adversarial high). If a node is unreachable, Nightshift can't confirm the evidence, so a dangerous repair can never be done inside the record, and the work happens outside it.

## Part 2: fixes that follow existing decisions (one yes/no)

1. **Group approval (FR-32; rubric and adversarial high; reconcile):**
   - The Glossary "Approval" gets a single, named exception for FR-32.
   - A group approval covers one repair at one catalogue version, for a set of clusters frozen and shown at the click. Clusters that join later need a new approval.
   - It is recorded per cluster, and each cluster is re-checked.
   - Waves stop on the stop conditions of FR-46 and FR-47.
   - It never covers a manual dangerous repair.
   - Its validity per wave follows the catalogue entry. [Accepted UX rule: targets frozen and displayed]
2. **Two people for a dangerous repair (FR-52; rubric and adversarial high).** The person who performs a manual dangerous repair is never the one who gave Orvex technical approval or reviewed the recovery plan. [Accepted UX rule: two different people where two approvals are required]
3. **FR-51 scope (rubric and adversarial high):**
   - A change "within the agreed scope" keeps the same repair entries and the same or narrower actions, targets and conditions, and may correct steps without widening what they do.
   - Anything else expands permissions and needs the customer's acceptance.
   - The customer can dispute a classification, as in FR-21; until Orvex has reviewed it again, the change is treated as expanding.
   - The "adds production impact" branch is replaced by: "a repair that can affect customer production leaves the policy and follows FR-21".
   - Amine's correction #29 is kept.
4. **Manual-repair window (FR-52; reconcile):**
   - The window limits when work may start; work already in progress when it ends is finished or recovered under the reviewed plan, never abandoned. [Accepted UX design proposal]
   - A review that materially changes the recovery plan asks the customer again.
5. **Timing words that need a bound (rubric medium):**
   - "Undo reject" is available for a short, fixed window, and the other approvers are notified when it ends. The length is [OPEN: architecture].
   - For FR-24, "nobody answers" means no decision on the open request by the time failure is predicted within about 30 minutes.
   - Withdrawing an approval takes effect as decided in D1.
6. **Stale PRD text (reconcile):**
   - FR-15 "If the customer permits no outbound channel" → "In a strict no-outbound deployment (see D3)".
   - UJ-1's climax: undo "where the repair can be undone".
   - UJ-2: "Cris is told that Orvex technical approval is still needed" instead of "Orvex is checking it".
7. **Records and settings (reconcile):**
   - FR-34 "who permitted it" adds the last-resort condition and the policy version.
   - SEC-7's list of what only administrators can change adds accepting a policy change, source-code consent (FR-43) and disputing a classification.
   - Among several customer administrators, the server orders decisions, and a later withdrawal or rejection before execution still counts. [Accepted UX rule]
8. **Mechanical (rubric):**
   - One term: "pre-run check".
   - "Heartbeat" is used for two things: FR-2's node heartbeat and FR-6's Fleet heartbeat, so they are named apart.
   - Section 10 item 8 cites FR-15.
   - Frontmatter and the status line are updated at close.
9. **UX spine tidy-up (reconcile):**
   - Remove "[ASSUMPTION: proposal, to confirm]" from the portal-off rule, which Amine has confirmed.
   - Change the "pending PRD change" markers to "in the PRD (2026-11-03)".
   - A repair on a cluster with stale data shows as "Unknown: no data since 02:10", not "Blocked", because local enforcement keeps running (NFR-5, SEC-8).
