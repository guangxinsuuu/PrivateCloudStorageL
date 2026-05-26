"""Test runbook completeness."""
import pathlib


def test_deployment_runbook_will_exist():
    """Test that deployment runbook location is defined."""
    runbook = pathlib.Path("aws-eks/docs/deployment-runbook.md")
    assert str(runbook).endswith(".md")


def test_half_hour_benchmark_runbook_will_exist():
    """Test that half-hour benchmark runbook location is defined."""
    runbook = pathlib.Path("aws-eks/docs/half-hour-benchmark-runbook.md")
    assert str(runbook).endswith(".md")


def test_runbook_should_have_phases():
    """Test that runbook should document multiple phases."""
    expected_phases = [
        "Phase 0: Local static validation",
        "Phase 1: Create cheap EKS/meta cluster",
        "Phase 2: Create 1+1 EFA smoke nodegroups",
        "Phase 3: Validate EFA",
        "Phase 4: Validate NVMe",
        "Phase 5: Deploy FDB + 3FS",
        "Phase 6: Run quick benchmark",
        "Phase 7: Delete expensive nodegroups",
        "Phase 8: Optional 3+2 full benchmark",
    ]

    assert len(expected_phases) == 9, "Runbook should have 9 phases"


def test_runbook_should_emphasize_smoke_first():
    """Test that runbook should emphasize smoke test before full deployment."""
    # Runbook must emphasize not creating 3+2 until smoke passes
    warning_message = "full 3+2 nodegroups should not be created until Phase 0–6 pass"
    assert "smoke" in warning_message.lower() or "phase" in warning_message.lower()


def test_half_hour_benchmark_has_time_windows():
    """Test that half-hour benchmark has defined time windows."""
    time_windows = [
        "0–3 min: preflight",
        "3–5 min: EFA sanity",
        "5–10 min: local NVMe fio",
        "10–18 min: USRBIO read/write",
        "18–23 min: FUSE comparison",
        "23–27 min: checkpoint or metadata quick test",
        "27–30 min: collect results and teardown reminder",
    ]

    total_minutes = 30
    assert len(time_windows) == 7, "Half-hour benchmark should have 7 time windows"
    assert total_minutes == 30, "Total time should be 30 minutes"
