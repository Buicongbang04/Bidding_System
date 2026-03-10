from __future__ import annotations

import re

from app.schemas.document_profiles import get_profile_by_legacy_type


DATE_PATTERN = re.compile(r"^\d{1,2}[/-]\d{1,2}[/-]\d{4}$")
DATE_FRAGMENT_PATTERN = re.compile(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}")
MONEY_PATTERN = re.compile(r"^\s*[\d\.\,\s]+(?:đồng|vnd|vnđ)?\s*$", re.IGNORECASE)


def validate_parsed_data(document_type: str, parsed_data: dict) -> dict:
    if not parsed_data:
        raise ValueError("parsed_data rỗng, không thể validate")

    resolved_document_type = parsed_data.get("legacy_document_type") or document_type
    profile = get_profile_by_legacy_type(resolved_document_type)
    uncertain_fields = set(parsed_data.get("uncertain_fields") or [])

    warnings = []
    violations = []

    for field_name in profile.required_fields:
        value = _normalize_value(parsed_data.get(field_name))

        if not value:
            warnings.append(_build_warning(
                code="MISSING_REQUIRED_FIELD",
                field=field_name,
                severity="high",
                message=f"Thiếu trường bắt buộc: {field_name}",
                evidence=None,
            ))
        elif field_name in uncertain_fields:
            warnings.append(_build_warning(
                code="UNCERTAIN_REQUIRED_FIELD",
                field=field_name,
                severity="medium",
                message=f"Trường bắt buộc chưa chắc chắn: {field_name}",
                evidence=None,
            ))

    for field_name, hint in profile.format_hints.items():
        value = _normalize_value(parsed_data.get(field_name))
        if not value:
            continue
        if not _is_valid_format(value, hint):
            warnings.append(_build_warning(
                code="INVALID_FIELD_FORMAT",
                field=field_name,
                severity="medium",
                message=f"Định dạng trường {field_name} không hợp lệ",
                evidence=None,
            ))

    violations.extend(_check_internal_conflicts(profile.legacy_type, parsed_data))

    final_status = "FAIL" if violations else "WARNING" if warnings else "PASS"
    validation_status = "invalid" if (warnings or violations) else "valid"
    failed_rules = _count_failed_rules(warnings, violations)

    return {
        "document_type": parsed_data.get("document_type", profile.llm_type),
        "legacy_document_type": profile.legacy_type,
        "warnings": warnings,
        "violations": violations,
        "final_status": final_status,
        "validation_status": validation_status,
        "errors": violations,
        "passed_rules": _count_passed_rules(profile.required_fields, warnings),
        "failed_rules": failed_rules,
        "total_rules": len(profile.required_fields),
    }


def _normalize_value(value: object) -> str | list[str] | None:
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return cleaned or None
    return value


def _is_valid_format(value: str | list[str], hint: str) -> bool:
    if isinstance(value, list):
        return all(_is_valid_format(item, hint) for item in value)

    if hint == "date":
        return bool(DATE_PATTERN.match(value))
    if hint == "money":
        return bool(MONEY_PATTERN.match(value))
    return True


def _check_internal_conflicts(
    legacy_document_type: str,
    parsed_data: dict,
) -> list[dict]:
    violations: list[dict] = []

    if legacy_document_type == "VAN_BAN_PHE_DUYET_NHA_THAU":
        approval_result = _as_text(parsed_data.get("approval_result"))
        approved_contractor = _as_text(parsed_data.get("approved_contractor"))
        if approval_result and "không" in approval_result.lower() and approved_contractor:
            violations.append({
                "code": "INTERNAL_DATA_CONFLICT",
                "field": "approval_result",
                "severity": "high",
                "message": "Kết quả phê duyệt mâu thuẫn với thông tin nhà thầu được duyệt",
                "evidence": None,
            })

    if legacy_document_type == "QUYET_DINH":
        opening_time = _as_text(parsed_data.get("opening_time"))
        issue_date = _as_text(parsed_data.get("issue_date"))
        if opening_time and issue_date and issue_date not in opening_time and not DATE_FRAGMENT_PATTERN.search(opening_time):
            violations.append({
                "code": "OPENING_TIME_CONFLICT",
                "field": "opening_time",
                "severity": "high",
                "message": "Thời gian mở thầu không rõ ràng hoặc mâu thuẫn với ngày ban hành",
                "evidence": None,
            })

    return violations


def _count_passed_rules(required_fields: tuple[str, ...], warnings: list[dict]) -> int:
    warned_fields = {
        warning["field"]
        for warning in warnings
        if warning["code"] in {"MISSING_REQUIRED_FIELD", "UNCERTAIN_REQUIRED_FIELD"}
    }
    return sum(1 for field_name in required_fields if field_name not in warned_fields)


def _count_failed_rules(warnings: list[dict], violations: list[dict]) -> int:
    relevant_warning_codes = {
        "MISSING_REQUIRED_FIELD",
        "UNCERTAIN_REQUIRED_FIELD",
        "INVALID_FIELD_FORMAT",
    }
    warning_count = sum(1 for warning in warnings if warning["code"] in relevant_warning_codes)
    return warning_count + len(violations)


def _build_warning(
    code: str,
    field: str,
    severity: str,
    message: str,
    evidence: str | None,
) -> dict:
    return {
        "code": code,
        "field": field,
        "severity": severity,
        "message": message,
        "evidence": evidence,
    }


def _as_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        joined = ", ".join(str(item).strip() for item in value if str(item).strip())
        return joined or None
    text = str(value).strip()
    return text or None
