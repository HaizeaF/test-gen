"""Schema for the Topic model."""

from pydantic import BaseModel

from src.backend.schemas.common import Name, ReadModel, UpdateModel


class TopicCreate(BaseModel):
    """Schema for creating a new topic."""

    name: Name


class TopicUpdate(UpdateModel):
    """Schema for updating an existing topic."""

    name: Name | None = None


class TopicRead(ReadModel):
    """Schema for reading a topic."""

    id: int
    name: Name
