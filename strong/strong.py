import inspect
from functools import wraps

from strong.type_checker import _type_checker


def strong(func):
    sig = inspect.signature(func)
    return_type = sig.return_annotation

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for key, value in bound.arguments.items():
            expected = sig.parameters[key].annotation

            if expected is inspect._empty:
                continue

            if not _type_checker(value, expected):
                raise TypeError(
                    f"argument '{key}' must be {expected}, got {type(value)}"
                )

        result = func(*args, **kwargs)

        if return_type is not inspect._empty and not _type_checker(result, return_type):
            raise TypeError(f"result {result} is not {return_type}")

        return result

    return wrapper
