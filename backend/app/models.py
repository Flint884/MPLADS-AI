"""SQLAlchemy database models for MPLADS Sentinel AI."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    """User model for authentication and roles."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # admin, mp, state_authority, district_authority, auditor
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Project(Base):
    """Project model for MPLADS projects."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String(50), unique=True, nullable=False, index=True)
    project_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    constituency = Column(String(100), nullable=True)
    category = Column(String(100), nullable=False, index=True)
    implementing_agency = Column(String(255), nullable=True)
    mp_name = Column(String(255), nullable=True)
    
    # Financial information
    estimated_cost = Column(Float, nullable=False)
    sanctioned_amount = Column(Float, nullable=False)
    amount_released = Column(Float, nullable=False)
    actual_expenditure = Column(Float, default=0.0)
    
    # Progress information
    progress_percentage = Column(Float, default=0.0)
    
    # Dates
    sanction_date = Column(DateTime, nullable=True)
    expected_completion_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String(50), default="Not Started")  # Not Started, In Progress, Completed, Delayed
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Payment(Base):
    """Payment model for project payments."""

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_reference = Column(String(100), nullable=True)
    payment_type = Column(String(50), nullable=True)  # Advance, Interim, Final
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Anomaly(Base):
    """Anomaly model for detected anomalies."""

    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    anomaly_type = Column(String(100), nullable=False)  # Cost Overrun, Delay, Low Progress, etc.
    anomaly_score = Column(Float, nullable=False)  # 0-1
    risk_level = Column(String(20), nullable=False)  # Low, Medium, High, Critical
    explanation = Column(Text, nullable=True)
    contributing_factors = Column(Text, nullable=True)  # JSON string
    detected_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="New")  # New, Under Review, Investigation, False Positive, Resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Investigation(Base):
    """Investigation model for anomaly investigations."""

    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    anomaly_id = Column(Integer, ForeignKey("anomalies.id"), nullable=False, index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="Open")  # Open, In Progress, Closed
    notes = Column(Text, nullable=True)
    decision = Column(String(100), nullable=True)  # Confirmed, False Positive, Under Review, Escalated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RiskScore(Base):
    """Risk Score model for project risk assessments."""

    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True, unique=True)
    overall_score = Column(Float, nullable=False)  # 0-100
    risk_category = Column(String(20), nullable=False)  # Low, Medium, High, Critical
    cost_overrun_risk = Column(Float, default=0.0)
    delay_risk = Column(Float, default=0.0)
    unusual_expenditure_risk = Column(Float, default=0.0)
    duplicate_work_risk = Column(Float, default=0.0)
    payment_pattern_risk = Column(Float, default=0.0)
    low_progress_risk = Column(Float, default=0.0)
    explanation = Column(Text, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    """Audit log model for tracking system changes."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    changes = Column(Text, nullable=True)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class DuplicateProject(Base):
    """Duplicate project model for detected similar projects."""

    __tablename__ = "duplicate_projects"

    id = Column(Integer, primary_key=True, index=True)
    project_id_1 = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project_id_2 = Column(Integer, ForeignKey("projects.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)  # 0-1
    similarity_type = Column(String(50), nullable=False)  # Description, Location, Cost, etc.
    risk_level = Column(String(20), nullable=False)  # Low, Medium, High
    explanation = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")  # Pending, Confirmed, Dismissed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemMetric(Base):
    """System metric model for dashboard KPIs."""

    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_date = Column(DateTime, nullable=False)
    category = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
