from typing import Generic, TypeVar

from typing_extensions import TypedDict

T = TypeVar("T", bound=str)


class ChallengeTagsDict(TypedDict):
    value: str


class ChallengeTypeTemplatesDict(TypedDict):
    """
    Represents the HTML templates for the UI to edit the challenge type
    """

    create: str
    update: str
    view: str


class ChallengeTypeScriptsDict(TypedDict):
    """
    Represents the JavaScript scripts for the UI to edit the challenge type
    """

    create: str
    update: str
    view: str


class ChallengeTypeDataDict(Generic[T], TypedDict):
    id: T
    name: T
    templates: ChallengeTypeTemplatesDict
    scripts: ChallengeTypeScriptsDict


class ChallengeRequirementsDict(TypedDict):
    """
    Represents the requirements of a challenge
    """

    prerequisites: list[int]
    anonymize: bool
