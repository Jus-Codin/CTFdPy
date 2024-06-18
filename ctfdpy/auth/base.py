from __future__ import annotations

import abc
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class BaseAuthStrategy(abc.ABC):
    @abc.abstractmethod
    def get_auth_flow(self, client: APIClient) -> httpx.Auth:
        raise NotImplementedError
