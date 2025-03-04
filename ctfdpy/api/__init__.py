from __future__ import annotations

from typing import TYPE_CHECKING

from ctfdpy.api.challenges import ChallengesAPI
from ctfdpy.api.files import FilesAPI
from ctfdpy.api.flags import FlagsAPI
from ctfdpy.api.hints import HintsAPI
from ctfdpy.api.tags import TagsAPI
from ctfdpy.api.teams import TeamsAPI
from ctfdpy.api.topics import TopicsAPI
from ctfdpy.api.users import UsersAPI

if TYPE_CHECKING:
    from ctfdpy.client import APIClient


class APIMixin:
    _client: APIClient

    def __init__(self, client: APIClient):
        self._client = client

        self._challenges_api = ChallengesAPI(self._client)
        self._files_api = FilesAPI(self._client)
        self._flags_api = FlagsAPI(self._client)
        self._hints_api = HintsAPI(self._client)
        self._tags_api = TagsAPI(self._client)
        self._teams_api = TeamsAPI(self._client)
        self._topics_api = TopicsAPI(self._client)
        self._users_api = UsersAPI(self._client)

    @property
    def challenges(self) -> ChallengesAPI:
        return self._challenges_api

    @property
    def files(self) -> FilesAPI:
        return self._files_api

    @property
    def flags(self) -> FlagsAPI:
        return self._flags_api

    @property
    def hints(self) -> HintsAPI:
        return self._hints_api

    @property
    def tags(self) -> TagsAPI:
        return self._tags_api

    @property
    def teams(self) -> TeamsAPI:
        return self._teams_api

    @property
    def topics(self) -> TopicsAPI:
        return self._topics_api

    @property
    def users(self) -> UsersAPI:
        return self._users_api
