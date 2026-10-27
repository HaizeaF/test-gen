"""Answer ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.backend.models.base import Base, utcnow

if TYPE_CHECKING:
    from src.backend.models.question import Question
    from src.backend.models.quiz_session import QuizSession


class Answer(Base):
    """One attempt at one question within a session."""

    __tablename__ = "answers"
    # Speed up per question and per date aggregations used by the analytics
    __table_args__ = (
        CheckConstraint("selected_option IS NULL OR selected_option IN ('a', 'b', 'c', 'd')", name="selected_option_valid"),
        Index("ix_answers_session_id", "session_id"),
        Index("ix_answers_question_id", "question_id"),
        Index("ix_answers_answered_at", "answered_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("quiz_sessions.id", ondelete="CASCADE"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="RESTRICT"))
    selected_option: Mapped[str | None] = mapped_column(String(1))
    is_correct: Mapped[bool]
    time_spent_seconds: Mapped[float]
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    session: Mapped[QuizSession] = relationship(back_populates="answers")
    question: Mapped[Question] = relationship(back_populates="answers")
