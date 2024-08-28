from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Literal, overload

from pydantic import Field, TypeAdapter, ValidationError

from ctfdpy.exceptions import (
    BadRequest,
    Forbidden,
    ModelValidationError,
    NotFound,
    Unauthorized,
)
from ctfdpy.models.files import (
    BaseFile,
    ChallengeFile,
    CreateFilePayload,
    FileType,
    MultipartFileTypes,
    PageFile,
    StandardFile,
)
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient

list_create_file_adapter = TypeAdapter(list[BaseFile])

list_file_adapter = TypeAdapter(
    list[
        Annotated[
            StandardFile | ChallengeFile | PageFile, Field(..., discriminator="type")
        ]
    ]
)

file_adapter = TypeAdapter(
    Annotated[StandardFile | ChallengeFile | PageFile, Field(..., discriminator="type")]
)


class FilesAPI:
    """
    Interface for interacting with the `/api/v1/files` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    @admin_only
    def list(
        self,
        *,
        type: FileType | None = None,
        location: str | None = None,
        q: str | None = None,
        field: Literal["type", "location"] | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]:
        """
        !!! note "This method is only available to admins"

        List all files with optional filtering.

        Parameters
        ----------
        type: FileType | None
            The type of file to filter by, defaults to None.
        location: str | None
            The location of the file to filter by, defaults to None.
        q: str | None
            The query string to search for, defaults to None.
        field: Literal["type", "location"] | None
            The field to search in, defaults to None.

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            A list of files that match the query.

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

        Examples
        --------
        Get all files:

        ```python
        files = ctfd.files.list()
        ```

        Get all challenge files:

        ```python
        files = ctfd.files.list(type=FileType.CHALLENGE)
        ```
        """
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if location is not None:
            params["location"] = location
        if q is not None:
            params["q"] = q
            params["field"] = field

        return self._client.request(
            "GET",
            "/api/v1/files",
            params=params,
            response_model=list_file_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_list(
        self,
        *,
        type: FileType | None = None,
        location: str | None = None,
        q: str | None = None,
        field: Literal["type", "location"] | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]:
        """
        !!! note "This method is only available to admins"

        List all files with optional filtering.

        Parameters
        ----------
        type: FileType | None
            The type of file to filter by, defaults to None.
        location: str | None
            The location of the file to filter by, defaults to None.
        q: str | None
            The query string to search for, defaults to None.
        field: Literal["type", "location"] | None
            The field to search in, defaults to None.

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            A list of files that match the query.

        Raises
        ------
        ValueError
            If q and field are both provided or both not provided.
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.

        Examples
        --------
        Get all files:

        ```python
        files = await ctfd.files.async_list()
        ```

        Get all challenge files:

        ```python
        files = await ctfd.files.async_list(type=FileType.CHALLENGE)
        ```
        """
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if type is not None:
            params["type"] = type.value
        if location is not None:
            params["location"] = location
        if q is not None:
            params["q"] = q
            params["field"] = field

        return await self._client.arequest(
            "GET",
            "/api/v1/files",
            params=params,
            response_model=list_file_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @overload
    def create(
        self, *, payload: CreateFilePayload
    ) -> list[StandardFile | ChallengeFile | PageFile]: ...

    @overload
    async def async_create(
        self, *, payload: CreateFilePayload
    ) -> list[StandardFile | ChallengeFile | PageFile]: ...

    @overload
    def create(
        self,
        *,
        files: list[MultipartFileTypes] | None = None,
        file_paths: list[str | os.PathLike] | None = None,
        type: FileType = FileType.STANDARD,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]: ...

    @overload
    async def async_create(
        self,
        *,
        files: list[MultipartFileTypes] | None = None,
        file_paths: list[str | os.PathLike] | None = None,
        type: FileType = FileType.STANDARD,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]: ...

    @admin_only
    def create(
        self,
        *,
        payload: CreateFilePayload = MISSING,
        files: list[MultipartFileTypes] | None = None,
        file_paths: list[str | os.PathLike] | None = None,
        type: FileType = FileType.STANDARD,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]:
        """
        !!! note "This method is only available to admins"

        Create a new file.

        Parameters
        ----------
        payload: CreateFilePayload
            The payload to create the file with. If this is provided, no other parameter should be provided.
        files: list[MultipartFileTypes] | None
            The files to upload. This can either be a `#!python FileContent` or a tuple of length between 2 and 4
            in the format `(filename, file, content_type, headers)`. Defaults to None.
        file_paths: list[str | os.PathLike] | None
            The paths to the files to upload. Defaults to None.
        type: FileType | None
            The type of the file, defaults to None.
        challenge_id: int | None
            The ID of the challenge to associate the file with, defaults to None.
        page_id: int | None
            The ID of the page to associate the file with, defaults to None.
        location: str | None
            The location on the server to upload the files to, defaults to None.

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            The files that were created.

        Raises
        ------
        ValueError
            If no files are provided.
        FileNotFoundError
            If a file path does not exist.
        ModelValidationError
            If the payload is invalid.
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.

        Examples
        --------
        Create a file for a challenge:

        ```python
        files = ctfd.files.create(
            files=[("filename.txt", open("/path/to/file.txt", "rb"))],
            type=FileType.CHALLENGE,
            challenge_id=1,
        )
        ```
        """
        if payload is MISSING:
            files = files or []

            if file_paths is not None:
                for file_path in file_paths:
                    file_path = Path(file_path)
                    if not file_path.exists():
                        raise FileNotFoundError(f"File not found: {file_path}")
                    files.append((file_path.name, file_path.open("rb")))

            if len(files) == 0:
                raise ValueError("At least one file must be provided")

            try:
                payload = CreateFilePayload(
                    files=files,
                    type=type,
                    challenge_id=challenge_id or challenge,
                    page_id=page_id or page,
                    location=location,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "POST",
            "/api/v1/files",
            data=payload.data_payload,
            files=payload.files_payload,  # we can't use payload.dump_json() here, see https://github.com/pydantic/pydantic/issues/8907
            headers={"Content-Type": "multipart/form-data"},
            response_model=list_create_file_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_create(
        self,
        *,
        payload: CreateFilePayload = MISSING,
        files: list[MultipartFileTypes] | None = None,
        file_paths: list[str | os.PathLike] | None = None,
        type: FileType = FileType.STANDARD,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]:
        """
        !!! note "This method is only available to admins"

        Create a new file.

        Parameters
        ----------
        payload: CreateFilePayload
            The payload to create the file with. If this is provided, no other parameter should be provided.
        files: list[MultipartFileTypes] | None
            The files to upload. This can either be a `#!python FileContent` or a tuple of length between 2 and 4
            in the format `(filename, file, content_type, headers)`. Defaults to None.
        file_paths: list[str | os.PathLike] | None
            The paths to the files to upload. Defaults to None.
        type: FileType | None
            The type of the file, defaults to None.
        challenge_id: int | None
            The ID of the challenge to associate the file with, defaults to None.
        page_id: int | None
            The ID of the page to associate the file with, defaults to None.
        location: str | None
            The location on the server to upload the files to, defaults to None.

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            The files that were created.

        Raises
        ------
        ValueError
            If no files are provided.
        FileNotFoundError
            If a file path does not exist.
        ModelValidationError
            If the payload is invalid.
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.

        Examples
        --------
        Create a file for a challenge:

        ```python
        files = await ctfd.files.async_create(
            files=[("filename.txt", open("/path/to/file.txt", "rb"))],
            type=FileType.CHALLENGE,
            challenge_id=1,
        )
        ```
        """
        if payload is MISSING:
            files = files or []

            if file_paths is not None:
                for file_path in file_paths:
                    file_path = Path(file_path)
                    if not file_path.exists():
                        raise FileNotFoundError(f"File not found: {file_path}")
                    files.append((file_path.name, file_path.open("rb")))

            if len(files) == 0:
                raise ValueError("At least one file must be provided")

            try:
                payload = CreateFilePayload(
                    files=files,
                    type=type,
                    challenge_id=challenge_id or challenge,
                    page_id=page_id or page,
                    location=location,
                )
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "POST",
            "/api/v1/files",
            data=payload.data_payload,
            files=payload.files_payload,  # we can't use payload.dump_json() here, see https://github.com/pydantic/pydantic/issues/8907
            headers={"Content-Type": "multipart/form-data"},
            response_model=list_create_file_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get(self, file_id: int) -> StandardFile | ChallengeFile | PageFile:
        """
        !!! note "This method is only available to admins"

        Get a file by its ID.

        Parameters
        ----------
        file_id: int
            The ID of the file to get.

        Returns
        -------
        StandardFile | ChallengeFile | PageFile
            The file with the provided ID.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        NotFound
            The file with the provided ID does not exist.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.

        Examples
        --------
        Get a file by its ID:

        ```python
        file = ctfd.files.get(1)
        ```
        """
        return self._client.request(
            "GET",
            f"/api/v1/files/{file_id}",
            response_model=file_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_get(self, file_id: int) -> StandardFile | ChallengeFile | PageFile:
        """
        !!! note "This method is only available to admins"

        Get a file by its ID.

        Parameters
        ----------
        file_id: int
            The ID of the file to get.

        Returns
        -------
        StandardFile | ChallengeFile | PageFile
            The file with the provided ID.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        NotFound
            The file with the provided ID does not exist.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.

        Examples
        --------
        Get a file by its ID:

        ```python
        file = await ctfd.files.async_get(1)
        ```
        """
        return await self._client.arequest(
            "GET",
            f"/api/v1/files/{file_id}",
            response_model=file_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    def delete(self, file_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Delete a file by its ID.

        Parameters
        ----------
        file_id: int
            The ID of the file to delete.

        Returns
        -------
        bool
            `#!python True` if the file was successfully deleted.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The file with the provided ID does not exist.

        Examples
        --------
        Delete a file by its ID:

        ```python
        success = ctfd.files.delete(1)
        ```
        """
        return self._client.request(
            "DELETE",
            f"/api/v1/files/{file_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    @admin_only
    async def async_delete(self, file_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Delete a file by its ID.

        Parameters
        ----------
        file_id: int
            The ID of the file to delete.

        Returns
        -------
        bool
            `#!python True` if the file was successfully deleted.

        Raises
        ------
        BadRequest
            An error occurred processing the provided or stored data.
        AuthenticationRequired
            You must be logged in to access this resource.
        AdminOnly
            You must be an admin to access this resource.
        NotFound
            The file with the provided ID does not exist.

        Examples
        --------
        Delete a file by its ID:

        ```python
        success = await ctfd.files.async_delete(1)
        ```
        """
        return await self._client.arequest(
            "DELETE",
            f"/api/v1/files/{file_id}",
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )
