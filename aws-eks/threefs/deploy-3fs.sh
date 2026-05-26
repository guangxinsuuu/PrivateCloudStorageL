#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
CHART_PATH="${CHART_PATH:-$REPO_ROOT/deploy/container/chart}"
echo "=== Apply namespaces ==="
kubectl apply -f "$ROOT/threefs/namespace.yaml"
echo
echo "=== Preflight checks ==="
"$ROOT/scripts/preflight-all.sh"
echo
echo "=== Chart path ==="
echo "$CHART_PATH"
if [ ! -f "$CHART_PATH/Chart.yaml" ]; then
  echo "ERROR: Chart.yaml not found at CHART_PATH=$CHART_PATH"
  echo "Available charts:"
  find "$REPO_ROOT" -name Chart.yaml -print
  exit 1
fi
echo
echo "=== Helm template dry-run ==="
helm template threefs "$CHART_PATH" \
  -n threefs \
  -f "$ROOT/threefs/values-eks-overlay.yaml" \
  > /tmp/threefs-rendered.yaml
echo "Rendered manifest saved to /tmp/threefs-rendered.yaml"
echo
echo "=== Helm upgrade/install 3FS ==="
helm upgrade --install threefs "$CHART_PATH" \
  -n threefs \
  -f "$ROOT/threefs/values-eks-overlay.yaml" \
  --create-namespace
echo
echo "=== 3FS status ==="
"$ROOT/threefs/check-3fs.sh"
