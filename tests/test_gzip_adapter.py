from io import BytesIO

from zlib_fast import gzip_adapter


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


def test_gzip_header_flag_constants():
    """Gzip header flag bits must match the stdlib values (RFC 1952)."""
    import gzip

    for name in ("FTEXT", "FHCRC", "FEXTRA", "FNAME", "FCOMMENT"):
        assert getattr(gzip_adapter, name) == getattr(gzip, name)
