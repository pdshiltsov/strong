import inspect


def handler_callable(args, value, _type_checker):
    if not callable(value):
        return False

    if not args:
        return True

    arg_types, return_type = args

    if arg_types is Ellipsis:
        return True

    try:
        sig = inspect.signature(value)
    except (ValueError, TypeError):
        return True

    parameters = list(sig.parameters.values())

    if len(parameters) != len(arg_types):
        return False

    for parameter, expected in zip(parameters, arg_types, strict=True):
        if parameter.annotation is inspect._empty:
            continue
        if not _type_checker(parameter.annotation, expected):
            return False

    return True
