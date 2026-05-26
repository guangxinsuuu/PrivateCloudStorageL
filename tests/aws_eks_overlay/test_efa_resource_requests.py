"""Test EFA resource requests in workloads."""
import pathlib
import yaml


def test_efa_test_pod_has_efa_resource():
    """Test that EFA test pod requests EFA resource."""
    pod_file = pathlib.Path("aws-eks/efa/efa-test-pod.yaml")
    if not pod_file.exists():
        return

    with open(pod_file) as f:
        pod = yaml.safe_load(f)

    container = pod["spec"]["containers"][0]
    requests = container.get("resources", {}).get("requests", {})
    limits = container.get("resources", {}).get("limits", {})

    assert "vpc.amazonaws.com/efa" in requests, "EFA test pod must request EFA"
    assert requests["vpc.amazonaws.com/efa"] == "1"
    assert "vpc.amazonaws.com/efa" in limits, "EFA test pod must limit EFA"
    assert limits["vpc.amazonaws.com/efa"] == "1"


def test_threefs_values_has_efa_resources():
    """Test that 3FS values overlay includes EFA resource requests."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_file.exists():
        return

    with open(values_file) as f:
        values = yaml.safe_load(f)

    # Check storage resources
    if "storage" in values and "resources" in values["storage"]:
        storage_res = values["storage"]["resources"]
        if "requests" in storage_res:
            assert "vpc.amazonaws.com/efa" in storage_res["requests"], \
                "storage must request EFA"

    # Check client/fuse resources
    for component in ["client", "fuse"]:
        if component in values and "resources" in values[component]:
            comp_res = values[component]["resources"]
            if "requests" in comp_res:
                assert "vpc.amazonaws.com/efa" in comp_res["requests"], \
                    f"{component} must request EFA"


def test_usrbio_fio_job_has_efa_resource():
    """Test that USRBIO FIO job requests EFA resource."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    if not job_file.exists():
        return

    with open(job_file) as f:
        job = yaml.safe_load(f)

    container = job["spec"]["template"]["spec"]["containers"][0]
    requests = container.get("resources", {}).get("requests", {})
    limits = container.get("resources", {}).get("limits", {})

    assert "vpc.amazonaws.com/efa" in requests, "USRBIO FIO job must request EFA"
    assert requests["vpc.amazonaws.com/efa"] == "1"
    assert "vpc.amazonaws.com/efa" in limits, "USRBIO FIO job must limit EFA"
    assert limits["vpc.amazonaws.com/efa"] == "1"
