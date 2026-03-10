from datetime import datetime


REQUIRED_PROJECT_DOCUMENT_TYPES = [
    "KE_HOACH_LUA_CHON_NHA_THAU",
    "VAN_BAN_PHE_DUYET_NHA_THAU",
    "QUYET_DINH",
]


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.strip().lower().split())


def _parse_money(value: str | None) -> float | None:
    if not value:
        return None

    cleaned = value.lower()
    for token in ["đồng", "vnd", ",", " "]:
        cleaned = cleaned.replace(token, "")
    cleaned = cleaned.replace(".", "")

    digits = "".join(ch for ch in cleaned if ch.isdigit())
    if not digits:
        return None

    try:
        return float(digits)
    except ValueError:
        return None


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None

    patterns = [
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    for fmt in patterns:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def _index_documents_by_type(documents: list) -> dict:
    result = {}
    for doc in documents:
        parsed_data = getattr(doc, "parsed_data", None) or {}
        resolved_type = parsed_data.get("legacy_document_type") or doc.document_type
        result[resolved_type] = doc
    return result


def _get_field_value(document, field_name: str):
    if not document or not document.parsed_data:
        return None

    direct_value = document.parsed_data.get(field_name)
    if direct_value not in (None, "", [], {}):
        return direct_value
    return None


def validate_project_documents(project_id: str, documents: list) -> dict:
    errors = []
    warnings = []
    checked_documents = []

    docs_by_type = _index_documents_by_type(documents)

    for doc_type in REQUIRED_PROJECT_DOCUMENT_TYPES:
        if doc_type not in docs_by_type:
            errors.append({
                "rule": "MISSING_DOCUMENT_TYPE",
                "message": f"Thiếu văn bản loại {doc_type}",
                "document_type": doc_type,
            })
        else:
            checked_documents.append(doc_type)

    plan_doc = docs_by_type.get("KE_HOACH_LUA_CHON_NHA_THAU")
    approval_doc = docs_by_type.get("VAN_BAN_PHE_DUYET_NHA_THAU")
    decision_doc = docs_by_type.get("QUYET_DINH")

    # Rule 1: package_name phải khớp
    if plan_doc and approval_doc and plan_doc.parsed_data and approval_doc.parsed_data:
        plan_package_name = _normalize_text(_get_field_value(plan_doc, "package_name"))
        approval_package_name = _normalize_text(_get_field_value(approval_doc, "package_name"))

        if plan_package_name and approval_package_name:
            if plan_package_name != approval_package_name:
                errors.append({
                    "rule": "PACKAGE_NAME_MATCH",
                    "message": "Tên gói thầu giữa kế hoạch và phê duyệt không khớp",
                    "plan_package_name": _get_field_value(plan_doc, "package_name"),
                    "approval_package_name": _get_field_value(approval_doc, "package_name"),
                })
        else:
            warnings.append({
                "rule": "PACKAGE_NAME_MISSING",
                "message": "Không đủ dữ liệu để đối chiếu tên gói thầu giữa kế hoạch và phê duyệt",
            })

    # Rule 2: approved_price <= package_price
    if plan_doc and approval_doc and plan_doc.parsed_data and approval_doc.parsed_data:
        package_price = _parse_money(_get_field_value(plan_doc, "package_price"))
        approved_price = _parse_money(_get_field_value(approval_doc, "approved_price"))

        if package_price is not None and approved_price is not None:
            if approved_price > package_price:
                errors.append({
                    "rule": "PRICE_COMPARISON",
                    "message": "Giá phê duyệt lớn hơn giá gói thầu",
                    "package_price": _get_field_value(plan_doc, "package_price"),
                    "approved_price": _get_field_value(approval_doc, "approved_price"),
                })
            elif approved_price < package_price * 0.5:
                warnings.append({
                    "rule": "PRICE_WARNING",
                    "message": "Giá phê duyệt thấp hơn 50% giá gói thầu",
                    "package_price": _get_field_value(plan_doc, "package_price"),
                    "approved_price": _get_field_value(approval_doc, "approved_price"),
                })
        else:
            warnings.append({
                "rule": "PRICE_MISSING",
                "message": "Không đủ dữ liệu để đối chiếu giá giữa kế hoạch và phê duyệt",
            })

    # Rule 3: ngày phê duyệt phải sau hoặc bằng ngày kế hoạch
    if plan_doc and approval_doc and plan_doc.parsed_data and approval_doc.parsed_data:
        plan_date = _parse_date(_get_field_value(plan_doc, "issued_date"))
        approval_date = _parse_date(_get_field_value(approval_doc, "issued_date"))

        if plan_date and approval_date:
            if approval_date < plan_date:
                errors.append({
                    "rule": "ISSUED_DATE_ORDER",
                    "message": "Ngày ban hành văn bản phê duyệt sớm hơn kế hoạch lựa chọn nhà thầu",
                    "plan_issued_date": _get_field_value(plan_doc, "issued_date"),
                    "approval_issued_date": _get_field_value(approval_doc, "issued_date"),
                })
        else:
            warnings.append({
                "rule": "ISSUED_DATE_MISSING",
                "message": "Không đủ dữ liệu để đối chiếu ngày ban hành giữa kế hoạch và phê duyệt",
            })

    # Rule 4: Quyết định phải có signer
    if decision_doc:
        signer = _get_field_value(decision_doc, "signer")

        if not signer:
            errors.append({
                "rule": "DECISION_SIGNER_REQUIRED",
                "message": "Quyết định thiếu người ký",
            })

    validation_status = "valid" if len(errors) == 0 else "invalid"

    final_status = "FAIL" if errors else "WARNING" if warnings else "PASS"

    return {
        "project_id": project_id,
        "validation_status": validation_status,
        "errors": errors,
        "violations": errors,
        "warnings": warnings,
        "final_status": final_status,
        "checked_documents": checked_documents,
        "total_errors": len(errors),
        "total_warnings": len(warnings),
    }
