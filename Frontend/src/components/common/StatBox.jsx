export default function StatBox({ label, value, sub, color = "#C0161D", icon = "■" }) {
  return (
    <div className="rounded-md border border-[#DDDDD8] bg-white px-5 py-[18px] shadow-[0_1px_4px_rgba(0,0,0,0.07)]">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="text-[11px] font-bold uppercase tracking-[0.06em] text-[#707068]">
            {label}
          </div>
          <div className="mt-3 text-[28px] font-black" style={{ color }}>
            {value}
          </div>
          <div className="mt-1 text-[11px] text-[#A0A09A]">{sub}</div>
        </div>
        <div
          className="flex h-11 w-11 items-center justify-center rounded-lg border text-xl"
          style={{
            color,
            backgroundColor: `${color}14`,
            borderColor: `${color}30`
          }}
        >
          {icon}
        </div>
      </div>
    </div>
  );
}
