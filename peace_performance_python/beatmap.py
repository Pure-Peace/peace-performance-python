from typing import Any
from ._peace_performance import pp as _p

from .common import asyncinit


@asyncinit
class Beatmap:
    async def __init__(self, osu_file_path: str) -> 'Beatmap':
        self._b = await raw_read_beatmap(osu_file_path)


async def raw_read_beatmap(osu_file_path: str) -> Any:
    '''
    Read and parse .osu files from local
    '''
    return await _p.read_beatmap(osu_file_path)
