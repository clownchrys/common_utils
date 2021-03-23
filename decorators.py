import time
import sys
import traceback
from typing import Any, Callable
from enum import Enum


def dummy_return(value: Any):
    """
    if the func raises exception, returns dummy value
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except:
                ret = value
            finally:
                return ret

        return wrapper
    return decorator


def retry(tries: int, wait: (int or float), exp: bool=False, info_level: int=2, **kwargs):
    """
    func tries up to designated tries

    - info_level
        0: no info served
        1: only minimal info
        2: detailed info when last try has failed
        3: only detailed info

    - kwargs
        print_func: print (as default) -> logger.warn, etc...
        wait_func: time.sleep (as default) -> asyncio.wait, etc...
    
    - example with dummy_return
        @dummy_return(value=None)  # if retry decorator raises exception, this returns dummy value
        @retry(tries=3, wait=2)
        def func(*args, **kwargs):
            ...
    """
    assert info_level in range(4)
    print_func = kwargs.get('print_func', print)
    wait_func = kwargs.get('wait_func', time.sleep)

    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except:
                    wait_func(wait ** i if exp else wait)

                    _type, _value, _tb = sys.exc_info()
                    minimal_info = f"{_value} {_type}"
                    detailed_info = traceback.format_exc()

                if info_level == 0:
                    continue
                elif info_level == 1:
                    logging_info = minimal_info
                elif info_level == 2:
                    logging_info = minimal_info if (i < tries) else detailed_info
                elif info_level == 3:
                    logging_info = detailed_info
                else:
                    pass  # pass without any exception, due to working assert statement above
                print_func(f"Try {func.__qualname__!r} ({i}/{tries}): {logging_info}")

            raise Exception(f"Tries exceeded: tries={tries!r}")

        return wrapper
    return decorator


def callback(Callable: Callable):
    """
    Callable has an only argument of func's return
    """
    assert callable(Callable)

    def decorator(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            Callable(ret)
            return ret
        
        return wrapper
    return decorator


def extend_enum(inherited_enum: Enum):
    """
    the decorator to extend(inherit) Enum class
    """

    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper
