from typing import Dict, Union
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

# PP Calculate objects
NativeRawStars = object
NativeRawPP = object
NativeRawCalcResult = object
NativeCalculator = object
NativeBeatmap = object

# Beatmap parse objects
NativeDifficultyPoint = object
NativeTimingPoint = object
NativePos2 = object
NativeHitObjectKind = object
NativeHitObject = object

ModeResult = Dict[str, Union[float, int, None]]
OsuModeInt = Literal[0, 1, 2, 3]
OsuModeStr = Literal['osu', 'taiko', 'ctb', 'mania']
