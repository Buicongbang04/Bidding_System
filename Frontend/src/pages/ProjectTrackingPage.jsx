import PageContainer from "../components/common/PageContainer";
import SectionCard from "../components/common/SectionCard";
import SecTitle from "../components/common/SecTitle";

const DISPLAY_STATUS_STYLES = {
  "Đã tạo": "bg-slate-100 text-slate-700 ring-slate-200",
  "Đang diễn ra": "bg-amber-100 text-amber-800 ring-amber-200",
  "Chờ duyệt": "bg-sky-100 text-sky-800 ring-sky-200",
  "Hoàn thành": "bg-emerald-100 text-emerald-800 ring-emerald-200",
  "Huỷ": "bg-rose-100 text-rose-700 ring-rose-200",
  "Chờ rà soát": "bg-orange-100 text-orange-700 ring-orange-200"
};

function TrackingStatusBadge({ status }) {
  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ring-1 ${
        DISPLAY_STATUS_STYLES[status] || DISPLAY_STATUS_STYLES["Đã tạo"]
      }`}
    >
      {status}
    </span>
  );
}

export default function ProjectTrackingPage({ workflow }) {
  const { projects, documentConfigs, openProject, openCreateProjectModal } = workflow;

  return (
    <PageContainer
      eyebrow="Project Tracking"
      title="Theo dõi dự án"
      description="Danh sách toàn bộ dự án hiện có và trạng thái xử lý của từng dự án."
      rightNode={
        <button
          onClick={openCreateProjectModal}
          className="rounded-[5px] border border-[#C0161D] bg-[#C0161D] px-[22px] py-[9px] text-[13px] font-bold text-white transition hover:bg-[#a40f15]"
        >
          Tạo gói thầu mới
        </button>
      }
    >
      <SectionCard
        title="Dự án hiện có"
        extra={<div className="text-sm text-slate-500">{projects.length} dự án</div>}
      >
        <SecTitle
          title="Dự án hiện có"
          sub="Hiển thị trạng thái xử lý của từng dự án trong hệ thống"
        />
        {projects.length === 0 ? (
          <div className="rounded-md border border-dashed border-[#DDDDD8] bg-[#F7F7F5] p-8 text-center text-sm text-[#707068]">
            Chưa có dự án nào để theo dõi.
          </div>
        ) : (
          <div className="grid gap-4">
            {projects.map((project) => (
              <button
                key={project.id}
                onClick={() => openProject(project.id)}
                className="grid gap-5 rounded-md border border-[#DDDDD8] bg-white p-5 text-left transition hover:border-[#B8860B] hover:shadow-[0_1px_8px_rgba(0,0,0,0.09)] xl:grid-cols-[minmax(0,1.7fr)_minmax(320px,0.9fr)]"
              >
                <div className="space-y-3">
                  <div className="flex flex-wrap items-center gap-3">
                    <span className="rounded-[3px] bg-[#EEEEEA] px-3 py-1 font-mono text-[11px] font-bold text-[#707068]">
                      {project.code}
                    </span>
                    <TrackingStatusBadge status={project.displayStatus} />
                  </div>

                  <div>
                    <h3 className="text-xl font-extrabold text-[#252520]">{project.name}</h3>
                    <p className="mt-1 text-sm text-[#707068]">
                      Chủ đầu tư: {project.investor_name}
                    </p>
                  </div>
                </div>

                <div className="grid gap-3 sm:grid-cols-3 xl:grid-cols-1">
                  <div className="rounded-[5px] border border-[#DDDDD8] bg-[#F7F7F5] px-4 py-3">
                    <div className="text-[11px] uppercase tracking-[0.06em] text-[#707068]">
                      Tiến độ tài liệu
                    </div>
                    <div className="mt-2 text-lg font-extrabold text-[#252520]">
                      {project.progressCount}/{documentConfigs.length}
                    </div>
                  </div>

                  <div className="rounded-[5px] border border-[#DDDDD8] bg-[#F7F7F5] px-4 py-3">
                    <div className="text-[11px] uppercase tracking-[0.06em] text-[#707068]">
                      Cập nhật gần nhất
                    </div>
                    <div className="mt-2 text-sm font-semibold text-[#252520]">
                      {project.updatedLabel}
                    </div>
                  </div>

                  <div className="rounded-[5px] border border-[#C0161D] bg-[#C0161D] px-4 py-3 text-white">
                    <div className="text-[11px] uppercase tracking-[0.06em] text-white/70">
                      Hành động
                    </div>
                    <div className="mt-2 text-sm font-bold">Mở trang tiến độ</div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </SectionCard>
    </PageContainer>
  );
}
