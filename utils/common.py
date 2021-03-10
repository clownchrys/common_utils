from typing import Iterable, List


def batch_splits(iterable:Iterable, batch_size:int) -> List:
    batches = []
    for i in range(0, len(iterable), batch_size):
        batch = iterable[i : i + batch_size]
        batches.append(batch)
    return batches
