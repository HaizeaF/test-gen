"""FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.backend.db.database import get_session
from src.backend.repositories.unit_of_work import UnitOfWork
from src.backend.services.question_service import QuestionService
from src.backend.services.section_service import SectionService
from src.backend.services.topic_service import TopicService

SessionDep = Annotated[Session, Depends(get_session)]


def get_unit_of_work(session: SessionDep) -> UnitOfWork:
    """Build the unit of work of the request on top of its database session."""
    return UnitOfWork(session)


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]


def get_topic_service(uow: UnitOfWorkDep) -> TopicService:
    return TopicService(uow)


def get_section_service(uow: UnitOfWorkDep) -> SectionService:
    return SectionService(uow)


def get_question_service(uow: UnitOfWorkDep) -> QuestionService:
    return QuestionService(uow)


TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
SectionServiceDep = Annotated[SectionService, Depends(get_section_service)]
QuestionServiceDep = Annotated[QuestionService, Depends(get_question_service)]
