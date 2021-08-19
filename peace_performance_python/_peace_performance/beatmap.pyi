from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union


class DifficultyPoint:
    '''
    DifficultyPoint object

    `time`: `float`

    `speed_multiplier`: `float`

    '''
    time: float
    speed_multiplier: float

    def __repr__(self) -> str:
        return f'<DifficultyPoint object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, float]: ...

    # Properties -----
    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict


class TimingPoint:
    '''
    TimingPoint object

    `time`: `float`

    `beat_len`: `float`

    '''
    time: float
    beat_len: float

    def __repr__(self) -> str:
        return f'<TimingPoint object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, float]: ...

    # Properties -----
    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict


class Pos2:
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

    def __repr__(self) -> str:
        return f'<Pos2 object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, float]: ...

    # Methods ------
    def dot(self, other: Pos2) -> float: ...
    def distance(self, other: Pos2) -> float: ...
    def normalize(self) -> Pos2: ...
    def add(self, other: Pos2) -> Pos2: ...
    def sub(self, rhs: Pos2) -> Pos2: ...
    def mul(self, rhs: float) -> Pos2: ...
    def div(self, rhs: float) -> Pos2: ...
    def add_assign(self, other: Pos2): ...

    # Properties -----

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict

    @property
    def as_tuple(self) -> Tuple[float, float]:
        '''Get (x, y) as tuple'''
        return self.as_tuple


class HitObjectKind:
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

    # cache needed attrs
    curve_points: Optional[List[Pos2]]

    def __repr__(self) -> str:
        return f'<HitObjectKind object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, float]: ...

    # Properties -----
    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict


class HitObject:
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

    # cache needed attrs
    pos: Pos2
    kind: HitObjectKind

    def __repr__(self) -> str:
        return f'<HitObject object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, float]: ...

    # Properties -----
    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict


class Beatmap:
    ...
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

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...


async def read_beatmap_async(path: Path) -> Beatmap: ...
def read_beatmap_sync(path: Path) -> Beatmap: ...
