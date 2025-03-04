from __future__ import annotations

from typing import TYPE_CHECKING, overload

from pydantic import TypeAdapter, ValidationError

from ctfdpy.exceptions import (
    BadRequest,
    Forbidden,
    ModelValidationError,
    NotFound,
    Unauthorized,
)
from ctfdpy.models.teams import CreateTeamPayload, TeamAdminView
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


member_id_list_adapter = TypeAdapter(list[int])


class TeamsAPI:
    def __init__(self, client: APIClient):
        self._client = client

    @overload
    def create(self, *payload: CreateTeamPayload) -> TeamAdminView: ...

    @overload
    async def async_create(self, *payload: CreateTeamPayload) -> TeamAdminView: ...

    @overload
    def create(
        self,
        *,
        name: str,
        email: str | None = None,
        password: str,
        banned: bool = False,
        hidden: bool = False,
        website: str | None = None,
        affiliation: str | None = None,
        country: str | None = None,
        bracket_id: int | None = None,
        captain_id: int | None = None,
        fields: list | None = None,
        secret: str | None = None,
    ) -> TeamAdminView: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        email: str | None = None,
        password: str,
        banned: bool = False,
        hidden: bool = False,
        website: str | None = None,
        affiliation: str | None = None,
        country: str | None = None,
        bracket_id: int | None = None,
        captain_id: int | None = None,
        fields: list | None = None,
        secret: str | None = None,
    ) -> TeamAdminView: ...

    @admin_only
    def create(
        self,
        *,
        payload: CreateTeamPayload = MISSING,
        **kwargs,
    ) -> TeamAdminView:
        if payload is MISSING:
            try:
                payload = CreateTeamPayload.model_validate(kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "POST",
            "/api/v1/teams",
            json=payload.dump_json(),
            response_model=TeamAdminView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_create(
        self,
        *,
        payload: CreateTeamPayload = MISSING,
        **kwargs,
    ) -> TeamAdminView:
        if payload is MISSING:
            try:
                payload = CreateTeamPayload.model_validate(kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "POST",
            "/api/v1/teams",
            json=payload.dump_json(),
            response_model=TeamAdminView,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def add_member(self, team_id: int, user_id: int) -> list[int]:
        return self._client.request(
            "POST",
            f"/api/v1/teams/{team_id}/members",
            json={"user_id": user_id},
            response_model=member_id_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_add_member(self, team_id: int, user_id: int) -> list[int]:
        return await self._client.arequest(
            "POST",
            f"/api/v1/teams/{team_id}/members",
            json={"user_id": user_id},
            response_model=member_id_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
