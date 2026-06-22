from isal import igzip
from isal.igzip import READ_BUFFER_SIZE, BadGzipFile

from .const import ZLIB_DEFAULT_COMPRESS_LEVEL
from .utils import gzip_compress_level_to_isal

_GZIP_MAGIC = b"\x1f\x8b"


def decompress(data):  # type: ignore[no-untyped-def]
    """
    Decompress a gzip-compressed bytes object in one shot.

    Matches stdlib ``gzip.decompress`` error semantics: a non-empty input whose
    first two bytes are not the gzip magic number raises ``BadGzipFile``. isal's
    raw ``igzip.decompress`` raises ``EOFError`` for such short/bad-magic inputs,
    which would break drop-in consumers that catch ``BadGzipFile``.
    """
    if data and data[:2] != _GZIP_MAGIC:
        raise BadGzipFile(f"Not a gzipped file ({data[:2]!r})")
    return igzip.decompress(data)


def open(  # type: ignore[no-untyped-def]
    filename,
    mode="rb",
    compresslevel=ZLIB_DEFAULT_COMPRESS_LEVEL,
    encoding=None,
    errors=None,
    newline=None,
):
    """Open a gzip-compressed file in binary or text mode."""
    return igzip.open(
        filename,
        mode,
        gzip_compress_level_to_isal(compresslevel),
        encoding,
        errors,
        newline,
    )


def compress(data, compresslevel=ZLIB_DEFAULT_COMPRESS_LEVEL, *, mtime=None):  # type: ignore[no-untyped-def]
    """
    Compress data in one shot and return the compressed string.

    Optional argument is the compression level, in range of 0-9.
    """
    return igzip.compress(data, gzip_compress_level_to_isal(compresslevel), mtime=mtime)


class GzipFileAdapter(igzip.GzipFile):
    def __init__(  # type: ignore[no-untyped-def]
        self,
        filename=None,
        mode=None,
        compresslevel=ZLIB_DEFAULT_COMPRESS_LEVEL,
        fileobj=None,
        mtime=None,
    ):
        super().__init__(
            filename, mode, gzip_compress_level_to_isal(compresslevel), fileobj, mtime
        )


IGzipFile = GzipFileAdapter
GzipFile = GzipFileAdapter

__all__ = (
    "READ_BUFFER_SIZE",
    "BadGzipFile",
    "GzipFile",
    "compress",
    "decompress",
    "open",
)
