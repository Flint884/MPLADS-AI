"""Projects API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Project, RiskScore
from app.schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.ml.risk_scoring import calculate_project_risk_score

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("")
def list_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0),
    limit: int = Query(100),
    state: Optional[str] = None,
    district: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
) -> dict:
    """List all projects with optional filters."""
    query = db.query(Project)

    if state:
        query = query.filter(Project.state == state)
    if district:
        query = query.filter(Project.district == district)
    if category:
        query = query.filter(Project.category == category)
    if status:
        query = query.filter(Project.status == status)
    if search:
        query = query.filter(
            (Project.project_name.ilike(f"%{search}%"))
            | (Project.description.ilike(f"%{search}%"))
        )

    total = query.count()
    projects = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "projects": [ProjectResponse.model_validate(p) for p in projects],
    }


@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)) -> dict:
    """Get project details by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    risk_score = db.query(RiskScore).filter(RiskScore.project_id == project_id).first()

    return {
        "project": ProjectResponse.model_validate(project),
        "risk_score": risk_score.overall_score if risk_score else None,
        "risk_category": risk_score.risk_category if risk_score else None,
    }


@router.post("")
def create_project(
    project: ProjectCreate, db: Session = Depends(get_db)
) -> dict:
    """Create a new project."""
    existing = db.query(Project).filter(Project.project_id == project.project_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project ID already exists")

    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return {"message": "Project created", "project": ProjectResponse.model_validate(db_project)}


@router.put("/{project_id}")
def update_project(
    project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db)
) -> dict:
    """Update project information."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = project_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(project)

    return {"message": "Project updated", "project": ProjectResponse.model_validate(project)}


@router.get("/{project_id}/risk-assessment")
def get_project_risk_assessment(project_id: int, db: Session = Depends(get_db)) -> dict:
    """Get AI risk assessment for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    risk_score = db.query(RiskScore).filter(RiskScore.project_id == project_id).first()

    if not risk_score:
        return {"error": "Risk assessment not yet calculated"}

    return {
        "project_id": project_id,
        "overall_score": risk_score.overall_score,
        "risk_category": risk_score.risk_category,
        "cost_overrun_risk": risk_score.cost_overrun_risk,
        "delay_risk": risk_score.delay_risk,
        "unusual_expenditure_risk": risk_score.unusual_expenditure_risk,
        "duplicate_work_risk": risk_score.duplicate_work_risk,
        "payment_pattern_risk": risk_score.payment_pattern_risk,
        "low_progress_risk": risk_score.low_progress_risk,
        "explanation": risk_score.explanation,
        "calculated_at": risk_score.calculated_at,
    }
