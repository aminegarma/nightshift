# Finalisation check: PRD Update 2026-11-15

Scope: the memlog entries from "PRD Update started (Amine, 2026-11-15)" to the end (conflict decisions 1-7, AP-9 to AP-20, remaining points 1-8) and `update-notes-2026-11-15.md`. Read-only check of prd.md, addendum.md, EXPERIENCE.md, ARCHITECTURE-SPINE.md, architecture-orvex.md and appendices A and B.

## Verdict

**Ready to finalise.** Critical: 0. High: 0. Medium: 5.

## Checks

1. **Memlog audit:** every decision is in prd.md with its qualifications and stated limits. That covers conflicts 1-7, AP-9 to AP-20 and remaining points 1-8. Nothing is missing or weakened.
   - Mechanism depth is in addendum.md (AD-18, AD-24, AD-45/68).
   - Spot-checked: the conflict 3 stated limits (FR-22); the conflict 4 move of the cutoff from 24 h to 1 h; the AP-7 restore plan (FR-47); "I've done it" does not close the fault (FR-52); the AP-11 "never unrecorded forward repairs" (FR-33); the AP-14 verification before closing (FR-22).
2. **Consistency:** no contradictions between the PRD, the UX and the architecture on the listed topics:
   - the approval-SMS permission: opt-in, its own permission, the post-decision notice under it, stops without a code, the post-stop notice on notifications;
   - the validity tiers, with no exception for approvals already received;
   - the exact Fleet service channel fields (PRIV-9 = Glossary = appendix A flows 1/6/6a/15 = EXPERIENCE B6b);
   - the AWS poller as optional, and FR-12 under Fleet reports;
   - PRIV-4, AP-7, the hardware representative, "I've done it", first install, the BMC, storage full, capacity, the 2-minute undo, SEC-10.
3. **Overclaims:** none found. Every "guarantee" hit is a negation. No document calls roster updates "data-free"; the PRD, the UX and appendix A all state the roster data. "No customer data" is gone from the update text. Timing values are labelled as starting values to test.
4. **Section 10:** items 24-26 and 28-30 are really decided. Item 27 (C-14) is open. Nothing that was decided is still listed as open.
5. **IDs:** FR-1 to FR-52 each appear once, as do SEC-1 to SEC-10 and NFR-1 to NFR-8. Section 10 numbering is complete (1-33, 7a, 7b). The frontmatter says `status: draft`, `updated: 2026-11-15`. Set it to final when you finalise.

## Medium

- **M1 Received vs applied (AP-20):** FR-14 shows "received and applied by the cluster" as one state, and spine AD-18/conventions show "received/applied by cluster". FR-22 says the two are kept distinct, but the record only names "sent" and "applied". Fix: either add a distinct "received, not yet applied" state or reword FR-22.
- **M2 Glossary "Approval" (prd.md l.167):** it says approvals are confirmed with passkey + SMS. It does not mention the opt-in permission or that, without it, only the passkey-only fallback or no approval is possible.
- **M3 FR-22 stated limit (l.404):** a Fleet outage of over 1 h "pauses policy repairs". The stale tier and the spine pause every repair that needs Orvex authority. The wording is narrower than the rule.
- **M4 EXPERIENCE Notifications row (l.445):** "check the portal" for stops. FR-22 says portal status is a convenience, not proof. Better: "check for the cluster's receipt".
- **M5 EXPERIENCE frontmatter:** it says `status: final` while it holds new copy marked "pending UX review". Either label it or note it in the finalisation.
