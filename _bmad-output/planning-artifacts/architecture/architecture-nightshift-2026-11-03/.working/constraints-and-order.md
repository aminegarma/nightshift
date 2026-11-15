# Key constraints and decision order (2026-11-03)

Working note for the architecture run. Built from prd.md (final 2026-11-03), the PRD addendum, EXPERIENCE.md open items O-1 to O-13, open-items-2026-11-03.md, the UX validation report and danny-qa-summary.md. Settled product decisions are inherited, not reopened.

## 1. Constraints the architecture inherits

### Shape
- Three levels, each watched from outside itself: a Nightshift agent per workload cluster; an optional management agent on the customer control cluster (which also runs its own agent); Quornex Fleet at Orvex as the external watchdog (FR-6).
- Each cluster looks after itself when the control cluster or Fleet is unreachable. Repairs across clusters wait (FR-29, NFR-5).
- One release and configuration everywhere. Customers differ only in permissions and settings (NFR-3). One design for OMK and EKS (NFR-2).

### Trust boundaries
- The agent that reads untrusted data is read-only. A separate executor holds change rights and checks authorisation, preconditions and risk itself. All outbound data goes through a separate gateway (SEC-8).
- Authorisations (approvals, ticks, delegations, policies) are signed and verified in the cluster, so a compromised portal, Slack or Fleet can't forge them. Fleet can send only a short list of commands (SEC-9).
- The record is append-only from the agent's side and held by an independently protected audit service (FR-35, SEC-2).
- BMC credentials are never stored in agents. A separate hardware component holds credentials scoped to specific actions and machines (SEC-3).
- Log text, Kubernetes names, BMC strings, metrics and model output are all untrusted. An automatic repair needs more than one independent signal (SEC-1, addendum).

### Repairs
- Repairs come only from the signed repair catalogue, never from AI-written commands (FR-17). Each entry carries action, preconditions, risk, production impact, interruption, approval validity, verification and rollback.
- The FR-21 approval table is settled. Dangerous repairs are manual (FR-52). Alert-only executes nothing (Glossary).
- Before every run: re-check preconditions and authorisation. A failed check blocks; an inconclusive one blocks automatic repairs (FR-22).
- A coordinator per cluster prevents conflicting repairs. It also accounts for Kubernetes controllers, deployments and people (FR-29). Limits cover impact, not just counts (FR-30). Crash recovery reads the real state (FR-31).

### Privacy
- Raw data and secrets stay in the cluster they came from, even between one customer's clusters (PRIV-1).
- Rule-based allowlists per channel, placeholders and a mandatory outbound check on every channel. AI redaction is only an extra layer (PRIV-2 to PRIV-4).
- External AI (hosted or shared GPU) only with explicit consent, zero retention, nothing preselected (PRIV-8). Source code is a separate consent (FR-43).
- Channels: Fleet heartbeat (required), Fleet reports, notifications, portal, external AI. Every other flow is assigned to one of them (PRIV-9).

### Intelligence and cost
- Rules and statistics first. AI only to match evidence and write explanations. The core loop works with no AI at all, using templates (Section 7).
- Hosted model is the focus for version 1. In-cluster GPU is the default for code fixes. Shared GPU is an option.
- Two cost numbers per cluster per month (technical, total operating) at 100 and 10,000 clusters, per model option and without AI. Customer-paid and Orvex-paid costs are kept apart. Human approval time is probably the dominant cost (COST-1 to COST-6, addendum).

## 2. Tensions found (not conflicts with product decisions; to design)

- **Ordering vs forging (FR-22 vs SEC-9).** The server orders decisions, but a compromised portal can't forge them because the cluster verifies signatures. A compromised portal could still *suppress* a withdrawal or rejection. Withdrawals need the same signed path, and the cluster needs a rule for conflicting signed decisions. Round 2.
- **Admin actions with the portal off (PRIV-9 vs SEC-7).** Withdrawals, alert-only and settings changes stay possible on the in-cluster dashboard, by authenticated customer administrators. That needs an identity path that doesn't depend on the portal. Round 2 (O-7).
- **Heartbeat through the gateway (FR-6 vs NFR-4).** If the heartbeat passes the gateway and the gateway dies, Fleet sees silence. That is the right signal, but it isn't a diagnosis. Decide whether the heartbeat gets its own tiny fixed-schema path. Round 3.
- **Offline revocation (FR-22, D1).** A withdrawal takes effect only when the executor receives it. A partition delays it, capped only by the catalogue's approval validity. Round 6 picks the validity values.

## 3. Proposed decision order

| Round | Decisions | Open items closed |
|---|---|---|
| 1. Shape | Paradigm; what runs per node, per cluster, on the control cluster and in Fleet; where authoritative state lives | |
| 2. Authorisation and trust | Approval signing and keys; ordering and revocation delivery; audit service; executor and coordinator; identities and roles | O-3, O-5, O-6, O-8, O-9, O-10, part of O-7 |
| 3. Observe | Metrics, logs, hardware and events collectors; independent checker; heartbeat path; OMK vs EKS adapters | O-1 (threshold proposal) |
| 4. Intelligence and outbound | Rules vs LLM split; gateway and fact builder; hosted provider rules; local and shared inference; call budget | O-11 |
| 5. Fleet | Fleet services; signed release and catalogue distribution; correlation and consolidated alerts; waves and group approvals | O-2 (defaults), O-4 |
| 6. Offline and failure recovery | Disconnection, crash mid-repair, Nightshift's own failure, timing values, undo-reject window | O-7 (remainder), O-13 |
| 7. Failure catalogue | Top 20, ranked, each predict / fix / only report, per platform | |
| 8. Cost model | Monthly cost at 100 and 10,000 clusters: hosted, shared GPU, in-cluster GPU, no AI; main drivers. Prices verified against primary sources | |
| 9. Finalize | Spine, Orvex architecture document, reviewer gate | O-12 stays with Orvex (brand) |

The order follows dependencies. The shape and trust model constrain every tool choice. Tools come before intelligence, because the gateway's design depends on the collectors. The failure catalogue needs the observe stack. The cost model needs everything.
