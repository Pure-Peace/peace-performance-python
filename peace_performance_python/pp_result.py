from .types import \
    ModeResult, \
    NativeRawCalcResult, \
    NativeRawPP, \
    NativeRawStars, \
    OsuModeInt, \
    OsuModeStr

NativeRawStars = object
NativeRawPP = object
NativeRawCalcResult = object


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

    _raw_attrs = ('stars', 'max_combo', 'ar', 'n_fruits',
                  'n_droplets', 'n_tiny_droplets', 'od', 'speed_strain',
                  'aim_strain', 'n_circles', 'n_spinners')
    _extra_attrs = ('_raw', )
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

    def __new__(cls, *_) -> 'RawStars':
        cls.__init_property__()
        obj: 'RawStars' = super().__new__(cls)
        return obj

    def __init__(self, raw: NativeRawStars):
        self._raw = raw

    @classmethod
    def __init_property__(cls) -> None:
        def _getter_wrapper(c: 'RawStars'): return c.getattr(attr)
        for attr in cls._raw_attrs:
            setattr(cls, attr, property(fget=_getter_wrapper))

    def getattr(self, attr) -> Any:
        return getattr(self._raw, attr)

    @property
    def attrs(self) -> str:
        return ', '.join((f'{attr}: {self.getattr(attr)}' for attr in self._raw_attrs))


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

    _raw: NativeRawPP
    aim: Optional[float]
    spd: Optional[float]
    str: Optional[float]
    acc: Optional[float]
    total: Optional[float]

    def __new__(cls, *_) -> 'RawPP':
        cls.__init_property__()
        obj: 'RawPP' = super().__new__(cls)
        return obj

    def __init__(self, raw: NativeRawPP):
        self._raw = raw

    @classmethod
    def __init_property__(cls) -> None:
        def _getter_wrapper(c: 'RawPP'): return c.getattr(attr)
        for attr in cls._raw_attrs:
            setattr(cls, attr, property(fget=_getter_wrapper))

    def getattr(self, attr) -> Any:
        return getattr(self._raw, attr)

    @property
    def attrs(self) -> str:
        return ', '.join((f'{attr}: {self.getattr(attr)}' for attr in self._raw_attrs))


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

    _raw_attrs = ('mode', 'mods', 'pp', 'raw_pp', 'stars', 'raw_stars',)
    _extra_attrs = ('_raw', )
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeRawCalcResult
    mode: int
    mods: int
    pp: float
    raw_pp: RawPP
    stars: float
    raw_stars: RawStars

    def __new__(cls, *_) -> 'CalcResult':
        cls.__init_property__()
        obj: 'CalcResult' = super().__new__(cls)
        return obj

    def __init__(self, raw: NativeRawCalcResult):
        self._raw = raw

    @classmethod
    def __init_property__(cls) -> None:
        def _getter_wrapper(c: 'CalcResult'): return c.getattr(attr)
        for attr in cls._raw_attrs:
            setattr(cls, attr, property(fget=_getter_wrapper))

    def getattr(self, attr) -> Any:
        return getattr(self._raw, attr)

    @property
    def attrs(self) -> str:
        return ', '.join((f'{attr}: {self.getattr(attr)}' for attr in self._raw_attrs))
