import pytest

from peace_performance_python.prelude import Beatmap, Calculator

from . import (
    join_beatmap,
    HITORIGOTO
)


def _gb(file: str) -> Beatmap:
    return Beatmap(join_beatmap(file))


@pytest.mark.std_pp
def test_hitorigoto() -> None:
    b = _gb(HITORIGOTO)

    pp_ss = Calculator().calculate(b).pp
    assert pp_ss == 183.6759796142578

    pp_95 = Calculator(acc=95).calculate(b).pp
    assert pp_95 == 122.74517822265625
