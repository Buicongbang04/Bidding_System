import PageContainer from "../components/common/PageContainer";
import SectionCard from "../components/common/SectionCard";
import LoadingOverlay from "../components/common/LoadingOverlay";
import ProjectForm from "../components/upload/ProjectForm";
import UploadCard from "../components/upload/UploadCard";
import UploadProgress from "../components/upload/UploadProgress";

export default function UploadWorkflowPage({ workflow }) {
  const {
    documentConfigs,
    projectForm,
    setProjectForm,
    projectId,
    documents,
    logs,
    globalLoading,
    globalLoadingText,
    progressCount,
    progressPercent,
    allValidated,
    anyError,
    createProjectHandler,
    selectFile,
    runDocumentWorkflow,
    validateWholeProject
  } = workflow;

  const canValidateProject = allValidated && !anyError && !!projectId;

  return (
    <>
      <LoadingOverlay visible={globalLoading} text={globalLoadingText} />

      <PageContainer
        title="Upload hồ sơ demo"
        description="Người dùng upload từng loại văn bản. Khi đủ 3 loại giấy tờ và toàn bộ bước xử lý đều hợp lệ, hệ thống sẽ chuyển sang dashboard thông báo kiểm tra thành công."
        rightNode={
          <UploadProgress
            percent={progressPercent}
            count={progressCount}
            total={documentConfigs.length}
          />
        }
      >
        <SectionCard title="Thông tin project">
          <ProjectForm
            value={projectForm}
            onChange={setProjectForm}
            onCreate={createProjectHandler}
            loading={globalLoading}
            projectId={projectId}
          />
        </SectionCard>

        <div className="grid gap-6 lg:grid-cols-[1.6fr_1fr]">
          <div className="space-y-4">
            {documentConfigs.map((doc) => (
              <UploadCard
                key={doc.key}
                docConfig={doc}
                docState={documents[doc.key]}
                onSelectFile={selectFile}
                onStartWorkflow={runDocumentWorkflow}
                disabled={globalLoading || !projectId}
              />
            ))}
          </div>

          <div className="space-y-6">
            <SectionCard title="Điều kiện để qua dashboard">
              <div className="space-y-3 text-sm text-slate-600">
                <div
                  className={`rounded-2xl p-4 ring-1 ${
                    progressCount === documentConfigs.length
                      ? "bg-emerald-50 text-emerald-700 ring-emerald-200"
                      : "bg-slate-50 text-slate-600 ring-slate-200"
                  }`}
                >
                  1. Đã xử lý hợp lệ đủ 3 loại văn bản bắt buộc
                </div>

                <div
                  className={`rounded-2xl p-4 ring-1 ${
                    !anyError && progressCount > 0
                      ? "bg-emerald-50 text-emerald-700 ring-emerald-200"
                      : "bg-slate-50 text-slate-600 ring-slate-200"
                  }`}
                >
                  2. Không có lỗi extract, parse hoặc validate document
                </div>

                <div
                  className={`rounded-2xl p-4 ring-1 ${
                    canValidateProject
                      ? "bg-emerald-50 text-emerald-700 ring-emerald-200"
                      : "bg-slate-50 text-slate-600 ring-slate-200"
                  }`}
                >
                  3. Sẵn sàng kiểm tra chéo toàn project
                </div>
              </div>

              <button
                onClick={validateWholeProject}
                disabled={!canValidateProject || globalLoading}
                className="mt-4 w-full rounded-2xl bg-emerald-600 px-4 py-3 text-sm font-medium text-white hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-300"
              >
                Kiểm tra toàn bộ hồ sơ
              </button>
            </SectionCard>

            <SectionCard title="Nhật ký xử lý">
              <div className="space-y-3">
                {logs.map((item, index) => (
                  <div
                    key={`${item}-${index}`}
                    className="rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-600"
                  >
                    {item}
                  </div>
                ))}
              </div>
            </SectionCard>
          </div>
        </div>
      </PageContainer>
    </>
  );
}