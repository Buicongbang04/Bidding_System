from __future__ import annotations

from app.schemas.document_profiles import DocumentProfile
from app.schemas.extraction_schema import ExtractedField
from app.services.parser_common_service import (
    extract_issued_date,
    extract_signer,
    extract_text_after_label,
    split_non_empty_lines,
)


LABELS_BY_FIELD: dict[str, list[str]] = {
    "project_name": ["Tên dự án", "Dự án"],
    "package_name": ["Tên gói thầu", "Gói thầu", "Tên gói"],
    "package_price": ["Giá gói thầu", "Giá gói", "Dự toán gói thầu"],
    "investor": ["Chủ đầu tư"],
    "selection_method": ["Hình thức lựa chọn nhà thầu", "Hình thức lựa chọn"],
    "contractor_selection_method": ["Phương thức lựa chọn nhà thầu", "Phương thức lựa chọn"],
    "contract_type": ["Loại hợp đồng"],
    "contract_duration": ["Thời gian thực hiện hợp đồng", "Thời hạn hợp đồng", "Thời gian thực hiện"],
    "approval_date": ["Ngày phê duyệt", "Ngày ban hành"],
    "funding_source": ["Nguồn vốn"],
    "start_time_for_selection": ["Thời gian tổ chức lựa chọn nhà thầu", "Thời gian tổ chức"],
    "approved_contractor": ["Nhà thầu được phê duyệt", "Nhà thầu trúng thầu", "Đơn vị trúng thầu"],
    "approved_price": ["Giá phê duyệt", "Giá trúng thầu", "Giá được phê duyệt"],
    "approval_result": ["Kết quả phê duyệt", "Nội dung phê duyệt"],
    "opening_time": ["Thời gian mở thầu", "Mở thầu vào lúc", "Thời điểm mở thầu"],
    "opening_location": ["Địa điểm mở thầu", "Mở thầu tại"],
    "inviting_party": ["Bên mời thầu"],
    "issue_date": ["Ngày ban hành", "Ngày lập biên bản"],
    "participants": ["Thành phần", "Đại diện tham dự"],
    "opening_method": ["Hình thức mở thầu", "Phương thức mở thầu"],
    "notes": ["Ghi chú", "Về việc"],
}


def run_heuristic_extraction(text: str, profile: DocumentProfile) -> dict[str, dict]:
    lines = split_non_empty_lines(text)
    fields: dict[str, dict] = {}

    for field_name in profile.required_fields + profile.optional_fields:
        extracted = _extract_by_field(field_name, text, lines)
        fields[field_name] = extracted.model_dump()

    return fields


def _extract_by_field(field_name: str, text: str, lines: list[str]) -> ExtractedField:
    if field_name in {"approval_date", "issue_date"}:
        value = extract_issued_date(text)
        evidence = _find_line_containing(lines, value) or _find_line_containing(lines, "ngày")
        return _build_field(value=value, evidence=evidence)

    if field_name == "signer":
        value = extract_signer(lines)
        evidence = _find_line_containing(lines, value)
        return _build_field(value=value, evidence=evidence)

    labels = LABELS_BY_FIELD.get(field_name, [])
    value = extract_text_after_label(text, labels) if labels else None
    evidence = _find_evidence_by_labels(lines, labels, value)
    return _build_field(value=value, evidence=evidence)


def _build_field(value: str | None, evidence: str | None) -> ExtractedField:
    if not value:
        return ExtractedField(
            value=None,
            status="missing",
            confidence=0.0,
            evidence=None,
        )

    confidence = 0.78 if evidence else 0.65
    return ExtractedField(
        value=value,
        status="found",
        confidence=confidence,
        evidence=evidence or value,
    )


def _find_evidence_by_labels(lines: list[str], labels: list[str], value: str | None) -> str | None:
    if value:
        direct_line = _find_line_containing(lines, value)
        if direct_line:
            return direct_line

    for label in labels:
        matched_line = _find_line_containing(lines, label)
        if matched_line:
            return matched_line
    return None


def _find_line_containing(lines: list[str], needle: str | None) -> str | None:
    if not needle:
        return None

    normalized_needle = needle.lower().strip()
    for line in lines:
        if normalized_needle in line.lower():
            return line
    return None
