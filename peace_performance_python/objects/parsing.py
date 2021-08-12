from typing import Dict, List, Optional, Tuple
from ..utils import _read_only_property_generator
from ..types import (
    NativeDifficultyPoint,
    NativeTimingPoint,
    NativePos2,
    NativeHitObjectKind,
    NativeHitObject
)


@_read_only_property_generator
class DifficultyPoint:
    '''
    DifficultyPoint object

    `time`: `float`

    `speed_multiplier`: `float`

    '''
    _raw_attrs = ('time', 'speed_multiplier',)
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeDifficultyPoint
    time: float
    speed_multiplier: float

    def __init__(self, raw: NativeDifficultyPoint):
        self._raw = raw

    def __repr__(self) -> str:
        return f'<DifficultyPoint object ({self.attrs})>'

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self._raw.as_dict


@_read_only_property_generator
class TimingPoint:
    '''
    TimingPoint object

    `time`: `float`

    `beat_len`: `float`

    '''
    _raw_attrs = ('time', 'beat_len',)
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeTimingPoint
    time: float
    beat_len: float

    def __init__(self, raw: NativeTimingPoint):
        self._raw = raw

    def __repr__(self) -> str:
        return f'<TimingPoint object ({self.attrs})>'

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self._raw.as_dict


@_read_only_property_generator
class Pos2:
    '''
    Pos2 object

    `x`: `float`

    `y`: `float`

    `length_squared`: `float`

    `length`: `float`

    '''
    _raw_attrs = ('x', 'y', 'length_squared', 'length',)
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativePos2
    x: float
    y: float
    length_squared: float
    length: float

    def __init__(self, raw: NativePos2):
        self._raw = raw

    def __repr__(self) -> str:
        return f'<Pos2 object ({self.attrs})>'

    # Methods ------
    def dot(self, other: 'Pos2') -> float:
        return self._raw.dot(other._raw)

    def distance(self, other: 'Pos2') -> float:
        return self._raw.distance(other._raw)

    def normalize(self) -> 'Pos2':
        return Pos2(self._raw.normalize())

    def add(self, other: 'Pos2') -> 'Pos2':
        return Pos2(self._raw.add(other._raw))

    def sub(self, rhs: 'Pos2') -> 'Pos2':
        return Pos2(self._raw.sub(rhs._raw))

    def mul(self, rhs: float) -> 'Pos2':
        return Pos2(self._raw.mul(rhs))

    def div(self, rhs: float) -> 'Pos2':
        return Pos2(self._raw.div(rhs))

    def add_assign(self, other: 'Pos2'):
        self._raw.add_assign(other._raw)

    # Properties -----

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self._raw.as_dict

    @property
    def as_tuple(self) -> Tuple[float, float]:
        '''Get (x, y) as tuple'''
        return self._raw.as_tuple


@_read_only_property_generator
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
    _raw_attrs = ('kind', 'pixel_len', 'repeats',
                  'path_type', 'end_time',)
    _extra_attrs = ('_raw', '_curve_points',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeHitObjectKind
    kind: float
    pixel_len: Optional[float]
    repeats: Optional[int]
    path_type: Optional[str]
    end_time: Optional[float]

    # cache needed attrs
    curve_points: Optional[List[Pos2]]

    def __init__(self, raw: NativeHitObjectKind):
        self._raw = raw

    def __repr__(self) -> str:
        return f'<HitObjectKind object ({self.attrs})>'

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self._raw.as_dict

    # Cache needed ------------
    @property
    def curve_points(self) -> Optional[List[Pos2]]:
        '''Returns wrapped Pos2 object list'''
        _attr = getattr(self, '_curve_points', None)
        if _attr:
            return _attr
        _tmp = self._raw.curve_points
        if not _tmp:
            return _tmp
        _attr = list(map(lambda obj: Pos2(obj), _tmp))
        setattr(self, '_curve_points', _attr)
        return _attr


@_read_only_property_generator
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
    _raw_attrs = ('start_time', 'sound', 'end_time', 'is_circle',
                  'is_slider', 'is_spinner', 'kind_str',)
    _extra_attrs = ('_raw', 'kind', 'pos')
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeHitObject
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

    def __init__(self, raw: NativeHitObject):
        self._raw = raw
        self.pos = Pos2(raw.pos)
        self.kind = HitObjectKind(raw.kind)

    def __repr__(self) -> str:
        return f'<HitObject object ({self.attrs})>'

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self._raw.as_dict
