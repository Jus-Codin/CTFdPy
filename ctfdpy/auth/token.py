from __future__ import annotations

import os
from typing import TYPE_CHECKING, Generator

import httpx

from ctfdpy.auth.base import BaseAuthStrategy

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class TokenAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Token {self.token}"
        yield request


class TokenAuthStrategy(BaseAuthStrategy):
    """API Token Authentication"""

    def __init__(self, token: str):
        self.token = token

    @classmethod
    def from_env(cls) -> TokenAuthStrategy:
        token = os.getenv("CTFD_TOKEN")
        if token is None:
            raise ValueError("CTFD_TOKEN environment variable must be set")
        return cls(token)

    def get_auth_flow(self, client: APIClient) -> httpx.Auth:
        return TokenAuth(self.token)
