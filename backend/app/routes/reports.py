"""Reports API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import csv
from io import StringIO

from app.database import get_db
from app.models import Project, RiskScore, Anomaly

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/high-risk-projects")
def get_high_risk_report(db: Session = Depends(get_db)) -> dict:
    """Get high-risk projects report."""
    high_risk_scores = db.query(RiskScore).filter(
        RiskScore.risk_category.in_(["High", "Critical"])
    ).all()
    
    projects_data = []
    for risk_score in high_risk_scores:
        project = db.query(Project).filter(Project.id == risk_score.project_id).first()
        if project:
            projects_data.append({
                "project_id": project.project_id,
                "project_name": project.project_name,
                "state": project.state,
                "district": project.district,
                "category": project.category,
                "risk_score": risk_score.overall_score,
                "risk_category": risk_score.risk_category,
                "estimated_cost": project.estimated_cost,
                "actual_expenditure": project.actual_expenditure,
            })
    
    return {
        "report_type": "High Risk Projects Report",
        "generated_at": datetime.utcnow().isoformat(),
        "total_high_risk": len(projects_data),
        "projects": projects_data,
    }


@router.get("/delayed-projects")
def get_delayed_projects_report(db: Session = Depends(get_db)) -> dict:
    """Get delayed projects report."""
    delayed_projects = db.query(Project).filter(Project.status == "Delayed").all()
    
    projects_data = []
    for project in delayed_projects:
        if project.expected_completion_date:
            delay_days = (datetime.utcnow() - project.expected_completion_date).days
        else:
            delay_days = 0
        
        projects_data.append({
            "project_id": project.project_id,
            "project_name": project.project_name,
            "state": project.state,
            "district": project.district,
            "expected_completion": project.expected_completion_date.isoformat() if project.expected_completion_date else None,
            "delay_days": delay_days,
            "progress": project.progress_percentage,
            "status": project.status,
        })
    
    return {
        "report_type": "Delayed Projects Report",
        "generated_at": datetime.utcnow().isoformat(),
        "total_delayed": len(projects_data),
        "projects": projects_data,
    }


@router.get("/cost-overrun-projects")
def get_cost_overrun_report(db: Session = Depends(get_db)) -> dict:
    """Get cost overrun projects report."""
    projects = db.query(Project).all()
    
    cost_overrun_projects = []
    for project in projects:
        if project.estimated_cost > 0:
            overrun_percentage = (
                (project.actual_expenditure - project.estimated_cost) / project.estimated_cost * 100
            )
            if overrun_percentage > 10:  # Flag if over 10%
                cost_overrun_projects.append({
                    "project_id": project.project_id,
                    "project_name": project.project_name,
                    "state": project.state,
                    "estimated_cost": project.estimated_cost,
                    "actual_expenditure": project.actual_expenditure,
                    "overrun_percentage": overrun_percentage,
                    "overrun_amount": project.actual_expenditure - project.estimated_cost,
                })
    
    return {
        "report_type": "Cost Overrun Report",
        "generated_at": datetime.utcnow().isoformat(),
        "total_cost_overrun": len(cost_overrun_projects),
        "projects": sorted(cost_overrun_projects, key=lambda x: x["overrun_percentage"], reverse=True),
    }


@router.get("/compliance-report")
def get_compliance_report(db: Session = Depends(get_db)) -> dict:
    """Get compliance monitoring report."""
    projects = db.query(Project).all()
    
    compliance_status = {
        "compliant": 0,
        "partially_compliant": 0,
        "non_compliant": 0,
        "requires_review": 0,
    }
    
    details = []
    for project in projects:
        issues = []
        
        if not project.sanction_date:
            issues.append("Missing sanction date")
        if not project.expected_completion_date:
            issues.append("Missing expected completion date")
        if project.estimated_cost <= 0:
            issues.append("Invalid estimated cost")
        if project.progress_percentage < 0 or project.progress_percentage > 100:
            issues.append("Invalid progress percentage")
        
        if len(issues) == 0:
            status = "compliant"
            compliance_status["compliant"] += 1
        elif len(issues) <= 2:
            status = "partially_compliant"
            compliance_status["partially_compliant"] += 1
        elif len(issues) >= 3:
            status = "non_compliant"
            compliance_status["non_compliant"] += 1
        
        details.append({
            "project_id": project.project_id,
            "project_name": project.project_name,
            "status": status,
            "issues": issues,
        })
    
    return {
        "report_type": "Compliance Report",
        "generated_at": datetime.utcnow().isoformat(),
        "summary": compliance_status,
        "projects": details,
    }


@router.get("/export-csv")
def export_projects_csv(report_type: str = "all", db: Session = Depends(get_db)) -> dict:
    """Export projects to CSV format."""
    if report_type == "all":
        projects = db.query(Project).all()
    elif report_type == "high-risk":
        high_risk_ids = db.query(RiskScore).filter(
            RiskScore.risk_category.in_(["High", "Critical"])
        ).with_entities(RiskScore.project_id).all()
        projects = db.query(Project).filter(Project.id.in_([r[0] for r in high_risk_ids])).all()
    elif report_type == "delayed":
        projects = db.query(Project).filter(Project.status == "Delayed").all()
    else:
        return {"status": "error", "message": "Invalid report_type"}
    
    # Create CSV
    output = StringIO()
    fieldnames = [
        "project_id", "project_name", "state", "district", "category",
        "estimated_cost", "sanctioned_amount", "actual_expenditure",
        "progress_percentage", "status", "expected_completion_date"
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for project in projects:
        writer.writerow({
            "project_id": project.project_id,
            "project_name": project.project_name,
            "state": project.state,
            "district": project.district,
            "category": project.category,
            "estimated_cost": project.estimated_cost,
            "sanctioned_amount": project.sanctioned_amount,
            "actual_expenditure": project.actual_expenditure,
            "progress_percentage": project.progress_percentage,
            "status": project.status,
            "expected_completion_date": project.expected_completion_date.isoformat() if project.expected_completion_date else "",
        })
    
    return {
        "status": "success",
        "report_type": report_type,
        "filename": f"mplads_{report_type}_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
        "csv_data": output.getvalue(),
        "row_count": len(projects),
    }
