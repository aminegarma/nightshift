# Adversarial lens: architecture-orvex.md (2026-11-15)

20 findings. Each gives the location, the problem, the suggested fix and the consequence if it ships as-is.

1. **4.12, 4.1: cluster-admin and node root are missing from the compromise table.**
   - **Problem:** whoever holds cluster-admin (Orvex on OMK; the account operator on EKS) can rewrite the ledger and pins, replace the executor, read the receipt and audit keys, and remove admission rules.
   - **Fix:** add a row saying what these holders can and can't do, and who holds cluster-admin on each platform. Decide whether cluster keys need a KMS, an HSM or sealed storage.
   - **If not fixed:** "authority only from signatures" reads as covering insiders, but one OMK operator can forge receipts.
2. **4.5, 4.9, 4.12: receipt detection relies on the portal it is meant to check.**
   - **Problem:** the portal shows the receipt that proves a stop arrived, but the portal is the very component that could be compromised.
   - **Fix:** verify the receipt in the browser against the pinned key, or confirm it on the local dashboard. Document the limit.
   - **If not fixed:** a compromised portal and relay can hide a stop and also show a fake "effective" status.
3. **3.2, 3.3: non-delete actions have no fence against a stale executor.**
   - **Problem:** only deletes and evictions carry UID and resourceVersion preconditions.
   - **Fix:** every action declares its fence (a resourceVersion precondition, or an epoch annotation checked by an admission rule). An action without a fence can't be automatic.
   - **If not fixed:** two executors both run a non-delete action, for example two rollbacks or two irreversible volume expansions.
4. **3.3: the recovery branch retries without revalidating.**
   - **Problem:** after a crash, the executor retries without re-checking approval validity, stops and evidence.
   - **Fix:** revalidate first, and say whether a crash counts as "started".
   - **If not fixed:** a retry runs on an approval that has expired or is out of date.
5. **4.6, 8.2: the cluster clock can be rolled back.**
   - **Problem:** status-statement age is judged by the cluster's own clock, which can be rolled back.
   - **Fix:** use a monotonic clock since receipt, an authenticated time source, and an alarm on backward jumps.
   - **If not fixed:** a cluster stays in the "fresh" tier indefinitely.
6. **4.3: the gateway knows the SMS code.**
   - **Problem:** the gateway sees the code and holds the SMS credentials, so it can phish roster phones or run up SMS charges.
   - **Fix:** state that the SMS gives no proof of possession against a compromised gateway. Add provider-side rate and spend limits and a template the provider enforces.
   - **If not fixed:** reviewers overestimate option B.
7. **4.4: who issues the first-admin code is unclear.**
   - **Problem:** the document doesn't say who generates and delivers the first-admin enrolment code. If install tooling generates it, the installer can enrol itself.
   - **Fix:** the cluster generates the code and shows it only on a channel the customer controls, with an audit record and a notice to the customer.
   - **If not fixed:** the root of the customer roster is captured at installation.
8. **7.3, 7.4: a release can break its own rollback trigger.**
   - **Problem:** a bad release that breaks the checker or the guard prevents its own rollback.
   - **Fix:** make probation a dead-man's switch, and keep the guard and checker outside the release being probed.
   - **If not fixed:** recovery is manual only.
9. **3.5, 7.3, 9: the admission webhook failure policy isn't specified.**
   - **Problem:** with "Ignore", a webhook outage removes the limits. With "Fail", it blocks recovery.
   - **Fix:** prefer ValidatingAdmissionPolicy; scope any webhook to Nightshift identities, exempt the guard's recovery write, and test an outage.
   - **If not fixed:** either the safety envelope disappears or recovery is impossible.
10. **4.6, 3.1: requests that never expire can exhaust the run quota.**
    - **Problem:** unanswered requests stay open forever, while open runs are capped.
    - **Fix:** keep pending approvals out of the run quota, deduplicate them, close stale ones as "obsolete", and reserve quota for safe repairs.
    - **If not fixed:** urgent repairs are refused.
11. **8.2: a full audit volume can refuse stops.**
    - **Fix:** reserve space for stops and halts only. If even that is exhausted, set alert-only rather than refuse a stop.
    - **If not fixed:** a withdrawal fails while work continues.
12. **4.10 against 2.2, 1 and 4.11: inconsistent gateway exception.**
    - **Problem:** 4.10 names only the heartbeat as a gateway exception, while AD-67 names three. Several flows also have no named path: the attention notice, recovery fetches and checkpoints.
    - **Fix:** reword 4.10 and give each flow a path and a row in the flow table.
    - **If not fixed:** the document contradicts itself in a privacy review.
13. **2.2 against 8.3: the dashboard contradicts the no-inbound rule.**
    - **Problem:** "nothing connects into a workload cluster" contradicts the dashboard's inbound endpoint.
    - **Fix:** qualify the rule and add the endpoint to the security boundaries.
    - **If not fixed:** the endpoint is never hardened.
14. **4.3, 7.2: no approval latency budget.**
    - **Fix:** set a budget from click to SMS, and derive the poll interval and the SMS expiry from it.
    - **If not fixed:** approvers get codes that have already expired.
15. **7.6, 4.12: group assurance can be overstated.**
    - **Problem:** clusters record "passkey + Fleet SMS (group)" even if the SMS was skipped.
    - **Fix:** record "SMS attested by Fleet (not verified by the cluster)", or have the assertion cover a hash of the SMS session.
    - **If not fixed:** audit records overstate assurance.
16. **11.1, 11.4: the cost summary frames only Orvex's saving.**
    - **Problem:** it doesn't say that the customer footprint exceeds Orvex's saving. The 100-cluster "without" line also equals the "with" line, which is unexplained.
    - **Fix:** add a total-system row (Orvex plus customer) and explain the 100-cluster figure.
    - **If not fixed:** cost shifts to customers unnoticed, or the model loses credibility.
17. **Header against 4.7: the date doesn't match.** The header says 2026-11-11, but the document cites a decision from 2026-11-15.
    - **Fix:** update the date and record the spine revision it was synced against.
18. **Header, 4.11: rules rest on draft working files.** Normative rules depend on files in `.working/`.
    - **Fix:** promote the flow table and the PRD change queue to versioned hand-in files, or inline them.
19. **3.5, 3.2: the executor's node loss pauses all repairs.**
    - **Problem:** losing the executor's node pauses repairs for at least 5 minutes, and how a new epoch is acquired isn't specified.
    - **Fix:** specify a Lease plus a guarded ledger write; a shorter toleration and anti-affinity, or a fenced warm standby.
    - **If not fixed:** Nightshift can't act during node loss, which is common on bare metal.
20. **2.3: the BMC-to-node binding is verified only at install.**
    - **Problem:** hardware swaps or BMC IP reuse can later bind a node to the wrong BMC.
    - **Fix:** re-verify on every use (BMC system UUID against the node's DMI UUID), and send any mismatch to a person.
    - **If not fixed:** two writers on the same data, and data corruption.
