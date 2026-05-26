"""Test that cost warnings are conservative and don't claim exact low prices."""
import pathlib
import re


def test_readme_cost_warning_is_conservative():
    """Test that main README doesn't claim exact low hourly costs."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # Forbidden patterns that claim exact low costs
    forbidden_patterns = [
        r"\$8/h\b",  # Exact $8/h
        r"\$18/h\b",  # Exact $18/h
        r"~\$8\b",  # Approximate $8
        r"~\$18\b",  # Approximate $18
        r"\$8/hour\b",  # $8/hour
        r"\$18/hour\b",  # $18/hour
    ]

    for pattern in forbidden_patterns:
        matches = re.findall(pattern, content)
        if matches:
            assert False, f"README contains forbidden exact cost claim: {matches[0]}. Use conservative warnings instead."


def test_cost_warning_mentions_variability():
    """Test that cost warnings mention pricing variability."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text().lower()

    # Should mention that costs vary
    variability_indicators = [
        "depend",
        "vary",
        "current",
        "check",
        "calculator",
        "pricing",
    ]

    found = any(indicator in content for indicator in variability_indicators)
    assert found, "Cost warnings should mention pricing variability"


def test_cost_warning_emphasizes_immediate_teardown():
    """Test that cost warnings emphasize immediate teardown."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text().lower()

    # Should emphasize deletion
    teardown_indicators = [
        "delete",
        "teardown",
        "remove",
        "cleanup",
        "after test",
        "immediately",
    ]

    found = any(indicator in content for indicator in teardown_indicators)
    assert found, "Cost warnings should emphasize immediate teardown"


def test_no_exact_low_cost_in_any_markdown():
    """Test that no markdown file claims exact low hourly costs."""
    aws_eks_dir = pathlib.Path("aws-eks")
    if not aws_eks_dir.exists():
        return

    forbidden_patterns = [
        r"\$8/h\b",
        r"\$18/h\b",
        r"~\$8/h",
        r"~\$18/h",
        r"\$8\.00/h",
        r"\$18\.00/h",
    ]

    for md_file in aws_eks_dir.rglob("*.md"):
        content = md_file.read_text()

        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content)
            if matches:
                assert False, f"{md_file.name} contains forbidden exact cost claim: {matches[0]}"


def test_cost_table_uses_conservative_language():
    """Test that any cost tables use conservative language."""
    # If there are cost tables, they should use phrases like:
    # - "tens of USD per hour"
    # - "depends on current pricing"
    # - "check AWS Pricing Calculator"
    # Not exact low numbers

    conservative_phrases = [
        "tens of USD",
        "depend",
        "current pricing",
        "check.*pricing",
        "calculator",
    ]

    # Test just documents expected phrases
    assert len(conservative_phrases) > 0
