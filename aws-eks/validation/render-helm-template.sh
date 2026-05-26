#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
CHART_PATH="${CHART_PATH:-$REPO_ROOT/deploy/container/chart}"
VALUES_FILE="${VALUES_FILE:-$ROOT/threefs/values-eks-overlay.yaml}"
OUT="${OUT:-/tmp/threefs-rendered.yaml}"

echo "=== Local-only Helm template validation ==="
echo "CHART_PATH=$CHART_PATH"
echo "VALUES_FILE=$VALUES_FILE"
echo "OUT=$OUT"

if [ ! -f "$CHART_PATH/Chart.yaml" ]; then
  echo "ERROR: Chart.yaml not found at $CHART_PATH"
  echo "Available Chart.yaml files:"
  find "$REPO_ROOT" -name Chart.yaml -print
  exit 1
fi

if [ ! -f "$VALUES_FILE" ]; then
  echo "ERROR: values file not found at $VALUES_FILE"
  exit 1
fi

echo
echo "Rendering Helm template (local-only, no deployment)..."
helm template threefs "$CHART_PATH" \
  -n threefs \
  -f "$VALUES_FILE" \
  > "$OUT"

echo "Rendered manifest written to $OUT"
wc -l "$OUT"
