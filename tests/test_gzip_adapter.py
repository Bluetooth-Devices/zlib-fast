import io
from io import BytesIO

import pytest

from zlib_fast import gzip_adapter

SEEK_DATA = b"the quick brown fox jumps over the lazy dog\n" * 250


def _reader():
    compressed = gzip_adapter.compress(SEEK_DATA, 9)
    return gzip_adapter.GzipFile(fileobj=BytesIO(compressed), mode="rb")


def test_compress():
    compressed = gzip_adapter.compress(b"anything", 9)
    assert compressed is not None
    assert gzip_adapter.decompress(compressed) == b"anything"


def test_open():
    compressed = gzip_adapter.compress(b"anything", 9)

    with gzip_adapter.open(BytesIO(compressed), "rb") as f:
        assert f.read() == b"anything"


def test_gzip_file():
    compressed = gzip_adapter.compress(b"anything", 9)
    with gzip_adapter.GzipFile(fileobj=BytesIO(compressed), mode="rb") as f:
        assert f.read() == b"anything"


def test_backward_seek_after_forward_seek():
    """
    A backward seek that follows a forward seek must reposition correctly.

    isal's C reader corrupts its state in this pattern (raising BadGzipFile);
    the adapter rebuilds the reader so the flagship tarfile r:gz path works.
    """
    with _reader() as f:
        f.seek(len(SEEK_DATA) - 1)  # forward seek near the end
        f.seek(512)  # backward seek
        assert f.read(20) == SEEK_DATA[512:532]


def test_seek_cur_backward():
    with _reader() as f:
        assert f.read(600) == SEEK_DATA[:600]
        f.seek(-500, io.SEEK_CUR)
        assert f.read(10) == SEEK_DATA[100:110]


def test_seek_end():
    with _reader() as f:
        f.seek(-30, io.SEEK_END)
        assert f.read() == SEEK_DATA[-30:]


def test_seek_invalid_whence():
    with _reader() as f, pytest.raises(ValueError):
        f.seek(0, 99)


def test_seek_write_mode():
    """Write-mode seeks delegate to the base implementation (zero-fill)."""
    buf = BytesIO()
    with gzip_adapter.GzipFile(fileobj=buf, mode="wb") as f:
        f.write(b"abc")
        f.seek(5)  # forward seek in write mode zero-fills
        f.write(b"z")
    with gzip_adapter.GzipFile(fileobj=BytesIO(buf.getvalue()), mode="rb") as f:
        assert f.read() == b"abc\x00\x00z"
