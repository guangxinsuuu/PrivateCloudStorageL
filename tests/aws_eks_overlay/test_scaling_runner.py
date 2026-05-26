"""Test scaling runner script."""
import pathlib


def test_scaling_runner_exists():
    """Test that run-scaling-benchmark.sh exists."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    assert script.exists(), "run-scaling-benchmark.sh must exist"


def test_scaling_runner_has_shebang():
    """Test that scaling runner has shebang."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    lines = content.split("\n")
    assert lines[0].startswith("#!"), "scaling runner must have shebang"


def test_scaling_runner_has_set_pipefail():
    """Test that scaling runner has set -euo pipefail."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "set -euo pipefail" in content, \
        "scaling runner must have set -euo pipefail"


def test_scaling_runner_supports_fuse_mode():
    """Test that scaling runner supports fuse mode."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "fuse" in content.lower(), "scaling runner must support fuse mode"


def test_scaling_runner_supports_usrbio_mode():
    """Test that scaling runner supports usrbio mode."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "usrbio" in content.lower(), "scaling runner must support usrbio mode"


def test_scaling_runner_has_client_pods_config():
    """Test that scaling runner has CLIENT_PODS configuration."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "CLIENT_PODS" in content, \
        "scaling runner must have CLIENT_PODS config"


def test_scaling_runner_references_fuse_job():
    """Test that scaling runner references fuse-fio-job.yaml."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "fuse-fio-job" in content, \
        "scaling runner must reference fuse-fio-job.yaml"


def test_scaling_runner_references_usrbio_job():
    """Test that scaling runner references usrbio-fio-job-template.yaml."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    assert "usrbio-fio-job" in content, \
        "scaling runner must reference usrbio-fio-job-template.yaml"


def test_scaling_runner_no_nodegroup_creation():
    """Test that scaling runner does not create nodegroups."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    content = script.read_text()
    # Should not contain eksctl create nodegroup
    assert "eksctl create nodegroup" not in content, \
        "scaling runner must not create nodegroups"
    assert "eksctl create" not in content, \
        "scaling runner must not create any eksctl resources"


def test_scaling_runner_is_executable():
    """Test that scaling runner is executable."""
    script = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    if not script.exists():
        return
    import os
    is_executable = os.access(script, os.X_OK)
    assert is_executable, "scaling runner must be executable"
