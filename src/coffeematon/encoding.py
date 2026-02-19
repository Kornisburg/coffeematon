"""Tools to estimate the entropy and complexity of the cellular automaton."""

import bz2
import gzip
from enum import Enum
from typing import Union

import numpy as np

try:
    import zstandard as zstd
except ModuleNotFoundError:
    zstd = None


class Compression(Enum):
    BZIP = "bzip"
    GZIP = "gzip"
    ZSTD = "zstd"


def zip_array(
    array: np.ndarray, compression: Union[Compression, str] = Compression.GZIP
) -> int:
    return zip_bytes(array.tobytes(), compression)


def zip_string(
    string: str, compression: Union[Compression, str] = Compression.GZIP
) -> int:
    byte_string = bytearray(string, "ascii")
    return zip_bytes(byte_string, compression)


def zip_bytes(data: bytes, compression: Union[Compression, str]) -> int:
    compression = Compression(compression)
    if compression is Compression.GZIP:
        return len(gzip.compress(data))
    if compression is Compression.BZIP:
        return len(bz2.compress(data))
    if compression is Compression.ZSTD:
        if zstd is None:
            raise ModuleNotFoundError(
                "zstandard is not installed. Install with `pip install zstandard`."
            )
        return len(zstd.ZstdCompressor(level=3).compress(data))
    raise ValueError(f"Unsupported compression: {compression}")


def write_string(array):
    return " ".join([" ".join([str(x) for x in row]) for row in array])
