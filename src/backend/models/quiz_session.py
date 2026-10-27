"""Quiz session ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base, utcnow

if TYPE_CHECKING:
    from src.backend.models.answer import Answer


class QuizSession(Base):
    """One test taken by the user, from start to finish."""

    __tablename__ = "quiz_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    duration_seconds: Mapped[float | None]
    mode: Mapped[str] = mapped_column(String(30))
    num_questions: Mapped[int] = mapped_column(default=0)
    num_correct: Mapped[int] = mapped_column(default=0)

    answers: Mapped[list[Answer]] = relationship(back_populates="session", cascade="all, delete-orphan", passive_deletes=True)
