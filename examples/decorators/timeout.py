import functools
import random
import six
import time
from concurrent.futures import TimeoutError, ThreadPoolExecutor as Pool

pool = Pool()


def timeout(duration=1.0, default=None):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            future = pool.submit(func, *args, **kwargs)
            try:
                return future.result(duration)
            except TimeoutError:
                six.print_("Timed out!")
                return default
        return inner
    return decorator


@timeout(duration=2.0)
def flaky():
    r = random.randint(0, 5)
    six.print_("Got: ", r)
    time.sleep(r)
    return r


if __name__ == "__main__":
    six.print_(flaky())
