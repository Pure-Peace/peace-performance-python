from typing import Any, Callable, Dict, Iterable


def _getter_maker(attr: str) -> Callable[[Any], Any]:
    '''Returns a getter for Wrapper(_raw) -> _raw'''
    def _fn(c: Any) -> Any:
        return getattr(c._raw, attr)
    return _fn


def _setter_maker(attr: str) -> Callable[[Any, Any], Any]:
    '''Returns a setter for Wrapper(_raw) -> _raw'''
    def _fn(c: Any, value) -> Any:
        return setattr(c._raw, attr, value)
    return _fn


def _deleter_maker(attr: str) -> Callable[[Any], Any]:
    '''Returns a deleter for Wrapper(_raw) -> _raw'''
    def _fn(c: Any) -> Any:
        return setattr(c._raw, attr, None)
    return _fn


def _mutable_property_generator(cls):
    '''Property generator for Wrapper(_raw) -> _raw (mutable)'''
    for attr in cls._raw_attrs:
        handlers = [_getter_maker(attr), _setter_maker(
            attr), _deleter_maker(attr)]
        for prefix, handler in zip(('get_', 'set_', 'del_',), handlers):
            setattr(cls, prefix + attr, handler)
        setattr(cls, attr, property(*handlers))
    return cls


def _read_only_property_generator(cls):
    '''Property generator for Wrapper(_raw) -> _raw (read only)'''
    for attr in cls._raw_attrs:
        setattr(cls, attr, property(fget=_getter_maker(attr)))
    return cls


def _get_attrs_str(target: object, attrs: Iterable[str]) -> str:
    '''Get object attrs as str'''
    return ', '.join([f'{attr}: {getattr(target, attr)}' for attr in attrs])


def _get_attrs_dict(target: object, attrs: Iterable[str]) -> Dict[str, Any]:
    '''Get object attrs as dict'''
    def _getattr(target, attr) -> Any:
        val = getattr(target, attr)
        dic = getattr(val, 'attrs_dict', None)
        return dic if dic else val
    return {attr: _getattr(target, attr) for attr in attrs}
