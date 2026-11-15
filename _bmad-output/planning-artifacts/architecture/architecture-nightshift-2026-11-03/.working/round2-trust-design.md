# Round 2: trust and authorisation (working design, 2026-11-03)

Working architecture choices made by Amine on 2026-11-03. **Design only: none of this is implemented or tested.** Values marked [to set] are proposals for testing. Every limitation listed here is part of the decision.

## 2.1 Person-bound approval with a passkey

### What gets signed

For every decision, the portal builds a **decision statement** in a canonical encoding (the encoding is chosen with the stack). It contains:

| Field | Meaning |
|---|---|
| `customer_id`, `cluster_id` | Whose cluster |
| `request_id`, `request_version` | The exact request. A material change creates a new version (FR-22) |
| `catalogue_entry_id`, `entry_version`, `entry_digest` | The exact tested repair |
| `target` | Kind and unique ID (for example pod UID, node ID) |
| `evidence_digest` | Fingerprint of the evidence shown |
| `decision` | approve / reject / withdraw / undo-reject |
| `role` | The role the person acts in: customer approver, delegated Orvex support, Orvex technical approver, manual-repair performer |
| `valid_from`, `valid_until` | Validity, capped by the catalogue entry (FR-22) |
| `cluster_nonce` | A one-time value the cluster issued for this request version |
| `decision_id` | Unique ID, used against replay |

The WebAuthn **challenge** is the SHA-256 fingerprint of that statement. The person's passkey signs over the authenticator data plus a hash of the client data, which contains the challenge ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAssertionResponse/signature)). User verification (PIN or biometric) is required, so each decision is also its own step-up authentication (O-5).

### What the executor checks before it counts a decision

1. The signature is valid for a credential in the **current signed roster** (see below), and the credential is active.
2. The challenge equals the fingerprint of the statement, the client data type is an assertion, the origin and relying-party ID are the portal's, and the user-verified flag is set.
3. The executor **rebuilds the expected statement from its own `RepairRun`** and compares it field by field: customer, cluster, request version, entry version and digest, target, evidence. A statement for anything Nightshift didn't propose is refused.
4. The `cluster_nonce` is one this cluster issued for this request version. The `decision_id` hasn't been used before. The time is within validity.
5. The signer currently holds the role for this customer, and any delegation is in scope and not revoked.
6. All required approvals for the FR-21 row are present, and they come from different people where both are required.
7. No stop decision covers this request version (2.2), and the mode allows the repair. Then the preconditions are re-checked as always (FR-22).

**The portal can't grant authority by signing on someone's behalf.** It holds no key the executor accepts as a person.

### Remaining risk: the passkey doesn't show what it signs

