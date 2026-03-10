export default function Breadcrumb({ items = [] }) {
  return (
    <div className="border-b border-[#DDDDD8] bg-[#F7F7F5]">
      <div className="mx-auto flex w-full max-w-[1400px] flex-wrap items-center gap-2 px-4 py-2 text-xs">
        <span className="text-[#A0A09A]">⌂</span>
        {items.map((item, index) => (
          <div key={`${item.label}-${index}`} className="flex items-center gap-2">
            <span className="text-[#C8C8C2]">›</span>
            <span
              className={index === items.length - 1 ? "font-semibold text-[#C0161D]" : "text-[#707068]"}
            >
              {item.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
