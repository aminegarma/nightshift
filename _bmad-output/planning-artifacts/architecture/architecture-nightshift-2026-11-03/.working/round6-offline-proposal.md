# Round 6 Offline operation and failure recovery (proposal, 2026-11-05, not decided)

AI proposal for Amine. Nothing here is adopted until Amine decides. Builds on: FR-31 crash recovery (round 1), P4/P6 API outages (AP-5), receipts and validity tiers (AP-4), the outbox (5.3), the rollback guard (5.4), the checker and heartbeat (3.4), O-1 timings.

## D1 What keeps working when something is unreachable (both platforms)

| Unreachable | Keeps working | Stops or waits | The person sees | Recovery |
|---|---|---|---|---|
| **Fleet** | Monitoring, catalogue repairs already authorised (validity tiers, AP-4), local stops, audit, outbox fills | New approvals and withdrawals from the portal (relay), new releases, AI credentials (M2) after expiry | Orvex: "unreachable from Fleet" after 3 missed heartbeats. Customer (portal): "Sent — not yet effective" | Outbox drains by priority (stops first), stable IDs, receiver deduplication |
| **Portal only** (Fleet reachable) | Everything automatic; Fleet heartbeat and reports | Approvals | Notifications still say what's waiting; in-cluster dashboard for stops | Pending requests reappear; expired approvals are re-asked |
| **AI provider** | Rules and templates; the core loop | AI wording, unfamiliar-problem analysis, code fixes | Plain template text, "AI explanation unavailable" | None needed; no queueing of AI calls for later |
| **Notification channels (SMS)** | Everything else | Option B approvals (no fallback unless policy enables passkey-only, recorded as reduced assurance) | "Confirmation code could not be sent" | Retry; never a silent downgrade |
| **Kubernetes API** (AP-5) | Running pods, checker, heartbeat, audit, outbox where cached | Every automatic repair that needs the API | "Kubernetes API unreachable: repairs paused", escalated | Recheck real state before resuming (FR-31) |
| **Cloud or hardware API** (EKS AWS APIs; OMK BMC) | Kubernetes-level signals | Hardware and AWS-sourced signals | Panel marked out of date, never green (O-1) | Freshness from the last successful read |

## D2 When Nightshift itself fails

| Failure | Effect | Detected by | Recovery |
|---|---|---|---|
| Agent (reader) | No new diagnoses | Checker; heartbeat says degraded | Kubernetes restart; nothing to undo (read-only) |
| Executor mid-repair | Repair paused | Checker; RepairRun stuck | FR-31: intent written first, UID guards, real state checked, ambiguous → person |
| Gateway | No outbound reports, AI or relay fetches | Checker ("gateway health check failed") | Restart; outbox survives |
| Checker | No local liveness checks | Fleet: heartbeat missing | Kubernetes restart; Fleet sees silence (NFR-4) |
| Prometheus or VictoriaLogs | Stale signals | Checker (freshness) | Disruptive repairs blocked while checks are unavailable (coordinator point 8) |
| Outbox or audit storage full | Reports or audit can't be written | Checker; size metrics | **Audit full blocks repairs** (no repair without a record, FR-33). Outbox full drops ordinary reports oldest first, never stops, withdrawals or receipts, and records the gap |
| Clock unsynchronised | Validity checks unreliable | Checker (skew against the API server and Fleet) | Time-limited approvals refused (5.6 G-C) |
| Bad Nightshift release | Any of the above | Probation check | Rollback guard (5.4 R2) |

## D3 In-cluster dashboard (O-7 remainder)
- **Where:** a Service in the Nightshift namespace, never exposed outside the cluster by Nightshift. Reached by `kubectl port-forward` (the Kubernetes login is a first gate) or the customer's own ingress if they choose.
- **What:** read-only problems and history; open requests when the portal is off; **stop-type actions only** (withdraw, reject, untick, alert-only). No approvals and nothing that widens permissions (FR-15, PRIV-9).
- **Authentication problem (verified):** a passkey works only on its own domain or a subdomain of it (MDN, rpId). Two ways:
  - **a. Separate local passkeys,** enrolled in advance for the dashboard's own origin and listed in the signed roster as "local stop credentials". *(AI recommendation.)*
  - **b. Put the dashboard under the portal's domain** so portal passkeys work. Rejected by the AI: every cluster's dashboard would then be able to ask for assertions for portal passkeys, so one compromised cluster could misuse them against the portal.
