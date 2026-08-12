from .api import Api, CloudVpsAPIError
from .resources import package_version

__author__ = "Grudin Anton"
__version__ = package_version()
__license__ = "MIT"
VERSION = __version__

__all__ = ["Api", "CloudVpsAPIError", "VERSION", "__version__"]
