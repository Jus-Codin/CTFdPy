from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import AliasChoices, Field

from ctfdpy.models.model import CreatePayloadModel, ResponseModel, UpdatePayloadModel
from ctfdpy.types.flags import FlagTypeTemplatesDict
from ctfdpy.utils import MISSING


class FlagType(StrEnum):
    STATIC = "static"
    REGEX = "regex"


class Flag(ResponseModel):
    """
    Represents a flag in CTFd.

    Parameters
    ----------
    id : int
        The ID of the flag
    type : FlagType
        The type of the flag
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge the flag is associated with
    content : str
        The content of the flag
    data : str
        Additional data for the flag, currently only supports `"case_insensitive"`

    Attributes
    ----------
    id : int
        The ID of the flag, read-only
    type : FlagType
        The type of the flag
    challenge_id : int
        The ID of the challenge the flag is associated with
    content : str
        The content of the flag
    data : str
        Additional data for the flag, currently only supports `"case_insensitive"`

    Properties
    ----------
    is_case_insensitive : bool
        Whether the flag is case-insensitive or not
    """

    id: int = Field(frozen=True, exclude=True)
    type: FlagType
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
    content: str
    data: Literal["case_insensitive", ""]
    templates: FlagTypeTemplatesDict | None = Field(None, exclude=True)

    @property
    def is_case_insensitive(self) -> bool:
        return self.data == "case_insensitive"

    def to_update_payload(self) -> UpdateFlagPayload:
        """
        Converts the flag to a payload for updating flags.

        Returns
        -------
        UpdateFlagPayload
            The payload for updating flags
        """
        return UpdateFlagPayload.model_validate(self, from_attributes=True)


class FlagTypeInfo(ResponseModel):
    """
    Information about the flag type.

    This is used internally by CTFd to create the UI modals for creating
    and updating flags.

    Parameters
    ----------
    name : str
        The name of the flag type
    templates : FlagTypeTemplatesDict
        The templates for the flag type

    Attributes
    ----------
    name : str
        The name of the flag type
    templates : FlagTypeTemplatesDict
        The templates for the flag type
    """

    name: str
    templates: FlagTypeTemplatesDict


class CreateFlagPayload(CreatePayloadModel):
    """
    Payload to create a flag in CTFd.

    Parameters
    ----------
    type : FlagType
        The type of the flag
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge the flag is associated with
    content : str
        The content of the flag
    data : Literal["case_insensitive", ""]
        Additional data for the flag, currently only supports `"case_insensitive"`
    """

    type: FlagType
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
    content: str
    data: Literal["case_insensitive", ""]


class UpdateFlagPayload(UpdatePayloadModel):
    """
    Payload to update a flag in CTFd.

    Parameters
    ----------
    type : FlagType
        The type of the flag
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge the flag is associated with
    content : str
        The content of the flag
    data : Literal["case_insensitive", ""]
        Additional data for the flag, currently only supports `"case_insensitive"`

    Attributes
    ----------
    type : FlagType
        The type of the flag
    challenge_id : int
        The ID of the challenge the flag is associated with
    content : str
        The content of the flag
    data : Literal["case_insensitive", ""]
        Additional data for the flag, currently only supports `"case_insensitive"`
    """

    type: FlagType = MISSING
    challenge_id: int = Field(
        MISSING, validation_alias=AliasChoices("challenge_id", "challenge")
    )
    content: str = MISSING
    data: Literal["case_insensitive", ""] = MISSING
