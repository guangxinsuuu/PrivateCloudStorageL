"""Test 3FS values overlay configuration."""
import pathlib
import yaml


def test_threefs_namespace_exists():
    """Test that 3FS namespace file exists."""
    ns_file = pathlib.Path("aws-eks/threefs/namespace.yaml")
    assert ns_file.exists(), "namespace.yaml must exist"


def test_threefs_namespace_defines_fdb_and_threefs():
    """Test that namespace file defines both fdb and threefs namespaces."""
    ns_file = pathlib.Path("aws-eks/threefs/namespace.yaml")
    if not ns_file.exists():
        return

    with open(ns_file) as f:
        content = f.read()
        docs = list(yaml.safe_load_all(content))

    namespaces = [doc["metadata"]["name"] for doc in docs if doc.get("kind") == "Namespace"]

    assert "fdb" in namespaces, "fdb namespace must be defined"
    assert "threefs" in namespaces, "threefs namespace must be defined"


def test_threefs_values_exists():
    """Test that 3FS values overlay exists."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    assert values_file.exists(), "values-eks-overlay.yaml must exist"


def test_threefs_values_has_node_selectors():
    """Test that 3FS values overlay has correct node selectors."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_file.exists():
        return

    with open(values_file) as f:
        values = yaml.safe_load(f)

    # Check mgmtd
    if "mgmtd" in values:
        assert values["mgmtd"].get("nodeSelector", {}).get("role") == "meta", \
            "mgmtd must use role=meta"

    # Check meta
    if "meta" in values:
        assert values["meta"].get("nodeSelector", {}).get("role") == "meta", \
            "meta must use role=meta"

    # Check storage
    if "storage" in values:
        assert values["storage"].get("nodeSelector", {}).get("role") == "storage", \
            "storage must use role=storage"

    # Check client or fuse
    for component in ["client", "fuse"]:
        if component in values:
            assert values[component].get("nodeSelector", {}).get("role") == "client", \
                f"{component} must use role=client"


def test_threefs_values_storage_has_nvme_and_efa():
    """Test that storage config has NVMe and EFA."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_file.exists():
        return

    with open(values_file) as f:
        values = yaml.safe_load(f)

    if "storage" not in values:
        return

    storage = values["storage"]

    # Check hostNetwork
    assert storage.get("hostNetwork") == True, "storage must use hostNetwork"

    # Check dataDirs or similar indicates /mnt/nvme0
    content_str = str(values)
    assert "/mnt/nvme" in content_str, "storage must reference /mnt/nvme data dirs"

    # Check EFA resource request
    if "resources" in storage:
        res = storage["resources"]
        if "requests" in res:
            assert "vpc.amazonaws.com/efa" in res["requests"], \
                "storage must request EFA"


def test_threefs_values_has_fdb_namespace():
    """Test that 3FS values references fdb namespace."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_file.exists():
        return

    content = values_file.read_text()
    assert "fdb" in content, "3FS values must reference fdb namespace"


def test_threefs_readme_exists():
    """Test that 3FS README exists."""
    readme_file = pathlib.Path("aws-eks/threefs/README.md")
    assert readme_file.exists(), "3FS README.md must exist"
