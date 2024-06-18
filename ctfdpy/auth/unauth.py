from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ctfdpy.auth.base import BaseAuthStrategy

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class UnauthAuthStrategy(BaseAuthStrategy):
    """Unauthenticated Strategy"""

    def get_auth_flow(self, client: APIClient) -> httpx.Auth:
        return httpx.Auth()
