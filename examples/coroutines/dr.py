from collections import defaultdict
from pprint import pprint

dependencies = defaultdict(set)
dependents = defaultdict(set)
delegates = {}


def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        try:
            next(g)
        except StopIteration:
            pass
        return g
    return inner


def register(func, driver, requires):
    dependencies[func] = set(requires)
    for r in requires:
        dependents[r].add(func)
    delegates[func] = driver


def call_func(func, requires, state):
    args = [state[r] for r in requires]
    return func(*args)


def send(coro, arg):
    try:
        coro.send(arg)
    except StopIteration:
        pass


def component(requires=None):
    requires = requires or []

    def decorator(func):
        @coroutine
        def driver(gens, state):
            still_needs = set(requires)
            if not still_needs:
                yield
            while still_needs:
                still_needs.remove((yield))
            try:
                state[func] = call_func(func, requires, state)
                for d in dependents[func]:
                    send(gens[d], func)
            except Exception as e:
                state.exceptions[func] = e
        register(func, driver, requires)
        return func
    return decorator


class Broker(object):
    def __init__(self):
        self.instances = {}
        self.exceptions = {}
        self.missing = {}

    def __setitem__(self, key, value):
        self.instances[key] = value

    def __getitem__(self, key):
        return self.instances[key]

    def __contains__(self, key):
        return key in self.instances

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default


def run(state=None):
    gens = {}
    state = state or Broker()
    for c, d in delegates.items():
        gens[c] = d(gens, state)

    for c, g in gens.items():
        if not dependencies[c]:
            send(g, None)

    for g in gens.values():
        g.close()
    return state


@component()
def three():
    return 3


@component([three])
def mul_four(t):
    return 4 * t


@component([three, mul_four])
def printer(t, m):
    print t, m


pprint(run().instances)
