"""Section endpoints."""

from fastapi import APIRouter, status

from src.backend.routes.dependencies import SectionServiceDep
from src.backend.schemas.section import SectionCreate, SectionRead, SectionUpdate

router = APIRouter(prefix="/sections", tags=["sections"])

@router.post("", response_model=SectionRead)
def create_section(section_create: SectionCreate, service: SectionServiceDep) -> SectionRead:
    return service.create(section_create)

@router.get("", response_model=list[SectionRead])
def list_sections(service: SectionServiceDep) -> list[SectionRead]:
    return service.get_all()

@router.patch("/{section_id}", response_model=SectionRead)
def update_section(section_id: int, section_update: SectionUpdate, service: SectionServiceDep) -> SectionRead:
    return service.update(section_id, section_update)

@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_section(section_id: int, service: SectionServiceDep) -> None:
    service.delete(section_id)