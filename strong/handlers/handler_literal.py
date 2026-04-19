from typing import Literal


def handler_literal(origin, args, value):
    if origin is Literal:
        return value in args
