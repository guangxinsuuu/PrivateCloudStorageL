#!/usr/bin/env bash
set -euo pipefail
OUT="${OUT:-/tmp/threefs-rendered.yaml}"

if [ ! -f "$OUT" ]; then
  echo "ERROR: rendered manifest not found at $OUT"
  echo "Run aws-eks/validation/render-helm-template.sh first."
  exit 1
fi

echo "=== Inspect rendered manifest: $OUT ==="

check() {
  local name="$1"
  local pattern="$2"
  echo
  echo "--- $name ---"
  if grep -n "$pattern" "$OUT" | head -50; then
    echo "✓ FOUND: $name"
  else
    echo "✗ MISSING: $name"
  fi
}

check "EFA resource" "vpc.amazonaws.com/efa"
check "storage role" "role: storage"
check "client role" "role: client"
check "meta role" "role: meta"
check "NVMe mount" "/mnt/nvme0"
check "hostNetwork" "hostNetwork: true"
check "gp3 storage class" "storageClassName: gp3"
check "image placeholders" "REPLACE_WITH"
check "USRBIO reference" "hf3fs_usrbio"

echo
echo "=== Summary hints ==="
echo "If EFA/NVMe/nodeSelector values are missing, the Helm chart may not consume values-eks-overlay.yaml."
echo "Patch deploy/container/chart/templates or update values-eks-overlay.yaml to match real chart fields."
