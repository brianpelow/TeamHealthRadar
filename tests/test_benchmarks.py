"""Tests for DORA benchmarks."""

from teamhealth.core.benchmarks import get_band, get_all_bands


def test_get_all_bands_returns_four() -> None:
    bands = get_all_bands()
    assert len(bands) == 4


def test_band_names() -> None:
    bands = get_all_bands()
    names = {b.name for b in bands}
    assert names == {"elite", "high", "medium", "low"}


def test_get_band_elite() -> None:
    band = get_band("elite")
    assert band is not None
    assert "multiple per day" in band.deployment_frequency


def test_get_band_unknown() -> None:
    band = get_band("unknown")
    assert band is None


def test_all_bands_have_description() -> None:
    for band in get_all_bands():
        assert len(band.description) > 0