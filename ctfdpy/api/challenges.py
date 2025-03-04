from __future__ import annotations

import os
from typing import TYPE_CHECKING, Annotated, Literal, Protocol, overload

from pydantic import Field, TypeAdapter, ValidationError

from ctfdpy.exceptions import (
    BadChallengeAttempt,
    BadRequest,
    Forbidden,
    ModelValidationError,
    NotFound,
    Unauthorized,
)
from ctfdpy.models.challenges import (
    AnonymousChallenge,
    ChallengeAttemptResult,
    ChallengeFileLocation,
    ChallengeListing,
    ChallengeRequirements,
    ChallengeSolve,
    ChallengeState,
    ChallengeTopic,
    ChallengeType,
    ChallengeTypeInfo,
    CreateDynamicChallengePayload,
    CreateStandardChallengePayload,
    DecayFunction,
    DynamicChallenge,
    DynamicChallengeWriteResult,
    StandardChallenge,
    StandardChallengeWriteResult,
    UpdateBaseChallengePayload,
    UpdateDynamicChallengePayload,
    UpdateStandardChallengePayload,
)
from ctfdpy.models.files import FileType
from ctfdpy.models.flags import Flag, FlagType
from ctfdpy.models.hints import Hint
from ctfdpy.models.tags import Tag
from ctfdpy.types.api import APIResponse
from ctfdpy.types.challenges import ChallengeRequirementsDict
from ctfdpy.utils import MISSING, admin_only

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class _HasChallengeID(Protocol):
    id: int


challenge_listing_adapter: TypeAdapter[list[AnonymousChallenge | ChallengeListing]] = (
    TypeAdapter(list[AnonymousChallenge | ChallengeListing])
)

flag_types = str | tuple[str] | tuple[str, FlagType] | tuple[str, FlagType, bool]

challenge_write_result_types = (
    StandardChallengeWriteResult | DynamicChallengeWriteResult
)
challenge_write_result_adapter: TypeAdapter[challenge_write_result_types] = TypeAdapter(
    Annotated[challenge_write_result_types, Field(discriminator="type")]
)

challenge_type_info_list_adapter: TypeAdapter[list[ChallengeTypeInfo]] = TypeAdapter(
    list[ChallengeTypeInfo]
)

challenge_types = StandardChallenge | DynamicChallenge | AnonymousChallenge
challenge_adapter: TypeAdapter[challenge_types] = TypeAdapter(
    Annotated[challenge_types, Field(discriminator="type")]
)

challenge_file_location_list_adapter: TypeAdapter[list[ChallengeFileLocation]] = (
    TypeAdapter(list[ChallengeFileLocation])
)

flag_list_adapter: TypeAdapter[list[Flag]] = TypeAdapter(list[Flag])

hint_list_adapter: TypeAdapter[list[Hint]] = TypeAdapter(list[Hint])

challenge_solves_list_adapter: TypeAdapter[list[ChallengeSolve]] = TypeAdapter(
    list[ChallengeSolve]
)

tag_list_adapter: TypeAdapter[list[Tag]] = TypeAdapter(list[Tag])

challenge_topic_list_adapter: TypeAdapter[list[ChallengeTopic]] = TypeAdapter(
    list[ChallengeTopic]
)


