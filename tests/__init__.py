import asyncio
from peace_performance_python import Beatmap
from .oppai_wrapper import OppaiWrapper

from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

BEATMAP_DIR = r'./test_beatmaps/'

# Test beatmaps
# std
PADORU = r'padoru.osu'  # super short - 5kb
HITORIGOTO = r'hitorigoto.osu'  # short - 15kb
FREEDOM_DIVE = r'freedom_dive.osu'  # stream medium - 50kb
SOTARKS = r'sotarks.osu'  # jump medium - 68kb
GALAXY_BURST = r'galaxy_burst.osu'  # tech - 102kb
UNFORGIVING = r'unforgiving.osu'  # marathon - 238kb
# taiko
THE_BIG_BLACK_TAIKO = r'the_big_black_taiko.osu'  # 35kb
# fruits
MEI_FRUITS = r'mei_fruits.osu'  # 107kb
# mania
BLUE_ZENITH_MANIA = r'blue_zenith_mania.osu'  # 16 stars - 244kb


def join_beatmap(beatmap: str) -> str:
    return BEATMAP_DIR + beatmap


def async_run(future):
    try:
        return asyncio.run(future)
    except AttributeError:
        # For <= python3.6
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(asyncio.wait([future]))


def read_beatmap(path: str, loop: Optional['AbstractEventLoop'] = None) -> Callable[[None], None]:
    p = join_beatmap(path)

    def wrapper_async() -> None:
        loop.run_until_complete(Beatmap.create_async_rs(p))

    def wrapper_sync() -> None:
        Beatmap.create(p)
    return wrapper_async if loop else wrapper_sync
