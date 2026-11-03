# Notes for the bmad-prd Update (2026-11-02)

Input for the next `bmad-prd` Update. Decisions are canonical in `.memlog.md` (entries from 2026-11-02); Danny's reply is verbatim in `../../danny-qa.md` (Exchange 5). Items marked [AI] were drafted by the AI; Amine accepted all of them on 2026-11-02.

## Decided (Amine, after Danny's Exchange 5)

- Incident history is kept and linked to the validated repair.
- 99.9% is a working target, not a promise; it depends on the customer's hardware and on whether the installation is highly available.
- AI redaction alone never makes data safe to share; rule-based allowlists, placeholders and the outbound check are the protection.
- Dangerous repairs are manual in version 1: Nightshift explains, gathers evidence and suggests steps; a person performs the repair.
- Approval depends on what a repair changes: routine tested platform repairs that don't affect customer production run under the agreed management policy without a customer tick; risky platform changes need Orvex approval; anything affecting customer production also needs the customer. A change to OMK or Quornex can affect customer production.
- An advance tick counts as customer approval only for the specific tested action and conditions it covers.
- External AI needs explicit consent, offered at onboarding with nothing preselected (what leaves, which provider, zero retention). It covers ongoing use within its scope and is asked again only if that use changes. Source code stays a separate permission. Wording drafted with Codex.
- Hosted AI stays the focus of version 1. In-cluster AI if the hardware allows; without AI, rules and template explanations.
- "No external AI" and "no outbound data" are separate requirements. Fleet heartbeats are an outbound channel: explicitly permitted, outbound-checked, never silently exempt. If heartbeats are prohibited, the PRD states that Fleet cannot tell a healthy disconnected cluster from a failed one.
- Alert-only mode stops every change Nightshift executes, including routine platform repairs; monitoring, predictions and recommendations continue; no hidden exception. Kubernetes' normal controllers and separately authorised maintenance are outside this mode. Alert-only is an ongoing customer option, not restricted to trials; trying the product first is one use of it.

## [AI] drafts, accepted by Amine (2026-11-02)

1. **Agreed management policy.** A versioned list of routine, tested repairs to OMK and Quornex components, each from the repair catalogue with its exact action and conditions. Orvex authorises the content: each entry is approved by an authorised Orvex engineer from the Nightshift team after testing. The customer agrees to the policy as part of the managed-service contract and can read it in the portal. New versions are signed (SEC-9), recorded and notified. Limits: never a change affecting customer production, never risky or dangerous; if the pre-run checks show a policy repair would affect customer production, it goes to approval instead. Never runs in alert-only mode.
2. **No outbound data.** Nothing leaves the cluster by any channel unless the customer explicitly permits that channel: external AI, Fleet heartbeat, Fleet reports (sanitised information), notifications (Slack, phone), portal. Every permitted channel sends only its allowlisted fields and passes the outbound check.
3. **Heartbeat contents.** Agent ID, timestamp, status (alive / degraded).
4. **Consequences to document.** Without the heartbeat: Fleet can't detect a dead agent from outside (FR-6, NFR-4 no longer hold), while Nightshift keeps working locally (NFR-5). Without notifications as well: no alert or approval request reaches anyone outside the cluster; only repairs authorised in advance run; problems are visible only on an in-cluster dashboard.
5. **UX state.** "Heartbeat not permitted by the customer: status unknown", distinct from "No data since 02:10".

## Also queued from the UX run (UX memlog)

Approval expiry (overrides FR-22 "no timers"); Slack as notification only in version 1 (narrows FR-14); what Reject does; extra history outcomes; the expected-interruption field; the Glossary "Approval" entry's missing delegation exception.

## Still open with Danny (never sent)

Who defines a "high-confidence" repair (#3); what happens to an unanswered request at 3am (#4).
