from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.document_service import (
    get_document_by_id,
    save_validation_result,
)
from app.services.validation_service import validate_parsed_data

router = APIRouter(tags=["Validation"])


@router.post("/documents/{document_id}/validate")
def validate_document_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    if not document.parsed_data:
        raise HTTPException(
            status_code=400,
            detail="Document chưa có parsed_data. Hãy chạy parse trước."
        )

    try:
        validation_result = validate_parsed_data(
            document_type=document.document_type,
            parsed_data=document.parsed_data,
        )

        updated_document = save_validation_result(
            db=db,
            document=document,
            validation_result=validation_result,
        )

        return {
            "document_id": str(updated_document.id),
            "document_type": updated_document.document_type,
            "status": updated_document.status,
            "validated_at": updated_document.validated_at,
            "validation_result": updated_document.validation_result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{document_id}/validation-result")
def get_validation_result_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    return {
        "document_id": str(document.id),
        "document_type": document.document_type,
        "status": document.status,
        "validated_at": document.validated_at,
        "validation_result": document.validation_result,
    }