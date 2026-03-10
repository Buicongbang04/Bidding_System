export default function PipelineStatus({ label, done, active, error }) {
  let className = "border-[#DDDDD8] bg-white text-[#707068]";

  if (error) className = "border-[#fca5a5] bg-[#FDF2F2] text-[#C0161D]";
  else if (done) className = "border-[#86efac] bg-[#F0F9F4] text-[#1A6B3A]";
  else if (active) className = "border-[#E8C84A] bg-[#FFF8E8] text-[#996600]";

  return (
    <div className={`rounded-[5px] border p-3 text-sm ${className}`}>
      <div className="font-bold">{label}</div>
      <div className="mt-1 text-[11px]">
        {error ? "Có lỗi" : done ? "Hoàn thành" : active ? "Đang chạy" : "Chưa chạy"}
      </div>
    </div>
  );
}
