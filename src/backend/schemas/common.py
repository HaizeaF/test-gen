"""Types shared by the API schemas."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, StringConstraints

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ReadModel(BaseModel):
    """Base for the schemas the API returns."""

    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)


class UpdateModel(BaseModel):
    """Base for the schemas of partial updates."""

    def changes(self) -> dict[str, Any]:
        """Return only the fields the client sent with a value."""
        return self.model_dump(exclude_unset=True, exclude_none=True)
