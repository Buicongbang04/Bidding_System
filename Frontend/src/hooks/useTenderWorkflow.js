import { useMemo, useState } from "react";
import {
  DOCUMENT_TYPES,
  INITIAL_PROJECT_FORM,
  createInitialDocumentState
} from "../utils/constants";
import {
  getProgressCount,
  getProgressPercent,
  hasAllRequiredDocuments,
  hasAnyDocumentError,
  isValidationPassed
} from "../utils/helpers";
import { createProject, validateProject } from "../api/projectApi";
import {
  uploadDocument,
  extractText,
  parseDocument,
  validateDocument
} from "../api/documentApi";

const PROJECT_STATUS = {
  ACTIVE: "Đang diễn ra",
  SUCCESS: "Thành công",
  DONE: "Kết thúc",
  CANCELLED: "Huỷ"
};

function getProjectDisplayStatus(project) {
  const progressCount = getProgressCount(project.documents, DOCUMENT_TYPES);
  const allValidated = hasAllRequiredDocuments(project.documents, DOCUMENT_TYPES);

  if (project.status === PROJECT_STATUS.CANCELLED) {
    return "Huỷ";
  }

  if (project.projectValidationResult) {
    return project.projectValidationResult?.validation_result?.validation_status === "valid"
      ? "Hoàn thành"
      : "Chờ rà soát";
  }

  if (allValidated) {
    return "Chờ duyệt";
  }

  if (progressCount === 0) {
    return "Đã tạo";
  }

  return "Đang diễn ra";
}

function formatProjectTime(dateString) {
  return new Intl.DateTimeFormat("vi-VN", {
    hour: "2-digit",
    minute: "2-digit",
    day: "2-digit",
    month: "2-digit",
    year: "numeric"
  }).format(new Date(dateString));
}

