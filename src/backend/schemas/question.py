"""Schema for the Question model."""

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from src.backend.schemas.common import ReadModel, Text, UpdateModel
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


class QuestionUpdate(UpdateModel):
    """Schema for updating an existing question."""

    model_config = ConfigDict(use_enum_values=True)

    section_id: int | None = None
    text: Text | None = None
    option_a: Text | None = None
    option_b: Text | None = None
    option_c: Text | None = None
    option_d: Text | None = None
    correct_option: Option | None = None
    active: bool | None = None
    flagged: bool | None = None


class QuestionRead(ReadModel):
    """Schema for reading a question."""

    id: int
    section_id: int
    section_name: str = Field(validation_alias=AliasPath("section", "name"))
    topic_id: int = Field(validation_alias=AliasPath("section", "topic_id"))
    topic_name: str = Field(validation_alias=AliasPath("section", "topic", "name"))
    text: Text
    option_a: Text
    option_b: Text
    option_c: Text
    option_d: Text
    correct_option: Option
    active: bool
    flagged: bool
