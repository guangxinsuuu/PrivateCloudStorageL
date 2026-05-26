"""Test EKS nodegroup configurations."""
import pathlib
import yaml


def test_cluster_phase1_meta_config_exists():
    """Test that cluster phase1 meta config exists."""
    config_file = pathlib.Path("aws-eks/configs/cluster-phase1-meta.yaml")
    assert config_file.exists(), "cluster-phase1-meta.yaml must exist"


def test_cluster_phase1_meta_config_valid():
    """Test that cluster phase1 meta config is valid."""
    config_file = pathlib.Path("aws-eks/configs/cluster-phase1-meta.yaml")
    if not config_file.exists():
        return

    with open(config_file) as f:
        config = yaml.safe_load(f)

    assert config["metadata"]["name"] == "3fs-demo"
    assert config["metadata"]["region"] == "us-east-1"
    assert config["metadata"]["version"] == "1.30"

    # Check availabilityZones
    assert "us-east-1a" in config["availabilityZones"]
    assert "us-east-1b" in config["availabilityZones"]

    # Check meta nodegroup
    meta_ng = None
    for ng in config["managedNodeGroups"]:
        if ng["name"] == "meta":
            meta_ng = ng
            break

    assert meta_ng is not None, "meta nodegroup must exist"
    assert meta_ng["instanceType"] == "c6i.4xlarge"
    assert meta_ng["desiredCapacity"] == 2
    assert meta_ng["labels"]["role"] == "meta"


def test_nodegroups_efa_1x1_config_exists():
    """Test that 1+1 EFA nodegroup config exists."""
    config_file = pathlib.Path("aws-eks/configs/nodegroups-efa-1x1.yaml")
    assert config_file.exists(), "nodegroups-efa-1x1.yaml must exist"


def test_nodegroups_efa_1x1_config_valid():
    """Test that 1+1 EFA nodegroup config is valid."""
    config_file = pathlib.Path("aws-eks/configs/nodegroups-efa-1x1.yaml")
    if not config_file.exists():
        return

    with open(config_file) as f:
        config = yaml.safe_load(f)

    assert config["metadata"]["name"] == "3fs-demo"
    assert config["metadata"]["region"] == "us-east-1"

    # Check storage nodegroup
    storage_ng = None
    client_ng = None
    for ng in config["managedNodeGroups"]:
        if ng["name"] == "storage":
            storage_ng = ng
        elif ng["name"] == "client":
            client_ng = ng

    assert storage_ng is not None, "storage nodegroup must exist"
    assert storage_ng["instanceType"] == "i3en.24xlarge"
    assert storage_ng["desiredCapacity"] == 1
    assert storage_ng.get("efaEnabled") == True, "storage must use efaEnabled: true"
    assert storage_ng["labels"]["role"] == "storage"
    assert len(storage_ng["taints"]) > 0

    assert client_ng is not None, "client nodegroup must exist"
    assert client_ng["instanceType"] == "c7gn.16xlarge"
    assert client_ng["desiredCapacity"] == 1
    assert client_ng.get("efaEnabled") == True, "client must use efaEnabled: true"
    assert client_ng["labels"]["role"] == "client"


def test_nodegroups_efa_3x2_config_exists():
    """Test that 3+2 EFA nodegroup config exists."""
    config_file = pathlib.Path("aws-eks/configs/nodegroups-efa-3x2.yaml")
    assert config_file.exists(), "nodegroups-efa-3x2.yaml must exist"


def test_nodegroups_efa_3x2_config_valid():
    """Test that 3+2 EFA nodegroup config is valid."""
    config_file = pathlib.Path("aws-eks/configs/nodegroups-efa-3x2.yaml")
    if not config_file.exists():
        return

    with open(config_file) as f:
        config = yaml.safe_load(f)

    assert config["metadata"]["name"] == "3fs-demo"
    assert config["metadata"]["region"] == "us-east-1"

    # Check storage-full and client-full nodegroups
    storage_full_ng = None
    client_full_ng = None
    for ng in config["managedNodeGroups"]:
        if ng["name"] == "storage-full":
            storage_full_ng = ng
        elif ng["name"] == "client-full":
            client_full_ng = ng

    assert storage_full_ng is not None, "storage-full nodegroup must exist"
    assert storage_full_ng["instanceType"] == "i3en.24xlarge"
    assert storage_full_ng["desiredCapacity"] == 3
    assert storage_full_ng.get("efaEnabled") == True
    assert storage_full_ng["labels"]["role"] == "storage"

    assert client_full_ng is not None, "client-full nodegroup must exist"
    assert client_full_ng["instanceType"] == "c7gn.16xlarge"
    assert client_full_ng["desiredCapacity"] == 2
    assert client_full_ng.get("efaEnabled") == True
    assert client_full_ng["labels"]["role"] == "client"


def test_no_invalid_efa_field():
    """Test that configs don't use invalid efa.enabled field."""
    config_files = [
        pathlib.Path("aws-eks/configs/nodegroups-efa-1x1.yaml"),
        pathlib.Path("aws-eks/configs/nodegroups-efa-3x2.yaml"),
    ]

    for config_file in config_files:
        if not config_file.exists():
            continue

        content = config_file.read_text()
        assert "efa:" not in content or "enabled: true" not in content, \
            f"{config_file} must not use efa.enabled field, use efaEnabled instead"
