from setuptools import setup

from rohrpost import __version__


def read(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="rohrpost",
    version=__version__,
    description="rohrpost WebSocket protocol for ASGI",
    long_description=read("README.rst"),
    url="https://github.com/axsemantics/rohrpost",
    author="Tobias Kunze",
    author_email="tobias.kunze@ax-semantics.com",
    license="MIT",
    python_requires=">=3.4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    packages=["rohrpost"],
)
