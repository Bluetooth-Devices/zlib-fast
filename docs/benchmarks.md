# Benchmarks

`zlib-fast` exists for one reason: speed. `benchmarks/benchmark.py` measures it
against the stdlib `zlib`/`gzip` it replaces, on deterministic, log-like data.

```bash
python benchmarks/benchmark.py            # ~5 MB payload
python benchmarks/benchmark.py --mb 50    # larger payload, steadier numbers
```

Representative output (5 MB, level 6 — hardware will vary):

```
payload: 5.0 MB  level 6  best of 5
ratio:   stdlib 5.0x  zlib-fast 3.9x

operation          stdlib ms   fast ms   speedup
------------------------------------------------
gzip.compress          201.6      17.6    11.43x
gzip.decompress         24.5      11.0     2.22x
tarfile w:gz           660.6      46.4    14.25x
```

## Reading the numbers

The `tarfile w:gz` row is the flagship case — building a gzip-compressed
backup archive, where stdlib `zlib` is the bottleneck `zlib-fast` removes.

The `ratio` line is reported on purpose. `zlib-fast` maps stdlib compression
levels onto isal's smaller 0-3 scale (see the level-mapping divergence in the
compatibility notes), so it trades a little compression ratio for a large speed
gain. The benchmark shows both so the trade-off is explicit rather than hidden.
