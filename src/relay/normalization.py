"""Catalog normalization rules.

Pure functions: str in, str out. This module imports nothing from relay,
so every other module can depend on it without creating an import cycle.
"""


def normalize_sku(sku: str) -> str:
    """Trim outer whitespace and uppercase."""
    return sku.strip().upper()


def normalize_name(name: str) -> str:
    """Collapse every run of whitespace to a single space and trim the ends."""
    return " ".join(name.split())
