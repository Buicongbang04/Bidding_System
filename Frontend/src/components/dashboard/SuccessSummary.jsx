export default function SuccessSummary({ projectForm }) {
  return (
    <div className="grid gap-5 md:grid-cols-3">
      <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div className="text-sm text-slate-500">Project</div>
        <div className="mt-2 text-xl font-semibold text-slate-900">{projectForm.name}</div>
      </div>

      <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div className="text-sm text-slate-500">Tình trạng hồ sơ</div>
        <div className="mt-2 text-xl font-semibold text-emerald-600">Đầy đủ giấy tờ</div>
      </div>

      <div className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div className="text-sm text-slate-500">Kết quả kiểm tra</div>
        <div className="mt-2 text-xl font-semibold text-emerald-600">Kiểm tra thành công</div>
      </div>
    </div>
  );
}