"""Test KVCache documentation."""
import pathlib
import re


def test_benchmark_readme_mentions_kvcache():
    """Test that benchmark README mentions KVCache-like."""
    readme = pathlib.Path("aws-eks/benchmark/README.md")
    if not readme.exists():
        return

    content = readme.read_text()
    assert "KVCache" in content or "kvcache" in content, \
        "Benchmark README must mention KVCache"


def test_benchmark_readme_disclaims_official_kvcache():
    """Test that README explicitly says it does not reproduce official DeepSeek KVCache."""
    readme = pathlib.Path("aws-eks/benchmark/README.md")
    if not readme.exists():
        return

    content = readme.read_text().lower()

    # Should contain disclaimer about not reproducing official results
    disclaimers = [
        "not reproduce",
        "does not reproduce",
        "synthetic",
        "poc scale",
        "kvcache-like",
    ]

    found = any(disclaimer in content for disclaimer in disclaimers)
    assert found, \
        "README must clarify that this is not official DeepSeek KVCache reproduction"


def test_benchmark_readme_lists_kvcache_jobs():
    """Test that README lists prepare/read/gc jobs."""
    readme = pathlib.Path("aws-eks/benchmark/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    required_mentions = [
        "prepare",
        "read",
        "gc",
    ]

    for mention in required_mentions:
        # Check for the word in context of kvcache
        pattern = re.compile(rf"kvcache.*{mention}|{mention}.*kvcache", re.IGNORECASE)
        assert pattern.search(content), \
            f"README must mention kvcache {mention}"


def test_benchmark_readme_lists_kvcache_metrics():
    """Test that README mentions read_mib_s, read_ops_s, gc_ops_s."""
    readme = pathlib.Path("aws-eks/benchmark/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    required_metrics = [
        "read_mib_s",
        "read_ops_s",
        "gc_ops_s",
    ]

    for metric in required_metrics:
        assert metric in content, \
            f"README must mention {metric} metric"


def test_kvcache_section_exists_in_readme():
    """Test that README has a dedicated KVCache section."""
    readme = pathlib.Path("aws-eks/benchmark/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # Should have a section header for KVCache
    patterns = [
        r"##.*KVCache",
        r"##.*kvcache",
        r"###.*KVCache",
        r"###.*kvcache",
    ]

    found = any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
    assert found, "README must have a KVCache section"


def test_main_readme_mentions_kvcache_figure():
    """Test that main README mentions KVCache in benchmark figures."""
    readme = pathlib.Path("aws-eks/README.md")
    if not readme.exists():
        return

    content = readme.read_text()

    # Should mention KVCache in context of figures or benchmarks
    has_kvcache = "KVCache" in content or "kvcache" in content
    assert has_kvcache, "Main README should mention KVCache benchmark"
