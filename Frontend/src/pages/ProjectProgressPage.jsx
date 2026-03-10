import LoadingOverlay from "../components/common/LoadingOverlay";
import PageContainer from "../components/common/PageContainer";
import SectionCard from "../components/common/SectionCard";
import UploadCard from "../components/upload/UploadCard";
import SecTitle from "../components/common/SecTitle";

function ResultPanel({ title, children }) {
  return (
    <div className="rounded-[5px] border border-[#DDDDD8] bg-[#F7F7F5] p-4">
      <div className="text-[11px] font-bold uppercase tracking-[0.06em] text-[#707068]">
        {title}
      </div>
      <div className="mt-3">{children}</div>
    </div>
  );
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "Không có dữ liệu";
  }

  if (typeof value === "object") {
    return JSON.stringify(value);
  }

  return String(value);
}

function BulletList({ data }) {
  const entries = Object.entries(data || {});

  if (!entries.length) {
    return <div className="text-sm text-[#707068]">Không có dữ liệu.</div>;
  }

  return (
    <ul className="space-y-2 text-sm text-[#383830]">
      {entries.map(([key, value]) => (
        <li key={key} className="flex gap-2">
          <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#C0161D]" />
          <span>
            <span className="font-semibold text-[#252520]">{key}:</span>{" "}
            {formatValue(value)}
          </span>
        </li>
      ))}
    </ul>
  );
}