The passkey prompt shows the site and the account, not the repair. WebAuthn Level 3 defines no transaction-display extension: the defined client extensions are appid, appidExclude, credProps, prf and largeBlob ([W3C](https://www.w3.org/TR/webauthn-3/)). So a **compromised portal could show one repair and ask the person to sign another**.

**Limits on the damage:** check 3 means the attacker can only get approval for a repair that Nightshift itself proposed for that cluster, from the catalogue, that is still open, and that still passes every check. It can't invent an action or a target.

**Proposed mitigation (practical, two parts):**
- **A request code from the cluster.** The cluster derives a short code from the statement's fingerprint, for example two words and two digits. It sends that code through the notifications channel, which the gateway sends, not the portal. The portal shows the code on the confirmation sheet. If the codes differ, the person stops. This ties in with the UX's deferred finding "a request code against phishing". *Limit:* people may not compare the codes. A customer with notifications off gets no independent code.
- **A confirmation from the cluster after every decision.** "You approved [repair] on [cluster] at 02:14. Not you? Withdraw." It goes through notifications. *Limit:* this detects misuse, it doesn't prevent it. A repair that starts at once may already have run.

### Enrolment, recovery and revocation (the portal is only a transport)

The cluster holds two **signed rosters** (lists of people, roles and passkey public keys). Each roster has a version and a validity.

- **Customer roster.** Every change is signed by the passkey of an existing customer admin. The portal can carry a change but can't sign one.
  - **First admin:** a one-time enrolment code goes to the customer's named contract contact, out of band. The first admin uses it to enrol their passkey, and the cluster pins that credential. The installer never enrols it (consistent with PRIV-9's "never the installer").
  - **Every roster change** (new person, new passkey, role change) triggers a cluster-originated notice to every customer admin.
  - Each person should register **two passkeys** (a phone and a laptop, or a synced passkey).
- **Recovery** (a person loses all their passkeys):
  - another customer admin re-enrols them;
  - if the *only* admin is locked out: the out-of-band procedure again, with a waiting period [to set, for example 48 hours]. The waiting period is announced to every customer channel and recorded. During it, any existing customer credential can cancel the recovery.
  - Orvex can help but can't silently add or restore a customer approver: Orvex-assisted recovery is always delayed, visible and recorded.
- **Revocation.** The person themselves or any customer admin can sign a revocation of a passkey or a person. It is a **stop decision** (2.2): it takes effect when received, and decisions signed by that credential that haven't been used yet stop counting.
- **Orvex roster.** Orvex engineers and support staff are signed by an **Orvex roster key**, kept apart from the release, Fleet and policy keys (addendum). Proposal: changes need two Orvex people.
  - The Orvex roster can't grant customer roles, and the customer roster can't grant Orvex roles.
  - Delegation to Orvex support is a customer-admin-signed object with its scope.

## 2.2 Stop beats go, scoped to the affected action

### Scope of each stop decision

| Stop decision | What it stops |
|---|---|
| Withdrawal | That person's approval on that request version. The request version closes |
| Rejection | That request version, for this occurrence of the problem (FR-50) |
| Untick | That customer's tick of that catalogue entry |
| Switch to alert-only | Every execution for that customer's cluster (FR-21) |
| Revoking a delegation | Unused approvals given under that delegation |
| Revoking a passkey or person | Unused decisions signed by that credential |

### Ordering and replay

- **The rule:** on a given request version, **any valid stop beats any approval, whatever the order in which they were signed or received.** An older approval can never override a newer stop. A stop closes that request version for good.
- **Renewal:** a deliberately renewed approval is possible only through the agreed request flow. The cluster issues a **new request version with a new nonce** (FR-50: one new request when the problem becomes critical or materially changes; undoing a rejection reopens the request). Every required approval is then given again on the new version. *Cost:* the other approver is asked again, as in O-3.
- **Server sequence:** the server still gives each decision a sequence number (FR-22: the server orders decisions). That sequence is used for display and history, and for the undo-rejection window. Safety doesn't depend on it.
- **Replay:** every decision carries the cluster's nonce for that request version and a unique `decision_id`. The executor keeps the used IDs durably and refuses a decision for an old version. Validity times bound the rest.
- **Stop decisions are verified locally,** like approvals: signature, roster, role and scope. An unverifiable stop is recorded and shown to Orvex and the customer, but not applied. Otherwise anyone could stop repairs by forging one.
- **After a restart or an outage,** stops are processed first, then authorisation, evidence and action state are revalidated (P5).

### Receipts

When the executor has *applied* a decision, the cluster signs a **receipt**: decision ID, request version, the time applied, the effect (applied / refused as invalid / arrived too late) and the executor epoch. The receipt goes back through the portal channel, or appears on the in-cluster dashboard when the portal is off. Until a receipt arrives, the person sees **"Sent — not yet effective in the cluster"** (FR-22).

### Bounded offline validity

Every signed authorisation object carries a `valid_until`. That covers ticks, the management policy, maintenance and rollback policies, last-resort permissions, delegations, rosters, approvals, channel permissions and allowlists.

- **Approvals:** the catalogue entry caps their validity (FR-22).
- **Long-lived objects** (ticks, policies, rosters, delegations, channel permissions): the content stays as the customer or Orvex signed it. The cluster also needs a fresh **status statement**, signed by the decision relay's key and pulled when connected. It says, in effect: "the latest decision sequence for this customer is N; nothing newer is pending". It is like a freshness stamp.
- **Tiers when the status statement can't be refreshed:**
  - **fresh** (age ≤ X): everything authorised may run;
  - **stale** (X < age ≤ Y): only safe ticked repairs and safe policy repairs continue (NFR-5 local autonomy). Last-resort repairs and anything else stop, and the record says why;
  - **expired** (age > Y): no automatic repairs at all. The cluster observes, reports and records, like alert-only, until a fresh status arrives.
  - X and Y are [to set and test], possibly per catalogue entry.
- **Local stops still work** during a cut, through the in-cluster dashboard (PRIV-9), with customer passkeys verified against the cached roster.
- **Cached outbound policies** (allowlists, channel permissions) are used until their `valid_until`. They are **never widened** when a refresh fails. After expiry, only the required heartbeat and a fixed, data-free "this cluster needs attention" notice may leave. The exact values are for round 4 and round 6.
- **Limit:** a compromised relay or Fleet could keep issuing fresh status statements while hiding a stop. Offline validity bounds how long a cut-off cluster acts on old permissions. It doesn't protect against a lying relay. The person's missing receipt is the visible sign.

## 2.3 Audit records stay in the originating cluster

### Local record

- An **audit service** in its own security boundary, with its own identity and its own volume. The agent and executor can only append. Nothing can update or delete through its API.
- Every record carries the fingerprint of the previous one (a **hash chain**), plus a sequence number.
- Raw records never leave the cluster (PRIV-1). The customer can read them, and export them to storage they control (to define).
- **Limit:** durable local storage doesn't by itself guarantee availability or safe recovery. A failed disk, or someone with full control of the cluster, can destroy the records. The checkpoints make that **detectable, not recoverable**. Backup to customer-controlled storage is deferred.

### Audit checkpoints (proposed PRD change, not an existing permission)

**Proposal:** add a minimal audit checkpoint to the required Fleet heartbeat (FR-6). Today FR-6 allows only agent ID, timestamp and status. This needs a `bmad-prd` Update (FR-6, PRIV-9, onboarding explanation) and a UX update (the onboarding field list). It is recorded in `prd-change-queue.md`.

| Field | Format | Meaning |
|---|---|---|
| `audit_seq` | unsigned 64-bit integer | Number of the last record in the chain |
| `chain_head` | exactly 32 bytes | SHA-256 fingerprint of that record (including the previous fingerprint) |
| `checkpoint_time` | timestamp | When the audit service signed the checkpoint |
| `audit_key_id` | fixed-length ID | Which audit-service key signed |
| `checkpoint_sig` | fixed-length signature | Signature by the audit service's key, so the agent and gateway can't forge it |

- **Sequence:** `audit_seq` only increases. Fleet stores each checkpoint per cluster. It flags a decrease, a different `chain_head` for an already-seen `audit_seq`, a bad signature, or missing checkpoints.
- **Authentication:** the heartbeat itself is authenticated with the heartbeat identity (mutual TLS). The checkpoint carries its own signature from the audit service's key, generated in the cluster at installation and registered with Fleet.
- **Outbound validation:** fixed schema, exact lengths and integer ranges, no text fields. Anything else is dropped and recorded (PRIV-3, PRIV-4).
- **Limit, a covert channel:** a 32-byte hash value can't be told apart from random data, so a compromised audit service could hide about 32 bytes per heartbeat in it. Checking the local chain against Fleet's stored checkpoints would later expose such fake heads, but only after the fact. This is recorded for the security review.
- **What a checkpoint can prove:**
  - that the history *before* a checkpoint hasn't been rewritten or cut short without detection, once the local chain is checked against Fleet's stored checkpoints;
  - that the record count kept growing;
  - that the audit service was alive and signing.
- **What it can't prove:**
  - that every event was recorded (a component that never logs leaves no gap). The SM-4 cross-check against Kubernetes audit logs covers part of this;
  - that the recorded content is true;
  - anything after the last checkpoint;
  - anything going forward, if the audit service's key is stolen (the past stays protected by the stored checkpoints).
- **Raw audit records stay local.**

## Carried forward

- Epoch checks reduce takeover races but don't eliminate them. Action-level duplicate protection stays (P2, P3).
- Cached permissions and outbound policies have a defined validity and conservative behaviour when they can't be refreshed (above). Values are for rounds 4 and 6.
- Local durable records don't automatically guarantee availability or safe recovery (above).

## Assumptions and open points

- People will compare request codes (weak, untested). Customers with notifications off get no independent code.
- Customers will register two passkeys, or use synced passkeys.
- The portal origin and relying-party ID are stable and owned by Orvex.
- Fleet stores checkpoints durably and separately from the clusters.
- Key custody (Orvex roster key, relay key, audit-service keys) is designed in the security review.
- Values to set: the recovery waiting period; offline tiers X and Y; checkpoint frequency (every heartbeat proposed); the request-code format.
- Re-asking every approver when a version changes may add human time (a cost-model input).

## 2.1 revised (Amine, 2026-11-04): passkey and SMS confirmation (option B)

Working proposal, **pending feasibility and usability testing**. It replaces the "compare the request code" mitigation above. Not implemented or tested.

### What a passkey actually signs

A passkey never signs readable text, and it doesn't display anything. The authenticator signs **its own authenticator data plus the SHA-256 of the browser's client data**. The client data includes the challenge bytes the relying party chose, the origin and the type ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/AuthenticatorAssertionResponse/signature)). We choose the challenge to be a fingerprint of the decision statement D. So the signature commits to D only indirectly, through that fingerprint.

