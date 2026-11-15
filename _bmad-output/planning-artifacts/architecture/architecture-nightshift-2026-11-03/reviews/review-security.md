# Security and privacy review: Nightshift architecture spine

- **Reviewed:** `ARCHITECTURE-SPINE.md` (updated 2026-11-11), against PRD section 6 (PRIV-1..PRIV-9, SEC-1..SEC-9) and `.working/prd-change-queue.md` (AP-1..AP-8).
- **Reviewer stance:** independent, read-only. This review checks the design only, because nothing has been built.
- **Date:** 2026-11-11

## Verdict

The authorisation core is strong. It has person-signed decisions verified in the cluster, nonce and decision_id replay protection, stop-beats-go, a relay and registry with no authority, and separate signing keys. The containment and privacy promises that sit around that core are weaker. "Raw logs never leave", "a compromised agent is contained", "independent evidence", "executor RBAC is bounded" and "the executor checks releases against the customer's policy" each depend on controls that are deferred, unspecified or placed at the wrong component. Several rules therefore document a property rather than enforce it.

| Severity | Count |
| --- | --- |
| Critical | 1 |
| High | 9 |
| Medium | 13 |
| Low | 5 |

How to read the "Judgement" column: **Prevents** means the rule as written blocks the attack. **Detects** means it makes the attack visible after the fact. **Documents** means it states the property but nothing in the spine enforces it.

## Threat coverage summary

| Threat | Spine rules | Judgement |
| --- | --- | --- |
| Prompt injection via logs reaching repair choice or execution | AD-8, AD-12, AD-34, AD-65 | **Prevents** for execution: rules only, signed catalogue, executor-side checks |
| Prompt injection reaching approvers (AI wording, names) | AD-34, conventions O-6 | **Documents**. Neutralisation is deferred, and local-model text may reach the portal (H-6, M-7) |
| Forged approvals (compromised portal, relay or Fleet) | AD-17, AD-22, AD-41 | **Prevents**. The residual "approve a different pending request" risk is honestly **detected** (AD-18) |
| Compromised agent: acting | AD-5, AD-17, AD-55 | **Prevents** unauthorised acts. A nuisance repair storm remains possible (L-3) |
| Compromised agent: exfiltration | AD-26 | **Documents** only. No egress enforcement (C-1), and typed fields leave a covert channel (M-5) |
| Compromised executor | AD-5, AD-59 | **Overclaims**. Catalogue verbs include code-execution-equivalent patches (H-2) |
| Compromised gateway | AD-26, AD-18 | Partial. It can rewrite the SMS and the notice (H-7). Its read scope is not limited (M-5) |
| Compromised checker or rollback guard | AD-33, AD-45 | Mostly bounded. Forced rollback and a Flux freeze remain possible (L-4) |
| Compromised audit service | AD-16 | **Documents**. The checkpoint channel is undecided (M-1) |
| Compromised Fleet service, relay or registry | AD-39, AD-41, AD-24 | Approvals: **prevents**. Withheld revocations and replayed rosters: not prevented (H-4, M-4) |
| Compromised signing pipeline or keys | AD-40 | **Documents**. There is no root of trust, rotation, revocation or threshold signing for releases (H-3, H-5) |
| One customer cluster compromised, affecting others | AD-36, AD-39, AD-47 | Gaps in SMS credential sharing (H-7), Fleet identity binding and report poisoning (H-9), and shared AI quota (M-3) |
| Cross-customer leakage | AD-39, AD-47, AD-48 | Mostly prevented. The risks are reversible fingerprints (M-6) and shared SMS and AI accounts (H-7, M-3) |
| Supply chain (images, models, catalogue) | AD-37, AD-40, AD-43, AD-46 | Good for Nightshift packages. Gaps in third-party image provenance and in image-level downgrade (H-3, M-10) |
| Covert channels (heartbeat, receipts, SMS, typed facts) | AD-27, AD-26 | Heartbeat: bounded until AP-1 adds 32 opaque bytes. Typed facts: unbounded (M-5) |
| Approval phishing | AD-18, O-6 | Partially **detected**. The SMS integrity and names gaps remain (H-7, M-7) |
| Offline and replay | AD-22, AD-24, AD-25 | Good for decisions. Gaps for signed metadata rollback (H-4) and for clock or etcd-restore rollback (M-8) |
| Denial of service on Fleet and AI quotas | AD-27, AD-36 | **Documents**. No intake rate limit or reconnect discipline (M-11), and no local AI budget (M-3) |
| Privileged collectors and node compromise | AD-3 | **Overclaims** the egress limits (H-10) |
| BMC network pivot | AD-31 | **Documents**. The pod-level rule does not stop node-level reachability (H-8) |

