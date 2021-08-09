from .types import NativeBeatmap

from ._peace_performance import pp as _pp_rust

from typing import Optional
from pathlib import Path


class Beatmap:
    '''
    The Beatmap used to calculate the pp, it contains the parsed .osu beatmap.

    ### Examples:
    ```
    # Read and parse .osu files from local
    beatmap = Beatmap('path_to_osu_file')
    # Same as
    beatmap = Beatmap.create('path_to_osu_file')

    # Async Rust
    beatmap = await Beatmap.create_async_rs('path_to_osu_file')
    # Async Python (wrapper)
    beatmap = await Beatmap.create_async_py('path_to_osu_file')



    # We can reload this .osu files as:
    beatmap.reload()

    # Async Rust
    await beatmap.reload_async_rs()
    # Async Python (wrapper)
    await beatmap.reload_async_py()

    # We can load another .osu files as:
    beatmap.init('path_to_another_osu_file')

    # Async Rust
    await beatmap.init_rs('path_to_another_osu_file')
    # Async Python (wrapper)
    await beatmap.init_py('path_to_another_osu_file')

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
    path: Optional[Path]

    def __init__(self, osu_file_path: Path) -> None:
        '''Init with .osu files'''
        self.path = osu_file_path
        self.reload()

    def __repr__(self) -> str:
        return f'<Beatmap object (path: {self.path}, is_initialized: {self.is_initialized})>'

    # Sync ------------
    def init(self, osu_file_path: Path) -> 'Beatmap':
        '''Load the .osu files with path'''
        self.path = osu_file_path
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    def reload(self) -> 'Beatmap':
        '''Reload this .osu files'''
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Create Beatmap with .osu files'''
        obj = cls(osu_file_path)
        obj.init(osu_file_path)
        return obj

    # Real Rust Async ------------
    # *May have performance issues: Rust future -> Python coroutine
    async def init_async_rs(self, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Real Rust Async

        ### *May have performance issues: Rust future -> Python coroutine 

        Load the .osu files with path
        '''
        self.path = osu_file_path
        self._raw = await _pp_rust.read_beatmap_async(self.path)
        return self

    async def reload_async_rs(self) -> 'Beatmap':
        '''
        ### Real Rust Async

        ### *May have performance issues: Rust future -> Python coroutine 

        Reload this .osu files'''
        self._raw = await _pp_rust.read_beatmap_async(self.path)
        return self

    @classmethod
    async def create_async_rs(cls, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Real Rust Async

        ### *May have performance issues: Rust future -> Python coroutine 

        Create Beatmap with .osu files'''
        obj: 'Beatmap' = cls.__new__(cls)
        obj.path = osu_file_path
        obj._raw = await _pp_rust.read_beatmap_async(obj.path)
        return obj

    # Python Async wrapper ------------
    async def init_async_py(self, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Load the .osu files with path'''
        self.path = osu_file_path
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    async def reload_async_py(self) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Reload this .osu files'''
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    async def create_async_py(cls, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Create Beatmap with .osu files'''
        obj: 'Beatmap' = cls.__new__(cls)
        obj.path = osu_file_path
        obj._raw = _pp_rust.read_beatmap_sync(obj.path)
        return obj

    # Properties ------------
    @property
    def is_initialized(self) -> bool:
        '''Returns whether the beatmap (.osu files) has been loaded and parsed'''
        return (self._raw and self.path) is not None


class AsyncBeatmapRust(Beatmap):
    '''
    Beatmap using Rust asynchronous methods by default

    ### *May have performance issues: Rust future -> Python coroutine 
    ### *Only available when the asynchronous features (`async_tokio`, `async_std`) is enabled.

    ## Examples:
    ```
    beatmap = await AsyncBeatmapRust('path_to_osu_files')
    # or
    beatmap = await AsyncBeatmapRust.crate('path_to_osu_files')
    ```
    '''

    def __init__(self, osu_file_path: Path) -> None:
        '''Init with .osu files'''
        self.path = osu_file_path

    def __await__(self):
        return self.reload().__await__()

    async def init(self, osu_file_path: Path) -> 'Beatmap':
        '''Async load the .osu files with path'''
        self.path = osu_file_path
        self._raw = await _pp_rust.read_beatmap_async(self.path)
        return self

    async def reload(self) -> 'Beatmap':
        '''Async reload this .osu files'''
        self._raw = await _pp_rust.read_beatmap_async(self.path)
        return self

    @classmethod
    async def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Async create Beatmap with .osu files'''
        obj = cls(osu_file_path)
        obj.path = osu_file_path
        obj._raw = await _pp_rust.read_beatmap_async(obj.path)
        return obj


class AsyncBeatmapPython(Beatmap):
    '''
    Beatmap using Python asynchronous methods by default

    ## Examples:
    ```
    beatmap = await AsyncBeatmapRust('path_to_osu_files')
    # or
    beatmap = await AsyncBeatmapRust.crate('path_to_osu_files')
    ```
    '''

    def __init__(self, osu_file_path: Path) -> None:
        '''Init with .osu files'''
        self.path = osu_file_path

    def __await__(self):
        return self.reload().__await__()

    async def init(self, osu_file_path: Path) -> 'Beatmap':
        '''Async load the .osu files with path'''
        self.path = osu_file_path
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    async def reload(self) -> 'Beatmap':
        '''Async reload this .osu files'''
        self._raw = _pp_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    async def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Async create Beatmap with .osu files'''
        obj = cls(osu_file_path)
        obj.path = osu_file_path
        obj._raw = _pp_rust.read_beatmap_sync(obj.path)
        return obj


def raw_read_beatmap_sync(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Sync
    Read and parse .osu files from local, returns native beatmap object
    '''
    return _pp_rust.read_beatmap_sync(osu_file_path)


async def raw_read_beatmap_async_rs(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Real Rust Async
    Read and parse .osu files from local, returns native beatmap object

    ### *May have performance issues: Rust future -> Python coroutine 
    ### *Only available when the asynchronous features (`async_tokio`, `async_std`) is enabled.
    '''
    return await _pp_rust.read_beatmap_async(osu_file_path)


async def raw_read_beatmap_async_py(osu_file_path: Path) -> NativeBeatmap:
    '''
    ### Python Async Wrapper
    Read and parse .osu files from local, returns native beatmap object
    '''
    return _pp_rust.read_beatmap_sync(osu_file_path)
