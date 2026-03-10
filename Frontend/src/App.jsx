import { useTenderWorkflow } from "./hooks/useTenderWorkflow";
import MainLayout from "./layouts/MainLayout";
import DashboardPage from "./pages/DashboardPage";
import ProjectProgressPage from "./pages/ProjectProgressPage";
import ProjectTrackingPage from "./pages/ProjectTrackingPage";
import ProjectForm from "./components/upload/ProjectForm";
import AlertBox from "./components/common/AlertBox";
function CreateProjectModal({ workflow }) {
  const {
    isCreateProjectModalOpen,
    closeCreateProjectModal,
    projectForm,
    setProjectForm,
    createProjectHandler,
    globalLoading
  } = workflow;

  if (!isCreateProjectModalOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-[#252520]/60 p-4">
      <div className="w-full max-w-3xl rounded-md border border-[#DDDDD8] bg-white p-6 shadow-2xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="text-[11px] uppercase tracking-[0.08em] text-[#C0161D]">
              New Project
            </div>
            <h2 className="mt-2 text-2xl font-black text-[#252520]">
              Tạo dự án mới
            </h2>
            <p className="mt-2 text-sm text-[#707068]">
              Điền thông tin cơ bản trước khi chuyển sang trang theo dõi tiến độ và upload hồ sơ theo từng mốc.
            </p>
          </div>

          <button
            onClick={closeCreateProjectModal}
            className="rounded-[5px] border border-[#DDDDD8] px-4 py-2 text-[13px] font-bold text-[#505048] hover:bg-[#F7F7F5]"
          >
            Đóng
          </button>
        </div>

        <div className="mt-6">
          <ProjectForm
            value={projectForm}
            onChange={setProjectForm}
            onCreate={createProjectHandler}
            loading={globalLoading}
            submitLabel="Tạo dự án và mở tiến độ"
          />
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const workflow = useTenderWorkflow();

  const handleNavigate = (target) => {
    if (target === "dashboard") workflow.goToDashboard();
    else if (target === "project-tracking") workflow.goToProjectTracking();
    else if (target === "project-progress" && workflow.currentProjectId) {
      workflow.openProject(workflow.currentProjectId);
    }
  };

  return (
    <MainLayout
      page={workflow.page}
      onNavigate={handleNavigate}
      currentProjectCode={workflow.currentProject?.code}
    >
      {workflow.page === "project-progress" ? (
        <ProjectProgressPage workflow={workflow} />
      ) : workflow.page === "project-tracking" ? (
        <ProjectTrackingPage workflow={workflow} />
      ) : (
        <DashboardPage workflow={workflow} />
      )}
      <CreateProjectModal workflow={workflow} />
    </MainLayout>
  );
}
