"""FastAPI application for TeamHealthRadar."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from teamhealth.core.config import RadarConfig
from teamhealth.core.scorer import compute_team_score
from teamhealth.core.narrator import generate_narrative
from teamhealth.core.benchmarks import get_all_bands
from teamhealth.collectors.github import GitHubCollector, _mock_dora, _mock_space
from teamhealth.models.metrics import TeamScore, TeamConfig

app = FastAPI(
    title="TeamHealthRadar",
    description="Engineering team health scoring for regulated industries",
    version="0.1.0",
)

config = RadarConfig.from_env()

MOCK_TEAMS: list[TeamConfig] = [
    TeamConfig(name="payments-team", github_repos=["org/payments-service"], jira_project="PAY", industry="fintech"),
    TeamConfig(name="platform-team", github_repos=["org/platform-infra"], jira_project="PLAT", industry="fintech"),
    TeamConfig(name="trading-team", github_repos=["org/trading-engine"], jira_project="TRADE", industry="fintech"),
]


class HealthResponse(BaseModel):
    status: str
    version: str
    industry: str


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version="0.1.0", industry=config.industry)


@app.get("/teams")
def list_teams() -> dict:
    return {
        "teams": [
            {"name": t.name, "repos": t.github_repos, "jira_project": t.jira_project}
            for t in MOCK_TEAMS
        ]
    }


@app.get("/teams/{team}/score")
def get_team_score(team: str) -> TeamScore:
    team_config = next((t for t in MOCK_TEAMS if t.name == team), None)
    if not team_config:
        raise HTTPException(status_code=404, detail=f"Team not found: {team}")

    collector = GitHubCollector(token=config.github_token)
    dora = collector.collect_dora(team_config.github_repos, config.lookback_days)
    space = collector.collect_space(team_config.github_repos, config.lookback_days)
    return compute_team_score(team, dora, space, config.lookback_days)


@app.get("/teams/{team}/metrics")
def get_team_metrics(team: str) -> dict:
    team_config = next((t for t in MOCK_TEAMS if t.name == team), None)
    if not team_config:
        raise HTTPException(status_code=404, detail=f"Team not found: {team}")

    collector = GitHubCollector(token=config.github_token)
    dora = collector.collect_dora(team_config.github_repos, config.lookback_days)
    space = collector.collect_space(team_config.github_repos, config.lookback_days)

    return {
        "team": team,
        "period_days": config.lookback_days,
        "dora": dora.model_dump(),
        "dora_bands": {
            "deployment": dora.deployment_band,
            "lead_time": dora.lead_time_band,
            "failure_rate": dora.failure_rate_band,
            "mttr": dora.mttr_band,
        },
        "space": space.model_dump(),
    }


@app.get("/teams/{team}/narrative")
def get_team_narrative(team: str) -> dict:
    team_config = next((t for t in MOCK_TEAMS if t.name == team), None)
    if not team_config:
        raise HTTPException(status_code=404, detail=f"Team not found: {team}")

    collector = GitHubCollector(token=config.github_token)
    dora = collector.collect_dora(team_config.github_repos, config.lookback_days)
    space = collector.collect_space(team_config.github_repos, config.lookback_days)
    score = compute_team_score(team, dora, space, config.lookback_days)
    narrative = generate_narrative(score, industry=config.industry)

    return {"team": team, "score": score.score, "band": score.band, "narrative": narrative}


@app.get("/benchmarks")
def get_benchmarks() -> dict:
    bands = get_all_bands()
    return {
        "source": "DORA State of DevOps Report",
        "bands": [b.model_dump() for b in bands],
    }


def run() -> None:
    import uvicorn
    uvicorn.run("teamhealth.api.main:app", host=config.host, port=config.port, reload=False)


if __name__ == "__main__":
    run()