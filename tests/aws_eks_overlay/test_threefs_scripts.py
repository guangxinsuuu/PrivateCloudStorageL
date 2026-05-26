"""Test 3FS deployment and management scripts."""
import pathlib


def test_deploy_3fs_script_exists():
    """Test that deploy-3fs.sh script exists."""
    script_file = pathlib.Path("aws-eks/threefs/deploy-3fs.sh")
    assert script_file.exists(), "deploy-3fs.sh must exist"


def test_check_3fs_script_exists():
    """Test that check-3fs.sh script exists."""
    script_file = pathlib.Path("aws-eks/threefs/check-3fs.sh")
    assert script_file.exists(), "check-3fs.sh must exist"


def test_delete_3fs_workloads_script_exists():
    """Test that delete-3fs-workloads.sh script exists."""
    script_file = pathlib.Path("aws-eks/threefs/delete-3fs-workloads.sh")
    assert script_file.exists(), "delete-3fs-workloads.sh must exist"


def test_deploy_3fs_has_set_euo_pipefail():
    """Test that deploy-3fs.sh has set -euo pipefail."""
    script_file = pathlib.Path("aws-eks/threefs/deploy-3fs.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()
    assert "#!/usr/bin/env bash" in content or "#!/bin/bash" in content
    assert "set -euo pipefail" in content


def test_check_3fs_has_set_euo_pipefail():
    """Test that check-3fs.sh has set -euo pipefail."""
    script_file = pathlib.Path("aws-eks/threefs/check-3fs.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()
    assert "#!/usr/bin/env bash" in content or "#!/bin/bash" in content
    assert "set -euo pipefail" in content


def test_delete_3fs_has_set_euo_pipefail():
    """Test that delete-3fs-workloads.sh has set -euo pipefail."""
    script_file = pathlib.Path("aws-eks/threefs/delete-3fs-workloads.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()
    assert "#!/usr/bin/env bash" in content or "#!/bin/bash" in content
    assert "set -euo pipefail" in content
