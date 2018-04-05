"""
This module contains a PEP 302 importer and loader for packages and modules
over an http/s connection.

Add an instance of the HttpImporter to the sys.meta_path like this:

sys.meta_path.append(HttpImporter("http://localhost:5000"))
"""

import imp
import logging
import os
import requests
import sys


log = logging.getLogger(__name__)


def download(path, expect_json=False):
    log.debug("Trying to download %s" % path)
    try:
        resp = requests.get(path, verify=False)
        resp.raise_for_status()
        return resp.json() if expect_json else resp.text
    except Exception as ex:
        log.exception(ex)


class HttpImporter(object):
    """
    Hook into python's import machinery so standard import statements can be
    used to load from an http(s) endpoint.
    """

    log = logging.getLogger("HttpImporter")

    def __init__(self, path, import_prefix="remote"):
        if not path.startswith(("http://", "https://")):
            raise ImportError("HttpImporter handles http(s) paths, not %s" % path)
        self.path = path.rstrip("/")
        self.import_prefix = import_prefix

    def find_module(self, fullname, paths=None):
        """
        Returns a HttpLoader for remote files.
        """
        base = self.path if not paths else paths[0]
        if fullname == self.import_prefix:
            return HttpLoader(self.path, None, True)

        if not fullname.startswith(self.import_prefix) or not base.startswith("http"):
            return None

        sub_paths = download(base, expect_json=True)
        dir_contents = set(sub_paths)

        fullname = fullname[(len(self.import_prefix) + 1):]
        name = fullname.split(".")[-1]
        if name not in dir_contents and name + ".py" not in dir_contents:
            return None

        is_pkg = False
        if name in dir_contents:
            is_pkg = True
            path = os.path.join(base, name)
            data = download(os.path.join(path, "__init__.py"))
        else:
            path = os.path.join(base, name + ".py")
            data = download(path)

        if data is not None:
            return HttpLoader(path, data, is_pkg)

        raise ImportError("Could not find %s" % fullname)

    def iter_modules(self, prefix=''):
        """
        Allows this importer to work with other pkgutil functions like
        walk_packages.
        """
        if self.path is None or not os.path.isdir(self.path):
            return

        yielded = {}
        try:
            filenames = os.listdir(self.path)
        except OSError:
            # ignore unreadable directories like import does
            filenames = []
        filenames.sort()  # handle packages before same-named modules

        for fn in filenames:
            modname, _ = os.path.splitext(fn)
            if modname == '__init__' or modname in yielded:
                continue

            path = os.path.join(self.path, fn)
            ispkg = False

            if os.path.isdir(path):
                ispkg = True
                modname = fn

            if modname and '.' not in modname:
                yielded[modname] = 1
                yield prefix + modname, ispkg


class HttpLoader(object):
    log = logging.getLogger("HttpLoader")

    def __init__(self, filename, source, is_pkg):
        self.log.debug("Creating loader for %s" % filename)
        self.filename = filename
        self.source = source or ""
        self.is_pkg = is_pkg
        self.code = None

    def is_package(self, fullname):
        return self.is_pkg

    def get_source(self, fullname=None):
        return self.source

    def get_code(self, fullname):
        if not self.code:
            self.code = compile(self.source, self.filename, "exec")
        return self.code

    def get_filename(self, path=None):
        return self.filename

    def load_module(self, fullname):
        self.log.debug("Loading %s" % fullname)
        try:
            return sys.modules[fullname]
        except KeyError:
            pass

        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        if self.is_package(fullname):
            mod.__loader__ = self
            mod.__path__ = [self.filename]
            mod.__package__ = fullname
        else:
            mod.__loader__ = self
            mod.__file__ = self.filename
            mod.__package__ = fullname.rpartition(".")[0]

        try:
            self.code = self.get_code(fullname)
            exec(self.code, mod.__dict__)
            self.log.debug("Loaded %s" % fullname)
            return sys.modules[fullname]
        except Exception as ex:
            self.log.exception(ex)
            raise ImportError(ex)
