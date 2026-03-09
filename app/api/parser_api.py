from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.document_service import (
    get_document_by_id,
    save_parsed_data,
    save_parse_error,
)
from app.services.parser_dispatcher_service import parse_document_by_type

router = APIRouter(tags=["Parser"])


@router.post("/documents/{document_id}/parse")
def parse_document_api(document_id: str, db: Session = Depends(get_db)):
    document = get_document_by_id(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Không tìm thấy document")

    if not document.ocr_text:
        raise HTTPException(
            status_code=400,
            detail="Document chưa có text. Hãy chạy extract-text trước."
        )

    try:
        parsed = parse_document_by_type(
            document_type=document.document_type,
            ocr_text=document.ocr_text,
        )

        updated_document = save_parsed_data(
            db=db,
            document=document,
            parsed_data=parsed,
        )

        return {
            "document_id": str(updated_document.id),
            "status": updated_document.status,
            "document_type": updated_document.document_type,
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
                "document_type": updated_document.document_type,
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
        "document_type": document.document_type,
        "status": document.status,
        "parsed_at": document.parsed_at,
        "parse_error_message": document.parse_error_message,
        "parsed_data": document.parsed_data,
    }