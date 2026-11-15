# Failure catalogue: top 20 (design draft, accepted by Amine 2026-11-11)

**What this is:** a design deliverable. It is **not** proof that any repair has been tested or approved to run. A "proposed catalogue repair" becomes a real catalogue entry only after testing and two reviewers (FR-39).

**Rules for every entry (Amine, 2026-11-11):**
- **Prediction** and lead times depend on the signals being available; they are not guarantees.
- **Risk and approval** depend on the exact action, target and effect on production (FR-21: platform-only vs customer production). The levels below are starting proposals.
- **Approval alone doesn't make an action safe.** Each action lists its support checks and preconditions; if any fails, the action doesn't run.
- **Fallbacks:** each entry says what happens when evidence is missing, the action fails, or rollback isn't possible.
- **Restore vs fix:** each entry separates *restoring service* from *fixing the underlying fault*.

**Ranking:** a labelled judgement (no fleet data yet), using impact on customer production if missed, then likelihood on cheap bare metal and EKS, then how much Nightshift can do.

**Sources:** facts checked 2026-11-11 against primary sources, recorded with quotes in `.working/round7-verification-storage.md`, `.working/round7-verification-nodes.md` and `.working/round7-verification-control.md`. "Unverified" marks what couldn't be confirmed.

**Defaults that apply everywhere:**
- **Missing or stale evidence:** no disruptive action; the panel shows "out of date" (O-1); escalate if the problem was already serious (coordinator point 8).
- **Kubernetes API unavailable:** no Kubernetes changes (AP-5).
- **Every action is checked again after it runs** (verification). If it didn't work, it isn't retried blindly: the RepairRun records the result and the problem goes to a person.

**Summary**

