"""Test NVMe DaemonSet configurations."""
import pathlib
import yaml


def test_nvme_check_daemonset_exists():
    """Test that NVMe check DaemonSet exists."""
    ds_file = pathlib.Path("aws-eks/nvme/nvme-check-daemonset.yaml")
    assert ds_file.exists(), "nvme-check-daemonset.yaml must exist"


def test_nvme_check_daemonset_valid():
    """Test that NVMe check DaemonSet is valid."""
    ds_file = pathlib.Path("aws-eks/nvme/nvme-check-daemonset.yaml")
    if not ds_file.exists():
        return

    with open(ds_file) as f:
        ds = yaml.safe_load(f)

    assert ds["kind"] == "DaemonSet"
    spec = ds["spec"]["template"]["spec"]

    # Check nodeSelector
    assert spec.get("nodeSelector", {}).get("role") == "storage", \
        "NVMe check must run on role=storage nodes"

    # Check tolerations
    tolerations = spec.get("tolerations", [])
    has_storage_toleration = False
    for tol in tolerations:
        if tol.get("key") == "role" and tol.get("value") == "storage":
            has_storage_toleration = True
            break
    assert has_storage_toleration, "NVMe check must tolerate role=storage:NoSchedule"

    # Check privileged
    container = spec["containers"][0]
    assert container["securityContext"].get("privileged") == True

    # Check hostPID
    assert spec.get("hostPID") == True

    # Check volumes
    volumes = {v["name"]: v for v in spec.get("volumes", [])}
    assert "host-dev" in volumes
    assert "host-mnt" in volumes
    assert volumes["host-dev"]["hostPath"]["path"] == "/dev"
    assert volumes["host-mnt"]["hostPath"]["path"] == "/mnt"


def test_nvme_mount_daemonset_exists():
    """Test that NVMe mount DaemonSet exists."""
    ds_file = pathlib.Path("aws-eks/nvme/nvme-mount-daemonset.yaml")
    assert ds_file.exists(), "nvme-mount-daemonset.yaml must exist"


def test_nvme_mount_daemonset_valid():
    """Test that NVMe mount DaemonSet is valid."""
    ds_file = pathlib.Path("aws-eks/nvme/nvme-mount-daemonset.yaml")
    if not ds_file.exists():
        return

    with open(ds_file) as f:
        ds = yaml.safe_load(f)

    assert ds["kind"] == "DaemonSet"
    spec = ds["spec"]["template"]["spec"]

    # Check nodeSelector
    assert spec.get("nodeSelector", {}).get("role") == "storage"

    # Check tolerations
    tolerations = spec.get("tolerations", [])
    has_storage_toleration = False
    for tol in tolerations:
        if tol.get("key") == "role" and tol.get("value") == "storage":
            has_storage_toleration = True
            break
    assert has_storage_toleration

    # Check privileged
    container = spec["containers"][0]
    assert container["securityContext"].get("privileged") == True

    # Check hostPID
    assert spec.get("hostPID") == True

    # Check mounts /mnt/nvme0 style paths in command
    command = " ".join(container.get("command", []))
    assert "/mnt/nvme" in command or "nvme" in command.lower()

    # Check warning about formatting
    assert "WARNING" in command or "warning" in command.lower(), \
        "Mount DaemonSet must warn about formatting"


def test_nvme_daemonsets_use_hostpath():
    """Test that NVMe DaemonSets use hostPath volumes."""
    ds_files = [
        pathlib.Path("aws-eks/nvme/nvme-check-daemonset.yaml"),
        pathlib.Path("aws-eks/nvme/nvme-mount-daemonset.yaml"),
    ]

    for ds_file in ds_files:
        if not ds_file.exists():
            continue

        with open(ds_file) as f:
            ds = yaml.safe_load(f)

        volumes = ds["spec"]["template"]["spec"].get("volumes", [])
        has_hostpath = False
        for vol in volumes:
            if "hostPath" in vol:
                has_hostpath = True
                break

        assert has_hostpath, f"{ds_file.name} must use hostPath volumes"
