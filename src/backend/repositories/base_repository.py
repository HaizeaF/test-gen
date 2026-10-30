"""Operations shared by every repository."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from src.backend.models.errors import NotFoundError


class BaseRepository[T]:
    """Add, get, update and delete rows of one model."""

    model: type[T]
    load_options: Sequence[ORMOption] = ()

    def __init__(self, session: Session) -> None:
        """Initialize the repository with a database session."""
        self.session = session

    def get(self, entity_id: int) -> T:
        """Return the row with this id, or raise NotFoundError naming what is missing."""
        entity = self.session.get(self.model, entity_id, options=self.load_options)
        if entity is None:
            raise NotFoundError(f"{self.model.__name__} {entity_id} not found")
        return entity

    def add(self, entity: T) -> T:
        """Mark a new row to be inserted on the next commit."""
        self.session.add(entity)
        return entity

    def update(self, entity: T, changes: dict[str, Any]) -> T:
        """Copy the changed fields onto the row. They are saved on the next commit."""
        for field, value in changes.items():
            setattr(entity, field, value)
        return entity

    def delete(self, entity: T) -> None:
        """Mark a row to be deleted on the next commit."""
        self.session.delete(entity)

    def _count(self, model: type, condition: ColumnElement[bool]) -> int:
        """Count the rows of model that satisfy condition."""
        return self.session.execute(select(func.count()).select_from(model).where(condition)).scalar_one()
