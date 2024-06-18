from typing import BinaryIO, Literal, Mapping

from typing_extensions import TypedDict

# From https://github.com/encode/httpx/blob/392dbe45f086d0877bd288c5d68abf860653b680/httpx/_types.py#L96-L106
FileContent = BinaryIO | bytes | str
MultipartFileTypes = (
    # file (or bytes)
    FileContent
    |
    # (filename, file (or bytes))
    tuple[str | None, FileContent]
    |
    # (filename, file (or bytes), content_type)
    tuple[str | None, FileContent, str | None]
    |
    # (filename, file (or bytes), content_type, headers)
    tuple[str | None, FileContent, str | None, Mapping[str, str]]
)


class CreateFilePayloadDict(TypedDict):
    files: list[tuple[Literal["file"], MultipartFileTypes]]
    data: dict[str, str | int]
