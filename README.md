# peace-performance-python

An extension module built using PyO3.

## Testing

This package is intended to be built using `maturin`. Once built, you can run the tests using `pytest`:

```shell
pip install maturin
maturin develop
pytest
```

# setuptools

## Building and Testing

To build this package, first install `setuptools_rust`:

```shell
pip install setuptools_rust
```

To build and test use `python setup.py develop`:

```shell
pip install -r requirements-dev.txt
python setup.py develop && pytest
```
