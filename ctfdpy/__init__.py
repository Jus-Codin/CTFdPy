"""
CTFd API Wrapper
~~~~~~~~~~~~~~~~

A Python wrapper for the CTFd API

:copyright: (c) 2024-present Jus-Codin
:license: MIT, see LICENSE for more details.
"""

__title__ = "ctfdpy"
__author__ = "Jus-Codin"
__license__ = "MIT"
__version__ = "0.1.0"

__all__ = [
    "CredentialAuthStrategy",
    "TokenAuthStrategy",
    "APIClient",
    "ChallengeState",
    "ChallengeType",
    "DecayFunction",
    "FileType",
    "FlagType",
    "HintType",
    "UserType",
]

from ctfdpy.auth import CredentialAuthStrategy, TokenAuthStrategy
from ctfdpy.client import APIClient
from ctfdpy.models.challenges import ChallengeState, ChallengeType, DecayFunction
from ctfdpy.models.files import FileType
from ctfdpy.models.flags import FlagType
from ctfdpy.models.hints import HintType
from ctfdpy.models.users import UserType
