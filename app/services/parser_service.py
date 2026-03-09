import re


def normalize_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_document_number(text: str):
    patterns = [
        r"Số\s*[:：]?\s*([^\n]+)",
        r"Quyết định\s*số\s*([^\n]+)"
    ]

    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    return None


def extract_date(text: str):

    patterns = [
        r"ngày\s*(\d{1,2})\s*tháng\s*(\d{1,2})\s*năm\s*(\d{4})",
        r"(\d{1,2}/\d{1,2}/\d{4})"
    ]

    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            if len(m.groups()) == 3:
                d, mth, y = m.groups()
                return f"{d}/{mth}/{y}"
            return m.group(1)

    return None


def extract_title(lines):

    for line in lines[:10]:

        if len(line) > 10 and line.isupper():
            return line

    return None


def extract_signer(lines):

    keywords = [
        "chủ tịch",
        "giám đốc",
        "trưởng phòng",
        "phó chủ tịch"
    ]

    for i, line in enumerate(lines):

        lower = line.lower()

        if any(k in lower for k in keywords):

            if i + 1 < len(lines):

                return lines[i + 1]

    return None


def extract_legal_bases(lines):

    bases = []

    for line in lines:

        if line.lower().startswith("căn cứ"):

            bases.append(line)

    return bases


def classify_document(text: str):

    text = text.lower()

    rules = {
        "KE_HOACH_LUA_CHON_NHA_THAU": [
            "kế hoạch lựa chọn nhà thầu"
        ],
        "HO_SO_MOI_THAU": [
            "hồ sơ mời thầu"
        ],
        "BAO_CAO_THAM_DINH": [
            "báo cáo thẩm định"
        ],
        "QUYET_DINH": [
            "quyết định"
        ],
        "THONG_BAO": [
            "thông báo"
        ],
    }

    for doc_type, keywords in rules.items():

        for k in keywords:

            if k in text:
                return doc_type, 0.8

    return "KHAC", 0.3


def parse_specialized_fields(doc_type, text):

    fields = {}

    if doc_type == "KE_HOACH_LUA_CHON_NHA_THAU":

        m = re.search(r"giá gói thầu\s*[:：]?\s*([^\n]+)", text, re.IGNORECASE)

        if m:
            fields["package_price"] = m.group(1)

    return fields


def parse_document(ocr_text):

    text = normalize_text(ocr_text)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    document_number = extract_document_number(text)
    issued_date = extract_date(text)
    signer = extract_signer(lines)
    title = extract_title(lines)
    legal_bases = extract_legal_bases(lines)

    doc_type, confidence = classify_document(text)

    specialized = parse_specialized_fields(doc_type, text)

    parsed = {
        "classification": {
            "document_type": doc_type,
            "confidence": confidence
        },
        "general_fields": {
            "document_number": document_number,
            "issued_date": issued_date,
            "title": title,
            "signer": signer
        },
        "specialized_fields": specialized,
        "legal_bases": legal_bases
    }

    return parsed