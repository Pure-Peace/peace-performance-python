import asyncio
import time

from peace_performance_python.functions import init_logger, set_log_level
from peace_performance_python.wrapper import read_beatmap, Wrapper

from tests.config import join_beatmap

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

set_log_level('debug')
init_logger()


async def main():
    await read_beatmap(join_beatmap('eae63c5e82313da9c08f7565f6b6505b.osu'))
    a = Wrapper('gg')


if __name__ == '__main__':
    asyncio.run(main())
