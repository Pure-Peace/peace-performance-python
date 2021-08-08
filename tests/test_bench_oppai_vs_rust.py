import asyncio
from typing import Callable
import pytest
import sys
import os

from peace_performance_python.prelude import Beatmap, Calculator, calculate_pp

from . import (
    OppaiWrapper,
    join_beatmap,
    PADORU,
    HITORIGOTO,
    FREEDOM_DIVE,
    SOTARKS,
    GALAXY_BURST,
    UNFORGIVING
)


OPPAI_PATH = 'oppai_build/liboppai.so'
loop = asyncio.get_event_loop()


def calc_rust(path) -> Callable[[None], None]:
    p = join_beatmap(path)

    def wrap() -> None:
        beatmap: Beatmap = loop.run_until_complete(Beatmap(p))
        c = Calculator()
        c.set_with_dict({'acc': 98.8, 'miss': 3})
        calculate_pp(beatmap, c)
    return wrap


def calc_oppai(path) -> Callable[[None], None]:
    p = join_beatmap(path)

    def wrap() -> None:
        with OppaiWrapper(OPPAI_PATH) as ezpp:
            ezpp.set_accuracy_percent(98.8)
            ezpp.set_nmiss(3)
            ezpp.calculate(p)
    return wrap


@pytest.mark.skipif(sys.platform == 'win32', reason='Oppai - No windows support!!')
@pytest.mark.skipif(not os.path.exists(OPPAI_PATH), reason='Oppai - Couldn\'t find shared library (.so file)!!')
@pytest.mark.benchmark(group="bench-oppai-vs-rust")
class TestBenchOppaiVsRust:
    # rust ---------
    def test_rust_padoru(self, benchmark) -> None:
        benchmark(calc_rust(PADORU))

    def test_rust_hitorigoto(self, benchmark) -> None:
        benchmark(calc_rust(HITORIGOTO))

    def test_rust_freedom_dive(self, benchmark) -> None:
        benchmark(calc_rust(FREEDOM_DIVE))

    def test_rust_sotarks(self, benchmark) -> None:
        benchmark(calc_rust(SOTARKS))

    def test_rust_galaxy_burst(self, benchmark) -> None:
        benchmark(calc_rust(GALAXY_BURST))

    def test_rust_unforgiving(self, benchmark) -> None:
        benchmark(calc_rust(UNFORGIVING))

    # oppai ---------
    def test_oppai_padoru(self, benchmark) -> None:
        benchmark(calc_oppai(PADORU))

    def test_oppai_hitorigoto(self, benchmark) -> None:
        benchmark(calc_oppai(HITORIGOTO))

    def test_oppai_freedom_dive(self, benchmark) -> None:
        benchmark(calc_oppai(FREEDOM_DIVE))

    def test_oppai_sotarks(self, benchmark) -> None:
        benchmark(calc_oppai(SOTARKS))

    def test_oppai_galaxy_burst(self, benchmark) -> None:
        benchmark(calc_oppai(GALAXY_BURST))

    def test_oppai_unforgiving(self, benchmark) -> None:
        benchmark(calc_oppai(UNFORGIVING))
