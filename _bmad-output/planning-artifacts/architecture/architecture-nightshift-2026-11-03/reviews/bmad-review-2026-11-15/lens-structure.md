# Editorial structure lens: architecture-orvex.md (2026-11-15)

**Purpose read:** helps Orvex engineers and the sponsor (Danny) understand Nightshift's design, its reasoning and trade-offs, and what still needs Orvex input on both OMK and EKS. It also has to support a 15-minute walkthrough.

**Structure model:** Explanation (conceptual), with a strategic/pyramid need for the sponsor.
- **Works:** abstract-to-concrete ordering.
- **Falls short:** top-down for a decision-maker. The cost verdict, risks and requests to Orvex appear only in §11–§12.

| Pass | Original text | Revised text | Changes |
|---|---|---|---|
| structure | §1 Overview has no bottom line; the cost verdict and main open dependencies appear only in §11.1 and §12.2 | ADD a 3–4 sentence "Bottom line" at the top of §1: the cost result under assumptions, nothing tested yet, and the top items Orvex must answer. Link to §11 and §12 | Sponsor-critical conclusions first (~+80 words) |
| structure | Front matter has no reading path for a 15-minute walkthrough | ADD a one-line reading guide (e.g. §1, 2.3, 3.3, 4.1–4.3, 4.12, 10, 11.4, 12.2) | Expectation-setting (~+40 words) |
| structure | The label legend explains AD ids only; AP, FR, PRIV, SEC, NFR, SM, COST, O-n, M2, D and G are unexplained | ADD the sources of these ids to the legend | Missing scaffolding (~+35 words) |
| structure | §4 has 12 subsections (~22% of the document) mixing human authority (4.1–4.9) with network, egress and compromise analysis (4.10–4.12) | MOVE: split into §4 Trust and approvals and a new §5 Security boundaries and outbound data, then renumber | Two mental models in one section |
| structure | §7.6 Group approvals sits under Fleet, and §4.3 points ahead to it | MOVE to §4 after option B, with a pointer left in 7.1 | Avoids a forward reference |
| structure | §4.9 "What the relay, registry and group-confirmation service can't do" overlaps with 4.12 and the 7.1 "Can't" column | MERGE into 4.8 as one bullet | Three-way overlap (~−30 words) |
| structure | The gateway-bypass rule is restated in §1, §2.2, §4.10, §4.11 and §12.5 | CONDENSE: keep the full statement in 4.10 and the AP-8 row; shorten §2.2 to a pointer | Repetition (~−40 words) |
| structure | §2.3 and §5 close with long runs of inline evidence citations | MOVE them to tool-comparison.md or a compact "Sources" note per section | Breaks flow after the key table (~−150 words) |
| structure | §6.6 Expected model calls has two tables | CONDENSE: keep the derived table; move the input table to cost-model/README.md | Working detail (~−140 words) |
| structure | §11.4 "What moves the cost most" comes after three dense tables | MOVE it to open §11 | Front-loads the interpretation |
| structure | §12.3 "Decided since the last version (removed)" | CUT | An author change log; Orvex never saw an earlier version (~−45 words) |
| structure | Links to `.working/` files (outbound flows, PRD change queue, verification notes) and "synced with spine AD-1..AD-71" | QUESTION: does Orvex receive `.working/`? If not, mark these as internal or move the files out. 4.11 relies on the flow table being reachable | Risk of broken links for the audience |
| structure | Offline behaviour is split across 4.6 (tiers), 8.1 (dependencies) and 7.9 | QUESTION: move the tiers table to 8.1, or cross-reference it | Readers of §8 get half the picture |
| structure | §9 Rejected row "Fine-tuned model … Deferred (6.5)" | CUT the row | Duplicate, and not an open-source alternative |
| structure | Mixed heading numbering; some headings carry round labels and status ("round 4", "M2") | CONDENSE: number all subsections consistently; move status notes into section bodies | Consistent scaffolding |
| structure | §1 picture and §2.2 topology, two overlapping diagrams | PRESERVE | Both help comprehension |
| structure | §3.3 crash example, §4.12 compromise table, §12 registers | PRESERVE | §12 is where Orvex can act from |
| structure | §10 Failure catalogue summary placed after §9 tool choices | QUESTION: place it before §9 or reference it from §1 | A primary deliverable |

**Summary:** 18 recommendations: 3 add, 4 move, 1 merge, 4 condense, 2 cut, 2 preserve, 2 questions. About 410 words removed and 155 added, a net cut of about 255 words (2.2%). Trade-off: moving inline citations makes the body less self-evidencing, so the linked sources must stay reachable.
