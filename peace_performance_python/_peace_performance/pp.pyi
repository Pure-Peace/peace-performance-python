from typing import Dict, Optional, Union

from .beatmap import Beatmap


class RawStars:
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
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...


class RawPP:
    ...
    aim: Optional[float]
    spd: Optional[float]
    str: Optional[float]
    acc: Optional[float]
    total: Optional[float]

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, Optional[float]]: ...


class Calculator:
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

    def __init__(self) -> 'Calculator': ...
    def reset(self) -> None: ...
    def calculate(self, beatmap: Beatmap) -> 'CalcResult': ...


class CalcResult:
    ...
    mode: int
    mode_str: str
    mods: int
    pp: float
    stars: float

    @property
    def raw_pp(self) -> RawPP: ...
    @property
    def raw_stars(self) -> RawStars: ...
    @property
    def as_string(self) -> str: ...

    @property
    def as_dict(self) -> Dict[str, Union[RawPP,
                                         RawStars, int, float]]: ...


def new_calculator() -> Calculator: ...
