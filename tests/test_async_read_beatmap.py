import asyncio

from peace_performance_python.wrapper import read_beatmap

loop = asyncio.get_event_loop()


def test_async_read_beatmap() -> None:
    loop.run_until_complete(read_beatmap(
        r'D:\PurePeace\Desktop\osudev\pp-server\example_data\beatmaps\eae63c5e82313da9c08f7565f6b6505b.osu'))
