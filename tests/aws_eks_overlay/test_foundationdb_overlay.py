"""Test FoundationDB overlay configuration."""
import pathlib
import yaml


def test_foundationdb_values_exists():
    """Test that FoundationDB values overlay exists."""
    values_file = pathlib.Path("aws-eks/foundationdb/values-fdb-eks.yaml")
    assert values_file.exists(), "values-fdb-eks.yaml must exist"


def test_foundationdb_values_valid():
    """Test that FoundationDB values overlay is valid."""
    values_file = pathlib.Path("aws-eks/foundationdb/values-fdb-eks.yaml")
    if not values_file.exists():
        return

    with open(values_file) as f:
        values = yaml.safe_load(f)

    fdb = values.get("foundationdb", values)

    # Check namespace
    assert fdb.get("namespace") == "fdb", "FDB must use fdb namespace"

    # Check storageClassName
    assert fdb.get("storageClassName") == "gp3", \
        "FDB must use gp3 storageClassName, not Alibaba storage"

    # Check nodeSelector
    node_selector = fdb.get("nodeSelector", {})
    assert node_selector.get("role") == "meta", "FDB must run on role=meta nodes"

    # Check volumeSize is set
    volume_size = fdb.get("volumeSize")
    assert volume_size is not None, "FDB volumeSize must be explicitly set"


def test_foundationdb_check_script_exists():
    """Test that FoundationDB check script exists."""
    script_file = pathlib.Path("aws-eks/foundationdb/check-fdb.sh")
    assert script_file.exists(), "check-fdb.sh must exist"


def test_foundationdb_readme_exists():
    """Test that FoundationDB README exists."""
    readme_file = pathlib.Path("aws-eks/foundationdb/README.md")
    assert readme_file.exists(), "FoundationDB README.md must exist"
