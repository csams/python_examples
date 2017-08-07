import importlib
import logging
import pkgutil
import six

log = logging.getLogger(__name__)


def get_name(obj):
    if six.callable(obj):
        return ".".join([obj.__module__, obj.__name__])
    return str(obj)


def naive_hash(args, kwargs):
    return hash(str(args) + str(kwargs))


def load_components(path):
    prefix = path.replace('/', '.') + '.'
    path = path.replace('.', '/')
    for _, name, _ in pkgutil.walk_packages(path=[path], prefix=prefix):
        log.debug("Importing %s" % name)
        importlib.import_module(name)
