from __future__ import annotations

import hashlib
import json
from pathlib import Path

from app.core.config import settings


def build_extraction_cache_key(document_type: str, text: str, model_name: str) -> str:
    payload = f"{document_type}\n{model_name}\n{text}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_cached_extraction(cache_key: str) -> dict | None:
    cache_file = _cache_dir() / f"{cache_key}.json"
    if not cache_file.exists():
        return None

    try:
        payload = json.loads(cache_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    normalized_payload = _normalize_cached_payload(payload)
    if normalized_payload != payload:
        save_cached_extraction(cache_key, normalized_payload)
    return normalized_payload


def save_cached_extraction(cache_key: str, payload: dict) -> None:
    cache_dir = _cache_dir()
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{cache_key}.json"
    cache_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _cache_dir() -> Path:
    return Path(settings.upload_dir) / ".cache" / "parsed_extractions"


def _normalize_cached_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}

    if "fields" in payload and isinstance(payload.get("fields"), dict):
        payload.setdefault("field_statuses", {})
        return payload

    flattened_fields = payload.get("flattened_fields")
    extraction_result = payload.get("extraction_result") or {}
    extraction_fields = extraction_result.get("fields") or {}

    if isinstance(flattened_fields, dict):
        field_statuses = {}
        for field_name, field_payload in extraction_fields.items():
            if isinstance(field_payload, dict):
                field_statuses[field_name] = field_payload.get("status", "missing")

        return {
            "document_type": payload.get("document_type"),
            "fields": flattened_fields,
            "field_statuses": field_statuses,
        }

    return payload
