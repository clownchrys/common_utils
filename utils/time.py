from datetime import datetime
from functools import wraps
from contextlib import contextmanager


class ETA:
    def __init__(self, total_length: int):
        self.init_time = datetime.now()
        self.total_length = total_length

    def __call__(self, current_position: int):
        if current_position:
            cur_time = datetime.now()
            rest_length = self.total_length - current_position
            per_time = (cur_time - self.init_time) / current_position
            return cur_time + (rest_length * per_time)
        
        else:
            return float('inf')


class TimeElapsed:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ts = datetime.now()
            print(f"[{ts}] {func.__qualname__!r} begins")

            ret = func(*args, **kwargs)

            te = datetime.now()
            print(f"[{te}] {func.__qualname__!r} ends (elapsed: {te - ts})")

            return ret
        return wrapper
    
    @contextmanager
    def contextmanager(name: str = "unknown"):
        ts = datetime.now()
        print(f"[{ts}] {name!r} begins")

        yield

        te = datetime.now()
        print(f"[{te}] {name!r} ends (elapsed: {te - ts})")
