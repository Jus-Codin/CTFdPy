from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from ctfdpy.exceptions import CTFdpyAdminOnlyException, CTFdpyUnauthorizedException

if TYPE_CHECKING:
    from ctfdpy.api.api import API


class _MissingSentinel:
    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING = _MissingSentinel()


_non_admins = set()  # stores tokens and usernames of non-admins


def admin_only(f):
    """
    Wrapper for endpoints that require the user to be an admin

    When a non-admin first tries to access an endpoint that requires admin privileges,
    it will send a request to the endpoint. The endpoint will then raise a 403 error.
    This wrapper will then cache the client's admin status and block all other requests to
    admin-only endpoints.
    """

    @wraps(f)
    def wrapper(self: API, *args, **kwargs):
        credentials = self.client.token or self.client.credentials[0]

        if credentials in _non_admins:
            raise CTFdpyAdminOnlyException("Admin user required")

        try:
            result = f(self, *args, **kwargs)
        except CTFdpyUnauthorizedException as e:
            response = e.response

            data = None
            try:
                data = response.json()
            except Exception:
                pass

            # This is a bit hacky, we look for the default Flask 403 error message
            # This is dangerous as the endpoints might raise this error message as well
            if data and data.get("message") == (
                "You don't have the permission to access the requested"
                " resource. It is either read-protected or not readable by the"
                " server."
            ):
                raise CTFdpyAdminOnlyException("Admin user required", response=response)

            _non_admins.add(credentials)
            raise e

        return result

    return wrapper
