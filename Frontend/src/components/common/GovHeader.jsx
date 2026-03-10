function HeaderNav({ page, onNavigate }) {
  const items = [
    { key: "dashboard", label: "Trang chủ" },
    { key: "project-tracking", label: "Gói thầu của tôi" },
    { key: "reports", label: "Báo cáo" }
  ];

  return (
    <div className="border-b border-[#505048] bg-[#252520]">
      <div className="mx-auto flex w-full max-w-[1400px] flex-wrap gap-6 px-4">
        {items.map((item) => {
          const isActive =
            (item.key === "dashboard" && page === "dashboard") ||
            ((item.key === "project-tracking" &&
              (page === "project-tracking" || page === "project-progress")));

          return (
            <button
              key={item.key}
              onClick={() => onNavigate(item.key)}
              className={`border-b-2 px-1 py-3 text-[13px] font-medium transition ${
                isActive
                  ? "border-[#D4A017] text-[#D4A017] font-bold"
                  : "border-transparent text-white/65 hover:text-white"
              }`}
            >
              {item.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default function GovHeader({ page, onNavigate }) {
  return (
    <header>
      <div className="border-b border-[#B8860B] bg-[#6B0000]">
        <div className="mx-auto flex w-full max-w-[1400px] items-center justify-between px-4 py-1.5 text-[11px]">
          <div className="flex flex-wrap items-center gap-3 text-white/70">
            <span>Trang chủ Chính phủ</span>
            <span className="text-white/30">|</span>
            <span>Cổng TTĐT tỉnh X</span>
            <span className="text-white/30">|</span>
            <span>Sở Nội vụ</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-white/60">Thứ Bảy, 07/03/2026</span>
            <button className="font-semibold text-[#F0C040]">Đăng xuất</button>
          </div>
        </div>
      </div>

      <div className="border-b-[3px] border-[#D4A017] bg-[linear-gradient(135deg,#8B0000,_#C0161D,_#8B0000)]">
        <div className="mx-auto flex w-full max-w-[1400px] items-center justify-between gap-6 px-4 py-4">
          <div className="flex min-w-0 items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full border-[3px] border-[#F0C040] bg-[radial-gradient(circle,#D4A017_0%,#B8860B_40%,#8B0000_100%)] text-2xl text-[#8B0000] shadow-[0_0_16px_#B8860B60]">
              ★
            </div>

            <div className="min-w-0">
              <div className="text-[11px] uppercase tracking-[0.12em] text-[#F0C040]">
                Cộng hòa Xã hội Chủ nghĩa Việt Nam
              </div>
              <div className="mt-1 text-xl font-black text-white">
                HỆ THỐNG ĐẤU THẦU ĐIỆN TỬ
              </div>
              <div className="mt-1 text-xs text-[#F0C040]">
                Sở Nội vụ tỉnh X — Kiểm tra hồ sơ nhà thầu bằng AI
              </div>
            </div>
          </div>

          <div className="hidden items-center gap-4 md:flex">
            <div className="relative text-white">🔔<span className="absolute -right-1 top-0 h-2 w-2 rounded-full bg-[#F0C040]" /></div>
            <div className="h-8 w-px bg-white/20" />
            <div className="flex items-center gap-3">
              <div className="flex h-[34px] w-[34px] items-center justify-center rounded-full bg-[#F0C040] text-sm font-bold text-[#8B0000]">
                SN
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-white">Sở Nội vụ tỉnh X</div>
                <div className="text-[11px] text-[#F0C040]">Chủ đầu tư</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <HeaderNav page={page} onNavigate={onNavigate} />
    </header>
  );
}
