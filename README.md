# Relay

[![CI](https://github.com/dok9612/relay/actions/workflows/ci.yml/badge.svg)](https://github.com/dok9612/relay/actions/workflows/ci.yml)

A batch-processing API for normalizing product-catalog records.

## Setup

Requires [uv](https://docs.astral.sh/uv/). It installs Python 3.14 if needed.

```bash
uv sync --locked
```

## Run

```bash
uv run uvicorn relay.main:app --reload
```

Interactive docs: http://127.0.0.1:8000/docs

## Test

```bash
uv run pytest -q
```

## Checks

The same checks run in CI on every push and pull request:

```bash
uv run ruff format --check
uv run ruff check
uv run mypy
uv run pytest -q
```

To run them automatically before each commit: `uv run pre-commit install`.

## Example

```bash
curl -i -X POST http://127.0.0.1:8000/v1/catalog-previews \
  -H 'Content-Type: application/json' \
  -d '{"records":[{"sku":" ab-12 ","name":"  Brake   pad  "}]}'
```

Response (`200 OK`):

```json
{"records":[{"sku":"AB-12","name":"Brake pad"}],"count":1}
```

## Rules

- SKU: trim outer whitespace, uppercase. 1–64 characters after normalization.
  Allowed characters: `A–Z`, `a–z`, `0–9`, `-`, `_`, `.` (ASCII only; see SKU policy).
- Name: collapse whitespace runs to one space, trim. 1–200 characters after normalization.
- 1–100 records per request. Each record has exactly `sku` and `name`, both strings.
- Order and duplicates are preserved. Nothing is stored.

## SKU character policy

SKUs are identifiers that people and machines compare exactly (search, scanning,
labels), so they use a small, unambiguous alphabet. Rejected examples:

- Look-alikes from other alphabets: Cyrillic `А` is a different character from Latin `A`.
- Characters that change length when uppercased: `ß` → `SS`, `ﬀ` → `FF`.
- Non-ASCII letters that uppercase into ASCII: `ı` → `I`, `ſ` → `S`.
- Invisible characters and inner whitespace.

Product **names** stay full Unicode: they are display text for humans, not identifiers.

## Error behavior

| Situation | Status | Why |
|---|---|---|
| Wrong method (e.g. GET) | 405 + `Allow: POST` | HTTP rule |
| Unknown path | 404 | HTTP rule |
| Body not labeled `application/json` | 422 | FastAPI default, kept (HTTP's closer fit is 415) |
| Malformed JSON | 422 | FastAPI default, kept (HTTP's closer fit is 400) |
| Missing field or body, `null`, wrong type, unknown field | 422 | Our policy: strict schema |
| Empty, blank, or too long after normalization | 422 | Our policy: normalization rules |
| SKU with a character outside the allowed set | 422 | Our policy: SKU character policy |

422 errors look like `{"detail": [{"loc": [...], "type": "...", "msg": "..."}]}`,
where `loc` says where the problem is and `type` says why.
404 and 405 return `{"detail": "..."}`. A single error format is planned (R18).

## Project layout

- `src/relay/normalization.py`: the normalization rules (pure functions, no framework imports)
- `src/relay/schemas.py`: request/response contracts and input validation
- `src/relay/preview.py`: builds a preview response from a validated request
- `src/relay/main.py`: the FastAPI app and route
- `tests/conftest.py`: shared fixtures (a fresh `TestClient` per test)
- `tests/`: unit tests for the rules and the preview, API tests through `TestClient`,
  and Hypothesis property tests (`test_properties.py`)
