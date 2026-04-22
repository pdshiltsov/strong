from copy import deepcopy


class _StrongDict:
    def __init__(self, _type_checker):
        self._type_checker = _type_checker

    def __class_getitem__(self, annotation):
        class TypedStrongDict:
            def __init__(self, obj):
                self.__data = {}
                self.annotation = annotation

                for key, value in obj.items():
                    if not _type_checker(key, self.annotation[0]):
                        raise TypeError(f"{self.name} - incorrect type for key, "
                                    f"got {type(key)}, expected {self.annotation[0]}")
                    
                    if not _type_checker(key, self.annotation[1]):
                        raise TypeError(f"{self.name} - incorrect type for value"
                                    f"got {type(value)}, expected {self.annotation[1]}")
                    
                    self.__data[deepcopy(key)] = deepcopy(value)

            def __getitem__(self, key):
                return deepcopy(self.__data[key])

            def keys(self):
                return deepcopy(self.__data.keys())

            def values(self):
                return deepcopy(self.__data.values())

            def items(self):
                return deepcopy(self.__data.items())

        return TypedStrongDict
