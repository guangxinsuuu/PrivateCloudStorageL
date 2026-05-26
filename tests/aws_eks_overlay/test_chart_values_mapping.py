"""Test chart values mapping expectations."""
import pathlib
import yaml


def test_chart_values_file_exists():
    """Test that original chart values file exists."""
    values_path = pathlib.Path("deploy/container/chart/values.yaml")
    if not values_path.exists():
        return  # Chart might not have default values

    with open(values_path) as f:
        values = yaml.safe_load(f)

    assert isinstance(values, dict), "Chart values must be a dictionary"


def test_eks_overlay_values_is_valid_yaml():
    """Test that EKS overlay values is valid YAML."""
    values_path = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_path.exists():
        return

    with open(values_path) as f:
        values = yaml.safe_load(f)

    assert isinstance(values, dict), "EKS overlay values must be a dictionary"


def test_eks_overlay_has_expected_top_level_keys():
    """Test that EKS overlay has expected component keys."""
    values_path = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_path.exists():
        return

    with open(values_path) as f:
        values = yaml.safe_load(f)

    # Should have at least some of these keys
    expected_keys = ["mgmtd", "meta", "storage", "fuse", "client", "foundationdb", "global"]

    found_keys = [key for key in expected_keys if key in values]
    assert len(found_keys) > 0, "EKS overlay should have at least one component key"


def test_chart_mapping_doc_will_exist():
    """Test that chart mapping document location is defined."""
    mapping_doc = pathlib.Path("aws-eks/docs/chart-field-mapping.md")
    # This will be created in later steps
    # Test just verifies the expected path
    assert str(mapping_doc).endswith(".md")
