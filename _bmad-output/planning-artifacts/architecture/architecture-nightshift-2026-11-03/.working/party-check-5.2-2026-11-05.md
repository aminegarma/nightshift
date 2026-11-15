# Party check of 5.2 (release and catalogue delivery): Flux, Argo CD and Rancher Fleet, 2026-11-05

Requested by Amine. The room: Winston (architecture), Vex (security), Moss (operations). **Nothing here changes the architecture until Amine decides.**

## Comparison (facts checked 2026-11-05 unless marked)

| | **Flux** | **Argo CD** | **Rancher Fleet** |
|---|---|---|---|
| Licence | Apache-2.0 (research, 2026-10-29) | Apache-2.0 (research) | Apache-2.0 (research) |
| How it works | Controllers **in each cluster** pull sources (Git, OCI, Helm) and apply them | Usually one **central** Argo CD that stores cluster credentials and manages remote clusters; it can also be installed in each cluster ([architecture](https://argo-cd.readthedocs.io/en/stable/operator-manual/architecture/)) | A central **Fleet controller**, plus an **agent in each cluster**. A "two-stage pull": the controller pulls from Git, agents pull from the controller ([architecture](https://fleet.rancher.io/explanations/architecture)) |
| Who opens connections | The cluster, outbound | Central mode: **Argo CD connects into each cluster** with its credentials | The agent: "The fleet controller does not initiate connections to downstream clusters" |
| Signed, pinned packages | OCI artifacts pinned by digest (`.spec.ref.digest`). **Cosign or Notation verification** with `.spec.verify`, **optional and off by default**. A failed check marks the source not verified and retries ([Flux OCIRepository](https://fluxcd.io/flux/components/source/ocirepositories/)) | OCI images supported as a source ([Argo CD OCI](https://argo-cd.readthedocs.io/en/stable/user-guide/oci/)). Signature checks cover **Git commits (GPG) only**: "not possible when using Helm or OCI application sources" ([source integrity, Git GPG](https://argo-cd.readthedocs.io/en/stable/user-guide/source-integrity-git-gpg/)). OCI signature verification: not documented as shipped | Not described on the architecture page *(unverified)* |
| Footprint per cluster | A few controllers, no UI | Per-cluster install: API server, repository server, application controller, plus supporting parts (heavier, includes a UI) | One agent |
| Central part to run | None required | The central instance holds every cluster's credentials | The Fleet controller (a Kubernetes cluster that 10,000 agents connect to) |
| Fit with Nightshift rules | Pull only; signature check available | Central mode breaks "clusters only connect out" and concentrates credentials. Per-cluster mode lacks OCI signature checks | Pull only. Signature checks would need to be added. The name clashes with "Quornex Fleet" |

## Findings

| # | Who | Finding |
|---|---|---|
| G1 | Vex | Central Argo CD holds credentials into every customer cluster: one breach reaches all of them. It breaks the outbound-only rule. Rejected for that mode |
| G2 | Vex | Flux's signature check is off by default. It must be required, and a cluster must refuse to start without it |
| G3 | Winston | **Separate delivery from trust.** Whatever tool fetches the packages, Nightshift checks the catalogue, policy and people-list signatures itself before use (SEC-5), and container images are checked at admission *(tool to choose; for example Sigstore policy-controller or Kyverno, unverified)*. Then reusing Quornex's existing tool is safe |
| G4 | Vex | GitOps controllers often run with very broad cluster rights. Flux's identity must be limited to Nightshift's own namespaces and objects *(feasibility to verify)* |
| G5 | Moss | Rancher Fleet's two-stage pull fits 10,000 clusters on paper, but its central controller is one more critical system at Orvex, and scale isn't stated on its architecture page *(unverified)*. Its name would confuse everyone in a Quornex Fleet design |
| G6 | Moss | If Quornex already runs Argo CD or Rancher Fleet, a second GitOps tool means two tools that could fight over the same objects. Reuse, with G3 |

## Recommendation

- **Flux in each cluster,** with digest pinning and signature verification **required**.
- **Reuse Quornex's existing tool if it has one,** but only together with G3: Nightshift verifies signatures itself, independently of the delivery tool.
- **Argo CD in central mode is rejected.** Rancher Fleet is rejected unless Quornex already runs it.

## Decisions for Amine

- **E1:** the delivery tool (Flux per cluster; reuse the existing Quornex tool if present).
- **E2:** separate trust from delivery (Nightshift verifies catalogue, policy and people-list signatures itself; images checked at admission).
- **E3:** limit the delivery tool's rights to Nightshift's namespaces (feasibility to verify).
