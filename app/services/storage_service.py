import os
import uuid
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg"
}

DOCUMENT_TYPES = {
    "KE_HOACH_LUA_CHON_NHA_THAU",
    "VAN_BAN_PHE_DUYET_NHA_THAU",
    "QUYET_DINH",
}


def ensure_upload_dir() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)


def get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def validate_extension(filename: str) -> None:
    ext = get_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Định dạng file không được hỗ trợ: {ext}")


async def validate_file_size(file: UploadFile) -> None:
    content = await file.read()
    size_in_mb = len(content) / (1024 * 1024)
    await file.seek(0)

    if size_in_mb > settings.max_file_size_mb:
        raise ValueError(f"File vượt quá dung lượng cho phép {settings.max_file_size_mb}MB")


def validate_document_type(document_type: str) -> None:
    if document_type not in DOCUMENT_TYPES:
        raise ValueError("document_type không hợp lệ")


async def save_upload_file(file: UploadFile, project_id: str) -> dict:
    ensure_upload_dir()

    ext = get_extension(file.filename)
    stored_file_name = f"{uuid.uuid4()}{ext}"

    project_dir = Path(settings.upload_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    file_path = project_dir / stored_file_name

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    await file.seek(0)

    return {
        "stored_file_name": stored_file_name,
        "file_path": str(file_path),
        "file_type": ext.replace(".", "").lower(),
        "mime_type": file.content_type,
    }