__version__ = "0.1.0"

import sys
import zlib as zlib_original

from . import gzip_adapter as best_gzip
from . import zlib_adapter as best_zlib


def enable() -> None:
    """Enable the adapter."""
    sys.modules["zlib"] = best_zlib
    sys.modules["gzip"] = best_gzip


def disable() -> None:
    """Disable the adapter restore the original zlib."""
    sys.modules["zlib"] = zlib_original
    sys.modules["gzip"] = zlib_original
