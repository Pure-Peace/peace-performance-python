import asyncio

from peace_performance_python.beatmap import raw_read_beatmap

from config import join_beatmap, TEST_BEATMAP_FILE


loop = asyncio.get_event_loop()


def test_async_read_beatmap() -> None:
    raw_beatmap = loop.run_until_complete(raw_read_beatmap(
        join_beatmap(TEST_BEATMAP_FILE)))
