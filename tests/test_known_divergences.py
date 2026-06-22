"""
Characterization tests for known isal-vs-stdlib drop-in divergences.

These lock in behaviors where zlib-fast (backed by ``isal``) cannot perfectly
match the stdlib ``zlib`` API. They are not aspirational parity tests — they
document the current contract executably so that an ``isal`` upgrade (or any
adapter change) that alters these behaviors fails loudly instead of silently
shifting the drop-in promise. See ``docs/compatibility.md`` for prose.

Each test also asserts that data integrity is preserved despite the divergent
observable API, so a reader can tell "different surface, same bytes" apart from
an actual corruption regression.
"""

import zlib as zlib_stdlib

from zlib_fast import zlib_adapter

DATA = b"the quick brown fox jumps over the lazy dog " * 200


def test_compress_decompress_objects_lack_copy():
    """
    Stdlib Compress/Decompress expose ``.copy()``; isal does not.

    The C-extension compression state cannot be duplicated from Python, so the
    adapter cannot offer ``.copy()`` without falling back to stdlib (which would
    defeat the library). Consumers relying on checkpoint/copy of an in-flight
    (de)compressor must guard for its absence.
    """
    assert hasattr(zlib_stdlib.compressobj(), "copy")
    assert hasattr(zlib_stdlib.decompressobj(), "copy")

    assert not hasattr(zlib_adapter.compressobj(), "copy")
    assert not hasattr(zlib_adapter.decompressobj(), "copy")


def test_decompressobj_max_length_unconsumed_tail_is_empty():
    """
    ``decompress(data, max_length)`` leaves ``unconsumed_tail`` empty on isal.

    stdlib returns at most ``max_length`` bytes and parks the still-unread
    *compressed* input in ``unconsumed_tail`` for the caller to feed back. isal
    buffers that input internally instead, so ``unconsumed_tail`` is always
    empty even when output was truncated. Data is still fully recoverable — but
    via repeated ``decompress`` calls, not via the ``unconsumed_tail`` round-trip
    the stdlib docs describe.
    """
    compressed = zlib_stdlib.compress(DATA, 6)

    # stdlib parks leftover compressed input in unconsumed_tail.
    std = zlib_stdlib.decompressobj()
    std_out = std.decompress(compressed, 100)
    assert len(std_out) == 100
    assert std.unconsumed_tail  # non-empty: stdlib contract

    # isal truncates output identically but reports an empty tail.
    obj = zlib_adapter.decompressobj()
    out = obj.decompress(compressed, 100)
    assert len(out) == 100
    assert obj.unconsumed_tail == b""  # divergence

    # Integrity preserved: the rest decompresses on a follow-up call.
    out += obj.decompress(obj.unconsumed_tail)
    while not obj.eof:
        chunk = obj.decompress(b"")
        if not chunk:
            break
        out += chunk
    assert out == DATA


def test_checksums_match_stdlib():
    """
    crc32/adler32 are bit-exact with stdlib — a parity guard, not a divergence.

    Included so a future isal change to checksum output would be caught here
    next to the divergences it would belong with.
    """
    assert zlib_adapter.crc32(DATA) == zlib_stdlib.crc32(DATA)
    assert zlib_adapter.adler32(DATA) == zlib_stdlib.adler32(DATA)
