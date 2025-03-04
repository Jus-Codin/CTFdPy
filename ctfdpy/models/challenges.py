from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any, Literal

from annotated_types import Len
from pydantic import AliasChoices, Discriminator, Field, Tag

from ctfdpy.models.files import FileType
from ctfdpy.models.model import CreatePayloadModel, ResponseModel, UpdatePayloadModel
from ctfdpy.types.challenges import (
    ChallengeRequirementsDict,
    ChallengeTagsDict,
    ChallengeTypeDataDict,
    ChallengeTypeScriptsDict,
    ChallengeTypeTemplatesDict,
)
from ctfdpy.utils import MISSING


class ChallengeType(StrEnum):
    STANDARD = "standard"
    DYNAMIC = "dynamic"


class ChallengeState(StrEnum):
    VISIBLE = "visible"
    HIDDEN = "hidden"
    LOCKED = "locked"  # undocumented challenge state, I do not recommend using this


class DecayFunction(StrEnum):
    LINEAR = "linear"
    LOGARITHMIC = "logarithmic"


class LockedChallengeHint(ResponseModel):
    """
    Represents a locked challenge hint in CTFd.

    Parameters
    ----------
    id : int
        The ID of the hint
    cost : int
        The cost of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    cost : int
        The cost of the hint
    """

    id: int = Field(frozen=True, exclude=True)
    cost: int


class UnlockedChallengeHint(ResponseModel):
    """
    Represents an unlocked challenge hint in CTFd.

    Parameters
    ----------
    id : int
        The ID of the hint
    cost : int
        The cost of the hint
    content : str
        The content of the hint

    Attributes
    ----------
    id : int
        The ID of the hint, read-only
    cost : int
        The cost of the hint
    content : str
        The content of the hint
    """

    id: int = Field(frozen=True, exclude=True)
    cost: int
    content: str


def _hint_model_discriminator(v: Any) -> str:
    if isinstance(v, dict):
        return "unlocked" if "content" in v else "locked"
    return "unlocked" if getattr(v, "content", None) is not None else "locked"


class ChallengeListing(ResponseModel):
    """
    Represents a challenge listing in CTFd.

    This is returned by the `GET /challenges` endpoint.

    Parameters
    ----------
    id : int
        The ID of the challenge
    type : ChallengeType
        The type of the challenge
    name : str
        The name of the challenge
    value : int
        The value of the challenge
    solves : int
        The number of solves of the challenge
    solved_by_me : bool
        Whether the challenge is solved by the current user
    category : str
        The category of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    template : str
        The HTML template of the modal for the challenge. Used internally by the CTFd frontend.
    script : str
        The Javascript code for the modal for the challenge. Used internally by the CTFd frontend

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    type : ChallengeType
        The type of the challenge
    name : str
        The name of the challenge
    value : int
        The value of the challenge
    solves : int
        The number of solves of the challenge
    solved_by_me : bool
        Whether the challenge is solved by the current user
    category : str
        The category of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    template : str
        The HTML template of the modal for the challenge. Used internally by the CTFd frontend.
    script : str
        The Javascript code for the modal for the challenge. Used internally by the CTFd frontend
    """

    id: int = Field(frozen=True, exclude=True)
    type: ChallengeType
    name: str
    value: int
    solves: int
    solved_by_me: bool
    category: str
    tags: list[ChallengeTagsDict]
    template: str = Field(frozen=True, exclude=True)
    script: str = Field(frozen=True, exclude=True)


