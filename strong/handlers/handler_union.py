from types import UnionType
from typing import Union

from strong.type_checker import _type_checker


def handler_union(origin, args, value):
    if (origin is Union) or (origin is UnionType):
        return any(_type_checker(value, arg) for arg in args)
