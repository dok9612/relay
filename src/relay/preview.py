"""Build a catalog preview from a validated request."""

from relay.normalization import normalize_name, normalize_sku
from relay.schemas import (
    CatalogPreviewRequest,
    CatalogPreviewResponse,
    NormalizedRecord,
)


def build_catalog_preview(request: CatalogPreviewRequest) -> CatalogPreviewResponse:
    """Return new normalized records in input order; the request is not mutated."""
    records = [
        NormalizedRecord(sku=normalize_sku(r.sku), name=normalize_name(r.name))
        for r in request.records
    ]
    return CatalogPreviewResponse(records=records, count=len(records))
