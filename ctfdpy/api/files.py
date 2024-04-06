from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Literal, overload

from pydantic import Field, TypeAdapter, ValidationError

from ctfdpy.api.api import API
from ctfdpy.exceptions import CTFdpyModelValidationError
from ctfdpy.models.files import (
    ChallengeFile,
    CreateFilePayload,
    FileType,
    MultipartFileTypes,
    PageFile,
    StandardFile,
)
from ctfdpy.utils import admin_only

file_adapter = TypeAdapter(
    Annotated[StandardFile | ChallengeFile | PageFile, Field(..., discriminator="type")]
)


class FilesAPI(API):
    """
    Class for interacting with the `/api/v1/files` endpoint

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

    Methods
    -------
    list(type: FileType | None = None, location: str | None = None, q: str | None = None, field: Literal["type", "location"] | None = None) -> list[File]
        Method to list all files with optional filtering
    create(payload: CreateFilePayload | None = None, files: list[MultipartFileTypes] | None = None, file_paths: list[str | os.PathLike] | None = None, type: FileType | None = None, challenge_id: int | None = None, challenge: int | None = None, page_id: int | None = None, page: int | None = None, location: str | None = None) -> list[File]
        Method to create files
    get(file_id: int) -> File
        Method to get a file by ID
    delete(file_id: int) -> bool
        Method to delete a file by ID
    """

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

        Method to list all files with optional filtering

        Parameters
        ----------
        type : FileType | None
            The type of the file to filter by, by default None
        location : str | None
            The location of the file to filter by, by default None
        q : str | None
            The query string to search for, by default None
        field : Literal["type", "location"] | None
            The field to search in, by default None

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            A list of files

        Raises
        ------
        ValueError
            If `q` is provided without `field` or vice versa
        CTFdpyBadRequestException
            An error occurred processing the provided or stored data
        CTFdpyUnauthorizedException
            The client is not authorized to access the endpoint

        Examples
        --------
        Get all files
        ```python
        files = client.files.list()
        ```

        Get all challenge files
        ```python
        files = client.files.list(type=FileType.CHALLENGE)
        ```
        """
        # Check that q and field are both provided or neither are provided
        if q is None != field is None:
            raise ValueError("Both q and field must be provided")

        params = {}
        if type is not None:
            params["type"] = type
        if location is not None:
            params["location"] = location
        if q is not None:
            params["q"] = q
            params["field"] = field

        result = self._get("/api/v1/files", params=params)

        return [file_adapter.validate_python(file) for file in result["data"]]

    @overload
    def create(
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

    @admin_only
    def create(
        self,
        *,
        payload: CreateFilePayload | None = None,
        files: list[MultipartFileTypes] | None = None,
        file_paths: list[str | os.PathLike] | None = None,
        type: FileType | None = None,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[StandardFile | ChallengeFile | PageFile]:
        """
        !!! note "This method is only available to admins"

        Method to create files

        Parameters
        ----------
        payload : CreateFilePayload
            The payload to create the files with. If this is provided, no other parameters should be provided
        files : list[MultipartFileTypes]
            The files to upload. This can either be a `#!python FileContent` type or a tuple of length between 2 and 4
            in the format `(filename, file, content_type, headers)`.
        file_paths : list[str | os.PathLike] | None
            The paths to the files to upload, by default None
        type : FileType | None
            The type of the files, by default None
        challenge_id : int | None
            The ID of the challenge associated with the files, by default None
        challenge : int | None
            Alias for `challenge_id`, by default None
        page_id : int | None
            The ID of the page associated with the files, by default None
        page : int | None
            Alias for `page_id`, by default None
        location : str | None
            The location to upload the files to, by default None

        Returns
        -------
        list[StandardFile | ChallengeFile | PageFile]
            A list of files created

        Raises
        ------
        ValueError
            If no files are provided
        FileNotFoundError
            If a provided file path does not exist
        CTFdpyBadRequestException
            An error occurred processing the provided or stored data
        CTFdpyUnauthorizedException
            The client is not authorized to access the endpoint
        CTFdpyModelValidationError
            The provided payload is invalid

        Examples
        --------
        Create a file for a challenge with ID of `1`
        ```python
        # Using `CreateFilePayload`

        payload = CreateFilePayload(
            files=[("file.txt", open("file.txt", "rb"))],
            type=FileType.CHALLENGE,
            challenge_id=1
        )
        file = client.files.create(payload=payload)

        # Or using file content

        file = client.files.create(
            files=[("file.txt", open("file.txt", "rb"))],
            type=FileType.CHALLENGE,
            challenge_id=1
        )

        # Or using file paths

        file = client.files.create(
            file_paths=[Path("file.txt")],
            type=FileType.CHALLENGE,
            challenge_id=1
        )

        ```
        """
        if payload is None:
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
                raise CTFdpyModelValidationError(e.errors())

        result = self._post(
            "/api/v1/files",
            headers={"Content-Type": "multipart/form-data"},
            **payload.to_payload(),  # We need to unpack the payload
        )

        return [file_adapter.validate_python(file) for file in result["data"]]

    @admin_only
    def get(self, file_id: int) -> StandardFile | ChallengeFile | PageFile:
        """
        !!! note "This method is only available to admins"

        Method to get a file by ID

        Parameters
        ----------
        file_id : int
            The ID of the file to get

        Returns
        -------
        StandardFile | ChallengeFile | PageFile
            The file

        Raises
        ------
        CTFdpyNotFoundException
            The file does not exist
        CTFdpyUnauthorizedException
            The client is not authorized to access the endpoint

        Examples
        --------
        Get a file
        ```python
        file = client.files.get(1)
        ```
        """
        result = self._get(f"/api/v1/files/{file_id}")

        return file_adapter.validate_python(result["data"])

    @admin_only
    def delete(self, file_id: int) -> bool:
        """
        !!! note "This method is only available to admins"

        Method to delete a file by ID

        Parameters
        ----------
        file_id : int
            The ID of the file to delete

        Returns
        -------
        bool
            Whether the file was deleted

        Raises
        ------
        CTFdpyNotFoundException
            The file does not exist
        CTFdpyUnauthorizedException
            The client is not authorized to access the endpoint

        Examples
        --------
        Delete a file
        ```python
        client.files.delete(1)
        ```
        """
        result = self._delete(f"/api/v1/files/{file_id}")

        return result["success"]
