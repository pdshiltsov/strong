def handler_stronglist(args, value, _type_checker):
    if args == value.annotations:
        return True
    return False
