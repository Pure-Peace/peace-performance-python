import asyncio

import pytest
from peace_performance_python.prelude import *

from config import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
beatmap: Beatmap = loop.run_until_complete(Beatmap.create(
    join_beatmap(HITORIGOTO)))


@pytest.mark.benchmark(group="bench-pp-calc")
def test_calculate_1(benchmark) -> CalcResult:
    def wrap(): calculate_pp(beatmap, Calculator({'acc': 98.8, 'miss': 3}))
    benchmark(wrap)


@pytest.mark.benchmark(group="bench-pp-calc")
def test_calculate_2(benchmark) -> CalcResult:
    def wrap():
        # --
        c = Calculator()
        # c.set_acc(98.8)
        # c.set_miss(3)

        # or
        c.acc = 98.8
        c.miss = 3

        # or
        # c.setattr('acc', 98.8)
        # c.setattr('miss', 3)
        calculate_pp(beatmap, c)
    benchmark(wrap)


@pytest.mark.benchmark(group="bench-pp-calc")
def test_calculate_3(benchmark) -> CalcResult:
    def wrap():
        c = Calculator()
        c.set_with_dict({'acc': 98.8, 'miss': 3})
        calculate_pp(beatmap, c)
    benchmark(wrap)


@pytest.mark.benchmark(group="bench-pp-calc")
def test_calculate_4(benchmark) -> CalcResult:
    def wrap(): Calculator({'acc': 98.8, 'miss': 3}).calculate(beatmap)
    benchmark(wrap)


@pytest.mark.benchmark(group="bench-pp-calc")
def test_calculate_5(benchmark) -> CalcResult:
    def wrap(): Calculator(acc=98.8, miss=3).calculate(beatmap)
    benchmark(wrap)
