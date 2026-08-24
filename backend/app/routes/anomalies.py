"""Anomalies API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Anomaly, Project
from app.schemas import AnomalyResponse, AnomalyUpdate

router = APIRouter(prefix="/api/anomalies", tags=["anomalies"])


@router.get("")
def list_anomalies(
    db: Session = Depends(get_db),
    skip: int = Query(0),
    limit: int = Query(100),
    project_id: Optional[int] = None,
    anomaly_type: Optional[str] = None,
    risk_level: Optional[str] = None,
    status: Optional[str] = None,
) -> dict:
    """List all detected anomalies with optional filters."""
    query = db.query(Anomaly).join(Project)

    if project_id:
        query = query.filter(Anomaly.project_id == project_id)
    if anomaly_type:
        query = query.filter(Anomaly.anomaly_type == anomaly_type)
    if risk_level:
        query = query.filter(Anomaly.risk_level == risk_level)
    if status:
        query = query.filter(Anomaly.status == status)

    query = query.order_by(Anomaly.detected_at.desc())
    total = query.count()
    anomalies = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "anomalies": [AnomalyResponse.model_validate(a) for a in anomalies],
    }


@router.get("/{anomaly_id}")
def get_anomaly(anomaly_id: int, db: Session = Depends(get_db)) -> dict:
    """Get anomaly details by ID."""
    anomaly = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")

    project = db.query(Project).filter(Project.id == anomaly.project_id).first()

    return {
        "anomaly": AnomalyResponse.model_validate(anomaly),
        "project": {"id": project.id, "name": project.project_name, "state": project.state},
    }


@router.put("/{anomaly_id}")
def update_anomaly(
    anomaly_id: int, anomaly_update: AnomalyUpdate, db: Session = Depends(get_db)
) -> dict:
    """Update anomaly status or add notes."""
    anomaly = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")

    update_data = anomaly_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(anomaly, field, value)

    db.commit()
    db.refresh(anomaly)

    return {"message": "Anomaly updated", "anomaly": AnomalyResponse.model_validate(anomaly)}


@router.get("/project/{project_id}/anomalies")
def get_project_anomalies(project_id: int, db: Session = Depends(get_db)) -> dict:
    """Get all anomalies for a specific project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    anomalies = db.query(Anomaly).filter(Anomaly.project_id == project_id).all()

    return {
        "project_id": project_id,
        "anomaly_count": len(anomalies),
        "anomalies": [AnomalyResponse.model_validate(a) for a in anomalies],
    }
