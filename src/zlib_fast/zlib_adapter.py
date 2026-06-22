import zlib as _zlib_original
from typing import Any, Optional

from isal import isal_zlib
from isal.isal_zlib import (
    DEF_BUF_SIZE,
    DEF_MEM_LEVEL,
    DEFLATED,
    MAX_WBITS,
    Z_BEST_COMPRESSION,
    Z_BEST_SPEED,
    Z_BLOCK,
    Z_DEFAULT_COMPRESSION,
    Z_DEFAULT_STRATEGY,
    Z_FILTERED,
    Z_FINISH,
    Z_FIXED,
    Z_FULL_FLUSH,
    Z_HUFFMAN_ONLY,
    Z_NO_FLUSH,
    Z_PARTIAL_FLUSH,
    Z_RLE,
    Z_SYNC_FLUSH,
    Z_TREES,
    Compress,
    Decompress,
    adler32,
    compress,
    crc32,
    crc32_combine,
    decompress,
    decompressobj,
    error,
)

from .utils import gzip_compress_level_to_isal

# Constants the stdlib `zlib` exposes but `isal_zlib` does not. Provided so the
# adapter is a complete drop-in: code that reads these names must not crash.
Z_NO_COMPRESSION = 0
# Streams produced by isal are standard zlib-format, so the system zlib version
# strings remain the honest answer for format-compatibility checks.
ZLIB_VERSION = _zlib_original.ZLIB_VERSION
ZLIB_RUNTIME_VERSION = _zlib_original.ZLIB_RUNTIME_VERSION


def compressobj(
    level: int = isal_zlib.Z_DEFAULT_COMPRESSION,
    method: int = isal_zlib.DEFLATED,
    wbits: int = isal_zlib.MAX_WBITS,
    memLevel: int = isal_zlib.DEF_MEM_LEVEL,
    strategy: int = isal_zlib.Z_DEFAULT_STRATEGY,
    zdict: Optional[Any] = None,
) -> isal_zlib.Compress:
    """Compressobj adapter to convert zlib level to isal compression level."""
    level = gzip_compress_level_to_isal(level)
    if zdict is not None:
        return isal_zlib.compressobj(
            level,
            method,
            wbits,
            memLevel,
            strategy,
            zdict,
        )

    return isal_zlib.compressobj(
        level,
        method,
        wbits,
        memLevel,
        strategy,
    )


__all__ = (
    "DEFLATED",
    "DEF_BUF_SIZE",
    "DEF_MEM_LEVEL",
    "MAX_WBITS",
    "ZLIB_RUNTIME_VERSION",
    "ZLIB_VERSION",
    "Z_BEST_COMPRESSION",
    "Z_BEST_SPEED",
    "Z_BLOCK",
    "Z_DEFAULT_COMPRESSION",
    "Z_DEFAULT_STRATEGY",
    "Z_FILTERED",
    "Z_FINISH",
    "Z_FIXED",
    "Z_FULL_FLUSH",
    "Z_HUFFMAN_ONLY",
    "Z_NO_COMPRESSION",
    "Z_NO_FLUSH",
    "Z_PARTIAL_FLUSH",
    "Z_RLE",
    "Z_SYNC_FLUSH",
    "Z_TREES",
    "Compress",
    "Decompress",
    "adler32",
    "compress",
    "compressobj",
    "crc32",
    "crc32_combine",
    "decompress",
    "decompressobj",
    "error",
)
