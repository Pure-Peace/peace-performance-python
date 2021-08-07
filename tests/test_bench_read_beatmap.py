import asyncio
from peace_performance_python.beatmap import Beatmap

from config import join_beatmap, HITORIGOTO


loop = asyncio.get_event_loop()
path = join_beatmap(HITORIGOTO)


def test_async_read_beatmap(benchmark) -> None:
    def wrap(): loop.run_until_complete(Beatmap(path))
    benchmark(wrap)
