# Consistency check of the 2026-11-15 amendments

Scope: decisions A1–A20 and E3/E6/E8/E9/E18/E21/E22/E23 as recorded at the end of `.memlog.md`, checked against `ARCHITECTURE-SPINE.md`, `architecture-orvex.md`, `failure-catalogue.md` and appendices A–C. Read-only; only critical/high issues and contradictions introduced by the fixes are reported.

## Lint

`lint_spine.py --workspace F`: ok, 0 findings.

## AP-1..AP-8

Still presented as pending everywhere (appendix B header, Orvex 13.5 "none is a PRD permission yet", spine open-items queue). No new issue.

## Issues (8, all high)

1. **A restore loses applied stops, so the stop guarantee is broken.** Locations: spine AD-24 (E18) and AD-50; Orvex 4.7 "State restore" and the 9.x "Protected storage full" row; AD-23 (relay keeps a decision only until its receipt); AD-2 (ledger holds switch-offs, used decision_ids, highest accepted versions). The problem: after an etcd or ledger restore, stops, revocations, switch-offs and version floors that were already receipted are gone from the ledger. The relay has already dropped them, and the recovery messages (status statements, key lists, stops) do not re-deliver them. Older but still-valid rosters or policies could then be accepted again. AD-50 and Orvex 9.x still say "a stop is never forgotten" / "repairs never silently resume". Why high: a revoked approver or an untick could come back to life, and the "never" overclaims what the design does. Fix: Fleet/relay keeps each cluster's current stop set, switch-offs and highest signed-object versions and re-sends them when a restore is detected; the cluster requires them before it reconciles. Change "never" to "not … unless state is restored or tampered with (AD-24, AD-72)".

2. **A11 contradicts E6.** Location: spine AD-50 and Orvex 9.x ("if even that space fills … running work follows its safe-stop or recovery procedure") vs AD-7 and Orvex 3.3 E6 ("if writing the intent to the audit service fails, the action does not run"). The problem: a safe-stop step is itself an action, so with audit space full it can't write its intent and therefore can't run. Why high: stop handling is undefined in exactly the failure it was written for. Fix: state that stop enforcement and pre-authorised safe-stop steps use the reserved stop audit space. If even that space fails, record the intent in the claims ledger and escalate, as an explicit exception to E6.

3. **The status-wording convention is out of date.** Location: spine conventions "Status wording" (line 653). The problem: it is missing the newly adopted states "sent", "received/applied by cluster", "expired" and "unreachable" (AD-18/A14), and "blocked", "exhausted" and "blocked: audit unavailable" (AD-7 E3/E6). The A14 "sent" also clashes with AP-3's "Sent — not yet effective in the cluster" (AD-23, Orvex 4.3 diagram, 4.6). Why high: these conventions bind every unit and the UX, so the two documents now give two different labels for the same state. Fix: map the A14 states onto the AP-3 wording, for example "Sent — not yet effective in the cluster" / "Applied in the cluster" / "Code expired" / "Cluster unreachable". Add all of them to line 653 and mark them under AP-2/AP-3 as pending UX.

4. **Orvex 3.3 still describes the old retry behaviour.** Location: Orvex 3.3, last sentence of the paragraph after the diagram. The problem: "If the retry is blocked (429) … there's no further retry" contradicts E3 (bounded backoff within validity and the attempt limit, recorded as "blocked"/"exhausted"). Why high: this is the old behaviour stated next to the new rule. Fix: replace it with "if refused (429), recorded as blocked; bounded retries per E3; when exhausted, a person takes over".

5. **Failure catalogue item 17 still relies on power-off alone.** Location: failure-catalogue.md item 17, "Possible later catalogue repair: the out-of-service taint, only with verified power-off and Orvex approval". The problem: AD-62/A20 say power-off is evidence only; stateful takeover also needs a verified fencing and storage-safety procedure and a re-checked BMC identity. Why high: a future catalogue entry could rely on power-off alone and run a stateful workload twice. Fix: "only under a verified fencing and storage-safety procedure (AD-62), BMC identity re-checked, and Orvex approval".

6. **Orvex 3.5 gives a different executor pause than A19.** Location: Orvex 3.5 "Not claimed" (repairs pause at least the default 5 minutes when the executor's node is lost) vs AD-7/A19 and Orvex 3.2 rule 5 (replacement delay shortened to 30–60 s, to test). Why high: the same document gives two different executor-recovery figures. Fix: "default 5 min; v1 shortens the executor's toleration to 30–60 s [To test]; total recovery time is not claimed".

7. **First install has no admin to approve it.** Location: spine AD-71 ("privileged installation … approved by an authorised customer admin") vs AD-19/A7 (no admin exists until enrolment, which happens after installation; bootstrap path before any admin exists). Why high: the first install depends on an approval that can't exist yet, so first install is not specified. Fix: in AD-71, first installation is approved by the independently verified contractual customer contact (A7); later upgrades are approved by a customer admin.

8. **The old first-admin wording sits next to the A7 split delivery.** Location: spine AD-19 first sentence and Orvex 4.5 "Rosters" bullet ("one-time out-of-band code to the contract contact"). The problem: this still describes the whole code going to the contract contact, which contradicts the A7 split delivery (half through protected local access, half through Fleet). Why high: it is a security-relevant enrolment step stated two ways in one AD. Fix: "with a split one-time code (A7, below)".
