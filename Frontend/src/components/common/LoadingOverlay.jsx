export default function LoadingOverlay({ visible, text = "Đang xử lý..." }) {
  if (!visible) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-[#252520]/40">
      <div className="rounded-md border border-[#DDDDD8] bg-white px-6 py-5 shadow-xl">
        <div className="text-sm font-bold text-[#505048]">{text}</div>
      </div>
    </div>
  );
}
