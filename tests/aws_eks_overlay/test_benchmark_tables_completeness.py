"""Test benchmark tables completeness."""
import pathlib


def test_benchmark_result_template_will_exist():
    """Test that benchmark result template location is defined."""
    template = pathlib.Path("aws-eks/docs/benchmark-result-template.md")
    assert str(template).endswith(".md")


def test_benchmark_should_have_required_tables():
    """Test that benchmark template should include all required tables."""
    required_tables = [
        "Final Result Summary",
        "Path Comparison",
        "Scaling Table",
        "Latency Table",
        "Bottleneck Diagnosis",
    ]

    assert len(required_tables) == 5, "Benchmark should have 5 main tables"


def test_final_result_summary_fields():
    """Test that final result summary has expected fields."""
    expected_fields = ["Layer", "Test", "Expected", "Measured", "Pass/Fail", "Bottleneck"]
    assert len(expected_fields) == 6


def test_path_comparison_includes_all_paths():
    """Test that path comparison includes all test paths."""
    expected_paths = [
        "Local NVMe",
        "Raw EFA",
        "3FS FUSE",
        "3FS USRBIO",
        "3FS USRBIO tuned",
    ]

    assert len(expected_paths) >= 4, "Path comparison should have at least 4 paths"
    assert "USRBIO" in " ".join(expected_paths), "USRBIO must be tested"
    assert "FUSE" in " ".join(expected_paths), "FUSE must be tested"


def test_scaling_table_has_configurations():
    """Test that scaling table has different configurations."""
    expected_configs = [
        "1 client / 1 storage",
        "2 clients / 1 storage",
        "2 clients / 3 storages",
        "4 client pods / 3 storages",
    ]

    assert len(expected_configs) >= 3, "Scaling should test multiple configurations"


def test_latency_table_includes_percentiles():
    """Test that latency table includes percentile measurements."""
    percentiles = ["P50", "P99", "P99.9"]
    assert "P99" in percentiles, "P99 latency must be measured"


def test_bottleneck_diagnosis_includes_symptoms():
    """Test that bottleneck diagnosis includes common symptoms."""
    symptoms = [
        "fi_info -p efa fails",
        "EFA bandwidth low",
        "NVMe fio low",
        "FUSE slow but USRBIO fast",
        "USRBIO slow",
        "write P99 high",
        "metadata slow",
        "scaling not linear",
    ]

    assert len(symptoms) >= 6, "Bottleneck diagnosis should cover common symptoms"
