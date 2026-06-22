(compatibility)=

# Drop-in compatibility

`zlib-fast` swaps the standard library `zlib` and `gzip` modules for
[`isal`](https://github.com/pycompression/python-isal)-backed adapters when you
call `zlib_fast.enable()`. The goal is a **drop-in** replacement: existing
code — most importantly `tarfile` opened with `"w:gz"` / `"r:gz"` — keeps
working without changes, just faster.

isal is not byte-for-byte identical to zlib, so a perfect drop-in is impossible.
This page documents what is guaranteed compatible and the handful of behaviours
that intentionally diverge.

## What stays compatible

- **Round-trips.** Anything compressed by the adapter decompresses with stdlib
  `zlib`/`gzip`, and vice-versa, across every level (`-1`, `0`–`9`).
- **The `tarfile` flagship.** Reading and writing `.tar.gz` archives under
  `enable()` behaves like stdlib, including the forward-then-backward seek
  pattern `tarfile` uses to reach a member payload.
- **Public API surface.** `compress` / `decompress` / `compressobj` /
  `decompressobj` / `gzip.open` / `gzip.GzipFile` accept the same arguments, and
  the `zlib`/`gzip` module-level constants consumers read (flush modes,
  strategies, `Z_*`, version strings, gzip header flags) are all present.
- **Checksums.** `crc32` and `adler32` return the same unsigned values as stdlib.
- **Multi-member gzip streams.** Concatenated gzip members decompress fully,
  matching stdlib.

## Known divergences

These are deliberate trade-offs of the isal backend. They are documented rather
than silently patched because changing them would alter observable output; a
maintainer should decide whether parity is worth the cost.

### Compression levels are mapped, not exact

zlib exposes 10 levels (`0`–`9`); isal exposes 4. `zlib-fast` maps each zlib
level to its nearest isal equivalent, so compressed **output bytes differ from
stdlib** even though both decompress correctly. The mapping is:

| zlib level | `-1` | `0` | `1` | `2` | `3` | `4` | `5` | `6` | `7` | `8` | `9` |
| ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| isal level | `2`  | `0` | `0` | `1` | `1` | `2` | `2` | `2` | `3` | `3` | `3` |

Code that asserts on exact compressed length or bytes will see differences. Code
that only round-trips data is unaffected.

### `level=0` still compresses

With stdlib, `gzip.compress(data, 0)` **stores** the data uncompressed (level 0
= no compression). isal has no "stored" mode, so level 0 maps to its fastest
_compressing_ level instead. For 1 000 repeated bytes:

|             | stdlib `gzip.compress(data, 0)` | adapter                |
| ----------- | ------------------------------- | ---------------------- |
| output size | 1023 bytes (stored)             | 143 bytes (compressed) |

If a consumer relies on level 0 producing a byte-for-byte stored stream, that
guarantee does not hold.

### Default gzip compression level is 6, not 9

stdlib `gzip.compress`, `gzip.open`, and `gzip.GzipFile` default to
`compresslevel=9`. `zlib-fast` defaults to `6`
(`zlib_fast.const.ZLIB_DEFAULT_COMPRESS_LEVEL`) to trade a little ratio for
speed. Pass an explicit `compresslevel` to pin the behaviour you want.

### Trailing garbage raises a different exception

stdlib raises `gzip.BadGzipFile` when bytes after a valid gzip stream are not a
valid next member; isal raises `EOFError` for the same input. A truncated stream
raises `EOFError` on both, and a completely non-gzip input raises `BadGzipFile`
on both. Only the _trailing-garbage_ case differs. Code that catches
`BadGzipFile` should also catch `EOFError` if it feeds the adapter
possibly-padded streams.

## Quick reference

```{list-table}
:header-rows: 1

* - Behaviour
  - stdlib
  - zlib-fast
* - Round-trip with stdlib
  - ✅
  - ✅
* - Exact compressed bytes
  - baseline
  - differ (level mapping)
* - `level=0`
  - stored, uncompressed
  - compressed
* - Default gzip level
  - 9
  - 6
* - Trailing garbage error
  - `BadGzipFile`
  - `EOFError`
```