## Findings

### Critical

#### C-1: Network containment is not part of the spine, so SEC-2, SEC-8 and PRIV-1 rest on a deferred item

- **Threat:** The agent parses untrusted log text and runs the in-cluster model, so it is the component most likely to be compromised. Once compromised, it reads VictoriaLogs and Prometheus and sends raw logs straight to the internet, bypassing the gateway.
  - The same applies to any customer pod, which can call the gateway's "typed facts for outbound" API, the audit append API, the llama.cpp endpoint or the Prometheus and VictoriaLogs write endpoints (H-1).
  - On EC2-backed EKS, any Nightshift pod can reach IMDS and obtain node-role AWS credentials unless IMDS is restricted. AD-32 makes that restriction a precondition only for the AWS poller, not a baseline.
- **Location:**
  - AD-3, AD-4, AD-26 ("The log store has no outbound path"), AD-27 and AD-37 ("reachable only from the agent").
  - Deferred: "Default-deny egress per Nightshift pod … to confirm with Amine" and AP-8. The OMK CNI is unknown, so NetworkPolicy enforcement itself is unconfirmed.
  - EKS: VPC CNI network policy must be explicitly enabled, and Fargate pods do not get it.
- **Gap:** No rule requires default-deny ingress and egress, per-destination egress allowlists, or authentication of in-cluster callers (projected ServiceAccount tokens with an audience, or mTLS). "Raw logs never leave" is therefore a property of well-behaved code, not of the deployment. AD-26 and AD-37 overclaim.
- **Fix:** Promote this to an ADOPTED invariant now, not with AP-8.
  - (a) Default-deny ingress and egress NetworkPolicy for every Nightshift namespace. Per-pod egress allowlists: agent to Prometheus, VictoriaLogs, audit, gateway, llama.cpp and the Kubernetes API only, with no internet. Only the gateway, checker, Flux and the AWS poller get external egress, each to fixed FQDNs or CIDRs through an egress proxy or FQDN policy.
  - (b) Every in-cluster API (gateway intake, audit append, executor dashboard endpoint, llama.cpp) authenticates the caller's ServiceAccount identity, using TokenReview with an audience or mTLS, and authorises per caller.
  - (c) On EKS, an IMDSv2 hop limit of 1 or blocking 169.254.169.254 for all Nightshift pods is a baseline. EKS Pod Identity or IRSA is used for every AWS credential.
  - (d) Make "a CNI that enforces NetworkPolicy (including egress)" an installation precondition on OMK. Name Fargate's lack of NetworkPolicy as reduced containment, or forbid scheduling sensitive Nightshift pods on Fargate.
  - (e) The checker probes that egress denial actually holds, and reports when it does not.

### High

#### H-1: Evidence stores are writable by untrusted parties, so "two independent signals" can be forged by one actor

- **Threat:** A compromised agent, a customer pod or a compromised app forges the evidence that triggers ticked automatic repairs, for example a node drain or pod deletion.
  - AD-15 lists metrics as written by "collectors, adapters write in", which implies a Prometheus remote-write receiver or a push path.
  - VictoriaLogs receives logs from Fluent Bit over its HTTP insert endpoint, which is unauthenticated by default and accepts arbitrary stream fields such as namespace, node or "kernel".
  - The executor's independent check (AD-12, AD-31: "re-run entry queries at source") queries the same Prometheus the agent can reach.
  - With app read scope (AD-61), customer pods are scraped. Without strict relabelling they can emit infrastructure metric names and labels.
