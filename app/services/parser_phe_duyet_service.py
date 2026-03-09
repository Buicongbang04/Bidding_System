from app.services.parser_common_service import (
    build_base_schema,
    extract_text_after_label,
)


def parse_van_ban_phe_duyet_nha_thau(text: str) -> dict:
    result = build_base_schema("VAN_BAN_PHE_DUYET_NHA_THAU", text)

    result.update({
        "package_name": extract_text_after_label(
            text,
            ["Tên gói thầu", "Gói thầu", "Tên gói"]
        ),
        "approved_contractor": extract_text_after_label(
            text,
            ["Nhà thầu được phê duyệt", "Nhà thầu trúng thầu", "Đơn vị trúng thầu"]
        ),
        "approved_price": extract_text_after_label(
            text,
            ["Giá phê duyệt", "Giá trúng thầu", "Giá được phê duyệt"]
        ),
        "contract_duration": extract_text_after_label(
            text,
            ["Thời gian thực hiện hợp đồng", "Thời hạn hợp đồng"]
        ),
        "approval_result": extract_text_after_label(
            text,
            ["Kết quả phê duyệt", "Nội dung phê duyệt"]
        ),
        "notes": extract_text_after_label(
            text,
            ["Ghi chú"]
        ),
    })

    return result