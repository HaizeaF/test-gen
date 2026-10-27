"""Topic ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base

if TYPE_CHECKING:
    from src.backend.models.section import Section


class Topic(Base):
    """Top-level study subject. Groups several sections."""

    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    sections: Mapped[list[Section]] = relationship(back_populates="topic", passive_deletes="all")
