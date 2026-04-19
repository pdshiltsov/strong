import inspect
from functools import wraps

from strong.type_checker import _type_checker


def strong(func):
    sig = inspect.signature(func)
    return_type = sig.return_annotation
    func_name = func.__name__
    ret_name = return_type.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for key, value in bound.arguments.items():
            expected = sig.parameters[key].annotation

            if expected is inspect._empty:
                continue

            if not _type_checker(value, expected):
                exp_name = expected.__name__
                val_name = type(value).__name__

                raise TypeError(
                    f"{func_name} argument '{key}' expected {exp_name}, got {val_name}"
                )

        result = func(*args, **kwargs)

        if return_type is not inspect._empty and not _type_checker(result, return_type):
            raise TypeError(f"{func_name} result {result} is not {ret_name}")

        return result

    return wrapper
