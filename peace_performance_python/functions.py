from ._peace_performance import functions as _fn


async def rust_sleep(seconds: int) -> None:
    return await _fn.rust_sleep(seconds)


def set_log_level(level: str) -> None:
    """
    Sets the internal server log level.

    Levels: [error, warning, info, debug, trace]

    trace levels log all internal server timings.
    """
    _fn.set_log_level(level)


def init_logger() -> None:
    """
    Initialises the logger for the server, this can only be called once.

    No logs will be displayed without calling this first however once called
    the level can no-longer be adjusted.
    """
    _fn.init_logger()
