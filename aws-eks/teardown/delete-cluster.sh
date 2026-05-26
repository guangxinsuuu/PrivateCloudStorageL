#!/usr/bin/env bash
set -euo pipefail
CLUSTER=${CLUSTER:-3fs-demo}
REGION=${REGION:-us-east-1}
echo "WARNING: This deletes the entire EKS cluster: $CLUSTER in $REGION"
echo "Sleeping 10 seconds. Press Ctrl+C to cancel."
sleep 10
eksctl delete cluster \
  --region "$REGION" \
  --name "$CLUSTER"
