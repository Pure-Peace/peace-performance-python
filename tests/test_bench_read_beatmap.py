import asyncio
from peace_performance_python.beatmap import (
    Beatmap,
    raw_read_beatmap_async_rs,
    raw_read_beatmap_async_py,
    raw_read_beatmap_sync
)

from . import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
path = join_beatmap(HITORIGOTO)


# Rust async
def test_async_rs_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap.create_async_rs(path))
    benchmark(wrap)


def test_async_rs_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap_async_rs(path))
    benchmark(wrap)


# Python async
def test_async_py_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap.create_async_py(path))
    benchmark(wrap)


def test_async_py_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap_async_py(path))
    benchmark(wrap)


# Sync
def test_sync_read_beatmap(benchmark) -> None:
    def wrap(): Beatmap.create(path)
    benchmark(wrap)


def test_sync_raw_read_beatmap(benchmark) -> None:
    def wrap(): raw_read_beatmap_sync(path)
    benchmark(wrap)
