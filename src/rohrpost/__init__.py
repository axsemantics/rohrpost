import importlib.metadata

try:
    __version__: str = importlib.metadata.version("rohrpost")
except importlib.metadata.PackageNotFoundError:
    # This happens when the package isn't installed
    __version__ = "0.0.0"

VERSION: str = __version__
