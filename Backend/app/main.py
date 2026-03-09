from fastapi import FastAPI
from sqlalchemy import text

from app.db.base import Base
from app.db.session import engine

from app.models.project import Project
from app.models.document import Document

from app.api.project_api import router as project_router
from app.api.document_api import router as document_router
from app.api.extract_api import router as extract_router
from app.api.parser_api import router as parser_router
from app.api.validation_api import router as validation_router
from app.api.project_validation_api import router as project_validation_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def ensure_extra_columns():
    statements = [
        """
        ALTER TABLE documents
        ADD COLUMN IF NOT EXISTS parsed_data JSONB NULL;
        """,
        """
        ALTER TABLE documents
        ADD COLUMN IF NOT EXISTS parsed_at TIMESTAMPTZ NULL;
        """,
        """
        ALTER TABLE documents
        ADD COLUMN IF NOT EXISTS parse_error_message TEXT NULL;
        """,
        """
        ALTER TABLE documents
        ADD COLUMN IF NOT EXISTS validation_result JSONB NULL;
        """,
        """
        ALTER TABLE documents
        ADD COLUMN IF NOT EXISTS validated_at TIMESTAMPTZ NULL;
        """,
        """
        ALTER TABLE projects
        ADD COLUMN IF NOT EXISTS validation_result JSONB NULL;
        """,
        """
        ALTER TABLE projects
        ADD COLUMN IF NOT EXISTS validated_at TIMESTAMPTZ NULL;
        """,
    ]

    with engine.begin() as connection:
        for stmt in statements:
            connection.execute(text(stmt))


app = FastAPI(
    title="Tender AI MVP",
    description="Upload hồ sơ, extract text, parse, validate document và cross validate project",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_tables()
    ensure_extra_columns()


app.include_router(project_router)
app.include_router(document_router)
app.include_router(extract_router)
app.include_router(parser_router)
app.include_router(validation_router)
app.include_router(project_validation_router)


@app.get("/")
def health_check():
    return {"message": "Tender AI MVP is running"}