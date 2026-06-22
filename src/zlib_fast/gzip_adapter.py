from isal import igzip
from isal.igzip import READ_BUFFER_SIZE, BadGzipFile, decompress

from .const import ZLIB_DEFAULT_COMPRESS_LEVEL
from .utils import gzip_compress_level_to_isal

# gzip header flag bits (RFC 1952). The stdlib `gzip` module exposes these but
# `igzip` does not; provide them so the adapter is a complete drop-in.
FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = 1, 2, 4, 8, 16


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
    "FCOMMENT",
    "FEXTRA",
    "FHCRC",
    "FNAME",
    "FTEXT",
    "READ_BUFFER_SIZE",
    "BadGzipFile",
    "GzipFile",
    "compress",
    "decompress",
    "open",
)
