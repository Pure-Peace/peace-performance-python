import asyncio
import pytest

from peace_performance_python.objects import Beatmap
from peace_performance_python.functions import (
    raw_read_beatmap_async_rs,
    raw_read_beatmap_async_py,
    raw_read_beatmap_sync
)

from . import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
path = join_beatmap(HITORIGOTO)


# Rust async
@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_async_rs_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap.create_async_rs(path))
    benchmark(wrap)


@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_async_rs_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap_async_rs(path))
    benchmark(wrap)


# Python async
@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_async_py_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap.create_async_py(path))
    benchmark(wrap)


@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_async_py_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap_async_py(path))
    benchmark(wrap)


# Sync
@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_sync_read_beatmap(benchmark) -> None:
    def wrap(): Beatmap.create(path)
    benchmark(wrap)


@pytest.mark.benchmark(group="async-vs-sync-beatmap")
def test_sync_raw_read_beatmap(benchmark) -> None:
    def wrap(): raw_read_beatmap_sync(path)
    benchmark(wrap)
