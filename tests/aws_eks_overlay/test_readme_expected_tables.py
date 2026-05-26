"""Test that README includes expected benchmark tables."""
import pathlib


def test_readme_has_layered_baseline_table():
    """Test that README includes layered baseline table."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # Check for table headers or key terms
    required_terms = [
        "Layer",
        "Test",
        "Expected",
        "EKS",
        "EFA",
        "NVMe",
        "3FS FUSE",
        "3FS USRBIO",
        "Metadata",
        "Checkpoint",
    ]

    missing_terms = []
    for term in required_terms:
        if term not in content:
            missing_terms.append(term)

    assert len(missing_terms) == 0, \
        f"README must include layered baseline table with terms: {missing_terms}"


def test_readme_has_path_comparison_table():
    """Test that README includes path comparison table."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    required_terms = [
        "Path",
        "Throughput",
        "Local NVMe",
        "Raw EFA",
        "USRBIO",
        "FUSE",
    ]

    missing_terms = []
    for term in required_terms:
        if term not in content:
            missing_terms.append(term)

    assert len(missing_terms) == 0, \
        f"README must include path comparison table with terms: {missing_terms}"


def test_readme_has_scaling_table():
    """Test that README includes scaling expectations table."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    required_terms = [
        "Scale",
        "client",
        "storage",
        "baseline",
        "linear",
    ]

    missing_terms = []
    for term in required_terms:
        if term.lower() not in content.lower():
            missing_terms.append(term)

    assert len(missing_terms) == 0, \
        f"README must include scaling table with terms: {missing_terms}"


def test_readme_has_bottleneck_diagnosis_table():
    """Test that README includes bottleneck diagnosis table."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    required_terms = [
        "Symptom",
        "Bottleneck",
        "fi_info",
        "bandwidth",
        "NVMe",
        "FUSE slow",
        "USRBIO slow",
        "metadata slow",
    ]

    found_count = sum(1 for term in required_terms if term.lower() in content.lower())

    assert found_count >= 6, \
        f"README must include bottleneck diagnosis table (found {found_count}/8 terms)"


def test_readme_has_cost_warning():
    """Test that README includes cost warning."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # Must warn about expensive nodes
    assert "WARNING" in content or "warning" in content.lower(), \
        "README must include WARNING"
    assert "i3en.24xlarge" in content, "README must mention i3en.24xlarge"
    assert "c7gn.16xlarge" in content, "README must mention c7gn.16xlarge"
    assert "expensive" in content.lower() or "cost" in content.lower(), \
        "README must warn about cost"


def test_readme_explains_teardown():
    """Test that README explains how to teardown."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    assert "teardown" in content.lower() or "delete" in content.lower(), \
        "README must explain teardown process"
    assert "delete-efa-nodegroups" in content or "nodegroup" in content, \
        "README must reference nodegroup deletion"


def test_readme_has_3fs_component_mapping():
    """Test that README maps 3FS components to AWS node roles."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    components = [
        "mgmtd",
        "meta",
        "storage",
        "FUSE",
        "USRBIO",
    ]

    roles = [
        "role=meta",
        "role=storage",
        "role=client",
    ]

    component_count = sum(1 for comp in components if comp in content)
    role_count = sum(1 for role in roles if role in content)

    assert component_count >= 4, \
        f"README must map 3FS components (found {component_count}/5)"
    assert role_count >= 2, \
        f"README must explain node roles (found {role_count}/3)"
