from typing import Iterable, Collection, Callable, TypeVar
from functools import reduce
from itertools import chain, groupby, zip_longest


Value = TypeVar("Value")
Stream = TypeVar("Stream")


class functional:
    _initial_missing = object()
    
    def __init__(self, obj: Iterable):
        self.pipe = iter(obj)
        
    def map(self, func: Callable) -> Stream:
        self.pipe = map(func, self.pipe)
        return self
    
    def flatmap(self, func: Callable) -> Stream:
        self.pipe = chain(*map(func, self.pipe))
        return self
    
    def filter(self, func: Callable) -> Stream:
        self.pipe = filter(func, self.pipe)
        return self
    
    def groupby(self, key: Callable) -> Stream:
        pipe = self.pipe
        pipe = sorted(pipe, key=key)
        pipe = groupby(pipe, key=key)
        self.pipe = map(lambda kv: (kv[0], list(kv[1])), pipe)
        return self
    
    def zip(self, *others: Iterable) -> Stream:
        self.pipe = zip(self.pipe, *map(iter, others))
        return self
    
    def zip_longest(self, *others: Iterable, fillvalue=None) -> Stream:
        self.pipe = zip_longest(self.pipe, *map(iter, others), fillvalue=fillvalue)
        return self
    
    def reduce(self, func: Callable, initial: Value = _initial_missing) -> Value:
        if initial == self._initial_missing:
            return reduce(func, self.pipe)
        else:
            return reduce(func, self.pipe, initial)
    
    def collect(self, collection: Collection) -> Value:
        return collection(self.pipe)
