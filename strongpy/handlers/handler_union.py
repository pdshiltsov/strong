def handler_union(args, value, _type_checker):
    return any(_type_checker(value, arg) for arg in args)