class ChallengesAPI:
    """
    Interface for interacting with the `/api/v1/challenges` CTFd API endpoint.
    """

    def __init__(self, client: APIClient):
        self._client = client

    def list(
        self,
        *,
        name: str | None = None,
        max_attempts: int | None = None,
        value: str | None = None,
        category: str | None = None,
        type: ChallengeType | None = None,
        state: ChallengeState | None = None,
        q: str | None = None,
        field: (
            Literal["name", "description", "category", "type", "state"] | None
        ) = None,
        view: Literal["admin"] | None = None,
        page: int | None = None,
    ) -> list[AnonymousChallenge, ChallengeListing]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if name is not None:
            params["name"] = name
        if max_attempts is not None:
            params["max_attempts"] = max_attempts
        if value is not None:
            params["value"] = value
        if category is not None:
            params["category"] = category
        if type is not None:
            params["type"] = type.value
        if state is not None:
            params["state"] = state.value
        if q is not None:
            params["q"] = q
            params["field"] = field
        if view is not None:
            params["view"] = view
        if page is not None:
            params["page"] = page

        return self._client.request(
            "GET",
            "/api/v1/challenges",
            params=params,
            response_model=challenge_listing_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    async def async_list(
        self,
        *,
        name: str | None = None,
        max_attempts: int | None = None,
        value: str | None = None,
        category: str | None = None,
        type: ChallengeType | None = None,
        state: ChallengeState | None = None,
        q: str | None = None,
        field: (
            Literal["name", "description", "category", "type", "state"] | None
        ) = None,
        view: Literal["admin"] | None = None,
        page: int | None = None,
    ) -> list[AnonymousChallenge, ChallengeListing]:
        # Check if q and field are both provided or both not provided
        if q is None != field is None:
            raise ValueError("q and field must be provided together")

        params = {}
        if name is not None:
            params["name"] = name
        if max_attempts is not None:
            params["max_attempts"] = max_attempts
        if value is not None:
            params["value"] = value
        if category is not None:
            params["category"] = category
        if type is not None:
            params["type"] = type.value
        if state is not None:
            params["state"] = state.value
        if q is not None:
            params["q"] = q
            params["field"] = field
        if view is not None:
            params["view"] = view
        if page is not None:
            params["page"] = page

        return await self._client.arequest(
            "GET",
            "/api/v1/challenges",
            params=params,
            response_model=challenge_listing_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    # Create with standard challenge payload and one flag
    @overload
    def create(
        self,
        *,
        payload: CreateStandardChallengePayload,
        flag: str | None = None,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        payload: CreateStandardChallengePayload,
        flag: str | None = None,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    # Create with standard challenge payload and multiple flags
    @overload
    def create(
        self,
        *,
        payload: CreateStandardChallengePayload,
        flags: list[flag_types] | None = None,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        payload: CreateStandardChallengePayload,
        flags: list[flag_types] | None = None,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    # Create with dynamic challenge payload and one flag
    @overload
    def create(
        self,
        *,
        payload: CreateDynamicChallengePayload,
        flag: str | None = None,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        payload: CreateDynamicChallengePayload,
        flag: str | None = None,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    # Create with dynamic challenge payload and multiple flags
    @overload
    def create(
        self,
        *,
        payload: CreateDynamicChallengePayload,
        flags: list[flag_types] | None = None,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        payload: CreateDynamicChallengePayload,
        flags: list[flag_types] | None = None,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    # Create standard challenge with individual parameters and one flag
    @overload
    def create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.STANDARD],
        value: int,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flag: str,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.STANDARD],
        value: int,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flag: str,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    # Create standard challenge with individual parameters and multiple flags
    @overload
    def create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.STANDARD],
        value: int,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flags: list[flag_types],
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.STANDARD],
        value: int,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flags: list[flag_types],
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> StandardChallengeWriteResult: ...

    # Create dynamic challenge with individual parameters and one flag
    @overload
    def create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.DYNAMIC],
        initial: int,
        decay: int,
        minimum: int,
        function: DecayFunction = DecayFunction.LINEAR,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flag: str,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.DYNAMIC],
        initial: int,
        decay: int,
        minimum: int,
        function: DecayFunction = DecayFunction.LINEAR,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flag: str,
        flag_type: FlagType = FlagType.STATIC,
        case_insensitive: bool = False,
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    # Create dynamic challenge with individual parameters and multiple flags
    @overload
    def create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.DYNAMIC],
        initial: int,
        decay: int,
        minimum: int,
        function: DecayFunction = DecayFunction.LINEAR,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flags: list[flag_types],
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_create(
        self,
        *,
        name: str,
        description: str,
        category: str,
        type: Literal[ChallengeType.DYNAMIC],
        initial: int,
        decay: int,
        minimum: int,
        function: DecayFunction = DecayFunction.LINEAR,
        state: ChallengeState = ChallengeState.HIDDEN,
        connection_info: str | None = None,
        next_id: int | None = None,
        max_attempts: int | None = None,
        prerequisites: list[int | _HasChallengeID] | None = None,
        anonymize: bool | None = None,
        flags: list[flag_types],
        hints: list[tuple[str, int]] | None = None,
        tags: list[str] | None = None,
        topics: list[str] | None = None,
        files: list[str | os.PathLike] | None = None,
    ) -> DynamicChallengeWriteResult: ...

    @admin_only
    def create(
        self,
        *,
        payload: (
            CreateStandardChallengePayload | CreateDynamicChallengePayload
        ) = MISSING,
        **kwargs,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult:
        flags = kwargs.pop("flags", None)

        if flags is None:
            flag = kwargs.pop("flag", None)

            if flag is not None:
                flag_type = kwargs.pop("flag_type", FlagType.STATIC)
                case_insensitive = kwargs.pop("case_insensitive", False)
                flags = [(flag, flag_type, case_insensitive)]
        else:
            _flags = []

            for flag in flags:
                if isinstance(flag, str):
                    _flags.append((flag, FlagType.STATIC, False))
                elif isinstance(flag, tuple):
                    if len(flag) == 1:
                        _flags.append((flag[0], FlagType.STATIC, False))
                    elif len(flag) == 2:
                        _flags.append((flag[0], flag[1], False))
                    elif len(flag) == 3:
                        _flags.append((flag[0], flag[1], flag[2]))
                    else:
                        raise ValueError("Invalid flag tuple")
                else:
                    raise ValueError("Invalid flag type")

            flags = _flags

        hints = kwargs.pop("hints", None)
        tags = kwargs.pop("tags", None)
        topics = kwargs.pop("topics", None)
        files = kwargs.pop("files", None)

        if payload is MISSING:
            prerequisites = kwargs.pop("prerequisites", None)
            anonymize = kwargs.pop("anonymize", None)

            requirements = None

            if prerequisites is not None:
                for i, prerequisite in enumerate(prerequisites):
                    if isinstance(prerequisite, int):
                        continue
                    elif hasattr(prerequisite, "id"):
                        prerequisites[i] = prerequisite.id
                    else:
                        raise ValueError(f"Invalid prerequisite: {prerequisite}")

                requirements = ChallengeRequirementsDict(prerequisites=prerequisites)

            if anonymize is not None:
                if requirements is None:
                    requirements = ChallengeRequirementsDict(anonymize=anonymize)
                else:
                    requirements["anonymize"] = anonymize

            challenge_type = kwargs.get("type")

            try:
                if challenge_type == ChallengeType.STANDARD:
                    payload = CreateStandardChallengePayload(
                        requirements=requirements, **kwargs
                    )
                elif challenge_type == ChallengeType.DYNAMIC:
                    payload = CreateDynamicChallengePayload(
                        requirements=requirements, **kwargs
                    )
                else:
                    raise ValueError(f"Invalid challenge type: {challenge_type}")
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        result = self._client.request(
            "POST",
            "/api/v1/challenges",
            json=payload.dump_json(),
            response_model=challenge_write_result_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

        if flags is not None:
            for flag in flags:
                self._client.flags.create(
                    challenge_id=result.id,
                    content=flag[0],
                    type=flag[1],
                    case_insensitive=flag[2],
                )

        if hints is not None:
            for hint in hints:
                self._client.hints.create(
                    challenge_id=result.id, content=hint[0], cost=hint[1]
                )

        if tags is not None:
            for tag in tags:
                self._client.tags.create(challenge_id=result.id, value=tag)

        if topics is not None:
            for topic in topics:
                self._client.topics.create(challenge_id=result.id, value=topic)

        if files is not None:
            self._client.files.create(
                challenge_id=result.id, file_paths=files, type=FileType.CHALLENGE
            )

        return result

    @admin_only
    async def async_create(
        self,
        *,
        payload: (
            CreateStandardChallengePayload | CreateDynamicChallengePayload
        ) = MISSING,
        **kwargs,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult:
        flags = kwargs.pop("flags", None)

        if flags is None:
            flag = kwargs.pop("flag", None)

            if flag is not None:
                flag_type = kwargs.pop("flag_type", FlagType.STATIC)
                case_insensitive = kwargs.pop("case_insensitive", False)
                flags = [(flag, flag_type, case_insensitive)]
        else:
            _flags = []

            for flag in flags:
                if isinstance(flag, str):
                    _flags.append((flag, FlagType.STATIC, False))
                elif isinstance(flag, tuple):
                    if len(flag) == 1:
                        _flags.append((flag[0], FlagType.STATIC, False))
                    elif len(flag) == 2:
                        _flags.append((flag[0], flag[1], False))
                    elif len(flag) == 3:
                        _flags.append((flag[0], flag[1], flag[2]))
                    else:
                        raise ValueError("Invalid flag tuple")
                else:
                    raise ValueError("Invalid flag type")

            flags = _flags

        hints = kwargs.pop("hints", None)
        tags = kwargs.pop("tags", None)
        topics = kwargs.pop("topics", None)
        files = kwargs.pop("files", None)

        if payload is MISSING:
            prerequisites = kwargs.pop("prerequisites", None)
            anonymize = kwargs.pop("anonymize", None)

            requirements = None

            if prerequisites is not None:
                for i, prerequisite in enumerate(prerequisites):
                    if isinstance(prerequisite, int):
                        continue
                    elif hasattr(prerequisite, "id"):
                        prerequisites[i] = prerequisite.id
                    else:
                        raise ValueError(f"Invalid prerequisite: {prerequisite}")

                requirements = ChallengeRequirementsDict(prerequisites=prerequisites)

            if anonymize is not None:
                if requirements is None:
                    requirements = ChallengeRequirementsDict(anonymize=anonymize)
                else:
                    requirements["anonymize"] = anonymize

            challenge_type = kwargs.get("type")

            try:
                if challenge_type == ChallengeType.STANDARD:
                    payload = CreateStandardChallengePayload(
                        requirements=requirements, **kwargs
                    )
                elif challenge_type == ChallengeType.DYNAMIC:
                    payload = CreateDynamicChallengePayload(
                        requirements=requirements, **kwargs
                    )
                else:
                    raise ValueError(f"Invalid challenge type: {challenge_type}")
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        result = await self._client.arequest(
            "POST",
            "/api/v1/challenges",
            json=payload.dump_json(),
            response_model=challenge_write_result_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

        if flags is not None:
            for flag in flags:
                await self._client.flags.async_create(
                    challenge_id=result.id,
                    content=flag[0],
                    type=flag[1],
                    case_insensitive=flag[2],
                )

        if hints is not None:
            for hint in hints:
                await self._client.hints.async_create(
                    challenge_id=result.id, content=hint[0], cost=hint[1]
                )

        if tags is not None:
            for tag in tags:
                await self._client.tags.async_create(challenge_id=result.id, value=tag)

        if topics is not None:
            for topic in topics:
                await self._client.topics.async_create(
                    challenge_id=result.id, value=topic
                )

        if files is not None:
            await self._client.files.async_create(
                challenge_id=result.id, file_paths=files, type=FileType.CHALLENGE
            )

        return result

    def attempt(self, challenge_id: int, submission: str) -> ChallengeAttemptResult:
        try:
            return self._client.request(
                "POST",
                "/api/v1/challenges/attempt",
                json={"challenge_id": challenge_id, "submission": submission},
                response_model=ChallengeAttemptResult,
                error_models={
                    400: BadRequest,
                    401: Unauthorized,
                    403: BadChallengeAttempt,
                    404: NotFound,
                    429: BadChallengeAttempt,
                },
            )
        except BadChallengeAttempt as e:
            # This is cursed
            try:
                data: APIResponse = e.response.json()
            except Exception:
                if e.response.status_code == 403:
                    raise Forbidden(response=e.response) from e
                else:
                    raise e from e

            try:
                return ChallengeAttemptResult.model_validate(data["data"])
            except Exception as e:
                raise e from e

    async def async_attempt(
        self, challenge_id: int, submission: str
    ) -> ChallengeAttemptResult:
        try:
            return await self._client.arequest(
                "POST",
                "/api/v1/challenges/attempt",
                json={"challenge_id": challenge_id, "submission": submission},
                response_model=ChallengeAttemptResult,
                error_models={
                    400: BadRequest,
                    401: Unauthorized,
                    403: BadChallengeAttempt,
                    404: NotFound,
                    429: BadChallengeAttempt,
                },
            )
        except BadChallengeAttempt as e:
            # This is cursed
            try:
                data: APIResponse = e.response.json()
            except Exception:
                if e.response.status_code == 403:
                    raise Forbidden(response=e.response) from e
                else:
                    raise e from e

            try:
                return ChallengeAttemptResult.model_validate(data["data"])
            except Exception as e:
                raise e from e

    @admin_only
    def get_types(self) -> list[ChallengeTypeInfo]:
        return self._client.request(
            "GET",
            "/api/v1/challenges/types",
            response_model=challenge_type_info_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_types(self) -> list[ChallengeTypeInfo]:
        return await self._client.arequest(
            "GET",
            "/api/v1/challenges/types",
            response_model=challenge_type_info_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    def get(self, challenge_id: int) -> StandardChallenge | DynamicChallenge:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}",
            response_model=challenge_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    async def async_get(
        self, challenge_id: int
    ) -> StandardChallenge | DynamicChallenge:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}",
            response_model=challenge_adapter,
            error_models={
                400: BadRequest,
                401: Unauthorized,
                403: Forbidden,
                404: NotFound,
            },
        )

    # Update with base challenge payload
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        payload: UpdateBaseChallengePayload,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        payload: UpdateBaseChallengePayload,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult: ...

    # Update with standard challenge payload
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        payload: UpdateStandardChallengePayload,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        payload: UpdateStandardChallengePayload,
    ) -> StandardChallengeWriteResult: ...

    # Update with dynamic challenge payload
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        payload: UpdateDynamicChallengePayload,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        payload: UpdateDynamicChallengePayload,
    ) -> DynamicChallengeWriteResult: ...

    # Update standard or dynamic challenge with individual parameters
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult: ...

    # Update standard challenge with individual parameters
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        value: int = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> StandardChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        value: int = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> StandardChallengeWriteResult: ...

    # Update dynamic challenge with individual parameters
    @overload
    def update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        initial: int = MISSING,
        decay: int = MISSING,
        minimum: int = MISSING,
        function: DecayFunction = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> DynamicChallengeWriteResult: ...

    @overload
    async def async_update(
        self,
        challenge_id: int,
        *,
        name: str = MISSING,
        description: str = MISSING,
        category: str = MISSING,
        initial: int = MISSING,
        decay: int = MISSING,
        minimum: int = MISSING,
        function: DecayFunction = MISSING,
        state: ChallengeState = MISSING,
        connection_info: str | None = MISSING,
        next_id: int | None = MISSING,
        max_attempts: int | None = MISSING,
        prerequisites: list[int | _HasChallengeID] | None = MISSING,
        anonymize: bool | None = MISSING,
    ) -> DynamicChallengeWriteResult: ...

    @admin_only
    def update(
        self,
        challenge_id: int,
        *,
        payload: (
            UpdateStandardChallengePayload | UpdateDynamicChallengePayload
        ) = MISSING,
        **kwargs,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult:
        if payload is MISSING:
            prerequisites = kwargs.pop("prerequisites", None)
            anonymize = kwargs.pop("anonymize", None)

            requirements = None

            if prerequisites is not None:
                for i, prerequisite in enumerate(prerequisites):
                    if isinstance(prerequisite, int):
                        continue
                    elif hasattr(prerequisite, "id"):
                        prerequisites[i] = prerequisite.id
                    else:
                        raise ValueError(f"Invalid prerequisite: {prerequisite}")

                requirements = ChallengeRequirementsDict(prerequisites=prerequisites)

            if anonymize is not None:
                if requirements is None:
                    requirements = ChallengeRequirementsDict(anonymize=anonymize)
                else:
                    requirements["anonymize"] = anonymize

            if requirements is not None:
                kwargs["requirements"] = requirements

            UNIQUE_FIELDS = {
                "standard": ("value",),
                "dynamic": ("initial", "decay", "minimum", "function"),
            }

            # check for unique fields, else fallback to base payload
            payload_type = None
            for key, value in UNIQUE_FIELDS.items():
                if any(k in kwargs for k in value):
                    payload_type = key
                    break

            try:
                if payload_type is None:
                    payload = UpdateBaseChallengePayload(**kwargs)
                elif payload_type == "standard":
                    payload = UpdateStandardChallengePayload(**kwargs)
                elif payload_type == "dynamic":
                    payload = UpdateDynamicChallengePayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return self._client.request(
            "PATCH",
            f"/api/v1/challenges/{challenge_id}",
            json=payload.dump_json(),
            response_model=challenge_write_result_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_update(
        self,
        challenge_id: int,
        *,
        payload: (
            UpdateStandardChallengePayload | UpdateDynamicChallengePayload
        ) = MISSING,
        **kwargs,
    ) -> StandardChallengeWriteResult | DynamicChallengeWriteResult:
        if payload is MISSING:
            prerequisites = kwargs.pop("prerequisites", None)
            anonymize = kwargs.pop("anonymize", None)

            requirements = None

            if prerequisites is not None:
                for i, prerequisite in enumerate(prerequisites):
                    if isinstance(prerequisite, int):
                        continue
                    elif hasattr(prerequisite, "id"):
                        prerequisites[i] = prerequisite.id
                    else:
                        raise ValueError(f"Invalid prerequisite: {prerequisite}")

                requirements = ChallengeRequirementsDict(prerequisites=prerequisites)

            if anonymize is not None:
                if requirements is None:
                    requirements = ChallengeRequirementsDict(anonymize=anonymize)
                else:
                    requirements["anonymize"] = anonymize

            if requirements is not None:
                kwargs["requirements"] = requirements

            UNIQUE_FIELDS = {
                "standard": ("value",),
                "dynamic": ("initial", "decay", "minimum", "function"),
            }

            # check for unique fields, else fallback to base payload
            payload_type = None
            for key, value in UNIQUE_FIELDS.items():
                if any(k in kwargs for k in value):
                    payload_type = key
                    break

            try:
                if payload_type is None:
                    payload = UpdateBaseChallengePayload(**kwargs)
                elif payload_type == "standard":
                    payload = UpdateStandardChallengePayload(**kwargs)
                elif payload_type == "dynamic":
                    payload = UpdateDynamicChallengePayload(**kwargs)
            except ValidationError as e:
                raise ModelValidationError(e.errors()) from e

        return await self._client.arequest(
            "PATCH",
            f"/api/v1/challenges/{challenge_id}",
            json=payload.dump_json(),
            response_model=challenge_write_result_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def delete(self, challenge_id: int) -> None:
        self._client.request(
            "DELETE",
            f"/api/v1/challenges/{challenge_id}",
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_delete(self, challenge_id: int) -> None:
        await self._client.arequest(
            "DELETE",
            f"/api/v1/challenges/{challenge_id}",
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_files(self, challenge_id: int) -> list[ChallengeFileLocation]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/files",
            response_model=challenge_file_location_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_files(self, challenge_id: int) -> list[ChallengeFileLocation]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/files",
            response_model=challenge_file_location_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_flags(self, challenge_id: int) -> list[Flag]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/flags",
            response_model=flag_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_flags(self, challenge_id: int) -> list[Flag]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/flags",
            response_model=flag_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_hints(self, challenge_id: int) -> list[Hint]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/hints",
            response_model=hint_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_hints(self, challenge_id: int) -> list[Hint]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/hints",
            response_model=hint_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_requirements(self, challenge_id: int) -> ChallengeRequirements:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/requirements",
            response_model=ChallengeRequirements,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_requirements(self, challenge_id: int) -> ChallengeRequirements:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/requirements",
            response_model=ChallengeRequirements,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_solves(self, challenge_id: int) -> list[ChallengeSolve]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/solves",
            response_model=challenge_solves_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_solves(self, challenge_id: int) -> list[ChallengeSolve]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/solves",
            response_model=challenge_solves_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_tags(self, challenge_id: int) -> list[Tag]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/tags",
            response_model=tag_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_tags(self, challenge_id: int) -> list[Tag]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/tags",
            response_model=tag_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    def get_topics(self, challenge_id: int) -> list[ChallengeTopic]:
        return self._client.request(
            "GET",
            f"/api/v1/challenges/{challenge_id}/topics",
            response_model=challenge_topic_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )

    @admin_only
    async def async_get_topics(self, challenge_id: int) -> list[ChallengeTopic]:
        return await self._client.arequest(
            "GET",
            f"/api/v1/challenges/{challenge_id}/topics",
            response_model=challenge_topic_list_adapter,
            error_models={400: BadRequest, 401: Unauthorized, 403: Forbidden},
        )
