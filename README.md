# peace-performance-python

*To calculate star ratings and performance points for all osu! gamemodes*

**[peace-performance](https://github.com/Pure-Peace/peace-performance)** (Rust) binding for python based on [PyO3](https://github.com/PyO3/pyo3).

Cross-platform support.

**Note**: This library is not currently uploaded to PypI, you may need to download it locally for compilation and then import it in python.

## Minimal Examples

```python
from peace_performance_python.prelude import *

beatmap = await Beatmap.create('path_to_osu_file') # Beatmap can be cached and reused!
result = Calculator(acc=98.8, miss=3).calculate(beatmap) # Calculator can also
```

## Full Examples

```python
import asyncio
import sys

# import all
from peace_performance_python.prelude import *
# or
# from peace_performance_python.beatmap import Beatmap
# from peace_performance_python.calculator import Calculator

from tests import join_beatmap, HITORIGOTO


# Initial Rust logger (optional)
set_log_level('trace')
init_logger()


# Choose a style you like
def calculate_1(beatmap: Beatmap) -> CalcResult:
    return calculate_pp(beatmap, Calculator({'acc': 98.8, 'miss': 3}))


def calculate_2(beatmap: Beatmap) -> CalcResult:
    # --
    c = Calculator()
    c.set_acc(98.8)
    c.set_miss(3)

    # or
    c.acc = 98.8
    c.miss = 3

    # or
    c.setattr('acc', 98.8)
    c.setattr('miss', 3)
    return calculate_pp(beatmap, c)


def calculate_3(beatmap: Beatmap) -> CalcResult:
    c = Calculator()
    c.set_with_dict({'acc': 98.8, 'miss': 3})
    return calculate_pp(beatmap, c)


def calculate_4(beatmap: Beatmap) -> CalcResult:
    return Calculator({'acc': 98.8, 'miss': 3}).calculate(beatmap)


def calculate_5(beatmap: Beatmap) -> CalcResult:
    return Calculator(acc=98.8, miss=3).calculate(beatmap)


async def main():
    path = join_beatmap(HITORIGOTO)
    # Load beatmap
    beatmap = await Beatmap.create(path)
    # Calculate pp
    result = calculate_5(beatmap)
    print('\n***** result:', result)
    print('\n***** result.pp:', result.pp)
    print('\n***** result as dict:', result.attrs_dict)
    print('\n***** result.raw_stars as dict:', result.raw_stars.attrs_dict)
    print('\n***** result.raw_pp as dict:', result.raw_pp.attrs_dict)

if __name__ == '__main__':
    asyncio.run(main())

```

### Running results

```rust
 TRACE peace_performance_python::methods::common > function=async_read_file duration=289.1µs
 TRACE peace_performance_python::methods::pp     > function=async_parse_beatmap duration=414µs
 TRACE peace_performance_python::methods::pp     > function=calc_with_any_pp duration=99.6µs
 TRACE peace_performance_python::objects::calculator > function=calc duration=245.4µs

...

***** result.pp: 152.19204711914062

...

***** result as dict: {
    'mode': 0, 
    'mods': 0, 
    'pp': 152.19204711914062, 
    'stars': 5.162832260131836, 
    'raw_pp': {
        'aim': 73.0337905883789, 
        'spd': 31.048368453979492, 
        'str': None, 
        'acc': 45.17241287231445, 
        'total': 152.19204711914062}, 
    'raw_stars': {
        'stars': 5.162832260131836, 
        'max_combo': 476, 
        'ar': 9.0, 
        'n_fruits': None, 
        'n_droplets': None, 
        'n_tiny_droplets': None, 
        'od': 8.5, 
        'speed_strain': 2.0723509788513184, 
        'aim_strain': 2.7511043548583984, 
        'n_circles': 207, 
        'n_spinners': 1
        }
    }

...
```

---

## Building

This package is intended to be built using `rust`, `maturin` or `setuptools_rust`.

**1. Install Rust**

*posix*

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

*windows*

```shell
https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe
```

**2. Install python dev dependencies**

```shell
pip install -r requirements-dev.txt
```

**3. Build native python lib**

```shell
maturin develop --release
```

**OR**

```shell
python setup.py develop
```

#### Compile to `.whl` to use pip installation

```shell
maturin build --release
```

**OR**

```shell
python setup.py bdist_wheel
```

**install .whl**

```shell
# maturin build
pip install target/wheels/<name>.whl

# setup.py build
pip install dist/<name>.whl
```

---

## Run tests and benchmarks

Once built, you can run the tests and benchmakrs using `pytest`

```shell
pytest
```

**or bench and draw a image**

```shell
pytest --benchmark-histogram
```

**Run examples**

```shell
python examples.py
```

---

### Simple Benchmarks

*Native vs wrapped beatmap object*
<img src="./benchmark_results/benchmark_20210807_190701.svg">

*Read and parsing time spent on beatmap of different sizes*
(forgiving is a beatmap over 50 minutes long and takes the longest)
<img src="./benchmark_results/benchmark_20210807_190701-bench-beatmap.svg">

*There are also subtle differences in the different calling methods*
<img src="./benchmark_results/benchmark_20210807_190701-bench-pp-calc.svg">

---

## MIT

pure-peace
