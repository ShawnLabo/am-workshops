import sys
import random

def _fibonacci(n):
    if n in [0, 1]:
        return 1
    return _fibonacci(n - 2) + _fibonacci(n - 1)


def run(min=None, max=None):
    if not min:
        min = 10
    if not max:
        max = random.randint(min, 30)
    fib = []
    for n in range(min, max):
        fib.append(_fibonacci(n))
    print(fib)
    return fib