"""Test benchmark suite completeness for all six figures."""
import pathlib


def test_storage_path_comparison_benchmarks_exist():
    """Test that storage path comparison benchmarks exist."""
    required_files = [
        "aws-eks/benchmark/nvme-fio-job.yaml",
        "aws-eks/benchmark/efa-libfabric-test-pod.yaml",
        "aws-eks/benchmark/fuse-fio-job.yaml",
        "aws-eks/benchmark/usrbio-fio-job-template.yaml",
    ]
    for file_path in required_files:
        f = pathlib.Path(file_path)
        assert f.exists(), f"Storage path comparison requires {file_path}"


def test_fuse_vs_usrbio_benchmarks_exist():
    """Test that FUSE vs USRBIO benchmarks exist."""
    required_files = [
        "aws-eks/benchmark/fuse-fio-job.yaml",
        "aws-eks/benchmark/usrbio-fio-job-template.yaml",
    ]
    for file_path in required_files:
        f = pathlib.Path(file_path)
        assert f.exists(), f"FUSE vs USRBIO requires {file_path}"


def test_checkpoint_benchmark_exists():
    """Test that checkpoint benchmark exists."""
    f = pathlib.Path("aws-eks/benchmark/checkpoint-benchmark-job.yaml")
    assert f.exists(), "Checkpoint benchmark requires checkpoint-benchmark-job.yaml"


def test_scaling_benchmark_exists():
    """Test that scaling benchmark runner exists."""
    f = pathlib.Path("aws-eks/benchmark/run-scaling-benchmark.sh")
    assert f.exists(), "Scaling benchmark requires run-scaling-benchmark.sh"


def test_metadata_benchmark_exists():
    """Test that metadata benchmark exists."""
    f = pathlib.Path("aws-eks/benchmark/metadata-heavy-job.yaml")
    assert f.exists(), "Metadata benchmark requires metadata-heavy-job.yaml"


def test_kvcache_benchmarks_exist():
    """Test that KVCache benchmarks exist."""
    required_files = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for file_path in required_files:
        f = pathlib.Path(file_path)
        assert f.exists(), f"KVCache benchmark requires {file_path}"


def test_all_six_benchmark_categories_covered():
    """Test that all six benchmark categories are covered."""
    categories = {
        "storage_path_comparison": [
            "nvme-fio-job.yaml",
            "efa-libfabric-test-pod.yaml",
            "fuse-fio-job.yaml",
            "usrbio-fio-job-template.yaml",
        ],
        "fuse_vs_usrbio": [
            "fuse-fio-job.yaml",
            "usrbio-fio-job-template.yaml",
        ],
        "checkpoint": [
            "checkpoint-benchmark-job.yaml",
        ],
        "scaling": [
            "run-scaling-benchmark.sh",
        ],
        "metadata": [
            "metadata-heavy-job.yaml",
        ],
        "kvcache": [
            "kvcache-prepare-job.yaml",
            "kvcache-read-job.yaml",
            "kvcache-gc-job.yaml",
        ],
    }

    benchmark_dir = pathlib.Path("aws-eks/benchmark")
    for category, files in categories.items():
        for filename in files:
            file_path = benchmark_dir / filename
            assert file_path.exists(), \
                f"Category '{category}' requires {filename}"


def test_benchmark_directory_has_minimum_files():
    """Test that benchmark directory has minimum required files."""
    benchmark_dir = pathlib.Path("aws-eks/benchmark")
    if not benchmark_dir.exists():
        return

    files = list(benchmark_dir.glob("*.yaml"))
    files.extend(list(benchmark_dir.glob("*.sh")))

    # Should have at least 10 files (8 YAML jobs + 2 scripts)
    assert len(files) >= 10, \
        f"Benchmark directory should have at least 10 files, found {len(files)}"
