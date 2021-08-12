from .parsing import DifficultyPoint, HitObject, TimingPoint
from ..utils import _read_only_property_generator
from ..types import NativeBeatmap

from .._peace_performance import beatmap as _beatmap_rust


from typing import Dict, List, Optional
from pathlib import Path


@_read_only_property_generator
class Beatmap:
    '''
    The Beatmap used to calculate the pp, it contains the parsed .osu beatmap.

    `path`: `Optional[Path]`

    `mode`: `int`

    `mode_str`: `str`

    `version`: `int`

    `n_circles`: `int`

    `n_sliders`: `int`

    `n_spinners`: `int`

    `ar`: `float`

    `od`: `float`

    `cs`: `float`

    `hp`: `float`

    `sv`: `float`

    `tick_rate`: `float`

    `stack_leniency`: `Optional[float]`

    `hit_objects`: `Optional[List[HitObject]]`

    `timing_points`: `Optional[List[TimingPoint]]`

    `difficulty_points`: `Optional[List[DifficultyPoint]]`


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
    _raw_attrs = ('version', 'n_circles', 'n_sliders',
                  'n_spinners', 'ar', 'od', 'cs',
                  'hp', 'sv', 'tick_rate', 'mode',
                  'mode_str', 'stack_leniency',)
    _extra_attrs = ('_raw', 'path', '_hit_objects',
                    '_timing_points', '_difficulty_points',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: Optional[NativeBeatmap]
    path: Optional[Path]
    # raw attrs
    mode: int
    mode_str: str
    version: int

    n_circles: int
    n_sliders: int
    n_spinners: int

    ar: float
    od: float
    cs: float
    hp: float
    sv: float
    tick_rate: float
    stack_leniency: Optional[float]

    # cache needed attrs
    hit_objects: Optional[List[HitObject]]
    timing_points: Optional[List[TimingPoint]]
    difficulty_points: Optional[List[DifficultyPoint]]

    def __init__(self, osu_file_path: Path) -> 'Beatmap':
        '''Init with .osu files'''
        self.path = osu_file_path
        self._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)

    def __repr__(self) -> str:
        return f'<Beatmap object ({self.attrs}), hidden: hit_objects, timing_points, difficulty_points>'

    # Sync ------------
    def init(self, osu_file_path: Path) -> 'Beatmap':
        '''Load the .osu files with path'''
        self.path = osu_file_path
        self._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)
        return self

    def reload(self) -> 'Beatmap':
        '''Reload this .osu files'''
        self._raw = _beatmap_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Create Beatmap with .osu files'''
        obj = cls(osu_file_path)
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
        self._raw = await _beatmap_rust.read_beatmap_async(osu_file_path)
        return self

    async def reload_async_rs(self) -> 'Beatmap':
        '''
        ### Real Rust Async

        ### *May have performance issues: Rust future -> Python coroutine 

        Reload this .osu files'''
        self._raw = await _beatmap_rust.read_beatmap_async(self.path)
        return self

    @classmethod
    async def create_async_rs(cls, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Real Rust Async

        ### *May have performance issues: Rust future -> Python coroutine 

        Create Beatmap with .osu files'''
        obj: 'Beatmap' = cls.__new__(cls)
        obj.path = osu_file_path
        obj._raw = await _beatmap_rust.read_beatmap_async(osu_file_path)
        return obj

    # Python Async wrapper ------------
    async def init_async_py(self, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Load the .osu files with path'''
        self.path = osu_file_path
        self._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)
        return self

    async def reload_async_py(self) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Reload this .osu files'''
        self._raw = _beatmap_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    async def create_async_py(cls, osu_file_path: Path) -> 'Beatmap':
        '''
        ### Python Async wrapper
        Create Beatmap with .osu files'''
        obj: 'Beatmap' = cls.__new__(cls)
        obj.path = osu_file_path
        obj._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)
        return obj

    # Properties ------------
    @property
    def is_initialized(self) -> bool:
        '''Returns whether the beatmap (.osu files) has been loaded and parsed'''
        return (self._raw and self.path) is not None

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return f'path: {self.path}, is_initialized: {self.is_initialized}, ' + self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, Optional[float]]:
        '''Get attrs as dict'''
        return {'path': self.path, 'is_initialized': self.is_initialized, **self._raw.as_dict}

    # Cache needed ------------
    @property
    def hit_objects(self) -> Optional[List[HitObject]]:
        '''Returns wrapped HitObject object list'''
        _attr = getattr(self, '_hit_objects', None)
        if _attr:
            return _attr
        _tmp = self._raw.hit_objects
        if not _tmp:
            return _tmp
        _attr = list(map(lambda obj: HitObject(obj), _tmp))
        setattr(self, '_hit_objects', _attr)
        return _attr

    @property
    def timing_points(self) -> Optional[List[TimingPoint]]:
        '''Returns wrapped TimingPoint object list'''
        _attr = getattr(self, '_timing_points', None)
        if _attr:
            return _attr
        _tmp = self._raw.timing_points
        if not _tmp:
            return _tmp
        _attr = list(map(lambda obj: TimingPoint(obj), _tmp))
        setattr(self, '_timing_points', _attr)
        return _attr

    @property
    def difficulty_points(self) -> Optional[List[DifficultyPoint]]:
        '''Returns wrapped DifficultyPoint object list'''
        _attr = getattr(self, '_difficulty_points', None)
        if _attr:
            return _attr
        _tmp = self._raw.difficulty_points
        if not _tmp:
            return _tmp
        _attr = list(map(lambda obj: DifficultyPoint(obj), _tmp))
        setattr(self, '_difficulty_points', _attr)
        return _attr


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
        self._raw = await _beatmap_rust.read_beatmap_async(osu_file_path)
        return self

    async def reload(self) -> 'Beatmap':
        '''Async reload this .osu files'''
        self._raw = await _beatmap_rust.read_beatmap_async(self.path)
        return self

    @classmethod
    async def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Async create Beatmap with .osu files'''
        obj = cls(osu_file_path)
        obj._raw = await _beatmap_rust.read_beatmap_async(osu_file_path)
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
        self._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)
        return self

    async def reload(self) -> 'Beatmap':
        '''Async reload this .osu files'''
        self._raw = _beatmap_rust.read_beatmap_sync(self.path)
        return self

    @classmethod
    async def create(cls, osu_file_path: Path) -> 'Beatmap':
        '''Async create Beatmap with .osu files'''
        obj = cls(osu_file_path)
        obj._raw = _beatmap_rust.read_beatmap_sync(osu_file_path)
        return obj
