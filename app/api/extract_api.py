from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.document_service import (
    get_document_by_id,
    update_document_status,
    save_extracted_text,
    save_extract_error,
)
from app.services.extract_service import extract_text_by_file_type

router = APIRouter(tags=["Extract Text"])


@router.post("/documents/{document_id}/extract-text")
def extract_text_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    if not document.file_path:
        raise HTTPException(status_code=400, detail="Document không có file_path")

    update_document_status(db, document, "extracting_text")

    try:
        extracted_text = extract_text_by_file_type(
            file_path=document.file_path,
            file_type=document.file_type or "",
        )

        updated_document = save_extracted_text(
            db=db,
            document=document,
            ocr_text=extracted_text,
            status="text_extracted",
        )

        preview = extracted_text[:500] if extracted_text else ""

        return {
            "document_id": str(updated_document.id),
            "status": updated_document.status,
            "text_length": len(extracted_text or ""),
            "preview_text": preview,
            "processed_at": updated_document.processed_at,
            "error_message": updated_document.error_message,
        }

    except Exception as e:
        updated_document = save_extract_error(db, document, str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "document_id": str(updated_document.id),
                "status": updated_document.status,
                "error_message": updated_document.error_message,
            },
        )


@router.get("/documents/{document_id}/text")
def get_document_text_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    return {
        "document_id": str(document.id),
        "file_name": document.file_name,
        "document_type": document.document_type,
        "status": document.status,
        "ocr_text": document.ocr_text,
        "error_message": document.error_message,
        "processed_at": document.processed_at,
    }