from typing import Optional


from .types import (
    OsuModeInt,
    OsuModeStr,
)


def set_log_level(log_level: str) -> None:
    '''
    Sets the internal log level.

    ### Available only when feature `rust_logger` is enabled. (Default disabled)

    Levels: `['error', 'warning', 'info', 'debug', 'trace']`

    trace levels log all internal timings.
    '''
    ...


def init_logger() -> None:
    '''
    Initialises the logger for the rust lib, this can only be called once.

    ### Available only when feature `rust_logger` is enabled. (Default disabled)

    No logs will be displayed without calling this first however once called
    the level can no-longer be adjusted.
    '''
    ...


async def rust_sleep(secs: int) -> None:
    '''
    Async sleep (rust).

    ### Available only when feature `async_tokio` / `async_std` is enabled. (Default enabled)
    '''
    ...


def osu_mode_str(mode: OsuModeInt) -> Optional[OsuModeStr]:
    '''Get osu! Mode str with mode int'''
    ...


def osu_mode_int(mode: OsuModeStr) -> Optional[OsuModeInt]:
    '''Get osu! Mode int with mode str'''
    ...
