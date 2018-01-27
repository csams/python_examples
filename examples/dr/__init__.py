import six
import traceback
from toposort import toposort_flatten as toposort

DELEGATES = {}


class MissingRequirements(Exception):
    pass


class Delegate(object):
    def __init__(self, comp, requires, optional):
        self.comp = comp
        self.requires = requires
        self.optional = optional
        self.dependences = set(requires) | set(optional)

    def __call__(self, broker):
        missing = set(self.requires) - set(broker)
        if missing:
            raise MissingRequirements(missing)
        args = [broker[a] for a in self.requires]
        args.extend(broker.get(a) for a in self.optional)
        return self.comp(*args)


def component(*requires, **kwargs):
    def inner(comp):
        DELEGATES[comp] = Delegate(comp, requires, kwargs.get("optional", []))
        return comp
    return inner


def run_order(graph):
    return toposort({d: v.dependences for d, v in graph.items()}, sort=False)


def run(results=None):
    results = results or {}
    for c in run_order(DELEGATES):
        if c in DELEGATES and c not in results:
            try:
                results[c] = DELEGATES[c](results)
            except MissingRequirements as mr:
                six.print_(mr)
            except Exception as ex:
                traceback.print_exc()
    return results
