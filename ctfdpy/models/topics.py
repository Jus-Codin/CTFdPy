from __future__ import annotations

from pydantic import AliasChoices, Field

from ctfdpy.models.model import ResponseModel


class Topic(ResponseModel):
    """
    Represents a topic in CTFd.

    Parameters
    ----------
    id : int
        The ID of the topic
    value : str
        The value of the topic

    Attributes
    ----------
    id : int
        The ID of the topic, read-only
    value : str
        The value of the topic
    """

    id: int = Field(frozen=True, exclude=True)
    value: str


class ChallengeTopicReference(ResponseModel):
    """
    Represents a reference to a topic for a challenge in CTFd.

    Parameters
    ----------
    id : int
        The ID of the challenge-topic reference
    challenge : int
        Alias for `challenge_id`
    challenge_id : int
        The ID of the challenge associated with the topic
    topic : int
        Alias for `topic_id`
    topic_id : int
        The ID of the topic associated with the challenge

    Attributes
    ----------
    id : int
        The ID of the challenge-topic reference, read-only
    challenge_id : int
        The ID of the challenge associated with the topic
    topic_id : int
        The ID of the topic associated with the challenge
    """

    id: int = Field(frozen=True, exclude=True)
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )
    topic_id: int = Field(validation_alias=AliasChoices("topic_id", "topic"))
