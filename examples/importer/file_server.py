#!/usr/bin/env python
"""
This little http server sends files and directory listings to the http_importer.
Start it in a directory where you have scripts you want to expose.
"""

import logging
import os
from flask import Flask, current_app, jsonify, send_from_directory

app = Flask(__name__)
isdir = os.path.isdir
isfile = os.path.isfile


def is_pkg(path):
    return isdir(path) and isfile(os.path.join(path, "__init__.py"))


def dir_listing(path):
    names = os.listdir(path)
    vals = dict((n, is_pkg(os.path.join(path, n))) for n in names)
    return jsonify(vals)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catchall(path):
    full_path = os.path.join(current_app.root_path, path)
    if isdir(full_path):
        return dir_listing(full_path)

    directory = os.path.dirname(full_path)
    base = os.path.basename(full_path)
    return send_from_directory(directory=directory, filename=base)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run()
