
from pathlib import Path
from typing import Dict, List, Optional, Union


class DifficultyPoint:
    ...
    time: float
    speed_multiplier: float

    def __repr__(self) -> str:
        return f'<DifficultyPoint object ({self.attrs})>'

    @property
    def as_string(self) -> str: ...
    @property
    def as_dict(self) -> Dict[str, float]: ...

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self.as_string

    @property
    def attrs_dict(self) -> Dict[str, float]:
        '''Get attrs as dict'''
        return self.as_dict


class TimingPoint:
    ...


class Pos2:
    ...


class HitObjectKind:
    ...


class HitObject:
    ...


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