class AnonymousChallenge(ResponseModel):
    """
    Represents an anonymized challenge in CTFd.

    All fields in this model will always be the same, except for `id`.

    This can be returned by the `GET /challenges` and `GET /challenges/<int:challenge_id>` endpoints.

    This occurs when the challenge has a prerequisite that has not been solved
    and is set to be anonymized instead of hidden.

    Parameters
    ----------
    id : int
        The ID of the challenge
    type : Literal["hidden"]
        The type of the challenge
    name : Literal["???"]
        The name of the challenge
    value : Literal[0]
        The value of the challenge
    solves : None
        The number of solves of the challenge
    solved_by_me : Literal[False]
        Whether the challenge is solved by the current user
    category : Literal["???"]
        The category of the challenge
    tags : list[Never]
        The tags of the challenge. Always an empty list.
    template : Literal[""]
        The HTML template of the modal for the challenge. Used internally by the CTFd frontend.
    script : Literal[""]
        The Javascript code for the modal for the challenge. Used internally by the CTFd frontend

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    type : Literal["hidden"]
        The type of the challenge
    name : Literal["???"]
        The name of the challenge
    value : Literal[0]
        The value of the challenge
    solves : None
        The number of solves of the challenge
    solved_by_me : Literal[False]
        Whether the challenge is solved by the current user
    category : Literal["???"]
        The category of the challenge
    tags : list[Never]
        The tags of the challenge. Always an empty list.
    template : Literal[""]
        The HTML template of the modal for the challenge. Used internally by the CTFd frontend.
    script : Literal[""]
        The Javascript code for the modal for the challenge. Used internally by the CTFd frontend
    """

    id: int = Field(frozen=True, exclude=True)
    type: Literal["hidden"] = "hidden"
    name: Literal["???"]
    value: Literal[0]
    solves: None
    solved_by_me: Literal[False]
    category: Literal["???"]
    tags: Annotated[list[Any], Len(0, 0)]
    template: Literal[""]
    script: Literal[""]


class _BaseChallenge(ResponseModel):
    """
    Internal base class for challenge models in CTFd.

    This is not meant to be used directly.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type
    """

    id: int = Field(frozen=True, exclude=True)
    name: str
    description: str
    category: str
    state: ChallengeState

    value: int

    connection_info: str | None
    next_id: int | None
    max_attempts: int | None

    type: ChallengeType
    type_data: ChallengeTypeDataDict[str]


class BaseChallenge(_BaseChallenge):
    """
    The base class for challenge models in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend
    """

    solves: int
    solved_by_me: bool
    attempts: int

    files: list[str]
    tags: list[ChallengeTagsDict]
    hints: list[
        Annotated[
            Annotated[LockedChallengeHint, Tag("locked")]
            | Annotated[UnlockedChallengeHint, Tag("unlocked")],
            Discriminator(_hint_model_discriminator),
        ]
    ]

    view: str


class StandardChallenge(BaseChallenge):
    """
    Represents a standard challenge in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend
    """

    type: Literal[ChallengeType.STANDARD] = ChallengeType.STANDARD
    type_data: ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]


class DynamicChallenge(BaseChallenge):
    """
    Represents a dynamic challenge in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]
        The data of the challenge type
    solves : int
        The number of solves the challenge has
    solved_by_me : bool
        Whether the challenge is solved by the current user
    attempts : int
        The number of attempts the current user has made on the challenge
    files : list[str]
        The URL paths to the files of the challenge
    tags : list[ChallengeTagsDict]
        The tags of the challenge
    hints : list[LockedChallengeHint | UnlockedChallengeHint]
        The hints of the challenge
    view : str
        The HTML template of the challenge. Used internally by the CTFd frontend
    """

    value: int = Field(frozen=True, exclude=True)
    initial: int
    decay: int
    minimum: int
    function: DecayFunction

    type: Literal[ChallengeType.DYNAMIC] = ChallengeType.DYNAMIC
    type_data: ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]


class BaseChallengeWriteResult(_BaseChallenge):
    """
    The base class for challenge write results in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : ChallengeType
        The type of the challenge
    type_data : ChallengeTypeDataDict
        The data of the challenge type
    """


class StandardChallengeWriteResult(BaseChallengeWriteResult):
    """
    Represents a standard challenge write result in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]
        The data of the challenge type

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]
        The data of the challenge type
    """

    type: Literal[ChallengeType.STANDARD] = ChallengeType.STANDARD
    type_data: ChallengeTypeDataDict[Literal[ChallengeType.STANDARD]]


