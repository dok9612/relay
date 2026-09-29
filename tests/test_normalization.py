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
        pytest.param("  Brake   pad  ", "Brake pad", id="spaces"),
        pytest.param("Brake\t\npad", "Brake pad", id="tab and newline"),
        pytest.param("Brake\r\npad", "Brake pad", id="windows line ending"),
        pytest.param("Brake\u00a0\u00a0pad", "Brake pad", id="non-breaking spaces"),
        pytest.param("Oil filter", "Oil filter", id="already clean"),
        pytest.param("   ", "", id="only whitespace"),
    ],
)
def test_normalize_name(raw, expected):
    assert normalize_name(raw) == expected
