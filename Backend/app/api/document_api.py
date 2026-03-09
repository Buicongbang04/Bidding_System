from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.project_service import get_project_by_id
from app.services.document_service import create_document, list_documents_by_project
from app.services.storage_service import (
    validate_extension,
    validate_file_size,
    validate_document_type,
    save_upload_file,
)

router = APIRouter(tags=["Documents"])


@router.post("/documents/upload")
async def upload_document_api(
    project_id: str = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy project")

    try:
        validate_document_type(document_type)
        validate_extension(file.filename)
        await validate_file_size(file)

        saved = await save_upload_file(file, project_id)

        document = create_document(
            db=db,
            project_id=project_id,
            file_name=file.filename,
            stored_file_name=saved["stored_file_name"],
            file_path=saved["file_path"],
            file_type=saved["file_type"],
            mime_type=saved["mime_type"],
            document_type=document_type,
            status="uploaded",
        )

        return {
            "id": str(document.id),
            "project_id": str(document.project_id),
            "file_name": document.file_name,
            "stored_file_name": document.stored_file_name,
            "file_path": document.file_path,
            "file_type": document.file_type,
            "mime_type": document.mime_type,
            "document_type": document.document_type,
            "status": document.status,
            "ocr_text": document.ocr_text,
            "error_message": document.error_message,
            "processed_at": document.processed_at,
            "parsed_data": document.parsed_data,
            "parsed_at": document.parsed_at,
            "parse_error_message": document.parse_error_message,
            "validation_result": document.validation_result,
            "validated_at": document.validated_at,
            "uploaded_at": document.uploaded_at,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/documents")
def list_documents_api(project_id: str, db: Session = Depends(get_db)):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy project")

    documents = list_documents_by_project(db, project_id)
    return [
        {
            "id": str(doc.id),
            "project_id": str(doc.project_id),
            "file_name": doc.file_name,
            "stored_file_name": doc.stored_file_name,
            "file_path": doc.file_path,
            "file_type": doc.file_type,
            "mime_type": doc.mime_type,
            "document_type": doc.document_type,
            "status": doc.status,
            "ocr_text": doc.ocr_text,
            "error_message": doc.error_message,
            "processed_at": doc.processed_at,
            "parsed_data": doc.parsed_data,
            "parsed_at": doc.parsed_at,
            "parse_error_message": doc.parse_error_message,
            "validation_result": doc.validation_result,
            "validated_at": doc.validated_at,
            "uploaded_at": doc.uploaded_at,
        }
        for doc in documents
    ]