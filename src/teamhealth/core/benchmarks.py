"""DORA benchmark band definitions."""

from __future__ import annotations

from pydantic import BaseModel


class BandDefinition(BaseModel):
    """Definition of a DORA performance band."""

    name: str
    deployment_frequency: str
    lead_time: str
    change_failure_rate: str
    mttr: str
    description: str


DORA_BANDS: list[BandDefinition] = [
    BandDefinition(
        name="elite",
        deployment_frequency="On-demand (multiple per day)",
        lead_time="Less than 1 hour",
        change_failure_rate="0-5%",
        mttr="Less than 1 hour",
        description="Top performers. Continuous delivery with high automation and confidence.",
    ),
    BandDefinition(
        name="high",
        deployment_frequency="Between once per day and once per week",
        lead_time="Between 1 day and 1 week",
        change_failure_rate="5-10%",
        mttr="Less than 1 day",
        description="Strong performers with mature delivery practices.",
    ),
    BandDefinition(
        name="medium",
        deployment_frequency="Between once per week and once per month",
        lead_time="Between 1 week and 1 month",
        change_failure_rate="10-15%",
        mttr="Between 1 day and 1 week",
        description="Developing teams with room to improve automation and deployment practices.",
    ),
    BandDefinition(
        name="low",
        deployment_frequency="Less than once per month",
        lead_time="More than 6 months",
        change_failure_rate="46-60%",
        mttr="More than 1 week",
        description="Early-stage delivery maturity. Significant investment needed.",
    ),
]


def get_band(name: str) -> BandDefinition | None:
    return next((b for b in DORA_BANDS if b.name == name), None)


def get_all_bands() -> list[BandDefinition]:
    return DORA_BANDS