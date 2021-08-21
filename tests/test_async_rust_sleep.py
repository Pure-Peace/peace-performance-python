from peace_performance_python.functions import rust_sleep

from . import async_run


def test_async_rust_sleep() -> None:
    async_run(rust_sleep(0))
