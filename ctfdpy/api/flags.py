from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from pydantic import TypeAdapter, ValidationError

from ctfdpy.exceptions import (
    BadRequest,
    Forbidden,
    ModelValidationError,
    NotFound,
    Unauthorized,
)
from ctfdpy.models.flags import (
    CreateFlagPayload,
    Flag,
    FlagType,
    FlagTypeInfo,
    UpdateFlagPayload,
)
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


flag_list_adapter = TypeAdapter(list[Flag])

flag_type_info_dict_adapter = TypeAdapter(dict[str, FlagTypeInfo])


class FlagsAPI:
    """
    Interface for interacting with the `/api/v1/flags` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    @admin_only
    def list(
        self,
        *,
        type: FlagType | None = None,
        challenge_id: int | None = None,
        content: str | None = None,
        data: str | None = None,
        q: str | None = None,
        field: Literal["type", "content", "data"] | None = None,
    ) -> list[Flag]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if content is not None:
            params["content"] = content
        if data is not None:
            params["data"] = data

        if q is not None:
            params["q"] = q
            params["field"] = field

        return self._client.request(
            "GET",
            "/api/v1/flags",
            params=params,
            response_model=flag_list_adapter,
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
        type: FlagType | None = None,
        challenge_id: int | None = None,
        content: str | None = None,
        data: str | None = None,
        q: str | None = None,
        field: Literal["type", "content", "data"] | None = None,
    ) -> list[Flag]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if content is not None:
            params["content"] = content
        if data is not None:
            params["data"] = data

        if q is not None:
            params["q"] = q
            params["field"] = field

        return await self._client.arequest(
            "GET",
            "/api/v1/flags",
            params=params,
            response_model=flag_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @overload
    def create(self, *, payload: CreateFlagPayload) -> Flag: ...

    @overload
    async def async_create(self, *, payload: CreateFlagPayload) -> Flag: ...

    @overload
    def create(
        self,
        *,
        challenge_id: int,
        content: str,
        type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
    ) -> Flag: ...

    @overload
    async def async_create(
        self,
        *,
        challenge_id: int,
        content: str,
        type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
    ) -> Flag: ...

    @admin_only
    def create(
        self,
        *,
        payload: CreateFlagPayload = MISSING,
        challenge_id: int | None = None,
        content: str | None = None,
        type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
    ) -> Flag:
        if payload is MISSING:
            data = "case_insensitive" if case_insensitive else ""
            try:
                payload = CreateFlagPayload(
                    challenge_id=challenge_id,
                    content=content,
                    type=type,
                    data=data,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "POST",
            "/api/v1/flags",
            json=payload.dump_json(),
            response_model=Flag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @admin_only
    async def async_create(
        self,
        *,
        payload: CreateFlagPayload = MISSING,
        challenge_id: int | None = None,
        content: str | None = None,
        type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
    ) -> Flag:
        if payload is MISSING:
            data = "case_insensitive" if case_insensitive else ""
            try:
                payload = CreateFlagPayload(
                    challenge_id=challenge_id,
                    content=content,
                    type=type,
                    data=data,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "POST",
            "/api/v1/flags",
            json=payload.dump_json(),
            response_model=Flag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @admin_only
    def get_flag_types(self) -> dict[str, FlagTypeInfo]:
        return self._client.request(
            "GET",
            "/api/v1/flags/types",
            response_model=flag_type_info_dict_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_flag_types(self) -> dict[str, FlagTypeInfo]:
        return await self._client.arequest(
            "GET",
            "/api/v1/flags/types",
            response_model=flag_type_info_dict_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_flag_type(self, type: str) -> FlagTypeInfo:
        return self._client.request(
            "GET",
            f"/api/v1/flags/types/{type}",
            response_model=FlagTypeInfo,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                500: NotFound,  # it raises KeyError when the flag type does not exist
            },
        )

    @admin_only
    async def async_get_flag_type(self, type: str) -> FlagTypeInfo:
        return await self._client.arequest(
            "GET",
            f"/api/v1/flags/types/{type}",
            response_model=FlagTypeInfo,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                500: NotFound,  # it raises KeyError when the flag type does not exist
            },
        )

    @admin_only
    def get(self, flag_id: int) -> Flag:
        return self._client.request(
            "GET",
            f"/api/v1/flags/{flag_id}",
            response_model=Flag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_get(self, flag_id: int) -> Flag:
        return await self._client.arequest(
            "GET",
            f"/api/v1/flags/{flag_id}",
            response_model=Flag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @overload
    def update(self, flag_id: int, *, payload: UpdateFlagPayload) -> Flag: ...

    @overload
    async def async_update(
        self, flag_id: int, *, payload: UpdateFlagPayload
    ) -> Flag: ...

    @overload
    def update(
        self,
        flag_id: int,
        *,
        challenge_id: int = MISSING,
        content: str = MISSING,
        type: FlagType = MISSING,
        case_insensitive: bool = MISSING,
    ) -> Flag: ...

    @overload
    async def async_update(
        self,
        flag_id: int,
        *,
        challenge_id: int = MISSING,
        content: str = MISSING,
        type: FlagType = MISSING,
        case_insensitive: bool = MISSING,
    ) -> Flag: ...

    @admin_only
    def update(
        self,
        flag_id: int,
        *,
        payload: UpdateFlagPayload = MISSING,
        **kwargs,
    ) -> Flag:
        if payload is MISSING:
            case_insensitive = kwargs.pop("case_insensitive", MISSING)
            if case_insensitive is not MISSING:
                kwargs["data"] = "case_insensitive" if case_insensitive else ""
            try:
                payload = UpdateFlagPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "PATCH",
            f"/api/v1/flags/{flag_id}",
            json=payload.dump_json(),
            response_model=Flag,
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
        flag_id: int,
        *,
        payload: UpdateFlagPayload = MISSING,
        **kwargs,
    ) -> Flag:
        if payload is MISSING:
            case_insensitive = kwargs.pop("case_insensitive", MISSING)
            if case_insensitive is not MISSING:
                kwargs["data"] = "case_insensitive" if case_insensitive else ""
            try:
                payload = UpdateFlagPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "PATCH",
            f"/api/v1/flags/{flag_id}",
            json=payload.dump_json(),
            response_model=Flag,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def delete(self, flag_id: int) -> Literal[True]:
        return self._client.request(
            "DELETE",
            f"/api/v1/flags/{flag_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, flag_id: int) -> Literal[True]:
        return await self._client.arequest(
            "DELETE",
            f"/api/v1/flags/{flag_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
