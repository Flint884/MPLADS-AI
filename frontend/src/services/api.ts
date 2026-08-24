import axios from 'axios';

const API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000/api' : '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Projects API
export const projectsApi = {
  list: (params?: any) => api.get('/projects', { params }),
  get: (id: number) => api.get(`/projects/${id}`),
  create: (data: any) => api.post('/projects', data),
  update: (id: number, data: any) => api.put(`/projects/${id}`, data),
  getRiskAssessment: (id: number) => api.get(`/projects/${id}/risk-assessment`),
};

// Anomalies API
export const anomaliesApi = {
  list: (params?: any) => api.get('/anomalies', { params }),
  get: (id: number) => api.get(`/anomalies/${id}`),
  update: (id: number, data: any) => api.put(`/anomalies/${id}`, data),
  getProjectAnomalies: (projectId: number) => api.get(`/anomalies/project/${projectId}/anomalies`),
};

// Analytics API
export const analyticsApi = {
  getDashboard: () => api.get('/analytics/dashboard'),
  getStateAnalytics: () => api.get('/analytics/states'),
  getDistrictAnalytics: (state: string) => api.get(`/analytics/districts/${state}`),
  getFundTrend: () => api.get('/analytics/fund-utilization-trend'),
  getStatusDistribution: () => api.get('/analytics/project-status-distribution'),
  getRiskDistribution: () => api.get('/analytics/risk-distribution'),
};

// Data API
export const dataApi = {
  getDemoInfo: () => api.get('/data/demo'),
  generateDemo: () => api.post('/data/generate-demo'),
  importCSV: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/data/import-csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  clearAll: () => api.delete('/data/clear-all'),
};

export const analysisApi = {
  runFullAnalysis: () => api.post('/analysis/run-full-analysis'),
};

// Reports API
export const reportsApi = {
  getHighRisk: () => api.get('/reports/high-risk-projects'),
  getDelayed: () => api.get('/reports/delayed-projects'),
  getCostOverrun: () => api.get('/reports/cost-overrun-projects'),
  getCompliance: () => api.get('/reports/compliance-report'),
  exportCSV: (reportType: string) => api.get('/reports/export-csv', { params: { report_type: reportType } }),
};

export default api;
