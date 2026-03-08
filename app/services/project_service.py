from uuid import UUID
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project_schema import ProjectCreate


def create_project(db: Session, payload: ProjectCreate) -> Project:
    project = Project(
        code=payload.code,
        name=payload.name,
        investor_name=payload.investor_name,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_project_by_id(db: Session, project_id: str) -> Project | None:
    try:
        project_uuid = UUID(project_id)
    except ValueError:
        return None

    return db.query(Project).filter(Project.id == project_uuid).first()