"""Schema for the Question model."""
from pydantic import BaseModel, ConfigDict
from src.backend.schemas.common import Text
from src.backend.schemas.enums import Option

class QuestionCreate(BaseModel):
    """Schema for creating a new question."""
    model_config = ConfigDict(use_enum_values=True)

    section_id: int
    text: Text
    option_a: Text
    option_b: Text
    option_c: Text
    option_d: Text
    correct_option: Option

class QuestionUpdate(BaseModel):
    """Schema for updating an existing question."""
    model_config = ConfigDict(use_enum_values=True)

    section_id: int | None = None
    text: Text | None = None
    option_a: Text | None = None
    option_b: Text | None = None
    option_c: Text | None = None
    option_d: Text | None = None
    correct_option: Option | None = None
    flagged: bool | None = None

class QuestionRead(BaseModel):
    """Schema for reading a question."""
    id: int
    section_id: int
    section_name: str
    topic_id: int
    topic_name: str
    text: Text
    option_a: Text
    option_b: Text
    option_c: Text
    option_d: Text
    correct_option: Option
    flagged: bool