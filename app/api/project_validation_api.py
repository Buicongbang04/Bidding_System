from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.project_service import get_project_by_id, save_project_validation_result
from app.services.document_service import list_documents_by_project
from app.services.project_validation_service import validate_project_documents

router = APIRouter(tags=["Project Validation"])


@router.post("/projects/{project_id}/validate")
def validate_project_api(project_id: str, db: Session = Depends(get_db)):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy project")

    documents = list_documents_by_project(db, project_id)

    if not documents:
        raise HTTPException(status_code=400, detail="Project chưa có document nào")

    validation_result = validate_project_documents(
        project_id=project_id,
        documents=documents,
    )

    updated_project = save_project_validation_result(
        db=db,
        project=project,
        validation_result=validation_result,
    )

    return {
        "project_id": str(updated_project.id),
        "validated_at": updated_project.validated_at,
        "validation_result": updated_project.validation_result,
    }


@router.get("/projects/{project_id}/validation-result")
def get_project_validation_result_api(project_id: str, db: Session = Depends(get_db)):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy project")

    return {
        "project_id": str(project.id),
        "validated_at": project.validated_at,
        "validation_result": project.validation_result,
    }