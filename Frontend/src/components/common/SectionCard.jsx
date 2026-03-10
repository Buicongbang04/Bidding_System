export default function SectionCard({ title, children, extra }) {
  return (
    <div className="rounded-md border border-[#DDDDD8] bg-white p-5 shadow-[0_1px_4px_rgba(0,0,0,0.07)]">
      {title || extra ? (
        <div className="flex items-center justify-between gap-4">
          {title ? <h2 className="text-base font-extrabold text-[#252520]">{title}</h2> : <div />}
          {extra}
        </div>
      ) : null}
      <div className={title || extra ? "mt-4" : ""}>{children}</div>
    </div>
  );
}
