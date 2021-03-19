from typing import Iterable, List
import inspect


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
