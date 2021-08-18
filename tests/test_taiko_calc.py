from peace_performance_python.objects.calculator import Calculator
from peace_performance_python.objects.beatmap import Beatmap
import pytest
from typing import Callable

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
    assert pp_ss == 551.592041015625

    pp_95 = Calculator(acc=95).calculate(b).pp
    assert pp_95 == 448.6329040527344


@pytest.mark.taiko_pp
def test_std_hitorigoto_convert_taiko() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator(mode=1).calculate(b).pp
    assert pp_ss == 112.30728149414062

    pp_95 = Calculator(mode=1, acc=95).calculate(b).pp
    assert pp_95 == 58.653507232666016
