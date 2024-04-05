from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

from ctfdpy.exceptions import (
    CTFdpyBadRequestException,
    CTFdpyNotFoundException,
    CTFdpyRequestException,
    CTFdpyUnauthorizedException,
)

if TYPE_CHECKING:
    from httpx import Response

    from ctfdpy.client import Client


class APIResponse(TypedDict):
    """API response structure."""

    data: Any | None
    success: bool
    errors: list[str] | dict[str, str] | None
    message: str | None


class API:
    """
    The base class for interacting with an API endpoint

    Parameters
    ----------
    client : ctfdy.Client
        The client to use for requests

    Attributes
    ----------
    client : ctfdpy.Client
        The client used for requests
    url : str
        The URL of the CTFd instance
    session : httpx.HttpClient
        The HTTP session used for requests

    Methods
    -------
    handle_response(response: httpx.Response) -> APIResponse
        Handles an API response
    _get(endpoint: str, **kwargs) -> APIResponse
        Sends a GET request to an endpoint
    _post(endpoint: str, json: dict[str, Any], **kwargs) -> APIResponse
        Sends a POST request to an endpoint
    _patch(endpoint: str, json: dict[str, Any], **kwargs) -> APIResponse
        Sends a PATCH request to an endpoint
    _delete(endpoint: str, **kwargs) -> APIResponse
        Sends a DELETE request to an endpoint
    """

    def __init__(self, client: Client):
        self.client = client
        self.url = client.url
        self.session = client.session

    def handle_response(self, response: Response) -> APIResponse:
        """
        Handles an API response

        Parameters
        ----------
        response : httpx.Response
            The response to handle

        Returns
        -------
        APIResponse
            The handled response

        Raises
        ------
        CTFdpyBadRequestException
            If the response status code is 400
        CTFdpyUnauthorizedException
            If the response status code is 403
        CTFdpyNotFoundException
            If the response status code is 404
        CTFdpyRequestException
            If the response status code is not 2xx, 400, 403, or 404
        """
        match response.status_code:

            case code if 200 <= code < 300:
                pass

            case 400:
                raise CTFdpyBadRequestException(response=response)

            case 403:
                raise CTFdpyUnauthorizedException(response=response)

            case 404:
                raise CTFdpyNotFoundException(response=response)

            case _:
                raise CTFdpyRequestException(response=response)

        data = response.json()
        if not data["success"]:
            raise Exception(data.get("errors") or data["message"])

        return data

    def _get(self, endpoint: str, **kwargs) -> APIResponse:
        response = self.session.get(self.url + endpoint, **kwargs)
        return self.handle_response(response)

    def _post(self, endpoint: str, json: dict[str, Any], **kwargs) -> APIResponse:
        response = self.session.post(self.url + endpoint, json=json, **kwargs)
        return self.handle_response(response)

    def _patch(self, endpoint: str, json: dict[str, Any], **kwargs) -> APIResponse:
        response = self.session.patch(self.url + endpoint, json=json, **kwargs)
        return self.handle_response(response)

    def _delete(self, endpoint: str, **kwargs) -> APIResponse:
        response = self.session.delete(self.url + endpoint, **kwargs)
        return self.handle_response(response)
