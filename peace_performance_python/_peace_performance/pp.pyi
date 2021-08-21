from typing import Dict, Optional, Tuple, Union

from .types import BaseGetter, ModeResult, OsuModeInt, OsuModeStr
from .beatmap import Beatmap


class Calculator(BaseGetter):
    '''
    Calculator (`Rust`) for storing pp calculation configurations (mode, mods, combo, 300, miss, acc, etc.)

    `mode`: `Optional[int]`

    `mods`: `Optional[int]`

    `n50`: `Optional[int]` # Irrelevant for osu!mania

    `n100`: `Optional[int]` # Irrelevant for osu!mania and osu!taiko

    `n300`: `Optional[int]` # Irrelevant for osu!mania

    `katu`: `Optional[int]` # Only relevant for osu!ctb

    `acc`: `Optional[float]` # Irrelevant for osu!mania

    `passed_obj`: `Optional[int]` 

    `combo`: `Optional[int]` # Irrelevant for osu!mania

    `miss`: `Optional[int]` # Irrelevant for osu!mania

    `score`: `Optional[int]` # Only relevant for osu!mania

    ### Examples:
    ```
    beatmap = Beatmap('path_to_osu_file')
    c = Calculator()
    c.set_acc(98.8)
    c.set_combo(727)
    # or
    c = Calculator({'acc': 98.8, 'combo': 727})
    # then
    result = c.calculate_raw(beatmap._raw)
    ```
    '''
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
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...
    @property
    def attrs_dict(self) -> Dict[str, Union[float, int, None]]: ...

    def __init__(self, data: Optional[Dict[str, Union[int, float, None]]] = None, **kwargs) -> 'Calculator':
        '''
        Create new Calculator

        ## Attrs:

        `mode`: `Optional[int]`

        `mods`: `Optional[int]`

        `n50`: `Optional[int]` # Irrelevant for osu!mania

        `n100`: `Optional[int]` # Irrelevant for osu!mania and osu!taiko

        `n300`: `Optional[int]` # Irrelevant for osu!mania

        `katu`: `Optional[int]` # Only relevant for osu!ctb

        `acc`: `Optional[float]` # Irrelevant for osu!mania

        `passed_obj`: `Optional[int]` 

        `combo`: `Optional[int]` # Irrelevant for osu!mania

        `miss`: `Optional[int]` # Irrelevant for osu!mania

        `score`: `Optional[int]` # Only relevant for osu!mania

        '''
        ...

    def new_empty() -> 'Calculator':
        '''Crate empty calculator'''
        ...

    def reset(self) -> None:
        '''Set Calculator to the default state'''
        ...

    def calculate_raw(self, beatmap: Beatmap) -> 'CalcResult':
        '''
        Calculate pp with a Beatmap (`Rust raw`).

        ### Examples:
        ```
        beatmap = Beatmap('path_to_osu_file')
        c = Calculator()
        c.set_acc(98.8)
        c.set_combo(727)
        # or
        c = Calculator({'acc': 98.8, 'combo': 727})
        # then
        result = c.calculate_raw(beatmap._raw)
        ```
        '''
        ...

    def getattr(self, attr: str) -> Union[int, float, None]: ...

    def setattr(self, attr: str, value: Union[int, float, None]) -> None: ...

    def set_with_str(self, attr: str, value: Union[int, float, None]) -> None:
        '''Set attr (rust native)'''
        ...

    def set_with_dict(self, data: Dict[str, Union[int, float, None]]) -> None:
        '''
        Set data with a dict.

        ### Examples:
        ```
        data = {
            'mode': 0,
            'n50': 66,
            'n100': 666
        }
        c = Calculator()
        c.set_with_dict(data)
        # or
        c = Calculator(data)
        ```
        '''
        ...

    # Interfaces -----
    def set_mode(self, val: Optional[int]) -> None: ...
    def set_mods(self, val: Optional[int]) -> None: ...

    def set_n50(self, val: Optional[int]) -> None:
        '''### Irrelevant for osu!mania'''
        ...

    def set_n100(self, val: Optional[int]) -> None:
        '''### Irrelevant for osu!mania and osu!taiko'''
        ...

    def set_n300(self, val: Optional[int]) -> None:
        '''### Irrelevant for osu!mania'''
        ...

    def set_katu(self, val: Optional[int]) -> None:
        '''### Only relevant for osu!ctb'''
        ...

    def set_acc(self, val: Optional[float]) -> None:
        '''### Irrelevant for osu!mania'''
        ...

    def set_passed_obj(self, val: Optional[int]) -> None: ...

    def set_combo(self, val: Optional[int]) -> None:
        '''### Irrelevant for osu!mania'''
        ...

    def set_miss(self, val: Optional[int]) -> None:
        '''### Irrelevant for osu!mania'''
        ...

    def set_score(self, val: Optional[int]) -> None:
        '''### Only relevant for osu!mania'''
        ...

    def del_mode(self) -> None: ...
    def del_mods(self) -> None: ...
    def del_n50(self) -> None: ...
    def del_n100(self) -> None: ...
    def del_n300(self) -> None: ...
    def del_katu(self) -> None: ...
    def del_acc(self) -> None: ...
    def del_passed_obj(self) -> None: ...
    def del_combo(self) -> None: ...
    def del_miss(self) -> None: ...
    def del_score(self) -> None: ...

    def get_mode(self) -> Optional[int]: ...
    def get_mods(self) -> Optional[int]: ...
    def get_n50(self) -> Optional[int]: ...
    def get_n100(self) -> Optional[int]: ...
    def get_n300(self) -> Optional[int]: ...
    def get_katu(self) -> Optional[int]: ...
    def get_acc(self) -> Optional[float]: ...
    def get_passed_obj(self) -> Optional[int]: ...
    def get_combo(self) -> Optional[int]: ...
    def get_miss(self) -> Optional[int]: ...
    def get_score(self) -> Optional[int]: ...


