from typing import Any, Dict, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


ModeResult = Dict[str, Union[float, int, None]]
OsuModeInt = Literal[0, 1, 2, 3]
OsuModeStr = Literal['osu', 'taiko', 'ctb', 'mania']


class BaseGetter:
    @property
    def as_string(self) -> str:
        '''Get attrs as text'''
        ...

    @property
    def as_dict(self) -> Dict[str, Any]:
        '''Get attrs as dict'''
        ...

    @property
    def attrs(self) -> str:
        '''Get attrs as text'''
        ...

    @property
    def attrs_dict(self) -> Dict[str, Any]:
        '''Get attrs as dict'''
        ...
