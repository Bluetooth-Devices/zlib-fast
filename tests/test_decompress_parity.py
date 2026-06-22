"""
Error-handling parity for the one-shot gzip.decompress adapter.

A drop-in replacement must preserve exception types for corrupt/untrusted
input. stdlib raises ``BadGzipFile`` as soon as the 2-byte magic number is
wrong; isal's raw decompress raises ``EOFError`` for short or bad-magic input
because it hits end-of-stream before validating the header. These tests pin the
adapter to stdlib's behavior.
"""

import gzip as gzip_std

import pytest
from isal.igzip import BadGzipFile

from zlib_fast import gzip_adapter

PAYLOAD = b"the quick brown fox" * 50


@pytest.mark.parametrize(
    "data",
    [
        b"not gzip",  # short, clearly not gzip
        b"\x1f",  # single byte
        b"PK",  # exactly 2 bytes, wrong magic (zip)
        b"PK\x03\x04" + b"x" * 96,  # long, wrong magic
        b"\x00\x01" + b"x" * 98,  # long, bad magic
    ],
)
def test_bad_magic_raises_badgzipfile_like_stdlib(data):
    with pytest.raises(BadGzipFile):
        gzip_std.decompress(data)
    with pytest.raises(BadGzipFile):
        gzip_adapter.decompress(data)


def test_empty_input_matches_stdlib():
    assert gzip_adapter.decompress(b"") == gzip_std.decompress(b"") == b""


def test_truncated_valid_stream_still_raises_eoferror():
    # Correct magic but truncated payload: both stdlib and isal raise EOFError.
    good = gzip_std.compress(PAYLOAD)
    truncated = good[: len(good) // 2]
    with pytest.raises(EOFError):
        gzip_std.decompress(truncated)
    with pytest.raises(EOFError):
        gzip_adapter.decompress(truncated)


def test_valid_stream_roundtrips():
    compressed = gzip_std.compress(PAYLOAD)
    assert gzip_adapter.decompress(compressed) == PAYLOAD


def test_multi_member_stream_decompresses_fully():
    # The magic precheck must not break concatenated members (stdlib joins them).
    stream = gzip_std.compress(PAYLOAD) + gzip_std.compress(b"second")
    assert gzip_adapter.decompress(stream) == PAYLOAD + b"second"
