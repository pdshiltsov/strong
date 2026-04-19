import inspect
from functools import wraps
from typing import Union, Literal
from typing import get_origin, get_args
from types import UnionType


def _type_checker(value, expected):
    origin = get_origin(expected)
    args = get_args(expected)
    
    # for int, str, list, etc
    if origin is None: 
        return isinstance(value, expected)

    # for list[...]
    if origin is list and isinstance(value, list):
        (item_type,) = args
        
        return isinstance(value, list) and all(
            _type_checker(element, item_type) for element in value
        )

    # for dict[...] 
    if origin is dict and isinstance(value, dict):
        key_type, value_type = args
        return isinstance(value, dict) and all(
            _type_checker(key, key_type) for key in value.keys()
        ) and all(
            _type_checker(val, value_type) for val in value.values()
        )

    # for Union
    if (origin is Union) or (origin is UnionType):
        return any(_type_checker(value, arg) for arg in args)

    # for Literal
    if origin is Literal:
        return value in args

    # for tuple cases
    if origin is tuple and isinstance(value, tuple):
        if len(args) == 2 and args[1] is Ellipsis:
            return all(
                _type_checker(val, args[0]) for val in value 
            )

        elif len(args) == len(value):
            return all(
                _type_checker(val, exp) for val, exp in zip(value, args)
            )

        elif len(args) != len(value):
            return False

        else:
            return isinstance(value, tuple)

    return isinstance(value, origin)
