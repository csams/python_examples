from setuptools import setup, find_packages

runtime = {
    "futures",
    "importlib",
    "six",
    "toposort",
}

develop = {
    "flake8",
    "pytest",
}

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
