import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)

    file_name = Column(Text, nullable=False)
    stored_file_name = Column(Text, nullable=False)
    file_path = Column(Text, nullable=False)
    file_type = Column(String(20), nullable=True)
    mime_type = Column(String(100), nullable=True)

    document_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="uploaded")

    ocr_text = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)

    parsed_data = Column(JSONB, nullable=True)
    parsed_at = Column(DateTime(timezone=True), nullable=True)
    parse_error_message = Column(Text, nullable=True)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="documents")