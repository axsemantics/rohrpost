import pkg_resources  # part of setuptools

try:
    dist = pkg_resources.get_distribution("rohrpost")
except pkg_resources.DistributionNotFound:
    # This happens when the package isn't installed
    __version__: str = "0.0.0"
else:
    __version__ = dist.version

VERSION: str = __version__
