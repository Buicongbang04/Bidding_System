from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentProfile:
    legacy_type: str
    llm_type: str
    display_name: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    detection_keywords: tuple[str, ...]
    format_hints: dict[str, str]


DOCUMENT_PROFILES: dict[str, DocumentProfile] = {
    "KE_HOACH_LUA_CHON_NHA_THAU": DocumentProfile(
        legacy_type="KE_HOACH_LUA_CHON_NHA_THAU",
        llm_type="procurement_plan",
        display_name="Kế hoạch lựa chọn nhà thầu",
        required_fields=(
            "project_name",
            "package_name",
            "package_price",
            "investor",
            "selection_method",
            "contractor_selection_method",
            "contract_type",
            "contract_duration",
            "approval_date",
            "signer",
        ),
        optional_fields=(
            "funding_source",
            "start_time_for_selection",
            "notes",
        ),
        detection_keywords=(
            "kế hoạch lựa chọn nhà thầu",
            "phê duyệt kế hoạch lựa chọn nhà thầu",
            "khlcnt",
        ),
        format_hints={
            "approval_date": "date",
            "package_price": "money",
        },
    ),
    "VAN_BAN_PHE_DUYET_NHA_THAU": DocumentProfile(
        legacy_type="VAN_BAN_PHE_DUYET_NHA_THAU",
        llm_type="bid_approval",
        display_name="Văn bản phê duyệt kết quả lựa chọn nhà thầu",
        required_fields=(
            "package_name",
            "approved_contractor",
            "approved_price",
            "contract_type",
            "contract_duration",
            "approval_result",
            "approval_date",
            "signer",
        ),
        optional_fields=(
            "funding_source",
            "notes",
        ),
        detection_keywords=(
            "phê duyệt kết quả lựa chọn nhà thầu",
            "kết quả lựa chọn nhà thầu",
            "nhà thầu trúng thầu",
        ),
        format_hints={
            "approval_date": "date",
            "approved_price": "money",
        },
    ),
    "QUYET_DINH": DocumentProfile(
        legacy_type="QUYET_DINH",
        llm_type="bid_opening_decision",
        display_name="Quyết định / biên bản mở thầu",
        required_fields=(
            "package_name",
            "opening_time",
            "opening_location",
            "inviting_party",
            "issue_date",
            "signer",
        ),
        optional_fields=(
            "participants",
            "opening_method",
            "notes",
        ),
        detection_keywords=(
            "mở thầu",
            "biên bản mở thầu",
            "quyết định mở thầu",
        ),
        format_hints={
            "issue_date": "date",
            "opening_time": "datetime_or_text",
        },
    ),
}

LLM_TYPE_TO_LEGACY: dict[str, str] = {
    profile.llm_type: profile.legacy_type
    for profile in DOCUMENT_PROFILES.values()
}


def get_profile_by_legacy_type(document_type: str) -> DocumentProfile:
    try:
        return DOCUMENT_PROFILES[document_type]
    except KeyError as exc:
        raise ValueError(f"document_type không được hỗ trợ: {document_type}") from exc


def get_profile_by_llm_type(document_type: str) -> DocumentProfile:
    legacy_type = LLM_TYPE_TO_LEGACY.get(document_type)
    if not legacy_type:
        raise ValueError(f"llm document_type không được hỗ trợ: {document_type}")
    return DOCUMENT_PROFILES[legacy_type]


def supported_legacy_document_types() -> set[str]:
    return set(DOCUMENT_PROFILES.keys())
