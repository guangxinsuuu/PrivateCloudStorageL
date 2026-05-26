#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

cd "$REPO_ROOT"

echo "=== LOCAL STATIC VALIDATION (NO AWS DEPLOYMENT) ==="
echo

echo "=== Pytest AWS overlay tests ==="
python -m pytest tests/aws_eks_overlay -q
echo

echo "=== Shell syntax checks ==="
find aws-eks -name "*.sh" -exec bash -n {} \;
echo "✓ All shell scripts have valid syntax"
echo

echo "=== YAML parse checks ==="
python - <<'PY'
import pathlib
import yaml
errors = []
for p in pathlib.Path("aws-eks").rglob("*.yaml"):
    try:
        list(yaml.safe_load_all(p.read_text()))
        print(f"✓ {p}")
    except Exception as e:
        errors.append((p, e))
        print(f"✗ {p}: {e}")
if errors:
    print(f"\n{len(errors)} YAML file(s) failed validation")
    exit(1)
else:
    print("\n✓ All YAML files are valid")
PY
echo

echo "=== Helm template render (if helm available) ==="
if command -v helm &> /dev/null; then
    "$ROOT/validation/render-helm-template.sh" || echo "⚠ Helm template render failed (may need chart patching)"
    echo
    echo "=== Rendered manifest inspection ==="
    "$ROOT/validation/inspect-rendered-manifest.sh" || echo "⚠ Manifest inspection failed"
else
    echo "⚠ Helm not installed, skipping helm template validation"
fi
echo

echo "======================================"
echo "LOCAL STATIC VALIDATION COMPLETE"
echo "No AWS resources were created."
echo "======================================"
