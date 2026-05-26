"""Test benchmark manifests and scripts."""
import pathlib
import yaml


def test_nvme_fio_job_exists():
    """Test that NVMe FIO job exists."""
    job_file = pathlib.Path("aws-eks/benchmark/nvme-fio-job.yaml")
    assert job_file.exists(), "nvme-fio-job.yaml must exist"


def test_efa_libfabric_test_pod_exists():
    """Test that EFA libfabric test pod exists."""
    pod_file = pathlib.Path("aws-eks/benchmark/efa-libfabric-test-pod.yaml")
    assert pod_file.exists(), "efa-libfabric-test-pod.yaml must exist"


def test_fuse_fio_job_exists():
    """Test that FUSE FIO job exists."""
    job_file = pathlib.Path("aws-eks/benchmark/fuse-fio-job.yaml")
    assert job_file.exists(), "fuse-fio-job.yaml must exist"


def test_usrbio_fio_template_script_exists():
    """Test that USRBIO FIO template script exists."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    assert script_file.exists(), "usrbio-fio-template.sh must exist"


def test_usrbio_fio_job_template_exists():
    """Test that USRBIO FIO job template exists."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    assert job_file.exists(), "usrbio-fio-job-template.yaml must exist"


def test_checkpoint_benchmark_job_exists():
    """Test that checkpoint benchmark job exists."""
    job_file = pathlib.Path("aws-eks/benchmark/checkpoint-benchmark-job.yaml")
    assert job_file.exists(), "checkpoint-benchmark-job.yaml must exist"


def test_metadata_heavy_job_exists():
    """Test that metadata-heavy job exists."""
    job_file = pathlib.Path("aws-eks/benchmark/metadata-heavy-job.yaml")
    assert job_file.exists(), "metadata-heavy-job.yaml must exist"


def test_collect_results_script_exists():
    """Test that collect-results.sh script exists."""
    script_file = pathlib.Path("aws-eks/benchmark/collect-results.sh")
    assert script_file.exists(), "collect-results.sh must exist"


def test_benchmark_readme_exists():
    """Test that benchmark README exists."""
    readme_file = pathlib.Path("aws-eks/benchmark/README.md")
    assert readme_file.exists(), "benchmark README.md must exist"


def test_benchmark_manifests_cover_required_tests():
    """Test that benchmark manifests cover all required test types."""
    required_tests = {
        "efa": "EFA/libfabric sanity",
        "nvme": "Local NVMe fio",
        "fuse": "FUSE fio",
        "usrbio": "USRBIO fio",
        "checkpoint": "Checkpoint benchmark",
        "metadata": "Metadata-heavy operations",
    }

    benchmark_dir = pathlib.Path("aws-eks/benchmark")
    if not benchmark_dir.exists():
        return

    files = [f.name for f in benchmark_dir.iterdir()]

    for test_key, test_desc in required_tests.items():
        found = any(test_key in f for f in files)
        assert found, f"Benchmark for {test_desc} not found (looking for '{test_key}' in filenames)"
