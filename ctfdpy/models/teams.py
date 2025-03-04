from __future__ import annotations

from datetime import datetime

from pydantic import AnyHttpUrl, Field

from ctfdpy.models.model import CreatePayloadModel, ResponseModel


class TeamAdminView(ResponseModel):
    id: int = Field(frozen=True, exclude=True)
    oauth_id: int | None = Field(None, frozen=True, exclude=True)

    name: str
    email: str | None

    banned: bool
    hidden: bool

    website: AnyHttpUrl | None
    affiliation: str | None
    country: str | None

    bracket_id: int | None
    captain_id: int | None

    fields: list
    secret: str | None

    created: datetime


class CreateTeamPayload(CreatePayloadModel):
    name: str = Field(min_length=1, max_length=128)
    email: str | None = Field(None, min_length=1, max_length=128)
    password: str

    banned: bool = False
    hidden: bool = False

    website: AnyHttpUrl | None = None
    affiliation: str | None = None
    country: str | None = None

    bracket_id: int | None = None
    captain_id: int | None = None

    fields: list = Field(default_factory=list)
    secret: str | None = None
