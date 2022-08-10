import pytest

from peace_performance_python.prelude import Beatmap, Calculator

from . import (
    join_beatmap,
    HITORIGOTO,
    BLUE_ZENITH_MANIA,
)


def _gb(file: str) -> Beatmap:
    return Beatmap(join_beatmap(file))


@pytest.mark.mania_pp
def test_blue_zenith() -> None:
    b = _gb(BLUE_ZENITH_MANIA)

    pp_ss = Calculator().calculate(b).pp

    pp_95 = Calculator(score=950000).calculate(b).pp
    assert pp_95 < pp_ss


@pytest.mark.mania_pp
def test_std_hitorigoto_convert_mania() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator(mode=3).calculate(b).pp

    pp_95 = Calculator(mode=3, score=950000).calculate(b).pp
    assert pp_95 < pp_ss
