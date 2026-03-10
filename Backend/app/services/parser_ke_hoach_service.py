from app.services.parser_common_service import (
    build_base_schema,
    extract_text_after_label,
)


def parse_ke_hoach_lua_chon_nha_thau(text: str) -> dict:
    result = build_base_schema("KE_HOACH_LUA_CHON_NHA_THAU", text)

    result.update({
        "package_name": extract_text_after_label(
            text,
            ["Tên gói thầu", "Gói thầu", "Tên gói"]
        ),
        "project_name": extract_text_after_label(
            text,
            ["Tên dự án", "Dự án"]
        ),
        "package_price": extract_text_after_label(
            text,
            ["Giá gói thầu", "Giá gói", "Đầu tư"]
        ),
        "funding_source": extract_text_after_label(
            text,
            ["Nguồn vốn"]
        ),
        "selection_method": extract_text_after_label(
            text,
            ["Hình thức lựa chọn nhà thầu", "Hình thức lựa chọn"]
        ),
        "contract_type": extract_text_after_label(
            text,
            ["Loại hợp đồng"]
        ),
        "implementation_time": extract_text_after_label(
            text,
            ["Thời gian thực hiện", "Thời gian thực hiện hợp đồng"]
        ),
        "bid_organization_time": extract_text_after_label(
            text,
            ["Thời gian tổ chức lựa chọn nhà thầu", "Thời gian tổ chức"]
        ),
    })

    return result