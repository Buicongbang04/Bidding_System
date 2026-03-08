from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project_schema import ProjectCreate
from app.services.project_service import create_project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("")
def create_project_api(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = create_project(db, payload)
    return {
        "id": str(project.id),
        "code": project.code,
        "name": project.name,
        "investor_name": project.investor_name,
        "created_at": project.created_at,
    }