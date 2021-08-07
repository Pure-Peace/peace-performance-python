import asyncio
import pytest

from peace_performance_python.beatmap import Beatmap

from config import read_beatmap as _rd, \
    PADORU, \
    HITORIGOTO, \
    FREEDOM_DIVE, \
    SOTARKS, \
    GALAXY_BURST, \
    UNFORGIVING

loop = asyncio.get_event_loop()


def read_beatmap(path):
    return _rd(path, loop)


@pytest.mark.benchmark(group="bench-beatmap")
def test_padoru(benchmark) -> None:
    benchmark(read_beatmap(PADORU))


@pytest.mark.benchmark(group="bench-beatmap")
def test_hitorigoto(benchmark) -> None:
    benchmark(read_beatmap(HITORIGOTO))


@pytest.mark.benchmark(group="bench-beatmap")
def test_freedom_dive(benchmark) -> None:
    benchmark(read_beatmap(FREEDOM_DIVE))


@pytest.mark.benchmark(group="bench-beatmap")
def test_sotarks(benchmark) -> None:
    benchmark(read_beatmap(SOTARKS))


@pytest.mark.benchmark(group="bench-beatmap")
def test_galaxy_burst(benchmark) -> None:
    benchmark(read_beatmap(GALAXY_BURST))


@pytest.mark.benchmark(group="bench-beatmap")
def test_unforgiving(benchmark) -> None:
    benchmark(read_beatmap(UNFORGIVING))
