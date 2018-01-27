import functools
import random
import six
from examples.util import get_name


def retry(num_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            exception = None
            attempts = num_retries + 1
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    six.print_("%s attempt %s failed!" % (get_name(func), attempt))
                    exception = ex
            raise exception
        return inner
    return decorator


@retry(num_retries=5)
def flaky():
    if random.random() < 0.5:
        raise Exception("Boom!")
    return "Success!"
