import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
  timeout: 30000000,
});

export const runPipeline = (payload) => api.post("/chat", payload);
export const healthCheck = () => api.get("/health");

export const submitHitlDecision = (body) => api.post("/hitl/decision", body);
export const submitBulkHitl = (body) => api.post("/hitl/bulk", body);
export const getHitlQueue = (runId) => api.get(`/hitl/${runId}`);
export const getAuditLog = (runId) => api.get(`/audit/${runId}`);

export default api;