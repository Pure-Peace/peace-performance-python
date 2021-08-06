from typing import Any, Callable, Optional, Tuple, Union
from ._peace_performance import pp as _p


RawCalculator = object


class Calculator:
    '''
    Calculator for storing pp calculation configurations (mode, mods, combo, 300, miss, acc, etc.)

    '''
    _calc_attrs = ('mode', 'mods', 'n50', 'n100', 'n300',
                   'katu', 'acc', 'passed_obj', 'combo', 'miss',)
    _extra_attrs = ('_cal', )
    __slots__ = _calc_attrs + _extra_attrs

    _cal: RawCalculator
    mode: Optional[int]
    mods: Optional[int]
    n50: Optional[int]
    n100: Optional[int]
    n300: Optional[int]
    katu: Optional[int]
    acc: Optional[float]
    passed_obj: Optional[int]
    combo: Optional[int]
    miss: Optional[int]

    def __repr__(self) -> str:
        return f'<Calculator object ({self.attrs})>'

    def __new__(cls) -> 'Calculator':
        cls.__init_property__()
        obj: 'Calculator' = super().__new__(cls)
        return obj

    def __init__(self) -> 'Calculator':
        '''Create new Calculator'''
        self._cal = _p.Calculator()

    @classmethod
    def __init_property__(cls) -> None:
        '''Initial property and methods'''
        for attr in cls._calc_attrs:
            handlers = cls.__property_handlers__(attr)
            for prefix, handler in zip(('get_', 'set_', 'del_',), handlers):
                setattr(cls, prefix + attr, handler)
            setattr(cls, attr, property(*handlers))

    @staticmethod
    def __property_handlers__(attr: str) -> Tuple[Callable]:
        '''Returns getter, setter and deleter methods for attr'''
        def _getter_wrapper(c: 'Calculator'):
            return c.getattr(attr)

        def _setter_wrapper(c: 'Calculator', value):
            return c.setattr(attr, value)

        def _deleter_wrapper(c: 'Calculator'):
            return c.setattr(attr, None)

        return (_getter_wrapper, _setter_wrapper, _deleter_wrapper,)

    def __clear_calc_attrs__(self) -> None:
        '''Clear all calc attr'''
        for attr in self._calc_attrs:
            self.setattr(attr, None)

    def getattr(self, attr) -> Any:
        return getattr(self._cal, attr)

    def setattr(self, attr, value) -> None:
        return setattr(self._cal, attr, value)

    @property
    def attrs(self) -> str:
        return ', '.join((f'{attr}: {self.getattr(attr)}' for attr in self._calc_attrs))

    def reset(self) -> None:
        '''Set self to the default state'''
        self._cal.reset()
        self.__clear_calc_attrs__()

    # Interfaces -----
    def set_mode(val: Optional[int]): ...
    def set_mods(val: Optional[int]): ...
    def set_n50(val: Optional[int]): ...
    def set_n100(val: Optional[int]): ...
    def set_n300(val: Optional[int]): ...
    def set_katu(val: Optional[int]): ...
    def set_acc(val: Optional[float]): ...
    def set_passed_obj(val: Optional[int]): ...
    def set_combo(val: Optional[int]): ...
    def set_miss(val: Optional[int]): ...

    def del_mode(): ...
    def del_mods(): ...
    def del_n50(): ...
    def del_n100(): ...
    def del_n300(): ...
    def del_katu(): ...
    def del_acc(): ...
    def del_passed_obj(): ...
    def del_combo(): ...
    def del_miss(): ...

    def get_mode(val: Optional[int]) -> Optional[int]: ...
    def get_mods(val: Optional[int]) -> Optional[int]: ...
    def get_n50(val: Optional[int]) -> Optional[int]: ...
    def get_n100(val: Optional[int]) -> Optional[int]: ...
    def get_n300(val: Optional[int]) -> Optional[int]: ...
    def get_katu(val: Optional[int]) -> Optional[int]: ...
    def get_acc(val: Optional[float]) -> Optional[float]: ...
    def get_passed_obj(val: Optional[int]) -> Optional[int]: ...
    def get_combo(val: Optional[int]) -> Optional[int]: ...
    def get_miss(val: Optional[int]) -> Optional[int]: ...


def new_raw_calculator() -> RawCalculator:
    '''Create new native calculator'''
    return _p.new_calculator()
