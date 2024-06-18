from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Any, Literal

from pydantic import AliasChoices, Field, model_serializer, model_validator

from ctfdpy.models.model import CreatePayloadModel, ResponseModel
from ctfdpy.types.files import CreateFilePayloadDict, MultipartFileTypes


class FileType(StrEnum):
    STANDARD = "standard"
    CHALLENGE = "challenge"
    PAGE = "page"


class BaseFile(ResponseModel):
    """
    A base file model. Not meant to be instantiated directly.

    Parameters
    ----------
    id : int
        The ID of the file
    type : FileType
        The type of the file
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file

    Attributes
    ----------
    id : int
        The ID of the file
    type : FileType
        The type of the file
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    """

    id: int = Field(frozen=True, exclude=True)
    type: FileType
    location: str
    sha1sum: str


class StandardFile(BaseFile):
    """
    Represents a standard file in CTFd.

    This model cannot be edited since there is no endpoint to update files in CTFd.

    Parameters
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.STANDARD]
        The type of the file. This should always be `"standard"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file

    Attributes
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.STANDARD]
        The type of the file. This should always be `"standard"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    """

    type: Literal[FileType.STANDARD]


class ChallengeFile(BaseFile):
    """
    Represents a challenge file in CTFd.

    This model cannot be edited since there is no endpoint to update files in CTFd.

    Parameters
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.CHALLENGE]
        The type of the file. This should always be `"challenge"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    challenge_id : int
        The ID of the challenge associated with the file
    challenge : int
        Alias for `challenge_id`

    Attributes
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.CHALLENGE]
        The type of the file. This should always be `"challenge"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    challenge_id : int
        The ID of the challenge associated with the file
    """

    type: Literal[FileType.CHALLENGE]
    challenge_id: int = Field(
        validation_alias=AliasChoices("challenge_id", "challenge")
    )


class PageFile(BaseFile):
    """
    Represents a page file in CTFd.

    This model cannot be edited since there is no endpoint to update files in CTFd.

    Parameters
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.PAGE]
        The type of the file. This should always be `"page"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    page_id : int
        The ID of the page associated with the file
    page : int
        Alias for `page_id`

    Attributes
    ----------
    id : int
        The ID of the file
    type : Literal[FileType.PAGE]
        The type of the file. This should always be `"page"`
    location : str
        The location of the file
    sha1sum : str
        The SHA-1 checksum of the file
    page_id : int
        The ID of the page associated with the file
    """

    type: Literal[FileType.PAGE]
    page_id: int = Field(validation_alias=AliasChoices("page_id", "page"))


class CreateFilePayload(CreatePayloadModel, arbitrary_types_allowed=True):
    """
    Payload to create files in CTFd

    Parameters
    ----------
    files : list[MultipartFileTypes]
        The files to create
    type : FileType
        The type of the files
    challenge_id : int | None
        The ID of the challenge associated with the files. Required if `type` is `"challenge"`
    challenge : int | None
        Alias for `challenge_id`
    page_id : int | None
        The ID of the page associated with the files. Required if `type` is `"page"`
    page : int | None
        Alias for `page_id`
    location : str | None
        The location to upload the files to. Cannot be specified if multiple files are provided

    Attributes
    ----------
    files : list[MultipartFileTypes]
        The files to create
    type : FileType
        The type of the files
    challenge_id : int | None
        The ID of the challenge associated with the files. Required if `type` is `"challenge"`
    page_id : int | None
        The ID of the page associated with the files. Required if `type` is `"page"`
    location : str | None
        The location to upload the files to. Cannot be specified if multiple files are provided
    """

    files: list[MultipartFileTypes]  # this might be slow...
    type: FileType = FileType.STANDARD
    challenge_id: int | None = Field(
        None, validation_alias=AliasChoices("challenge_id", "challenge")
    )
    page_id: int | None = Field(None, validate_alias=AliasChoices("page_id", "page"))
    location: str | None = Field(None)

    @model_serializer()
    def _model_ser(self) -> CreateFilePayloadDict:
        data = {"type": self.type}
        if self.challenge_id is not None:
            data["challenge_id"] = self.challenge_id
        if self.page_id is not None:
            data["page_id"] = self.page_id
        if self.location is not None:
            data["location"] = self.location

        return {"files": [("file", file) for file in self.files], "data": data}

    if TYPE_CHECKING:
        # Ensure type checkers see the correct return type
        def model_dump(
            self,
            *,
            mode: Literal["json", "python"] | str = "python",
            include: Any = None,
            exclude: Any = None,
            by_alias: bool = False,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
        ) -> CreateFilePayloadDict: ...

    @model_validator(mode="after")
    def check_file_type(self) -> CreateFilePayload:
        match self.type:
            case FileType.STANDARD:
                if self.challenge_id is not None or self.page_id is not None:
                    raise ValueError(
                        "Challenge ID and page ID must be None for standard files"
                    )
            case FileType.CHALLENGE:
                if self.challenge_id is None:
                    raise ValueError(
                        "Challenge ID must be provided for challenge files"
                    )
                if self.page_id is not None:
                    raise ValueError("Page ID must be None for challenge files")
            case FileType.PAGE:
                if self.page_id is None:
                    raise ValueError("Page ID must be provided for page files")
                if self.challenge_id is not None:
                    raise ValueError("Challenge ID must be None for page files")
        return self

    @model_validator(mode="after")
    def check_file_count(self) -> CreateFilePayload:
        if len(self.files) == 0:
            raise ValueError("At least one file must be provided")
        elif len(self.files) > 1 and self.location is not None:
            raise ValueError(
                "Location cannot be specified when multiple files are provided"
            )
        return self
