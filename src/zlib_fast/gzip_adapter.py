import io
from typing import IO, cast

from isal import igzip
from isal.igzip import READ, READ_BUFFER_SIZE, BadGzipFile, _GzipReader, decompress

from .const import ZLIB_DEFAULT_COMPRESS_LEVEL
from .utils import gzip_compress_level_to_isal


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
        # Remember where the gzip stream starts so a backward seek can rebuild
        # the reader from the true origin (handles fileobj opened mid-stream).
        self._stream_start = (
            cast(IO[bytes], self.fileobj).tell() if self.mode == READ else 0
        )

    def seek(self, offset, whence=io.SEEK_SET):  # type: ignore[no-untyped-def]
        """
        Seek within the stream.

        isal's C ``_GzipReader`` mishandles a backward seek that follows a
        forward seek (its rewind leaves the underlying file mispositioned,
        raising ``BadGzipFile``). This breaks the flagship ``tarfile`` r:gz
        path, which seeks back to a member's payload after scanning the
        archive. Forward seeks work, so we resolve every seek to an absolute
        target and, when it moves backward, rebuild a fresh reader from the
        stream origin and seek forward to the target.
        """
        if self.mode != READ:
            return super().seek(offset, whence)

        if whence == io.SEEK_SET:
            target = offset
        elif whence == io.SEEK_CUR:
            target = self._buffer.tell() + offset
        elif whence == io.SEEK_END:
            # Drain to the end so the absolute size is known, then apply offset.
            self._buffer.read()
            target = self._buffer.tell() + offset
        else:
            raise ValueError(f"Invalid whence value: {whence}")

        if target < self._buffer.tell():
            self.fileobj.seek(self._stream_start)  # type: ignore[union-attr]
            raw = _GzipReader(self.fileobj, READ_BUFFER_SIZE)  # type: ignore[arg-type]
            self._buffer = io.BufferedReader(raw)  # type: ignore[type-var]
        return self._buffer.seek(target, io.SEEK_SET)


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
