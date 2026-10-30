"""Schema for the Section model."""
from pydantic import BaseModel
from src.backend.schemas.common import Name

class SectionCreate(BaseModel):
    """Schema for creating a new section."""
    topic_id: int
    name: Name

class SectionUpdate(BaseModel):
    """Schema for updating an existing section."""
    topic_id: int | None = None
    name: Name | None = None

class SectionRead(BaseModel):
    """Schema for reading a section."""
    id: int
    name: Name
    topic_id: int
    topic_name: str