### Protocol

1. **Sign-in:** the person signs in to the portal with a passkey. That session is verified by the portal only. The cluster doesn't rely on it.
2. **Approve clicked:** the portal asks the cluster, through the relay, to start a confirmation. It sends the request, version, decision, person and role.
3. **The cluster builds D** (the round 2.1 fields, including a fresh `cluster_nonce` and a `decision_id`). It also:
   - generates a random one-time code;
   - stores D and a keyed hash of the code, with an expiry [to set] and an attempt limit;
   - sends the SMS **through the gateway** to the phone number in the **signed roster**, for example "Approve: Restart one replica of checkout · cluster X · code 123456 · expires 02:24";
   - returns D to the portal. D isn't secret.
4. **The person checks the task in the SMS** and types, pastes or auto-fills the code.
5. **Face ID:** the portal asks the passkey for a fresh assertion with `challenge = SHA-256("nightshift-decision-v1" ‖ canonical(D))`, user verification required, and only the person's registered credentials allowed. The person confirms with Face ID or a PIN.
6. **Forwarding:** the portal sends {decision_id, code, assertion} through the relay. The cluster fetches it.
7. **The cluster verifies, in order:**
   1. the decision_id is pending, not expired, and has attempts left;
   2. the code matches the stored keyed hash for **that decision_id**;
   3. the challenge in the client data equals the fingerprint of the **stored D for that same decision_id**, the type is `webauthn.get`, and the origin is the portal's;
   4. the relying-party hash and the user-verified flag are correct;
   5. the signature is valid over the authenticator data plus the hash of the client data;
   6. the credential belongs to the person in the signed roster, and the SMS went to that person's roster number;
   7. the role, delegation and distinct-people rules hold, and the required approvals are complete (round 2.1);
   8. no stop decision applies, and the mode allows the repair (2.2).
   - Then it marks the code and the decision_id as used, records the assurance level **"passkey + SMS"**, and sends a signed receipt.

