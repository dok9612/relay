import pytest

from relay.normalization import normalize_name, normalize_sku


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (" ab-12 ", "AB-12"),
        ("\tab-12\n", "AB-12"),
        ("XY-9", "XY-9"),
        ("   ", ""),
    ],
)
def test_normalize_sku(raw, expected):
    assert normalize_sku(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  Brake   pad  ", "Brake pad"),
        ("Brake\t\npad", "Brake pad"),
        ("Oil filter", "Oil filter"),
        ("   ", ""),
    ],
)
def test_normalize_name(raw, expected):
    assert normalize_name(raw) == expected
