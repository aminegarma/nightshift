# Re-review: ARCHITECTURE-SPINE.md after the round 9 fixes (D1-D15)

Reviewed 2026-11-11. Read-only. Inputs: the revised spine; the four review-*.md reports and reconcile-prd.md; `.memlog.md` from "Round 9 reconcile" to the end; `.working/round9-outbound-flows.md`.

**Verdict:** Most gate findings are fixed and the D1-D15 wording is reflected faithfully. However, three new contradictions came in with the fixes (AD-64 vs AD-69, AD-17 vs AD-51/AD-48, AD-68 vs the install path). AD-15 and the option B diagram were not updated. Fix these before the spine is called final.

**Lint:** `lint_spine.py --workspace F` reported `ok: true`, 0 findings.

**AD ids:** AD-1 to AD-71 are all defined, and every reference points to an existing AD.

## 1. Earlier critical and high findings

**Counts (58 total):** 40 resolved · 1 deferred · 17 still open or partly open.

| Report | Id | Status | Where / what remains |
| --- | --- | --- | --- |
| rubric | C1 | resolved | AD-48 and the Group decision convention. AD-17 still has no group branch (see N2) |
| rubric | H1 | **open (partial)** | AD-2 now names the state homes. AD-15 has no rows for the executor-owned Secrets, customer settings or policies, and does not list the gateway as a reader (see N5) |
| rubric | H2 | **open (partial)** | Encoding (JCS) and the route of D are now in Conventions. The option B sequence diagram still never sends D to the portal |
| rubric | H3 | resolved | Inbox is pull (AD-23); management agent (AD-66); checkpoints (AD-16). The AD-4 edge label still says "transport not decided" |
| rubric | H4 | **open (partial)** | AD-68 covers Nightshift releases. AD-53 still says the executor checks platform updates "before applying", but it does not apply them |
| rubric | H5 | resolved | AD-70 plus the draft table. The Deferred row "Outbound flow-to-channel table" is stale |
| rubric | H6 | resolved | AD-15 appenders updated. The AD-4 diagram lacks GW→AU, RG→AU and CHK→AU |
| rubric | H7 | resolved | AD-40 adds the root and key list; map, switch-off and weights are covered. The signer of Orvex's advance last-resort permission (AD-55) is still unnamed |
| rubric | H8 | resolved | AD-71 plus Deferred (Fleet monitoring, recovery targets) |
| rubric | H9 | resolved | AD-71 |
| reality | H1 | resolved | AD-35 uses the runtime endpoint and the per-Region account mode. The Deferred row still says "ZDR eligibility (allowed_modes includes none)", which is not checkable on that path |
| reality | H2 | resolved | AD-35 (permitted Regions or route, "none" in every Region) |
| reality | H3 | **open (partial)** | AD-68 defines the update path. AD-43 still claims "a cluster refuses to start without it" |
| adversarial | C-1 | resolved | AD-23 receipt key pinned at install |
| adversarial | C-2 | resolved | AD-68 |
| adversarial | C-3 | **open (partial)** | Conventions fixed. The sequence diagram still has no D return step (same as rubric H2) |
| adversarial | H-1 | resolved | AD-23 durable inbox; relay keeps decisions until receipt |
| adversarial | H-2 | **open (partial)** | Enums are closed. Missing: required role and scope per decision kind; the nonce and request_version rule for tick, settings, delegation, revocation and halt-clear; claim release |
| adversarial | H-3 | **open** | AD-17 accepts local origin for stops only, but AD-51/D15 allows settings changes there. No per-credential allowed kinds |
| adversarial | H-4 | resolved | AD-48. Merkle hash rules (leaf/node separation, ordering) are not specified |
| adversarial | H-5 | resolved | AD-17 occurrence rule. evidence_digest is still undefined |
| adversarial | H-6 | **open (partial)** | Monotonic versions adopted. Consent and channel withdrawal are not stop-class, and the gateway has no anti-rollback for the consent it reads |
| adversarial | H-7 | resolved | AD-15 |
| adversarial | H-8 | resolved | AD-2 |
| adversarial | H-9 | resolved | AD-2 |
| adversarial | H-10 | **open** | Heartbeat status is still untyped (no release or probation fields); "agent ID" vs cluster_id is unmapped |
| adversarial | H-11 | **open (pending)** | Policy key signs the map (D10), but its two-reviewer gate is only "proposed" in AD-56 |
| adversarial | H-12 | resolved | AD-65 (D6) |
| adversarial | H-13 | resolved | AD-62 |
| adversarial | H-14 | **open (partial)** | The pin is registered with Fleet, which is still Orvex-rewritable. No second-contact notice |
| security | C-1 | resolved | AD-67 (AP-8 PRD change deferred) |
| security | H-1 | resolved | AD-65 |
| security | H-2 | resolved | AD-69. AD-59 still says "RBAC is bounded to the catalogue's verbs" |
| security | H-3 | **open (partial)** | Two reviewers (AD-40) and the release reference (AD-68) are in. Image admission still accepts any signed image, including old vulnerable ones |
| security | H-4 | resolved | Signed-object versions convention |
| security | H-5 | resolved | AD-40. Protection of in-cluster keys is unstated |
| security | H-6 | resolved | AD-34 (D8) |
| security | H-7 | resolved | AD-18 (D9), residual recorded |
| security | H-8 | **open** | BMC network pivot: no node-route or read-only-account rule, and no Deferred row |
| security | H-9 | **open (partial)** | Identity binding is in AD-47. No per-customer cap, so one tenant can still stall a fleet rollout |
| security | H-10 | **open (partial)** | AD-3 states the node-compromise limit. No mitigation (capabilities, dedicated nodes) and no Deferred row |
| reconcile-prd | C-1 | resolved | AD-67; AP-8 in Deferred |
| reconcile-prd | C-2 | **open (partial)** | Same as rubric H4. AD-15 still lists "policies" as written by Fleet pipelines |
| reconcile-prd | H-1 | resolved | AD-70 (draft); flow 14 still open |
| reconcile-prd | H-2 | **open (partial)** | AD-54 is fine, but AD-15 has no customer-settings row and the gateway is not a reader |
| reconcile-prd | H-3 | resolved | AD-55 |
| reconcile-prd | H-4 | resolved | AD-56 (gate proposed) |
| reconcile-prd | H-5 | resolved | AD-57 |
| reconcile-prd | H-6 | resolved | AD-58 |
| reconcile-prd | H-7 | resolved | AD-59. The diagnostic scope "deferred" is missing from the Deferred table |
| reconcile-prd | H-8 | resolved | AD-60. D has no start-window or recovery-plan field |
| reconcile-prd | H-9 | deferred | Deferred row "Code-fix path detail" |
| reconcile-prd | H-10 | resolved | AD-61 |
| reconcile-prd | H-11 | resolved | AD-62 (D14) |
| reconcile-prd | H-12 | resolved | AD-66 |
| reconcile-prd | H-13 | resolved | AD-62 |
| reconcile-prd | H-14 | resolved | AD-63 |
| reconcile-prd | H-15 | resolved | AD-64 (but see N1) |