- **Location:** AD-15 (sole-writer table), AD-29, AD-30, AD-31, AD-65.
- **Gap:** "Sole writer" is stated but not enforced. AD-65 defines independence as "different source or vantage point", but two sources fed by the same untrusted writer or the same store are not independent.
- **Fix:**
  - Disable the Prometheus admin API and the remote-write receiver. Adapters expose scrape endpoints instead of pushing.
  - Restrict VictoriaLogs insert to the Fluent Bit identity using NetworkPolicy plus an auth token, and put agent reads behind a read-only query path.
  - Set `honor_labels: false` and use a separate job or tenant for app-scope metrics. Add a rule that app-scope metrics and app logs never count as evidence for infrastructure entries.
  - Redefine "independent" as different trust domains: at least one signal must come from a source the target workload cannot write, such as the kubelet or API server state, which the executor reads itself.
  - Where possible, the executor reads one signal directly from the Kubernetes API rather than from Prometheus.

#### H-2: Executor RBAC "bounded to the catalogue's verbs and resources" is not a meaningful bound

- **Threat:** A compromised executor, or a bug driven by a crafted RepairRun, turns repair verbs into arbitrary code execution.
  - Catalogue actions such as rollout restart need `patch deployments`, which lets the holder rewrite the pod template: any image, any ServiceAccount, mounted Secrets, hostPath.
  - Cordon needs `patch nodes`, which also allows changing labels and taints, so the holder can steer workloads.
  - The result is effectively cluster-admin over customer namespaces, and it also breaks AD-59 ("never modifies … Secrets"), because a patched pod can read and use them.
- **Location:** AD-5, AD-8, AD-59.
- **Gap:** RBAC is verb and resource granular, not field granular. The spine claims a containment that RBAC alone cannot provide.
- **Fix:** Add a rule that every executor mutation is also constrained by a ValidatingAdmissionPolicy keyed to the executor's ServiceAccount. Examples:
  - Deployment patches may change only `spec.template.metadata.annotations["kubectl.kubernetes.io/restartedAt"]`.
  - Node patches may change only `spec.unschedulable` and Nightshift-owned taints.
  - Deletes and evictions are allowed only with the AD-6 preconditions.
  - The executor has no get, list or watch on Secrets.

  Ship these admission policies through the separately authorised install path (AD-43). Note this policy matches the executor's identity, not customer namespaces, so it does not conflict with AD-64. State in AD-59 that the admission policy, not RBAC, is the enforcement.

#### H-3: The release path makes the Fleet rollout controller the de facto authority, and the release key is the crown jewel without a two-person rule

- **Threat:**
  - **Compromised rollout controller:** it pushes a signed release outside the customer's policy.
  - **Compromised release pipeline or key:** it signs a malicious executor that runs in up to 10,000 clusters.
  - **Downgrade through images:** a signed older vulnerable image is reintroduced.
- **Location:** AD-43, AD-44, AD-45, AD-46, AD-53; Deferred: "Whether release signing also needs two reviewers".
- **Gap:**
  - AD-53 says the executor checks every release against the customer-signed maintenance policy before applying it. But Flux pulls and applies releases (AD-43), and the executor is not in Flux's path.
  - A new release replaces the executor itself, so the policy check is either done by the code being installed or not done at all.
  - Who sets the digest Flux pulls is unstated.
  - AD-46's downgrade protection covers release metadata, but admission-time image verification (AD-43) accepts any validly signed image, including old vulnerable ones. The rollback guard can also edit workloads in the Nightshift namespace.
  - The release key is the only key whose compromise defeats every in-cluster check, yet its signing gate is one pipeline "after testing".
- **Fix:**
  - (a) The running, already-trusted executor (or a small dedicated release gate) writes the Flux OCIRepository digest after verifying release metadata against the customer policy, version monotonicity and the window. Flux's source object is writable only by that gate.
  - (b) The image admission policy admits only digests listed in the currently accepted signed release manifest, not "any Orvex-signed image".
  - (c) Release signing uses a threshold of two people plus the pipeline. Releases that change the executor, gateway, audit or admission policies get extra review, which is already in Deferred and should be promoted.
  - (d) State that compromise of the release key equals compromise of every cluster's Nightshift rights. That makes the H-2 field-level bounds the last line of defence.

#### H-4: No anti-rollback for signed rosters, policies, catalogue, platform map and settings

- **Threat:** Whoever controls the delivery path (Fleet, relay, registry, or a compromised gateway) replays an older but still validly signed object. Examples:
  - A customer roster that still lists a removed admin or approver, re-enabling that person's passkey.
  - An older management policy, an older delegation, an older consent or channel-permission object that widens outbound flows, or an older platform map that labels a component platform-only.
