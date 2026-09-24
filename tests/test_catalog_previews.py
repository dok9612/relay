import pytest
from fastapi.testclient import TestClient

from relay.main import app


client = TestClient(app)


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


@pytest.mark.parametrize(
    "payload",
    [
        # missing required field
        {
            "records": [
                {
                    "sku": "ab-12",
                }
            ]
        },
        # unknown field
        {
            "records": [
                {
                    "sku": "ab-12",
                    "name": "Brake pad",
                    "banana": 123,
                }
            ]
        },
        # wrong type
        {
            "records": [
                {
                    "sku": 123,
                    "name": "Brake pad",
                }
            ]
        },
        # empty list
        {
            "records": [],
        },
        # sku blank after normalization
        {
            "records": [
                {
                    "sku": "     ",
                    "name": "Brake pad",
                }
            ]
        },
        # name blank after normalization
        {
            "records": [
                {
                    "sku": "ab-12",
                    "name": "      ",
                }
            ]
        },
    ],
)
def test_catalog_preview_reject_invalid_request(payload):
    result = client.post("/v1/catalog-previews", json=payload)
    assert result.status_code == 422


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
