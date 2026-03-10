export const DOCUMENT_TYPES = [
  {
    key: "KE_HOACH_LUA_CHON_NHA_THAU",
    title: "Kế hoạch lựa chọn nhà thầu",
    shortTitle: "KHLCNT",
    description:
      "Tài liệu dùng để kiểm tra tên gói thầu, giá gói thầu và hình thức lựa chọn nhà thầu."
  },
  {
    key: "VAN_BAN_PHE_DUYET_NHA_THAU",
    title: "Văn bản phê duyệt nhà thầu",
    shortTitle: "Phê duyệt",
    description:
      "Dùng để kiểm tra nhà thầu được phê duyệt, giá phê duyệt và kết quả phê duyệt."
  },
  {
    key: "QUYET_DINH",
    title: "Quyết định mở thầu",
    shortTitle: "Quyết định",
    description:
      "Dùng để kiểm tra quyết định mở thầu, người ký và các điều khoản chính."
  }
];

export const INITIAL_PROJECT_FORM = {
  code: "DA-001",
  name: "Gói thầu mua sắm thiết bị y tế",
  investor_name: "Ban QLDA A"
};

export function createInitialDocumentState() {
  return DOCUMENT_TYPES.reduce((acc, item) => {
    acc[item.key] = {
      file: null,
      documentId: "",
      uploaded: false,
      extracting: false,
      extracted: false,
      parsing: false,
      parsed: false,
      validating: false,
      validated: false,
      hasError: false,
      errorMessage: "",
      extractedTextPreview: "",
      parsedData: null,
      validationResult: null
    };
    return acc;
  }, {});
}

export const DOCUMENT_INITIAL_STATE = createInitialDocumentState();
