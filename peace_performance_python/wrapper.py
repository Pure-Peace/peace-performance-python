from ._peace_performance import wrapper as _wrap


async def read_beatmap(path: str) -> None:
    return await _wrap.read_beatmap(path)


class Wrapper:
    hello: str

    def __init__(self, hello: str) -> None:
        self.hello = hello
