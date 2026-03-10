import axiosClient from "./axiosClient";

export async function createProject(payload) {
  const response = await axiosClient.post("/projects", payload);
  return response.data;
}

export async function validateProject(projectId) {
  const response = await axiosClient.post(`/projects/${projectId}/validate`);
  return response.data;
}

export async function getProjectValidationResult(projectId) {
  const response = await axiosClient.get(`/projects/${projectId}/validation-result`);
  return response.data;
}