class DynamicChallengeWriteResult(BaseChallengeWriteResult):
    """
    Represents a dynamic challenge write result in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]
        The data of the challenge type

    Attributes
    ----------
    id : int
        The ID of the challenge, read-only
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    value : int
        The value of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge
    type_data : ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]
        The data of the challenge type
    """

    value: int = Field(frozen=True, exclude=True)
    initial: int
    decay: int
    minimum: int
    function: DecayFunction

    type: Literal[ChallengeType.DYNAMIC] = ChallengeType.DYNAMIC
    type_data: ChallengeTypeDataDict[Literal[ChallengeType.DYNAMIC]]


class CreateBaseChallengePayload(CreatePayloadModel):
    """
    Represents the base payload for creating a challenge in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    type : ChallengeType
        The type of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    type : ChallengeType
        The type of the challenge
    """

    name: str
    description: str
    category: str
    state: ChallengeState

    connection_info: str | None = None
    next_id: int | None = None
    max_attempts: int | None = None

    requirements: ChallengeRequirementsDict | None = None

    type: ChallengeType


class CreateStandardChallengePayload(CreateBaseChallengePayload):
    """
    Represents the payload for creating a standard challenge in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    value : int
        The value of the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    value : int
        The value of the challenge
    type : Literal[ChallengeType.STANDARD]
        The type of the challenge
    """

    value: int
    type: Literal[ChallengeType.STANDARD] = ChallengeType.STANDARD


class CreateDynamicChallengePayload(CreateBaseChallengePayload):
    """
    Represents the payload for creating a dynamic challenge in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    type : Literal[ChallengeType.DYNAMIC]
        The type of the challenge
    """

    initial: int
    decay: int
    minimum: int
    function: DecayFunction
    type: Literal[ChallengeType.DYNAMIC] = ChallengeType.DYNAMIC


class UpdateBaseChallengePayload(UpdatePayloadModel):
    """
    The base class for challenge update payloads in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    """

    name: str = MISSING
    description: str = MISSING
    category: str = MISSING
    state: ChallengeState = MISSING

    connection_info: str | None = MISSING
    next_id: int | None = MISSING
    max_attempts: int | None = MISSING

    requirements: ChallengeRequirementsDict | None = MISSING


class UpdateStandardChallengePayload(UpdateBaseChallengePayload):
    """
    Represents a standard challenge update payload in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    value : int
        The value of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    value : int
        The value of the challenge
    """

    value: int = MISSING


class UpdateDynamicChallengePayload(UpdateBaseChallengePayload):
    """
    Represents a dynamic challenge update payload in CTFd.

    Parameters
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge

    Attributes
    ----------
    name : str
        The name of the challenge
    description : str
        The description of the challenge
    category : str
        The category of the challenge
    state : ChallengeState
        The state of the challenge
    connection_info : str | None
        The connection information of the challenge
    next_id : int | None
        The ID of the next challenge
    max_attempts : int | None
        The maximum number of attempts for the challenge
    requirements : ChallengeRequirementsDict | None
        The requirements of the challenge
    initial : int
        The initial value of the challenge
    decay : int
        The decay value of the challenge
    minimum : int
        The minimum value of the challenge
    function : DecayFunction
        The decay function of the challenge
    """

    initial: int = MISSING
    decay: int = MISSING
    minimum: int = MISSING
    function: DecayFunction = MISSING


class ChallengeAttemptResult(ResponseModel):
    """
    Represents a challenge attempt result in CTFd.

    This is returned by the `POST /challenges/attempts` endpoint.

    Parameters
    ----------
    status : Literal["correct", "incorrect", "authentication_required", "paused", "ratelimited", "already_solved"]
        The status of the attempt
    message : str
        The message of the attempt

    Attributes
    ----------
    status : Literal["correct", "incorrect", "authentication_required", "paused", "ratelimited", "already_solved"]
        The status of the attempt
    message : str
        The message of the attempt

    Properties
    ----------
    is_correct : bool
        Whether the attempt is correct
    """

    status: Literal[
        "correct",
        "incorrect",
        "authentication_required",
        "paused",
        "ratelimited",
        "already_solved",
    ]
    message: str

    @property
    def is_correct(self) -> bool:
        return self.status == "correct"


