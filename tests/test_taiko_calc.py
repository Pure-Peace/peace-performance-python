import pytest

from peace_performance_python.prelude import Beatmap, Calculator

from . import (
    join_beatmap,
    HITORIGOTO,
    THE_BIG_BLACK_TAIKO,
)


def _gb(file: str) -> Beatmap:
    return Beatmap(join_beatmap(file))


@pytest.mark.taiko_pp
def test_the_big_black() -> None:
    b = _gb(THE_BIG_BLACK_TAIKO)

    pp_ss = Calculator().calculate(b).pp

    pp_95 = Calculator(acc=95).calculate(b).pp
    assert pp_95 < pp_ss


@pytest.mark.taiko_pp
def test_std_hitorigoto_convert_taiko() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator(mode=1).calculate(b).pp

    pp_95 = Calculator(mode=1, acc=95).calculate(b).pp
    assert pp_95 < pp_ss
