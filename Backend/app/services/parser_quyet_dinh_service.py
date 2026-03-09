import re

from app.services.parser_common_service import (
    build_base_schema,
    extract_text_after_label,
    extract_section_content,
)


def extract_decision_subject(text: str) -> str | None:
    title_match = re.search(r"(QUYẾT ĐỊNH[^\n]*)", text, flags=re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    return extract_text_after_label(text, ["Về việc"])


def parse_quyet_dinh(text: str) -> dict:
    result = build_base_schema("QUYET_DINH", text)

    result.update({
        "decision_subject": extract_decision_subject(text),
        "article_1": extract_section_content(text, "Điều 1.", ["Điều 2.", "Điều 3.", "Nơi nhận:"]),
        "article_2": extract_section_content(text, "Điều 2.", ["Điều 3.", "Điều 4.", "Nơi nhận:"]),
        "article_3": extract_section_content(text, "Điều 3.", ["Điều 4.", "Nơi nhận:"]),
        "effective_date": extract_text_after_label(
            text,
            ["Hiệu lực từ ngày", "Có hiệu lực từ ngày"]
        ),
        "recipient": extract_section_content(text, "Nơi nhận:", []),
    })

    return result