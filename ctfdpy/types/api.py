from typing import Any

from typing_extensions import TypedDict


class _PaginationDict(TypedDict):
    page: int
    next: int
    prev: int
    pages: int
    per_page: int
    total: int


class _MetaDict(TypedDict):
    pagination: _PaginationDict


class APIResponse(TypedDict):
    """API response structure."""

    data: Any | None
    success: bool
    errors: list[str] | dict[str, str] | None
    message: str | None
    meta: _MetaDict | None