## 2. New problems introduced by the fixes

| # | Sev | Problem | Suggested fix |
| --- | --- | --- | --- |
| N1 | high | AD-64 says Nightshift admission checks "match Nightshift namespaces only and never customer namespaces". AD-69 needs admission rules on the executor's changes to customer workloads. A team that follows one AD breaks the other | Reword AD-64: match only requests made by Nightshift identities, or objects in Nightshift namespaces; never fail closed on customer requests |
| N2 | high | AD-17 accepts the local-dashboard origin for stop decisions only, so D15/AD-51 local settings changes fail verification. AD-17 also has no group branch: it requires the decision-v1 tag over the cluster's own D, while AD-48 signs G under group-decision-v1 | Add to AD-17 "or settings changes from the local dashboard (AD-51)" and "group decisions are verified per AD-48 instead of the D rebuild" |
| N3 | high | AD-68 limits the release reference, Flux verification settings and trust keys to two writers (executor, guard), with admission rules rejecting others. AD-43 and AD-71 have the install path update Flux and pin keys, and AD-40 rotates trust keys through a signed key list | Name the install-path identity as the third writer (AD-69 style), and state who writes rotated key lists |
| N4 | high | AD-15 says "policies" are written by Fleet pipelines and signed with the policy key. AD-53/AD-54 say they are customer-signed. There is no row for customer settings or policies, the executor-owned Secrets, or the gateway reading consent | Add AD-15 rows: customer settings/policies (customer admins, admin passkeys, readers executor and gateway, stored in executor Secrets); Orvex policy separate |
| N5 | high (possible) | AD-24: after outbound-policy expiry "only the heartbeat and a fixed data-free attention notice leave". That blocks the relay status and key-list fetches (flow 6) a cluster needs to recover, which is a possible deadlock | Exempt the flow-6 required service traffic in AD-24 (ties to AP-8) |
| N6 | medium | AD-67 says "only three outbound paths bypass the gateway". Flow 18 (installer → Fleet registrations) is a fourth | List it in AD-67 and AP-8, or route it through the gateway |
| N7 | medium | AD-2 forbids private persistent stores for repair state. AD-23 adds a gateway durable inbox of decisions | Name the outbox and inbox as allowed transport stores in AD-2 |
| N8 | medium | D requires request_id, request_version and nonce, but tick, settings, delegation, revocation and halt-clear have no request version. AD-60's recovery plan is not in D | Per-kind field and nonce rules in Conventions |
| N9 | medium | After a guard rollback, nothing stops the executor re-advancing to the broken (newer, policy-allowed) release (AD-46/AD-68) | Mark a rolled-back release ineligible until a newer release or person clears it |
| N10 | low | AD-40 gives two different key lists. The group-confirmation key has no named requester and is missing from the AD-41 diagram (which also lacks the root). "Signs it with its cluster key" (Route of D) names a key not in AD-40 | Align the lists; name the key |
| N11 | low | Stale or overclaiming text: the AD-4 diagram ("transport not decided", missing audit edges); the Deferred flow-table row; the Deferred row "allowed_modes includes none"; AD-43 "refuses to start"; AD-53 "platform update"; AD-59 RBAC wording | Update the text |

All D1-D15 wording matches the spine. The one exception is D15, which the spine reflects only in AD-51; AD-17 contradicts it (N2).
