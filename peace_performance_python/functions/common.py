from ..types import NativeBeatmap, OsuModeInt, OsuModeStr, NativeCalculator

from .._peace_performance import common as _common
from .._peace_performance import beatmap as _beatmap_rust
from .._peace_performance import pp as _pp_rust


from pathlib import Path


async def rust_sleep(seconds: int) -> None:
    '''Async sleep (rust).'''
    return await _common.rust_sleep(seconds)


def set_log_level(level: str) -> None:
    '''
    Sets the internal log level.

    ### Levels: `['error', 'warning', 'info', 'debug', 'trace']`

    trace levels log all internal timings.
    '''
    _common.set_log_level(level)


def init_logger() -> None:
    '''
    Initialises the logger for the rust lib, this can only be called once.

    ### No logs will be displayed without calling this first however once called
    the level can no-longer be adjusted.
    '''
    _common.init_logger()


def osu_mode_str(mode: OsuModeInt) -> OsuModeStr:
    '''Get osu! Mode str with mode int'''
    if mode == 0:
        return 'osu'
    if mode == 1:
        return 'taiko'
    if mode == 2:
        return 'ctb'
    if mode == 3:
        return 'mania'


def osu_mode_int(mode: OsuModeStr) -> OsuModeInt:
    '''Get osu! Mode int with mode str'''
    if mode == 'osu':
        return 0
    if mode == 'taiko':
        return 1
    if mode == 'ctb':
        return 2
    if mode == 'mania':
        return 3


def raw_read_beatmap_sync(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Sync
    Read and parse .osu files from local, returns native beatmap object
    '''
    return _beatmap_rust.read_beatmap_sync(osu_file_path)


async def raw_read_beatmap_async_rs(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Real Rust Async
    Read and parse .osu files from local, returns native beatmap object

    ### *May have performance issues: Rust future -> Python coroutine 
    ### *Only available when the asynchronous features (`async_tokio`, `async_std`) is enabled.
    '''
    return await _beatmap_rust.read_beatmap_async(osu_file_path)


async def raw_read_beatmap_async_py(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Python Async Wrapper
    Read and parse .osu files from local, returns native beatmap object
    '''
    return _beatmap_rust.read_beatmap_sync(osu_file_path)


def raw_calculator() -> NativeCalculator:
    '''Create new native calculator'''
    return _pp_rust.new_calculator()
