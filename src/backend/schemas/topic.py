"""Schema for the Topic model."""
from pydantic import BaseModel, ConfigDict
from src.backend.schemas.common import Name

class TopicCreate(BaseModel):
    """Schema for creating a new topic."""
    name: Name

class TopicUpdate(BaseModel):
    """Schema for updating an existing topic."""
    name: Name | None = None

class TopicRead(BaseModel):
    """Schema for reading a topic."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: Name