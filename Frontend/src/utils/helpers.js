export function getStatusBadgeType(state) {
  if (state.hasError) return "error";
  if (state.validated) return "success";
  if (state.uploaded) return "processing";
  return "idle";
}

export function isValidationPassed(validationResult) {
  return validationResult?.validation_status === "valid";
}

export function hasAllRequiredDocuments(documents, docTypes) {
  return docTypes.every((item) => documents[item.key]?.validated);
}

export function hasAnyDocumentError(documents, docTypes) {
  return docTypes.some((item) => documents[item.key]?.hasError);
}

export function getProgressCount(documents, docTypes) {
  return docTypes.filter((item) => documents[item.key]?.validated).length;
}

export function getProgressPercent(documents, docTypes) {
  const count = getProgressCount(documents, docTypes);
  return Math.round((count / docTypes.length) * 100);
}