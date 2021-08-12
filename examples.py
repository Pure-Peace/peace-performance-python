import asyncio

# import all
from peace_performance_python.prelude import *
# or
# from peace_performance_python.objects import Beatmap, Calculator

from tests import join_beatmap, HITORIGOTO, UNFORGIVING


# Initialize Rust logger (optional)
set_log_level('trace')
init_logger()


# Choose a style you like
def calculate(beatmap: Beatmap, calculator: Calculator) -> CalcResult:
    return calculator.calculate(beatmap)


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
    return calculate(beatmap, c)


def calculate_3(beatmap: Beatmap) -> CalcResult:
    c = Calculator()
    c.set_with_dict({'acc': 98.8, 'miss': 3})
    return calculate(beatmap, c)


def calculate_4(beatmap: Beatmap) -> CalcResult:
    return Calculator({'acc': 98.8, 'miss': 3}).calculate(beatmap)


def calculate_5(beatmap: Beatmap) -> CalcResult:
    return Calculator(acc=98.8, miss=3).calculate(beatmap)


async def main() -> None:
    path = join_beatmap(HITORIGOTO)
    # Load beatmap
    beatmap = Beatmap(path)
    # beatmap = Beatmap.create(path)

    # Async
    # beatmap = await Beatmap.create_async_rs(path)
    # beatmap = await Beatmap.create_async_py(path)
    # or
    # beatmap = await AsyncBeatmapRust(path)
    # beatmap = await AsyncBeatmapPython(path)
    print('\n**** Beatmap:', beatmap)

    # Calculate pp
    # result = calculate_5(beatmap)
    c = Calculator(acc=98.8, miss=3)
    print('\n***** Calculator as dict:', c.attrs_dict)
    result = c.calculate(beatmap)

    # Print results
    # print('\n***** result:', result)
    print('\n***** result.pp:', result.pp)
    print('\n***** result as dict:', result.attrs_dict)
    # print('\n***** result.raw_stars as dict:', result.raw_stars.attrs_dict)
    # print('\n***** result.raw_pp as dict:', result.raw_pp.attrs_dict)

    # Reset calculator
    c.reset()
    print('\n***** reseted Calculator as dict:', c.attrs_dict)

    # Calc again
    result2 = c.calculate(beatmap)
    print('\n***** result2 as dict:', result2)

    # Load another .osu files
    path2 = join_beatmap(UNFORGIVING)
    beatmap.init(path2)
    print(beatmap)


if __name__ == '__main__':
    asyncio.run(main())
