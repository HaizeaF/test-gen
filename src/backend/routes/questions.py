"""Question endpoints."""

from fastapi import APIRouter, status

from src.backend.routes.dependencies import QuestionServiceDep
from src.backend.schemas.question import QuestionCreate, QuestionRead, QuestionUpdate

router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("", response_model=QuestionRead)
def create_question(question_create: QuestionCreate, service: QuestionServiceDep) -> QuestionRead:
    return service.create(question_create)

@router.get("", response_model=list[QuestionRead])
def list_questions(service: QuestionServiceDep) -> list[QuestionRead]:
    return service.get_all()

@router.patch("/{question_id}", response_model=QuestionRead)
def update_question(question_id: int, question_update: QuestionUpdate, service: QuestionServiceDep) -> QuestionRead:
    return service.update(question_id, question_update)

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, service: QuestionServiceDep) -> None:
    service.delete(question_id)