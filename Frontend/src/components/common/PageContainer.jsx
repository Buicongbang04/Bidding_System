export default function PageContainer({
  eyebrow = "Tender AI MVP",
  title,
  description,
  rightNode,
  children
}) {
  return (
    <div className="space-y-6">
      <div className="rounded-md border border-[#DDDDD8] bg-white p-6 shadow-[0_1px_4px_rgba(0,0,0,0.07)]">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <div className="text-[11px] uppercase tracking-[0.12em] text-[#C0161D]">
              {eyebrow}
            </div>
            <h1 className="mt-2 text-[28px] font-black text-[#252520]">{title}</h1>
            <p className="mt-2 max-w-3xl text-sm text-[#707068]">{description}</p>
          </div>
          {rightNode}
        </div>
      </div>

      {children}
    </div>
  );
}