export function useTenderWorkflow() {
  const [projectForm, setProjectForm] = useState(INITIAL_PROJECT_FORM);
  const [projects, setProjects] = useState([]);
  const [currentProjectId, setCurrentProjectId] = useState("");
  const [selectedDocumentIndex, setSelectedDocumentIndex] = useState(0);
  const [page, setPage] = useState("dashboard");
  const [isCreateProjectModalOpen, setIsCreateProjectModalOpen] = useState(false);
  const [globalLoading, setGlobalLoading] = useState(false);
  const [globalLoadingText, setGlobalLoadingText] = useState("Đang xử lý...");

  const currentProject = useMemo(
    () => projects.find((item) => item.id === currentProjectId) || null,
    [projects, currentProjectId]
  );

  const addProjectLog = (projectId, message) => {
    setProjects((prev) =>
      prev.map((project) =>
        project.id === projectId
          ? {
              ...project,
              logs: [message, ...project.logs].slice(0, 12),
              updatedAt: new Date().toISOString()
            }
          : project
      )
    );
  };

  const updateCurrentProject = (updater) => {
    setProjects((prev) =>
      prev.map((project) =>
        project.id === currentProjectId
          ? typeof updater === "function"
            ? updater(project)
            : updater
          : project
      )
    );
  };

  const setDocumentState = (docType, updater) => {
    updateCurrentProject((project) => ({
      ...project,
      updatedAt: new Date().toISOString(),
      documents: {
        ...project.documents,
        [docType]:
          typeof updater === "function"
            ? updater(project.documents[docType])
            : updater
      }
    }));
  };

  const openCreateProjectModal = () => {
    setProjectForm(INITIAL_PROJECT_FORM);
    setIsCreateProjectModalOpen(true);
  };

  const closeCreateProjectModal = () => {
    setIsCreateProjectModalOpen(false);
  };

  const goToDashboard = () => {
    setPage("dashboard");
  };

  const goToProjectTracking = () => {
    setPage("project-tracking");
  };

  const openProject = (projectId) => {
    setCurrentProjectId(projectId);
    const project = projects.find((item) => item.id === projectId);
    if (project) {
      const firstPendingIndex = DOCUMENT_TYPES.findIndex(
        (item) => !project.documents[item.key]?.validated
      );
      setSelectedDocumentIndex(firstPendingIndex >= 0 ? firstPendingIndex : 0);
    }
    setPage("project-progress");
  };

  const createProjectHandler = async () => {
    try {
      setGlobalLoading(true);
      setGlobalLoadingText("Đang tạo project...");
      const response = await createProject(projectForm);

      const now = new Date().toISOString();
      const newProject = {
        id: response.id,
        code: projectForm.code,
        name: projectForm.name,
        investor_name: projectForm.investor_name,
        status: PROJECT_STATUS.ACTIVE,
        createdAt: now,
        updatedAt: now,
        documents: createInitialDocumentState(),
        logs: [
          `Đã tạo dự án thành công: ${projectForm.name}`,
          "Chờ upload tài liệu ở mốc đầu tiên: Kế hoạch lựa chọn nhà thầu."
        ],
        projectValidationResult: null
      };

      setProjects((prev) => [newProject, ...prev]);
      setCurrentProjectId(newProject.id);
      setPage("project-progress");
      setIsCreateProjectModalOpen(false);
    } catch (error) {
      alert(error.message);
    } finally {
      setGlobalLoading(false);
    }
  };

  const selectFile = (docType, file) => {
    setDocumentState(docType, (prev) => ({
      ...prev,
      file,
      hasError: false,
      errorMessage: "",
      documentId: "",
      uploaded: false,
      extracting: false,
      extracted: false,
      parsing: false,
      parsed: false,
      validating: false,
      validated: false,
      extractedTextPreview: "",
      parsedData: null,
      validationResult: null
    }));
  };

  const activeDocumentIndex = useMemo(() => {
    if (!currentProject) return -1;
    return DOCUMENT_TYPES.findIndex((item) => !currentProject.documents[item.key]?.validated);
  }, [currentProject]);

  const activeDocumentConfig = useMemo(() => {
    if (activeDocumentIndex < 0) return null;
    return DOCUMENT_TYPES[activeDocumentIndex] || null;
  }, [activeDocumentIndex]);

  const maxAccessibleDocumentIndex = useMemo(() => {
    if (!currentProject) return 0;
    return activeDocumentIndex >= 0 ? activeDocumentIndex : DOCUMENT_TYPES.length - 1;
  }, [activeDocumentIndex, currentProject]);

  const currentDocumentIndex = useMemo(() => {
    if (!currentProject) return 0;
    return Math.min(selectedDocumentIndex, maxAccessibleDocumentIndex);
  }, [currentProject, maxAccessibleDocumentIndex, selectedDocumentIndex]);

  const currentDocumentConfig = useMemo(() => {
    if (!currentProject) return null;
    return DOCUMENT_TYPES[currentDocumentIndex] || null;
  }, [currentDocumentIndex, currentProject]);

  const runDocumentWorkflow = async (docType) => {
    if (!currentProject) {
      alert("Bạn cần chọn dự án trước.");
      return;
    }

    if (currentProject.status === PROJECT_STATUS.CANCELLED) {
      alert("Dự án đã bị huỷ.");
      return;
    }

    if (activeDocumentConfig && activeDocumentConfig.key !== docType) {
      alert("Bạn cần hoàn thành mốc hiện tại trước khi sang bước tiếp theo.");
      return;
    }

    const current = currentProject.documents[docType];
    if (!current?.file) {
      alert("Bạn chưa chọn file.");
      return;
    }

    try {
      setDocumentState(docType, (prev) => ({
        ...prev,
        hasError: false,
        errorMessage: ""
      }));

      setGlobalLoading(true);
      setGlobalLoadingText(`Đang upload ${current.file.name}...`);

      const uploaded = await uploadDocument({
        projectId: currentProject.id,
        documentType: docType,
        file: current.file
      });

      setDocumentState(docType, (prev) => ({
        ...prev,
        documentId: uploaded.id,
        uploaded: true
      }));

      addProjectLog(currentProject.id, `Upload thành công: ${current.file.name}`);

      setDocumentState(docType, (prev) => ({
        ...prev,
        extracting: true
      }));
      setGlobalLoadingText(`Đang extract text: ${current.file.name}`);

      const extracted = await extractText(uploaded.id);

      setDocumentState(docType, (prev) => ({
        ...prev,
        extracting: false,
        extracted: true,
        extractedTextPreview: extracted.preview_text || ""
      }));

      addProjectLog(currentProject.id, `Extract text thành công: ${current.file.name}`);

      setDocumentState(docType, (prev) => ({
        ...prev,
        parsing: true
      }));
      setGlobalLoadingText(`Đang parse schema: ${current.file.name}`);

      const parsed = await parseDocument(uploaded.id);

      setDocumentState(docType, (prev) => ({
        ...prev,
        parsing: false,
        parsed: true,
        parsedData: parsed.parsed_data
      }));

      addProjectLog(currentProject.id, `Parse thành công: ${current.file.name}`);

      setDocumentState(docType, (prev) => ({
        ...prev,
        validating: true
      }));
      setGlobalLoadingText(`Đang validate: ${current.file.name}`);

      const validated = await validateDocument(uploaded.id);

      const passed = isValidationPassed(validated.validation_result);

      setDocumentState(docType, (prev) => ({
        ...prev,
        validating: false,
        validated: passed,
        hasError: !passed,
        errorMessage: passed
          ? ""
          : validated.validation_result?.errors?.[0]?.message || "Tài liệu không hợp lệ",
        validationResult: validated.validation_result
      }));

      addProjectLog(
        currentProject.id,
        passed
          ? `Validate thành công: ${current.file.name}`
          : `Validate phát hiện lỗi: ${current.file.name}`
      );
    } catch (error) {
      setDocumentState(docType, (prev) => ({
        ...prev,
        extracting: false,
        parsing: false,
        validating: false,
        hasError: true,
        errorMessage: error.message || "Có lỗi xảy ra"
      }));

      addProjectLog(currentProject.id, `Lỗi xử lý ${current.file.name}: ${error.message}`);
      alert(error.message);
    } finally {
      setGlobalLoading(false);
    }
  };

  const validateWholeProject = async () => {
    if (!currentProject) return;

    try {
      setGlobalLoading(true);
      setGlobalLoadingText("Đang kiểm tra chéo toàn bộ hồ sơ...");

      const result = await validateProject(currentProject.id);
      const validationStatus = result?.validation_result?.validation_status;

      updateCurrentProject((project) => ({
        ...project,
        updatedAt: new Date().toISOString(),
        projectValidationResult: result,
        status:
          validationStatus === "valid"
            ? PROJECT_STATUS.SUCCESS
            : PROJECT_STATUS.DONE
      }));

      addProjectLog(currentProject.id, "Validate toàn project thành công.");

    } catch (error) {
      addProjectLog(currentProject.id, `Validate project thất bại: ${error.message}`);
      alert(error.message);
    } finally {
      setGlobalLoading(false);
    }
  };

  const cancelCurrentProject = () => {
    if (!currentProject) return;

    updateCurrentProject((project) => ({
      ...project,
      updatedAt: new Date().toISOString(),
      status: PROJECT_STATUS.CANCELLED
    }));
    addProjectLog(currentProject.id, "Dự án đã được chuyển sang trạng thái huỷ.");
    setPage("dashboard");
  };

  const goToPreviousStep = () => {
    setSelectedDocumentIndex((prev) => Math.max(0, prev - 1));
  };

  const goToNextStep = () => {
    setSelectedDocumentIndex((prev) =>
      Math.min(maxAccessibleDocumentIndex, prev + 1)
    );
  };

  const progressCount = useMemo(
    () => getProgressCount(currentProject?.documents || {}, DOCUMENT_TYPES),
    [currentProject]
  );

  const progressPercent = useMemo(
    () => getProgressPercent(currentProject?.documents || {}, DOCUMENT_TYPES),
    [currentProject]
  );

  const allValidated = useMemo(
    () => hasAllRequiredDocuments(currentProject?.documents || {}, DOCUMENT_TYPES),
    [currentProject]
  );

  const anyError = useMemo(
    () => hasAnyDocumentError(currentProject?.documents || {}, DOCUMENT_TYPES),
    [currentProject]
  );

  const currentProjectTimeline = useMemo(() => {
    if (!currentProject) return [];

    return [
      ...DOCUMENT_TYPES.map((item, index) => {
        const state = currentProject.documents[item.key];
        const isCurrent = index === activeDocumentIndex;

        let timelineState = "locked";
        if (state.hasError) timelineState = "error";
        else if (state.validated) timelineState = "done";
        else if (isCurrent) timelineState = "current";

        return {
          key: item.key,
          title: item.shortTitle,
          description: item.title,
          state: timelineState
        };
      }),
      {
        key: "FINAL_VALIDATION",
        title: "Mở thầu",
        description: "Kiểm tra và hoàn tất bước mở thầu",
        state: currentProject.projectValidationResult
          ? currentProject.projectValidationResult?.validation_result?.validation_status ===
            "valid"
            ? "done"
            : "error"
          : allValidated && !anyError
            ? "current"
            : "locked"
      }
    ];
  }, [activeDocumentIndex, allValidated, anyError, currentProject]);

  const statusCounts = useMemo(
    () =>
      projects.reduce(
        (acc, project) => {
          const progressCount = getProgressCount(project.documents, DOCUMENT_TYPES);
          const allValidated = hasAllRequiredDocuments(project.documents, DOCUMENT_TYPES);

          acc.total += 1;

          if (project.status === PROJECT_STATUS.CANCELLED) {
            acc.cancelled += 1;
            return acc;
          }

          if (project.projectValidationResult) {
            acc.completed += 1;
            return acc;
          }

          if (allValidated) {
            acc.pendingApproval += 1;
            return acc;
          }

          if (progressCount === 0) {
            acc.created += 1;
            return acc;
          }

          acc.ongoing += 1;
          return acc;
        },
        {
          total: 0,
          created: 0,
          ongoing: 0,
          pendingApproval: 0,
          completed: 0,
          cancelled: 0
        }
      ),
    [projects]
  );

  const decoratedProjects = useMemo(
    () =>
      projects.map((project) => ({
        ...project,
        progressCount: getProgressCount(project.documents, DOCUMENT_TYPES),
        updatedLabel: formatProjectTime(project.updatedAt),
        displayStatus: getProjectDisplayStatus(project)
      })),
    [projects]
  );

  return {
    documentConfigs: DOCUMENT_TYPES,
    page,
    projectForm,
    setProjectForm,
    projects: decoratedProjects,
    currentProjectId,
    currentProject,
    currentProjectLogs: currentProject?.logs || [],
    currentProjectTimeline,
    activeDocumentConfig,
    currentDocumentConfig,
    currentDocumentIndex,
    maxAccessibleDocumentIndex,
    documents: currentProject?.documents || createInitialDocumentState(),
    globalLoading,
    globalLoadingText,
    progressCount,
    progressPercent,
    allValidated,
    anyError,
    projectValidationResult: currentProject?.projectValidationResult || null,
    statusCounts,
    isCreateProjectModalOpen,
    openCreateProjectModal,
    closeCreateProjectModal,
    goToDashboard,
    openProject,
    goToProjectTracking,
    goToPreviousStep,
    goToNextStep,
    createProjectHandler,
    selectFile,
    runDocumentWorkflow,
    validateWholeProject,
    cancelCurrentProject
  };
}
