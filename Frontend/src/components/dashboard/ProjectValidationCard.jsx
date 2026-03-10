export default function ProjectValidationCard({ projectValidationResult }) {
  const result = projectValidationResult?.validation_result;

  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
      <h2 className="text-lg font-semibold text-slate-900">Kết quả kiểm tra chéo hồ sơ</h2>

      {!result ? (
        <div className="mt-4 text-sm text-slate-500">Chưa có dữ liệu validate project.</div>
      ) : (
        <div className="mt-4 space-y-3 text-sm text-slate-600">
          <div className="rounded-2xl bg-slate-50 p-4">
            Trạng thái:{" "}
            <span className="font-semibold text-emerald-700">
              {result.validation_status}
            </span>
          </div>

          <div className="rounded-2xl bg-slate-50 p-4">
            Số lỗi: <span className="font-semibold">{result.total_errors}</span>
          </div>

          <div className="rounded-2xl bg-slate-50 p-4">
            Số cảnh báo: <span className="font-semibold">{result.total_warnings}</span>
          </div>
        </div>
      )}
    </div>
  );
}