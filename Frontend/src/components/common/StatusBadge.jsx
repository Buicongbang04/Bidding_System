const MAP = {
  idle: "border-[#C8C8C2] bg-[#EEEEEA] text-[#707068]",
  processing: "border-[#E8C84A] bg-[#FFF8E8] text-[#996600]",
  success: "border-[#86efac] bg-[#F0F9F4] text-[#1A6B3A]",
  error: "border-[#fca5a5] bg-[#FDF2F2] text-[#C0161D]"
};

const LABEL = {
  idle: "Chưa upload",
  processing: "Đang xử lý",
  success: "Hợp lệ",
  error: "Lỗi"
};

export default function StatusBadge({ type = "idle" }) {
  return (
    <span
      className={`rounded-[3px] border px-[10px] py-[3px] text-[11px] font-bold tracking-[0.03em] ${MAP[type] || MAP.idle}`}
    >
      {LABEL[type] || LABEL.idle}
    </span>
  );
}
