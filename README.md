# zlib-fast

<p align="center">
  <a href="https://github.com/bluetooth-devices/zlib-fast/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/bluetooth-devices/zlib-fast/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://zlib-fast.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/zlib-fast.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/bluetooth-devices/zlib-fast">
    <img src="https://img.shields.io/codecov/c/github/bluetooth-devices/zlib-fast.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/zlib-fast/">
    <img src="https://img.shields.io/pypi/v/zlib-fast.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/zlib-fast.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/zlib-fast.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://zlib-fast.readthedocs.io" target="_blank">https://zlib-fast.readthedocs.io </a>

**Source Code**: <a href="https://github.com/bluetooth-devices/zlib-fast" target="_blank">https://github.com/bluetooth-devices/zlib-fast </a>

---

A wrapper to use the fastest available zlib

zlib is be a bottleneck for creating backups with `tarfile`. `zlib-fast` replaces usage of `zlib` with [`isal`](https://github.com/pycompression/python-isal) which is a drop-in faster replacement.

Unlike the base isal implementation, this module maps zlib compression
levels for `compressobj` to their nearest `isal` equivalent which allows
it to be used as a drop in replacement with `tarfile`.

## Installation

Install this via pip (or your favourite package manager):

`pip install zlib-fast`

## Usage

Enable zlib-fast support by calling `zlib_fast.enable()`.

```python

import zlib_fast

zlib_fast.enable()
zlib_fast.disable()
```

For a scoped swap that always restores the previous state — even if the block raises — use the `enabled()` context manager:

```python
import zlib_fast

with zlib_fast.enabled():
    ...  # zlib/gzip resolve to the fast adapters in here
# previous zlib/gzip restored on exit
```

The most common use case is for use with `tarfile` which does a late import. `enable` will only be effective for future imports of `zlib`, and will not redirect existing imports. If you need to use this module for other use cases, be sure to call `zlib_fast.enable()` before any code that loads `zlib`.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
