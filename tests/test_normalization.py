from relay.normalization import normalize_catalog
from relay.schemas import CatalogPreviewRequest, CatalogRecord


def test_normalize_catalog():
    request = CatalogPreviewRequest(
        records=[
            CatalogRecord(
                sku=" ab-12 ",
                name="  Brake   pad  ",
            ),
            CatalogRecord(
                sku="xy-9",
                name="Oil filter",
            ),
        ]
    )

    result = normalize_catalog(request)

    assert result.records[0].sku == "AB-12"
    assert result.records[0].name == "Brake pad"
    assert result.records[1].sku == "XY-9"
    assert result.records[1].name == "Oil filter"
    assert result.count == 2


def test_normalize_does_not_mutate():
    request = CatalogPreviewRequest(
        records=[
            CatalogRecord(
                sku=" ab-12 ",
                name="  Brake   pad  ",
            ),
            CatalogRecord(
                sku="xy-9",
                name="Oil filter",
            ),
        ]
    )

    normalize_catalog(request)
    assert request.records[0].sku == " ab-12 "
    assert request.records[0].name == "  Brake   pad  "
    assert request.records[1].sku == "xy-9"
    assert request.records[1].name == "Oil filter"
