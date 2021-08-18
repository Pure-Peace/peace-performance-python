from peace_performance_python.objects.calculator import Calculator
from peace_performance_python.objects.beatmap import Beatmap
import pytest
from typing import Callable

from . import (
    join_beatmap,
    HITORIGOTO,
    MEI_FRUITS,
)


def _gb(file: str) -> Beatmap:
    return Beatmap(join_beatmap(file))


@pytest.mark.fruits_pp
def test_mei() -> None:
    b = _gb(MEI_FRUITS)

    pp_ss = Calculator().calculate(b).pp
    assert pp_ss == 1036.869384765625

    pp_95 = Calculator(acc=95).calculate(b).pp
    assert pp_95 == 782.4349975585938


@pytest.mark.fruits_pp
def test_std_hitorigoto_convert_fruits() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator(mode=2).calculate(b).pp
    assert pp_ss == 196.4501495361328

    pp_95 = Calculator(mode=2, acc=95).calculate(b).pp
    assert pp_95 == 148.42703247070312
