import string

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

from relay.normalization import normalize_name, normalize_sku
from relay.schemas import CatalogRecord

SKU_ALPHABET = string.ascii_letters + string.digits + "-_."
valid_sku_body = st.text(alphabet=SKU_ALPHABET, min_size=1, max_size=64)
padding = st.text(alphabet=" \t\n\r", max_size=3)
# at least one non-ASCII character somewhere in the string
non_ascii_text = st.tuples(st.text(), st.characters(min_codepoint=128), st.text()).map(
    "".join
)


# ---- normalize_name -------------------------------------------------------


@given(st.text())
def test_normalize_name_is_idempotent(raw):
    once = normalize_name(raw)
    assert normalize_name(once) == once


@given(st.text())
def test_normalize_name_output_is_clean(raw):
    out = normalize_name(raw)
    assert out == out.strip()
    assert "  " not in out
    assert all(ch == " " or not ch.isspace() for ch in out)


# ---- normalize_sku + SKU policy --------------------------------------------


@given(st.text())
def test_normalize_sku_is_idempotent(raw):
    once = normalize_sku(raw)
    assert normalize_sku(once) == once


@given(padding, valid_sku_body, padding)
def test_valid_sku_is_accepted_and_never_gets_longer(left, body, right):
    raw = left + body + right
    record = CatalogRecord(sku=raw, name="x")

    assert normalize_sku(record.sku) == body.upper()
    assert len(normalize_sku(raw)) <= len(raw)


@given(non_ascii_text)
def test_sku_with_any_non_ascii_character_is_rejected(raw):
    with pytest.raises(ValidationError):
        CatalogRecord(sku=raw, name="x")
