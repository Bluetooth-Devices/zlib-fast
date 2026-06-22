__version__ = "0.2.1"

import gzip as gzip_original
import sys
import zlib as zlib_original
from contextlib import contextmanager
from typing import Iterator

from . import gzip_adapter as best_gzip
from . import zlib_adapter as best_zlib


def enable() -> None:
    """Enable the adapter."""
    sys.modules["zlib"] = best_zlib
    sys.modules["gzip"] = best_gzip


def disable() -> None:
    """Disable the adapter restore the original zlib."""
    sys.modules["zlib"] = zlib_original
    sys.modules["gzip"] = gzip_original


@contextmanager
def enabled() -> Iterator[None]:
    """Enable the adapter for the duration of the ``with`` block.

    Restores whichever ``zlib``/``gzip`` modules were installed before the
    block on exit — even if the block raises. Nests safely and never leaks
    the ``sys.modules`` swap.
    """
    prev_zlib = sys.modules.get("zlib")
    prev_gzip = sys.modules.get("gzip")
    enable()
    try:
        yield
    finally:
        sys.modules["zlib"] = prev_zlib
        sys.modules["gzip"] = prev_gzip
