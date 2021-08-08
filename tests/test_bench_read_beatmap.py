import asyncio
from peace_performance_python.beatmap import Beatmap, raw_read_beatmap_async, raw_read_beatmap_sync

from . import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
path = join_beatmap(HITORIGOTO)


def test_async_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap(path))
    benchmark(wrap)


def test_async_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap_async(path))
    benchmark(wrap)


def test_sync_read_beatmap(benchmark) -> None:
    def wrap(): Beatmap.create_sync(path)
    benchmark(wrap)


def test_sync_raw_read_beatmap(benchmark) -> None:
    def wrap(): raw_read_beatmap_sync(path)
    benchmark(wrap)
