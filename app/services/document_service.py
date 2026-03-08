from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    project_id: str,
    file_name: str,
    stored_file_name: str,
    file_path: str,
    file_type: str | None,
    mime_type: str | None,
    document_type: str,
    status: str = "uploaded",
) -> Document:
    document = Document(
        project_id=UUID(project_id),
        file_name=file_name,
        stored_file_name=stored_file_name,
        file_path=file_path,
        file_type=file_type,
        mime_type=mime_type,
        document_type=document_type,
        status=status,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_document_by_id(db: Session, document_id: str) -> Document | None:
    try:
        document_uuid = UUID(document_id)
    except ValueError:
        return None

    return db.query(Document).filter(Document.id == document_uuid).first()


def list_documents_by_project(db: Session, project_id: str) -> list[Document]:
    project_uuid = UUID(project_id)
    return (
        db.query(Document)
        .filter(Document.project_id == project_uuid)
        .order_by(Document.uploaded_at.desc())
        .all()
    )


def update_document_status(
    db: Session,
    document: Document,
    status: str,
    error_message: str | None = None,
) -> Document:
    document.status = status
    document.error_message = error_message
    db.commit()
    db.refresh(document)
    return document


def save_extracted_text(
    db: Session,
    document: Document,
    ocr_text: str,
    status: str = "ocr_done",
) -> Document:
    document.ocr_text = ocr_text
    document.status = status
    document.error_message = None
    document.processed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(document)
    return document


def save_extract_error(
    db: Session,
    document: Document,
    error_message: str,
) -> Document:
    document.status = "error"
    document.error_message = error_message
    document.processed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(document)
    return document


def save_parsed_data(
    db: Session,
    document: Document,
    parsed_data: dict,
) -> Document:
    document.parsed_data = parsed_data
    document.parse_error_message = None
    document.parsed_at = datetime.now(timezone.utc)
    document.status = "parsed"
    db.commit()
    db.refresh(document)
    return document


def save_parse_error(
    db: Session,
    document: Document,
    error_message: str,
) -> Document:
    document.parse_error_message = error_message
    document.parsed_at = datetime.now(timezone.utc)
    document.status = "error"
    db.commit()
    db.refresh(document)
    return document