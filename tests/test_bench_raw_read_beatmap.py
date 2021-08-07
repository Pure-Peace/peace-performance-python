import asyncio
from peace_performance_python.beatmap import raw_read_beatmap

from . import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
path = join_beatmap(HITORIGOTO)


def test_async_raw_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(raw_read_beatmap(path))
    benchmark(wrap)
