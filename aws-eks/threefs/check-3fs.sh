#!/usr/bin/env bash
set -euo pipefail
echo "=== namespaces ==="
kubectl get ns | grep -E "threefs|fdb" || true
echo
echo "=== 3FS pods ==="
kubectl get pods -n threefs -o wide || true
echo
echo "=== FDB pods ==="
kubectl get pods -n fdb -o wide || true
echo
echo "=== services ==="
kubectl get svc -n threefs || true
kubectl get svc -n fdb || true
echo
echo "=== pvc ==="
kubectl get pvc -n threefs || true
kubectl get pvc -n fdb || true
echo
echo "=== recent events threefs ==="
kubectl get events -n threefs --sort-by=.lastTimestamp | tail -50 || true
echo
echo "=== logs summary ==="
kubectl get pods -n threefs --no-headers 2>/dev/null | awk '{print $1}' | while read -r p; do
  echo "--- $p ---"
  kubectl logs -n threefs "$p" --all-containers --tail=50 || true
done
