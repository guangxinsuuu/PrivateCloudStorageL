#!/usr/bin/env bash
set -euo pipefail

# Scaling Benchmark Runner
# Automates repeated benchmark runs for different client parallelism levels
# Supports Figure 4: Client Scaling Efficiency

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE=${NAMESPACE:-threefs}
MODE=${MODE:-fuse}
CLIENT_PODS=${CLIENT_PODS:-"1 2 4"}
OUT_DIR=${OUT_DIR:-"scaling-results-$(date +%Y%m%d-%H%M%S)"}

mkdir -p "$OUT_DIR"

echo "benchmark=scaling"
echo "mode=${MODE}"
echo "client_pods=${CLIENT_PODS}"
echo "out_dir=${OUT_DIR}"

if [ "$MODE" != "fuse" ] && [ "$MODE" != "usrbio" ]; then
  echo "ERROR: MODE must be fuse or usrbio"
  exit 1
fi

for n in $CLIENT_PODS; do
  echo "=== Scaling run: mode=$MODE pods=$n ==="

  i=0
  while [ "$i" -lt "$n" ]; do
    job_name="scaling-${MODE}-${n}-${i}"

    if [ "$MODE" = "fuse" ]; then
      base="$ROOT/fuse-fio-job.yaml"
    else
      base="$ROOT/usrbio-fio-job-template.yaml"
    fi

    tmp="/tmp/${job_name}.yaml"
    cp "$base" "$tmp"

    # Replace job name conservatively
    sed -i.bak "s/name: threefs-fuse-fio/name: ${job_name}/g" "$tmp" || true
    sed -i.bak "s/name: threefs-usrbio-fio/name: ${job_name}/g" "$tmp" || true
    sed -i.bak "s/name: fuse-fio/name: ${job_name}/g" "$tmp" || true
    sed -i.bak "s/name: usrbio-fio/name: ${job_name}/g" "$tmp" || true

    # Delete existing job if any
    kubectl delete job -n "$NAMESPACE" "$job_name" --ignore-not-found || true

    # Apply new job
    kubectl apply -f "$tmp"

    i=$((i+1))
  done

  echo "Waiting for jobs..."
  i=0
  while [ "$i" -lt "$n" ]; do
    job_name="scaling-${MODE}-${n}-${i}"
    kubectl wait -n "$NAMESPACE" --for=condition=complete --timeout=900s "job/${job_name}" || true
    kubectl logs -n "$NAMESPACE" "job/${job_name}" > "${OUT_DIR}/${job_name}.log" 2>&1 || true
    i=$((i+1))
  done

  echo "completed_pods=${n}" >> "${OUT_DIR}/summary.txt"
done

echo "status=complete"
echo "results=${OUT_DIR}"
