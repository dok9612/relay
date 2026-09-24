from fastapi import FastAPI

from relay.preview import build_catalog_preview
from relay.schemas import CatalogPreviewRequest, CatalogPreviewResponse

app = FastAPI(title="Relay")


@app.post("/v1/catalog-previews")
def create_catalog_preview(request: CatalogPreviewRequest) -> CatalogPreviewResponse:
    # 200, not 201: a preview creates no stored resource.
    return build_catalog_preview(request)