**What binds the two:** the code and the assertion must both resolve to **the same decision_id**, and D (built and stored by the cluster) contains the request version, target and evidence. Either factor alone isn't accepted.

### What each part proves, and what it doesn't

- **The assertion** proves that the holder of the registered passkey, after user verification, produced a signature over a fingerprint of D, for the portal's origin.
- **The code** proves that someone with the SMS sent to the registered number entered it in this flow, before it expired. SMS is a restricted authenticator: SIM swaps, number porting and interception are possible ([NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html), sec. 3.1.3.3).
- **Typing the code doesn't prove the person read the task.** Paste and auto-fill can fill it without the message being read. The SMS gives the person an independent view of the action. It doesn't guarantee they looked.

### Accessibility

Paste and auto-fill stay allowed, for people who struggle to retype a code. This accepts that some people won't read the SMS. Format to check in the UX update: the action comes first in the text, and possibly an origin-bound code line so auto-fill offers the code only on the real portal [to check].

### Remaining misleading-portal risk

A compromised portal can still show a false description on screen. If the person doesn't read the SMS, they could approve a different repair that is **genuinely pending**. The cluster's checks limit this to repairs Nightshift itself proposed, from the catalogue, still open and still passing every check. The cluster's post-decision notice ("You approved… Not you? Withdraw") helps detect it, but doesn't prevent it.

### Passkey-only fallback

- Allowed **only where the applicable policy explicitly enables it**:
  - for customer approvals, a setting signed by a customer admin;
  - for Orvex approvals, an Orvex-signed policy.
  - Policy may limit fallback by risk level [to decide].
- **When it's used:**
  - the person sees "SMS confirmation unavailable: approving with passkey only (reduced assurance)";
  - the decision, the receipt and the history record the assurance level "passkey only".
- **SMS failure never silently downgrades the approval requirements.** That covers delivery failure, a provider outage and notifications being off. Without an enabled fallback, the approval can't be given. The request stays open (FR-22) and escalation continues. Who must approve never changes.
