from __future__ import annotations

from typing import Literal, overload

from pydantic import Field, TypeAdapter, ValidationError

from ctfdpy.api.api import API
from ctfdpy.exceptions import CTFdpyModelValidationError
from ctfdpy.models.hints import (
    CreateHintPayload,
    Hint,
    HintType,
    LockedHint,
    UnlockedHint,
    UpdateHintPayload,
)
from ctfdpy.utils import admin_only

hint_adapter = TypeAdapter(Hint | UnlockedHint | LockedHint)


class HintsAPI(API):
    """
    Class for interacting with the `/api/v1/hints` endpoint

    Parameters
    ----------
    client : ctfdy.Client
        The client to use for requests

    Attributes
    ----------
    client : ctfdpy.Client
        The client used for requests
    url : str
        The URL of the CTFd instance
    session : httpx.HttpClient
        The HTTP session used for requests
    """

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

        !!! warning "This method returns limited information for hints"

        Method to list all hints with optional filtering

        Parameters
        ----------
        type : HintType | None
            The type of the hint
        challenge_id : int | None
            The ID of the challenge associated with the hint
        content : str | None
            The content of the hint
        cost : int | None
            The cost of the hint
        q : str | None
            The query string to search for
        field : Literal["type", "content"] | None
            The field to search in

        Returns
        -------
        list[LockedHint]
            The list of hints
        """
        # Check that q and field are both provided or neither are provided
        if q is None != field is None:
            raise ValueError(
                "Both q and field must be provided or neither must be provided"
            )

        params = {}
        if type is not None:
            params["type"] = type
        if challenge_id is not None:
            params["challenge_id"] = challenge_id
        if content is not None:
            params["content"] = content
        if cost is not None:
            params["cost"] = cost
        if q is not None:
            params["q"] = q
            params["field"] = field

        result = self._get("/api/v1/hints", params=params)

        return [LockedHint.model_validate(hint) for hint in result["data"]]

    @overload
    def create(self, *, payload: CreateHintPayload) -> Hint: ...

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

    @admin_only
    def create(
        self,
        *,
        payload: CreateHintPayload | None = None,
        challenge_id: int | None = None,
        content: str | None = None,
        cost: int | None = None,
        type: HintType = HintType.STANDARD,
        requirements: dict[str, str] | None = None,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Method to create a hint

        Parameters
        ----------
        payload : CreateHintPayload
            The payload for creating a hint. If this is provided, no other parameters should be provided
        challenge_id : int
            The ID of the challenge associated with the hint
        content : str
            The content of the hint
        cost : int
            The cost of the hint
        type : HintType
            The type of the hint
        requirements : dict[str, str]
            The requirements of the hint

        Returns
        -------
        Hint
            The created hint
        """
        if payload is None:
            try:
                payload = CreateHintPayload(
                    challenge_id=challenge_id,
                    content=content,
                    cost=cost,
                    type=type,
                    requirements=requirements,
                )
            except ValidationError as e:
                raise CTFdpyModelValidationError(e.errors())

        result = self._post("/api/v1/hints", json=payload.to_payload())

        return Hint.model_validate(result)

    @admin_only
    def get(self, hint_id: int) -> Hint | LockedHint | UnlockedHint:
        """
        !!! note "This method is only available to admins"

        Gets a hint by ID

        Parameters
        ----------
        hint_id : int
            The ID of the hint

        Returns
        -------
        LockedHint
            The hint
        """
        result = self._get(f"/api/v1/hints/{hint_id}")

        return hint_adapter.validate_python(result["data"])

    @overload
    def update(self, hint_id: int, *, payload: UpdateHintPayload) -> Hint: ...

    @overload
    def update(
        self,
        hint_id: int,
        *,
        challenge_id: int,
        content: str,
        cost: int,
        type: HintType,
        requirements: dict[str, str] | None,
    ) -> Hint: ...

    @admin_only
    def update(
        self,
        hint_id: int,
        *,
        payload: UpdateHintPayload | None = None,
        **kwargs,
    ) -> Hint:
        """
        !!! note "This method is only available to admins"

        Method to update a hint

        Parameters
        ----------
        hint_id : int
            The ID of the hint
        payload : UpdateHintPayload
            The payload for updating a hint. If this is provided, no other parameters should be provided
        challenge_id : int
            The ID of the challenge associated with the hint
        content : str
            The content of the hint
        cost : int
            The cost of the hint
        type : HintType
            The type of the hint
        requirements : dict[str, str] | None
            The requirements of the hint

        Returns
        -------
        Hint
            The updated hint
        """
        if payload is None:
            try:
                payload = UpdateHintPayload(**kwargs)
            except ValidationError as e:
                raise CTFdpyModelValidationError(e.errors())

        result = self._patch(f"/api/v1/hints/{hint_id}", json=payload.to_payload())

        return Hint.model_validate(result)

    @admin_only
    def delete(self, hint_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Method to delete a hint

        Parameters
        ----------
        hint_id : int
            The ID of the hint

        Returns
        -------
        bool
            Whether the hint was deleted successfully
        """
        result = self._delete(f"/api/v1/hints/{hint_id}")

        return result["success"]
