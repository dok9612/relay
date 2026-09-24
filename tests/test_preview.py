from relay.preview import build_catalog_preview
from relay.schemas import CatalogPreviewRequest, CatalogRecord


def make_request() -> CatalogPreviewRequest:
    return CatalogPreviewRequest(
        records=[
            CatalogRecord(sku=" ab-12 ", name="  Brake   pad  "),
            CatalogRecord(sku="xy-9", name="Oil filter"),
            CatalogRecord(sku="xy-9", name="Oil filter"),
        ]
    )


def test_build_catalog_preview_normalizes_in_order_and_keeps_duplicates():
    result = build_catalog_preview(make_request())

    assert [(r.sku, r.name) for r in result.records] == [
        ("AB-12", "Brake pad"),
        ("XY-9", "Oil filter"),
        ("XY-9", "Oil filter"),
    ]
    assert result.count == 3


def test_build_catalog_preview_does_not_mutate_request():
    request = make_request()
    before = request.model_dump()

    build_catalog_preview(request)

    assert request.model_dump() == before
