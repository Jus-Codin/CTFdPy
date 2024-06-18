"""
## Exception Hierachy

- [`CTFdpyException`][ctfdpy.exceptions.CTFdpyException]
    - [`RequestTimeout`][ctfdpy.exceptions.RequestTimeout]
    - [`AuthenticationError`][ctfdpy.exceptions.AuthenticationError]
    - [`APIResponseException`][ctfdpy.exceptions.APIResponseException]
        - [`BadRequest`][ctfdpy.exceptions.BadRequest]
        - [`Unauthorized`][ctfdpy.exceptions.Unauthorized]
        - [`Forbidden`][ctfdpy.exceptions.Forbidden]
        - [`NotFound`][ctfdpy.exceptions.NotFound]
        - [`AdminOnly`][ctfdpy.exceptions.AdminOnly]
        - [`UnsuccessfulResponse`][ctfdpy.exceptions.UnsuccessfulResponse]
        - [`BadChallengeAttempt`][ctfdpy.exceptions.BadChallengeAttempt]
    - [`ModelValidationError`][ctfdpy.exceptions.ModelValidationError]
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Request, Response


class CTFdpyException(Exception):
    """
    Base exception for CTFdpy
    """

    pass


class RequestTimeout(CTFdpyException):
    """
    Exception raised when a request times out
    """

    def __init__(self, *args, request: dict[str, Request] | None = None):
        self.request = request
        super().__init__(*args)


class AuthenticationError(CTFdpyException):
    """
    Exception raised when a user is not authenticated
    """


class APIResponseException(CTFdpyException):
    """
    Exception raised when a request to the CTFd API fails
    """

    def __init__(self, *args, response: Response | None = None):
        self.response = response
        super().__init__(*args)


class BadRequest(APIResponseException):
    """
    Exception raised when a request returns a 400
    """

    pass


class Unauthorized(APIResponseException):
    """
    Exception raised when a request returns a 401
    """

    pass


class Forbidden(APIResponseException):
    """
    Exception raised when a request returns a 403
    """

    pass


class NotFound(APIResponseException):
    """
    Exception raised when a request returns a 404
    """

    pass


class AdminOnly(APIResponseException):
    """
    Exception raised when a request requires the user to be an admin
    """

    pass


class UnsuccessfulResponse(APIResponseException):
    """
    Exception raised when the response is not successful
    """

    pass


class BadChallengeAttempt(APIResponseException):
    """
    Exception raised when a challenge attempt returns a non200 response
    """

    pass


class ModelValidationError(CTFdpyException):
    """
    Exception raised when a model fails validation
    """

    pass
