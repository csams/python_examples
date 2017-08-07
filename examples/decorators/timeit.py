import logging
import functools
import time

from examples.util import get_name

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# *args and **kwargs

# closure

# Here's a more useful example. It's slightly more complicated because it
# defines and returns an inner function instead of just returning the original
# argument. It also demonstrates a function closure as well as *args and **kwargs.


def timeit(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start = time.clock()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.clock() - start
            log.debug("%s took %s" % (get_name(func), duration))

    # note that we return inner instead of func!
    return inner


@timeit
def sum_to_n(a):
    """Let's sum some numbers!"""

    total = a
    for x in range(a):
        total += x
        time.sleep(1)
    return total
