import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(100), nullable=True)
    name = Column(Text, nullable=False)
    investor_name = Column(Text, nullable=True)

    validation_result = Column(JSONB, nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship(
        "Document",
        back_populates="project",
        cascade="all, delete-orphan"
    )