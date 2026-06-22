"""
End-to-end drop-in regression tests for the flagship ``tarfile`` use case.

The README pitches ``zlib_fast`` as a drop-in replacement whose primary purpose
is speeding up ``tarfile`` backups via ``isal``. That promise rests on two
guarantees the unit tests never exercised directly:

* archives produced under ``enable()`` are readable by the *stdlib*, and
* archives produced by the stdlib are readable under ``enable()``.

These tests pin both directions so a future change to the gzip adapter can't
silently break the cross-compatibility the library exists to provide.
"""

import gzip as gzip_original
import io
import tarfile
import zlib as zlib_original

import pytest

import zlib_fast

DATA = b"the quick brown fox jumps over the lazy dog\n" * 250


@pytest.fixture
def adapter_enabled():
    """Enable the adapter for the test body and always restore the stdlib."""
    zlib_fast.enable()
    try:
        yield
    finally:
        zlib_fast.disable()


def _write_targz(data: bytes, compresslevel: int) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=compresslevel) as tar:
        info = tarfile.TarInfo("payload.bin")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def _read_targz(raw: bytes) -> bytes:
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        member = tar.extractfile("payload.bin")
        assert member is not None
        return member.read()


# Levels that exercise the full gzip<->isal level mapping (utils maps 0-9 to 0-3).
LEVELS = [0, 1, 6, 9, -1]


@pytest.mark.parametrize("level", LEVELS)
def test_tarfile_written_under_adapter_reads_with_stdlib(adapter_enabled, level):
    """Tarfile compressing through the adapter must produce stdlib-readable gzip."""
    raw = _write_targz(DATA, level)
    # Restore the stdlib before reading so the reader is genuinely independent.
    zlib_fast.disable()
    assert _read_targz(raw) == DATA


@pytest.mark.parametrize("level", LEVELS)
def test_tarfile_written_by_stdlib_reads_under_adapter(level):
    """The adapter must decompress archives produced by the unpatched stdlib."""
    raw = _write_targz(DATA, level)  # stdlib is active here
    zlib_fast.enable()
    try:
        assert _read_targz(raw) == DATA
    finally:
        zlib_fast.disable()


def test_tarfile_roundtrips_entirely_under_adapter(adapter_enabled):
    """Write and read back within a single enabled session."""
    raw = _write_targz(DATA, 9)
    assert _read_targz(raw) == DATA


def test_enable_redirects_tarfile_late_import(adapter_enabled):
    """
    Tarfile's lazy ``import gzip`` must resolve to the adapter, not the stdlib.

    This is the mechanism the README relies on: ``enable()`` only affects
    *future* imports, and tarfile imports gzip lazily inside ``gzopen``.
    """
    _write_targz(DATA, 6)  # forces tarfile to import gzip under the override
    import gzip

    assert gzip is not gzip_original
    assert gzip is zlib_fast.gzip_adapter


def test_disable_restores_stdlib_modules():
    """After disable(), a fresh import resolves back to the real modules."""
    zlib_fast.enable()
    zlib_fast.disable()
    import gzip
    import zlib

    assert gzip is gzip_original
    assert zlib is zlib_original
