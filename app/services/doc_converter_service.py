import subprocess
import os
from pathlib import Path


def convert_doc_to_docx(input_path: str) -> str:
    """
    Convert .doc -> .docx using LibreOffice headless
    """

    input_file = Path(input_path)

    if input_file.suffix.lower() != ".doc":
        return input_path

    output_dir = input_file.parent

    command = [
        "soffice",
        "--headless",
        "--convert-to",
        "docx",
        str(input_file),
        "--outdir",
        str(output_dir),
    ]

    subprocess.run(command, check=True)

    output_file = input_file.with_suffix(".docx")

    if not output_file.exists():
        raise RuntimeError("Convert DOC -> DOCX thất bại")

    return str(output_file)