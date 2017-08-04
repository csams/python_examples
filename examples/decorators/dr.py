import logging
from toposort import toposort_flatten

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


def run(state={}):
    state = state or {}
    for c in toposort_flatten(dependencies):
        if c not in state and c in delegates:
            try:
                state[c] = delegates[c](state)
            except MissingRequirements as m:
                log.debug("[%s] missing %s" % (c.__name__, str(m.args[0])))
            except Exception as ex:
                log.exception(ex)
    return state
