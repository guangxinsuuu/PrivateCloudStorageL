#!/usr/bin/env bash
set -euo pipefail
CLUSTER=${CLUSTER:-3fs-demo}
REGION=${REGION:-us-east-1}
for ng in storage client storage-full client-full; do
  echo "Deleting nodegroup: $ng"
  eksctl delete nodegroup \
    --cluster "$CLUSTER" \
    --region "$REGION" \
    --name "$ng" \
    --wait || true
done
echo "Remaining nodegroups:"
eksctl get nodegroup --cluster "$CLUSTER" --region "$REGION" || true
echo "Remaining nodes:"
kubectl get nodes -o wide || true
