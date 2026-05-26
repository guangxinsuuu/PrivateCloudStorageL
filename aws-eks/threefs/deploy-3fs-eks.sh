#!/usr/bin/env bash
set -euo pipefail

# Deploy 3FS on EKS with automatic post-processing
# This script handles all Alibaba → AWS field replacements

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
AWS_EKS_DIR="${PROJECT_ROOT}/aws-eks"

echo "=== 3FS EKS Deployment Script ==="
echo "Project root: ${PROJECT_ROOT}"

# Check required environment variables
if [ -z "${ECR_REGISTRY:-}" ]; then
  echo "ERROR: ECR_REGISTRY environment variable not set"
  echo "Example: export ECR_REGISTRY=123456789012.dkr.ecr.us-east-1.amazonaws.com"
  exit 1
fi

if [ -z "${IMAGE_TAG:-}" ]; then
  echo "ERROR: IMAGE_TAG environment variable not set"
  echo "Example: export IMAGE_TAG=v0.1.5-abc123"
  exit 1
fi

echo "ECR Registry: ${ECR_REGISTRY}"
echo "Image Tag: ${IMAGE_TAG}"

# Check prerequisites
echo ""
echo "=== Checking Prerequisites ==="

if ! command -v helm &>/dev/null; then
  echo "ERROR: helm not found. Install from https://helm.sh"
  exit 1
fi

if ! command -v kubectl &>/dev/null; then
  echo "ERROR: kubectl not found"
  exit 1
fi

if ! command -v yq &>/dev/null; then
  echo "WARNING: yq not found. Installing via pip..."
  pip3 install yq || {
    echo "ERROR: Failed to install yq. Please install manually: pip3 install yq"
    exit 1
  }
fi

echo "✓ All prerequisites met"

# Check kubectl connection
echo ""
echo "=== Checking Kubernetes Connection ==="
if ! kubectl cluster-info &>/dev/null; then
  echo "ERROR: Cannot connect to Kubernetes cluster"
  echo "Run: aws eks update-kubeconfig --name 3fs-demo --region us-east-1"
  exit 1
fi

CURRENT_CONTEXT=$(kubectl config current-context)
echo "✓ Connected to: ${CURRENT_CONTEXT}"

# Confirm deployment
echo ""
echo "=== Deployment Confirmation ==="
echo "This will deploy 3FS with the following configuration:"
echo "  - ECR Registry: ${ECR_REGISTRY}"
echo "  - Image Tag: ${IMAGE_TAG}"
echo "  - Cluster: ${CURRENT_CONTEXT}"
read -p "Continue? (yes/no): " CONFIRM

if [ "${CONFIRM}" != "yes" ]; then
  echo "Deployment cancelled"
  exit 0
fi

# Create namespace
echo ""
echo "=== Creating Namespace ==="
kubectl create namespace threefs --dry-run=client -o yaml | kubectl apply -f -
echo "✓ Namespace 'threefs' ready"

# Render Helm template
echo ""
echo "=== Rendering Helm Template ==="
CHART_PATH="${PROJECT_ROOT}/deploy/container/chart"
VALUES_FILE="${AWS_EKS_DIR}/threefs/values-eks-overlay.yaml"
RENDERED_FILE="/tmp/threefs-rendered-original.yaml"
PROCESSED_FILE="/tmp/threefs-rendered-processed.yaml"

if [ ! -d "${CHART_PATH}" ]; then
  echo "ERROR: Chart not found at ${CHART_PATH}"
  exit 1
fi

if [ ! -f "${VALUES_FILE}" ]; then
  echo "ERROR: Values file not found at ${VALUES_FILE}"
  exit 1
fi

helm template threefs "${CHART_PATH}" \
  --namespace threefs \
  --values "${VALUES_FILE}" \
  > "${RENDERED_FILE}"

echo "✓ Rendered to ${RENDERED_FILE}"

# Post-process manifest
echo ""
echo "=== Post-Processing Manifest ==="

cp "${RENDERED_FILE}" "${PROCESSED_FILE}"

