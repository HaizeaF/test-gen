"""Question ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base, utcnow

if TYPE_CHECKING:
    from src.backend.models.answer import Answer
    from src.backend.models.section import Section


class Question(Base):
    """Multiple-choice question with four options and a single correct answer."""

    __table_args__ = (CheckConstraint("correct_option IN ('a', 'b', 'c', 'd')", name="correct_option_valid"),)

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id", ondelete="RESTRICT"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(Text, nullable=False)
    option_b: Mapped[str] = mapped_column(Text, nullable=False)
    option_c: Mapped[str] = mapped_column(Text, nullable=False)
    option_d: Mapped[str] = mapped_column(Text, nullable=False)
    correct_option: Mapped[str] = mapped_column(String(1), nullable=False)  # 'a', 'b', 'c' or 'd'
    flagged: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    section: Mapped[Section] = relationship(back_populates="questions")
    answers: Mapped[list[Answer]] = relationship(back_populates="question", passive_deletes="all")
