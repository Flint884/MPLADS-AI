// Types for MPLADS Sentinel AI application

export interface Project {
  id: number;
  project_id: string;
  project_name: string;
  description?: string;
  state: string;
  district: string;
  constituency?: string;
  category: string;
  implementing_agency?: string;
  mp_name?: string;
  estimated_cost: number;
  sanctioned_amount: number;
  amount_released: number;
  actual_expenditure: number;
  progress_percentage: number;
  sanction_date?: string;
  expected_completion_date?: string;
  completion_date?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Anomaly {
  id: number;
  project_id: number;
  anomaly_type: string;
  anomaly_score: number;
  risk_level: string;
  explanation?: string;
  contributing_factors?: string;
  status: string;
  detected_at: string;
  created_at: string;
}

export interface RiskScore {
  id: number;
  project_id: number;
  overall_score: number;
  risk_category: string;
  cost_overrun_risk: number;
  delay_risk: number;
  unusual_expenditure_risk: number;
  duplicate_work_risk: number;
  payment_pattern_risk: number;
  low_progress_risk: number;
  explanation?: string;
  calculated_at: string;
  created_at: string;
}

export interface DashboardMetrics {
  total_projects: number;
  total_fund_allocated: number;
  total_fund_utilized: number;
  fund_utilization_percentage: number;
  projects_completed: number;
  projects_in_progress: number;
  delayed_projects: number;
  high_risk_projects: number;
  critical_alerts: number;
  potential_duplicate_works: number;
  anomalous_transactions: number;
}

export interface StatewisePerformance {
  state: string;
  num_projects: number;
  fund_utilization: number;
  completion_rate: number;
  risk_score: number;
  delayed_projects: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  state?: string;
  district?: string;
  is_active: boolean;
  created_at: string;
}

export interface Investigation {
  id: number;
  anomaly_id: number;
  assigned_to?: number;
  status: string;
  notes?: string;
  decision?: string;
  created_at: string;
  updated_at: string;
}

export interface DuplicateProject {
  id: number;
  project_id_1: number;
  project_id_2: number;
  similarity_score: number;
  similarity_type: string;
  risk_level: string;
  explanation?: string;
  status: string;
  created_at: string;
}

export type RiskCategory = 'Low' | 'Medium' | 'High' | 'Critical';
export type ProjectStatus = 'Not Started' | 'In Progress' | 'Completed' | 'Delayed';
export type UserRole = 'admin' | 'mp' | 'state_authority' | 'district_authority' | 'auditor';
