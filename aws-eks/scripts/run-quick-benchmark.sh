#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== Preflight ==="
"$ROOT/scripts/preflight-all.sh"
echo
echo "=== Local NVMe fio ==="
kubectl delete job nvme-fio --ignore-not-found
kubectl apply -f "$ROOT/benchmark/nvme-fio-job.yaml"
kubectl logs -f job/nvme-fio || true
echo
echo "=== FUSE fio ==="
kubectl delete job -n threefs threefs-fuse-fio --ignore-not-found || true
kubectl apply -f "$ROOT/benchmark/fuse-fio-job.yaml" || true
kubectl logs -n threefs -f job/threefs-fuse-fio || true
echo
echo "=== Checkpoint benchmark ==="
kubectl delete job -n threefs threefs-checkpoint-benchmark --ignore-not-found || true
kubectl apply -f "$ROOT/benchmark/checkpoint-benchmark-job.yaml" || true
kubectl logs -n threefs -f job/threefs-checkpoint-benchmark || true
echo
echo "=== Metadata-heavy benchmark ==="
kubectl delete job -n threefs threefs-metadata-heavy --ignore-not-found || true
kubectl apply -f "$ROOT/benchmark/metadata-heavy-job.yaml" || true
kubectl logs -n threefs -f job/threefs-metadata-heavy || true
echo
echo "=== Collect results ==="
"$ROOT/benchmark/collect-results.sh"
