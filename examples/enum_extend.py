from enum import EnumMeta


class MetaClsEnumJoin(EnumMeta):
    """
    Metaclass that creates a new `enum.Enum` from multiple existing Enums.

    @code
        from enum import Enum

        ENUMA = Enum('ENUMA', {'a': 1, 'b': 2})
        ENUMB = Enum('ENUMB', {'c': 3, 'd': 4})
        class ENUMJOINED(Enum, metaclass=MetaClsEnumJoin, enums=(ENUMA, ENUMB)):
            pass

        print(ENUMJOINED.a)
        print(ENUMJOINED.b)
        print(ENUMJOINED.c)
        print(ENUMJOINED.d)
    @endcode
    """

    @classmethod
    def __prepare__(metacls, name, bases, enums=None, **kargs):
        """
        Generates the class's namespace.
        @param enums Iterable of `enum.Enum` classes to include in the new class.  Conflicts will
            be resolved by overriding existing values defined by Enums earlier in the iterable with
            values defined by Enums later in the iterable.
        """
        #kargs = {"myArg1": 1, "myArg2": 2}
        if enums is None:
            raise ValueError('Class keyword argument `enums` must be defined to use this metaclass.')
        ret = super().__prepare__(name, bases, **kargs)
        for enm in enums:
            for item in enm:
                ret[item.name] = item.value  #Throws `TypeError` if conflict.
        return ret

    def __new__(metacls, name, bases, namespace, **kargs):
        return super().__new__(metacls, name, bases, namespace)
        #DO NOT send "**kargs" to "type.__new__".  It won't catch them and
        #you'll get a "TypeError: type() takes 1 or 3 arguments" exception.

    def __init__(cls, name, bases, namespace, **kargs):
        super().__init__(name, bases, namespace)
        #DO NOT send "**kargs" to "type.__init__" in Python 3.5 and older.  You'll get a
        #"TypeError: type.__init__() takes no keyword arguments" exception.


if __name__ == '__main__':
    from enum import Enum

    ENUM_A = Enum('ENUMA', {'a': 1, 'b': 2})
    ENUM_B = Enum('ENUMB', {'c': 3, 'd': 4})
    class ENUMJOINED(
        Enum, metaclass=MetaClsEnumJoin, enums=(ENUM_A, ENUM_B)):
        e = 5
        f = 6