- **Location:** AD-15, AD-19, AD-24, AD-54, AD-56; "delivery path for policies and the Orvex roster" is deferred.
- **Gap:** Every object carries valid_until, but nothing requires a monotonic version or a hash chain. Revocation is defined as a stop decision on "unused decisions under it" (AD-22), not as a permanent roster state. Relay freshness statements (AD-24) do not say which version is current. AD-46 covers releases only.
- **Fix:** Every signed authorisation object carries `object_type, scope (customer_id, cluster_id), version (monotonic), prev_digest`.
  - The cluster durably stores the highest accepted version per object and rejects lower or equal versions, and forks.
  - Roster changes form a hash chain anchored at the pinned first-admin credential.
  - Relay status statements carry the current version vector (roster, policy, delegations, settings, catalogue switch-offs), so a cluster can detect withheld newer objects.
  - Revocation removes the credential from the roster, and that removal is irreversible except by a new enrolment.

#### H-5: No root of trust, key rotation or key-compromise recovery, and the platform-map signer is unspecified

- **Threat:**
  - Compromise of the catalogue, policy, people-list, relay or release key, with no defined way for 10,000 clusters to stop trusting it.
  - The platform-only map decides whether customer approval is needed (AD-12), yet "Orvex-signed (key not specified)". Whoever can sign it can relabel customer production as platform-only and skip customer approval.
  - The audit and receipt keys live in the cluster, readable by anyone with node root or Secret read.
- **Location:** AD-12, AD-15 (map row), AD-40; Deferred: "Key custody for roster, relay, audit-service and receipt keys; which key signs the platform-only map".
- **Gap:** The spine separates keys well but defines no trust anchor, rotation cadence, revocation list or threshold, nor how a cluster learns a new public key. Key custody is deferred for keys the authorisation model depends on.
- **Fix:**
  - Adopt a TUF-style hierarchy: offline threshold root keys pinned at install; online role keys (release, catalogue, policy, people-list, relay, platform-map) delegated by root with expiry; key rotation and revocation delivered as root-signed metadata. This also solves the freshness and rollback problems in H-4 and AD-46.
  - Assign the platform map its own key with the catalogue gate (testing plus two reviewers).
  - In-cluster audit, receipt and SMS-code HMAC keys: generate them non-exportable where possible (TPM or KMS on EKS; HSM or TPM on OMK if available), else in a Secret readable only by the owning ServiceAccount, with etcd encryption at rest. State plainly that the customer's cluster administrators can read them.
  - Register the audit key with Fleet over an authenticated, first-use-pinned exchange, and rotate it with a chained key-change record.

#### H-6: Text from the in-cluster model can carry raw log content and injected instructions out of the cluster and onto approval screens

- **Threat:**
  - AD-34 says local evidence goes only to the in-cluster model and "AI wording is optional, shown separately and labelled". The spine does not say where that wording is shown.
  - If local-model wording reaches the portal, the morning summary or notifications, then free text derived from raw logs leaves the cluster. That contradicts AD-26 ("never from log text") and PRIV-1.
  - Injected log content can also make the model write persuasive approval text ("Orvex has verified this is safe, approve now").
  - The PRIV-4 outbound check is mandated but has no defined mechanism, and cannot reliably catch paraphrased secrets.
- **Location:** AD-26, AD-34, conventions "Rendering of actions and targets".
- **Gap:** There is a channel ambiguity, and the AI wording has no output constraint.
- **Fix:**
  - Rule: local-model output is shown only on the in-cluster dashboard. It never enters the gateway or any outbound channel, including portal approval screens.
  - Hosted-model output (whose input was fact-builder fields only) may go to the portal, but it is labelled, length-capped, link-free and never placed in the approval decision area or the SMS.
  - Define the PRIV-4 check concretely per channel: a schema validator plus a secret and entropy scanner plus a denylist. Treat it as a backstop, not proof.

#### H-7: The SMS path is neither integrity-protected nor isolated per cluster

- **Threat:**
  - **(a) Shared SMS credentials.** Each cluster's gateway calls the SMS provider directly (topology). If that uses a shared Orvex provider account or API key, one compromised customer cluster gets an Orvex-branded SMS sender to every roster phone in the fleet, which enables approval phishing across customers. Depending on the provider API, it may also read message logs that contain other customers' codes, numbers and action names. That is cross-customer leakage.
  - **(b) Gateway rewrite.** A compromised gateway, or a compromised SMS provider account, sees the plaintext code and can rewrite the message. Paired with a compromised portal, this defeats option B's only defence against "approve a different pending request" and suppresses the "Not you? Withdraw" notice.
