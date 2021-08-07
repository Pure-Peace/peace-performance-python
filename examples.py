import asyncio
import time

# import all
from peace_performance_python.prelude import *
# or
# from peace_performance_python.beatmap import Beatmap
# from peace_performance_python.calculator import Calculator

from tests.config import join_beatmap, TEST_BEATMAP_FILE

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Initial Rust logger (optional)
set_log_level('trace')
init_logger()


# Choose a style you like
def calculate_1(beatmap: Beatmap) -> CalcResult:
    return calculate_pp(beatmap, Calculator({'acc': 98.8, 'miss': 3}))


def calculate_2(beatmap: Beatmap) -> CalcResult:
    # --
    c = Calculator()
    c.set_acc(98.8)
    c.set_miss(3)

    # or
    # c.acc = 98.8
    # c.miss = 3

    # or
    # c.setattr('acc', 98.8)
    # c.setattr('miss', 3)
    return calculate_pp(beatmap, c)


def calculate_3(beatmap: Beatmap) -> CalcResult:
    c = Calculator()
    c.set_with_dict({'acc': 98.8, 'miss': 3})
    return calculate_pp(beatmap, c)


def calculate_4(beatmap: Beatmap) -> CalcResult:
    return Calculator({'acc': 98.8, 'miss': 3}).calculate(beatmap)


def calculate_5(beatmap: Beatmap) -> CalcResult:
    return Calculator(acc=98.8, miss=3).calculate(beatmap)


async def main():
    path = join_beatmap(TEST_BEATMAP_FILE)
    # Load beatmap
    beatmap = await Beatmap.create(path)
    # Calculate pp
    result = calculate_5(beatmap)
    print(result.attrs_dict)

if __name__ == '__main__':
    asyncio.run(main())
