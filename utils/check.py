from typing import Any


def is_exception(obj: Any) -> bool:
    return issubclass(type(obj), BaseException)


def is_iterable(obj: Any) -> bool:
    try:
        iter(obj)
    except:
        return False
    else:
        return True
