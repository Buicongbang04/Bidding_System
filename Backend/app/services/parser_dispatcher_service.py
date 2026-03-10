from __future__ import annotations

from app.core.config import settings
from app.schemas.document_profiles import get_profile_by_legacy_type, supported_legacy_document_types
from app.services.document_detector import detect_document_type
from app.services.extraction_cache_service import (
    build_extraction_cache_key,
    load_cached_extraction,
    save_cached_extraction,
)
from app.services.heuristic_extraction_service import run_heuristic_extraction
from app.services.llm_extractor import (
    extract_document_fields_with_llm,
    find_missing_or_uncertain_fields,
)
from app.services.parser_common_service import normalize_text
from app.services.text_compression_service import build_compressed_context


SUPPORTED_DOCUMENT_TYPES = supported_legacy_document_types()


def parse_document_by_type(document_type: str, ocr_text: str) -> dict:
    text = normalize_text(ocr_text)

    if not text:
        raise ValueError("ocr_text rỗng, không thể parse")

    if document_type not in SUPPORTED_DOCUMENT_TYPES:
        raise ValueError(f"document_type không được hỗ trợ: {document_type}")

    detected = detect_document_type(text=text, hinted_document_type=document_type)
    profile = get_profile_by_legacy_type(detected["legacy_type"])

    cache_key = build_extraction_cache_key(
        document_type=profile.legacy_type,
        text=text,
        model_name=settings.ollama_model,
    )
    cached_extraction = load_cached_extraction(cache_key)
    if cached_extraction:
        extraction = cached_extraction
    else:
        heuristic_fields = run_heuristic_extraction(text=text, profile=profile)
        target_fields = find_missing_or_uncertain_fields(profile=profile, fields=heuristic_fields)
        compressed_text = build_compressed_context(
            text=text,
            profile=profile,
            target_fields=target_fields,
        )

        extraction = extract_document_fields_with_llm(
            text=compressed_text or text[:5000],
            profile=profile,
            target_fields=target_fields,
            existing_fields=heuristic_fields,
        )
        save_cached_extraction(cache_key, extraction)

    parsed_data = {
        "document_type": extraction["document_type"],
        "legacy_document_type": profile.legacy_type,
        "raw_text_preview": text[:1000],
    }
    parsed_data.update(extraction["fields"])
    parsed_data["uncertain_fields"] = [
        field_name
        for field_name, status in (extraction.get("field_statuses") or {}).items()
        if status == "uncertain"
    ]
    return parsed_data