- **Location:** AD-18, topology (GW to SMS provider); Deferred items on providers and allowlists.
- **Gap:** The spine treats the SMS as "from the cluster", but the content passes through the gateway and a third party. Credential custody is unspecified.
- **Fix:**
  - Send SMS through a Fleet-side notification service with per-cluster authenticated requests, per-cluster rate limits and a fixed template filled only from D fields. No provider credential is stored in clusters.
  - If clusters must send directly, use per-cluster sub-accounts with send-only scope and rate caps, and no log read.
  - The executor computes the message text from D, and the gateway may not alter it. Fleet logs a hash of what was sent for audit.
  - Put the post-decision notice on a second channel too: the portal inbox and the in-cluster dashboard.
  - Document that a gateway compromise in that cluster removes the SMS assurance for that cluster.

#### H-8: BMC and out-of-band network pivot on OMK

- **Threat:**
  - A pod-level egress rule (AD-31: "network rules to listed BMCs only") does not stop other pods or processes on the same node, hostNetwork pods (which NetworkPolicy does not cover) or a compromised node from reaching the BMC network, if nodes have a route to it.
  - BMCs are high-value: power control, virtual media, console. A compromised BMC is also an untrusted input source to the BMC reader, which parses Redfish or IPMI responses.
  - IPMI-over-LAN RAKP leaks password hashes to anyone who can reach the BMC.
  - "Just-in-time credentials" has no defined issuer, scope or storage.
- **Location:** AD-31, AD-62, SEC-3; topology "OBM to BMCs on out-of-band network"; Deferred "Hardware-action component".
- **Gap:** Containment is described at the pod level only. There is no rule that BMC accounts are read-only, and no rule on where the credential broker lives.
- **Fix:**
  - The BMC reader reaches BMCs only through a read-only Redfish proxy placed on the out-of-band side, or runs on a dedicated tainted node that is the only node with a route to the BMC network. No workload node gets a route to the out-of-band network.
  - BMC accounts use the Redfish ReadOnly role. IPMI-over-LAN stays disabled or out of scope.
  - Credentials are issued per read by a broker outside the cluster, or a customer vault, scoped to listed BMCs with a short time-to-live.
  - BMC responses are size-limited and parsed as untrusted input.
  - Record the customer's out-of-band network design as an install precondition, or treat it as reduced coverage.

#### H-9: Fleet does not bind report content to the sending cluster's identity, so one cluster can poison correlation and stall fleet-wide rollouts

- **Threat:**
  - A compromised cluster, or a malicious customer, sends reports or heartbeats claiming other clusters' IDs. It could hide another cluster's outage or frame it.
  - It could also flood reports correlated with a newly updated release. AD-44 and AD-47 stop the rollout on "concentration on newly updated clusters", so a single tenant could block security updates for every customer.
  - It could also feed the learning pipeline (FR-37..40) with crafted fingerprints.
- **Location:** AD-27, AD-39, AD-44, AD-47.
- **Gap:** No rule says Fleet derives cluster_id and customer_id from the authenticated client identity. Cluster identity bootstrap and per-cluster credentials are unspecified. Correlation has no per-cluster or per-customer weight caps.
- **Fix:**
  - Per-cluster workload identity is issued at install, with a key that is non-exportable where possible. Fleet services take cluster_id and customer_id only from the authenticated identity and reject mismatched payload fields.
  - Apply per-cluster rate limits at intake.
  - Correlation counts distinct clusters and distinct customers, caps each customer's contribution, and requires more than one customer, or Orvex wave-0 clusters, before an automatic fleet-wide rollout stop. A single-customer signal stops only that customer's rollout and alerts Orvex.
  - The learning pipeline treats reports as untrusted.

#### H-10: Privileged collectors are an easy node escape, and nothing keeps sensitive pods off the nodes they run on

