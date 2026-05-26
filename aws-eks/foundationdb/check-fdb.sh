#!/usr/bin/env bash
set -euo pipefail
echo "=== FDB namespace ==="
kubectl get ns fdb || true
echo
echo "=== FDB pods ==="
kubectl get pods -n fdb -o wide || true
echo
echo "=== FDB services ==="
kubectl get svc -n fdb || true
echo
echo "=== FDB pvc ==="
kubectl get pvc -n fdb || true
echo
echo "=== FDB-related all namespaces ==="
kubectl get pods -A | grep -Ei "fdb|foundation" || true
