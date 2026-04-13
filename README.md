# TeamHealthRadar

> Engineering team health scoring — DORA metrics, SPACE framework signals, and AI-synthesized insights.

![CI](https://github.com/brianpelow/TeamHealthRadar/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)

## Overview

`TeamHealthRadar` is a FastAPI service that continuously scores engineering
team health by combining DORA delivery metrics, SPACE framework signals, and
AI-synthesized narratives. It gives engineering leaders a weekly, data-driven
view of team performance without relying on subjective pulse surveys alone.

Built for engineering leaders in regulated financial services and manufacturing
where team performance data feeds into capacity planning, audit evidence, and
executive reporting.

## API endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Service health check |
| `GET /teams` | List all tracked teams |
| `GET /teams/{team}/score` | Current health score for a team |
| `GET /teams/{team}/metrics` | DORA + SPACE metrics breakdown |
| `GET /teams/{team}/narrative` | AI-synthesized weekly health narrative |
| `GET /benchmarks` | DORA elite/high/medium/low band definitions |

## Metrics tracked

### DORA
- Deployment frequency
- Lead time for changes
- Change failure rate
- Mean time to restore

### SPACE
- Satisfaction signals (PR review sentiment)
- Performance (throughput, quality)
- Activity (commits, reviews, deployments)
- Communication (PR turnaround, comment density)
- Efficiency (cycle time, WIP limits)

## Quick start

```bash
pip install TeamHealthRadar

export GITHUB_TOKEN=your_token
export JIRA_URL=https://your-org.atlassian.net
export JIRA_TOKEN=your_token

team-health-radar
# API available at http://localhost:8000
```

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub API token | No |
| `JIRA_URL` | JIRA instance URL | No |
| `JIRA_TOKEN` | JIRA API token | No |
| `ANTHROPIC_API_KEY` | For AI narratives | No |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — see [LICENSE](LICENSE).