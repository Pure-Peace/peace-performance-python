import asyncio
import time

from peace_performance_python.common import init_logger, set_log_level
from peace_performance_python.beatmap import raw_read_beatmap, Beatmap
from peace_performance_python.calculator import Calculator

from tests.config import join_beatmap, TEST_BEATMAP_FILE

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

set_log_level('trace')
init_logger()


async def main():
    beatmap_path = join_beatmap(TEST_BEATMAP_FILE)
    raw_beatmap = await raw_read_beatmap(beatmap_path)
    print(raw_beatmap)
    wrapped_beatmap = await Beatmap.create(beatmap_path)
    print(wrapped_beatmap.is_initialed)
    calc = Calculator()
    calc.set_n100(66)
    print(calc.n100)
    calc.del_n100()
    print(calc.n100, calc.get_n100())

if __name__ == '__main__':
    asyncio.run(main())
