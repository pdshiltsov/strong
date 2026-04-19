from strong.type_checker import _type_checker


def handler_list(origin, args, value):
    if origin is list and isinstance(value, list):
        (item_type,) = args

        return isinstance(value, list) and all(
            _type_checker(element, item_type) for element in value
        )
