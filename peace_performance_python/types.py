from pathlib import Path
from typing import Dict, List, Optional, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


ModeResult = Dict[str, Union[float, int, None]]
OsuModeInt = Literal[0, 1, 2, 3]
OsuModeStr = Literal['osu', 'taiko', 'ctb', 'mania']

# Beatmap parse objects
NativeDifficultyPoint = object
NativeTimingPoint = object
NativePos2 = object
NativeHitObjectKind = object
NativeHitObject = object


# PP Calculate objects
class NativeRawStars:
    ...
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

    @property
    def as_string() -> str: ...
    @property
    def as_dict() -> ModeResult: ...


class NativeRawPP:
    ...
    aim: Optional[float]
    spd: Optional[float]
    str: Optional[float]
    acc: Optional[float]
    total: Optional[float]

    @property
    def as_string() -> str: ...
    @property
    def as_dict() -> Dict[str, Optional[float]]: ...


class NativeBeatmap:
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
    def hit_objects(self) -> List[NativeHitObject]: ...
    @property
    def timing_points(self) -> List[NativeTimingPoint]: ...
    @property
    def difficulty_points(self) -> List[NativeDifficultyPoint]: ...

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...


class NativeCalculator:
    ...
    mode: Optional[int]
    mods: Optional[int]
    n50: Optional[int]  # Irrelevant for osu!mania
    n100: Optional[int]  # Irrelevant for osu!mania and osu!taiko
    n300: Optional[int]  # Irrelevant for osu!mania
    katu: Optional[int]  # Only relevant for osu!ctb
    acc: Optional[float]  # Irrelevant for osu!mania
    passed_obj: Optional[int]
    combo: Optional[int]  # Irrelevant for osu!mania
    miss: Optional[int]  # Irrelevant for osu!mania
    score: Optional[int]  # Only relevant for osu!mania

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...

    def __init__(self) -> 'NativeCalculator': ...
    def reset(self) -> None: ...
    def calculate(self, beatmap: NativeBeatmap) -> 'NativeRawCalcResult': ...


class NativeRawCalcResult:
    ...
    mode: int
    mode_str: str
    mods: int
    pp: float
    stars: float

    @property
    def raw_pp(self) -> NativeRawPP: ...
    @property
    def raw_stars(self) -> NativeRawStars: ...
    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, Union[NativeRawPP,
                                         NativeRawStars, int, float]]: ...


# Modules
class PpModule:
    '''Native module `pp`'''
    ...
    def new_calculator() -> NativeCalculator: ...
    def Calculator() -> NativeCalculator: ...


class BeatmapModule:
    '''Native module `beatmap`'''
    ...
    async def read_beatmap_async(path: Path) -> NativeBeatmap: ...
    def read_beatmap_sync(path: Path) -> NativeBeatmap: ...


class CommonModule:
    '''Native module `common`'''
    ...
    def set_log_level(log_level: str) -> None: ...
    def init_logger() -> None: ...
    async def rust_sleep(secs: int) -> None: ...
