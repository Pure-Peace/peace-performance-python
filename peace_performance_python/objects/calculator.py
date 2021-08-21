from .beatmap import Beatmap
from .._peace_performance.pp import (
    CalcResult,
    Calculator as CalculatorRust
)


class Calculator(CalculatorRust):
    '''
    Calculator for storing pp calculation configurations (mode, mods, combo, 300, miss, acc, etc.)

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
    result = c.calculate(beatmap)
    ```
    '''

    def calculate(self, beatmap: Beatmap) -> CalcResult:
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
        return self.calculate_raw(beatmap._raw)
