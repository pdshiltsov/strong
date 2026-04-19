def handler_dict(args, value, _type_checker):
    key_type, value_type = args
    return (
        isinstance(value, dict)
        and all(_type_checker(key, key_type) for key in value.keys())
        and all(_type_checker(val, value_type) for val in value.values())
    )
