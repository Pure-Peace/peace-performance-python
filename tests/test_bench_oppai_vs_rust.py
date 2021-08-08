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

if sys.platform == 'win32':
    raise Exception('Oppai - No windows support!!')

OPPAI_PATH = 'oppai_build/liboppai.so'
if not os.path.exists(OPPAI_PATH):
    raise Exception("Oppai - Couldn't find shared library (.so file)!!")

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


# rust ---------
@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_padoru(benchmark) -> None:
    benchmark(calc_rust(PADORU))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_hitorigoto(benchmark) -> None:
    benchmark(calc_rust(HITORIGOTO))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_freedom_dive(benchmark) -> None:
    benchmark(calc_rust(FREEDOM_DIVE))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_sotarks(benchmark) -> None:
    benchmark(calc_rust(SOTARKS))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_galaxy_burst(benchmark) -> None:
    benchmark(calc_rust(GALAXY_BURST))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_rust_unforgiving(benchmark) -> None:
    benchmark(calc_rust(UNFORGIVING))


# oppai ---------
@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_padoru(benchmark) -> None:
    benchmark(calc_oppai(PADORU))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_hitorigoto(benchmark) -> None:
    benchmark(calc_oppai(HITORIGOTO))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_freedom_dive(benchmark) -> None:
    benchmark(calc_oppai(FREEDOM_DIVE))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_sotarks(benchmark) -> None:
    benchmark(calc_oppai(SOTARKS))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_galaxy_burst(benchmark) -> None:
    benchmark(calc_oppai(GALAXY_BURST))


@pytest.mark.benchmark(group="bench-oppai-vs-rust")
def test_oppai_unforgiving(benchmark) -> None:
    benchmark(calc_oppai(UNFORGIVING))
