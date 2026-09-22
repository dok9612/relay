from pydantic import BaseModel, ConfigDict, Field, field_validator

# from relay.normalization import normalize_sku


class CatalogRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sku: str = Field(strict=True)
    name: str = Field(strict=True)

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str):
        normalized_sku = value.strip().upper()
        if not 1 <= len(normalized_sku) <= 64:
            raise ValueError("sku must be between 1 and 64.")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        normalized_name = " ".join(value.split())
        if not 1 <= len(normalized_name) <= 200:
            raise ValueError("name must be between len 1 and 200.")
        return value


class CatalogPreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    records: list[CatalogRecord] = Field(min_length=1, max_length=100)


class CatalogPreviewResponse(BaseModel):
    records: list[CatalogRecord]
    count: int = Field(ge=1, le=100)
