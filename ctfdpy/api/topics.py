from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from pydantic import TypeAdapter

from ctfdpy.exceptions import BadRequest, Forbidden, NotFound, Unauthorized
from ctfdpy.models.topics import ChallengeTopicReference, Topic
from ctfdpy.types.api import APIResponse
from ctfdpy.utils import admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


topic_list_adapter = TypeAdapter(list[Topic])


class TopicsAPI:
    """
    Interface for interacting with the `/api/v1/topics` CTFd API endpoint.
    """
    def __init__(self, client: APIClient):
        self._client = client

    @admin_only
    def list(
        self,
        *,
        value: str | None = None,
        q: str | None,
        field: Literal["value"] | None = None,
    ) -> list[Topic]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if value is not None:
            params["value"] = value

        if q is not None:
            params["q"] = q
            params["field"] = field

        return self._client.request(
            "GET",
            "/api/v1/topics",
            params=params,
            model=topic_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @admin_only
    async def async_list(
        self,
        *,
        value: str | None = None,
        q: str | None,
        field: Literal["value"] | None = None,
    ) -> list[Topic]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if value is not None:
            params["value"] = value

        if q is not None:
            params["q"] = q
            params["field"] = field

        return await self._client.arequest(
            "GET",
            "/api/v1/topics",
            params=params,
            model=topic_list_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
            },
        )

    @overload
    def create(self, value: str) -> Literal[True]: ...

    @overload
    async def async_create(self, value: str) -> Literal[True]: ...

    @overload
    def create(self, value: str, *, challenge_id: int) -> ChallengeTopicReference: ...

    @overload
    async def async_create(
        self, value: str, *, challenge_id: int
    ) -> ChallengeTopicReference: ...

    @overload
    def create(self, topic_id: int) -> Literal[True]: ...

    @overload
    async def async_create(self, topic_id: int) -> Literal[True]: ...

    @overload
    def create(
        self, topic_id: int, *, challenge_id: int
    ) -> ChallengeTopicReference: ...

    @overload
    async def async_create(
        self, topic_id: int, *, challenge_id: int
    ) -> ChallengeTopicReference: ...

    @admin_only
    def create(
        self, value_or_topic_id: str | int, *, challenge_id: int | None = None
    ) -> ChallengeTopicReference | Literal[True]:
        if isinstance(value_or_topic_id, str):
            params = {"value": value_or_topic_id}
        elif isinstance(value_or_topic_id, int):
            params = {"topic_id": value_or_topic_id}
        else:
            raise TypeError(
                f"value_or_topic_id must be str or int, not {type(value_or_topic_id).__name__}"
            )

        if challenge_id is not None:
            # If challenge_id is provided, create a ChallengeTopic
            params["challenge_id"] = challenge_id
            params["type"] = "challenge"

        try:
            result = self._client.request(
                "POST",
                "/api/v1/topics",
                json=params,
                model=ChallengeTopicReference,
                error_models={
                    400: BadRequest,
                    401: Unauthorized,
                    403: Forbidden,
                    404: NotFound,
                },
            )
        except BadRequest as e:
            response: APIResponse = e.response.json()
            if response["success"] is False and response.get("errors") is None:
                return True
            else:
                raise e from e

        return result

    @admin_only
    async def async_create(
        self, value_or_topic_id: str | int, *, challenge_id: int | None = None
    ) -> ChallengeTopicReference | Literal[True]:
        if isinstance(value_or_topic_id, str):
            params = {"value": value_or_topic_id}
        elif isinstance(value_or_topic_id, int):
            params = {"topic_id": value_or_topic_id}
        else:
            raise TypeError(
                f"value_or_topic_id must be str or int, not {type(value_or_topic_id).__name__}"
            )

        if challenge_id is not None:
            # If challenge_id is provided, create a ChallengeTopic
            params["challenge_id"] = challenge_id
            params["type"] = "challenge"

        try:
            result = await self._client.arequest(
                "POST",
                "/api/v1/topics",
                json=params,
                model=ChallengeTopicReference,
                error_models={
                    400: BadRequest,
                    401: Unauthorized,
                    403: Forbidden,
                    404: NotFound,
                },
            )
        except BadRequest as e:
            response: APIResponse = e.response.json()
            if response["success"] is False and response.get("errors") is None:
                return True
            else:
                raise e from e

        return result

    @admin_only
    def delete_challenge_topic(self, challenge_topic_id: int) -> Literal[True]:
        return self._client.request(
            "DELETE",
            "/api/v1/topics",
            params={
                "type": "challenge",
                "target_id": challenge_topic_id,
            },
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete_challenge_topic(
        self, challenge_topic_id: int
    ) -> Literal[True]:
        return await self._client.arequest(
            "DELETE",
            "/api/v1/topics",
            params={
                "type": "challenge",
                "target_id": challenge_topic_id,
            },
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def get(self, topic_id: int) -> Topic:
        return self._client.request(
            "GET",
            f"/api/v1/topics/{topic_id}",
            model=Topic,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_get(self, topic_id: int) -> Topic:
        return await self._client.arequest(
            "GET",
            f"/api/v1/topics/{topic_id}",
            model=Topic,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def delete(self, topic_id: int) -> Literal[True]:
        return self._client.request(
            "DELETE",
            f"/api/v1/topics/{topic_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, topic_id: int) -> Literal[True]:
        return await self._client.arequest(
            "DELETE",
            f"/api/v1/topics/{topic_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
