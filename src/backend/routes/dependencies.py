"""FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.backend.db.database import get_session
from src.backend.services.question_service import QuestionService
from src.backend.services.section_service import SectionService
from src.backend.services.topic_service import TopicService

SessionDep = Annotated[Session, Depends(get_session)]


def get_topic_service(session: SessionDep) -> TopicService:
    return TopicService(session)


def get_section_service(session: SessionDep) -> SectionService:
    return SectionService(session)


def get_question_service(session: SessionDep) -> QuestionService:
    return QuestionService(session)


TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
SectionServiceDep = Annotated[SectionService, Depends(get_section_service)]
QuestionServiceDep = Annotated[QuestionService, Depends(get_question_service)]