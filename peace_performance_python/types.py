from typing import Dict, Literal, Union


NativeRawStars = object
NativeRawPP = object
NativeRawCalcResult = object
NativeCalculator = object
NativeBeatmap = object

ModeResult = Dict[str, Union[float, int, None]]
OsuModeInt = Literal[0, 1, 2, 3]
OsuModeStr = Literal['osu', 'taiko', 'ctb', 'mania']