# 1. Replace RDMA resource: Alibaba provider → vpc.amazonaws.com/efa
echo "  - Replacing RDMA resource (Alibaba → vpc.amazonaws.com/efa)"
sed -i.bak 's|aliyun/erdma|vpc.amazonaws.com/efa|g' "${PROCESSED_FILE}"

# 2. Replace storage class: alibabacloud-disk-ephemeral → gp3
echo "  - Replacing storage class (alibabacloud-disk-ephemeral → gp3)"
sed -i.bak 's|alibabacloud-disk-ephemeral|gp3|g' "${PROCESSED_FILE}"

# 3. Replace image registry and tag
echo "  - Replacing image registry and tag"
sed -i.bak "s|registry-vpc.cn-beijing.aliyuncs.com/huweiwen-test/3fs-|${ECR_REGISTRY}/3fs-|g" "${PROCESSED_FILE}"
sed -i.bak "s|:dev|:${IMAGE_TAG}|g" "${PROCESSED_FILE}"

# 4. Add nodeSelector, tolerations, hostNetwork using yq
echo "  - Adding nodeSelector for storage pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   .spec.template.spec.nodeSelector.role) = "storage"
' "${PROCESSED_FILE}"

echo "  - Adding tolerations for storage pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   .spec.template.spec.tolerations) = [
     {"key": "role", "operator": "Equal", "value": "storage", "effect": "NoSchedule"}
   ]
' "${PROCESSED_FILE}"

echo "  - Adding hostNetwork for storage pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   .spec.template.spec.hostNetwork) = true |
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   .spec.template.spec.dnsPolicy) = "ClusterFirstWithHostNet"
' "${PROCESSED_FILE}"

echo "  - Adding nodeSelector for meta pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "meta-threefs") |
   .spec.template.spec.nodeSelector.role) = "meta"
' "${PROCESSED_FILE}"

echo "  - Adding hostNetwork for meta pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "meta-threefs") |
   .spec.template.spec.hostNetwork) = true |
  (select(.kind == "StatefulSet" and .metadata.name == "meta-threefs") |
   .spec.template.spec.dnsPolicy) = "ClusterFirstWithHostNet"
' "${PROCESSED_FILE}"

echo "  - Adding nodeSelector for mgmtd pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "mgmtd-threefs") |
   .spec.template.spec.nodeSelector.role) = "meta"
' "${PROCESSED_FILE}"

echo "  - Adding hostNetwork for mgmtd pods"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "mgmtd-threefs") |
   .spec.template.spec.hostNetwork) = true |
  (select(.kind == "StatefulSet" and .metadata.name == "mgmtd-threefs") |
   .spec.template.spec.dnsPolicy) = "ClusterFirstWithHostNet"
' "${PROCESSED_FILE}"

echo "  - Adding nodeSelector for fuse pods"
yq eval -i '
  (select(.kind == "Pod" and .metadata.name == "fuse-threefs") |
   .spec.nodeSelector.role) = "client"
' "${PROCESSED_FILE}"

echo "  - Adding hostNetwork for fuse pods"
yq eval -i '
  (select(.kind == "Pod" and .metadata.name == "fuse-threefs") |
   .spec.hostNetwork) = true |
  (select(.kind == "Pod" and .metadata.name == "fuse-threefs") |
   .spec.dnsPolicy) = "ClusterFirstWithHostNet"
' "${PROCESSED_FILE}"

# 5. Convert storage volumeClaimTemplates to hostPath (for Instance Store NVMe)
echo "  - Converting storage PVCs to hostPath (for Instance Store NVMe)"
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   del(.spec.volumeClaimTemplates))
' "${PROCESSED_FILE}"

# Add hostPath volumes for storage
yq eval -i '
  (select(.kind == "StatefulSet" and .metadata.name == "storage-threefs") |
   .spec.template.spec.volumes) += [
     {"name": "data-0", "hostPath": {"path": "/mnt/data0", "type": "DirectoryOrCreate"}},
     {"name": "data-1", "hostPath": {"path": "/mnt/data1", "type": "DirectoryOrCreate"}},
     {"name": "data-2", "hostPath": {"path": "/mnt/data2", "type": "DirectoryOrCreate"}},
     {"name": "data-3", "hostPath": {"path": "/mnt/data3", "type": "DirectoryOrCreate"}},
     {"name": "data-4", "hostPath": {"path": "/mnt/data4", "type": "DirectoryOrCreate"}},
     {"name": "data-5", "hostPath": {"path": "/mnt/data5", "type": "DirectoryOrCreate"}},
     {"name": "data-6", "hostPath": {"path": "/mnt/data6", "type": "DirectoryOrCreate"}},
     {"name": "data-7", "hostPath": {"path": "/mnt/data7", "type": "DirectoryOrCreate"}}
   ]
