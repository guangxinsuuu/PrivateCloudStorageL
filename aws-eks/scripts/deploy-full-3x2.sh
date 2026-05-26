#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Create 3+2 full EFA nodegroups ==="
eksctl create nodegroup -f "$ROOT/configs/nodegroups-efa-3x2.yaml"
echo
echo "=== Check EFA ==="
"$ROOT/efa/check-efa.sh"
echo
echo "=== Ensure NVMe mount DaemonSet exists ==="
kubectl apply -f "$ROOT/nvme/nvme-mount-daemonset.yaml"
kubectl get pods -l app=nvme-mount -o wide
kubectl logs -l app=nvme-mount --tail=200 || true
