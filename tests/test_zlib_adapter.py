import pytest

from zlib_fast import zlib_adapter


def test_compressobj():
    assert zlib_adapter.compressobj() is not None
    assert zlib_adapter.compressobj(zdict=b"") is not None
    with pytest.raises(ValueError, match="Invalid compression level: -80"):
        zlib_adapter.compressobj(level=-80)
    for level in range(10):
        zlib_adapter.compressobj(level=level)


def test_decompressobj():
    assert zlib_adapter.decompressobj() is not None


def test_drop_in_constants_match_stdlib():
    """Constants stdlib zlib exposes must exist on the adapter with matching values."""
    import zlib

    for name in (
        "Z_NO_COMPRESSION",
        "Z_BLOCK",
        "Z_PARTIAL_FLUSH",
        "Z_TREES",
        "ZLIB_VERSION",
        "ZLIB_RUNTIME_VERSION",
    ):
        assert getattr(zlib_adapter, name) == getattr(zlib, name)
