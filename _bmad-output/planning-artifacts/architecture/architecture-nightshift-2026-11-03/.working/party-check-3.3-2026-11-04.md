# Party check of the 3.3 hardware design (OMK and EKS), 2026-11-04

Requested by Amine: check the AI's 3.3 proposal for architecture, security and operational coverage. The room: Winston (architect), Vex (security) and Moss (operations; the same ad-hoc personas as on 2026-11-03). **Nothing here changes the architecture until Amine decides.** The personas' claimed experience is not operational evidence.

## Findings

| # | Area | Finding | Proposed fix |
|---|---|---|---|
| H1 | Architecture | The EKS column covers EC2 and Fargate, but **EKS Hybrid Nodes** run on the customer's own machines. Their hardware is the customer's, as on OMK, and AWS doesn't repair it | Add a hybrid-nodes column that follows the OMK rules: hardware sources if the customer provides them (SMART, an optional BMC), otherwise limited visibility. The customer is responsible |
| H2 | Architecture | "The AWS node agent or node-problem-detector, never both" can lose signals: the two check different things | Disagreement: use the union of distinct checks with duplicates removed (Moss), or the AWS agent only, on EKS, to keep fewer privileged pods (Vex) |
| H3 | Architecture | Without BMC on OMK, the PRD's limited-visibility mode (FR-7) applies. The table didn't say so | Reference FR-7 in the OMK column |
| H4 | Architecture | Fargate isn't "none": pod status and probes still work | State what remains visible, and record the rest as unavailable in the coverage report |
| H5 | Security | AWS read access: many EC2 `Describe*` calls may not support resource-level limits, so the adapter could see instances outside its cluster *(to verify)* | Use a pod-identity role with the minimum calls. The adapter filters to its own nodes, and nothing from other clusters enters the evidence (PRIV-1). If the customer doesn't grant the role, coverage is reduced |
| H6 | Security | Privileged node exporters (SMART needs root; node-problem-detector reads host logs) on every node are attractive targets | Run each in its own pod with its own identity: read-only root filesystem, no egress except to the local metrics store, no Kubernetes write rights |
| H7 | Security | The OMK adapter needs a route to the BMC management network, which is a pivot path (addendum). BMC strings are untrusted input | Run the adapter on its own pod and identity, with network rules allowing only the listed BMCs. Fetch credentials just in time (SEC-3). Treat Redfish/IPMI and AWS text fields as untrusted (SEC-1) |
| H8 | Security | A compromised node can lie about its own health | Independent signals must come from different vantage points: BMC vs in-OS on OMK, EC2 status checks vs the node agent on EKS (SEC-1) |
| H9 | Operations | AWS auto repair acts on the same node agent conditions Nightshift reads | Nightshift reads them as evidence and never double-acts (coordinator point 5) |
| H10 | Operations | Coverage drifts: BMC credentials expire, firmware changes Redfish paths, IAM roles change | Revalidate coverage periodically. A coverage loss opens a monitoring failure case (FR-4) and updates the coverage report |
| H11 | Operations | AWS Health API access may need a paid support plan *(to verify)*. Scheduled events are also visible through `DescribeInstanceStatus` | Use `DescribeInstanceStatus` (status checks and scheduled events) as the base. Health and EventBridge are optional |
| H12 | Operations | AWS API polling across many clusters may hit per-account rate limits *(estimate)* | Poll slowly [interval to set] and back off. It's a cost-model and test input |

## Disagreements

- **D1 (H2):** both node checkers with duplicates removed (Moss), or only the AWS agent on EKS (Vex). Winston: union of distinct checks, but on Auto Mode only what AWS allows.
- **D2 (H5):** broad AWS read access for full coverage (Moss), or minimal access and accept reduced coverage (Vex). Winston: discovery from Kubernetes node data first, the AWS API as an optional, customer-granted extra.
- **D3 (H6):** one combined privileged node agent to cut pods (Moss), or one minimal pod per exporter (Vex).

## Assumptions and items to verify

- Resource-level permissions of EC2 `Describe*` calls (to verify).
- Whether the AWS Health API needs a paid support plan (to verify).
- How the EKS node monitoring agent is installed, and whether Auto Mode includes it (to verify).
- Who owns the EKS AWS account for a Quornex customer (to confirm).
- AWS API rate limits at fleet scale (estimate).
- Whether BMCs enforce read-only accounts (to test).
