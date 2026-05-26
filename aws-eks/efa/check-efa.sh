#!/usr/bin/env bash
set -euo pipefail
CLUSTER=${CLUSTER:-3fs-demo}
REGION=${REGION:-us-east-1}
echo "=== Nodes with EFA allocatable ==="
kubectl get nodes \
  -o=custom-columns=NAME:.metadata.name,TYPE:.metadata.labels.node\\.kubernetes\\.io/instance-type,ROLE:.metadata.labels.role,EFA:.status.allocatable.vpc\\.amazonaws\\.com/efa
echo
echo "=== EFA daemonsets/pods ==="
kubectl get ds -A | grep -i efa || true
kubectl get pods -A | grep -i efa || true
echo
echo "=== Nodegroups ==="
eksctl get nodegroup --cluster "$CLUSTER" --region "$REGION"
