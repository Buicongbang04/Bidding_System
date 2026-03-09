from pathlib import Path
import tempfile
import re

import fitz
import pytesseract
from PIL import Image
from docx import Document as DocxDocument

from app.services.doc_converter_service import convert_doc_to_docx


OCR_LANG = "vie+eng"
PDF_DIRECT_TEXT_MIN_LENGTH = 50


def normalize_extracted_text(text: str) -> str:
    """
    Chuẩn hóa text sau khi extract/OCR để parser phía sau ổn định hơn.
    """
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def ensure_file_exists(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    return path


def extract_text_from_docx(file_path: str) -> str:
    """
    Trích text từ file .docx bằng python-docx
    """
    ensure_file_exists(file_path)

    doc = DocxDocument(file_path)
    paragraphs: list[str] = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)

    return normalize_extracted_text("\n".join(paragraphs))


def extract_text_from_doc(file_path: str) -> str:
    """
    Convert .doc -> .docx rồi extract text
    """
    ensure_file_exists(file_path)

    converted_docx_path = convert_doc_to_docx(file_path)
    return extract_text_from_docx(converted_docx_path)


def extract_text_from_image(file_path: str) -> str:
    """
    OCR ảnh bằng Tesseract
    """
    ensure_file_exists(file_path)

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang=OCR_LANG)
    return normalize_extracted_text(text)


def extract_text_from_pdf_direct(file_path: str) -> str:
    """
    Trích text trực tiếp từ PDF text-based
    """
    ensure_file_exists(file_path)

    texts: list[str] = []
    doc = fitz.open(file_path)

    try:
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                texts.append(page_text)
    finally:
        doc.close()

    return normalize_extracted_text("\n".join(texts))


def extract_text_from_pdf_ocr(file_path: str) -> str:
    """
    OCR toàn bộ các trang PDF bằng cách render từng trang thành ảnh
    """
    ensure_file_exists(file_path)

    page_texts: list[str] = []
    doc = fitz.open(file_path)

    try:
        for page in doc:
            pix = page.get_pixmap()
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                temp_image_path = tmp.name

            try:
                pix.save(temp_image_path)
                image = Image.open(temp_image_path)
                text = pytesseract.image_to_string(image, lang=OCR_LANG)
                page_texts.append(text.strip())
            finally:
                Path(temp_image_path).unlink(missing_ok=True)
    finally:
        doc.close()

    return normalize_extracted_text("\n".join(page_texts))


def extract_text_from_pdf(file_path: str) -> str:
    """
    Ưu tiên extract text trực tiếp.
    Nếu text quá ít thì coi như PDF scan và fallback sang OCR.
    """
    direct_text = extract_text_from_pdf_direct(file_path)

    if len(direct_text) >= PDF_DIRECT_TEXT_MIN_LENGTH:
        return direct_text

    return extract_text_from_pdf_ocr(file_path)


def extract_text_by_file_type(file_path: str, file_type: str) -> str:
    """
    Dispatcher chính theo loại file.
    Hỗ trợ:
    - doc
    - docx
    - pdf
    - png
    - jpg
    - jpeg
    """
    if not file_type:
        raise ValueError("file_type rỗng")

    normalized_type = file_type.lower().strip()

    if normalized_type == "doc":
        return extract_text_from_doc(file_path)

    if normalized_type == "docx":
        return extract_text_from_docx(file_path)

    if normalized_type == "pdf":
        return extract_text_from_pdf(file_path)

    if normalized_type in {"png", "jpg", "jpeg"}:
        return extract_text_from_image(file_path)

    raise ValueError(f"File type không hỗ trợ: {file_type}")