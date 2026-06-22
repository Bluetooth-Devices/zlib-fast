#!/usr/bin/env python3
"""Benchmark zlib-fast against the stdlib zlib/gzip it replaces.

Runs the three operations that matter for the flagship ``tarfile`` backup use
case — ``gzip.compress``, ``gzip.decompress`` and a ``tarfile`` ``w:gz`` write —
with and without ``zlib_fast.enable()``, on deterministic, moderately
compressible data.

The compression-ratio column is reported deliberately: zlib-fast maps stdlib
levels onto isal's smaller 0-3 scale, so it trades a little ratio for a lot of
speed. Seeing both numbers keeps the comparison honest.

Usage::

    python benchmarks/benchmark.py            # ~5 MB payload
    python benchmarks/benchmark.py --mb 50    # larger payload, steadier numbers

Run from a checkout (``pip install -e .`` or ``poetry install``) so ``isal`` and
``zlib_fast`` import.
"""

from __future__ import annotations

import argparse
import io
import random
import tarfile
import time
from typing import Callable

LEVEL = 6
REPEATS = 5


def build_payload(target_bytes: int) -> bytes:
    """Generate deterministic, log-like data (~5x compressible)."""
    random.seed(1)
    words = (
        "the quick brown fox jumps over lazy dog error warn info debug user "
        "session id token request response 200 404 500 GET POST"
    ).split()
    out: list[str] = []
    size = 0
    i = 0
    while size < target_bytes:
        line = (
            f"2026-06-22T13:{i % 60:02d}:00Z {random.choice(words)} "
            f"{random.choice(words)} id={random.randint(0, 99999)} "
            f"{random.choice(words)}\n"
        )
        out.append(line)
        size += len(line)
        i += 1
    return "".join(out).encode()


def best_of(fn: Callable[[], object], repeats: int = REPEATS) -> float:
    """Return the fastest wall-clock time over ``repeats`` runs, in seconds."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


def make_tar(payload: bytes) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        info = tarfile.TarInfo("data.bin")
        info.size = len(payload)
        tf.addfile(info, io.BytesIO(payload))
    return buf.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mb", type=float, default=5.0, help="payload size in MB (default: 5)"
    )
    args = parser.parse_args()

    payload = build_payload(int(args.mb * 1_000_000))

    # Stdlib baseline — measure before enable() so we use the real zlib/gzip.
    import gzip

    std_compress = best_of(lambda: gzip.compress(payload, LEVEL))
    std_blob = gzip.compress(payload, LEVEL)
    std_decompress = best_of(lambda: gzip.decompress(std_blob))
    std_tar = best_of(lambda: make_tar(payload))

    # Swap in zlib-fast. tarfile imports gzip lazily, so enable() reaches it.
    import zlib_fast

    zlib_fast.enable()
    import gzip as fast_gzip

    fast_compress = best_of(lambda: fast_gzip.compress(payload, LEVEL))
    fast_blob = fast_gzip.compress(payload, LEVEL)
    fast_decompress = best_of(lambda: fast_gzip.decompress(fast_blob))
    fast_tar = best_of(lambda: make_tar(payload))
    zlib_fast.disable()

    def row(name: str, std: float, fast: float) -> str:
        return f"{name:<18} {std * 1e3:9.1f} {fast * 1e3:9.1f} {std / fast:8.2f}x"

    print(
        f"payload: {len(payload) / 1e6:.1f} MB  "
        f"level {LEVEL}  best of {REPEATS}\n"
        f"ratio:   stdlib {len(payload) / len(std_blob):.1f}x  "
        f"zlib-fast {len(payload) / len(fast_blob):.1f}x\n"
    )
    print(f"{'operation':<18} {'stdlib ms':>9} {'fast ms':>9} {'speedup':>9}")
    print("-" * 48)
    print(row("gzip.compress", std_compress, fast_compress))
    print(row("gzip.decompress", std_decompress, fast_decompress))
    print(row("tarfile w:gz", std_tar, fast_tar))


if __name__ == "__main__":
    main()