' "${PROCESSED_FILE}"

echo "✓ Post-processing complete"

# Validation
echo ""
echo "=== Validating Processed Manifest ==="

# Check for remaining Alibaba references
if grep -q "aliyun" "${PROCESSED_FILE}"; then
  echo "WARNING: Found remaining 'aliyun' references:"
  grep -n "aliyun" "${PROCESSED_FILE}" || true
fi

if grep -q "alibabacloud" "${PROCESSED_FILE}"; then
  echo "WARNING: Found remaining 'alibabacloud' references:"
  grep -n "alibabacloud" "${PROCESSED_FILE}" || true
fi

if grep -q "cn-beijing" "${PROCESSED_FILE}"; then
  echo "WARNING: Found remaining 'cn-beijing' references:"
  grep -n "cn-beijing" "${PROCESSED_FILE}" || true
fi

# Check for AWS references
echo "Checking for AWS-specific fields:"
echo -n "  - vpc.amazonaws.com/efa: "
if grep -q "vpc.amazonaws.com/efa" "${PROCESSED_FILE}"; then
  echo "✓ Found"
else
  echo "✗ Not found (CRITICAL)"
fi

echo -n "  - nodeSelector role=storage: "
if grep -A2 "nodeSelector" "${PROCESSED_FILE}" | grep -q "role: storage"; then
  echo "✓ Found"
else
  echo "✗ Not found (WARNING)"
fi

echo -n "  - hostNetwork: "
if grep -q "hostNetwork: true" "${PROCESSED_FILE}"; then
  echo "✓ Found"
else
  echo "✗ Not found (WARNING)"
fi

echo -n "  - ECR registry: "
if grep -q "${ECR_REGISTRY}" "${PROCESSED_FILE}"; then
  echo "✓ Found"
else
  echo "✗ Not found (CRITICAL)"
fi

# Save for inspection
cp "${PROCESSED_FILE}" "${AWS_EKS_DIR}/threefs/threefs-rendered-final.yaml"
echo ""
echo "✓ Final manifest saved to: ${AWS_EKS_DIR}/threefs/threefs-rendered-final.yaml"

# Apply to cluster
echo ""
echo "=== Applying to Cluster ==="
read -p "Apply manifest to cluster now? (yes/no): " APPLY_CONFIRM

if [ "${APPLY_CONFIRM}" != "yes" ]; then
  echo "Manifest ready but not applied. To apply manually:"
  echo "  kubectl apply -f ${AWS_EKS_DIR}/threefs/threefs-rendered-final.yaml"
  exit 0
fi

kubectl apply -f "${PROCESSED_FILE}"

echo ""
echo "✓ 3FS deployment submitted"

# Wait for pods
echo ""
echo "=== Waiting for Pods ==="
echo "Waiting for mgmtd pods..."
kubectl rollout status statefulset/mgmtd-threefs -n threefs --timeout=300s || true

echo "Waiting for meta pods..."
kubectl rollout status statefulset/meta-threefs -n threefs --timeout=300s || true

echo "Waiting for storage pods..."
kubectl rollout status statefulset/storage-threefs -n threefs --timeout=300s || true

# Check status
echo ""
echo "=== Current Status ==="
kubectl get pods -n threefs

echo ""
echo "=== Deployment Complete ==="
echo "To check logs:"
echo "  kubectl logs -n threefs -l app.kubernetes.io/component=mgmtd"
echo "  kubectl logs -n threefs -l app.kubernetes.io/component=meta"
echo "  kubectl logs -n threefs -l app.kubernetes.io/component=storage"
echo ""
echo "To verify FUSE mount (if fuse pod deployed):"
echo "  kubectl exec -n threefs fuse-threefs -- df -h | grep 3fs"
