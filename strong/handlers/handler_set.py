def handler_set(args, value, _type_checker):
    if not isinstance(value, set):
        return False

    if not args:
        return True

    (item_type,) = args

    return all(
        _type_checker(val, item_type) for val in value
    )