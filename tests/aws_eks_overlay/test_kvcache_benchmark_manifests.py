"""Test KVCache benchmark manifests."""
import pathlib
import yaml


def test_kvcache_prepare_exists():
    """Test that kvcache-prepare-job.yaml exists."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-prepare-job.yaml")
    assert job.exists(), "kvcache-prepare-job.yaml must exist"


def test_kvcache_read_exists():
    """Test that kvcache-read-job.yaml exists."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-read-job.yaml")
    assert job.exists(), "kvcache-read-job.yaml must exist"


def test_kvcache_gc_exists():
    """Test that kvcache-gc-job.yaml exists."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-gc-job.yaml")
    assert job.exists(), "kvcache-gc-job.yaml must exist"


def test_kvcache_jobs_are_valid_yaml():
    """Test that all kvcache jobs are valid YAML."""
    jobs = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for job_path in jobs:
        job = pathlib.Path(job_path)
        if not job.exists():
            continue
        content = job.read_text()
        docs = list(yaml.safe_load_all(content))
        assert len(docs) > 0, f"{job_path} must contain valid YAML"


def test_kvcache_jobs_are_job_kind():
    """Test that all kvcache jobs are Kubernetes Job kind."""
    jobs = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for job_path in jobs:
        job = pathlib.Path(job_path)
        if not job.exists():
            continue
        content = job.read_text()
        docs = list(yaml.safe_load_all(content))
        for doc in docs:
            if doc and "kind" in doc:
                assert doc["kind"] == "Job", f"{job_path} must be Job kind"


def test_kvcache_jobs_namespace_threefs():
    """Test that all kvcache jobs are in threefs namespace."""
    jobs = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for job_path in jobs:
        job = pathlib.Path(job_path)
        if not job.exists():
            continue
        content = job.read_text()
        docs = list(yaml.safe_load_all(content))
        for doc in docs:
            if doc and "metadata" in doc and "namespace" in doc["metadata"]:
                assert doc["metadata"]["namespace"] == "threefs", \
                    f"{job_path} must be in threefs namespace"


def test_kvcache_jobs_use_client_role():
    """Test that all kvcache jobs use nodeSelector role=client."""
    jobs = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for job_path in jobs:
        job = pathlib.Path(job_path)
        if not job.exists():
            continue
        content = job.read_text()
        assert "role: client" in content, \
            f"{job_path} must use nodeSelector role=client"


def test_kvcache_jobs_mount_threefs():
    """Test that all kvcache jobs mount /mnt/3fs."""
    jobs = [
        "aws-eks/benchmark/kvcache-prepare-job.yaml",
        "aws-eks/benchmark/kvcache-read-job.yaml",
        "aws-eks/benchmark/kvcache-gc-job.yaml",
    ]
    for job_path in jobs:
        job = pathlib.Path(job_path)
        if not job.exists():
            continue
        content = job.read_text()
        assert "/mnt/3fs" in content, \
            f"{job_path} must mount /mnt/3fs"


def test_prepare_job_has_block_config():
    """Test that prepare job contains BLOCK_COUNT and BLOCK_KB."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-prepare-job.yaml")
    if not job.exists():
        return
    content = job.read_text()
    assert "BLOCK_COUNT" in content, "prepare job must have BLOCK_COUNT env"
    assert "BLOCK_KB" in content, "prepare job must have BLOCK_KB env"


def test_read_job_has_worker_config():
    """Test that read job contains WORKERS and RUNTIME_SECONDS."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-read-job.yaml")
    if not job.exists():
        return
    content = job.read_text()
    assert "WORKERS" in content, "read job must have WORKERS env"
    assert "RUNTIME_SECONDS" in content, "read job must have RUNTIME_SECONDS env"


def test_read_job_has_hotset_config():
    """Test that read job contains HOTSET_PERCENT and HOT_READ_PERCENT."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-read-job.yaml")
    if not job.exists():
        return
    content = job.read_text()
    assert "HOTSET_PERCENT" in content, "read job must have HOTSET_PERCENT env"
    assert "HOT_READ_PERCENT" in content, "read job must have HOT_READ_PERCENT env"


def test_gc_job_has_delete_config():
    """Test that gc job contains DELETE_COUNT and MODE."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-gc-job.yaml")
    if not job.exists():
        return
    content = job.read_text()
    assert "DELETE_COUNT" in content, "gc job must have DELETE_COUNT env"
    assert "MODE" in content, "gc job must have MODE env"


def test_gc_job_supports_rename_delete():
    """Test that gc job supports rename_delete mode."""
    job = pathlib.Path("aws-eks/benchmark/kvcache-gc-job.yaml")
    if not job.exists():
        return
    content = job.read_text()
    assert "rename_delete" in content, "gc job must support rename_delete mode"
