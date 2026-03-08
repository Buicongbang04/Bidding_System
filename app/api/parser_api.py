from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.document_service import (
    get_document_by_id,
    update_document_status,
    save_parsed_data,
    save_parse_error,
)
from app.services.parser_service import parse_document_structure

router = APIRouter(tags=["Parser"])


@router.post("/documents/{document_id}/parse-structure")
def parse_document_structure_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    if not document.ocr_text:
        raise HTTPException(
            status_code=400,
            detail="Document chưa có ocr_text. Hãy chạy extract-text trước."
        )

    update_document_status(db, document, "parsing")

    try:
        parsed = parse_document_structure(
            ocr_text=document.ocr_text,
            document_type=document.document_type,
        )

        updated_document = save_parsed_data(
            db=db,
            document=document,
            parsed_data=parsed,
        )

        return {
            "document_id": str(updated_document.id),
            "status": updated_document.status,
            "parsed_at": updated_document.parsed_at,
            "parse_error_message": updated_document.parse_error_message,
            "parsed_data": updated_document.parsed_data,
        }

    except Exception as e:
        updated_document = save_parse_error(db, document, str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "document_id": str(updated_document.id),
                "status": updated_document.status,
                "parse_error_message": updated_document.parse_error_message,
            },
        )


@router.get("/documents/{document_id}/parsed")
def get_parsed_document_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    return {
        "document_id": str(document.id),
        "status": document.status,
        "parsed_at": document.parsed_at,
        "parse_error_message": document.parse_error_message,
        "parsed_data": document.parsed_data,
    }