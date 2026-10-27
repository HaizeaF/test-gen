"""Section ORM model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base

if TYPE_CHECKING:
    from src.backend.models.question import Question
    from src.backend.models.topic import Topic


class Section(Base):
    """Subdivision of a topic. Groups several questions."""

    __tablename__ = "sections"
    __table_args__ = (UniqueConstraint("topic_id", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="RESTRICT"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    topic: Mapped[Topic] = relationship(back_populates="sections")
    questions: Mapped[list[Question]] = relationship(back_populates="section", passive_deletes="all")
