# Contributing

## Development setup

```bash
git clone https://github.com/brianpelow/TeamHealthRadar
cd TeamHealthRadar
uv sync
uv run pytest
uv run team-health-radar
```

## Standards

- All PRs require passing CI
- Test coverage must not decrease
- Update CHANGELOG.md for user-facing changes