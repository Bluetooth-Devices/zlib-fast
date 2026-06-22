(usage)=

# Usage

Assuming that you've followed the {ref}`installations steps <installation>`, you're now ready to use this package.

Import it and call `zlib_fast.enable()` **before** the code that imports
`zlib` or `gzip` runs. `enable()` swaps the adapters into `sys.modules`, so any
later `import zlib` / `import gzip` (including the lazy import `tarfile` does
internally) resolves to the fast isal-backed versions.

```python
import zlib_fast

zlib_fast.enable()

import tarfile

# This .tar.gz is now created with isal instead of stdlib zlib.
with tarfile.open("backup.tar.gz", "w:gz") as tar:
    tar.add("data/")
```

Call `zlib_fast.disable()` to restore the original `zlib`/`gzip` modules.

## Compatibility

`zlib-fast` is a drop-in replacement, but isal is not byte-for-byte identical to
stdlib zlib. See {ref}`compatibility` for the guarantees and the handful of
intentional divergences (level mapping, `level=0`, default level, error types).
