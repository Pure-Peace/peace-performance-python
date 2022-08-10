import pytest
from peace_performance_python.objects.utils import Mods

from peace_performance_python.prelude import Beatmap, Calculator

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

    pp_95 = Calculator(acc=95).calculate(b).pp
    assert pp_95 < pp_ss
    
    pp_hdhr = Calculator(mods=Mods.HARDROCK | Mods.HIDDEN).calculate(b).pp
    assert pp_hdhr > pp_ss


@pytest.mark.fruits_pp
def test_std_hitorigoto_convert_fruits() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator(mode=2).calculate(b).pp

    pp_95 = Calculator(mode=2, acc=95).calculate(b).pp
    assert pp_95 < pp_ss
    
    pp_hdhr = Calculator(mods=Mods.HARDROCK | Mods.HIDDEN).calculate(b).pp
    assert pp_hdhr > pp_ss
