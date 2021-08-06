import asyncio

from peace_performance_python.beatmap import raw_read_beatmap

from config import join_beatmap, TEST_BEATMAP_FILE

loop = asyncio.get_event_loop()


def do_read_beatmap():
    loop.run_until_complete(raw_read_beatmap(
        join_beatmap(TEST_BEATMAP_FILE)))


def test_bench_async_read_beatmap(benchmark) -> None:
    benchmark(do_read_beatmap)
