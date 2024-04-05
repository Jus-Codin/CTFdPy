from __future__ import annotations

from pydantic import BaseModel


class Model(BaseModel, validate_assignment=True, extra="allow"):
    """
    The base model for all models

    This class should not be instantiated directly
    """


# class ResponseModel(Model, extra="allow"):
#     """
#     The base model for all response models returned by the API

#     This class should not be instantiated directly
#     """


class CreatePayloadModel(Model, extra="forbid"):
    """
    The base model for all create payload models

    This class should not be instantiated directly
    """


class UpdatePayloadModel(Model, extra="forbid"):
    """
    The base model for all update payload models

    This class should not be instantiated directly
    """
