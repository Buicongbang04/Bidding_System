from __future__ import annotations

from app.schemas.document_profiles import DocumentProfile
from app.services.parser_common_service import split_non_empty_lines


MAX_CONTEXT_CHARS = 5000
HEAD_LINE_COUNT = 40
TAIL_LINE_COUNT = 20

COMMON_KEYWORDS = (
    "gói thầu",
    "dự án",
    "chủ đầu tư",
    "bên mời thầu",
    "hình thức",
    "loại hợp đồng",
    "thời gian",
    "thời hạn",
    "ngày",
    "ký",
    "nhà thầu",
    "mở thầu",
    "phê duyệt",
)

FIELD_LABEL_HINTS: dict[str, tuple[str, ...]] = {
    "project_name": ("tên dự án", "dự án"),
    "package_name": ("tên gói thầu", "gói thầu", "tên gói"),
    "package_price": ("giá gói thầu", "giá gói"),
    "investor": ("chủ đầu tư",),
    "selection_method": ("hình thức lựa chọn nhà thầu", "hình thức lựa chọn"),
    "contractor_selection_method": ("phương thức lựa chọn nhà thầu", "phương thức lựa chọn"),
    "contract_type": ("loại hợp đồng",),
    "contract_duration": ("thời gian thực hiện hợp đồng", "thời hạn hợp đồng", "thời gian thực hiện"),
    "approval_date": ("ngày",),
    "signer": ("chủ tịch", "giám đốc", "trưởng phòng", "phó chủ tịch"),
    "funding_source": ("nguồn vốn",),
    "start_time_for_selection": ("thời gian tổ chức lựa chọn nhà thầu", "thời gian tổ chức"),
    "approved_contractor": ("nhà thầu trúng thầu", "nhà thầu được phê duyệt", "đơn vị trúng thầu"),
    "approved_price": ("giá phê duyệt", "giá trúng thầu", "giá được phê duyệt"),
    "approval_result": ("kết quả phê duyệt", "nội dung phê duyệt"),
    "opening_time": ("thời gian mở thầu", "mở thầu vào lúc", "thời điểm mở thầu"),
    "opening_location": ("địa điểm mở thầu", "mở thầu tại"),
    "inviting_party": ("bên mời thầu",),
    "issue_date": ("ngày",),
    "participants": ("thành phần", "đại diện", "tham dự"),
    "opening_method": ("hình thức mở thầu", "phương thức mở thầu"),
    "notes": ("ghi chú", "về việc"),
}


def build_compressed_context(
    text: str,
    profile: DocumentProfile,
    target_fields: list[str] | tuple[str, ...] | None = None,
) -> str:
    lines = split_non_empty_lines(text)
    if not lines:
        return ""

    relevant_indices: set[int] = set(range(min(len(lines), HEAD_LINE_COUNT)))
    relevant_indices.update(range(max(0, len(lines) - TAIL_LINE_COUNT), len(lines)))

    target_keywords = set(profile.detection_keywords) | set(COMMON_KEYWORDS)
    for field_name in target_fields or []:
        target_keywords.update(FIELD_LABEL_HINTS.get(field_name, ()))

    for index, line in enumerate(lines):
        lower_line = line.lower()
        if any(keyword in lower_line for keyword in target_keywords):
            start = max(0, index - 1)
            end = min(len(lines), index + 2)
            relevant_indices.update(range(start, end))

    compressed_lines = [lines[index] for index in sorted(relevant_indices)]
    compressed_text = "\n".join(_dedupe_preserve_order(compressed_lines))
    return compressed_text[:MAX_CONTEXT_CHARS]


def _dedupe_preserve_order(lines: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []

    for line in lines:
        key = line.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(line)

    return result
