from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.api.v1.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.db.session import get_db
from app.exceptions import EntityNotFoundException
from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with name and description. Maximum 10 projects allowed.",
)
def create_project(
    project: ProjectCreate, service: ProjectService = Depends(get_project_service)
):
    success, message = service.create_project(project.name, project.description)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    created_project = service.project_repository.get_by_name(project.name)
    return created_project


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="List all projects",
    description="Retrieve a list of all projects.",
)
def list_projects(service: ProjectService = Depends(get_project_service)):
    projects = service.get_all_projects()
    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID",
    description="Retrieve a specific project by its ID.",
)
def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    try:
        project = service.get_project_by_id(project_id)
        return project
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project and all its associated tasks.",
)
def delete_project(
    project_id: int, service: ProjectService = Depends(get_project_service)
):
    success, message = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
