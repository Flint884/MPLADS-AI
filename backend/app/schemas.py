"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""

    name: str
    email: EmailStr
    role: str
    state: Optional[str] = None
    district: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""

    password: str


class UserResponse(UserBase):
    """User response schema."""

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Project Schemas
class ProjectBase(BaseModel):
    """Base project schema."""

    project_id: str
    project_name: str
    description: Optional[str] = None
    state: str
    district: str
    constituency: Optional[str] = None
    category: str
    implementing_agency: Optional[str] = None
    mp_name: Optional[str] = None
    estimated_cost: float
    sanctioned_amount: float
    amount_released: float
    actual_expenditure: float = 0.0
    progress_percentage: float = 0.0
    sanction_date: Optional[datetime] = None
    expected_completion_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    status: str = "Not Started"


class ProjectCreate(ProjectBase):
    """Project creation schema."""

    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""

    project_name: Optional[str] = None
    actual_expenditure: Optional[float] = None
    progress_percentage: Optional[float] = None
    status: Optional[str] = None
    completion_date: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    """Project response schema."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Payment Schemas
class PaymentBase(BaseModel):
    """Base payment schema."""

    project_id: int
    amount: float
    payment_date: datetime
    payment_reference: Optional[str] = None
    payment_type: Optional[str] = None
    remarks: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Payment creation schema."""

    pass


class PaymentResponse(PaymentBase):
    """Payment response schema."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Anomaly Schemas
class AnomalyBase(BaseModel):
    """Base anomaly schema."""

    project_id: int
    anomaly_type: str
    anomaly_score: float
    risk_level: str
    explanation: Optional[str] = None
    contributing_factors: Optional[str] = None


class AnomalyCreate(AnomalyBase):
    """Anomaly creation schema."""

    pass


class AnomalyUpdate(BaseModel):
    """Anomaly update schema."""

    status: Optional[str] = None


class AnomalyResponse(AnomalyBase):
    """Anomaly response schema."""

    id: int
    status: str
    detected_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Risk Score Schemas
class RiskScoreBase(BaseModel):
    """Base risk score schema."""

    project_id: int
    overall_score: float
    risk_category: str
    cost_overrun_risk: float = 0.0
    delay_risk: float = 0.0
    unusual_expenditure_risk: float = 0.0
    duplicate_work_risk: float = 0.0
    payment_pattern_risk: float = 0.0
    low_progress_risk: float = 0.0
    explanation: Optional[str] = None


class RiskScoreCreate(RiskScoreBase):
    """Risk score creation schema."""

    pass


class RiskScoreResponse(RiskScoreBase):
    """Risk score response schema."""

    id: int
    calculated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# Investigation Schemas
class InvestigationBase(BaseModel):
    """Base investigation schema."""

    anomaly_id: int
    assigned_to: Optional[int] = None
    status: str = "Open"
    notes: Optional[str] = None
    decision: Optional[str] = None


class InvestigationCreate(InvestigationBase):
    """Investigation creation schema."""

    pass


class InvestigationUpdate(BaseModel):
    """Investigation update schema."""

    status: Optional[str] = None
    notes: Optional[str] = None
    decision: Optional[str] = None


class InvestigationResponse(InvestigationBase):
    """Investigation response schema."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Duplicate Project Schemas
class DuplicateProjectBase(BaseModel):
    """Base duplicate project schema."""

    project_id_1: int
    project_id_2: int
    similarity_score: float
    similarity_type: str
    risk_level: str
    explanation: Optional[str] = None


class DuplicateProjectCreate(DuplicateProjectBase):
    """Duplicate project creation schema."""

    pass


class DuplicateProjectResponse(DuplicateProjectBase):
    """Duplicate project response schema."""

    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardMetrics(BaseModel):
    """Dashboard metrics schema."""

    total_projects: int
    total_fund_allocated: float
    total_fund_utilized: float
    fund_utilization_percentage: float
    projects_completed: int
    projects_in_progress: int
    delayed_projects: int
    high_risk_projects: int
    critical_alerts: int
    potential_duplicate_works: int
    anomalous_transactions: int


class StatewisePerformance(BaseModel):
    """State-wise performance schema."""

    state: str
    num_projects: int
    fund_utilization: float
    completion_rate: float
    risk_score: float
    delayed_projects: int


# Analytics Schemas
class AnalyticsData(BaseModel):
    """Analytics data schema."""

    label: str
    value: float
    percentage: Optional[float] = None
