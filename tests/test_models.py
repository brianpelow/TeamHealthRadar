"""Tests for metric models."""

from teamhealth.models.metrics import DoraMetrics, SpaceMetrics, TeamScore, TeamConfig


def test_dora_deployment_band_elite() -> None:
    dora = DoraMetrics(deployment_frequency=2.0)
    assert dora.deployment_band == "elite"


def test_dora_deployment_band_high() -> None:
    dora = DoraMetrics(deployment_frequency=0.5)
    assert dora.deployment_band == "high"


def test_dora_deployment_band_medium() -> None:
    dora = DoraMetrics(deployment_frequency=0.05)
    assert dora.deployment_band == "medium"


def test_dora_deployment_band_low() -> None:
    dora = DoraMetrics(deployment_frequency=0.01)
    assert dora.deployment_band == "low"


def test_dora_lead_time_band_elite() -> None:
    dora = DoraMetrics(lead_time_hours=0.5)
    assert dora.lead_time_band == "elite"


def test_dora_failure_rate_band_elite() -> None:
    dora = DoraMetrics(change_failure_rate=3.0)
    assert dora.failure_rate_band == "elite"


def test_dora_mttr_band_elite() -> None:
    dora = DoraMetrics(mttr_hours=0.5)
    assert dora.mttr_band == "elite"


def test_team_score_defaults() -> None:
    score = TeamScore(team="test-team")
    assert score.score == 0
    assert score.band == "medium"
    assert score.trend == "stable"


def test_team_config_defaults() -> None:
    config = TeamConfig(name="payments-team")
    assert config.github_repos == []
    assert config.jira_project == ""
    assert config.industry == "fintech"