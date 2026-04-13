"""Tests for TeamHealthRadar FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from teamhealth.api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_list_teams_endpoint() -> None:
    response = client.get("/teams")
    assert response.status_code == 200
    data = response.json()
    assert "teams" in data
    assert len(data["teams"]) == 3


def test_get_team_score_valid() -> None:
    response = client.get("/teams/payments-team/score")
    assert response.status_code == 200
    data = response.json()
    assert data["team"] == "payments-team"
    assert 0 <= data["score"] <= 100
    assert data["band"] in ("elite", "high", "medium", "low")


def test_get_team_score_not_found() -> None:
    response = client.get("/teams/nonexistent-team/score")
    assert response.status_code == 404


def test_get_team_metrics_valid() -> None:
    response = client.get("/teams/payments-team/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "dora" in data
    assert "space" in data
    assert "dora_bands" in data


def test_get_benchmarks() -> None:
    response = client.get("/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert "bands" in data
    assert len(data["bands"]) == 4