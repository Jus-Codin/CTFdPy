"""
## Exception Hierarchy

- [`CTFdpyException`][ctfdpy.exceptions.CTFdpyException]
    - [`CTFdpyRequestException`][ctfdpy.exceptions.CTFdpyRequestException]
        - [`CTFdpyBadRequestException`][ctfdpy.exceptions.CTFdpyBadRequestException]
        - [`CTFdpyUnauthorizedException`][ctfdpy.exceptions.CTFdpyUnauthorizedException]
        - [`CTFdpyNotFoundException`][ctfdpy.exceptions.CTFdpyNotFoundException]
        - [`CTFdpyAdminOnlyException`][ctfdpy.exceptions.CTFdpyAdminOnlyException]
    - [`CTFdpyModelValidationError`][ctfdpy.exceptions.CTFdpyModelValidationError]
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response


class CTFdpyException(Exception):
    """
    Base exception for CTFdpy
    """

    pass


class CTFdpyRequestException(CTFdpyException):
    """
    Exception raised when a request to the CTFd API fails
    """

    def __init__(self, *args, response: Response | None = None):
        self.response = response
        super().__init__(*args)


class CTFdpyBadRequestException(CTFdpyRequestException):
    """
    Exception raised when a request returns a 400
    """

    pass


class CTFdpyUnauthorizedException(CTFdpyRequestException):
    """
    Exception raised when a request returns a 403
    """

    pass


class CTFdpyNotFoundException(CTFdpyRequestException):
    """
    Exception raised when a resource is not found
    """

    pass


class CTFdpyAdminOnlyException(CTFdpyRequestException):
    """
    Exception raised when a request requires the user to be an admin
    """

    pass


class CTFdpyModelValidationError(CTFdpyException):
    """
    Exception raised when a model fails validation
    """

    pass
