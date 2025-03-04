from typing import TypedDict


class HintRequirementsDict(TypedDict):
    """
    Represents the requirements of a hint in CTFd.
    """

    prerequisites: list[int]
