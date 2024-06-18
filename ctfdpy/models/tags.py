from __future__ import annotations

from pydantic import AliasChoices, Field

from ctfdpy.models.model import ResponseModel


class Tag(ResponseModel):
    """
    Represents a tag in CTFd.

    Parameters
    ----------
    id : int
        The ID of the tag
    value : str
        The value of the tag
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge the tag is associated with

    Attributes
    ----------
    id : int
        The ID of the tag, read-only
    value : str
        The value of the tag
    challenge_id : int
        The ID of the challenge the tag is associated with
    """

    id: int = Field(frozen=True, exclude=True)
    value: str
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
