from __future__ import annotations

from typing import TYPE_CHECKING, Literal, overload

from pydantic import TypeAdapter, ValidationError

from ctfdpy.exceptions import (
    BadRequest,
    Forbidden,
    ModelValidationError,
    NotFound,
    Unauthorized,
)
from ctfdpy.models.hints import (
    CreateHintPayload,
    Hint,
    HintType,
    LockedHint,
    UnlockedHint,
    UpdateHintPayload,
)
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


locked_hint_list_adapter = TypeAdapter(list[LockedHint])

# TODO: Optimize TypeAdapters using discriminators
hint_adapter = TypeAdapter(Hint | UnlockedHint | LockedHint)


class HintsAPI:
    """
    Interface for interacting with the `/api/v1/hints` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    @admin_only
    def list(
        self,
        *,
        type: HintType | None = None,
        challenge_id: int | None = None,
        content: str | None = None,
        cost: int | None = None,
        q: str | None = None,
        field: Literal["type", "content"] | None = None,
    ) -> list[LockedHint]:
        """
        !!! note "This method is only available to admins"

        !!! warning "This method returns limited information about hints"

        List all hints with optional filtering.

        Parameters
        ----------
        type: HintType | None
            The type of hint to filter by, defaults to None
        challenge_id: int | None
            The challenge ID to filter by, defaults to None
        content: str | None
            The content of the hint to filter by, defaults to None
        cost: int | None
            The cost of the hint to filter by, defaults to None
        q: str | None
            The query string to search for, defaults to None
        field: Literal["type", "content"] | None
            The field to search in, defaults to None

        Returns
        -------
        list[LockedHint]
            A list of hints

        Raises
        ------
        ValueError
            If q and field are not provided together.
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        """
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if content is not None:
            params["content"] = content
        if cost is not None:
            params["cost"] = cost
        if q is not None:
            params["q"] = q
            params["field"] = field

        return self._client.request(
            "GET",
            "/api/v1/hints",
            params=params,
            response_model=locked_hint_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_list(
        self,
        *,
        type: HintType | None = None,
        challenge_id: int | None = None,
        content: str | None = None,
        cost: int | None = None,
        q: str | None = None,
        field: Literal["type", "content"] | None = None,
    ) -> list[LockedHint]:
        """
        !!! note "This method is only available to admins"

        !!! warning "This method returns limited information about hints"

        List all hints with optional filtering.

        Parameters
        ----------
        type: HintType | None
            The type of hint to filter by, defaults to None
        challenge_id: int | None
            The challenge ID to filter by, defaults to None
        content: str | None
            The content of the hint to filter by, defaults to None
        cost: int | None
            The cost of the hint to filter by, defaults to None
        q: str | None
            The query string to search for, defaults to None
        field: Literal["type", "content"] | None
            The field to search in, defaults to None

        Returns
        -------
        list[LockedHint]
            A list of hints

        Raises
        ------
        ValueError
            If q and field are not provided together.
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        """
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if content is not None:
            params["content"] = content
        if cost is not None:
            params["cost"] = cost
        if q is not None:
            params["q"] = q
            params["field"] = field

        return await self._client.arequest(
            "GET",
            "/api/v1/hints",
            params=params,
            response_model=locked_hint_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @overload
    def create(self, *, payload: CreateHintPayload) -> Hint: ...

    @overload
    async def async_create(self, *, payload: CreateHintPayload) -> Hint: ...

    @overload
    def create(
        self,
        *,
        challenge_id: int,
        content: str,
        cost: int,
        type: HintType = HintType.STANDARD,
        requirements: dict[str, str] | None = None,
    ) -> Hint: ...

    @overload
    async def async_create(
        self,
        *,
        challenge_id: int,
        content: str,
        cost: int,
        type: HintType = HintType.STANDARD,
        requirements: dict[str, str] | None = None,
    ) -> Hint: ...

    @admin_only
    def create(
        self,
        *,
        payload: CreateHintPayload = MISSING,
        challenge_id: int | None = None,
        content: str | None = None,
        cost: int | None = None,
        type: HintType = HintType.STANDARD,
        requirements: dict[str, str] | None = None,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Create a new hint.

        Parameters
        ----------
        payload: CreateHintPayload
            The payload to create the hint with. If this is provided, no other parameters should be provided.
        challenge_id: int | None
            The challenge ID to create the hint for, defaults to None
        content: str | None
            The content of the hint, defaults to None
        cost: int | None
            The cost of the hint, defaults to None
        type: HintType, default=HintType.STANDARD
            The type of hint, defaults to HintType.STANDARD
        requirements: dict[str, str] | None
            The requirements to unlock the hint, defaults to None

        Returns
        -------
        Hint
            The created hint

        Raises
        ------
        ModelValidationError
            If the provided payload is invalid
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        """
        if payload is MISSING:
            try:
                payload = CreateHintPayload(
                    challenge_id=challenge_id,
                    content=content,
                    cost=cost,
                    type=type,
                    requirements=requirements,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "POST",
            "/api/v1/hints",
            json=payload.dump_json(),
            response_model=Hint,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_create(
        self,
        *,
        payload: CreateHintPayload = MISSING,
        challenge_id: int | None = None,
        content: str | None = None,
        cost: int | None = None,
        type: HintType = HintType.STANDARD,
        requirements: dict[str, str] | None = None,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Create a new hint.

        Parameters
        ----------
        payload: CreateHintPayload
            The payload to create the hint with. If this is provided, no other parameters should be provided.
        challenge_id: int | None
            The challenge ID to create the hint for, defaults to None
        content: str | None
            The content of the hint, defaults to None
        cost: int | None
            The cost of the hint, defaults to None
        type: HintType, default=HintType.STANDARD
            The type of hint, defaults to HintType.STANDARD
        requirements: dict[str, str] | None
            The requirements to unlock the hint, defaults to None

        Returns
        -------
        Hint
            The created hint

        Raises
        ------
        ModelValidationError
            If the provided payload is invalid
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        """
        if payload is MISSING:
            try:
                payload = CreateHintPayload(
                    challenge_id=challenge_id,
                    content=content,
                    cost=cost,
                    type=type,
                    requirements=requirements,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "POST",
            "/api/v1/hints",
            json=payload.dump_json(),
            response_model=Hint,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get(self, hint_id: int) -> Hint | LockedHint | UnlockedHint:
        """
        !!! note "This method is only available to admins"

        Get a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to get

        Returns
        -------
        Hint | LockedHint | UnlockedHint
            The hint

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        return self._client.request(
            "GET",
            f"/api/v1/hints/{hint_id}",
            response_model=hint_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_get(self, hint_id: int) -> Hint | LockedHint | UnlockedHint:
        """
        !!! note "This method is only available to admins"

        Get a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to get

        Returns
        -------
        Hint | LockedHint | UnlockedHint
            The hint

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        return await self._client.arequest(
            "GET",
            f"/api/v1/hints/{hint_id}",
            response_model=hint_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @overload
    def update(self, hint_id: int, *, payload: UpdateHintPayload) -> Hint: ...

    @overload
    async def async_update(
        self, hint_id: int, *, payload: UpdateHintPayload
    ) -> Hint: ...

    @overload
    def update(
        self,
        hint_id: int,
        *,
        challenge_id: int = MISSING,
        content: str = MISSING,
        cost: int = MISSING,
        type: HintType = MISSING,
        requirements: dict[str, str] | None = None,
    ) -> Hint: ...

    @overload
    async def async_update(
        self,
        hint_id: int,
        *,
        challenge_id: int = MISSING,
        content: str = MISSING,
        cost: int = MISSING,
        type: HintType = MISSING,
        requirements: dict[str, str] | None = None,
    ) -> Hint: ...

    @admin_only
    def update(
        self,
        hint_id: int,
        *,
        payload: UpdateHintPayload = MISSING,
        **kwargs,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Update a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to update
        payload: UpdateHintPayload
            The payload to update the hint with. If this is provided, no other parameters should be provided.
        challenge_id: int
            The challenge ID to update the hint for, defaults to None
        content: str
            The content of the hint, defaults to None
        cost: int
            The cost of the hint, defaults to None
        type: HintType
            The type of hint, defaults to None
        requirements: dict[str, str] | None
            The requirements to unlock the hint, defaults to None

        Returns
        -------
        Hint
            The updated hint

        Raises
        ------
        ModelValidationError
            If the provided payload is invalid
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        if payload is MISSING:
            try:
                payload = UpdateHintPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "PATCH",
            f"/api/v1/hints/{hint_id}",
            json=payload.dump_json(),
            response_model=Hint,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_update(
        self,
        hint_id: int,
        *,
        payload: UpdateHintPayload = MISSING,
        **kwargs,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Update a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to update
        payload: UpdateHintPayload
            The payload to update the hint with. If this is provided, no other parameters should be provided.
        challenge_id: int
            The challenge ID to update the hint for, defaults to None
        content: str
            The content of the hint, defaults to None
        cost: int
            The cost of the hint, defaults to None
        type: HintType
            The type of hint, defaults to None
        requirements: dict[str, str] | None
            The requirements to unlock the hint, defaults to None

        Returns
        -------
        Hint
            The updated hint

        Raises
        ------
        ModelValidationError
            If the provided payload is invalid
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        if payload is MISSING:
            try:
                payload = UpdateHintPayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "PATCH",
            f"/api/v1/hints/{hint_id}",
            json=payload.dump_json(),
            response_model=Hint,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def delete(self, hint_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Delete a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to delete

        Returns
        -------
        bool
            `#!python True` if the hint was successfully deleted.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        return self._client.request(
            "DELETE",
            f"/api/v1/hints/{hint_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, hint_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Delete a hint by its ID.

        Parameters
        ----------
        hint_id: int
            The ID of the hint to delete

        Returns
        -------
        bool
            `#!python True` if the hint was successfully deleted.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The hint with the provided ID does not exist.
        """
        return await self._client.arequest(
            "DELETE",
            f"/api/v1/hints/{hint_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
