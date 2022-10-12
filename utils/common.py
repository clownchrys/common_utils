from typing import Iterable, List
import inspect
import psutil
import sys


def batch_splits(iterable: Iterable, batch_size: int) -> List:
    batches = []
    for i in range(0, len(iterable), batch_size):
        batch = iterable[i : i + batch_size]
        batches.append(batch)
    return batches


def line_at():
    current_frame = inspect.currentframe()
    outer_frame = current_frame.f_back

    result = (
        outer_frame.f_code.co_filename,
        outer_frame.f_lineno
    )
    return result


def print_eval(evaluatable: str):
    print(f"{evaluatable} = {eval(evaluatable)!r}")
    
    
def get_multiprocess_count(mem_threshold_percent: int or float, recall: float = 1.0) -> int:
    mem = psutil.virtual_memory()
    mem_capacity = max(mem_threshold_percent // (mem.percent * recall) - 1, 1)
    count = min(sys.cpu_count(), mem_capacity)
    print(f"multiprocess_count: {count}")
    return count
