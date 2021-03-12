import time
import sys
import traceback
from typing import Any, Callable


def retry(tries:int, wait:(int or float), exp:bool=False, info_level:int=2, raise_exc:bool=True, dummy_return:Any=None, **kwargs):
    """
    - info_level
        0: no info served
        1: only minimal info
        2: detailed info when last try has failed
        3: only detailed info

    - raise_exc
        whether raise exception or not, if all tries have failed
        dummy_return will be returned when False

    - kwargs
        print_func: print, logger.warn, etc...
    """
    assert info_level in range(4)
    print_func = kwargs.get('print_func', print)

    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except:
                    time.sleep(wait ** i if exp else wait)
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

            if raise_exc:
                raise Exception(f"Retry exceed: tries={tries!r}")
            else:
                return dummy_return

        return wrapper
    return decorator


def callback(Callable: Callable):
    """
    Callable has an argument with func's return
    """
    assert callable(Callable)

    def decorator(func):
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            Callable(ret)
            return ret
        
        return wrapper
    return decorator
