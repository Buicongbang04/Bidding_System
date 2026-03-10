import StatusBadge from "../common/StatusBadge";
import PipelineStatus from "./PipelineStatus";
import { getStatusBadgeType } from "../../utils/helpers";

export default function UploadCard({
  docConfig,
  docState,
  onSelectFile,
  onStartWorkflow,
  disabled,
  isCurrentStep = false
}) {
  const badgeType = getStatusBadgeType(docState);

  return (
    <div className="rounded-md border border-[#DDDDD8] bg-white p-6 shadow-[0_1px_4px_rgba(0,0,0,0.07)]">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className="rounded-[3px] bg-[#EEEEEA] px-3 py-1 text-[11px] font-bold text-[#707068]">
              {docConfig.shortTitle}
            </span>
            <StatusBadge type={badgeType} />
            {isCurrentStep ? (
              <span className="rounded-[3px] border border-[#E8C84A] bg-[#FFF8E8] px-3 py-1 text-[11px] font-bold text-[#996600]">
                Mốc đang mở
              </span>
            ) : null}
          </div>

          <h3 className="text-xl font-extrabold text-[#252520]">{docConfig.title}</h3>
          <p className="max-w-2xl text-sm text-[#707068]">{docConfig.description}</p>

          {docState.file ? (
            <div className="text-sm text-[#707068]">
              File hiện tại:{" "}
              <span className="font-semibold text-[#252520]">{docState.file.name}</span>
            </div>
          ) : null}

          {docState.hasError ? (
            <div className="rounded-[5px] border border-[#fca5a5] bg-[#FDF2F2] px-4 py-3 text-sm text-[#C0161D]">
              {docState.errorMessage}
            </div>
          ) : null}
        </div>

        <div className="w-full max-w-xs space-y-3">
          <label className="block">
            <span className="mb-2 block text-[13px] font-semibold text-[#383830]">
              Tệp tài liệu <span className="text-[#C0161D]">*</span>
            </span>
            <input
              type="file"
              className="block w-full rounded-[6px] border-2 border-dashed border-[#C8C8C2] bg-[#F7F7F5] px-3 py-3 text-[12px] text-[#505048] file:mr-4 file:rounded-[5px] file:border file:border-[#C0161D] file:bg-[#C0161D] file:px-4 file:py-2 file:text-[12px] file:font-bold file:text-white hover:file:bg-[#a40f15]"
              onChange={(e) => onSelectFile(docConfig.key, e.target.files?.[0] || null)}
              disabled={disabled}
            />
          </label>

          <button
            onClick={() => onStartWorkflow(docConfig.key)}
            disabled={!docState.file || disabled}
            className="w-full rounded-[5px] border border-[#B8860B] bg-[#B8860B] px-[22px] py-[9px] text-[13px] font-bold text-white hover:bg-[#9b710a] disabled:cursor-not-allowed disabled:border-[#DDDDD8] disabled:bg-[#EEEEEA] disabled:text-[#A0A09A]"
          >
            {docState.validated ? "Đã hoàn thành" : "Upload và xử lý"}
          </button>
        </div>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-4">
        <PipelineStatus
          label="Upload"
          done={docState.uploaded}
          active={false}
          error={docState.hasError && !docState.extracted}
        />
        <PipelineStatus
          label="Extract text"
          done={docState.extracted}
          active={docState.extracting}
          error={docState.hasError && !docState.parsed}
        />
        <PipelineStatus
          label="Parse schema"
          done={docState.parsed}
          active={docState.parsing}
          error={docState.hasError && !docState.validated && docState.extracted}
        />
        <PipelineStatus
          label="Validate"
          done={docState.validated}
          active={docState.validating}
          error={docState.hasError && !docState.validated}
        />
      </div>
    </div>
  );
}
