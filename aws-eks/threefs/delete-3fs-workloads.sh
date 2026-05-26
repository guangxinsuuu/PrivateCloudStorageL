#!/usr/bin/env bash
set -euo pipefail
echo "=== Helm releases ==="
helm list -A || true
for ns in threefs fdb default; do
  helm list -n "$ns" --short 2>/dev/null | grep -Ei "3fs|three|fdb|foundation" | while read -r r; do
    echo "helm uninstall $r -n $ns"
    helm uninstall "$r" -n "$ns" || true
  done
done
kubectl delete job -n threefs threefs-fuse-fio --ignore-not-found || true
kubectl delete job -n threefs threefs-usrbio-fio --ignore-not-found || true
kubectl delete job -n threefs threefs-checkpoint-benchmark --ignore-not-found || true
kubectl delete job -n threefs threefs-metadata-heavy --ignore-not-found || true
echo "DONE"
