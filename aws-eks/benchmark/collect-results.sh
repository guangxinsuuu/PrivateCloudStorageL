#!/usr/bin/env bash
set -euo pipefail
OUT_DIR=${OUT_DIR:-results/$(date +%Y%m%d-%H%M%S)}
mkdir -p "$OUT_DIR"
echo "Collecting cluster state into $OUT_DIR"
kubectl get nodes -o wide > "$OUT_DIR/nodes.txt"
kubectl get nodes -L role,node.kubernetes.io/instance-type > "$OUT_DIR/nodes-labeled.txt"
kubectl get pods -A -o wide > "$OUT_DIR/pods.txt"
kubectl get svc -A > "$OUT_DIR/services.txt"
kubectl get pvc -A > "$OUT_DIR/pvc.txt"
kubectl get events -A --sort-by=.lastTimestamp > "$OUT_DIR/events.txt" || true
kubectl top nodes > "$OUT_DIR/top-nodes.txt" || true
kubectl top pods -A > "$OUT_DIR/top-pods.txt" || true
for ns in default threefs fdb kube-system; do
  mkdir -p "$OUT_DIR/logs/$ns"
  kubectl get pods -n "$ns" --no-headers 2>/dev/null | awk '{print $1}' | while read -r p; do
    kubectl logs -n "$ns" "$p" --all-containers --tail=500 > "$OUT_DIR/logs/$ns/$p.log" 2>&1 || true
  done
done
echo "DONE: $OUT_DIR"
