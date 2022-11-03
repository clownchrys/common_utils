from typing import Iterable, Collection, Callable, Tuple, TypeVar
from functools import reduce
from itertools import chain, groupby, zip_longest, tee


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
    
    def split(self, n: int) -> Tuple[Stream]:
        return tuple(map(functional, tee(self.pipe, n)))
    
    def __iter__(self):
        return iter(self.pipe)
    
    
if __name__ == "__main__":
    # _non_iterable = 1
    # functional(_non_iterable) # TypeError: 'int' object is not iterable
    
    _iterable = [1, 2, 3, 4]
    
    result1 = functional(_iterable).map(lambda x: x + 1).collect(tuple)
    print(result1) # (2, 3, 4, 5)
    
    tmp1, tmp2 = functional(_iterable).map(lambda x: x + 1).split(2)
    tmp1 = tmp1.filter(lambda x: x > 3) # 4, 5
    tmp2 = tmp2.filter(lambda x: x <= 3) # 2, 3
    result2 = tmp1.zip_longest(tmp2, result1).collect(list)
    print(result2) # [(4, 2, 2), (5, 3, 3), (None, None, 4), (None, None, 5)]
    
    result3 = functional(result1).zip(result2).collect(dict)
    print(result3) # {2: (4, 2, 2), 3: (5, 3, 3), 4: (None, None, 4), 5: (None, None, 5)}
