# Appendix C: Failure catalogue sources

Part of the architecture hand-in (2026-11-15). Primary-source checks (2026-11-11) behind `failure-catalogue.md`, with quotes and URLs. Process history: `.working/round7-verification-*.md`.

## Round 7 verification: storage items 1, 2, 3, 17, 18 (checked 2026-11-11; research agent, primary sources)

- **Corrections to assumptions:**
  - EBS modification limit is "up to four times within a rolling 24-hour period", each must complete before the next (docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html); not a 6-hour wait.
  - node_exporter has no SMART collector: SMART comes from prometheus-community/smartctl_exporter (needs smartmontools >= 7.0).
  - Kubernetes: "You should avoid using external garbage collection tools, as these can break the kubelet behavior and remove containers that should exist" (kubernetes.io garbage-collection). `crictl rmi --prune` as a supported action: UNVERIFIED.
- **1 Node disk:** DiskPressure on nodefs/imagefs/containerfs available and inodesFree; default hard thresholds nodefs.available<10%, imagefs.available<15%, nodefs.inodesFree<5%, imagefs.inodesFree<5%; kubelet reclaims by GC of dead pods/containers, then unused images; image GC high/low 85/80% (node-pressure-eviction; kubelet-config.v1beta1). No rollback for deleted images (re-pull).
- **2 PV filling:** kubelet_volume_stats_available_bytes (ALPHA metric). Expansion stable since 1.24; requires allowVolumeExpansion true, CSI driver support, XFS/Ext3/Ext4; online expansion; unused PVC needs a Pod to finish; failures retried until an admin acts; recovery by a smaller size still above status.capacity; **no shrinking** (persistent-volumes). EBS CSI supports resizing; EBS modifications can't be cancelled or decreased.
- **3 Disk failing:** bare metal: node_exporter diskstats, mdadm, hwmon, textfile; SMART via smartctl_exporter; kernel I/O error messages UNVERIFIED (no kernel.org quote). EKS: EBS volume status every 5 min, impaired disables I/O by default until re-enabled or autoEnableIO; warning = degraded performance (io1/io2/gp3) (monitoring-volume-checks); EC2 StatusCheckFailed_AttachedEBS; AWS remedies: wait, replace volume, stop/start instance (monitoring-system-instance-status-check).
- **17 Volume stuck:** VolumeAttachment objects; "Multi-Attach error"; EBS CSI FAQ: stuck attaching when attachment slots run out. Non-graceful shutdown (stable 1.28): taint node.kubernetes.io/out-of-service; precondition "it should be verified that the node is already in shutdown or power off state"; taint removed manually after recovery (node-shutdown). Automatic force detach after 6 min if node unhealthy; may corrupt data if workload still running; disable-force-detach-on-timeout on kube-controller-manager (EKS exposure UNVERIFIED). EBS Force Detach: "only as a last resort … can cause damage to the file system", irreversible, then fsck (ebs-detaching-volume). **Not an autonomous action.**
- **18 Backend degraded:** EKS: EBS volume status, I/O performance Degraded / Severely Degraded, AttachedEBS check. Bare metal: backend unknown (UNVERIFIED); only Kubernetes symptoms (PVC events, VolumeAttachment, volume stats).

## Round 7 verification: node and network items 4, 5, 6, 8, 20 (checked 2026-11-11; research agent, primary sources)

- **4 NIC hung or flapping:**
  - Bare metal: node_exporter netclass (enabled by default): node_network_carrier, carrier_changes_total, carrier_up/down_changes_total, node_network_up. Kernel: "NETDEV WATCHDOG: CPU: %d: transmit queue %u timed out %u ms" in sch_generic.c dev_watchdog() (read via the GitHub mirror); match on the prefix.
  - EKS: node monitoring agent NetworkingReady condition, reasons InterfaceNotUp / InterfaceNotRunning, repair action Replace (node-health-nma).
  - **Drain** (kubectl_drain): DaemonSet pods are never deleted (needs --ignore-daemonsets); --delete-emptydir-data loses local data; bare pods need --force; --disable-eviction bypasses PDBs (**never used**).
  - **Eviction API:** 429 = PDB block *or* rate limiting; 500 = several PDBs on one pod.
  - Undo = uncordon; evicted pods aren't restored, and emptyDir data is lost.
- **5 L2/L3:**
  - EKS: ENA allowance counters (bw_in/out_allowance_exceeded, pps_, conntrack_, linklocal_allowance_exceeded, conntrack_allowance_available), cumulative since driver reset, ENA ≥ 2.2.10 (monitoring-network-performance-ena). These are **shaping drops, not fault indicators**. The node monitoring agent emits them as events only, with no repair. Reachability Analyzer = configuration analysis, charged per run.
  - Bare metal: node_exporter netdev/netclass only.
  - Kubernetes has no native L2/L3 signal (unverified negative).