- **Threat:**
  - Fluent Bit parses attacker-controlled log lines with hostPath access, and has had memory-corruption CVEs.
  - smartctl_exporter runs privileged. node-problem-detector and the node monitoring agent run with host access.
  - Compromising any of them gives node root on every node, and with it the ServiceAccount tokens, mounted keys and volumes of any co-located executor, gateway, audit service (audit key and chain) or rollback guard.
  - AD-3's "egress only to the local metrics store" cannot hold for a privileged or hostNetwork container, which can rewrite the host firewall and is not subject to NetworkPolicy.
- **Location:** AD-3, Structural Seed ("smartctl_exporter, privileged").
- **Gap:** The containment overclaims for privileged pods, and nothing separates node placement.
- **Fix:**
  - Replace "privileged" with the minimum capabilities and devices: for example `CAP_SYS_RAWIO` plus the specific block devices for smartctl, and Fluent Bit unprivileged with read-only hostPath to log directories.
  - Pin and patch collector images on an SLA.
  - Run the executor, gateway, audit service and rollback guard on a small set of dedicated, tainted system nodes where the cluster allows it, and state the residual risk where it does not: node root equals the rights of every Nightshift pod on that node.
  - Reword AD-3 so the egress limit applies to non-host-network pods. Host-level egress is the node firewall's job.

### Medium

#### M-1: Audit tamper detection has no channel yet

- **Location:** AD-16, Deferred "Transport for audit checkpoints before AP-1".
- **Gap:** SEC-2 requires that missing or interrupted reporting is detectable. Until a checkpoint transport is chosen, an attacker with audit-volume access rewrites history undetectably. AD-16 merely documents this.
- **Fix:** Before build, pick an interim channel: a signed checkpoint as a typed Fleet report, plus a local customer-visible copy. Fleet alerts on sequence gaps, regressions and forks.

#### M-2: Audit append is open to flooding and to false attribution

- **Location:** AD-16, AD-50.
- **Threat:** A compromised agent, a log storm that drives agent appends, or a dashboard client floods the audit append API. "Full protected storage" suspends all new repairs (AD-50), so this is a cheap denial of service. Records may also be attributed to the wrong writer.
- **Fix:**
  - Set a per-writer quota and rate limit. The agent's share must never consume the space reserved for executor records, stops and receipts.
  - The audit service stamps the authenticated caller identity on every record and does not trust a writer field in the payload.

#### M-3: AI quota and cost abuse, and credential-vending misdirection

- **Location:** AD-35, AD-36.
- **Threat:**
  - A compromised gateway, or a flood of "unfamiliar problems" from crafted logs, burns Bedrock tokens. With account quotas shared per cell, one cluster can starve every customer in that cell.
  - A compromised credential-vending service returns credentials for an attacker-owned AWS account or profile, and consented prompts go there.
  - Application inference profiles that wrap cross-Region system profiles send prompts outside the customer's Region. That breaks the sovereign-Region promise.
- **Fix:**
  - Add a local token and request budget per cluster in the gateway (signed policy), plus per-cluster profile-level throttling.
  - The gateway pins account ID, Region and inference-profile ARN from signed configuration and verifies the vended identity (for example with GetCallerIdentity) before sending.
  - Rule: application profiles are built from single-Region foundation-model ARNs only. Cross-Region inference is never used.
  - Size cells so one cluster cannot exhaust a cell's quota.

#### M-4: Relay status statements prove liveness, not completeness

- **Location:** AD-24, AD-41.
- **Threat:** One relay key, fleet-wide, signs freshness for every cluster. A compromised relay keeps a cluster in the "fresh" tier while withholding revocations, stops and newer rosters. A statement for cluster A may be replayable to cluster B.
- **Fix:** Bind each statement to cluster_id, a cluster-issued nonce or monotonic counter, and the version vector from H-4. Fleet keeps an independent signed transparency log of issued stops and revocations, and the cluster's receipts are compared against it, so a withheld stop is detected without the relay's help.

#### M-5: Covert channels through typed fields, the heartbeat and receipts

- **Location:** AD-26, AD-27, AP-1, conventions.
- **Threat:**
  - "Typed, allowlisted fields" still include numbers, durations and IDs that a compromised agent fills. Millisecond durations and arbitrary integers carry kilobytes per message to Fleet and Bedrock, past the PRIV-4 check.
  - AP-1 adds `chain_head` (32 opaque bytes) to every heartbeat, about 46 KB a day per cluster, which a compromised audit service or checker controls.
