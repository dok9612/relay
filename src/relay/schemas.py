"""HTTP request/response contracts for the catalog preview."""

import string

from pydantic import BaseModel, ConfigDict, Field, field_validator

from relay.normalization import normalize_name, normalize_sku

# SKU policy: identifiers are compared exactly by people and machines, so they
# use a small, unambiguous alphabet. Names stay full Unicode (display text).
SKU_CHARS = frozenset(string.ascii_uppercase + string.digits + "-_.")


class CatalogRecord(BaseModel):
    """One record as a client sends it (raw, not yet normalized)."""

    model_config = ConfigDict(extra="forbid")

    sku: str = Field(strict=True)
    name: str = Field(strict=True)

    # Length limits apply to the value AFTER normalization, using the same
    # functions the preview uses, so the check and the transformation can
    # never disagree. The raw value is returned unchanged.
    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str) -> str:
        sku = normalize_sku(value)
        if not 1 <= len(sku) <= 64:
            raise ValueError("sku must be 1-64 characters after normalization")
        # isascii() on the RAW value: some non-ASCII letters uppercase into
        # ASCII look-alikes ("ı" -> "I", "ſ" -> "S"), so checking only the
        # normalized SKU would let them through.
        if not value.isascii() or not set(sku) <= SKU_CHARS:
            raise ValueError("sku may only contain A-Z, a-z, 0-9, '-', '_' and '.'")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not 1 <= len(normalize_name(value)) <= 200:
            raise ValueError("name must be 1-200 characters after normalization")
        return value


class NormalizedRecord(BaseModel):
    """One record as the API returns it."""

    sku: str
    name: str


class CatalogPreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    records: list[CatalogRecord] = Field(min_length=1, max_length=100)


class CatalogPreviewResponse(BaseModel):
    records: list[NormalizedRecord]
    count: int
