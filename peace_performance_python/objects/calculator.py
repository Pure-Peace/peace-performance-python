from .pp_result import CalcResult
from .beatmap import Beatmap

from ..utils import _mutable_property_generator

from .._peace_performance import pp as _pp_rust

from typing import Any, Dict, Optional, Union


@_mutable_property_generator
class Calculator:

    _raw_attrs = ('mode', 'mods', 'n50', 'n100', 'n300',
                  'katu', 'acc', 'passed_obj', 'combo', 'miss', 'score',)
    _extra_attrs = ('_raw',)
    __slots__ = _raw_attrs + _extra_attrs

    _raw: _pp_rust.Calculator
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






