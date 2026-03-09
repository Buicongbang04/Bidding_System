REQUIRED_FIELDS_BY_DOCUMENT_TYPE = {
    "KE_HOACH_LUA_CHON_NHA_THAU": [
        ("document_number", "Thiếu số văn bản"),
        ("issued_date", "Thiếu ngày ban hành"),
        ("signer", "Thiếu người ký"),
        ("package_name", "Thiếu tên gói thầu"),
        ("package_price", "Thiếu giá gói thầu"),
        ("selection_method", "Thiếu hình thức lựa chọn nhà thầu"),
    ],
    "VAN_BAN_PHE_DUYET_NHA_THAU": [
        ("document_number", "Thiếu số văn bản"),
        ("issued_date", "Thiếu ngày ban hành"),
        ("signer", "Thiếu người ký"),
        ("approved_contractor", "Thiếu nhà thầu được phê duyệt"),
        ("approved_price", "Thiếu giá phê duyệt"),
        ("approval_result", "Thiếu kết quả phê duyệt"),
    ],
    "QUYET_DINH": [
        ("document_number", "Thiếu số văn bản"),
        ("issued_date", "Thiếu ngày ban hành"),
        ("signer", "Thiếu người ký"),
        ("decision_subject", "Thiếu nội dung quyết định"),
        ("article_1", "Thiếu Điều 1"),
    ],
}


def _is_missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, list) and len(value) == 0:
        return True
    if isinstance(value, dict) and len(value) == 0:
        return True
    return False


def validate_parsed_data(document_type: str, parsed_data: dict) -> dict:
    if not parsed_data:
        raise ValueError("parsed_data rỗng, không thể validate")

    if document_type not in REQUIRED_FIELDS_BY_DOCUMENT_TYPE:
        raise ValueError(f"document_type không được hỗ trợ: {document_type}")

    required_rules = REQUIRED_FIELDS_BY_DOCUMENT_TYPE[document_type]

    errors = []
    warnings = []
    passed_rules = 0
    failed_rules = 0

    for field_name, error_message in required_rules:
        field_value = parsed_data.get(field_name)

        if _is_missing(field_value):
            errors.append({
                "field": field_name,
                "message": error_message,
            })
            failed_rules += 1
        else:
            passed_rules += 1

    validation_status = "valid" if failed_rules == 0 else "invalid"

    return {
        "document_type": document_type,
        "validation_status": validation_status,
        "errors": errors,
        "warnings": warnings,
        "passed_rules": passed_rules,
        "failed_rules": failed_rules,
        "total_rules": len(required_rules),
    }