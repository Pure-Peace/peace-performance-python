from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .types import BaseGetter


class DifficultyPoint(BaseGetter):
    '''
    DifficultyPoint object (`Rust`)

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
    TimingPoint object (`Rust`)

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
    Pos2 object (`Rust`)

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
    HitObjectKind object (`Rust`)

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
    HitObject object (`Rust`)

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
    The Beatmap (`Rust`) used to calculate the pp, it contains the parsed .osu beatmap.

    `path`: `Optional[Path]`

    `mode`: `int`

    `mode_str`: `Optional[str]`

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
    '''
    mode: int
    mode_str: Optional[str]
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
    def as_dict(self) -> Dict[str, float, str, None]: ...
    @property
    def attrs_dict(self) -> Dict[str, float, str, None]: ...

    @property
    def hit_objects(self) -> List[HitObject]: ...
    @property
    def timing_points(self) -> List[TimingPoint]: ...
    @property
    def difficulty_points(self) -> List[DifficultyPoint]: ...


async def read_beatmap_async(path: Path) -> Beatmap:
    '''Read a beatmap async, returns Beatmap object (`Rust`)'''
    ...


def read_beatmap_sync(path: Path) -> Beatmap:
    '''Read a beatmap, returns Beatmap object (`Rust`)'''
    ...
