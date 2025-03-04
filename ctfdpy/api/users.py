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
from ctfdpy.models.users import (
    CreateUserPayload,
    UpdateSelfUserPayload,
    UpdateUserPayload,
    UserAdminView,
    UserListing,
    UserPrivateView,
    UserPublicView,
    UserType,
)
from ctfdpy.utils import MISSING, admin_only, auth_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


user_listing_list_adapter = TypeAdapter(list[UserListing])

user_adapter = TypeAdapter(UserPublicView | UserAdminView)


class UsersAPI:
    """
    Interface for interacting with the `/api/v1/users` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    def list(
        self,
        *,
        affiliation: str | None = None,
        country: str | None = None,
        bracket: str | None = None,
        q: str | None = None,
        field: (
            Literal["name", "website", "country", "bracket", "affiliation", "email"]
            | None
        ) = None,
        view: Literal["admin"] | None = None,
        page: int | None = None,
    ) -> list[UserListing]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if affiliation is not None:
            params["affiliation"] = affiliation
        if country is not None:
            params["country"] = country
        if bracket is not None:
            params["bracket"] = bracket
        if q is not None:
            params["q"] = q
            params["field"] = field
        if view is not None:
            params["view"] = view
        if page is not None:
            params["page"] = page

        return self._client.request(
            "GET",
            "/api/v1/users",
            params=params,
            response_model=user_listing_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    async def async_list(
        self,
        *,
        affiliation: str | None = None,
        country: str | None = None,
        bracket: str | None = None,
        q: str | None = None,
        field: (
            Literal["name", "website", "country", "bracket", "affiliation", "email"]
            | None
        ) = None,
        view: Literal["admin"] | None = None,
        page: int | None = None,
    ) -> list[UserListing]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if affiliation is not None:
            params["affiliation"] = affiliation
        if country is not None:
            params["country"] = country
        if bracket is not None:
            params["bracket"] = bracket
        if q is not None:
            params["q"] = q
            params["field"] = field
        if view is not None:
            params["view"] = view
        if page is not None:
            params["page"] = page

        return await self._client.arequest(
            "GET",
            "/api/v1/users",
            params=params,
            response_model=user_listing_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @overload
    def create(
        self, *, payload: CreateUserPayload, notify: bool = False
    ) -> UserAdminView: ...

    @overload
    async def async_create(
        self, *, payload: CreateUserPayload, notify: bool = False
    ) -> UserAdminView: ...

    @overload
    def create(
        self,
        *,
        name: str,
        email: str,
        password: str,
        type: UserType = UserType.USER,
        banned: bool = False,
        hidden: bool = False,
        verified: bool = False,
        language: str | None = None,
        website: str | None = None,
        affiliation: str | None = None,
        country: str | None = None,
        bracket_id: int | None = None,
        fields: list | None = None,
        secret: str | None = None,
        notify: bool = False,
    ) -> UserAdminView: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        email: str,
        password: str,
        type: UserType = UserType.USER,
        banned: bool = False,
        hidden: bool = False,
        verified: bool = False,
        language: str | None = None,
        website: str | None = None,
        affiliation: str | None = None,
        country: str | None = None,
        bracket_id: int | None = None,
        fields: list | None = None,
        secret: str | None = None,
        notify: bool = False,
    ) -> UserAdminView: ...

    @admin_only
    def create(
        self,
        *,
        payload: CreateUserPayload = MISSING,
        notify: bool = False,
        **kwargs,
    ) -> UserAdminView:
        if payload is MISSING:
            try:
                payload = CreateUserPayload.model_validate(kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        if notify:
            return self._client.request(
                "POST",
                "/api/v1/users",
                params={"notify": "true"},
                json=payload.dump_json(),
                response_model=UserAdminView,
                error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
            )
        else:
            return self._client.request(
                "POST",
                "/api/v1/users",
                json=payload.dump_json(),
                response_model=UserAdminView,
                error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
            )

    @admin_only
    async def async_create(
        self,
        *,
        payload: CreateUserPayload = MISSING,
        notify: bool = False,
        **kwargs,
    ) -> UserAdminView:
        if payload is MISSING:
            try:
                payload = CreateUserPayload.model_validate(kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        if notify:
            return await self._client.arequest(
                "POST",
                "/api/v1/users",
                params={"notify": "true"},
                json=payload.dump_json(),
                response_model=UserAdminView,
                error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
            )
        else:
            return await self._client.arequest(
                "POST",
                "/api/v1/users",
                json=payload.dump_json(),
                response_model=UserAdminView,
                error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
            )

    @auth_only
    def get_self(self) -> UserPrivateView:
        return self._client.request(
            "GET",
            "/api/v1/users/me",
            response_model=UserPrivateView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @auth_only
    async def async_get_self(self) -> UserPrivateView:
        return await self._client.arequest(
            "GET",
            "/api/v1/users/me",
            response_model=UserPrivateView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @overload
    def update_self(self, *, payload: UpdateSelfUserPayload) -> UserPrivateView: ...

    @overload
    async def async_update_self(
        self, *, payload: UpdateSelfUserPayload
    ) -> UserPrivateView: ...

    @overload
    def update_self(
        self,
        *,
        name: str = MISSING,
        email: str = MISSING,
        password: str = MISSING,
        # only needed if password is provided and user is not admin
        old_password: str = MISSING,
        language: str | None = MISSING,
        website: str | None = MISSING,
        affiliation: str | None = MISSING,
        country: str | None = MISSING,
        fields: list = MISSING,
    ) -> UserPrivateView: ...

    @overload
    async def async_update_self(
        self,
        *,
        name: str = MISSING,
        email: str = MISSING,
        password: str = MISSING,
        # only needed if password is provided and user is not admin
        old_password: str = MISSING,
        language: str | None = MISSING,
        website: str | None = MISSING,
        affiliation: str | None = MISSING,
        country: str | None = MISSING,
        fields: list = MISSING,
    ) -> UserPrivateView: ...

    @auth_only
    def update_self(
        self,
        *,
        payload: UpdateSelfUserPayload | None = None,
        **kwargs,
    ) -> UserPrivateView:
        if payload is None:
            try:
                payload = UpdateSelfUserPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "PATCH",
            "/api/v1/users/me",
            json=payload.dump_json(),
            response_model=UserPrivateView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @auth_only
    def get_self_awards(self):
        raise NotImplementedError

    @auth_only
    async def async_get_self_awards(self):
        raise NotImplementedError

    @auth_only
    def get_self_fails(self):
        raise NotImplementedError

    @auth_only
    async def async_get_self_fails(self):
        raise NotImplementedError

    @auth_only
    def get_self_solves(self):
        raise NotImplementedError

    @auth_only
    async def async_get_self_solves(self):
        raise NotImplementedError

    def get(self, user_id: int) -> UserPublicView | UserAdminView:
        return self._client.request(
            "GET",
            f"/api/v1/users/{user_id}",
            response_model=user_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    async def async_get(self, user_id: int) -> UserPublicView | UserAdminView:
        return await self._client.arequest(
            "GET",
            f"/api/v1/users/{user_id}",
            response_model=user_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @overload
    def update(self, user_id: int, *, payload: UpdateUserPayload) -> UserAdminView: ...

    @overload
    async def async_update(
        self, user_id: int, *, payload: UpdateUserPayload
    ) -> UserAdminView: ...

    @overload
    def update(
        self,
        user_id: int,
        *,
        name: str = MISSING,
        email: str = MISSING,
        password: str = MISSING,
        type: UserType = MISSING,
        banned: bool = MISSING,
        hidden: bool = MISSING,
        verified: bool = MISSING,
        language: str | None = MISSING,
        website: str | None = MISSING,
        affiliation: str | None = MISSING,
        country: str | None = MISSING,
        bracket_id: int | None = MISSING,
        fields: list = MISSING,
        secret: str = MISSING,
    ) -> UserAdminView: ...

    @overload
    async def async_update(
        self,
        user_id: int,
        *,
        name: str = MISSING,
        email: str = MISSING,
        password: str = MISSING,
        type: UserType = MISSING,
        banned: bool = MISSING,
        hidden: bool = MISSING,
        verified: bool = MISSING,
        language: str | None = MISSING,
        website: str | None = MISSING,
        affiliation: str | None = MISSING,
        country: str | None = MISSING,
        bracket_id: int | None = MISSING,
        fields: list = MISSING,
        secret: str = MISSING,
    ) -> UserAdminView: ...

    @admin_only
    def update(
        self,
        user_id: int,
        *,
        payload: UpdateUserPayload = MISSING,
        **kwargs,
    ) -> UserAdminView:
        if payload is MISSING:
            try:
                payload = UpdateUserPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "PATCH",
            f"/api/v1/users/{user_id}",
            json=payload.dump_json(),
            response_model=UserAdminView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_update(
        self,
        user_id: int,
        *,
        payload: UpdateUserPayload = MISSING,
        **kwargs,
    ) -> UserAdminView:
        if payload is MISSING:
            try:
                payload = UpdateUserPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "PATCH",
            f"/api/v1/users/{user_id}",
            json=payload.dump_json(),
            response_model=UserAdminView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def delete(self, user_id: int) -> bool:
        return self._client.request(
            "DELETE",
            f"/api/v1/users/{user_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, user_id: int) -> bool:
        return await self._client.arequest(
            "DELETE",
            f"/api/v1/users/{user_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    def get_awards(self, user_id: int):
        raise NotImplementedError

    async def async_get_awards(self, user_id: int):
        raise NotImplementedError

    def get_fails(self, user_id: int):
        raise NotImplementedError

    async def async_get_fails(self, user_id: int):
        raise NotImplementedError

    def get_solves(self, user_id: int):
        raise NotImplementedError

    async def async_get_solves(self, user_id: int):
        raise NotImplementedError

    @admin_only
    def email(self, user_id: int, text: str):
        return self._client.request(
            "POST",
            f"/api/v1/users/{user_id}/email",
            json={"text": text},
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_email(self, user_id: int, text: str):
        return await self._client.arequest(
            "POST",
            f"/api/v1/users/{user_id}/email",
            json={"text": text},
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
