import axiosClient from "./axiosClient";

export async function uploadDocument({ projectId, documentType, file }) {
  const formData = new FormData();
  formData.append("project_id", projectId);
  formData.append("document_type", documentType);
  formData.append("file", file);

  const response = await axiosClient.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });

  return response.data;
}

export async function extractText(documentId) {
  const response = await axiosClient.post(`/documents/${documentId}/extract-text`);
  return response.data;
}

export async function getDocumentText(documentId) {
  const response = await axiosClient.get(`/documents/${documentId}/text`);
  return response.data;
}

export async function parseDocument(documentId) {
  const response = await axiosClient.post(`/documents/${documentId}/parse`);
  return response.data;
}

export async function validateDocument(documentId) {
  const response = await axiosClient.post(`/documents/${documentId}/validate`);
  return response.data;
}

export async function getParsedDocument(documentId) {
  const response = await axiosClient.get(`/documents/${documentId}/parsed`);
  return response.data;
}

export async function getValidationResult(documentId) {
  const response = await axiosClient.get(
    `/documents/${documentId}/validation-result`
  );
  return response.data;
}