- **Gap:** The gateway trusts the agent's values. The spine does not state what the gateway can read.
- **Fix:**
  - The gateway quantises numeric fields: buckets, coarse durations, enums from the catalogue.
  - It caps message rate and size per channel.
  - The gateway, not the agent, resolves catalogue IDs and codes against the signed catalogue.
  - State that the gateway has no read access to VictoriaLogs, Prometheus or Secrets.
  - Fleet verifies that `checkpoint_sig` matches the registered audit key, and alerts on unexpected heartbeat cadence.
  - Document a residual covert-channel bandwidth figure instead of claiming none.

#### M-6: "Allowed-field fingerprint" may be reversible

- **Location:** AD-47, conventions (correlation key).
- **Threat:** A fingerprint is a hash of private or low-entropy content, such as an error message, path or name. Dictionary attacks at Fleet, or by another customer through shared incident views, reverse it.
- **Fix:** Build fingerprints only from catalogue failure codes and allowlisted enums, never from hashed free text. Customers see only aggregated incident labels.

#### M-7: Untrusted names in SMS and portal, and names as private data

- **Location:** conventions O-6 (deferred), AD-18, AD-26.
- **Threat:** Pod and namespace names created by any lower-privileged user in the customer's cluster appear in the SMS and on the portal. They can carry phishing text or misleading look-alikes, and they are customer data leaving the cluster, which PRIV-1 and PRIV-3 cover.
- **Fix:** Before build, define strict rendering: length cap, a restricted character set, visible escaping, and UID plus kind shown alongside. Decide explicitly, in the PRIV-3 allowlist, whether names may leave at all, or are replaced by placeholders outside the in-cluster dashboard.

#### M-8: Clock and state rollback

- **Location:** AD-22, AD-25.
- **Threat:**
  - NTP spoofing on the cluster's time source extends every valid_until. "Unsynchronised" detection does not catch a confidently wrong clock.
  - An etcd or backup restore rolls back the used decision_ids, nonces, epochs and highest seen versions, which re-enables replay within validity.
- **Fix:**
  - Use authenticated time (NTS) or a cross-check against relay statement time and Fleet time.
  - Keep replay and rollback state in the audit chain, or in a store outside etcd backups. After a detected restore (epoch or audit sequence regression), invalidate all pending nonces and refuse outstanding decisions.

#### M-9: In-cluster dashboard read access is unspecified

- **Location:** AD-51.
- **Threat:** The dashboard reads the audit chain and evidence, which may include private data, on the customer's internal network. Authentication is specified only for stops and settings. CSRF and session handling are unaddressed.
- **Fix:**
  - All dashboard access needs a local passkey session with roles.
  - Use origin-checked, CSRF-protected state changes in which every stop or setting is a fresh WebAuthn assertion verified by the executor.
  - Allowlist dashboard ingress by network.

#### M-10: Third-party image and model supply chain

- **Location:** AD-37, AD-43, Stack.
- **Threat:** Upstream images (Prometheus, Fluent Bit, VictoriaLogs, exporters, llama.cpp, Flux itself) are pulled by tag or from public registries. GGUF parsing in llama.cpp has had memory-safety CVEs.
- **Fix:**
  - Mirror every third-party image into the Fleet registry, scan it, generate an SBOM, re-sign it with the release key and pin it by digest in the release manifest.
  - The admission policy admits only manifest digests (H-3).
  - Model weights are verified before load, and llama.cpp runs with no network egress and no ServiceAccount token.

#### M-11: Denial of service on Fleet at 10,000 clusters

- **Location:** AD-27, AD-28, AD-49.
- **Threat:** After a Fleet or network outage, 10,000 outboxes and relay fetchers reconnect at once. A single cluster floods intake. Heartbeat rate limits exist, but intake, relay and vending limits do not.
- **Fix:**
  - Clusters use jittered exponential backoff on reconnect.
  - Fleet applies per-cluster admission limits, with stops and receipts in a separate priority lane.
  - The heartbeat watchdog runs on separate capacity so a report flood cannot turn into false "unreachable from Fleet" alarms.

#### M-12: The code-fix path imports AI-written code

- **Location:** AD-8 ("never from AI-written commands"), AD-38; Deferred code-fix design.
- **Threat:** Source code and context sent to the model contain injection (for example in comments or logs). The returned patch is AI-written code that may be deployed.
- **Fix:**
  - Constrain the deferred design now: patches are untrusted proposals, never applied by the executor, and need named human review, testing in an isolated environment and the customer's normal deploy pipeline.
  - Secret scanning runs on both the outbound code and the returned patch.

