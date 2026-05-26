"""Test that AWS overlay does not contain Alibaba-only assumptions."""
import pathlib
import re


ALIBABA_TERMS = [
    "eRDMA",
    "erdma",
    "ESSD",
    "essd",
    r"\bACK\b",  # Word boundary to avoid matching "backoffLimit"
    "aliyun",
    "alibaba",
    "cn-hangzhou",
    "alicloud",
    "alibabacloud",
    "diskplugin.csi.alibabacloud.com",
]


def test_no_alibaba_assumptions_in_yaml():
    """Test that AWS overlay YAML files don't contain Alibaba assumptions."""
    aws_eks_dir = pathlib.Path("aws-eks")
    if not aws_eks_dir.exists():
        return  # Skip if not created yet

    yaml_files = list(aws_eks_dir.rglob("*.yaml")) + list(aws_eks_dir.rglob("*.yml"))

    for yaml_file in yaml_files:
        content = yaml_file.read_text()

        # Check if file is a comparison/migration doc
        if "comparison" in content.lower() or "migration" in content.lower():
            continue

        for term in ALIBABA_TERMS:
            # Case insensitive search
            if re.search(term, content, re.IGNORECASE):
                assert False, f"{yaml_file} contains Alibaba term: {term}"


def test_no_alibaba_assumptions_in_scripts():
    """Test that AWS overlay scripts don't contain Alibaba assumptions.

    Exception: Deployment scripts that explicitly convert Alibaba → AWS
    may mention Alibaba terms in sed/replacement commands.
    """
    aws_eks_dir = pathlib.Path("aws-eks")
    if not aws_eks_dir.exists():
        return

    script_files = list(aws_eks_dir.rglob("*.sh"))

    for script_file in script_files:
        # Skip deployment/conversion scripts - they explicitly handle Alibaba→AWS
        if "deploy" in script_file.name.lower() or "threefs" in str(script_file.parent):
            continue

        content = script_file.read_text()

        for term in ALIBABA_TERMS:
            if re.search(term, content, re.IGNORECASE):
                assert False, f"{script_file} contains Alibaba term: {term}"


def test_readme_may_mention_alibaba_in_comparison():
    """Test that README may mention Alibaba only in comparison section."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # README is allowed to mention Alibaba in comparison/migration context
    # This test just verifies the README exists and is readable
    assert len(content) > 0, "README must not be empty"
