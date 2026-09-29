import pytest

URL = "/v1/catalog-previews"


def test_catalog_preview_success(client):
    response = client.post(
        URL,
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
def test_rejects_invalid_input_with_specific_error(client,payload, loc, error_type):
    response = client.post(URL, json=payload)

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == loc  # WHERE it failed
    assert error["type"] == error_type  # WHY it failed


def test_catalog_preview_accepts_100_records(client):
    payload = {
        "records": [{"sku": f"sku-{i}", "name": f"Product {i}"} for i in range(100)]
    }
    result = client.post(URL, json=payload)

    assert result.status_code == 200


def test_catalog_preview_rejects_101_records(client):
    payload = {
        "records": [{"sku": f"sku-{i}", "name": f"Product {i}"} for i in range(101)]
    }
    result = client.post(URL, json=payload)
    assert result.status_code == 422


@pytest.mark.parametrize(
    "sku",
    [
        pytest.param("ß" * 33, id="german sharp s (uppercases to SS)"),
        pytest.param("ﬀ-12", id="ff ligature (uppercases to FF)"),
        pytest.param("АB-12", id="cyrillic A look-alike"),
        pytest.param("ıd-12", id="dotless i (uppercases to ASCII I)"),
        pytest.param("AB 12", id="inner space"),
        pytest.param("AB\x1f12", id="invisible control char"),
        pytest.param("AB#12", id="symbol outside the set"),
    ],
)
def test_sku_outside_allowed_characters_is_rejected(client, sku):
    response = client.post(URL, json={"records": [{"sku": sku, "name": "Brake pad"}]})

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == REC + ["sku"]
    assert error["type"] == "value_error"


def test_sku_allowed_characters_are_accepted_and_uppercased(client):
    response = client.post(
        URL, json={"records": [{"sku": " ab_12.v-2 ", "name": "Brake pad"}]}
    )

    assert response.status_code == 200
    assert response.json()["records"][0]["sku"] == "AB_12.V-2"


def test_wrong_method_returns_405_with_allow_header(client):
    response = client.get(URL)
    assert response.status_code == 405
    assert response.headers["allow"] == "POST"


def test_unknown_route_returns_404(client):
    response = client.post("/v1/nope", json={})
    assert response.status_code == 404


def test_nonjson_content_is_rejected(client):
    response = client.post(
        URL,
        content='{"records":[{"sku":"a","name":"b"}]}',
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "model_attributes_type"


def test_malformed_json_is_rejected(client):
    # Policy: FastAPI default kept (HTTP's closer fit would be 400).
    response = client.post(
        URL,
        content='{"records":[',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "json_invalid"


def test_missing_body_is_rejected(client):
    response = client.post(URL)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"


@pytest.mark.parametrize(
    ("sku", "name", "expected_status"),
    [
        pytest.param("a" * 64, "Brake pad", 200, id="sku at limit 64"),
        pytest.param("a" * 65, "Brake pad", 422, id="sku one past 65"),
        pytest.param(
            "  " + "a" * 64 + "  ", "Brake pad", 200, id="sku 68 raw, 64 after trim"
        ),
        pytest.param("ab-12", "n" * 200, 200, id="name at limit 200"),
        pytest.param("ab-12", "n" * 201, 422, id="name one past 201"),
        pytest.param(
            "ab-12", "a" + " " * 300 + "b", 200, id="name 302 raw, 3 after collapse"
        ),
    ],
)
def test_length_limits_apply_after_normalization(client, sku, name, expected_status):
    response = client.post(URL, json={"records": [{"sku": sku, "name": name}]})
    assert response.status_code == expected_status

def test_preview_preserves_order_duplicates_and_count(client):
    # Deliberately NOT alphabetical: a sorting bug must change the output.
    records = [
        {"sku": "b-2", "name": "Second"},
        {"sku": "a-1", "name": "First"},
        {"sku": "b-2", "name": "Second"},
    ]
    response = client.post(URL, json={"records": records})

    assert response.status_code == 200
    assert response.json() == {
        "records": [
            {"sku": "B-2", "name": "Second"},
            {"sku": "A-1", "name": "First"},
            {"sku": "B-2", "name": "Second"},
        ],
        "count": 3,
    }