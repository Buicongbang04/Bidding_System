from app.services.parser_common_service import normalize_text
from app.services.parser_ke_hoach_service import parse_ke_hoach_lua_chon_nha_thau
from app.services.parser_phe_duyet_service import parse_van_ban_phe_duyet_nha_thau
from app.services.parser_quyet_dinh_service import parse_quyet_dinh


SUPPORTED_DOCUMENT_TYPES = {
    "KE_HOACH_LUA_CHON_NHA_THAU",
    "VAN_BAN_PHE_DUYET_NHA_THAU",
    "QUYET_DINH",
}


def parse_document_by_type(document_type: str, ocr_text: str) -> dict:
    text = normalize_text(ocr_text)

    if not text:
        raise ValueError("ocr_text rỗng, không thể parse")

    if document_type not in SUPPORTED_DOCUMENT_TYPES:
        raise ValueError(f"document_type không được hỗ trợ: {document_type}")

    if document_type == "KE_HOACH_LUA_CHON_NHA_THAU":
        return parse_ke_hoach_lua_chon_nha_thau(text)

    if document_type == "VAN_BAN_PHE_DUYET_NHA_THAU":
        return parse_van_ban_phe_duyet_nha_thau(text)

    if document_type == "QUYET_DINH":
        return parse_quyet_dinh(text)

    raise ValueError(f"Không tìm thấy parser cho document_type={document_type}")