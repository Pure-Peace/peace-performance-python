import asyncio
import time

from peace_performance_python.common import init_logger, set_log_level
from peace_performance_python.beatmap import raw_read_beatmap

from tests.config import join_beatmap, TEST_BEATMAP_FILE

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

set_log_level('trace')
init_logger()


async def main():
    raw_beatmap = await raw_read_beatmap(join_beatmap(TEST_BEATMAP_FILE))


if __name__ == '__main__':
    asyncio.run(main())
