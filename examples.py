import asyncio

# import all
from peace_performance_python.prelude import *
# or
# from peace_performance_python.beatmap import Beatmap
# from peace_performance_python.calculator import Calculator

from tests import join_beatmap, HITORIGOTO


# Initialize Rust logger (optional)
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
    c.acc = 98.8
    c.miss = 3

    # or
    c.setattr('acc', 98.8)
    c.setattr('miss', 3)
    return calculate_pp(beatmap, c)


def calculate_3(beatmap: Beatmap) -> CalcResult:
    c = Calculator()
    c.set_with_dict({'acc': 98.8, 'miss': 3})
    return calculate_pp(beatmap, c)


def calculate_4(beatmap: Beatmap) -> CalcResult:
    return Calculator({'acc': 98.8, 'miss': 3}).calculate(beatmap)


def calculate_5(beatmap: Beatmap) -> CalcResult:
    return Calculator(acc=98.8, miss=3).calculate(beatmap)


async def main() -> None:
    path = join_beatmap(HITORIGOTO)
    # Load beatmap
    beatmap = await Beatmap.create(path)
    # Calculate pp
    result = calculate_5(beatmap)
    print('\n***** result:', result)
    print('\n***** result.pp:', result.pp)
    print('\n***** result as dict:', result.attrs_dict)
    print('\n***** result.raw_stars as dict:', result.raw_stars.attrs_dict)
    print('\n***** result.raw_pp as dict:', result.raw_pp.attrs_dict)

if __name__ == '__main__':
    asyncio.run(main())
