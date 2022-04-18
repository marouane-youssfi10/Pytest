from typing import Callable
import pytest

from api.fibonacci.dynamic import fibonacci_dynamic
from api.fibonacci.naive import fibonacci_naive
from api.fibonacci.cashed import fibonacci_cached, fibonacci_lru_cached

from api.fixtures import time_tracker
# @my_parametrized(identifiers="n,expected", values=[(0, 0), (1, 1), (2, 1), (20, 6765)])
@pytest.mark.parametrize("fib_func", [
    fibonacci_naive, fibonacci_cached, fibonacci_lru_cached, fibonacci_dynamic
        ])
@pytest.mark.parametrize("n,expected", [(1, 1)])
def test_fibonacci(time_tracker, fib_func: Callable[[int], int], n: int, expected: int) -> None:
    res = fib_func(n)
    assert res == expected