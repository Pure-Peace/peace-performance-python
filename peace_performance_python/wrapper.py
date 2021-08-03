from ._peace_performance import wrapper


async def read_beatmap(path: str) -> None:
    return await wrapper.read_beatmap(path)
