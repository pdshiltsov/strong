from copy import deepcopy

from strongpy.type_checker import _type_checker


class StrongList:
    ''' def __init__(self, annotation, obj):
        self.annotation = annotation
        self.__data = []

        for item in deepcopy(obj):
            if _type_checker(obj, annotation):
                self.__data.append(obj)
            else:
                raise TypeError(f"{self.__name__}"
                    f"only accepts {self.annotation}, not {type(item)}") 
    '''
    def __class_getitem__(cls, annotation):
        class TypedStrongList(cls):
            def __init__(self, obj):
                self.__data = []
                
                for item in deepcopy(obj):
                    if _type_checker(obj, annotation):
                        self.__data.append(obj)
                    else:
                        raise TypeError(f"{self.__name__}"
                        f"only accepts {self.annotation}, not {type(item)}") 


            def __getitem__(self, key):
                if hasattr(self.__data[key], "__hash__"):
                    return self.__data[key]

                result = deepcopy(self.__data[key])
                return result
            
            
            def __iter__(self):
                return deepcopy(self.__data)

            def __len__(self):
                return len(self.__data)
            
        return TypedStrongList
