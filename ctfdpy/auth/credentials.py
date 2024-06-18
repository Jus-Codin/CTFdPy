from __future__ import annotations

import os
from typing import TYPE_CHECKING, AsyncGenerator, Generator

import httpx

from ctfdpy.auth.base import BaseAuthStrategy
from ctfdpy.exceptions import AuthenticationError

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class CredentialAuth(httpx.Auth):
    def __init__(self, client: APIClient, username: str, password: str):
        self.client = client
        self.username = username
        self.password = password

    def build_login_request(
        self, http_client: httpx.Client | httpx.AsyncClient
    ) -> httpx.Request:
        return http_client.build_request(
            "POST",
            "/login",
            json={"name": self.username, "password": self.password},
        )

    def sync_auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        http_client = self.client.get_sync_client()

        attempted_login = False

        # First, check if the `session` cookie is already set
        if http_client.cookies.get("session", self.client.url.host) is None:
            response = yield self.build_login_request(http_client)

            response.raise_for_status()

            while response.is_redirect:
                response = yield response.next_request

            # If we are back at the login page, the login failed
            if response.url.path == "/login":
                raise AuthenticationError("Incorrect username or password")

            attempted_login = True

        response = yield request

        if response.status_code == 401 and not attempted_login:
            # If the request failed, try logging in again
            response = yield self.build_login_request(http_client)

            response.raise_for_status()

            while response.is_redirect:
                response = yield response.next_request

            if response.url.path == "/login":
                raise AuthenticationError("Incorrect username or password")

            response = yield request

        yield request

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        http_client = self.client.get_async_client()

        attempted_login = False

        # First, check if the `session` cookie is already set
        if http_client.cookies.get("session", self.client.url.host) is None:
            response = yield self.build_login_request(http_client)

            response.raise_for_status()

            while response.is_redirect:
                response = yield response.next_request

            # If we are back at the login page, the login failed
            if response.url.path == "/login":
                raise AuthenticationError("Incorrect username or password")

            attempted_login = True

        response = yield request

        if response.status_code == 401 and not attempted_login:
            # If the request failed, try logging in again
            response = yield self.build_login_request(http_client)

            response.raise_for_status()

            while response.is_redirect:
                response = yield response.next_request

            if response.url.path == "/login":
                raise AuthenticationError("Incorrect username or password")

            response = yield request

        yield request


class CredentialAuthStrategy(BaseAuthStrategy):
    """Credential-based Authentication"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @classmethod
    def from_env(cls) -> CredentialAuthStrategy:
        username = os.getenv("CTFD_USERNAME")
        password = os.getenv("CTFD_PASSWORD")
        if username is None or password is None:
            raise ValueError(
                "CTFD_USERNAME and CTFD_PASSWORD environment variables must be set"
            )
        return cls(username, password)

    def get_auth_flow(self, client: APIClient) -> httpx.Auth:
        return CredentialAuth(client, self.username, self.password)
