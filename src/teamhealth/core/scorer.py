"""Team health scoring engine."""

from __future__ import annotations

from teamhealth.models.metrics import DoraMetrics, SpaceMetrics, TeamScore


BAND_SCORES = {"elite": 100, "high": 75, "medium": 50, "low": 25}


def score_dora(dora: DoraMetrics) -> int:
    """Convert DORA metrics to a 0-100 score."""
    scores = [
        BAND_SCORES.get(dora.deployment_band, 50),
        BAND_SCORES.get(dora.lead_time_band, 50),
        BAND_SCORES.get(dora.failure_rate_band, 50),
        BAND_SCORES.get(dora.mttr_band, 50),
    ]
    return int(sum(scores) / len(scores))


def score_space(space: SpaceMetrics) -> int:
    """Convert SPACE metrics to a 0-100 score."""
    scores = []

    scores.append(min(100, int(space.satisfaction_score)))

    if space.pr_throughput >= 50:
        scores.append(100)
    elif space.pr_throughput >= 20:
        scores.append(75)
    elif space.pr_throughput >= 10:
        scores.append(50)
    else:
        scores.append(25)

    if space.review_turnaround_hours <= 4:
        scores.append(100)
    elif space.review_turnaround_hours <= 24:
        scores.append(75)
    elif space.review_turnaround_hours <= 72:
        scores.append(50)
    else:
        scores.append(25)

    if space.cycle_time_hours <= 24:
        scores.append(100)
    elif space.cycle_time_hours <= 72:
        scores.append(75)
    elif space.cycle_time_hours <= 168:
        scores.append(50)
    else:
        scores.append(25)

    return int(sum(scores) / len(scores))


def compute_team_score(
    team: str,
    dora: DoraMetrics,
    space: SpaceMetrics,
    period_days: int = 30,
) -> TeamScore:
    """Compute composite team health score."""
    dora_score = score_dora(dora)
    space_score = score_space(space)
    overall = int(dora_score * 0.6 + space_score * 0.4)

    if overall >= 85:
        band = "elite"
    elif overall >= 65:
        band = "high"
    elif overall >= 45:
        band = "medium"
    else:
        band = "low"

    return TeamScore(
        team=team,
        score=overall,
        dora_score=dora_score,
        space_score=space_score,
        trend="stable",
        band=band,
        period_days=period_days,
        dora=dora,
        space=space,
    )