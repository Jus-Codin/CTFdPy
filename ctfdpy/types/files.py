from typing import Mapping, Protocol, TypedDict, runtime_checkable


# We have to do this as file objects cannot be properly type hinted for pydantic
# See https://github.com/pydantic/pydantic/issues/5443
@runtime_checkable
class SupportsReadBytes(Protocol):
    def read(self, size: int) -> bytes: ...


# From https://github.com/encode/httpx/blob/392dbe45f086d0877bd288c5d68abf860653b680/httpx/_types.py#L96-L106
FileContent = SupportsReadBytes | bytes | str
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
    type: str
    challenge_id: int | None
    page_id: int | None
    location: str | None
