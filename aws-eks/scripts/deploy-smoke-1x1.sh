#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Create 1+1 EFA nodegroups ==="
eksctl create nodegroup -f "$ROOT/configs/nodegroups-efa-1x1.yaml"
echo
echo "=== Check EFA ==="
"$ROOT/efa/check-efa.sh"
echo
echo "=== Apply EFA test pod ==="
kubectl delete pod efa-test --ignore-not-found
kubectl apply -f "$ROOT/efa/efa-test-pod.yaml"
kubectl get pod efa-test -o wide
echo
echo "=== Apply NVMe check ==="
kubectl apply -f "$ROOT/nvme/nvme-check-daemonset.yaml"
kubectl get pods -l app=nvme-check -o wide
kubectl logs -l app=nvme-check --tail=200 || true
echo
echo "=== Apply NVMe mount ==="
kubectl apply -f "$ROOT/nvme/nvme-mount-daemonset.yaml"
kubectl get pods -l app=nvme-mount -o wide
kubectl logs -l app=nvme-mount --tail=200 || true
