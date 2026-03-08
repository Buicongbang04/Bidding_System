import re
from typing import Any


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_non_empty_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def extract_document_number(text: str) -> str | None:
    patterns = [
        r"(?:Số|SO|SỐ)\s*[:：]?\s*([^\n]+)",
        r"(?:Số\s*văn\s*bản)\s*[:：]?\s*([^\n]+)",
        r"(?:Quyết định\s*số)\s*[:：]?\s*([^\n]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .;-")
    return None


def extract_issued_date(text: str) -> str | None:
    patterns = [
        r"ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{4})",
        r"(\d{1,2}-\d{1,2}-\d{4})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            if len(match.groups()) == 3:
                day, month, year = match.groups()
                return f"{int(day):02d}/{int(month):02d}/{year}"
            return match.group(1)
    return None


def extract_legal_bases(lines: list[str]) -> list[str]:
    legal_bases = []

    for line in lines:
        lower_line = line.lower()
        if lower_line.startswith("căn cứ"):
            legal_bases.append(line)

    return legal_bases[:10]


def extract_signer(lines: list[str]) -> str | None:
    signer_patterns = [
        r"(?:Người ký|NGƯỜI KÝ)\s*[:：]?\s*(.+)",
        r"(?:Ký bởi|Ký tên)\s*[:：]?\s*(.+)",
    ]

    full_text = "\n".join(lines)
    for pattern in signer_patterns:
        match = re.search(pattern, full_text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()

    title_keywords = [
        "chủ tịch",
        "phó chủ tịch",
        "giám đốc",
        "phó giám đốc",
        "thủ trưởng",
        "bộ trưởng",
        "trưởng phòng",
        "phó trưởng phòng",
    ]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in title_keywords):
            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()
                if 2 <= len(candidate) <= 100:
                    return candidate

    for line in reversed(lines[-8:]):
        if re.fullmatch(r"[A-ZÀÁẠẢÃĂẮẰẶẲẴÂẤẦẬẨẪĐÈÉẸẺẼÊẾỀỆỂỄÌÍỊỈĨÒÓỌỎÕÔỐỒỘỔỖƠỚỜỢỞỠÙÚỤỦŨƯỨỪỰỬỮỲÝỴỶỸ\s]+", line):
            cleaned = line.strip()
            if len(cleaned.split()) >= 2:
                return cleaned.title()

    return None


def infer_document_kind(text: str, document_type: str | None = None) -> str | None:
    text_lower = text.lower()

    if document_type and document_type != "KHAC":
        return document_type

    rules = [
        ("KE_HOACH_LUA_CHON_NHA_THAU", ["kế hoạch lựa chọn nhà thầu"]),
        ("QUYET_DINH_PHE_DUYET_KET_QUA", ["phê duyệt kết quả lựa chọn nhà thầu"]),
        ("HO_SO_MOI_THAU", ["hồ sơ mời thầu"]),
        ("BAO_CAO_THAM_DINH", ["báo cáo thẩm định"]),
        ("THONG_BAO_MOI_THAU", ["thông báo mời thầu"]),
        ("QUYET_DINH_PHE_DUYET_DU_AN", ["quyết định phê duyệt dự án"]),
    ]

    for doc_kind, keywords in rules:
        if any(keyword in text_lower for keyword in keywords):
            return doc_kind

    return "KHAC"


def extract_summary(lines: list[str]) -> str | None:
    ignore_prefixes = ("cộng hòa", "độc lập", "số", "căn cứ")

    summary_candidates = []
    for line in lines:
        lower_line = line.lower()
        if any(lower_line.startswith(prefix) for prefix in ignore_prefixes):
            continue

        if len(line) < 10:
            continue

        summary_candidates.append(line)
        if len(summary_candidates) >= 3:
            break

    if not summary_candidates:
        return None

    return " ".join(summary_candidates)


def extract_issuing_authority(lines: list[str]) -> str | None:
    first_lines = lines[:8]
    for line in first_lines:
        if len(line) > 5 and len(line) < 150:
            upper_ratio = sum(1 for c in line if c.isupper()) / max(len([c for c in line if c.isalpha()]), 1)
            if upper_ratio > 0.5:
                return line
    return None


def compute_missing_fields(parsed_data: dict[str, Any]) -> list[str]:
    required_fields = [
        "document_number",
        "issued_date",
        "signer",
        "legal_bases",
        "summary",
    ]

    missing = []
    for field in required_fields:
        value = parsed_data.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, list) and len(value) == 0:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)

    return missing


def compute_confidence(parsed_data: dict[str, Any]) -> float:
    fields = [
        parsed_data.get("document_number"),
        parsed_data.get("issued_date"),
        parsed_data.get("signer"),
        parsed_data.get("summary"),
    ]
    legal_bases = parsed_data.get("legal_bases") or []

    score = 0
    for field in fields:
        if field:
            score += 1

    if legal_bases:
        score += 1

    return round(score / 5, 2)


def parse_document_structure(ocr_text: str, document_type: str | None = None) -> dict[str, Any]:
    text = normalize_text(ocr_text)
    lines = split_non_empty_lines(text)

    if not text:
        raise ValueError("ocr_text rỗng, không thể parse cấu trúc văn bản")

    parsed_data = {
        "document_kind": infer_document_kind(text, document_type),
        "document_number": extract_document_number(text),
        "issued_date": extract_issued_date(text),
        "issuing_authority": extract_issuing_authority(lines),
        "signer": extract_signer(lines),
        "legal_bases": extract_legal_bases(lines),
        "summary": extract_summary(lines),
        "preview_lines": lines[:15],
    }

    parsed_data["missing_fields"] = compute_missing_fields(parsed_data)
    parsed_data["confidence_score"] = compute_confidence(parsed_data)

    return parsed_data