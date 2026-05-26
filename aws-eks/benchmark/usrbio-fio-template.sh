#!/usr/bin/env bash
set -euo pipefail
ENGINE=${ENGINE:-/opt/3fs/lib/hf3fs_usrbio.so}
DIR=${DIR:-/mnt/3fs}
RUNTIME=${RUNTIME:-180}
BS=${BS:-1M}
IODEPTH=${IODEPTH:-64}
NUMJOBS=${NUMJOBS:-8}
SIZE=${SIZE:-20G}
echo "=== USRBIO fio config ==="
echo "ENGINE=$ENGINE"
echo "DIR=$DIR"
echo "RUNTIME=$RUNTIME"
echo "BS=$BS"
echo "IODEPTH=$IODEPTH"
echo "NUMJOBS=$NUMJOBS"
echo "SIZE=$SIZE"
if [ ! -f "$ENGINE" ]; then
  echo "ERROR: USRBIO fio engine not found at $ENGINE"
  echo "Searching for hf3fs_usrbio.so..."
  find / -name 'hf3fs_usrbio.so' 2>/dev/null | head -20 || true
  exit 1
fi
fio \
  -ioengine=external:${ENGINE} \
  -directory="${DIR}" \
  -name=usrbio-seq-read \
  -size="${SIZE}" \
  -rw=read \
  -bs="${BS}" \
  -numjobs="${NUMJOBS}" \
  -iodepth="${IODEPTH}" \
  -group_reporting \
  -time_based=1 \
  -runtime="${RUNTIME}" \
  -direct=0 \
  --output-format=json \
  --output=usrbio-seq-read.json
fio \
  -ioengine=external:${ENGINE} \
  -directory="${DIR}" \
  -name=usrbio-seq-write \
  -size="${SIZE}" \
  -rw=write \
  -bs="${BS}" \
  -numjobs="${NUMJOBS}" \
  -iodepth="${IODEPTH}" \
  -group_reporting \
  -time_based=1 \
  -runtime="${RUNTIME}" \
  -direct=0 \
  --output-format=json \
  --output=usrbio-seq-write.json
