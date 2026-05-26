"""Test AWS overlay directory structure."""
import pathlib


def test_aws_eks_directory_exists():
    """Test that aws-eks/ directory exists."""
    aws_eks_dir = pathlib.Path("aws-eks")
    assert aws_eks_dir.exists(), "aws-eks/ directory must exist"
    assert aws_eks_dir.is_dir(), "aws-eks/ must be a directory"


def test_required_subdirectories_exist():
    """Test that all required subdirectories exist."""
    required_dirs = [
        "aws-eks/configs",
        "aws-eks/efa",
        "aws-eks/nvme",
        "aws-eks/foundationdb",
        "aws-eks/threefs",
        "aws-eks/benchmark",
        "aws-eks/teardown",
        "aws-eks/scripts",
    ]
    for dir_path in required_dirs:
        p = pathlib.Path(dir_path)
        assert p.exists(), f"{dir_path} must exist"
        assert p.is_dir(), f"{dir_path} must be a directory"


def test_aws_eks_readme_exists():
    """Test that AWS EKS README exists."""
    readme = pathlib.Path("aws-eks/README.md")
    assert readme.exists(), "aws-eks/README.md must exist"
    assert readme.is_file(), "aws-eks/README.md must be a file"
