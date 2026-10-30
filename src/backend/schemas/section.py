"""Schema for the Section model."""

from pydantic import AliasPath, BaseModel, Field

from src.backend.schemas.common import Name, ReadModel, UpdateModel


class SectionCreate(BaseModel):
    """Schema for creating a new section."""

    topic_id: int
    name: Name


class SectionUpdate(UpdateModel):
    """Schema for updating an existing section."""

    topic_id: int | None = None
    name: Name | None = None


class SectionRead(ReadModel):
    """Schema for reading a section."""

    id: int
    name: Name
    topic_id: int
    topic_name: str = Field(validation_alias=AliasPath("topic", "name"))
