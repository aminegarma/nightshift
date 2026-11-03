# Prose polish: addendum.md

**Purpose read:** this document exists to help the architecture author pick up design depth that the Nightshift PRD deliberately pushed downstream, with each point traced to its source.

**Scope:** prose lens only. The structure pass did not run, so there are no CUT or MERGE tags to respect. Reader type: humans. Word count: 145 (11 in the title block, 126 under "For the architecture").

**Voice and style to preserve:** terse, note-like register; bold lead-in labels with parenthetical status tags (FR numbers, "unconfirmed", "unverified"); sentence fragments ("Depth that belongs downstream…", "Basis: …"); the arrow chain as a compact pipeline notation; bracketed source tags. British spelling and no serial comma are author directives and are not flagged.

| Pass  | Original Text | Revised Text | Changes |
| ----- | ------------- | ------------ | ------- |
| prose | Basis: Danny mentions the launch hosting provider in his bare-metal paragraph and as where Quornex Fleet runs (danny-qa Exchange 4). | Basis: Danny names the launch hosting provider both in his bare-metal paragraph and as the place where Quornex Fleet runs (danny-qa Exchange 4). | The two halves after "and" were not parallel ("in his … paragraph" and "as where … runs"), so the sentence read as garbled. "Both … and" plus "the place where" make the two mentions parallel. |
| prose | so that if Prometheus stops, Nightshift still notices | Consider: "so that if Prometheus stops, Nightshift still notices [that Prometheus has stopped / faults on the fleet]"? | "Notices" has no object, so the reader cannot tell what Nightshift keeps detecting. The author should supply the intended object. The meaning is not changed. |
| prose | **Where Quornex Fleet runs (AI reading, unconfirmed):** | Consider: **Where Quornex Fleet runs (AI's reading, unconfirmed):** | "AI reading" can be read as "the AI is reading". The possessive makes it clear that this is the AI's interpretation, and it matches "AI's session-2 coaching feedback" in the next bullet. |
| prose | the architecture may name the provider for the prototype | Consider: "the architecture is free to name the provider for the prototype"? | "May" can mean permission or possibility. If permission is meant, "is free to" removes the ambiguity. If possibility is meant, keep "may". |
| prose | independent from Prometheus | independent of Prometheus | "Independent of" is the standard idiom. |
| prose | sanitised evidence → a person diagnoses → rule and fix → replay test | Consider: "sanitised evidence → human diagnosis → rule and fix → replay test"? | "A person diagnoses" is the only clause in a chain of noun phrases, so it breaks the rhythm of the pipeline. Leave it as is if the clause wording is deliberate, for example to stress that a human is in the loop. |
| prose | not hosted Kubernetes like EKS | not hosted Kubernetes such as EKS | The Microsoft Writing Style Guide uses "such as" to introduce examples, and keeps "like" for comparisons. |

The addendum has 7 prose recommendations: 3 definitive and 4 phrased as "Consider". None of them changes the content or the bracketed source tags.
