from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.project import Project


def create_project(db: Session, payload) -> Project:
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


def save_project_validation_result(db: Session, project: Project, validation_result: dict) -> Project:
    project.validation_result = validation_result
    project.validated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(project)
    return project