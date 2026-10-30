"""Helpers shared by the services."""

from src.backend.services.errors import NotFoundError, ConflictError
from pydantic import BaseModel
from sqlalchemy import ColumnElement, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def get[T](session: Session, model: type[T], object_id: int) -> T:
    """Return the row with this id, or raise NotFoundError naming what is missing."""
    obj = session.get(model, object_id)
    if obj is None:
        raise NotFoundError(f"{model.__name__} {object_id} not found")
    return obj


def commit(session: Session, message: str) -> None:
    """Commit. If the database refuses (unique or foreign key), roll back."""
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ConflictError(message)


def count_rows(session: Session, model: type, condition: ColumnElement[bool]) -> int:
    """Count the rows of model that satisfy condition."""
    return session.execute(select(func.count()).select_from(model).where(condition)).scalar_one()


def apply_updates(obj: object, data: BaseModel) -> None:
    """Copy the fields the client sent onto obj."""
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(obj, field, value)