class RawStars(BaseGetter):
    '''
    Raw PP Calculation results: `RawStars` (`Rust`) (read only).

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
    def as_dict(self) -> Dict[str, Union[float, int, None]]: ...
    @property
    def attrs_dict(self) -> Dict[str, Union[float, int, None]]: ...

    def get_mode_attrs(self, mode: Union[OsuModeInt, OsuModeStr]) -> Tuple[str]:
        '''Get attrs with gamemode (str or int): ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})'''
        ...

    def get_mode(self, mode: Union[OsuModeInt, OsuModeStr]) -> ModeResult:
        '''Get attrs Dict with gamemode (str or int): ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})'''
        ...

    @property
    def mode_osu(self) -> ModeResult:
        '''RawStars info with gamemode `osu`'''
        ...

    @property
    def mode_taiko(self) -> ModeResult:
        '''RawStars info with gamemode `taiko`'''
        ...

    @property
    def mode_ctb(self) -> ModeResult:
        '''RawStars info with gamemode `ctb`'''
        ...

    @property
    def mode_mania(self) -> ModeResult:
        '''RawStars info with gamemode `mania`'''
        ...


class RawPP(BaseGetter):
    '''
    Raw PP Calculation results: `RawPP` (`Rust`) (read only).

    ### Attrs (Optional<f32>):

    `aim`: Aim pp

    `spd`: Speed pp

    `str`: Strain pp

    `acc`: Accuracy pp

    `total`: Total pp

    '''
    aim: Optional[float]
    spd: Optional[float]
    str: Optional[float]
    acc: Optional[float]
    total: Optional[float]

    @property
    def as_dict(self) -> Dict[str, Optional[float]]: ...
    @property
    def attrs_dict(self) -> Dict[str, Optional[float]]: ...


class CalcResult(BaseGetter):
    '''
    PP Calculation results: `CalcResult` (`Rust`) (read only).

    ### Attrs:

    `mode`: `u8` ({`0`: `osu`, `1`: `taiko`, `2`: `catch the beat`, `3`: `mania`})

    `mods`: `u32` (Detail here: `https://github.com/ppy/osu-api/wiki#mods`)

    `pp`: `f32`

    `raw_pp`: `RawPP` object

    `stars`: `f32`

    `raw_stars`: `RawStars` object
    '''
    mode: int
    mode_str: str
    mods: int
    pp: float
    stars: float
    raw_pp: RawPP
    raw_stars: RawStars

    @property
    def as_dict(self) -> Dict[str, Union[
        RawPP, RawStars, int, float]]: ...

    @property
    def attrs_dict(self) -> Dict[str, Union[
        RawPP, RawStars, int, float]]: ...


def new_calculator() -> Calculator:
    '''Create new native Calculator (`Rust`)'''
    ...
