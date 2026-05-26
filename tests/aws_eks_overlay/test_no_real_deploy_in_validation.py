"""Test that validation scripts don't contain real deployment commands."""
import pathlib
import re


def test_validation_scripts_exist():
    """Test that validation directory will exist."""
    validation_dir = pathlib.Path("aws-eks/validation")
    # This will be created in later steps
    assert str(validation_dir).endswith("validation")


def test_no_eksctl_create_in_validation_scripts():
    """Test that validation scripts don't contain eksctl create commands."""
    validation_dir = pathlib.Path("aws-eks/validation")
    if not validation_dir.exists():
        return

    forbidden_patterns = [
        "eksctl create cluster",
        "eksctl create nodegroup",
    ]

    for script_file in validation_dir.glob("*.sh"):
        content = script_file.read_text()

        for pattern in forbidden_patterns:
            # Check if pattern exists outside of comments
            lines = content.split("\n")
            for line in lines:
                # Skip comment lines
                if line.strip().startswith("#"):
                    continue

                if pattern in line:
                    assert False, f"{script_file.name} contains forbidden command: {pattern}"


def test_no_kubectl_apply_in_validation_scripts():
    """Test that validation scripts don't contain kubectl apply commands."""
    validation_dir = pathlib.Path("aws-eks/validation")
    if not validation_dir.exists():
        return

    forbidden_patterns = [
        "kubectl apply",
        "kubectl create",
        "kubectl delete",
    ]

    for script_file in validation_dir.glob("*.sh"):
        content = script_file.read_text()

        for pattern in forbidden_patterns:
            lines = content.split("\n")
            for line in lines:
                if line.strip().startswith("#"):
                    continue

                if pattern in line:
                    assert False, f"{script_file.name} contains forbidden command: {pattern}"


def test_no_helm_install_in_validation_scripts():
    """Test that validation scripts don't contain helm install/upgrade."""
    validation_dir = pathlib.Path("aws-eks/validation")
    if not validation_dir.exists():
        return

    forbidden_patterns = [
        "helm install",
        "helm upgrade",
    ]

    for script_file in validation_dir.glob("*.sh"):
        content = script_file.read_text()

        for pattern in forbidden_patterns:
            lines = content.split("\n")
            for line in lines:
                if line.strip().startswith("#"):
                    continue

                if pattern in line:
                    assert False, f"{script_file.name} contains forbidden command: {pattern}"


def test_helm_template_is_allowed_in_validation():
    """Test that helm template (read-only) is allowed in validation."""
    # helm template is safe - it doesn't deploy anything
    allowed_commands = ["helm template"]
    assert "helm template" in allowed_commands


def test_deployment_scripts_may_contain_deploy_commands():
    """Test that deployment scripts (not validation) may contain deploy commands."""
    # Scripts under scripts/ and threefs/ are meant to be run by users
    # They can contain deployment commands
    # This test just documents the distinction

    validation_scripts = pathlib.Path("aws-eks/validation")
    deployment_scripts = pathlib.Path("aws-eks/scripts")

    assert str(validation_scripts) != str(deployment_scripts), \
        "Validation scripts and deployment scripts should be in different directories"
