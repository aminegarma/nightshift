# ID and section mapping: Nightshift PRD, 2026-10-31

Structural pass (reorganisation and de-duplication only; no rule, number or decision changed). Old numbering is the PRD as of 2026-10-30/31 before this pass; new numbering is by position in the reorganised `prd.md`. IDs not listed kept their number: FR-1 to FR-19, PRIV-1, PRIV-2, COST-1 to COST-3, COST-6, every SEC, NFR, SM and SM-C ID.

## Sections

| Old | New |
|---|---|
| 1 Vision | 1 Vision (now ends with a section map) |
| 2 Glossary | 4 Glossary |
| 3 Features (3.1-3.11) | 5 Features (5.1-5.11, same internal order) |
| 4 Constraints (4.1 Privacy, 4.2 Security, 4.3 Cost) | 6 Constraints (6.1, 6.2, 6.3) |
| 5 Model options | 7 Model options |
| 6 Users and key journeys | 2 Users and key journeys |
| 7 Non-functional requirements | 8 Non-functional requirements |
| 8 Success metrics | 9 Success metrics |
| 9 Scope and non-goals (9.1, 9.2) | 3 Scope and non-goals (3.1, 3.2) |
| 10 Open questions | 10 Open questions |
| 11 Requirements for the other deliverables | 11 Requirements for the other deliverables |

## Functional requirements

| Old | New | Note |
|---|---|---|
| FR-19 (hardware-faults block) | FR-20 | Split out of FR-19 as its own FR: "Hardware and provider-side faults: mitigate, report uncertainty, escalate". FR-19 keeps its number for problems without a tested repair. |
| FR-20 | FR-21 | |
| FR-21 | FR-22 | |
| FR-22 | FR-23 | |
| FR-23 | FR-24 | |
| FR-24 | FR-25 | |
| FR-25 | FR-26 | |
| FR-26 | FR-27 | |
| FR-27 | FR-28 | |
| FR-28 | FR-29 | |
| FR-48 | FR-30 | First FR in 5.7 |
| FR-29 | FR-31 | |
| FR-30 | FR-32 | |
| FR-31 | FR-33 | |
| FR-32 | FR-34 | |
| FR-33 | FR-35 | |
| FR-34 | FR-36 | |
| FR-35 | FR-37 | |
| FR-36 | FR-38 | |
| FR-37 | FR-39 | |
| FR-38 | FR-40 | |
| FR-39 | FR-41 | |
| FR-40 | FR-42 | |
| FR-41 | FR-43 | |
| FR-42 | FR-44 | |
| FR-43 | FR-45 | |
| FR-44 | FR-46 | |
| FR-49 | FR-47 | Second FR in 5.11 |
| FR-45 | (none) | Folded into the 5.11 description; it held only pointers to FR-6, FR-30 (now FR-32) and FR-15 |
| FR-46 | FR-48 | |
| FR-47 | FR-49 | |

Ranges: "FR-24 to FR-27" is now "FR-25 to FR-28"; "FR-35 to FR-38" (addendum) is now "FR-37 to FR-40"; "FR-8 to FR-10" and "FR-8 to FR-11" are unchanged.

## Privacy

| Old | New |
|---|---|
| PRIV-7 (allowed fields, recipients and destinations) | PRIV-3 |
| PRIV-3 (outbound check) | PRIV-4 |
| PRIV-4 (combined views) | PRIV-5 |
| PRIV-5 (customer code) | PRIV-6 |
| PRIV-6 (proving privacy) | PRIV-7 |

## Cost

| Old | New |
|---|---|
| COST-5 (proving the business case) | COST-4 |
| COST-4 (target) | COST-5 |

## User journeys (reordered by the product's flow: predict, approve, act, report, fleet)

| Old | New |
|---|---|
| UJ-4 (warned hours before checkout fails) | UJ-1 |
| UJ-1 (approves a rollback while checkout is failing) | UJ-2 |
| UJ-5 (approves a ticked risky repair) | UJ-3 |
| UJ-3 (reads the night's summary) | UJ-4 |
| UJ-2 (one big problem across 300 clusters) | UJ-5 |

## Open questions

Numbers unchanged. Items 7, 9, 10 and 11 (answered or decided) moved to an "Answered and decided" list at the end of Section 10.

## New IDs added on 2026-11-02 (Update after Danny's Exchange 5; no renumbering)

- FR-50: Rejecting a request (5.5)
- FR-51: Agreed management policy (5.5)
- FR-52: Dangerous repairs are manual in the first version (5.4)
- PRIV-8: External AI only with the customer's explicit consent
- PRIV-9: Every outbound channel is permitted explicitly
- Section 10 items 18 (approval validity), 19 and 20 (danny-qa #3 and #4)
