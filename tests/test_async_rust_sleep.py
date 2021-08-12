import asyncio

from peace_performance_python.functions import rust_sleep

loop = asyncio.get_event_loop()


def test_async_rust_sleep() -> None:
    loop.run_until_complete(rust_sleep(0))
