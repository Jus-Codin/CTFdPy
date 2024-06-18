from __future__ import annotations

from functools import wraps
from inspect import isawaitable
from typing import TYPE_CHECKING, Any, Callable, ParamSpec, TypeVar

from httpx import Response

from ctfdpy.auth.unauth import UnauthAuthStrategy
from ctfdpy.exceptions import AdminOnly, AuthenticationError, Forbidden

if TYPE_CHECKING:
    from ctfdpy.client import APIClient

T = TypeVar("T")
P = ParamSpec("P")


class _MissingSentinel:
    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING: Any = _MissingSentinel()


class _API:
    _client: APIClient


def auth_only(f: Callable[P, T]) -> Callable[P, T]:
    """
    Wrapper for endpoints that require the user to be authenticated.

    Checks if the client has a token or credentials set and raises an `AuthenticationRequired` exception if not.
    """

    @wraps(f)
    def wrapper(self: _API, *args: P.args, **kwargs: P.kwargs) -> T:
        if isinstance(self._client.auth, UnauthAuthStrategy):
            raise AuthenticationError("Authentication required to access this endpoint")

        return f(self, *args, **kwargs)

    return wrapper


def _is_non_admin_response(response: Response) -> bool:
    try:
        data = response.json()
    except Exception:
        return False

    # This is a bit hacky, we look for the default Flask 403 error message
    # This is dangerous as the endpoints might raise this error message as well
    if data.get("message") == (
        "You don't have the permission to access the requested"
        " resource. It is either read-protected or not readable by the"
        " server."
    ):
        return True

    return False


def admin_only(f: Callable[P, T]) -> Callable[P, T]:
    """
    Wrapper for endpoints that require the user to be an admin.

    Raises an `AdminOnly` exception if the user is not an admin, or `AuthenticationRequired` if the user is not authenticated.
    """

    @wraps(f)
    def wrapper(self: _API, *args: P.args, **kwargs: P.kwargs) -> T:
        if isinstance(self._client.auth, UnauthAuthStrategy):
            raise AuthenticationError("Authentication required to access this endpoint")

        try:
            result = f(self, *args, **kwargs)
        except Forbidden as e:
            if _is_non_admin_response(e.response):
                raise AdminOnly("Admin user required", response=e.response)
            else:
                raise e from e

        if isawaitable(result):

            async def _wrapper() -> T:
                try:
                    return await result
                except Forbidden as e:
                    if _is_non_admin_response(e.response):
                        raise AdminOnly("Admin user required", response=e.response)
                    else:
                        raise e from e

            return _wrapper()
        else:
            return result

    return wrapper
