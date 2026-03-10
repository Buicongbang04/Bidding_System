import GovHeader from "../components/common/GovHeader";
import Breadcrumb from "../components/common/Breadcrumb";
import GovFooter from "../components/common/GovFooter";

function getBreadcrumbs(page, currentProjectCode) {
  if (page === "project-tracking") {
    return [{ label: "Gói thầu của tôi" }];
  }

  if (page === "project-progress") {
    return [{ label: "Gói thầu của tôi" }, { label: currentProjectCode || "Mã dự án" }];
  }

  return [{ label: "Trang chủ" }];
}

export default function MainLayout({
  children,
  page,
  onNavigate,
  currentProjectCode
}) {
  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#252520]">
      <GovHeader page={page} onNavigate={onNavigate} />
      <Breadcrumb items={getBreadcrumbs(page, currentProjectCode)} />

      <div className="mx-auto w-full max-w-[1400px] px-4 py-6">
        <main>{children}</main>
      </div>

      <GovFooter />
    </div>
  );
}
