"""Tests for the health scoring engine."""

from teamhealth.core.scorer import score_dora, score_space, compute_team_score
from teamhealth.collectors.github import _mock_dora, _mock_space
from teamhealth.models.metrics import DoraMetrics, SpaceMetrics


def test_score_dora_elite() -> None:
    dora = DoraMetrics(
        deployment_frequency=2.0,
        lead_time_hours=0.5,
        change_failure_rate=2.0,
        mttr_hours=0.5,
    )
    assert score_dora(dora) == 100


def test_score_dora_low() -> None:
    dora = DoraMetrics(
        deployment_frequency=0.01,
        lead_time_hours=500.0,
        change_failure_rate=50.0,
        mttr_hours=200.0,
    )
    assert score_dora(dora) == 25


def test_score_space_returns_int() -> None:
    space = _mock_space()
    score = score_space(space)
    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_compute_team_score_returns_score() -> None:
    score = compute_team_score("test-team", _mock_dora(), _mock_space())
    assert score.team == "test-team"
    assert 0 <= score.score <= 100
    assert score.band in ("elite", "high", "medium", "low")


def test_compute_team_score_elite_band() -> None:
    dora = DoraMetrics(deployment_frequency=2.0, lead_time_hours=0.5, change_failure_rate=2.0, mttr_hours=0.5)
    space = SpaceMetrics(satisfaction_score=95.0, pr_throughput=100, review_turnaround_hours=2.0, cycle_time_hours=8.0)
    score = compute_team_score("elite-team", dora, space)
    assert score.band == "elite"
    assert score.score >= 85


def test_compute_team_score_stores_metrics() -> None:
    dora = _mock_dora()
    space = _mock_space()
    score = compute_team_score("test-team", dora, space)
    assert score.dora.deployment_frequency == dora.deployment_frequency
    assert score.space.pr_throughput == space.pr_throughput