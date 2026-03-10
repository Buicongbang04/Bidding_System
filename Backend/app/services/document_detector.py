from __future__ import annotations

from app.schemas.document_profiles import (
    DOCUMENT_PROFILES,
    get_profile_by_legacy_type,
)


def detect_document_type(text: str, hinted_document_type: str | None = None) -> dict:
    normalized_text = (text or "").lower()

    if hinted_document_type and hinted_document_type in DOCUMENT_PROFILES:
        hinted_profile = get_profile_by_legacy_type(hinted_document_type)
    else:
        hinted_profile = None

    best_profile = None
    best_score = -1

    for profile in DOCUMENT_PROFILES.values():
        score = sum(1 for keyword in profile.detection_keywords if keyword in normalized_text)
        if score > best_score:
            best_profile = profile
            best_score = score

    if best_profile and best_score > 0:
        confidence = min(0.99, 0.55 + best_score * 0.15)
        return {
            "legacy_type": best_profile.legacy_type,
            "llm_type": best_profile.llm_type,
            "confidence": confidence,
            "method": "heuristic",
        }

    if hinted_profile:
        return {
            "legacy_type": hinted_profile.legacy_type,
            "llm_type": hinted_profile.llm_type,
            "confidence": 0.6,
            "method": "upload_hint",
        }

    raise ValueError("Không thể xác định loại văn bản từ nội dung và document_type gợi ý")
