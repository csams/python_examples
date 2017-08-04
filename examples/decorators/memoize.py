import logging
import six
from collections import deque

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class Memoizer(object):
    def __init__(self, cache_size=5):
        self.cache = {}
        self.args_queue = deque()
        self.cache_size = cache_size

    def __call__(self, func):
        @six.wraps(func)
        def inner(*args, **kwargs):
            key = self.naive_hash(args, kwargs)
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

    @staticmethod
    def naive_hash(args, kwargs):
        return hash(str(args) + str(kwargs))


def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)


@Memoizer(cache_size=10)
def memfib(n):
    if n < 2:
        return 1
    return memfib(n - 1) + memfib(n - 2)
