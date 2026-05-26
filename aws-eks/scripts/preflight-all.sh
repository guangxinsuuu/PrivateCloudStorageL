#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "=== AWS identity ==="
aws sts get-caller-identity
echo
echo "=== Region ==="
aws configure get region || true
echo
echo "=== EKS clusters ==="
aws eks list-clusters --region us-east-1
echo
echo "=== kubectl nodes ==="
kubectl get nodes -L role,node.kubernetes.io/instance-type -o wide
echo
echo "=== EFA ==="
"$ROOT/efa/check-efa.sh" || true
echo
echo "=== FDB ==="
"$ROOT/foundationdb/check-fdb.sh" || true
echo
echo "=== 3FS ==="
"$ROOT/threefs/check-3fs.sh" || true
