from typing import get_args, get_origin

from strong.handlers import HANDLERS


def _type_checker(value, expected):
    origin = get_origin(expected)
    args = get_args(expected)

    if origin is None:
        return isinstance(value, expected)

    if origin in HANDLERS:
        return HANDLERS[origin](args, value, _type_checker)

    if isinstance(origin, type):
        return isinstance(value, origin)

    return isinstance(value, origin)
