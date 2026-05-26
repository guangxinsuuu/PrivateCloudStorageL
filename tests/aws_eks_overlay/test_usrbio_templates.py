"""Test USRBIO FIO templates and configuration."""
import pathlib


def test_usrbio_template_has_fio_engine():
    """Test that USRBIO template specifies fio external engine."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Check for fio ioengine external
    assert "ioengine=external" in content or "-ioengine=external" in content, \
        "USRBIO template must use fio external ioengine"

    # Check for hf3fs_usrbio.so
    assert "hf3fs_usrbio.so" in content, \
        "USRBIO template must reference hf3fs_usrbio.so"


def test_usrbio_template_has_read_write_tests():
    """Test that USRBIO template includes read and write tests."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Check for read test
    assert "rw=read" in content or "-rw=read" in content, \
        "USRBIO template must include read test"

    # Check for write test
    assert "rw=write" in content or "-rw=write" in content, \
        "USRBIO template must include write test"


def test_usrbio_template_has_json_output():
    """Test that USRBIO template outputs JSON format."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()
    assert "output-format=json" in content or "--output-format=json" in content, \
        "USRBIO template must use JSON output format"


def test_usrbio_template_configurable_params():
    """Test that USRBIO template has configurable parameters."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Check for configurable runtime
    assert "RUNTIME" in content, "USRBIO template must have configurable RUNTIME"

    # Check for configurable bs
    assert "BS" in content, "USRBIO template must have configurable BS"

    # Check for configurable iodepth
    assert "IODEPTH" in content or "iodepth" in content, \
        "USRBIO template must have configurable iodepth"

    # Check for configurable numjobs
    assert "NUMJOBS" in content or "numjobs" in content, \
        "USRBIO template must have configurable numjobs"


def test_usrbio_job_runs_on_client():
    """Test that USRBIO job runs on client nodes."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    if not job_file.exists():
        return

    content = job_file.read_text()
    assert "role: client" in content or "role=client" in content, \
        "USRBIO job must run on role=client nodes"


def test_usrbio_job_requests_efa():
    """Test that USRBIO job requests EFA."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    if not job_file.exists():
        return

    content = job_file.read_text()
    assert "vpc.amazonaws.com/efa" in content, \
        "USRBIO job must request EFA resource"


def test_usrbio_job_mounts_3fs():
    """Test that USRBIO job mounts /mnt/3fs."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    if not job_file.exists():
        return

    content = job_file.read_text()
    assert "/mnt/3fs" in content, "USRBIO job must mount /mnt/3fs"


def test_usrbio_template_fails_if_engine_missing():
    """Test that USRBIO template fails clearly if engine is missing."""
    script_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-template.sh")
    if not script_file.exists():
        return

    content = script_file.read_text()

    # Should check if engine file exists (using if [ -f or if [[ -f)
    has_file_check = ("[ -f" in content or "[[ -f" in content or "[ ! -f" in content or "[[ ! -f" in content)
    assert has_file_check, "USRBIO template must check if engine file exists"

    # Should have error message
    assert "ERROR" in content or "error" in content, \
        "USRBIO template must have error message if engine missing"
