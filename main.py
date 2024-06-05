from collections import OrderedDict
from typing import Any, Callable, List
import time


class Storage:
    def __init__(self, value: Any, start_time: float) -> None:
        self.value = value
        self.start_time = start_time


"""
TASK 1 & 2
"""


def cache(cache_size: int = 1) -> Callable:
    def cache_decorator(func: Callable) -> Callable:
        storage = {}

        def wrapper(*args, **kwargs) -> Any:
            print("---------------------------")
            key = func.__name__ + str((*args, *(kwargs.values())))

            if key in storage:
                print("Retrieving from cache")
                return storage[key].value

            if len(storage) == cache_size:
                key_for_delete = next(iter(storage))
                del storage[key_for_delete]

            print("Computing result")
            result = func(*args, **kwargs)

            storage[key] = Storage(result, time.time())

            return result

        return wrapper

    return cache_decorator


"""
TASK 3
"""


def cache_with_time(cache_time: int = 1) -> Callable:
    def cache_with_time_decorator(func: Callable) -> Callable:
        storage: OrderedDict[str, Storage] = OrderedDict()

        def wrapper(*args, **kwargs):
            print("---------------------------")
            current_time = time.time()

            while storage:
                _, storage_obj = next(iter(storage.items()))
                if current_time - storage_obj.start_time > cache_time:
                    storage.popitem(last=False)
                else:
                    break

            key = f"{func.__name__}{args}{kwargs}"
            if key in storage:
                print("Retrieving from cache")
                return storage[key].value

            print("Computing result")
            result = func(*args, **kwargs)

            storage[key] = Storage(result, current_time)

            return result

        return wrapper

    return cache_with_time_decorator


@cache()
def some_sum_func(a: List[int], b: List[int]) -> None:
    return a + b


@cache_with_time()
def some_reverse_func(a: List[int], b: List[int]) -> None:
    return (a + b)[::-1]


print(some_sum_func([1], [2]))
print(some_sum_func([1], [2]))
print(some_sum_func([2], [3]))
print(some_sum_func([1], [2]))

print(some_reverse_func([1], [2]))
print(some_reverse_func([1], [2]))
print(some_reverse_func([2], [3]))
time.sleep(2)
print(some_reverse_func([1], [2]))
