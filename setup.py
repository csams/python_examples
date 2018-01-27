import sys
from setuptools import setup, find_packages

runtime = set([
    "futures",
    "six",
    "toposort",
])

if sys.version_info.major == 2:
    runtime.add("importlib")

develop = set([
    "flake8",
    "pytest",
    "ipython",
])

if __name__ == "__main__":
    setup(
        name="python_examples",
        author_email="cwsams@gmail.com",
        license="Apache 2",
        packages=find_packages(),
        install_requires=list(runtime),
        extras_require={
            "develop": list(runtime | develop),
        },
        include_package_data=True
    )
