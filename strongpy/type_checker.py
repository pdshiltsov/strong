from functools import lru_cache
from typing import Any, Never, NoReturn, get_args, get_origin

from strongpy.handlers import HANDLERS


@lru_cache(None)
def analyze_type(tp):
    return get_origin(tp), get_args(tp)


def _type_checker(value, expected):
    origin, args = analyze_type(expected)

    if expected is Any:
        return True

    if expected is Never:
        return False

    if expected is NoReturn:
        return False

    if origin is None:
        return isinstance(value, expected)

    if origin in HANDLERS:
        return HANDLERS[origin](args, value, _type_checker)

    if isinstance(origin, type):
        return isinstance(value, origin)

    return isinstance(value, origin)
