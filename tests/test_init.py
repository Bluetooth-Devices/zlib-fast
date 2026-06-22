import gzip as gzip_original
import sys
import zlib as zlib_original

import pytest

from zlib_fast import disable, enable, enabled
from zlib_fast import gzip_adapter as best_gzip
from zlib_fast import zlib_adapter as best_zlib


def test_enable_disable():
    """Test enable/disable."""
    import gzip
    import zlib

    assert zlib is zlib_original
    assert gzip is gzip_original
    enable()
    import gzip
    import zlib

    assert zlib is best_zlib
    assert gzip is best_gzip
    disable()
    import gzip
    import zlib

    assert zlib is zlib_original
    assert gzip is gzip_original


def test_enabled_context_manager():
    """enabled() swaps inside the block and restores on exit."""
    disable()
    assert sys.modules["zlib"] is zlib_original
    assert sys.modules["gzip"] is gzip_original

    with enabled():
        assert sys.modules["zlib"] is best_zlib
        assert sys.modules["gzip"] is best_gzip

    assert sys.modules["zlib"] is zlib_original
    assert sys.modules["gzip"] is gzip_original


def test_enabled_restores_on_exception():
    """enabled() restores the prior modules even if the block raises."""
    disable()
    with pytest.raises(RuntimeError):
        with enabled():
            assert sys.modules["zlib"] is best_zlib
            raise RuntimeError("boom")

    assert sys.modules["zlib"] is zlib_original
    assert sys.modules["gzip"] is gzip_original


def test_enabled_restores_prior_enabled_state():
    """Nesting: an already-enabled adapter is restored, not reset to stdlib."""
    enable()
    try:
        with enabled():
            assert sys.modules["zlib"] is best_zlib
        # prior state was enabled, so it must remain enabled here
        assert sys.modules["zlib"] is best_zlib
        assert sys.modules["gzip"] is best_gzip
    finally:
        disable()
