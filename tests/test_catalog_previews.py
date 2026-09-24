import pytest
from fastapi.testclient import TestClient

from relay.main import app


client = TestClient(app)
URL = "/v1/catalog-previews"


def test_catalog_preview_success():
    response = client.post(
        "/v1/catalog-previews",
        json={
            "records": [
                {
                    "sku": " ab-12 ",
                    "name": "  Brake   pad  ",
                },
                {
                    "sku": "xy-9",
                    "name": "Oil filter",
                },
            ]
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "records": [
            {
                "sku": "AB-12",
                "name": "Brake pad",
            },
            {
                "sku": "XY-9",
                "name": "Oil filter",
            },
        ],
        "count": 2,
    }


REC = ["body", "records", 0]  # location prefix for fields inside the first record


@pytest.mark.parametrize(
    ("payload", "loc", "error_type"),
    [
        # --- the four ways a field can be wrong ---
        pytest.param(
            {"records": [{"name": "Brake pad"}]},
            REC + ["sku"],
            "missing",
            id="sku omitted",
        ),
        pytest.param(
            {"records": [{"sku": None, "name": "Brake pad"}]},
            REC + ["sku"],
            "string_type",
            id="sku null",
        ),
        pytest.param(
            {"records": [{"sku": "", "name": "Brake pad"}]},
            REC + ["sku"],
            "value_error",
            id="sku empty",
        ),
        pytest.param(
            {"records": [{"sku": 123, "name": "Brake pad"}]},
            REC + ["sku"],
            "string_type",
            id="sku number",
        ),
        # --- blank after normalization (your rule, so a value_error) ---
        pytest.param(
            {"records": [{"sku": "   ", "name": "Brake pad"}]},
            REC + ["sku"],
            "value_error",
            id="sku blank",
        ),
        pytest.param(
            {"records": [{"sku": "ab-12", "name": "   "}]},
            REC + ["name"],
            "value_error",
            id="name blank",
        ),
        pytest.param(
            {"records": [{"sku": "ab-12", "name": 5}]},
            REC + ["name"],
            "string_type",
            id="name number",
        ),
        # --- unknown fields, at both levels ---
        pytest.param(
            {"records": [{"sku": "ab-12", "name": "Brake pad", "banana": 1}]},
            REC + ["banana"],
            "extra_forbidden",
            id="unknown record field",
        ),
        pytest.param(
            {"records": [{"sku": "ab-12", "name": "Brake pad"}], "extra": 1},
            ["body", "extra"],
            "extra_forbidden",
            id="unknown top-level field",
        ),
        # --- the records list itself ---
        pytest.param({}, ["body", "records"], "missing", id="records omitted"),
        pytest.param(
            {"records": None}, ["body", "records"], "list_type", id="records null"
        ),
        pytest.param(
            {"records": {}}, ["body", "records"], "list_type", id="records object"
        ),
        pytest.param(
            {"records": []}, ["body", "records"], "too_short", id="records empty"
        ),
    ],
)
def test_rejects_invalid_input_with_specific_error(payload, loc, error_type):
    response = client.post(URL, json=payload)

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == loc  # WHERE it failed
    assert error["type"] == error_type  # WHY it failed


def test_catalog_preview_accepts_100_records():
    payload = {
        "records": [{"sku": f"sku-{i}", "name": f"Product {i}"} for i in range(100)]
    }
    result = client.post("/v1/catalog-previews", json=payload)

    assert result.status_code == 200


def test_catalog_preview_rejects_101_records():
    payload = {
        "records": [{"sku": f"sku-{i}", "name": f"Product {i}"} for i in range(101)]
    }
    result = client.post("/v1/catalog-previews", json=payload)
    assert result.status_code == 422


def test_catalog_preview_checks_length_after_normalization():
    # "ß" is 1 character but uppercases to "SS": 33 raw chars become 66 > 64.
    payload = {"records": [{"sku": "ß" * 33, "name": "Brake pad"}]}
    result = client.post("/v1/catalog-previews", json=payload)
    assert result.status_code == 422


def test_wrong_method_returns_405_with_allow_header():
    response = client.get(URL)
    assert response.status_code == 405
    assert response.headers["allow"] == "POST"


def test_unknown_route_returns_404():
    response = client.post("/v1/nope", json={})
    assert response.status_code == 404


def test_nonjson_content_is_rejected():
    response = client.post(
        URL,
        content='{"records":[{"sku":"a","name":"b"}]}',
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "model_attributes_type"


def test_malformed_json_is_rejected():
    # Policy: FastAPI default kept (HTTP's closer fit would be 400).
    response = client.post(
        URL,
        content='{"records":[',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"


def test_missing_body_is_rejected():
    response = client.post(URL)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
