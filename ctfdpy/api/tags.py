from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import TypeAdapter

from ctfdpy.exceptions import BadRequest, Forbidden, NotFound, Unauthorized
from ctfdpy.models.tags import Tag
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


tag_list_adapter = TypeAdapter(list[Tag])


class TagsAPI:
    """
    Interface for interacting with the `/api/v1/tags` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    @admin_only
    def list(
        self,
        *,
        value: str | None = None,
        challenge_id: int | None = None,
        q: str | None = None,
        field: Literal["value", "challenge_id"] | None = None,
    ) -> list[Tag]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if value is not None:
            params["value"] = value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if q is not None:
            params["q"] = q
            params["field"] = field

        return self._client.request(
            "GET",
            "/api/v1/tags",
            params=params,
            model=tag_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @admin_only
    async def async_list(
        self,
        *,
        value: str | None = None,
        challenge_id: int | None = None,
        q: str | None = None,
        field: Literal["value", "challenge_id"] | None = None,
    ) -> list[Tag]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if value is not None:
            params["value"] = value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if q is not None:
            params["q"] = q
            params["field"] = field

        return await self._client.request(
            "GET",
            "/api/v1/tags",
            params=params,
            model=tag_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @admin_only
    def create(self, value: str, challenge_id: int) -> Tag:
        return self._client.request(
            "POST",
            "/api/v1/tags",
            json={"value": value, "challenge_id": challenge_id},
            response_model=Tag,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_create(self, value: str, challenge_id: int) -> Tag:
        return await self._client.request(
            "POST",
            "/api/v1/tags",
            json={"value": value, "challenge_id": challenge_id},
            response_model=Tag,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get(self, tag_id: int) -> Tag:
        return self._client.request(
            "GET",
            f"/api/v1/tags/{tag_id}",
            response_model=Tag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_get(self, tag_id: int) -> Tag:
        return await self._client.request(
            "GET",
            f"/api/v1/tags/{tag_id}",
            response_model=Tag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def update(
        self,
        tag_id: int,
        *,
        value: str = MISSING,
        challenge_id: int = MISSING,
    ) -> Tag:
        payload = {}
        if value is not MISSING:
            payload["value"] = value
        if challenge_id is not MISSING:
            # I have no idea what would happen if this is changed
            payload["challenge_id"] = challenge_id

        return self._client.request(
            "PATCH",
            f"/api/v1/tags/{tag_id}",
            json=payload,
            response_model=Tag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_update(
        self,
        tag_id: int,
        *,
        value: str = MISSING,
        challenge_id: int = MISSING,
    ) -> Tag:
        payload = {}
        if value is not MISSING:
            payload["value"] = value
        if challenge_id is not MISSING:
            # I have no idea what would happen if this is changed
            payload["challenge_id"] = challenge_id

        return await self._client.request(
            "PATCH",
            f"/api/v1/tags/{tag_id}",
            json=payload,
            response_model=Tag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def delete(self, tag_id: int) -> Literal[True]:
        return self._client.request(
            "DELETE",
            f"/api/v1/tags/{tag_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, tag_id: int) -> Literal[True]:
        return await self._client.request(
            "DELETE",
            f"/api/v1/tags/{tag_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
