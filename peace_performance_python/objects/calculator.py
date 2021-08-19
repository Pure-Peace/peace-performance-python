from .pp_result import CalcResult
from .beatmap import Beatmap

from ..utils import _mutable_property_generator
from ..types import NativeCalculator, PpModule as _pp_rust

from .._peace_performance import pp as _pp_rust

from typing import Any, Dict, Optional, Union


@_mutable_property_generator
class Calculator:
    '''
    Calculator for storing pp calculation configurations (mode, mods, combo, 300, miss, acc, etc.)

    `mode`: `Optional[int]` # gamemode convert

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
    result = c.calculate(beatmap)
    ```
    '''
    _raw_attrs = ('mode', 'mods', 'n50', 'n100', 'n300',
                  'katu', 'acc', 'passed_obj', 'combo', 'miss', 'score',)
    _extra_attrs = ('_raw',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: NativeCalculator
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

    def __init__(self, data: Optional[Dict[str, Union[int, float, None]]] = None, **kwargs) -> 'Calculator':
        '''
        Create new Calculator

        ## Attrs:

        `mode`: `Optional[int]` # gamemode convert

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
        self._raw = _pp_rust.Calculator()
        set = data or kwargs
        if set:
            self.set_with_dict(set)

    def __repr__(self) -> str:
        return f'<Calculator object ({self.attrs})>'

    def getattr(self, attr) -> Any:
        '''Set attr from _raw'''
        return getattr(self._raw, attr)

    def setattr(self, attr, value) -> None:
        '''Get attr to _raw'''
        return setattr(self._raw, attr, value)

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        return self._raw.as_string

    @property
    def attrs_dict(self) -> Dict[str, Union[int, float, None]]:
        '''Get attrs as dict'''
        return self._raw.as_dict

    def reset(self) -> None:
        '''Set Calculator to the default state'''
        self._raw.reset()

    def set_with_dict(self, data: Dict[str, Any]) -> None:
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
        for attr, value in data.items():
            self.setattr(attr, value)

    def calculate(self, beatmap: 'Beatmap') -> 'CalcResult':
        '''
        Calculate pp with a Beatmap.

        ### Examples:
        ```
        beatmap = Beatmap('path_to_osu_file')
        c = Calculator()
        c.set_acc(98.8)
        c.set_combo(727)
        # or
        c = Calculator({'acc': 98.8, 'combo': 727})
        # then
        result = c.calculate(beatmap)
        ```
        '''
        return CalcResult(self._raw.calculate(beatmap._raw))

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