- Every action is audited and gets a cluster receipt like any other decision.

## D4 Undo-reject window (O-13)
- **2 minutes** *(assumption to test)*, fixed, measured by the cluster from receiving the rejection.
- Undo only reopens the request (new request version); the other approvers are told when the window ends. An undo that arrives late is refused with a receipt.

## D5 Two approvals, one runs out (O-3, not yet decided in round 2)
- If the evidence hasn't materially changed: only the person whose approval ran out is re-asked, on the **same request version**, and told "Your approval ran out at 23:10; you were asked again".
- If the evidence changed: a **new request version**, and **both** approvals are needed again.

## D6 Timing values in one place (all assumptions to test)
- Heartbeat every 60 s; missing after 3 misses; data out of date about 2 minutes after the last successful observation (O-1, decided).
- Validity tiers (AP-4) need values: **fresh** up to 1 hour since the last relay status statement, **stale** up to 24 hours, then **expired** *(proposal)*.
- Approval validity 30 min / 2 h / group cap (5.6). Undo-reject 2 min (D4). AI credentials 15 min (M2).

---

## Decisions (Amine, 2026-11-05)

- **D1 accepted.** After reconnecting, the **executor receives and applies pending stops before resuming queued repairs**; draining the cluster's outbox first isn't enough. A Kubernetes API outage blocks Kubernetes changes and repairs needing unavailable checks; other observation and escalation continue where their dependencies still work.
- **D2 accepted.** Full audit storage blocks **new repairs and new repair steps**; space is **reserved** for recording ongoing work and recovery. Ordinary reports may be dropped with a recorded gap. Stops, withdrawals and receipts get **reserved, bounded capacity and a defined overflow response** (a finite outbox can't promise unlimited storage).
- **D3 option a, provisionally.** Local access stays independent of the portal. The stable address and authentication configuration must be defined (WebAuthn binds credentials to a relying-party ID checked against the origin). `kubectl port-forward` depends on the Kubernetes API, so it isn't access that survives an API outage.
- **D4 and D5 accepted** as proposed.

## Follow-up proposals (AI, not decided)

**D2 overflow response for the reserved capacity**
- Reserved space is sized for an assumed worst-case disconnection *(e.g. 7 days at the maximum decision rate; assumption to test)*.
- Receipts are compacted first: a later receipt for the same decision replaces earlier ones; nothing is lost that a later record still proves.
- If the reserved space still fills: the cluster switches to **alert-only** (no new automatic repairs, because it can no longer prove what it did), reports "degraded" in the heartbeat, and escalates. Stops already received are still applied, and the stop record is kept in the audit even when the outbox can't hold it.

**D3 stable address and authentication configuration**
- **Address:** one fixed HTTPS hostname per cluster, on the customer's internal DNS (for example `nightshift.<cluster>.<customer-internal-domain>`), chosen at installation and never changed. TLS from the customer's internal CA or cert-manager.
- **Relying-party ID = that hostname.** It is not under the portal's domain, so these credentials can't be used against the portal, and portal credentials can't be used here.
- **The signed roster lists, per person:** the local credential ID, its public key and its relying-party ID; the dashboard accepts only assertions whose origin and relying-party ID match exactly.
- **Enrolment** happens in advance while the portal and cluster are both reachable, and is confirmed by the existing roster process (two Orvex people for Orvex staff; the customer admin for customer staff).
- **Reachability by platform:**
  - **EKS:** an internal load balancer to the dashboard. *(Whether it keeps forwarding during a Kubernetes API outage is unverified.)*
  - **OMK:** the customer's existing ingress or load balancer *(unknown for OMK; to confirm with Orvex)*.
  - `kubectl port-forward` is a convenience path only, and not available during an API outage.
- **Honest limit:** if the API server is down and the ingress or load balancer also depends on it, local stops may be unreachable. Stops already delivered still apply, and approvals already given still expire on time.

## Final decisions on the follow-ups (Amine, 2026-11-05)

- **D2 overflow:** when protected storage fills, new repairs are suspended and shown as **"repairs suspended: storage full"**. The customer's chosen alert-only setting is not changed. **Only delivery receipts are compacted; the audit history is preserved.** Stops are still accepted while audit storage permits.
- **D3 (provisional):** a stable address, with a **controlled migration process** if it must change. DNS, certificates and routing are to be verified on each platform. Separate passkey domains help isolate local access, but correct origin and credential verification still matter.
- **D6:** values accepted as assumptions to test.