#### M-13: Management agent trust direction

- **Location:** AD-66; Deferred transport.
- **Threat:** The management agent aggregates sanitised data from many clusters. Anything it sends to workload clusters (coordination for multi-cluster repairs) is cross-cluster input into the executor's decisions, and it has no defined transport.
- **Fix:**
  - State that management-agent messages are untrusted coordination hints, never evidence, authority or decisions.
  - Workload clusters pull them, consistent with AD-4. Each message is size- and schema-limited.
  - Treat the management agent's compromise as at most a delay of multi-cluster repairs.

### Low

- **L-1: Merkle proofs reveal target-set size.**
  - Location: AD-48.
  - Detail: A cluster learns the group size from proof depth. This is acceptable, but should be documented. Pad to a fixed depth if group sizes are sensitive.
- **L-2: The post-decision notice and SMS invite sender spoofing.**
  - Location: AD-18.
  - Detail: Alphanumeric sender IDs are spoofable in many countries.
  - Fix: SMS messages never contain links. "Withdraw" is done only in the portal or on the dashboard. Say so in the notice.
- **L-3: A compromised agent can trigger ticked safe repairs repeatedly, across many targets.**
  - Location: AD-65.
  - Detail: Repeat caps apply per entry and target.
  - Fix: Add a per-cluster cap on automatic repairs per time window that halts and calls a person, as in AD-58.
- **L-4: A compromised checker or rollback guard can force probation rollbacks or keep the Nightshift Flux object suspended.**
  - Location: AD-45.
  - Detail: These are bounded by "named previous signed release, probation window only". AD-46 detects a held-back cluster only through expired metadata.
  - Fix: The guard's suspension expires automatically, and every suspension is reported to Fleet.
- **L-5: Receipts prove only possession of an in-cluster key.**
  - Location: AD-23.
  - Detail: Customer cluster admins and node root can sign receipts.
  - Fix: Document that receipts are evidence of cluster state as reported by the cluster, not proof against the customer's own administrators.

## Overclaims to reword

| Rule | Current wording | Suggested |
| --- | --- | --- |
| AD-3 | "egress only to the local metrics store" for privileged exporters | "For non-host-network pods, egress is limited by NetworkPolicy. Privileged or host-network pods are limited by the node firewall, and their compromise equals node compromise." |
| AD-26 | "Raw logs never leave … The log store has no outbound path" | "…enforced by default-deny egress (C-1). Text from the local model never enters outbound channels." |
| AD-37 | "reachable only from the agent" | This holds only once C-1's NetworkPolicy and caller authentication exist. |
| AD-59 | "executor RBAC is bounded to the catalogue's verbs and resources" | Bounded by RBAC plus field-level admission policy (H-2). |
| AD-53 | "the executor checks it against that policy itself" | The executor does not see Flux applies. Either move the gate (H-3) or reword. |
| AD-65 | "two independent signals (different source or vantage point)" | "Different trust domains, at least one not writable by the target workload or the agent" (H-1). |
| AD-16 | "Periodic authenticated checkpoints are stored independently outside the cluster" | This is true only once a channel exists (M-1). |
| AD-24 | A fresh status statement implies current authority | A status statement shows that the relay is reachable, not that no revocation was withheld (M-4). |

## What is already strong (keep)

- **AD-17:** challenge binding over a cluster-built D with a cluster nonce, user verification, origin and RP ID checks, and distinct-person counting.
- **AD-22:** stop beats go, regardless of order. Replay is blocked by durably stored decision_ids.
- **AD-41:** the registry and relay are explicitly authority-free.
- **AD-40:** keys separated by artefact, and receipts signed by the cluster rather than Fleet.
- **AD-34 and AD-8:** AI is kept entirely off the authorisation and execution path. Repairs come only from the signed catalogue.
- **AD-18:** the honest statement of its limits, including that the passkey signs a fingerprint and that the portal-substitution attack is only detected.
- **AD-42 and AD-4:** clusters only connect out, and no central component holds cluster credentials.
- **AD-32:** the AWS poller is gated on verified credential isolation. Extend the same IMDS baseline to every pod (C-1).
