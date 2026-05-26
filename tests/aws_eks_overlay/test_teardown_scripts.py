"""Test teardown scripts."""
import pathlib


def test_delete_efa_nodegroups_script_exists():
    """Test that delete-efa-nodegroups.sh exists."""
    script_file = pathlib.Path("aws-eks/teardown/delete-efa-nodegroups.sh")
    assert script_file.exists(), "delete-efa-nodegroups.sh must exist"


def test_delete_cluster_script_exists():
    """Test that delete-cluster.sh exists."""
    script_file = pathlib.Path("aws-eks/teardown/delete-cluster.sh")
    assert script_file.exists(), "delete-cluster.sh must exist"


def test_teardown_readme_exists():
    """Test that teardown README exists."""
    readme_file = pathlib.Path("aws-eks/teardown/README.md")
    assert readme_file.exists(), "teardown README.md must exist"


def test_delete_efa_nodegroups_deletes_correct_nodegroups():
    """Test that delete-efa-nodegroups.sh targets correct nodegroups."""
    script_file = pathlib.Path("aws-eks/teardown/delete-efa-nodegroups.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Must delete expensive nodegroups
    assert "storage" in content, "Must delete storage nodegroup"
    assert "client" in content, "Must delete client nodegroup"
    assert "storage-full" in content, "Must delete storage-full nodegroup"
    assert "client-full" in content, "Must delete client-full nodegroup"


def test_delete_efa_nodegroups_does_not_delete_meta():
    """Test that delete-efa-nodegroups.sh does not delete meta by default."""
    script_file = pathlib.Path("aws-eks/teardown/delete-efa-nodegroups.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Should not explicitly delete meta in the default flow
    # Meta may appear in comments but not in deletion commands
    lines = content.split("\n")
    for line in lines:
        if "eksctl delete nodegroup" in line and not line.strip().startswith("#"):
            # This is an actual deletion command, not a comment
            assert "meta" not in line, \
                "delete-efa-nodegroups.sh must not delete meta nodegroup by default"


def test_delete_cluster_is_separate_script():
    """Test that delete-cluster.sh is a separate script."""
    delete_nodegroups = pathlib.Path("aws-eks/teardown/delete-efa-nodegroups.sh")
    delete_cluster = pathlib.Path("aws-eks/teardown/delete-cluster.sh")

    assert delete_nodegroups.exists() and delete_cluster.exists(), \
        "delete-efa-nodegroups.sh and delete-cluster.sh must be separate scripts"


def test_teardown_scripts_have_set_euo_pipefail():
    """Test that teardown scripts have set -euo pipefail."""
    script_files = [
        pathlib.Path("aws-eks/teardown/delete-efa-nodegroups.sh"),
        pathlib.Path("aws-eks/teardown/delete-cluster.sh"),
    ]

    for script_file in script_files:
        if not script_file.exists():
            continue

        content = script_file.read_text()
        assert "#!/usr/bin/env bash" in content or "#!/bin/bash" in content
        assert "set -euo pipefail" in content
