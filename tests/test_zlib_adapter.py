import zlib

import pytest

from zlib_fast import zlib_adapter


def test_compress_roundtrips_all_levels():
    """Compress must accept every zlib level (-1, 0-9) and roundtrip."""
    data = b"hello world" * 100
    for level in (-1, *range(10)):
        compressed = zlib_adapter.compress(data, level)
        assert zlib.decompress(compressed) == data


def test_compress_default_level():
    """Default level (-1) must work, matching stdlib zlib.compress."""
    data = b"anything"
    assert zlib.decompress(zlib_adapter.compress(data)) == data


def test_compress_invalid_level():
    with pytest.raises(ValueError, match="Invalid compression level: 42"):
        zlib_adapter.compress(b"x", 42)


def test_compressobj():
    assert zlib_adapter.compressobj() is not None
    assert zlib_adapter.compressobj(zdict=b"") is not None
    with pytest.raises(ValueError, match="Invalid compression level: -80"):
        zlib_adapter.compressobj(level=-80)
    for level in range(10):
        zlib_adapter.compressobj(level=level)


def test_decompressobj():
    assert zlib_adapter.decompressobj() is not None
