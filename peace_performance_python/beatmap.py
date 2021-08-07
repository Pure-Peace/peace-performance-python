from .types import NativeBeatmap

from ._peace_performance import pp as _p

from typing import Optional
from pathlib import Path


class Beatmap:
    '''
    The Beatmap used to calculate the pp, it contains the parsed .osu beatmap.

    ### Examples:
    ```
    # Read and parse .osu files from local
    beatmap = await Beatmap('path_to_osu_file')
    # Same as
    beatmap = await Beatmap.create('path_to_osu_file')

    # We can reload this .osu files as:
    await beatmap
    # or
    await beatmap.reload()

    # We can load another .osu files as:
    await beatmap.async_init('path_to_another_osu_file')

    # Calculate PP
    c = Calculator()
    c.set_acc(98.8)
    c.set_combo(727)
    # or
    c = Calculator({'acc': 98.8, 'combo': 727})
    # then
    result = c.calculate(beatmap)

    ```
    '''
    __slots__ = ('_raw', 'path')

    _raw: Optional[NativeBeatmap]
    path: Path

    def __repr__(self) -> str:
        return f'<Beatmap object ({self.path})>'

    def __init__(self, osu_file_path: Path):
        '''Init async with .osu files'''
        self.path = osu_file_path

    def __await__(self):
        return self.reload(self.path).__await__()

    async def reload(self) -> 'Beatmap':
        '''Reload this .osu files'''
        self._raw = await raw_read_beatmap(self.path)
        return self

    async def async_init(self, osu_file_path: Path) -> 'Beatmap':
        '''Load the .osu files with path'''
        self.path = osu_file_path
        self._raw = await raw_read_beatmap(self.path)
        return self

    @classmethod
    async def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Init async with .osu files'''
        obj = cls(osu_file_path)
        await obj.async_init(osu_file_path)
        return obj

    @property
    def is_initialed(self) -> bool:
        '''Returns whether the beatmap (.osu files) has been loaded and parsed'''
        return bool(self._raw)


async def raw_read_beatmap(osu_file_path: Path) -> NativeBeatmap:
    '''Read and parse .osu files from local, returns native beatmap object'''
    return await _p.read_beatmap(osu_file_path)
