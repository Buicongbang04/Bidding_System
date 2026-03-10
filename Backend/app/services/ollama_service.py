from __future__ import annotations

import json
from urllib import error, request

from app.core.config import settings


class OllamaServiceError(RuntimeError):
    pass


def generate_json(prompt: str) -> tuple[dict, dict]:
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
        },
    }

    http_request = request.Request(
        url=f"{settings.ollama_base_url.rstrip('/')}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(http_request, timeout=settings.ollama_timeout_seconds) as response:
            body = response.read().decode("utf-8")
    except error.URLError as exc:
        raise OllamaServiceError(
            f"Không thể kết nối Ollama tại {settings.ollama_base_url}: {exc}"
        ) from exc
    except TimeoutError as exc:
        raise OllamaServiceError("Timeout khi gọi Ollama") from exc

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError as exc:
        raise OllamaServiceError("Ollama trả về response không phải JSON hợp lệ") from exc

    raw_response = parsed.get("response")
    if isinstance(raw_response, dict):
        return raw_response, parsed
    if not isinstance(raw_response, str) or not raw_response.strip():
        raise OllamaServiceError("Ollama không trả về nội dung extraction")

    extraction_json = _load_json_with_repair(raw_response)
    return extraction_json, parsed


def _load_json_with_repair(raw_response: str) -> dict:
    candidates = [raw_response.strip()]

    first_brace = raw_response.find("{")
    last_brace = raw_response.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidates.append(raw_response[first_brace:last_brace + 1].strip())

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            continue

    raise OllamaServiceError("Không parse được JSON extraction từ Ollama")
