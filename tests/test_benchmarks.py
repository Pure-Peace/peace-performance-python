import asyncio

from peace_performance_python.wrapper import read_beatmap

from config import join_beatmap

loop = asyncio.get_event_loop()


def do_read_beatmap():
    loop.run_until_complete(read_beatmap(
        join_beatmap('eae63c5e82313da9c08f7565f6b6505b.osu')))


def test_bench_async_read_beatmap(benchmark) -> None:
    benchmark(do_read_beatmap)
