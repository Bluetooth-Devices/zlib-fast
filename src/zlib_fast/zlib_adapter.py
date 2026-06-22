from typing import Any, Optional

from isal import isal_zlib
from isal.isal_zlib import (
    DEF_BUF_SIZE,
    DEF_MEM_LEVEL,
    DEFLATED,
    MAX_WBITS,
    Z_BEST_COMPRESSION,
    Z_BEST_SPEED,
    Z_DEFAULT_COMPRESSION,
    Z_DEFAULT_STRATEGY,
    Z_FILTERED,
    Z_FINISH,
    Z_FIXED,
    Z_FULL_FLUSH,
    Z_HUFFMAN_ONLY,
    Z_NO_FLUSH,
    Z_RLE,
    Z_SYNC_FLUSH,
    Compress,
    Decompress,
    adler32,
    crc32,
    crc32_combine,
    decompress,
    decompressobj,
    error,
)

from .utils import gzip_compress_level_to_isal


def compress(
    data: Any,
    level: int = -1,
    wbits: int = isal_zlib.MAX_WBITS,
) -> bytes:
    """
    Compress adapter to convert zlib level to isal compression level.

    ``isal_zlib.compress`` only accepts levels 0-3, whereas the stdlib
    ``zlib.compress`` accepts 0-9 or -1. Translate the level so this stays a
    drop-in replacement.
    """
    return isal_zlib.compress(data, gzip_compress_level_to_isal(level), wbits)


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
    "Z_BEST_COMPRESSION",
    "Z_BEST_SPEED",
    "Z_DEFAULT_COMPRESSION",
    "Z_DEFAULT_STRATEGY",
    "Z_FILTERED",
    "Z_FINISH",
    "Z_FIXED",
    "Z_FULL_FLUSH",
    "Z_HUFFMAN_ONLY",
    "Z_NO_FLUSH",
    "Z_RLE",
    "Z_SYNC_FLUSH",
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
