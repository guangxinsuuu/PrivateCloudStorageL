#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== 0-3 min: preflight ==="
"$ROOT/scripts/preflight-all.sh"
echo
echo "=== 3-5 min: EFA sanity ==="
kubectl delete pod efa-libfabric-test --ignore-not-found
kubectl apply -f "$ROOT/benchmark/efa-libfabric-test-pod.yaml"
kubectl get pod efa-libfabric-test -o wide
sleep 20
kubectl logs efa-libfabric-test --tail=100 || true
echo
echo "=== 5-10 min: local NVMe fio ==="
kubectl delete job nvme-fio --ignore-not-found
kubectl apply -f "$ROOT/benchmark/nvme-fio-job.yaml"
kubectl logs -f job/nvme-fio || true
echo
echo "=== 10-20 min: USRBIO benchmark if configured ==="
if grep -q "REPLACE_WITH_3FS_CLIENT_OR_BENCHMARK_IMAGE" "$ROOT/benchmark/usrbio-fio-job-template.yaml"; then
  echo "Skipping USRBIO benchmark because image placeholder is not replaced."
else
  kubectl delete job -n threefs threefs-usrbio-fio --ignore-not-found || true
  kubectl apply -f "$ROOT/benchmark/usrbio-fio-job-template.yaml" || true
  kubectl logs -n threefs -f job/threefs-usrbio-fio || true
fi
echo
echo "=== 20-25 min: FUSE quick comparison ==="
kubectl delete job -n threefs threefs-fuse-fio --ignore-not-found || true
kubectl apply -f "$ROOT/benchmark/fuse-fio-job.yaml" || true
kubectl logs -n threefs -f job/threefs-fuse-fio || true
echo
echo "=== 25-30 min: collect results ==="
"$ROOT/benchmark/collect-results.sh"
echo
echo "IMPORTANT: delete expensive nodegroups if benchmark is done:"
echo "$ROOT/teardown/delete-efa-nodegroups.sh"