- **6 NotReady and power:**
  - Ready Unknown after node-monitor-grace-period (default 50 s): Unknown → unreachable taint, False → not-ready taint. Default tolerationSeconds 300 (pods stay bound 5 minutes).
  - Redfish: Power deprecated in favour of PowerSubsystem; PowerSupply LineInputStatus Normal / LossOfInput / OutOfRange. Older BMCs may expose only the legacy Power resource (unverified per vendor).
  - EKS: StatusCheckFailed_System includes "Loss of system power".
  - **EKS auto repair** (node-repair): Auto Mode (always on), managed node groups (opt-in) and Karpenter (feature gate); not Windows. Waits: Ready 30 min; Kernel / Networking / Storage / ContainerRuntime 30 min; AcceleratedHardware 10 min. **No repair** for DiskPressure or MemoryPressure. Stops when more than 20% of nodes are unhealthy (managed node groups larger than 5 nodes) and during an ARC zonal shift. Auto Mode and Karpenter before v1.15 delete pods with a minimal grace period, **bypassing PDBs**. Irreversible (node replaced).
- **8 Memory hardware:**
  - Bare metal: node_exporter edac (enabled by default): node_edac_correctable_errors_total, uncorrectable_errors_total, plus per-csrow/channel with dimm_label.
  - **EKS:** the node monitoring agent has **no host ECC detection** (GPU and Neuron only). EC2 scheduled events (instance-stop, instance-retirement, instance-reboot, system-reboot, system-maintenance) via describe-instance-status.
- **20 Capacity:**
  - Signal: FailedScheduling "insufficient cpu".
  - Cluster Autoscaler controls the ASG's DesiredReplicas.
  - Auto Mode: Karpenter-based, shaped by NodePools.
  - UpdateNodegroupConfig scalingConfig: asynchronous, update ID, 409 ResourceInUse, reversible by setting the values again. **A manual desiredSize can be overridden by Cluster Autoscaler (inferred).** Insufficient-capacity errors can block scale-up. Karpenter details unverified.

## Round 7 verification: control plane and app items 7, 9-16, 19 (checked 2026-11-11; research agent, primary sources)

- **7 OOM:**
  - Signal: lastState terminated, exitCode 137, reason OOMKilled; the kubelet restarts the container. Restart doesn't fix it ("killed, restarted, killed again").
  - In-place resize: stable since v1.35. CPU and memory only; QoS can't change; memory decrease best-effort; status via PodResizePending / PodResizeInProgress.
  - A resize edits the pod, not the Deployment template, so the next rollout discards it (inference). A limit change on the Deployment creates a new revision and a rollout.
- **9 Bad deploy:**
  - `kubectl rollout undo [--to-revision]`; 10 old ReplicaSets kept by default; revisionHistoryLimit 0 = no undo. A revision exists only when .spec.template changes.
  - Rollback doesn't revert ConfigMaps, Secrets or DB migrations: an inference from the template rule, not quoted.
  - EKS best practice revisionHistoryLimit 2 limits how far back.
- **10 Certificates:**
  - kubeadm certs check-expiration; leaf certs 1 year, CA 10 years. Renewal must run on all control-plane nodes, then the control-plane pods must be restarted (no dynamic reload); renewed automatically during upgrades. kubelet client certs rotate; kubelet serving CSRs aren't auto-approved. No documented undo (back up the pki directory first: assumption).
  - cert-manager renews at 2/3 of the duration by default; `cmctl renew`; deleting the Secret is not recommended.
  - EKS: AWS appends and activates a successor CA automatically. The customer updates self-managed nodes and external kubeconfigs; rollback possible until 45 days before expiry.
- **11 etcd:**
  - Default quota 2 GiB, suggested max 8 GiB. NOSPACE = maintenance mode (reads and deletes only). Recovery: compact, defrag, alarm disarm. Defrag blocks the member, so one member at a time (etcd.io v3.5). Metrics: etcd_disk_wal_fsync_duration_seconds, etcd_server_has_leader.
  - EKS: CloudWatch AWS/EKS etcd_mvcc_db_total_size_in_use_in_bytes (decides read-only mode), v1.28+; standard mode up to 8 GB, provisioned tiers 16/24 GB. EKS defragments itself; the customer's only lever is deleting objects.
- **12 API:**
  - apiserver_flowcontrol_rejected_requests_total, current_inqueue_request. EKS CloudWatch: apiserver_request_total_429 and _5XX, P99 latency.
  - EKS standard mode scales automatically; provisioned mode has no automatic tier scaling.
- **13 DNS:**
  - coredns_dns_responses_total by rcode; coredns_forward_* deprecated for coredns_proxy_*.
  - The Kubernetes DNS debugging page does **not** document restarting CoreDNS as a remedy.
  - EKS add-on: Corefile edits are overwritten; use configurationValues. Modifying managed fields stops EKS managing the add-on.
- **14 IPs:**
  - Subnet availableIpAddressCount; CNI Metrics Helper (awscni_* names unverified).
  - Prefix delegation: new node groups rather than a rolling replacement, effectively not reversible. Warm-pool settings reset on CNI update. AWS recommends VPC redesign (IPv6, secondary CIDR).
- **15 Clock:**
  - chronyc tracking; makestep warning ("Certain software will be seriously affected by such jumps").
  - EC2: Amazon Time Sync at 169.254.169.123, default on AL2023; the link-local limit is shared with DNS and IMDS.
  - node_exporter timex metric names unverified on a primary source.
- **16 Image pull:** ImagePullBackOff, back-off up to 300 s.
- **19 Bad release:** ProgressDeadlineExceeded (default 600 s). "Kubernetes takes no action on a stalled Deployment other than to report a status condition".

