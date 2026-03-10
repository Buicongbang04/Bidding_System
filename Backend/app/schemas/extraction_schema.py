from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


FieldStatus = Literal["found", "missing", "uncertain"]


class ExtractedField(BaseModel):
    value: str | list[str] | None = None
    status: FieldStatus
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    evidence: str | None = None

    @field_validator("evidence")
    @classmethod
    def normalize_evidence(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None
