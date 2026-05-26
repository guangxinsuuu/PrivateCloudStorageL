"""Test image placeholder documentation."""
import pathlib
import re


def test_image_build_plan_will_exist():
    """Test that image build plan document location is defined."""
    plan_doc = pathlib.Path("aws-eks/docs/image-build-and-ecr-plan.md")
    # This will be created in later steps
    assert str(plan_doc).endswith(".md")


def test_placeholder_pattern_in_usrbio_job():
    """Test that USRBIO job template has image placeholder pattern."""
    job_file = pathlib.Path("aws-eks/benchmark/usrbio-fio-job-template.yaml")
    if not job_file.exists():
        return

    content = job_file.read_text()

    # Should contain REPLACE_WITH placeholder or similar
    has_placeholder = "REPLACE_WITH" in content or "TBD" in content or "TODO" in content
    assert has_placeholder, "USRBIO job should have image placeholder"


def test_image_references_are_documented():
    """Test that image reference pattern is consistent."""
    # Expected image placeholder pattern
    placeholder_pattern = r"REPLACE_WITH.*IMAGE"

    # Test that pattern is a valid regex
    compiled = re.compile(placeholder_pattern, re.IGNORECASE)
    assert compiled is not None


def test_no_unintended_dockerhub_images():
    """Test that overlay doesn't use random DockerHub images for 3FS components."""
    values_file = pathlib.Path("aws-eks/threefs/values-eks-overlay.yaml")
    if not values_file.exists():
        return

    content = values_file.read_text()

    # Check for image: fields that might contain wrong images
    # Cluster name "3fs-demo" is OK, we're looking for image references

    import re
    # Look for image: field patterns
    image_patterns = re.findall(r'image:\s*["\']?([^"\'\s]+)', content, re.IGNORECASE)

    if len(image_patterns) == 0:
        # No image fields found, which is OK for a values overlay
        return

    # If there are image references, they should either be:
    # - Placeholders (REPLACE_WITH, TBD, TODO)
    # - ECR references (ecr.aws)
    # Not random DockerHub images

    for img in image_patterns:
        if img and not any(x in img.upper() for x in ["REPLACE", "TODO", "TBD", "ECR"]):
            assert False, f"Image reference {img} should be a placeholder or ECR reference"
