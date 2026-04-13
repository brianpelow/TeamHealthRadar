"""Pydantic models for team health metrics."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class DoraMetrics(BaseModel):
    """DORA four key metrics."""

    deployment_frequency: float = Field(0.0, description="Deployments per day")
    lead_time_hours: float = Field(0.0, description="Lead time for changes in hours")
    change_failure_rate: float = Field(0.0, description="Percentage of deployments causing failures")
    mttr_hours: float = Field(0.0, description="Mean time to restore in hours")

    @property
    def deployment_band(self) -> str:
        if self.deployment_frequency >= 1.0:
            return "elite"
        elif self.deployment_frequency >= 1/7:
            return "high"
        elif self.deployment_frequency >= 1/30:
            return "medium"
        return "low"

    @property
    def lead_time_band(self) -> str:
        if self.lead_time_hours <= 1:
            return "elite"
        elif self.lead_time_hours <= 24:
            return "high"
        elif self.lead_time_hours <= 168:
            return "medium"
        return "low"

    @property
    def failure_rate_band(self) -> str:
        if self.change_failure_rate <= 5:
            return "elite"
        elif self.change_failure_rate <= 10:
            return "high"
        elif self.change_failure_rate <= 15:
            return "medium"
        return "low"

    @property
    def mttr_band(self) -> str:
        if self.mttr_hours <= 1:
            return "elite"
        elif self.mttr_hours <= 24:
            return "high"
        elif self.mttr_hours <= 168:
            return "medium"
        return "low"


class SpaceMetrics(BaseModel):
    """SPACE framework signals."""

    satisfaction_score: float = Field(0.0, description="0-100 satisfaction signal from PR sentiment")
    pr_throughput: int = Field(0, description="PRs merged in period")
    review_turnaround_hours: float = Field(0.0, description="Avg hours to first PR review")
    commit_frequency: float = Field(0.0, description="Commits per engineer per day")
    wip_count: int = Field(0, description="Current work in progress items")
    cycle_time_hours: float = Field(0.0, description="Avg hours from first commit to merge")


class TeamScore(BaseModel):
    """Composite team health score."""

    team: str
    score: int = Field(0, description="Overall health score 0-100")
    dora_score: int = Field(0, description="DORA component score 0-100")
    space_score: int = Field(0, description="SPACE component score 0-100")
    trend: str = Field("stable", description="improving/stable/declining")
    band: str = Field("medium", description="elite/high/medium/low")
    period_days: int = Field(30)
    dora: DoraMetrics = Field(default_factory=DoraMetrics)
    space: SpaceMetrics = Field(default_factory=SpaceMetrics)
    narrative: Optional[str] = None


class TeamConfig(BaseModel):
    """Configuration for a tracked team."""

    name: str
    github_repos: list[str] = Field(default_factory=list)
    jira_project: str = ""
    members: list[str] = Field(default_factory=list)
    industry: str = "fintech"