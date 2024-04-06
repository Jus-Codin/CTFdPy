from __future__ import annotations

from enum import StrEnum
from typing import TypedDict

from pydantic import AliasChoices, Field

from ctfdpy.models.model import CreatePayloadModel, Model, UpdatePayloadModel
from ctfdpy.utils import MISSING


class HintType:
    STANDARD = "standard"


class HintRequirementsDict(TypedDict):
    """
    Represents the requirements of a hint in CTFd.
    """

    prerequisites: list[int]


class BaseHint(Model):
    """
    A base hint model. Not meant to be instantiated directly.

    Parameters
    ----------
    id : int
        The ID of the hint
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    type : HintType
        The type of the hint
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint
    """

    id: int = Field(frozen=True, exclude=True)
    type: HintType
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
    cost: int

    def to_update_payload(self) -> UpdateHintPayload:
        """
        Converts the hint to a payload for updating hints.

        Returns
        -------
        HintUpdatePayload
            The payload for updating hints
        """
        return UpdateHintPayload.model_validate(self, from_attributes=True)


class Hint(BaseHint):
    """
    Represents a hint in CTFd.

    Parameters
    ----------
    id : int
        The ID of the hint
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    content : str
        The content of the hint
    html : str
        The HTML content of the hint
    cost : int
        The cost of the hint
    requirements : HintRequirementsDict | None
        The requirements of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    type : HintType
        The type of the hint
    challenge_id : int
        The ID of the challenge associated with the hint
    content : str
        The content of the hint
    html : str
        The HTML content of the hint, read-only
    cost : int
        The cost of the hint
    requirements : HintRequirementsDict | None
        The requirements of the hint
    """

    content: str
    html: str = Field(frozen=True, exclude=True)
    requirements: HintRequirementsDict | None = None


class LockedHint(BaseHint):
    """
    Represents a locked hint in CTFd.

    Parameters
    ----------
    id : int
        The ID of the hint
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    type : HintType
        The type of the hint
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint
    """


class UnlockedHint(BaseHint):
    """
    Represents an unlocked hint in CTFd.

    Parameters
    ----------
    id : int
        The ID of the hint
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    content : str
        The content of the hint
    html : str
        The HTML content of the hint
    cost : int
        The cost of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    type : HintType
        The type of the hint
    challenge_id : int
        The ID of the challenge associated with the hint
    content : str
        The content of the hint
    html : str
        The HTML content of the hint, read-only
    cost : int
        The cost of the hint
    """

    content: str
    html: str = Field(frozen=True, exclude=True)


class CreateHintPayload(CreatePayloadModel):
    """
    Represents a hint create payload in CTFd.

    Parameters
    ----------
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint
    content : str
        The content of the hint
    requirements : HintRequirementsDict | None
        The requirements of the hint
    """

    type: HintType
    challenge_id: int = (
        Field(validation_alias=AliasChoices("challenge_id", "challenge")),
    )
    cost: int
    content: str
    requirements: HintRequirementsDict | None


class UpdateHintPayload(UpdatePayloadModel):
    """
    Represents a hint update payload in CTFd.

    Parameters
    ----------
    type : HintType
        The type of the hint
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint
    content : str
        The content of the hint
    requirements : HintRequirementsDict | None
        The requirements of the hint. Specify `None` to remove the requirements

    Attributes
    ----------
    type : HintType
        The type of the hint
    challenge_id : int
        The ID of the challenge associated with the hint
    cost : int
        The cost of the hint
    content : str
        The content of the hint
    requirements : HintRequirementsDict | None
        The requirements of the hint
    """

    type: HintType = MISSING
    challenge_id: int = Field(
        MISSING, validation_alias=AliasChoices("challenge_id", "challenge")
    )
    cost: int = MISSING
    content: str = MISSING
    requirements: HintRequirementsDict | None = MISSING
