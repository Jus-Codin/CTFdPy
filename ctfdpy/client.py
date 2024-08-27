from __future__ import annotations

import os
from contextvars import ContextVar
from types import TracebackType
from typing import Any, Callable, Generic, Type, TypeVar, cast, overload

import httpx
from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)
from pydantic import BaseModel, TypeAdapter

from ctfdpy.api import APIMixin
from ctfdpy.auth import BaseAuthStrategy, TokenAuthStrategy, UnauthAuthStrategy
from ctfdpy.auth.credentials import CredentialAuthStrategy
from ctfdpy.exceptions import APIResponseException, CTFdpyException, RequestTimeout
from ctfdpy.types.api import APIResponse

T = TypeVar("T")
A = TypeVar("A", bound=BaseAuthStrategy)
AS = TypeVar("AS", bound=BaseAuthStrategy)


class APIClient(Generic[A], APIMixin):
    """
    The main class for interacting with the CTFd API

    Parameters
    ----------
    url : str | httpx.URL
        The base URL of the CTFd instance
    auth : BaseAuthStrategy | str | None
        The authentication strategy to use. If a string is provided, it is assumed to be a token.
        If `None` is provided, no authentication is used.
    user_agent : str, optional
        The user agent to use for requests, by default "CTFdPy/0.1.0"
    follow_redirects : bool, optional
        Whether to follow redirects, by default False

    Attributes
    ----------
    url : httpx.URL
        The base URL of the CTFd instance
    auth : BaseAuthStrategy
        The authentication strategy to use
    challenges : ChallengesAPI
        Interface for interacting with the `/api/v1/challenges` CTFd API endpoint.
    files : FilesAPI
        Interface for interacting with the `/api/v1/files` CTFd API endpoint.
    flags : FlagsAPI
        Interface for interacting with the `/api/v1/flags` CTFd API endpoint.
    hints : HintsAPI
        Interface for interacting with the `/api/v1/hints` CTFd API endpoint.
    tags : TagsAPI
        Interface for interacting with the `/api/v1/tags` CTFd API endpoint.
    topics : TopicsAPI
        Interface for interacting with the `/api/v1/topics` CTFd API endpoint.
    users : UsersAPI
        Interface for interacting with the `/api/v1/users` CTFd API endpoint.
    """

    @overload
    def __init__(
        self: APIClient[UnauthAuthStrategy],
        url: str | httpx.URL,
        auth: None = None,
        *,
        user_agent: str = "CTFdPy/0.1.0",
        follow_redirects: bool = False,
    ): ...

    @overload
    def __init__(
        self: APIClient[TokenAuthStrategy],
        url: str | httpx.URL,
        auth: str,
        *,
        user_agent: str = "CTFdPy/0.1.0",
        follow_redirects: bool = False,
    ): ...

    @overload
    def __init__(
        self: APIClient[AS],
        url: str | httpx.URL,
        auth: AS,
        *,
        user_agent: str = "CTFdPy/0.1.0",
        follow_redirects: bool = False,
    ): ...

    def __init__(
        self,
        url: str | httpx.URL,
        auth: A | str | None = None,
        *,
        user_agent: str = "CTFdPy/0.1.0",
        follow_redirects: bool = False,
    ):
        if isinstance(auth, str):
            auth = TokenAuthStrategy(auth)
        elif auth is None:
            auth = UnauthAuthStrategy()

        self.auth: A = auth

        self.url = httpx.URL(url)
        self._user_agent = user_agent
        self._follow_redirects = follow_redirects

        self.__sync_client: ContextVar[httpx.Client | None] = ContextVar(
            "sync_client", default=None
        )
        self.__async_client: ContextVar[httpx.AsyncClient | None] = ContextVar(
            "async_client", default=None
        )

        super().__init__(self)

    def _get_client_defaults(self) -> dict[str, str]:
        auth_flow = None
        if self.auth is not None:
            auth_flow = self.auth.get_auth_flow(self)

        headers = {"User-Agent": self._user_agent, "Content-Type": "application/json"}

        return {
            "auth": auth_flow,
            "base_url": self.url,
            "headers": headers,
            "follow_redirects": self._follow_redirects,
        }

    def _create_sync_client(self) -> httpx.Client:
        return httpx.Client(**self._get_client_defaults())

    def get_sync_client(self) -> httpx.Client:
        client = self.__sync_client.get()
        if client is not None:
            return client
        else:
            client = self._create_sync_client()
            self.__sync_client.set(client)
            return client

    def close(self) -> None:
        client = self.__sync_client.get()
        if client is not None:
            client.close()
            self.__sync_client.set(None)

    def __enter__(self) -> APIClient:
        if self.__sync_client.get() is not None:
            raise RuntimeError("Sync HTTP client already exists")
        self.__sync_client.set(self._create_sync_client())
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        cast(httpx.Client, self.__sync_client.get()).close()
        self.__sync_client.set(None)

    def _create_async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(**self._get_client_defaults())

    def get_async_client(self) -> httpx.AsyncClient:
        client = self.__async_client.get()
        if client is not None:
            return client
        else:
            client = self._create_async_client()
            self.__async_client.set(client)
            return client

    async def aclose(self) -> None:
        client = self.__async_client.get()
        if client is not None:
            await client.aclose()
            self.__async_client.set(None)

    async def __aenter__(self) -> APIClient:
        if self.__async_client.get() is not None:
            raise RuntimeError("Async HTTP client already exists")
        self.__async_client.set(self._create_async_client())
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        await cast(httpx.AsyncClient, self.__async_client.get()).aclose()
        self.__async_client.set(None)

    def _request(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
    ) -> httpx.Response:
        client = self.get_sync_client()
        try:
            return client.request(
                method,
                url,
                params=params,
                content=content,
                data=data,
                files=files,
                json=json,
                headers=headers,
                cookies=cookies,
            )
        except httpx.TimeoutException as e:
            raise RequestTimeout(request=e.request) from e
        except Exception as e:
            raise CTFdpyException(repr(e)) from e

    async def _arequest(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
    ) -> httpx.Response:
        client = self.get_async_client()
        try:
            return await client.request(
                method,
                url,
                params=params,
                content=content,
                data=data,
                files=files,
                json=json,
                headers=headers,
                cookies=cookies,
            )
        except httpx.TimeoutException as e:
            raise RequestTimeout(request=e.request) from e
        except Exception as e:
            raise CTFdpyException(repr(e)) from e

    @overload
    def _handle_response(
        self,
        response: httpx.Response,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> bool | APIResponse: ...

    @overload
    def _handle_response(
        self,
        response: httpx.Response,
        response_model: Type[T] | TypeAdapter[T] | Callable[[APIResponse], T],
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T: ...

    def _handle_response(
        self,
        response: httpx.Response,
        response_model: (
            Type[T] | TypeAdapter[T] | Callable[[APIResponse], T] | None
        ) = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T | bool | APIResponse:
        if not response.is_success:
            error_models = error_models or {}
            status_code = response.status_code

            # This is uh... not great
            error_model = error_models.get(
                status_code,
                error_models.get(
                    f"{str(status_code)[0]}XX",
                    error_models.get("default", APIResponseException),
                ),
            )

            raise error_model(response=response)

        response_data: APIResponse = response.json()

        if response_model is None:
            try:
                return response_data["success"]
            except KeyError:
                return response_data
        elif response_data.get("data") is None:
            raise ValueError("Response data expected to have 'data' key")

        if issubclass(response_model, BaseModel):
            response_data = response_model.model_validate(response_data["data"])
        elif isinstance(response_model, TypeAdapter):
            response_data = response_model.validate_python(response_data["data"])
        elif callable(response_model):
            response_data = response_model(response_data)
        else:
            # This should never happen
            raise ValueError("Invalid response model")

        return response_data

    @overload
    def request(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> bool | APIResponse: ...

    @overload
    def request(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        response_model: Type[T] | TypeAdapter[T] | Callable[[APIResponse], T],
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T: ...

    def request(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        response_model: (
            Type[T] | TypeAdapter[T] | Callable[[APIResponse], T] | None
        ) = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T | bool | APIResponse:
        response = self._request(
            method,
            url,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            headers=headers,
            cookies=cookies,
        )
        return self._handle_response(
            response, response_model=response_model, error_models=error_models
        )

    @overload
    async def arequest(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> bool | APIResponse: ...

    @overload
    async def arequest(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        response_model: Type[T] | TypeAdapter[T] | Callable[[APIResponse], T],
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T: ...

    async def arequest(
        self,
        method: str,
        url: str | httpx.URL,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        response_model: (
            Type[T] | TypeAdapter[T] | Callable[[APIResponse], T] | None
        ) = None,
        error_models: dict[str, APIResponseException] | None = None,
    ) -> T | bool | APIResponse:
        response = await self._arequest(
            method,
            url,
            params=params,
            content=content,
            data=data,
            files=files,
            json=json,
            headers=headers,
            cookies=cookies,
        )
        return self._handle_response(
            response, response_model=response_model, error_models=error_models
        )

    @overload
    @classmethod
    def from_env(
        cls: Type[APIClient[AS]],
        *,
        user_agent: str = "CTFdPy/0.1.0",
        follow_redirects: bool = False,
    ) -> APIClient[AS]: ...

    @classmethod
    def from_env(cls: Type[APIClient[AS]], **kwargs) -> APIClient[AS]:
        """
        Create an APIClient from environment variables

        The following environment variables are used:
        
        - `CTFD_URL`: The base URL of the CTFd instance
        - `CTFD_TOKEN`: The token to use for authentication
        - `CTFD_USERNAME`: The username to use for authentication
        - `CTFD_PASSWORD`: The password to use for authentication
        """
        url = os.getenv("CTFD_URL")
        if url is None:
            raise ValueError("CTFD_URL environment variable must be set")

        auth = None

        token = os.getenv("CTFD_TOKEN")
        if token is not None:
            auth = TokenAuthStrategy(token)

        username = os.getenv("CTFD_USERNAME")
        password = os.getenv("CTFD_PASSWORD")
        if username is not None and password is not None and auth is None:
            auth = CredentialAuthStrategy(username, password)

        return cls(url, auth, **kwargs)
