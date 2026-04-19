def handler_list(args, value, _type_checker):
    (item_type,) = args

    return isinstance(value, list) and all(
        _type_checker(element, item_type) for element in value
    )
