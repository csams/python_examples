import logging
import six
from collections import deque

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def naive_hash(args, kwargs):
    return hash(str(args) + str(kwargs))


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
        check_evict()

    def decorator(func):
        @six.wraps(func)
        def inner(*args, **kwargs):
            key = naive_hash(args, kwargs)
            if key not in cache:
                memoize(key, func(*args, **kwargs))
            return cache[key]
        return inner

    return decorator


class Memoizer(object):
    def __init__(self, cache_size=5):
        self.cache = {}
        self.args_queue = deque()
        self.cache_size = cache_size

    def __call__(self, func):
        @six.wraps(func)
        def inner(*args, **kwargs):
            key = naive_hash(args, kwargs)
            if key not in self.cache:
                self._memoize(key, func(*args, **kwargs))
            return self.cache[key]
        return inner

    def _check_evict(self):
        if len(self.args_queue) > self.cache_size:
            old_key = self.args_queue.popleft()
            del self.cache[old_key]

    def _memoize(self, key, value):
        self.cache[key] = value
        self.args_queue.append(key)
        self._check_evict()


def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@Memoizer(cache_size=10)
def memfib(n):
    if n < 2:
        return 1
    return memfib(n - 1) + memfib(n - 2)