class ChallengeTypeInfo(ResponseModel):
    """
    Represents the information of a challenge type in CTFd.

    This is returned by the `GET /challenges/types` endpoint.

    Parameters
    ----------
    id : ChallengeType
        The ID of the challenge type
    name : ChallengeType
        The name of the challenge type
    templates : ChallengeTypeTemplatesDict
        The templates of the challenge type
    scripts : ChallengeTypeScriptsDict
        The scripts of the challenge type
    create : str
        The HTML template for the form to create a challenge of the type
    """

    id: ChallengeType
    name: ChallengeType
    templates: ChallengeTypeTemplatesDict
    scripts: ChallengeTypeScriptsDict
    create: str


class ChallengeFileLocation(ResponseModel):
    """
    Represents a location of a challenge file in CTFd.

    This is returned by the `GET /challenges/<int:challenge_id>/files` endpoint.

    Not to be confused with the `ChallengeFile` model.

    Parameters
    ----------
    id : int
        The ID of the file location
    type : Literal[FileType.CHALLENGE]
        The type of the file location
    location : str
        The URL path to the file

    Attributes
    ----------
    id : int
        The ID of the file location, read-only
    type : Literal[FileType.CHALLENGE]
        The type of the file location
    location : str
        The URL path to the file
    """

    id: int = Field(frozen=True, exclude=True)
    type: Literal[FileType.CHALLENGE]
    location: str


class ChallengeRequirements(ResponseModel):
    """
    Represents the requirements of a challenge in CTFd.

    This is returned by the `GET /challenges/<int:challenge_id>/requirements` endpoint.

    Parameters
    ----------
    prerequisites : list[int]
        The IDs of the prerequisites of the challenge
    anonymize : bool
        Whether the challenge is anonymized

    Attributes
    ----------
    prerequisites : list[int]
        The IDs of the prerequisites of the challenge
    anonymize : bool
        Whether the challenge is anonymized
    """

    prerequisites: list[int]
    anonymize: bool


class ChallengeSolve(ResponseModel):
    """
    Represents a challenge solve in CTFd.

    This is returned by the `GET /challenges/<int:challenge_id>/solves` endpoint.

    Parameters
    ----------
    account_id : int
        The ID of the account that solved the challenge
    name : str
        The name of the account that solved the challenge
    date : datetime
        The date the challenge was solved
    account_url : str
        The URL path to the account that solved the challenge

    Attributes
    ----------
    account_id : int
        The ID of the account that solved the challenge
    name : str
        The name of the account that solved the challenge
    date : datetime
        The date the challenge was solved
    account_url : str
        The URL path to the account that solved the challenge
    """

    account_id: int
    name: str
    date: datetime
    account_url: str


class ChallengeTopic(ResponseModel):
    """
    Represents a challenge topic in CTFd.

    This is returned by the `GET /challenges/<int:challenge_id>/topics` endpoint.

    This model is similar to `ChallengeTopicReference` but includes the topic value.

    Parameters
    ----------
    id : int
        The ID of the challenge topic
    challenge_id : int
        The ID of the challenge
    topic_id : int
        The ID of the topic
    value : str
        The value of the topic

    Attributes
    ----------
    id : int
        The ID of the challenge topic, read-only
    challenge_id : int
        The ID of the challenge
    topic_id : int
        The ID of the topic
    value : str
        The value of the topic
    """

    id: int = Field(frozen=True, exclude=True)
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
    topic_id: int = Field(validation_alias=AliasChoices("topic_id", "topic"))
    value: str
