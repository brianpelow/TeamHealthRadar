"""Nightly agent — automated maintenance for TeamHealthRadar."""

from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent


def update_benchmark_snapshot() -> None:
    """Write current DORA benchmark definitions to docs."""
    from teamhealth.core.benchmarks import get_all_bands
    bands = get_all_bands()
    snapshot = {
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "source": "DORA State of DevOps Report",
        "bands": [b.model_dump() for b in bands],
    }
    out = REPO_ROOT / "docs" / "benchmark-snapshot.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2))
    print(f"[agent] Updated benchmark snapshot -> {out}")


def compute_mock_scores() -> None:
    """Compute health scores for mock teams and save to docs."""
    from teamhealth.core.scorer import compute_team_score
    from teamhealth.collectors.github import _mock_dora, _mock_space
    teams = ["payments-team", "platform-team", "trading-team"]
    scores = []
    for team in teams:
        score = compute_team_score(team, _mock_dora(), _mock_space())
        scores.append({
            "team": team,
            "score": score.score,
            "band": score.band,
            "dora_score": score.dora_score,
            "space_score": score.space_score,
        })
    out = REPO_ROOT / "docs" / "mock-scores.json"
    out.write_text(json.dumps({
        "generated_at": datetime.utcnow().isoformat(),
        "date": date.today().isoformat(),
        "scores": scores,
    }, indent=2))
    print(f"[agent] Updated mock scores -> {out}")


def refresh_changelog() -> None:
    changelog = REPO_ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return
    today = date.today().isoformat()
    content = changelog.read_text()
    if today not in content:
        content = content.replace("## [Unreleased]", f"## [Unreleased]\n\n_Last checked: {today}_", 1)
        changelog.write_text(content)
    print("[agent] Refreshed CHANGELOG timestamp")


if __name__ == "__main__":
    print(f"[agent] Starting nightly agent - {date.today().isoformat()}")
    update_benchmark_snapshot()
    compute_mock_scores()
    refresh_changelog()
    print("[agent] Done.")