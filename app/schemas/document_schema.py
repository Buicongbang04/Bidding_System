from pydantic import BaseModel
from datetime import datetime
from typing import Any


class DocumentResponse(BaseModel):
    id: str
    project_id: str
    file_name: str
    stored_file_name: str
    file_path: str
    file_type: str | None = None
    mime_type: str | None = None
    document_type: str
    status: str
    ocr_text: str | None = None
    error_message: str | None = None
    processed_at: datetime | None = None
    parsed_data: dict[str, Any] | None = None
    parsed_at: datetime | None = None
    parse_error_message: str | None = None
    uploaded_at: datetime


class ExtractTextResponse(BaseModel):
    document_id: str
    status: str
    text_length: int
    preview_text: str | None = None
    processed_at: datetime | None = None
    error_message: str | None = None


class DocumentTextResponse(BaseModel):
    document_id: str
    file_name: str
    status: str
    ocr_text: str | None = None
    error_message: str | None = None
    processed_at: datetime | None = None


class ParseStructureResponse(BaseModel):
    document_id: str
    status: str
    parsed_at: datetime | None = None
    parse_error_message: str | None = None
    parsed_data: dict[str, Any] | None = None