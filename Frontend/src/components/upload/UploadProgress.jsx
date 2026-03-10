export default function UploadProgress({ percent, count, total }) {
  return (
    <div className="rounded-[5px] border border-[#DDDDD8] bg-[#F7F7F5] px-5 py-4">
      <div className="text-[11px] uppercase tracking-[0.06em] text-[#707068]">Tiến độ hồ sơ</div>
      <div className="mt-1 text-2xl font-black text-[#252520]">{percent}%</div>
      <div className="text-[11px] text-[#707068]">
        {count}/{total} tài liệu hợp lệ
      </div>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-[#EEEEEA]">
        <div
          className="h-full rounded-full bg-[linear-gradient(90deg,#C0161D,_#B8860B)]"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
