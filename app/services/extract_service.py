from pathlib import Path

import fitz
import pytesseract
from PIL import Image
from docx import Document as DocxDocument


def extract_text_from_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang="vie+eng")
    return text.strip()


def extract_text_from_pdf_direct(file_path: str) -> str:
    doc = fitz.open(file_path)
    texts = []

    for page in doc:
        page_text = page.get_text("text")
        if page_text:
            texts.append(page_text)

    doc.close()
    return "\n".join(texts).strip()


def extract_text_from_pdf_ocr(file_path: str) -> str:
    doc = fitz.open(file_path)
    page_texts = []

    for page in doc:
        pix = page.get_pixmap()
        image_path = f"/tmp/{page.number}_temp_page.png"
        pix.save(image_path)

        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang="vie+eng")
        page_texts.append(text.strip())

        Path(image_path).unlink(missing_ok=True)

    doc.close()
    return "\n".join(page_texts).strip()


def extract_text_from_pdf(file_path: str) -> str:
    direct_text = extract_text_from_pdf_direct(file_path)

    if len(direct_text) >= 50:
        return direct_text

    return extract_text_from_pdf_ocr(file_path)


def extract_text_by_file_type(file_path: str, file_type: str) -> str:
    file_type = file_type.lower()

    if file_type == "docx":
        return extract_text_from_docx(file_path)

    if file_type == "pdf":
        return extract_text_from_pdf(file_path)

    if file_type in {"png", "jpg", "jpeg"}:
        return extract_text_from_image(file_path)

    raise ValueError(f"Không hỗ trợ xử lý file_type={file_type}")