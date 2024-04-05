from __future__ import annotations

import os

from httpx import AsyncClient as AsyncHttpClient
from httpx import Client as HttpClient

from ctfdpy.api import *


class Client:
    """
    The main class for interacting with a CTFd instance

    Parameters
    ----------
    url : str
        The URL of the CTFd instance
    token : str, optional
        The token to use for authentication, by default None
    credentials : tuple[str, str], optional
        The username and password to use for authentication, by default None

    Attributes
    ----------
    token : str | None
        The token used for authentication
    credentials : tuple[str, str] | None
        The username and password used for authentication
    url : str
        The URL of the CTFd instance
    session : HttpClient
        The HTTP session used for requests

    Methods
    -------
    with_token(url: str, token: str) -> Client
        Creates a Client instance with a token
    with_credentials(url: str, credentials: tuple[str, str]) -> Client
        Creates a Client instance with credentials
    from_env() -> Client
        Creates a Client instance from environment variables
    login()
        Logs into the CTFd instance
    """

    def __init__(
        self,
        url: str = "http://localhost:8080",
        token: str | None = None,
        credentials: tuple[str, str] | None = None,
    ) -> None:
        self.token = token
        self.credentials = credentials

        if self.token is None and self.credentials is None:
            raise ValueError("Either token or credentials must be provided")

        self.url = url.rstrip("/")

        self.session = HttpClient()
        self.session.headers.update({"Content-Type": "application/json"})

        if token is not None:
            self.session.headers.update({"Authorization": f"Token {token}"})

    @classmethod
    def with_token(cls, url: str, token: str) -> Client:
        """
        Creates a Client instance with a token

        Parameters
        ----------
        url : str
            The URL of the CTFd instance
        token : str
            The token to use for authentication

        Returns
        -------
        Client
            The Client instance
        """
        return cls(url=url, token=token)

    @classmethod
    def with_credentials(cls, url: str, credentials: tuple[str, str]) -> Client:
        """
        Creates a Client instance with credentials

        Parameters
        ----------
        url : str
            The URL of the CTFd instance
        credentials : tuple[str, str]
            The username and password to use for authentication

        Returns
        -------
        Client
            The Client instance
        """
        client = cls(url=url, credentials=credentials)
        client.login()
        return client

    @classmethod
    def from_env(cls) -> Client:
        """
        Creates a Client instance from environment variables

        Returns
        -------
        Client
            The Client instance
        """
        url = os.getenv("CTFD_URL")
        token = os.getenv("CTFD_TOKEN")
        credentials = (os.getenv("CTFD_USERNAME"), os.getenv("CTFD_PASSWORD"))

        if token is not None:
            return cls.with_token(url, token)
        elif credentials is not None:
            return cls.with_credentials(url, credentials)
        else:
            raise ValueError("No credentials found in environment")

    def login(self) -> None:
        """Logs into the CTFd instance

        This should only be used if you do not want to use a token.

        Returns
        -------
        None

        Raises
        ------
        httpx.HTTPError
            If the request fails
        """
        response = self.session.post(
            f"{self.url}/login",
            data={"name": self.credentials[0], "password": self.credentials[1]},
        )
        response.raise_for_status()
