from relay.schemas import CatalogRecord, CatalogPreviewRequest, CatalogPreviewResponse


def normalize_sku(sku: str) -> str:
    return sku.strip().upper()


def normalize_name(name: str) -> str:
    return " ".join(name.split())


def normalize_record(record: CatalogRecord) -> CatalogRecord:
    return CatalogRecord(
        sku=normalize_sku(record.sku), name=normalize_name(record.name)
    )


def normalize_catalog(request: CatalogPreviewRequest) -> CatalogPreviewResponse:
    normalized_records = [normalize_record(record) for record in request.records]
    return CatalogPreviewResponse(
        records=normalized_records,
        count=len(normalized_records),
    )
