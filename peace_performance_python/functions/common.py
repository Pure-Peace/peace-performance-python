from pathlib import Path


from .._peace_performance.beatmap import (
    Beatmap,
    read_beatmap_sync as raw_read_beatmap_sync,
    read_beatmap_async as raw_read_beatmap_async
)
from .._peace_performance.common import (
    rust_sleep as raw_rust_sleep,
    set_log_level,
    init_logger
)
from .._peace_performance.pp import (
    new_calculator as raw_calculator
)

from ..objects.calculator import Calculator


async def raw_read_beatmap_async_rs(osu_file_path: Path) -> Beatmap:
    '''Read a beatmap async, returns Beatmap object (`Rust`)'''
    return await raw_read_beatmap_async(osu_file_path)


async def raw_read_beatmap_async_py(osu_file_path: Path) -> Beatmap:
    '''
    ### Python Async Wrapper

    Read and parse .osu files from local, returns native beatmap object
    '''
    return raw_read_beatmap_sync(osu_file_path)


def new_calculator() -> Calculator:
    '''Create new Calculator'''
    return Calculator()


async def rust_sleep(secs: int) -> None:
    '''
    Async sleep (rust).

    ### Available only when feature `async_tokio` / `async_std` is enabled.
    '''
    await raw_rust_sleep(secs)
