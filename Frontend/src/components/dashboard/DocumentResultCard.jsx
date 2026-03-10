export default function DocumentResultCard({ title, shortTitle, state }) {
  return (
    <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm text-emerald-700">{shortTitle}</div>
          <div className="mt-1 font-semibold text-slate-900">{title}</div>
          <div className="mt-1 text-sm text-slate-600">{state.file?.name}</div>
        </div>
        <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-200">
          Ready
        </span>
      </div>
    </div>
  );
}