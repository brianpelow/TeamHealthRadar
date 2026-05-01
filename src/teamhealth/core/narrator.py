"""AI-powered team health narrative generation."""

from __future__ import annotations

import os
from teamhealth.models.metrics import TeamScore


def generate_narrative(score: TeamScore, industry: str = "fintech") -> str:
    """Generate a weekly team health narrative using Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _fallback_narrative(score, industry)

    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        prompt = f"""You are an engineering director writing a weekly team health summary for a {industry} engineering team.

Team: {score.team}
Overall health score: {score.score}/100 ({score.band} band)
DORA score: {score.dora_score}/100
SPACE score: {score.space_score}/100
Trend: {score.trend}

DORA metrics:
- Deployment frequency: {score.dora.deployment_frequency:.2f}/day ({score.dora.deployment_band} band)
- Lead time for changes: {score.dora.lead_time_hours:.1f} hours ({score.dora.lead_time_band} band)
- Change failure rate: {score.dora.change_failure_rate:.1f}% ({score.dora.failure_rate_band} band)
- MTTR: {score.dora.mttr_hours:.1f} hours ({score.dora.mttr_band} band)

SPACE metrics:
- Satisfaction: {score.space.satisfaction_score:.0f}/100
- PR throughput: {score.space.pr_throughput} PRs merged
- Review turnaround: {score.space.review_turnaround_hours:.1f} hours
- Cycle time: {score.space.cycle_time_hours:.1f} hours
- WIP count: {score.space.wip_count}

Write a 3-paragraph executive summary that:
1. States the overall health status and what is going well
2. Identifies the 1-2 most important areas for improvement with specific data points
3. Recommends concrete next steps appropriate for a {industry} regulated engineering team

Be specific, data-driven, and actionable. Avoid generic platitudes."""

        message = client.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.choices[0].message.content

    except Exception:
        return _fallback_narrative(score, industry)


def _fallback_narrative(score: TeamScore, industry: str) -> str:
    status = {
        "elite": "excellent",
        "high": "strong",
        "medium": "moderate",
        "low": "needs attention",
    }.get(score.band, "moderate")

    return f"""## {score.team} â€” Weekly Health Summary

**Overall status**: {status.title()} ({score.score}/100)

The team is performing at a **{score.band}** level this period with a composite score of {score.score}/100. DORA metrics scored {score.dora_score}/100 and SPACE signals scored {score.space_score}/100. Deployment frequency is {score.dora.deployment_frequency:.2f} deployments/day with a lead time of {score.dora.lead_time_hours:.1f} hours.

The primary area for improvement is {"lead time for changes" if score.dora.lead_time_band in ("medium", "low") else "change failure rate" if score.dora.failure_rate_band in ("medium", "low") else "deployment frequency"}. The team should focus on reducing cycle time (currently {score.space.cycle_time_hours:.1f} hours) and maintaining the current deployment cadence.

**Recommended actions**: Review WIP limits (currently {score.space.wip_count} items), invest in automated testing to reduce change failure rate ({score.dora.change_failure_rate:.1f}%), and ensure runbooks are current per {industry} compliance requirements.
"""