from typing import Dict, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


ModeResult = Dict[str, Union[float, int, None]]
OsuModeInt = Literal[0, 1, 2, 3]
OsuModeStr = Literal['osu', 'taiko', 'ctb', 'mania']
