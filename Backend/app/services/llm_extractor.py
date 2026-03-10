from __future__ import annotations

from app.schemas.document_profiles import DocumentProfile
from app.schemas.extraction_schema import ExtractedField
from app.services.ollama_service import generate_json


def extract_document_fields_with_llm(
    text: str,
    profile: DocumentProfile,
    target_fields: list[str],
    existing_fields: dict[str, dict] | None = None,
) -> dict:
    existing_fields = existing_fields or {}
    normalized_existing_fields = {
        field_name: _normalize_field_payload(field_payload)
        for field_name, field_payload in existing_fields.items()
    }

    if not target_fields:
        return _build_payload(profile=profile, normalized_fields=normalized_existing_fields)

    prompt = _build_extraction_prompt(
        text=text,
        profile=profile,
        target_fields=target_fields,
        existing_fields=normalized_existing_fields,
    )
    llm_payload, _ = generate_json(prompt)
    normalized_fields = _merge_llm_fields(
        llm_payload=llm_payload,
        profile=profile,
        target_fields=target_fields,
        existing_fields=normalized_existing_fields,
    )
    return _build_payload(profile=profile, normalized_fields=normalized_fields)


def _build_extraction_prompt(
    text: str,
    profile: DocumentProfile,
    target_fields: list[str],
    existing_fields: dict[str, ExtractedField],
) -> str:
    target_field_schema = ", ".join(f'"{name}"' for name in target_fields)
    prior_values = []
    for field_name, field_payload in existing_fields.items():
        if field_payload.status == "found" and field_payload.value is not None:
            prior_values.append(f'- {field_name}: {field_payload.value}')
    prior_values_text = "\n".join(prior_values) if prior_values else "- không có"

    return f"""
Bạn là hệ thống trích xuất dữ liệu hồ sơ đấu thầu.
Nhiệm vụ: đọc văn bản và chỉ trả về JSON duy nhất, không giải thích.

Loại văn bản:
- legacy_type: {profile.legacy_type}
- document_type: {profile.llm_type}
- display_name: {profile.display_name}

Các field đã có sẵn từ heuristic, chỉ dùng để tham chiếu:
{prior_values_text}

Chỉ trích xuất các field sau:
{", ".join(target_fields)}

JSON bắt buộc:
{{
  "document_type": "{profile.llm_type}",
  "fields": {{
    {target_field_schema}: {{
      "value": string | array | null,
      "status": "found" | "missing" | "uncertain",
      "confidence": number từ 0 đến 1,
      "evidence": string | null
    }}
  }}
}}

Quy tắc:
- Không thêm field ngoài danh sách cần trích xuất.
- Nếu không chắc chắn thì dùng "uncertain".
- Nếu không có bằng chứng thì dùng "missing".
- evidence phải là đoạn ngắn nguyên văn từ tài liệu.
- Không kết luận pháp lý.

Văn bản đã rút gọn:
\"\"\"
{text}
\"\"\"
""".strip()


def _merge_llm_fields(
    llm_payload: dict,
    profile: DocumentProfile,
    target_fields: list[str],
    existing_fields: dict[str, ExtractedField],
) -> dict[str, ExtractedField]:
    raw_fields = llm_payload.get("fields")
    if not isinstance(raw_fields, dict):
        raise ValueError("Payload từ Ollama thiếu object fields")

    normalized_fields = dict(existing_fields)
    supported_fields = set(profile.required_fields) | set(profile.optional_fields)

    for field_name in supported_fields:
        if field_name in target_fields:
            normalized_fields[field_name] = _normalize_field_payload(raw_fields.get(field_name))
        else:
            normalized_fields.setdefault(
                field_name,
                ExtractedField(value=None, status="missing", confidence=0.0, evidence=None),
            )

    return normalized_fields


def _build_payload(
    profile: DocumentProfile,
    normalized_fields: dict[str, ExtractedField],
) -> dict:
    flattened_fields: dict[str, str | list[str] | None] = {}
    field_statuses: dict[str, str] = {}

    for field_name in profile.required_fields + profile.optional_fields:
        normalized_field = normalized_fields.get(field_name) or ExtractedField(
            value=None,
            status="missing",
            confidence=0.0,
            evidence=None,
        )
        flattened_fields[field_name] = normalized_field.value
        field_statuses[field_name] = normalized_field.status

    flattened_fields.update(_build_legacy_alias_values(profile.legacy_type, flattened_fields))

    return {
        "document_type": profile.llm_type,
        "fields": flattened_fields,
        "field_statuses": field_statuses,
    }


def find_missing_or_uncertain_fields(profile: DocumentProfile, fields: dict[str, dict]) -> list[str]:
    target_fields: list[str] = []

    for field_name in profile.required_fields + profile.optional_fields:
        field_payload = _normalize_field_payload(fields.get(field_name))
        if field_payload.status in {"missing", "uncertain"} or field_payload.value is None:
            target_fields.append(field_name)

    return target_fields


def _normalize_field_payload(field_payload: object) -> ExtractedField:
    if isinstance(field_payload, ExtractedField):
        return field_payload

    if not isinstance(field_payload, dict):
        return ExtractedField(value=None, status="missing", confidence=0.0, evidence=None)

    value = field_payload.get("value")
    status = field_payload.get("status")
    confidence = field_payload.get("confidence")
    evidence = field_payload.get("evidence")

    if status not in {"found", "missing", "uncertain"}:
        status = "found" if value else "missing"

    try:
        normalized_confidence = float(confidence)
    except (TypeError, ValueError):
        normalized_confidence = 0.0 if status == "missing" else 0.5

    normalized_confidence = max(0.0, min(1.0, normalized_confidence))

    if isinstance(value, str):
        value = value.strip() or None
    elif isinstance(value, list):
        value = [str(item).strip() for item in value if str(item).strip()]
        value = value or None
    elif value is not None:
        value = str(value).strip() or None

    if status == "missing":
        value = None

    return ExtractedField(
        value=value,
        status=status,
        confidence=normalized_confidence,
        evidence=evidence,
    )


def _build_legacy_alias_values(
    legacy_type: str,
    flattened_fields: dict[str, str | list[str] | None],
) -> dict[str, str | list[str] | None]:
    if legacy_type == "KE_HOACH_LUA_CHON_NHA_THAU":
        return {
            "issued_date": flattened_fields.get("approval_date"),
            "implementation_time": flattened_fields.get("contract_duration"),
            "bid_organization_time": flattened_fields.get("start_time_for_selection"),
        }

    if legacy_type == "VAN_BAN_PHE_DUYET_NHA_THAU":
        return {
            "issued_date": flattened_fields.get("approval_date"),
        }

    if legacy_type == "QUYET_DINH":
        return {
            "issued_date": flattened_fields.get("issue_date"),
            "decision_subject": flattened_fields.get("notes"),
        }

    return {}