| # | Failure | Predict? (if signals exist) | Nightshift does | Underlying fix belongs to |
|---|---|---|---|---|
| 1 | Node disk filling | Yes, trend | Report; drain the node if eviction is near (risky) | Platform or customer (what is filling it) |
| 2 | Persistent volume filling | Yes, trend | Expand the volume (approval; can't be undone) | Customer (data growth) |
| 3 | Disk failing | Partly | Drain (risky); report | Customer hardware (OMK); AWS (EKS) |
| 4 | NIC hung or link flapping | Partly | Drain (risky); report | Customer hardware or network |
| 5 | L2/L3 network fault | Rarely | Report only; fleet correlation | Customer network (OMK); customer VPC config (EKS) |
| 6 | Node NotReady (incl. power) | Partly (power redundancy) | Report; EKS auto repair where enabled | Customer hardware (OMK); AWS (EKS) |
| 7 | Pods killed for memory | Yes, trend | Propose a limit change (approval) | Customer app or platform team |
| 8 | Memory hardware errors | Yes on OMK only | Drain (risky); report | Customer hardware |
| 9 | Customer app failing after a deploy | No | Roll back the Deployment (approval or rollback policy) | Customer app |
| 10 | Certificate expiry | Yes, dates | Trigger cert-manager renewal; control-plane certs: report | Platform (OMK); AWS for the EKS CA |
| 11 | etcd near its size limit or slow | Yes, size trend | OMK: compact and defragment (risky); EKS: report | Platform (OMK); AWS (EKS) |
| 12 | Kubernetes API overloaded or down | Partly | Report and escalate | Platform (OMK); AWS (EKS) |
| 13 | DNS failing | Partly | Report; restart CoreDNS only as a tested repair (risky) | Platform |
| 14 | Pod IP addresses running out | Yes, trend | Report | Network design (customer VPC on EKS) |
| 15 | Clock drift | Yes, offset | Report; time-limited approvals blocked | Platform or customer hardware |
| 16 | Image pull failures | No | Report | Customer app or registry |
| 17 | Volume stuck attaching | No | Report and escalate | Platform or AWS |
| 18 | Storage backend degraded | Partly | Report | Customer storage (OMK); AWS (EKS) |
| 19 | Bad release across many clusters | No | Stop rollout; rollback guard | Orvex |
| 20 | Not enough capacity | Yes, recurring pattern | EKS: propose scaling (approval); OMK: report | Customer (capacity) |

---

## 1. Node disk filling (images, logs, ephemeral storage)

- **Signals (both platforms):** node `DiskPressure`; filesystem metrics. Default hard eviction thresholds: `nodefs.available<10%`, `imagefs.available<15%`, inodes `<5%`.
- **Predict:** yes, from the fill trend, if metrics are fresh.
- **What Kubernetes already does:** the kubelet deletes dead containers and unused images itself (image cleanup from 85% down to 80% by default). Kubernetes advises *against* outside cleanup tools ("can break the kubelet behavior"). **So Nightshift doesn't delete images itself.**
- **Restore:** if eviction is imminent and the kubelet's own cleanup isn't enough, cordon and drain the node (risky; same preconditions as #4).
- **Fix:** report what is filling the disk (logs, images, emptyDir) to the owner.
- **No evidence:** report only. **Drain fails:** see #4. **Rollback:** uncordon; evicted pods aren't restored.

## 2. Persistent volume filling (customer data, databases)

- **Signals (both):** `kubelet_volume_stats_available_bytes` (an alpha metric: it can change between releases).
- **Predict:** yes, from the trend.
- **Restore:** expand the volume. **Support checks:**
  - the StorageClass has `allowVolumeExpansion: true`;
  - the CSI driver supports expansion (the EBS CSI driver does);
  - the filesystem is XFS, Ext3 or Ext4;
  - the volume is in use by a pod (otherwise expansion doesn't finish);
  - EKS: fewer than 4 modifications in the last 24 hours, and none in progress.
- **Approval:** customer production, so the customer's approval (FR-21).
- **No rollback:** Kubernetes can't shrink a volume, and EBS can't cancel a modification or decrease a size. The approval screen must say so.
- **Action fails:** Kubernetes retries indefinitely. Nightshift reports it and stops; a person may retry with a smaller increase (still above the current size).
- **Fix:** the data growth is the customer's to address.

## 3. Disk failing

- **Signals:**
  - **OMK:** SMART through the separate `smartctl_exporter` (node_exporter has **no** SMART collector); node_exporter `diskstats` and `mdadm`; kernel I/O errors *(log pattern unverified)*.
  - **EKS:** EBS volume status (`impaired` stops I/O by default); EC2 `StatusCheckFailed_AttachedEBS`.
- **Predict:** partly (SMART warnings on OMK, if the BMC or disks expose them).
- **Restore:** drain the node so workloads move (risky; preconditions as #4).
- **Fix:** OMK: disk replacement is the customer's (they own the hardware). EKS: AWS's remedies are to wait, replace the volume, or stop/start the instance. Nightshift reports them and doesn't do them.
- **No rollback** for data already lost; Nightshift never touches the data.

## 4. NIC hung or link flapping

- **Signals:**
  - **OMK:** node_exporter `node_network_carrier_changes_total`, `node_network_up`; kernel message starting "NETDEV WATCHDOG".
  - **EKS:** node monitoring agent `NetworkingReady` condition (`InterfaceNotUp`, `InterfaceNotRunning`); its repair action is node replacement.
- **Predict:** partly (rising carrier changes or errors).
- **Restore:** cordon and drain (risky). **Preconditions:**
  - eviction through the Eviction API only, never bypassing PodDisruptionBudgets;
  - pods with local data (`emptyDir`) or without a controller need explicit approval, because their data is lost or they aren't recreated;
  - enough spare capacity on other nodes;
  - the claims ledger confirms no other repair is acting on the same workloads.
- **Action fails:** a `429` means a disruption budget blocks it **or** API rate limiting. Nightshift waits and reports; it never forces.
- **Rollback:** uncordon. Evicted pods aren't restored; `emptyDir` data is lost.
- **Fix:** NIC or cabling (customer hardware); on EKS, node replacement.

## 5. L2/L3 network fault (MTU, bonding, switch, routing)

- **Signals:**
  - **OMK:** node_exporter netdev/netclass; cross-node probes from the checker.
  - **EKS:** cross-node probes. The ENA `*_allowance_exceeded` counters show **traffic dropped for exceeding AWS limits, not network faults**; they're reported separately.
  - Kubernetes has no built-in L2/L3 signal *(unverified negative)*.
- **Predict:** rarely.
- **Action:** report only. Fleet correlation (5.5) groups many clusters at one site or Region.
- **Fix:** customer network (OMK) or customer VPC configuration (EKS).

## 6. Node NotReady (kubelet, crash, power supply)

- **Signals:**
  - **Both:** `Ready` becomes Unknown after 50 s without contact; pods stay 5 minutes by default (`tolerationSeconds=300`), then are evicted.
  - **OMK:** Redfish `PowerSubsystem` → PowerSupply `LineInputStatus` (`LossOfInput`); older BMCs may expose only the deprecated `Power` resource *(per vendor, unverified)*.
  - **EKS:** `StatusCheckFailed_System` includes loss of power.
- **Predict:** partly: a lost redundant power supply warns before total loss.
- **Restore:** Kubernetes moves the pods itself after 5 minutes.
  - **EKS auto repair** replaces the node where enabled (Auto Mode always; managed node groups and Karpenter opt-in). It waits 30 minutes and pauses when more than 20% of nodes are unhealthy. On Auto Mode it **bypasses disruption budgets**. Nightshift reports that it happened; it doesn't trigger it.
- **Fix:** OMK: the customer's hardware. EKS: AWS.
- **No evidence** (BMC unreachable): "unreachable from the checker", never "dead" (3.4).

## 7. Pods killed for running out of memory (OOM)

- **Signals (both):** container `lastState` terminated, reason `OOMKilled`, exit code 137.
- **Predict:** yes, from memory trend against the limit.
- **Restarting doesn't fix it:** the kubelet already restarts the container, and it's killed again.
- **Restore:** propose a higher memory limit on the Deployment (a new revision and rollout). Approval needed (customer production for customer apps). In-place resize (stable since Kubernetes 1.35) changes only the running pod and is lost on the next rollout, so it isn't used as the repair.
- **Fix:** the app's memory use (customer) or the platform component's sizing (platform team).
- **Rollback:** roll the Deployment back (see #9).

## 8. Memory hardware errors (ECC)

- **Signals:**
  - **OMK:** node_exporter `node_edac_correctable_errors_total` and `uncorrectable` (with DIMM labels); BMC event log.
  - **EKS:** **not visible**: AWS's node monitoring agent reports no host memory errors (GPU only). EC2 scheduled events (for example `instance-retirement`) are the only signal.
- **Predict:** OMK yes (correctable errors rising); EKS no.
- **Restore:** drain (risky; preconditions as #4).
- **Fix:** OMK: DIMM replacement (customer). EKS: AWS.

## 9. Customer app failing after a deploy (UJ-2)

- **Signals (both):** `CrashLoopBackOff`; the Deployment condition `ProgressDeadlineExceeded` (default 600 s); app health checks.
- **Predict:** no.
- **Restore:** `kubectl rollout undo`, under approval or the customer's rollback policy (FR-47). **Support checks:**
  - a previous revision exists (`revisionHistoryLimit` > 0; EKS guidance suggests as low as 2);
  - the previous revision was healthy.
- **Limit:** a rollback restores only the pod template. ConfigMaps, Secrets and database migrations aren't reverted *(inference from Kubernetes' revision rule)*. If the bad deploy changed those, rollback may not restore service; the request must say so.
- **Fix:** the customer's code.

## 10. Certificate expiry

- **Signals:**
  - **OMK:** `kubeadm certs check-expiration` *(assumes OMK is kubeadm-like, to confirm)*; leaf certs last 1 year.
  - **Both:** cert-manager Certificate status for ingress and app certificates.
  - **EKS:** AWS manages the cluster CA and appends a successor CA automatically. The customer updates self-managed nodes and outside kubeconfigs.
- **Predict:** yes (dates).
- **Restore:**
  - cert-manager certificates: trigger renewal (`cmctl renew`; deleting the Secret isn't recommended). Proposed risk: safe for platform certificates, depending on target.
  - OMK control-plane certificates: renewal must run on **every** control-plane node, then the control-plane pods must restart. That's risky and has no documented undo, so it is **reported for a person**, not automated in v1.
- **Fix:** the platform team's certificate process (kubeadm renews automatically during upgrades).

## 11. etcd near its size limit or slow

- **Signals:**
  - **OMK:** default quota 2 GiB (8 GiB suggested max); `etcd_disk_wal_fsync_duration_seconds`; `etcd_server_has_leader`.
  - **EKS:** CloudWatch `etcd_mvcc_db_total_size_in_use_in_bytes` (decides read-only mode); standard mode up to 8 GB.
- **Predict:** yes, from the size trend.
- **When full:** etcd enters a mode that accepts only reads and deletes: the cluster can't change anything.
- **Restore:**
  - **OMK:** compact, defragment one member at a time (defrag blocks that member), then disarm the alarm. Risky; Orvex platform approval.
  - **EKS:** AWS defragments itself; the only lever is deleting objects, so report.
- **Fix:** whatever is creating too many objects.

## 12. Kubernetes API overloaded or down

- **Signals (both):** checker probes; `apiserver_flowcontrol_rejected_requests_total`. EKS CloudWatch: `apiserver_request_total_429`, `_5XX`, P99 latency.
- **Predict:** partly (rising rejections and latency).
- **Action:** report and escalate (AP-5). EKS standard mode scales the control plane itself; provisioned mode doesn't scale automatically.
- **During the outage:** no Kubernetes changes; observation and escalation continue where their dependencies work (round 6 D1).

## 13. DNS failing (CoreDNS)

- **Signals (both):** `coredns_dns_responses_total` by response code (SERVFAIL rising); `coredns_proxy_*` (the `forward` metrics are deprecated); DNS probes.
- **Predict:** partly.
- **Restore:** Kubernetes' DNS debugging guide doesn't document a CoreDNS restart as a fix. A restart is therefore **only a tested catalogue repair, risky**: DNS for the whole cluster can blip.
- **EKS:** the CoreDNS add-on overwrites direct changes, and editing fields it manages stops EKS managing it. Configuration goes through the add-on's `configurationValues`.
- **Fix:** the cause (upstream DNS, load, configuration). Report.

## 14. Pod IP addresses running out

- **Signals:**
  - **EKS:** subnet `availableIpAddressCount`; CNI Metrics Helper *(exact metric names unverified)*.
  - **OMK:** depends on the CNI *(unknown, to confirm)*.
- **Predict:** yes, from the trend.
- **Action:** report only. Prefix delegation needs new node groups and is effectively not reversible; AWS recommends network redesign (IPv6, secondary CIDR) instead.
- **Fix:** network design.

## 15. Clock drift or time sync failure

- **Signals:** chrony status (not synchronised; offset). EKS nodes use Amazon Time Sync by default on AL2023. node_exporter `timex` *(metric names unverified on a primary source)*.
- **Predict:** yes, from the offset trend.
- **Action:** report. Nightshift refuses time-limited approvals on that cluster (5.6 G-C). No automatic clock stepping: chrony warns that "certain software will be seriously affected by such jumps".
- **Fix:** the time source or its network path.

## 16. Image pull failures

- **Signals (both):** `ImagePullBackOff` (Kubernetes retries with back-off up to 5 minutes).
- **Predict:** no.
- **Action:** report the reason (wrong name, missing pull secret, registry down). Kubernetes already retries.
- **Fix:** the customer or the registry.

## 17. Volume stuck attaching or detaching

- **Signals:** VolumeAttachment objects; "Multi-Attach error" events; on EKS, attachment slots running out.
- **Predict:** no.
- **Action: report and escalate only.**
  - EBS force detach is "only as a last resort" and can damage the file system.
  - Kubernetes' safe route (the `out-of-service` taint) requires that the node is **verified** powered off. On EKS that means EC2 state; on OMK, the BMC.
  - Kubernetes already force-detaches after 6 minutes on an unhealthy node, with a risk of data corruption if the workload is still running.
- **Possible later catalogue repair:** the `out-of-service` taint, only with verified power-off and Orvex approval.

## 18. Storage backend degraded

- **Signals:**
  - **EKS:** EBS volume status (`warning`, `impaired`), I/O performance degraded; `StatusCheckFailed_AttachedEBS`.
  - **OMK:** the storage system is unknown *(to confirm with Orvex)*. Only Kubernetes symptoms: PVC events, VolumeAttachment, volume stats.
- **Action:** report.
- **Fix:** the storage owner.

## 19. Bad release across many clusters (FR-32)

- **Signals:** Fleet correlation (5.5); `ProgressDeadlineExceeded`; probation check failures.
- **Action:** the rollout stops (5.4 R1). The rollback guard reverts within probation where the release is rollback-safe (R2). One consolidated alert.
- **Note:** Kubernetes itself takes no action on a stalled Deployment; recovery is Nightshift's and Fleet's job.

## 20. Not enough capacity (pods Pending; the 3 AM peak)

- **Signals (both):** `FailedScheduling` events ("insufficient cpu"); recurring usage patterns.
- **Predict:** yes, for recurring patterns.
- **Restore:**
  - **EKS:** propose scaling (`UpdateNodegroupConfig`, asynchronous, reversible by setting the values back). Customer approval because of cost. **Precondition:** no Cluster Autoscaler or Karpenter managing that group (it would override the change); with Auto Mode, capacity comes through NodePools instead.
  - **OMK:** report only (no spare hardware).
- **Action fails:** AWS can return insufficient capacity; report.
- **Fix:** the customer's capacity planning.

---

## Not in the top 20

- **Backup failures:** out of scope for this list. Nightshift never modifies or deletes backups, but may monitor their health where reading is authorised.
- **GPU faults:** only where customers run GPUs (EKS reports several GPU conditions).
- **Kernel panics:** covered by #6.
- **Security incidents:** report only.

## Open items for this catalogue

- OMK details to confirm with Orvex: distribution (kubeadm-like?), CNI, storage system, BMC Redfish support.
- Unverified metric names: CNI Metrics Helper, node_exporter `timex`, kernel I/O error patterns.
- Every proposed repair needs testing and two reviewers before it is a catalogue entry (FR-39).
