export default function ProjectForm({
  value,
  onChange,
  onCreate,
  loading,
  projectId,
  submitLabel = "Tạo project"
}) {
  const handleFieldChange = (field, fieldValue) => {
    onChange((prev) => ({
      ...prev,
      [field]: fieldValue
    }));
  };

  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div>
        <label className="text-[13px] font-semibold text-[#383830]">
          Mã dự án <span className="text-[#C0161D]">*</span>
        </label>
        <input
          value={value.code}
          onChange={(e) => handleFieldChange("code", e.target.value)}
          className="mt-2 w-full rounded-[5px] border border-[#C8C8C2] bg-white px-3 py-[9px] text-[13px] outline-none focus:border-[#B8860B]"
        />
      </div>

      <div>
        <label className="text-[13px] font-semibold text-[#383830]">
          Tên dự án <span className="text-[#C0161D]">*</span>
        </label>
        <input
          value={value.name}
          onChange={(e) => handleFieldChange("name", e.target.value)}
          className="mt-2 w-full rounded-[5px] border border-[#C8C8C2] bg-white px-3 py-[9px] text-[13px] outline-none focus:border-[#B8860B]"
        />
      </div>

      <div>
        <label className="text-[13px] font-semibold text-[#383830]">
          Chủ đầu tư <span className="text-[#C0161D]">*</span>
        </label>
        <input
          value={value.investor_name}
          onChange={(e) => handleFieldChange("investor_name", e.target.value)}
          className="mt-2 w-full rounded-[5px] border border-[#C8C8C2] bg-white px-3 py-[9px] text-[13px] outline-none focus:border-[#B8860B]"
        />
      </div>

      <div className="md:col-span-3 flex flex-wrap items-center gap-3">
        <button
          onClick={onCreate}
          disabled={loading || !!projectId}
          className="rounded-[5px] border border-[#C0161D] bg-[#C0161D] px-[22px] py-[9px] text-[13px] font-bold text-white hover:bg-[#a40f15] disabled:cursor-not-allowed disabled:border-[#DDDDD8] disabled:bg-[#EEEEEA] disabled:text-[#A0A09A]"
        >
          {projectId ? "Đã tạo project" : loading ? "Đang tạo..." : submitLabel}
        </button>

        {projectId ? (
          <div className="rounded-[5px] border border-[#86efac] bg-[#F0F9F4] px-4 py-3 text-sm text-[#1A6B3A]">
            Project ID: {projectId}
          </div>
        ) : null}
      </div>
    </div>
  );
}
