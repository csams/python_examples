import random
import time

from examples.decorators.dr import component
from examples.decorators.memoizer import Memoizer
from examples.decorators.retries import retry
from examples.decorators.timeit import timeit


@component()
def some_input():
    return random.randint(0, 2)


@component()
def three():
    return 3


@component([some_input, three])
def add(a, b):
    return a + b


@component([some_input, three])
@retry(num_retries=5)
def flaky_add(a, b):
    if random.random() < 0.5:
        raise Exception("Flaky Add Goes Boom!")
    return a + b + 1


@component()
def boom():
    raise Exception("Boom!")


@component([add])
@timeit
@Memoizer()
def long_running(a):
    time.sleep(a)
    return a


class Common(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.obj)


@component([add])
class A(Common):
    pass


@component([flaky_add])
class B(Common):
    pass


@component(["c"])
class C(Common):
    pass
