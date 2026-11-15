# 5.6 Group approvals across waves (O-4) and approval validity (O-2): proposal, 2026-11-05, not decided

AI proposal for Amine. Nothing here is adopted until Amine decides. Already settled by the PRD (FR-32): one repair at one catalogue version; a frozen target set shown at approval; recorded per cluster; each cluster re-checked before it runs; runs in waves with stop conditions; each target needs a valid, unexpired approval; a later wave can't reuse an expired one; never for manual dangerous repairs; customer permission still needed where customer production is affected. 5.5 C4: newly affected clusters don't inherit it.

## G-A What the approver signs
- One decision statement D for the group: repair, catalogue version, the **frozen target set**, validity, the wave plan, and the stop conditions, confirmed once with option B (passkey + SMS + fresh passkey over D).
- **Isolation problem:** listing every cluster ID in D would show each customer's cluster the other customers' cluster IDs. Proposal: D holds a **commitment to the target list** (a Merkle root); each cluster receives D plus a short proof that it is in the list. The approver still sees the full list in the console.
- The relay delivers D and the proof to each target. Each executor checks: signature, its own membership, validity, catalogue version, and its own preconditions and current evidence. Customer approvals stay per cluster where required.

## G-B Validity across waves
- The console shows, before approving: "Approval valid until 04:10. Planned waves end 05:30. Targets in waves after 04:10 will need a new approval." The approver can approve for the targets that fit, or accept a re-ask later.
- A later wave can't reuse an expired approval (FR-32). The re-ask covers **only the remaining targets**, with fresh evidence.
- **A stop voids the rest.** If a stop condition fires, the remaining targets don't run, and resuming needs a **new approval** with the new evidence. Not a "resume" of the old one.

## G-C Default validity (O-2), a field on each catalogue entry
- Validity starts when the approval is given. The executor must **start** before it expires; it checks preconditions again at the start. A repair already running isn't interrupted by expiry, but no new step starts that needs a fresh check (as in FR-31 recovery).
- **Validity is a limit, not a promise:** a material change in the evidence the cluster sees voids the approval earlier, whatever the clock says.
- **Starting defaults (assumptions for Orvex to set per entry):**

| Repair | Default validity |
|---|---|
| Risky, or affects customer production | 30 minutes |
| Other approved repairs | 2 hours |
| Group approval | the entry's own validity, never longer than a policy cap (e.g. 4 hours) |

- **Clocks:** the cluster judges expiry with its own clock, allowing a small, fixed skew *(value to set)*; a cluster whose clock is unsynchronised refuses time-limited approvals and reports it.
- Unanswered requests don't expire (UX O-2); only given approvals do.
