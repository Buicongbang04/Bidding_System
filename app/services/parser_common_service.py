import re


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


def extract_title(lines: list[str]) -> str | None:
    for line in lines[:12]:
        cleaned = line.strip()
        if len(cleaned) >= 10 and cleaned.upper() == cleaned:
            if not cleaned.lower().startswith(("cộng hòa", "độc lập", "số")):
                return cleaned
    return None


def extract_issuing_authority(lines: list[str]) -> str | None:
    for line in lines[:8]:
        cleaned = line.strip()
        if 5 <= len(cleaned) <= 150:
            alpha_chars = [c for c in cleaned if c.isalpha()]
            if not alpha_chars:
                continue
            upper_ratio = sum(1 for c in alpha_chars if c.isupper()) / len(alpha_chars)
            if upper_ratio > 0.6:
                return cleaned
    return None


def extract_legal_bases(lines: list[str]) -> list[str]:
    results = []
    for line in lines:
        if line.lower().startswith("căn cứ"):
            results.append(line)
    return results[:20]


def extract_signer(lines: list[str]) -> str | None:
    title_keywords = [
        "chủ tịch",
        "phó chủ tịch",
        "giám đốc",
        "phó giám đốc",
        "trưởng phòng",
        "phó trưởng phòng",
        "thủ trưởng",
        "bộ trưởng",
    ]

    for i, line in enumerate(lines):
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in title_keywords):
            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()
                if 2 <= len(candidate) <= 100:
                    return candidate.title()

    return None


def extract_text_after_label(text: str, labels: list[str]) -> str | None:
    for label in labels:
        pattern = rf"{label}\s*[:：]?\s*([^\n]+)"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .;")
    return None


def extract_section_content(text: str, section_label: str, next_labels: list[str] | None = None) -> str | None:
    next_labels = next_labels or []
    escaped_next = "|".join(re.escape(label) for label in next_labels)

    if escaped_next:
        pattern = rf"({re.escape(section_label)}.*?)(?={escaped_next}|$)"
    else:
        pattern = rf"({re.escape(section_label)}.*)$"

    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def build_base_schema(document_type: str, text: str) -> dict:
    lines = split_non_empty_lines(text)

    return {
        "document_type": document_type,
        "document_number": extract_document_number(text),
        "issued_date": extract_issued_date(text),
        "issuing_authority": extract_issuing_authority(lines),
        "signer": extract_signer(lines),
        "title": extract_title(lines),
        "legal_bases": extract_legal_bases(lines),
        "raw_text_preview": text[:1000],
    }