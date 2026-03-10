export default function SecTitle({ title, sub, action }) {
  return (
    <div className="mb-[18px] flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
      <div className="flex items-start gap-3">
        <div className="mt-1 flex flex-col gap-1">
          <span className="h-4 w-1 rounded-[2px] bg-[#C0161D]" />
          <span className="h-2 w-1 rounded-[2px] bg-[#B8860B]" />
        </div>
        <div>
          <div className="text-[17px] font-extrabold tracking-[-0.01em] text-[#252520]">
            {title}
          </div>
          {sub ? <div className="mt-1 text-xs text-[#707068]">{sub}</div> : null}
        </div>
      </div>
      {action}
    </div>
  );
}
