from __future__ import annotations

from pathlib import Path
from typing import IO, Literal, overload

from pydantic import ValidationError

from ctfdpy.api.api import API
from ctfdpy.exceptions import CTFdpyModelValidationError
from ctfdpy.models.files import (
    CreateFilePayload,
    File,
    FileContent,
    FileType,
    MultipartFileTypes,
)
from ctfdpy.utils import admin_only


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
    list_files(type: FileType | None = None, location: str | None = None, q: str | None = None, field: Literal["type", "location"] | None = None) -> list[File]
        Lists all files
    create_files(payload_or_files: CreateFilePayload | list[MultipartFileTypes] | None = None, /, file_paths: list[Path] | None = None, *, type: FileType | None = None, challenge_id: int | None = None, challenge: int | None = None, page_id: int | None = None, page: int | None = None, location: str | None = None) -> list[File]
        Creates files
    get_file(file_id: int) -> File
        Gets a file by ID
    delete_file(file_id: int) -> bool
        Deletes a file by ID
    """

    @admin_only
    def list_files(
        self,
        type: FileType | None = None,
        location: str | None = None,
        q: str | None = None,
        field: Literal["type", "location"] | None = None,
    ) -> list[File]:
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
        list[File]
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
        files = client.files.list_files()
        ```

        Get all challenge files
        ```python
        files = client.files.list_files(type=FileType.CHALLENGE)
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

        return [File.model_validate(file) for file in result["data"]]

    @overload
    def create_files(self, payload: CreateFilePayload, /) -> list[File]: ...

    @overload
    def create_files(
        self,
        files: list[MultipartFileTypes],
        /,
        file_paths: list[Path],
        *,
        type: FileType,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[File]: ...

    @admin_only
    def create_files(
        self,
        payload_or_files: CreateFilePayload | list[MultipartFileTypes] | None = None,
        /,
        file_paths: list[Path] | None = None,
        *,
        type: FileType | None = None,
        challenge_id: int | None = None,
        challenge: int | None = None,
        page_id: int | None = None,
        page: int | None = None,
        location: str | None = None,
    ) -> list[File]:
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
        file_paths : list[Path], optional
            The paths to the files to upload, by default None
        type : FileType, optional
            The type of the files, by default None
        challenge_id : int, optional
            The ID of the challenge associated with the files, by default None
        challenge : int, optional
            Alias for `challenge_id`, by default None
        page_id : int, optional
            The ID of the page associated with the files, by default None
        page : int, optional
            Alias for `page_id`, by default None
        location : str, optional
            The location to upload the files to, by default None

        Returns
        -------
        list[File]
            A list of files created

        Raises
        ------
        ValueError
            If no files are provided
        CTFdpyBadRequestException
            An error occurred processing the provided or stored data
        CTFdpyUnauthorizedException
            The client is not authorized to access the endpoint
        CTFdpyModelValidationError
            The provided payload is invalid
        """
        if isinstance(payload_or_files, CreateFilePayload):
            payload = payload_or_files
        else:
            files = payload_or_files or []
            files.extend(
                (file_path.name, file_path.open("rb")) for file_path in file_paths
            )

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

        result = self._post("/api/v1/files", json=payload.model_dump(model="json"))

        return [File.model_validate(file) for file in result["data"]]

    @admin_only
    def get_file(self, file_id: int) -> File:
        """
        !!! note "This method is only available to admins"

        Method to get a file by ID

        Parameters
        ----------
        file_id : int
            The ID of the file to get

        Returns
        -------
        File
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
        file = client.files.get_file(1)
        ```
        """
        result = self._get(f"/api/v1/files/{file_id}")

        return File.model_validate(result["data"])

    @admin_only
    def delete_file(self, file_id: int) -> bool:
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
        client.files.delete_file(1)
        ```
        """
        result = self._delete(f"/api/v1/files/{file_id}")

        return result["success"]
