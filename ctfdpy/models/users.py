from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import AliasChoices, AnyHttpUrl, EmailStr, Field

from ctfdpy.models.model import CreatePayloadModel, ResponseModel, UpdatePayloadModel
from ctfdpy.utils import MISSING


class UserType(StrEnum):
    ADMIN = "admin"
    USER = "user"


class BaseUser(ResponseModel):
    """
    A base user model. Not meant to be instantiated directly.

    Parameters
    ----------
    id : int
        The ID of the user
    oauth_id : int | None
        The OAuth ID of the user
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user

    Attributes
    ----------
    id : int
        The ID of the user
    oauth_id : int | None
        The OAuth ID of the user
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    """

    id: int = Field(frozen=True, exclude=True)
    oauth_id: int | None = Field(None, frozen=True, exclude=True)

    name: str

    website: str | None
    affiliation: str | None
    country: str | None

    bracket_id: int | None
    team_id: int | None

    fields: list  # not fully implemented by us yet

    def to_update_paylaod(self) -> UpdateUserPayload:
        """
        Converts the user to a payload for updating users.

        Returns
        -------
        UpdateUserPayload
            The payload for updating users
        """
        return UpdateUserPayload.model_validate(self, from_attributes=True)


class UserListing(BaseUser):
    """
    Represents a user listing in CTFd.

    Returned by the `GET /users` endpoint.

    Parameters
    ----------
    id : int
        The ID of the user
    oauth_id : int | None
        The OAuth ID of the user
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user

    Attributes
    ----------
    id : int
        The ID of the user, read-only
    oauth_id : int | None
        The OAuth ID of the user, read-only
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    """


class UserPublicView(BaseUser):
    """
    Represents a public view of a user in CTFd.

    Parameters
    ----------
    id : int
        The ID of the user
    oauth_id : int | None
        The OAuth ID of the user
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    place : int | None
        The placing of the user. Not returned by all endpoints
    score : int | None
        The score of the user. Not returned by all endpoints

    Attributes
    ----------
    id : int
        The ID of the user, read-only
    oauth_id : int | None
        The OAuth ID of the user, read-only
    name : str
        The name of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    place : int | None
        The placing of the user. Not returned by all endpoints
    score : int | None
        The score of the user. Not returned by all endpoints
    """

    place: int | None = None
    score: int | None = None


class UserPrivateView(BaseUser):
    """
    Represents a private view of a user in CTFd.

    This is returned when viewing the user's own profile.

    Parameters
    ----------
    id : int
        The ID of the user
    oauth_id : int | None
        The OAuth ID of the user
    name : str
        The name of the user
    email : str
        The email of the user
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    place : int
        The placing of the user. Not returned by all endpoints
    score : int
        The score of the user. Not returned by all endpoints

    Attributes
    ----------
    id : int
        The ID of the user, read-only
    oauth_id : int | None
        The OAuth ID of the user, read-only
    name : str
        The name of the user
    email : str
        The email of the user
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    place : int
        The placing of the user. Not returned by all endpoints
    score : int
        The score of the user. Not returned by all endpoints
    """

    email: str
    language: str | None
    place: int | None = None
    score: int | None = None


class UserAdminView(BaseUser):
    """
    Represents an admin view of a user in CTFd.

    This is returned when viewing a user as an admin.

    Parameters
    ----------
    id : int
        The ID of the user, read-only
    oauth_id : int | None
        The OAuth ID of the user, read-only
    name : str
        The name of the user
    email : str
        The email of the user
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    created : datetime
        The creation date of the user
    secret : str
        Not sure what this is
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    place : int
        The placing of the user. Not returned by all endpoints
    score : int
        The score of the user. Not returned by all endpoints

    Attributes
    ----------
    id : int
        The ID of the user, read-only
    oauth_id : int | None
        The OAuth ID of the user, read-only
    name : str
        The name of the user
    email : str
        The email of the user
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    team_id : int | None
        The ID of the team the user is in
    fields : list
        The fields of the user
    created : datetime
        The creation date of the user
    secret : str
        Not sure what this is
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    place : int
        The placing of the user. Not returned by all endpoints
    score : int
        The score of the user. Not returned by all endpoints
    """

    email: str

    created: datetime
    secret: str | None  # not sure what this is

    type: UserType

    banned: bool
    hidden: bool
    verified: bool

    place: int | None = None
    score: int | None = None


class CreateUserPayload(CreatePayloadModel):
    """
    Represents a user create payload in CTFd.

    Parameters
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user
    secret : str | None
        Not sure what this is

    Attributes
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user
    secret : str | None
        Not sure what this is
    """

    name: str = Field(min_length=1, max_length=128)
    email: EmailStr = Field(min_length=1, max_length=128)
    password: str

    type: UserType = UserType.USER

    banned: bool = False
    hidden: bool = False
    verified: bool = False

    language: str | None = None
    website: AnyHttpUrl | None = None
    affiliation: str | None = None
    country: str | None = None

    bracket_id: int | None = None
    fields: list = Field(default_factory=list)
    secret: str | None = None


class UpdateSelfUserPayload(UpdatePayloadModel):
    """
    Represents a self user update payload in CTFd.

    Parameters
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    confirm : str
        The old password of the user. Must be provided if `password` is provided and user is not an admin
    old_password : str
        Alias for `confirm`
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user

    Attributes
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    confirm : str
        The old password of the user. Must be provided if `password` is provided and user is not an admin
    old_password : str
        Alias for `confirm`
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user
    """

    name: str = Field(MISSING, min_length=1, max_length=128)
    email: EmailStr = Field(MISSING, min_length=1, max_length=128)

    password: str = MISSING
    confirm: str = Field(
        MISSING, validation_alias=AliasChoices("confirm", "old_password")
    )

    language: str | None = MISSING
    website: AnyHttpUrl | None = MISSING
    affiliation: str | None = MISSING
    country: str | None = MISSING

    bracket_id: int | None = MISSING
    fields: list = MISSING


class UpdateUserPayload(UpdatePayloadModel):
    """
    Represents a user update payload in CTFd.

    Parameters
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    confirm : str
        The old password of the user.
    old_password : str
        Alias for `confirm`
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user
    secret : str | None
        Not sure what this is
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified

    Attributes
    ----------
    name : str
        The name of the user
    email : str
        The email of the user
    password : str
        The password of the user
    confirm : str
        The old password of the user.
    old_password : str
        Alias for `confirm`
    type : UserType
        The type of the user
    banned : bool
        Whether the user is banned
    hidden : bool
        Whether the user is hidden
    verified : bool
        Whether the user is verified
    language : str | None
        The language setting of the user
    website : str | None
        The website of the user
    affiliation : str | None
        The affiliation of the user
    country : str | None
        The country of the user
    bracket_id : int | None
        The ID of the bracket the user is in
    fields : list
        The fields of the user
    secret : str | None
        Not sure what this is
    """

    name: str = Field(MISSING, min_length=1, max_length=128)
    email: EmailStr = Field(MISSING, min_length=1, max_length=128)

    password: str = MISSING
    confirm: str = Field(
        MISSING, validation_alias=AliasChoices("confirm", "old_password")
    )  # since this payload is only used in admin endpoints, technically we don't need this?

    type: UserType = MISSING

    banned: bool = MISSING
    hidden: bool = MISSING
    verified: bool = MISSING

    language: str | None = MISSING
    website: AnyHttpUrl | None = MISSING
    affiliation: str | None = MISSING
    country: str | None = MISSING

    bracket_id: int | None = MISSING
    fields: list = MISSING
    secret: str | None = MISSING
