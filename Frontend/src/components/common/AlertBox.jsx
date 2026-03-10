const STYLES = {
  info: "border-l-[#1B4F8A] bg-[#EFF4FB] text-[#383830]",
  warn: "border-l-[#996600] bg-[#FEFAE8] text-[#383830]",
  error: "border-l-[#C0161D] bg-[#FDF2F2] text-[#383830]",
  gold: "border-l-[#B8860B] bg-[#FDF6E3] text-[#383830]"
};

export default function AlertBox({ type = "info", children }) {
  return (
    <div className={`rounded-[5px] border-l-4 px-[14px] py-3 text-xs leading-7 ${STYLES[type]}`}>
      {children}
    </div>
  );
}
