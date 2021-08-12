from ..types import (
    ModeResult,
    NativeRawCalcResult,
    NativeRawPP,
    NativeRawStars,
    OsuModeInt,
    OsuModeStr
)
from ..functions.common import osu_mode_str
from ..utils import _read_only_property_generator, _get_attrs_dict, _get_attrs_str

from typing import Dict, Optional, Tuple, Union

_str = str


@_read_only_property_generator
class RawStars:
    '''
    Raw PP Calculation results: `RawStars` (read only).

    #### Depending on the mode (`osu`, `taiko`, `ctb`, `mania`), will get different results.

    ### Methods:

    `get_osu()`,
    `get_taiko()`,
    `get_ctb()`,
    `get_mania()`,

    ### Attrs:

    `stars`: `Optional<f32>`

    `max_combo`: `Optional<usize>`

    `ar`: `Optional<f32>`

    `n_fruits`: `Optional<usize>`

    `n_droplets`: `Optional<usize>`

    `n_tiny_droplets`: `Optional<usize>`

    `od`: `Optional<f32>`

    `speed_strain`: `Optional<f32>`

    `aim_strain`: `Optional<f32>`

    `n_circles`: `Optional<usize>`

    `n_spinners`: `Optional<usize>`

    '''

    # mode attrs
    mode_attrs: Dict[ModeResult, Tuple[str]] = {
        'osu': ('stars', 'ar', 'od', 'speed_strain',
                'aim_strain', 'max_combo', 'n_circles', 'n_spinners',),
        'taiko': ('stars',),
        'ctb': ('stars', 'max_combo', 'ar', 'n_fruits', 'n_droplets',
                'n_tiny_droplets',),
        'mania': ('stars',)
    }

    # object attrs
    _raw_attrs = ('stars', 'max_combo', 'ar', 'n_fruits',
                  'n_droplets', 'n_tiny_droplets', 'od', 'speed_strain',
                  'aim_strain', 'n_circles', 'n_spinners',)
    _extra_attrs = ('_raw',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeRawStars
    stars: Optional[float]
    max_combo: Optional[int]
    ar: Optional[float]
    n_fruits: Optional[int]
    n_droplets: Optional[int]
    n_tiny_droplets: Optional[int]
    od: Optional[float]
    speed_strain: Optional[float]
    aim_strain: Optional[float]
    n_circles: Optional[int]
    n_spinners: Optional[int]

    def __repr__(self) -> str:
        return f'<RawStars object ({self.attrs})>'

    def __init__(self, raw: NativeRawStars):
        self._raw = raw

    def get_mode_attrs(self, mode: Union[OsuModeInt, OsuModeStr]) -> Tuple[str]:
        '''Get attrs with mode (str or int): ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})'''
        if isinstance(mode, int):
            mode = osu_mode_str(mode)
        return self.mode_attrs.get(mode, tuple())

    def get_mode(self, mode: Union[OsuModeInt, OsuModeStr]) -> ModeResult:
        '''Get attrs Dict with mode (str or int): ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})'''
        return {attr: getattr(self._raw, attr) for attr in self.get_mode_attrs(mode)}

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return _get_attrs_str(self._raw, self._raw_attrs)

    @property
    def attrs_dict(self) -> ModeResult:
        '''Get attrs as dict'''
        return _get_attrs_dict(self._raw, self._raw_attrs)

    @property
    def mode_osu(self) -> ModeResult:
        '''RawStars info with mode `osu`'''
        return self.get_mode('osu')

    @property
    def mode_taiko(self) -> ModeResult:
        '''RawStars info with mode `taiko`'''
        return self.get_mode('taiko')

    @property
    def mode_ctb(self) -> ModeResult:
        '''RawStars info with mode `ctb`'''
        return self.get_mode('ctb')

    @property
    def mode_mania(self) -> ModeResult:
        '''RawStars info with mode `mania`'''
        return self.get_mode('mania')


@_read_only_property_generator
class RawPP:
    '''
    Raw PP Calculation results: `RawPP` (read only).

    ### Attrs (Optional<f32>):

    `aim`: Aim pp

    `spd`: Speed pp

    `str`: Strain pp

    `acc`: Accuracy pp

    `total`: Total pp

    '''

    _raw_attrs = ('aim', 'spd', 'str', 'acc', 'total',)
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeRawCalcResult
    aim: Optional[float]
    spd: Optional[float]
    str: Optional[float]
    acc: Optional[float]
    total: Optional[float]

    def __repr__(self) -> _str:
        return f'<RawPP object ({self.attrs})>'

    def __init__(self, raw: NativeRawPP):
        self._raw = raw

    @property
    def attrs(self) -> _str:
        '''Get attrs as text'''
        return _get_attrs_str(self._raw, self._raw_attrs)

    @property
    def attrs_dict(self) -> Dict[_str, Optional[float]]:
        '''Get attrs as dict'''
        return _get_attrs_dict(self._raw, self._raw_attrs)


@_read_only_property_generator
class CalcResult:
    '''
    PP Calculation results: `CalcResult` (read only).

    ### Attrs:

    `mode`: `u8` ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})

    `mods`: `u32` (Detail here: `https://github.com/ppy/osu-api/wiki#mods`)

    `pp`: `f32`

    `raw_pp`: `RawPP` object

    `stars`: `f32`

    `raw_stars`: `RawStars` object
    '''

    _raw_attrs = ('mode', 'mods', 'pp', 'stars', )
    _manual_impl = ('raw_pp', 'raw_stars', )
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _manual_impl + _extra_attrs

    _raw: NativeRawCalcResult
    raw_pp: RawPP
    raw_stars: RawStars
    mode: int
    mods: int
    pp: float
    stars: float

    def __repr__(self) -> str:
        return f'<CalcResult object ({self.attrs})>'

    def __init__(self, raw: NativeRawCalcResult) -> None:
        self.raw_pp = RawPP(raw.raw_pp)
        self.raw_stars = RawStars(raw.raw_stars)
        self._raw = raw

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return ', '.join((
            _get_attrs_str(self._raw, self._raw_attrs),
            _get_attrs_str(self, self._manual_impl),
        ))

    @property
    def attrs_dict(self) -> Dict[str, Union[RawPP, RawStars, int, float]]:
        '''Get attrs as dict'''
        return {**_get_attrs_dict(self._raw, self._raw_attrs),
                **_get_attrs_dict(self, self._manual_impl)}
