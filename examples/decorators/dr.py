import logging
import operator

log = logging.getLogger(__name__)
dependencies = {}
delegates = {}


class MissingRequirements(Exception):
    pass


def validate_requirements(requires, state):
    missing = [r for r in requires if r not in state]
    if missing:
        raise MissingRequirements(missing)


def register(func, delegate, requires):
    dependencies[func] = set(requires)
    delegates[func] = delegate


def call_func(func, requires, state):
    args = [state[r] for r in requires]
    return func(*args)


def component(requires=[]):
    def decorator(func):
        def delegate(state):
            validate_requirements(requires, state)
            return call_func(func, requires, state)
        register(func, delegate, requires)
        return func
    return decorator


def run_order(graph):
    graph = graph.copy()
    all_deps = reduce(operator.or_, graph.values(), set())
    graph.update({l: set() for l in all_deps if l not in graph})
    results = []
    seen = set()
    while graph:
        n = set(n for n in graph if not graph[n])
        if not n:
            raise Exception("Circular dependency: %s" % graph)
        results.extend(n)
        seen |= n
        graph = {k: (v - n) for k, v in graph.items() if k not in seen}
    return results


def run(state={}):
    state = state or {}
    for c in run_order(dependencies):
        if c not in state and c in delegates:
            try:
                state[c] = delegates[c](state)
            except MissingRequirements as m:
                log.debug("[%s] is missing %s" % (c.__name__, str(m.args[0])))
            except Exception as ex:
                log.exception(ex)
    return state
