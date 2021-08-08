from peace_performance_python.beatmap import Beatmap
from .oppai_wrapper import OppaiWrapper

from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

BEATMAP_DIR = r'./test_beatmaps/'

# Test beatmaps
PADORU = r'padoru.osu'  # super short - 5kb
HITORIGOTO = r'hitorigoto.osu'  # short - 15kb
FREEDOM_DIVE = r'freedom_dive.osu'  # stream medium - 50kb
SOTARKS = r'sotarks.osu'  # jump medium - 68kb
GALAXY_BURST = r'galaxy_burst.osu'  # tech - 102kb
UNFORGIVING = r'unforgiving.osu'  # marathon - 238kb


def join_beatmap(beatmap: str) -> str:
    return BEATMAP_DIR + beatmap


def read_beatmap(path: str, loop: Optional['AbstractEventLoop'] = None) -> Callable[[None], None]:
    p = join_beatmap(path)

    def wrapper_async() -> None:
        loop.run_until_complete(Beatmap(p))

    def wrapper_sync() -> None:
        Beatmap.create_sync(p)
    return wrapper_async if loop else wrapper_sync
