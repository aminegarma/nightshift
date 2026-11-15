# Round 7 Failure catalogue: candidate list and format (proposal, 2026-11-05, not decided)

AI proposal for Amine. Sources for the list: the challenge (hung NICs, full memory, disks, links), Danny Exchange 4 (disk, NIC and power-supply failures, L2/L3 networking, misconfigurations, Kubernetes issues; customers own their hardware), the brief addendum (hardware is a central case on cheap bare metal), PRD UJ-2 and FR-32. **The ranking is an assumption:** there is no fleet data yet. Signals and repair details are verified per entry when the full catalogue is written.

## Ranking criteria (proposal)
1. Impact on customer production if missed.
2. Likelihood on cheap, poorly maintained bare metal and on EKS *(judgement, not measured)*.
3. How much Nightshift can do: predict, repair, or only report.

## Format of each full entry
Failure · signals on OMK · signals on EKS · predict (lead time, confidence) · Nightshift action (catalogue repair and its risk, or report only) · who owns the fix (customer hardware, OMK/Orvex, AWS, customer app) · approval needed · verification · sources.

## Candidate list (one line each)

| # | Failure | OMK signal | EKS signal | Predict? | Nightshift action |
|---|---|---|---|---|---|
| 1 | Node disk filling (images, logs, ephemeral) | Node metrics, kubelet DiskPressure | Same | Yes (trend) | Safe cleanup of platform-owned files; else report |
| 2 | Persistent volume filling (customer data, DB) | Volume metrics | Same (EBS) | Yes (trend) | Expand volume if the storage class allows (customer production: approval); else report |
| 3 | Disk failing | SMART, kernel I/O errors, read-only remount | EBS status checks; instance store errors | Partly (SMART) | Cordon and drain (risky); replacement is the customer's: report |
| 4 | NIC hung or link flapping | Kernel NIC watchdog, link and error counters | Instance status checks; ENI errors | Partly (error counters rising) | Cordon and drain (risky); report |
| 5 | L2/L3 network fault (MTU, bonding, switch, routing) | Cross-node probes, packet loss | VPC reachability, cross-node probes | Rarely | Report only (customer network); fleet correlation |
| 6 | Node NotReady (kubelet, crash, power supply) | Node condition; BMC power and PSU sensors | Node condition; status checks | Partly (PSU redundancy lost) | Provider-native replacement on EKS (if the node mode allows); kubelet restart (risky); report |
| 7 | Pods killed for memory (OOM) | Container restarts, OOMKilled | Same | Yes (trend) | Platform pods: safe restart. Customer app: propose a limit change (approval) |
| 8 | Memory hardware errors (ECC) | EDAC counters, BMC event log | Status checks (AWS-managed hardware) | Yes (correctable errors rising, OMK) | Cordon and drain (risky); report |
| 9 | Customer app failing after a deploy (CrashLoopBackOff, failed health checks; UJ-2) | Pod status, app health checks | Same | No | Roll back the deployment (approval or rollback policy) |
| 10 | Certificate expiry | Cert expiry dates (control plane, kubelet, ingress) | Ingress and app certs (control plane AWS-managed) | Yes (dates) | Trigger renewal where safe; control-plane certs: report |
| 11 | etcd near its size limit or slow | etcd metrics | AWS-managed: API latency only | Yes (size trend) | Compaction or defragmentation (risky); report on EKS |
| 12 | Kubernetes API overloaded or down | API probes (checker) | Same | Partly | Report and escalate (AP-5) |
| 13 | DNS failing (CoreDNS) | DNS probes, CoreDNS errors | Same (add-on) | Partly | Restart CoreDNS pods (safe); scaling (risky) |
| 14 | Pod IP addresses running out | CNI IP pool metrics *(CNI unknown for OMK)* | VPC CNI subnet free IPs | Yes (trend) | Report (subnet or pool changes are infrastructure) |
| 15 | Clock drift or time sync failure | chrony status | Time sync status | Yes (offset trend) | Report; blocks time-limited approvals (6 D6) |
| 16 | Image pull failures (registry, credentials, limits) | Pod events | Same | No | Report; retry is Kubernetes' own |
| 17 | Volume stuck attaching or detaching | CSI and attach events | EBS attach errors | No | Detach and reattach (risky, approval) |
| 18 | Storage backend degraded | Storage system health *(OMK storage unknown)* | EBS volume status | Partly | Report |
| 19 | Bad release across many clusters (FR-32) | Fleet correlation | Same | No | Rollout stop, rollback guard (5.4) |
| 20 | Not enough capacity (pods Pending; the 3 AM peak) | Scheduler events, usage pattern | Same | Yes (recurring pattern) | EKS: scale nodes if the policy allows (cost, approval); OMK: report (no spare hardware) |

## Not in the top 20 (to say so in the document)
GPU faults (only where customers run GPUs), kernel panics as a separate item (covered by 6), security incidents (out of scope for repair; report), backups (out of scope: never touched by Nightshift).
