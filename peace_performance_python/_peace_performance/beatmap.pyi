from pathlib import Path
from . import BaseGetter
from typing import Dict, List, Optional, Tuple


class DifficultyPoint(BaseGetter):
    '''
    DifficultyPoint object

    `time`: `float`

    `speed_multiplier`: `float`

    '''
    time: float
    speed_multiplier: float

    @property
    def as_dict(self) -> Dict[str, float]: ...
    @property
    def attrs_dict(self) -> Dict[str, float]: ...


class TimingPoint(BaseGetter):
    '''
    TimingPoint object

    `time`: `float`

    `beat_len`: `float`

    '''
    time: float
    beat_len: float

    @property
    def as_dict(self) -> Dict[str, float]: ...
    @property
    def attrs_dict(self) -> Dict[str, float]: ...


class Pos2(BaseGetter):
    '''
    Pos2 object

    `x`: `float`

    `y`: `float`

    `length_squared`: `float`

    `length`: `float`

    '''
    x: float
    y: float
    length_squared: float
    length: float

    # Methods ------

    def dot(self, other: Pos2) -> float: ...
    def distance(self, other: Pos2) -> float: ...
    def normalize(self) -> Pos2: ...
    def add(self, other: Pos2) -> Pos2: ...
    def sub(self, rhs: Pos2) -> Pos2: ...
    def mul(self, rhs: float) -> Pos2: ...
    def div(self, rhs: float) -> Pos2: ...
    def add_assign(self, other: Pos2): ...

    @property
    def as_dict(self) -> Dict[str, float]: ...
    @property
    def attrs_dict(self) -> Dict[str, float]: ...

    @property
    def as_tuple(self) -> Tuple[float, float]:
        '''Get (x, y) as tuple'''
        ...


class HitObjectKind(BaseGetter):
    '''
    HitObjectKind object

    `kind`: `str`

    `pixel_len`: `float` | `None`

    `repeats`: `int` | `None`

    `curve_points`: `List[Pos2]` | `None`

    `path_type`: `str` | `None`

    `end_time`: `float` | `None`

    '''
    kind: float
    pixel_len: Optional[float]
    repeats: Optional[int]
    path_type: Optional[str]
    end_time: Optional[float]
    curve_points: Optional[List[Pos2]]

    @property
    def as_dict(self) -> Dict[str, float]: ...
    @property
    def attrs_dict(self) -> Dict[str, float]: ...


class HitObject(BaseGetter):
    '''
    HitObject object

    `start_time`: `float`

    `sound`: `int`

    `end_time`: `float`

    `is_circle`: `bool`

    `is_slider`: `bool`

    `is_spinner`: `bool`

    `pos`: `Pos2`

    `kind_str`: `str`

    `kind`: `HitObjectKind`

    '''
    start_time: float
    sound: int
    end_time: float
    is_circle: bool
    is_slider: bool
    is_spinner: bool
    kind_str: str
    pos: Pos2
    kind: HitObjectKind

    @property
    def as_dict(self) -> Dict[str, float]: ...
    @property
    def attrs_dict(self) -> Dict[str, float]: ...


class Beatmap(BaseGetter):
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


    # Examples:
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

    @property
    def hit_objects(self) -> List[HitObject]: ...
    @property
    def timing_points(self) -> List[TimingPoint]: ...
    @property
    def difficulty_points(self) -> List[DifficultyPoint]: ...


async def read_beatmap_async(path: Path) -> Beatmap: ...
def read_beatmap_sync(path: Path) -> Beatmap: ...
