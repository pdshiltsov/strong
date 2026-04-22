def handler_strongdict(args, value, _type_cheker):
    if args == value.annotations:
        return True
    return False
