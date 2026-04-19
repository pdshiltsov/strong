def handler_tuple(args, value, _type_checker):
    
    if len(args) == 2 and args[1] is Ellipsis:
        return all(_type_checker(val, args[0]) for val in value)

    elif len(args) == len(value):
        return all(
            _type_checker(val, exp) for val, exp in zip(value, args, strict=True)
        )

    elif len(args) != len(value):
        return False

    else:
        return isinstance(value, tuple)
