"""Configuration for TeamHealthRadar."""

from __future__ import annotations

import os
from pydantic import BaseModel, Field


class RadarConfig(BaseModel):
    """Runtime configuration for TeamHealthRadar."""

    github_token: str = Field("", description="GitHub API token")
    jira_url: str = Field("", description="JIRA instance URL")
    jira_token: str = Field("", description="JIRA API token")
    openrouter_api_key: str = Field("", description="OpenRouter API key")
    industry: str = Field("fintech", description="Industry context")
    lookback_days: int = Field(30, description="Days of history to analyse")
    host: str = Field("0.0.0.0", description="API server host")
    port: int = Field(8000, description="API server port")

    @classmethod
    def from_env(cls) -> "RadarConfig":
        return cls(
            github_token=os.environ.get("GITHUB_TOKEN", ""),
            jira_url=os.environ.get("JIRA_URL", ""),
            jira_token=os.environ.get("JIRA_TOKEN", ""),
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY", ""),
            industry=os.environ.get("RADAR_INDUSTRY", "fintech"),
        )

    @property
    def has_github(self) -> bool:
        return bool(self.github_token)

    @property
    def has_jira(self) -> bool:
        return bool(self.jira_url and self.jira_token)