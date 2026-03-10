import PageContainer from "../components/common/PageContainer";
import SectionCard from "../components/common/SectionCard";
import SuccessSummary from "../components/dashboard/SuccessSummary";
import DocumentResultCard from "../components/dashboard/DocumentResultCard";
import ProjectValidationCard from "../components/dashboard/ProjectValidationCard";

export default function SuccessDashboardPage({ workflow }) {
  const {
    documentConfigs,
    documents,
    projectForm,
    projectValidationResult,
    resetToUpload
  } = workflow;

  return (
    <PageContainer
      title="Kiểm tra hồ sơ thành công"
      description="Hồ sơ đã đủ 3 loại văn bản bắt buộc, toàn bộ bước extract, parse, validate tài liệu và kiểm tra chéo project đều đã hoàn tất."
      rightNode={
        <button
          onClick={resetToUpload}
          className="rounded-2xl border border-slate-200 px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          Quay lại màn hình upload
        </button>
      }
    >
      <SuccessSummary projectForm={projectForm} />

      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <SectionCard title="Danh sách hồ sơ đã xác nhận">
          <div className="grid gap-4">
            {documentConfigs.map((doc) => (
              <DocumentResultCard
                key={doc.key}
                title={doc.title}
                shortTitle={doc.shortTitle}
                state={documents[doc.key]}
              />
            ))}
          </div>
        </SectionCard>

        <ProjectValidationCard projectValidationResult={projectValidationResult} />
      </div>
    </PageContainer>
  );
}