import time
import sys
import traceback
import asyncio
import concurrent
from functools import wraps, partial
from enum import Enum
from typing import *


def dummy_return(value: Any):
    """
    if the func raises exception, returns dummy value
    """
    def decorator(func):
        
        @wraps(func)
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
    assert info_level in range(4), 'Argument "info_level" should be in range(4)'

    print_func = kwargs.get('print_func', print)
    wait_func = kwargs.get('wait_func', time.sleep)

    def decorator(func):
        
        @wraps(func)
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


def callback(callback: Callable, out: bool=False):
    """
    callback is a callable object with an only argument of func's return

    - out
        if out is True, func returns callback's output
        if False, func's return just passes callback
    """
    assert callable(callback), 'Argument "callback" shoud be a callable object'

    def decorator(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs) 
            _ret = callback(ret)
            if out:
                return _ret
            else:
                return ret

        return wrapper
    return decorator


def extend_enum(inherited_enum: Enum):
    """
    the decorator to extend(or inherit) Enum class
    """

    @wraps(func)
    def wrapper(added_enum):
        joined = {}
        for item in inherited_enum:
            joined[item.name] = item.value
        for item in added_enum:
            joined[item.name] = item.value
        return Enum(added_enum.__name__, joined)

    return wrapper


class asynchronous:
    """
    the decorator to make synchronous function to asynchronous one
    """
    
    def __init__(
        self,
        loop: Optional[asyncio.BaseEventLoop],
        executor: Optional[concurrent.futures.ThreadPoolExecutor],
    ):
        self.loop = loop
        self.executor = executor
        
    def __call__(self, func: Callable):
        docstrings = [
            func.__doc__,
            "\n",
            f"[Info] following kwargs are added for @{self.__class__.__qualname__}:",
            "loop     :: Optional[asyncio.BaseEventLoop]",
            "executor :: Optional[concurrent.futures.ThreadPoolExecutor]",
        ]
        func.__doc__ = "\n".join(docstrings)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            loop = kwargs.get("loop", self.loop)
            executor = kwargs.get("executor", self.executor)
            if loop is None:
                loop = asyncio.get_event_loop()
            return await loop.run_in_executor(executor, partial(func, *args, **kwargs))        
        return wrapper
