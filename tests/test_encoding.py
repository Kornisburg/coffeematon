import pytest

from coffeematon.encoding import Compression, zip_string


def test_zip_string_backends():
    data = "0101010101010101"
    assert zip_string(data, Compression.GZIP) > 0
    assert zip_string(data, Compression.BZIP) > 0


def test_zip_string_zstd_optional():
    data = "0101010101010101"
    try:
        result = zip_string(data, Compression.ZSTD)
        assert result > 0
    except ModuleNotFoundError:
        pytest.skip("zstandard not installed")
