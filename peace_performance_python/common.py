from .types import OsuModeInt, OsuModeStr
from ._peace_performance import common as _c

from typing import Any, Dict, Iterable


async def rust_sleep(seconds: int) -> None:
    '''Async sleep (rust).'''
    return await _c.rust_sleep(seconds)


def set_log_level(level: str) -> None:
    '''
    Sets the internal log level.

    ### Levels: `['error', 'warning', 'info', 'debug', 'trace']`

    trace levels log all internal timings.
    '''
    _c.set_log_level(level)


def init_logger() -> None:
    '''
    Initialises the logger for the rust lib, this can only be called once.

    ### No logs will be displayed without calling this first however once called
    the level can no-longer be adjusted.
    '''
    _c.init_logger()


def get_attrs_str(target: object, attrs: Iterable[str]) -> str:
    '''Get object attrs as str'''
    return ', '.join((f'{attr}: {getattr(target, attr)}' for attr in attrs))


def get_attrs_dict(target: object, attrs: Iterable[str]) -> Dict[str, Any]:
    '''Get object attrs as dict'''
    def _getattr(target, attr):
        val = getattr(target, attr)
        dic = getattr(val, 'attrs_dict', None)
        return dic if dic else val
    return {attr: _getattr(target, attr) for attr in attrs}


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
