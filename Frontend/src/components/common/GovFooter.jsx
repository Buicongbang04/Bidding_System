export default function GovFooter() {
  return (
    <footer className="mt-10">
      <div className="border-t-[3px] border-[#B8860B] bg-[#252520]">
        <div className="mx-auto grid w-full max-w-[1400px] gap-8 px-4 py-6 md:grid-cols-[2fr_1fr_1fr_1fr]">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#B8860B] text-sm font-black text-[#8B0000]">
                ★
              </div>
              <div>
                <div className="text-[13px] font-extrabold text-white">SỞ NỘI VỤ TỈNH X</div>
                <div className="text-[10px] text-[#F0C040]">Hệ thống Đấu thầu điện tử</div>
              </div>
            </div>
            <p className="max-w-xl text-xs leading-7 text-white/45">
              Hệ thống hỗ trợ quản lý, theo dõi và kiểm tra hồ sơ đấu thầu điện tử, phục vụ công tác chuyên môn của cơ quan nhà nước và các đơn vị tham gia.
            </p>
          </div>

          <div className="space-y-3 text-xs text-white/50">
            <div className="border-b border-white/10 pb-2 font-bold uppercase tracking-[0.06em] text-[#F0C040]">
              Liên kết nhanh
            </div>
            <div>Trang chủ</div>
            <div>Gói thầu đang mở</div>
            <div>Kết quả đấu thầu</div>
            <div>Văn bản pháp luật</div>
          </div>

          <div className="space-y-3 text-xs text-white/50">
            <div className="border-b border-white/10 pb-2 font-bold uppercase tracking-[0.06em] text-[#F0C040]">
              Hỗ trợ
            </div>
            <div>Hướng dẫn sử dụng</div>
            <div>Câu hỏi thường gặp</div>
            <div>Liên hệ hỗ trợ</div>
            <div>Báo lỗi hệ thống</div>
          </div>

          <div className="space-y-3 text-xs text-white/50">
            <div className="border-b border-white/10 pb-2 font-bold uppercase tracking-[0.06em] text-[#F0C040]">
              Liên hệ
            </div>
            <div>📍 Trung tâm hành chính tỉnh X</div>
            <div>📞 1900 1234</div>
            <div>✉ support@dauthau.gov.vn</div>
            <div>🕐 08:00 - 17:00</div>
          </div>
        </div>
      </div>

      <div className="bg-[#6B0000] py-2 text-center text-[11px] text-white/40">
        © 2026 Sở Nội vụ tỉnh X - Hệ thống Đấu thầu điện tử
      </div>
    </footer>
  );
}
