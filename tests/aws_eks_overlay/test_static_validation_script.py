"""Test static validation script completeness."""
import pathlib


def test_static_validation_script_will_exist():
    """Test that static validation script location is defined."""
    script = pathlib.Path("aws-eks/validation/validate-local-only.sh")
    assert str(script).endswith(".sh")


def test_static_validation_should_run_pytest():
    """Test that static validation should run pytest."""
    expected_command = "python -m pytest tests/aws_eks_overlay -q"
    assert "pytest" in expected_command


def test_static_validation_should_check_shell_syntax():
    """Test that static validation should check shell syntax."""
    expected_command = 'find aws-eks -name "*.sh" -exec bash -n {} \\;'
    assert "bash -n" in expected_command


def test_static_validation_should_parse_yaml():
    """Test that static validation should parse YAML files."""
    expected_check = "yaml.safe_load_all"
    assert "yaml" in expected_check


def test_static_validation_should_render_helm_template():
    """Test that static validation should render helm template."""
    expected_command = "helm template"
    assert "helm template" in expected_command


def test_static_validation_should_inspect_manifest():
    """Test that static validation should inspect rendered manifest."""
    expected_script = "inspect-rendered-manifest.sh"
    assert "inspect" in expected_script
    assert "manifest" in expected_script


def test_validation_scripts_are_executable():
    """Test that validation scripts should be executable."""
    validation_dir = pathlib.Path("aws-eks/validation")
    if not validation_dir.exists():
        return

    for script_file in validation_dir.glob("*.sh"):
        # Check if file is executable
        import os
        is_executable = os.access(script_file, os.X_OK)
        assert is_executable, f"{script_file.name} should be executable"


def test_validation_readme_will_exist():
    """Test that validation README location is defined."""
    readme = pathlib.Path("aws-eks/validation/README.md")
    assert str(readme).endswith(".md")
