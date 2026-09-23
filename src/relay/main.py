from fastapi import FastAPI

from relay.schemas import CatalogPreviewRequest, CatalogPreviewResponse
from relay.normalization import normalize_catalog

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "hello"}


@app.post("/v1/catalog-previews", response_model=CatalogPreviewResponse)
def catalog_preview(data: CatalogPreviewRequest) -> CatalogPreviewResponse:
    normalized_catalog = normalize_catalog(data)
    return normalized_catalog
