import PageContainer from "../components/common/PageContainer";
import SecTitle from "../components/common/SecTitle";
import StatBox from "../components/common/StatBox";
import AlertBox from "../components/common/AlertBox";

export default function DashboardPage({ workflow }) {
  const { statusCounts, goToProjectTracking } = workflow;

  return (
    <PageContainer
      eyebrow="Home"
      title="Tổng quan dự án người dùng"
      description="Theo dõi nhanh số lượng dự án theo từng trạng thái và điều hướng sang trang theo dõi dự án khi cần xem chi tiết."
      rightNode={
        <button
          onClick={goToProjectTracking}
          className="rounded-[5px] border border-[#B8860B] bg-[#FDF6E3] px-[22px] py-[9px] text-[13px] font-bold text-[#B8860B] transition hover:bg-[#faefd0]"
        >
          Gói thầu của tôi
        </button>
      }
    >
      <AlertBox type="warn">
        Chào mừng, Sở Nội vụ tỉnh X. Theo dõi nhanh số lượng dự án, trạng thái hồ sơ và chuyển sang luồng tạo dự án hoặc theo dõi chi tiết khi cần.
      </AlertBox>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <StatBox label="Tổng dự án" value={statusCounts.total} sub="Toàn bộ dự án của người dùng" color="#C0161D" icon="▣" />
        <StatBox label="Dự án đã tạo" value={statusCounts.created} sub="Mới khởi tạo, chưa upload" color="#707068" icon="◫" />
        <StatBox label="Đang diễn ra" value={statusCounts.ongoing} sub="Đang thực hiện các mốc hồ sơ" color="#B8860B" icon="◧" />
        <StatBox label="Chờ duyệt" value={statusCounts.pendingApproval} sub="Đã đủ hồ sơ, chờ kiểm tra cuối" color="#1B4F8A" icon="◩" />
        <StatBox label="Hoàn thành" value={statusCounts.completed} sub="Đã đối soát và chốt hồ sơ" color="#1A6B3A" icon="✓" />
        <StatBox label="Đã huỷ" value={statusCounts.cancelled} sub="Không tiếp tục xử lý" color="#C0161D" icon="✕" />
      </div>
    </PageContainer>
  );
}
