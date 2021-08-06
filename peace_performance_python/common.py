from ._peace_performance import common as _c


async def rust_sleep(seconds: int) -> None:
    '''
    Async sleep (rust)
    '''
    return await _c.rust_sleep(seconds)


def set_log_level(level: str) -> None:
    '''
    Sets the internal log level.

    Levels: [error, warning, info, debug, trace]

    trace levels log all internal timings.
    '''
    _c.set_log_level(level)


def init_logger() -> None:
    '''
    Initialises the logger for the rust lib, this can only be called once.

    No logs will be displayed without calling this first however once called
    the level can no-longer be adjusted.
    '''
    _c.init_logger()


def asyncinit(cls):
    '''
    Async init decorator
    '''
    __new__ = cls.__new__

    async def init(obj, *arg, **kwarg):
        await obj.__init__(*arg, **kwarg)
        return obj

    def new(cls, *arg, **kwarg):
        print(1)
        obj = __new__(cls, *arg, **kwarg)
        coro = init(obj, *arg, **kwarg)
        return coro

    cls.__new__ = new
    return cls
