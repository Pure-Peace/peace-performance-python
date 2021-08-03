from ._peace_performance import functions


async def rust_sleep(seconds: int) -> None:
    return await functions.rust_sleep(seconds)
