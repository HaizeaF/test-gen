"""Question endpoints."""

from fastapi import APIRouter, status

from src.backend.routes.dependencies import QuestionServiceDep
from src.backend.schemas.question import QuestionCreate, QuestionRead, QuestionUpdate

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(question_create: QuestionCreate, service: QuestionServiceDep) -> QuestionRead:
    """Create a question."""
    return service.create(question_create)


@router.get("", response_model=list[QuestionRead])
def list_questions(service: QuestionServiceDep) -> list[QuestionRead]:
    """List every question, flagged ones first."""
    return service.get_all()


@router.patch("/{question_id}", response_model=QuestionRead)
def update_question(question_id: int, question_update: QuestionUpdate, service: QuestionServiceDep) -> QuestionRead:
    """Update a question, including moving it, flagging it or deactivating it."""
    return service.update(question_id, question_update)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, service: QuestionServiceDep) -> None:
    """Delete a question."""
    service.delete(question_id)
