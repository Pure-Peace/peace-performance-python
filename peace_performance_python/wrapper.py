from ._peace_performance import wrapper as _wrap


class Wrapper:
    hello: str
    __obj: _wrap.Wrapper

    def __init__(self, hello: str) -> None:
        self.__obj = _wrap.Wrapper(hello)

    @property
    def hello(self) -> str:
        return self.__obj.hello

    @hello.setter
    def hello(self, hello: str) -> str:
        self.__obj.hello = hello
        return self.__obj.hello


async def read_beatmap(path: str) -> Wrapper:
    return await _wrap.read_beatmap(path)