function ErrorList({ errors }) {
  if (!errors?.length) {
    return null;
  }

  return (
    <ul className="mt-3 space-y-2 text-sm text-[#383830]">
      {errors.map((error, index) => (
        <li key={`${error.message || "error"}-${index}`} className="flex gap-2">
          <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-[#C0161D]" />
          <span>
            <span className="font-semibold text-[#252520]">
              {error.field || error.location || `Lỗi ${index + 1}`}:
            </span>{" "}
            {error.message || JSON.stringify(error)}
          </span>
        </li>
      ))}
    </ul>
  );
}

function ValidationStatus({ status }) {
  const isValid = status === "valid";

  return (
    <span
      className={`rounded-[3px] border px-[10px] py-[3px] text-[11px] font-bold tracking-[0.03em] ${
        isValid
          ? "border-[#86efac] bg-[#F0F9F4] text-[#1A6B3A]"
          : "border-[#fca5a5] bg-[#FDF2F2] text-[#C0161D]"
      }`}
    >
      {isValid ? "valid" : "invalid"}
    </span>
  );
}

function TimelineStep({ step, state, index, isLast }) {
  const circleMap = {
    done: "border-[#1A6B3A] bg-[#1A6B3A] text-white",
    current: "border-[#D4A017] bg-[#C0161D] text-white shadow-[0_0_0_2px_#D4A017]",
    error: "border-[#C0161D] bg-[#C0161D] text-white",
    locked: "border-[#DDDDD8] bg-[#DDDDD8] text-[#A0A09A]"
  };

  const lineMap = {
    done: "bg-[#1A6B3A]",
    current: "bg-[#DDDDD8]",
    error: "bg-[#C0161D]",
    locked: "bg-[#DDDDD8]"
  };

  return (
    <div className="relative flex min-w-0 flex-1 flex-col items-center text-center">
      {!isLast ? (
        <div
          className={`absolute left-1/2 top-[14px] h-[2px] w-full ${lineMap[state]}`}
          style={{ transform: "translateX(24px)" }}
        />
      ) : null}

      <div
        className={`relative z-10 flex h-7 w-7 items-center justify-center rounded-full border text-xs font-bold ${
          circleMap[state]
        }`}
      >
        {state === "done" ? "✓" : index + 1}
      </div>

      <div
        className={`mt-4 text-[12px] font-semibold ${
          state === "current"
            ? "text-[#C0161D]"
            : state === "done"
              ? "text-[#1A6B3A]"
              : state === "error"
                ? "text-[#C0161D]"
                : "text-[#A0A09A]"
        }`}
      >
        {step.title}
      </div>
    </div>
  );
}

export default function ProjectProgressPage({ workflow }) {
  const {
    currentProject,
    currentProjectTimeline,
    activeDocumentConfig,
    currentDocumentConfig,
    currentDocumentIndex,
    maxAccessibleDocumentIndex,
    documents,
    globalLoading,
    globalLoadingText,
    allValidated,
    anyError,
    projectValidationResult,
    selectFile,
    runDocumentWorkflow,
    validateWholeProject,
    cancelCurrentProject,
    goToPreviousStep,
    goToNextStep
  } = workflow;

  if (!currentProject) {
    return null;
  }

  const canValidateProject = allValidated && !anyError;
  const isProjectClosed =
    currentProject.status === "Huỷ" ||
    currentProject.status === "Thành công" ||
    currentProject.status === "Kết thúc";
  const currentDocumentState = currentDocumentConfig
    ? documents[currentDocumentConfig.key]
    : null;
  const hasDocumentResult =
    !!currentDocumentState?.parsedData || !!currentDocumentState?.validationResult;
  const isViewingCurrentStep =
    !!currentDocumentConfig &&
    !!activeDocumentConfig &&
    currentDocumentConfig.key === activeDocumentConfig.key;
  const canGoPrevious = currentDocumentIndex > 0;
  const canGoNext = currentDocumentIndex < maxAccessibleDocumentIndex;

  return (
    <>
      <LoadingOverlay visible={globalLoading} text={globalLoadingText} />

      <PageContainer
        eyebrow="Project Progress"
        title={currentProject.name}
        description={`Mã dự án ${currentProject.code}. Upload đúng loại tài liệu theo từng mốc, hệ thống sẽ chỉ mở khóa bước tiếp theo khi bước hiện tại hợp lệ.`}
        rightNode={
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={cancelCurrentProject}
              disabled={isProjectClosed}
              className="rounded-2xl border border-rose-200 px-4 py-3 text-sm font-medium text-rose-600 transition hover:bg-rose-50 disabled:cursor-not-allowed disabled:border-slate-200 disabled:text-slate-400"
            >
              Huỷ dự án
            </button>
          </div>
        }
      >
        <div className="grid gap-6">
          <SectionCard>
            <SecTitle
              title="Quy trình mở thầu"
              sub="Theo dõi 4 bước xử lý hồ sơ theo đúng quy trình"
            />
            <div className="overflow-x-auto pb-2">
              <div className="flex min-w-[720px] items-start px-2">
              {currentProjectTimeline.map((step, index) => (
                <TimelineStep
                  key={step.key}
                  step={step}
                  state={step.state}
                  index={index}
                  isLast={index === currentProjectTimeline.length - 1}
                />
              ))}
              </div>
            </div>
          </SectionCard>
        </div>

        <SectionCard
          title={
            currentDocumentConfig
              ? `Mốc đang xem: ${currentDocumentConfig.title}`
              : "Kiểm tra chéo toàn bộ hồ sơ"
          }
        >
          <SecTitle
            title={
              currentDocumentConfig
                ? `Mốc đang xem: ${currentDocumentConfig.title}`
                : "Kiểm tra chéo toàn bộ hồ sơ"
            }
            sub="Tải lên đúng loại tài liệu để hệ thống xử lý theo pipeline AI"
          />
          {currentDocumentConfig ? (
            <div className="mx-auto max-w-5xl space-y-6">
              {!isViewingCurrentStep ? (
                <div className="rounded-[5px] border border-[#E8C84A] bg-[#FFF8E8] px-4 py-3 text-sm text-[#996600]">
                  Bạn đang xem lại thông tin của bước trước. Chỉ mốc đang mở mới cho phép upload và kiểm tra tiếp.
                </div>
              ) : null}

              <UploadCard
                docConfig={currentDocumentConfig}
                docState={currentDocumentState}
                onSelectFile={selectFile}
                onStartWorkflow={runDocumentWorkflow}
                disabled={globalLoading || isProjectClosed || !isViewingCurrentStep}
                isCurrentStep={isViewingCurrentStep}
              />

              {hasDocumentResult ? (
                <div className="space-y-4">
                  <SecTitle
                    title="Kết quả"
                    sub="Hiển thị dữ liệu parse và kết quả validate sau khi hệ thống xử lý tài liệu"
                  />

                  {currentDocumentState?.parsedData ? (
                    <ResultPanel title="Dữ liệu đã lọc">
                      <BulletList data={currentDocumentState.parsedData} />
                    </ResultPanel>
                  ) : null}

                  {currentDocumentState?.validationResult ? (
                    <ResultPanel title="Kết quả Validate">
                      <div className="mb-3 flex flex-wrap items-center gap-3">
                        <span className="text-sm font-semibold text-[#252520]">
                          Trạng thái:
                        </span>
                        <ValidationStatus
                          status={currentDocumentState.validationResult?.validation_status}
                        />
                      </div>

                      {currentDocumentState.validationResult?.validation_status !==
                      "valid" ? (
                        <ErrorList
                          errors={currentDocumentState.validationResult?.errors}
                        />
                      ) : null}
                    </ResultPanel>
                  ) : null}
                </div>
              ) : null}

              <div className="flex flex-wrap items-center justify-between gap-3 border-t border-[#EEEEEA] pt-4">
                <button
                  onClick={goToPreviousStep}
                  disabled={!canGoPrevious}
                  className="rounded-[5px] border border-[#C8C8C2] bg-[#F7F7F5] px-[22px] py-[9px] text-[13px] font-bold text-[#505048] transition hover:bg-[#EEEEEA] disabled:cursor-not-allowed disabled:border-[#DDDDD8] disabled:bg-[#EEEEEA] disabled:text-[#A0A09A]"
                >
                  Quay về
                </button>

                <button
                  onClick={goToNextStep}
                  disabled={!canGoNext}
                  className="rounded-[5px] border border-[#C0161D] bg-[#C0161D] px-[22px] py-[9px] text-[13px] font-bold text-white transition hover:bg-[#a40f15] disabled:cursor-not-allowed disabled:border-[#DDDDD8] disabled:bg-[#EEEEEA] disabled:text-[#A0A09A]"
                >
                  Tiếp tục
                </button>
              </div>
            </div>
          ) : (
            <div className="mx-auto max-w-3xl space-y-4">
              <div className="rounded-[5px] border border-[#E8C84A] bg-[#FDF6E3] p-5 text-sm text-[#505048]">
                Toàn bộ tài liệu bắt buộc đã hợp lệ. Thực hiện kiểm tra chéo để chốt trạng thái cuối cùng của dự án.
              </div>
              <button
                onClick={validateWholeProject}
                disabled={!canValidateProject || globalLoading || isProjectClosed}
                className="rounded-[5px] border border-[#B8860B] bg-[#B8860B] px-[22px] py-[9px] text-[13px] font-bold text-white transition hover:bg-[#9b710a] disabled:cursor-not-allowed disabled:border-[#DDDDD8] disabled:bg-[#EEEEEA] disabled:text-[#A0A09A]"
              >
                {projectValidationResult ? "Đã kiểm tra toàn bộ hồ sơ" : "Kiểm tra toàn bộ hồ sơ"}
              </button>
            </div>
          )}
        </SectionCard>
      </PageContainer>
    </>
  );
}
