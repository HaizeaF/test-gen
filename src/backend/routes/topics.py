"""Topic endpoints."""

from fastapi import APIRouter, status

from src.backend.routes.dependencies import TopicServiceDep
from src.backend.schemas.topic import TopicCreate, TopicRead, TopicUpdate

router = APIRouter(prefix="/topics", tags=["topics"])


@router.post("", response_model=TopicRead, status_code=status.HTTP_201_CREATED)
def create_topic(topic_create: TopicCreate, service: TopicServiceDep) -> TopicRead:
    """Create a topic."""
    return service.create(topic_create)


@router.get("", response_model=list[TopicRead])
def list_topics(service: TopicServiceDep) -> list[TopicRead]:
    """List every topic."""
    return service.get_all()


@router.patch("/{topic_id}", response_model=TopicRead)
def update_topic(topic_id: int, topic_update: TopicUpdate, service: TopicServiceDep) -> TopicRead:
    """Update a topic."""
    return service.update(topic_id, topic_update)


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(topic_id: int, service: TopicServiceDep) -> None:
    """Delete a topic."""
    service.delete(topic_id)
