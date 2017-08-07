import logging
import six
from collections import deque

from examples.util import naive_hash

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def memoizer(cache_size=5):
    cache = {}
    args_queue = deque()
    cache_size = cache_size

    def check_evict():
        if len(args_queue) > cache_size:
            old_key = args_queue.popleft()
            del cache[old_key]

    def memoize(key, value):
        cache[key] = value
        args_queue.append(key)

    def decorator(func):
        @six.wraps(func)
        def inner(*args, **kwargs):
            key = naive_hash(args, kwargs)
            if key not in cache:
                memoize(key, func(*args, **kwargs))
            check_evict()
            return cache[key]
        return inner

    return decorator


@memoizer(cache_size=10)
def memfib(n):
    if n < 2:
        return 1
    return memfib(n - 1) + memfib(n - 2)

# same as
#
# memo = memoizer(cache_size=10)
#
# def memfib(n):
#     if n < 2:
#         return 1
#     return memfib(n - 1) + memfib(n - 2)
#
# memfib = memo(memfib)


class Memoizer(object):
    def __init__(self, cache_size=5):
        self.cache = {}
        self.args_queue = deque()
        self.cache_size = cache_size

    def _check_evict(self):
        if len(self.args_queue) > self.cache_size:
            old_key = self.args_queue.popleft()
            del self.cache[old_key]

    def _memoize(self, key, value):
        self.cache[key] = value
        self.args_queue.append(key)

    def __call__(self, func):
        @six.wraps(func)
        def inner(*args, **kwargs):
            key = naive_hash(args, kwargs)
            if key not in self.cache:
                self._memoize(key, func(*args, **kwargs))
            self._check_evict()
            return self.cache[key]
        return inner


@Memoizer(cache_size=10)
def memfib2(n):
    if n < 2:
        return 1
    return memfib2(n - 1) + memfib2(n - 2)


# same as
#
# memo = Memoizer(cache_size=10)
#
# def memfib2(n):
#     if n < 2:
#         return 1
#     return memfib2(n - 1) + memfib2(n - 2)
#
# memfib2 = memo(memfib2)
