"""Analytics API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import Project, RiskScore, Anomaly
from app.schemas import DashboardMetrics, StatewisePerformance

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/dashboard")
def get_dashboard_metrics(db: Session = Depends(get_db)) -> DashboardMetrics:
    """Get dashboard KPI metrics."""
    total_projects = db.query(func.count(Project.id)).scalar() or 0
    
    # Financial metrics
    total_fund_allocated = db.query(func.sum(Project.estimated_cost)).scalar() or 0.0
    total_fund_utilized = db.query(func.sum(Project.actual_expenditure)).scalar() or 0.0
    fund_utilization_percentage = (total_fund_utilized / total_fund_allocated * 100) if total_fund_allocated > 0 else 0
    
    # Project status metrics
    projects_completed = db.query(func.count(Project.id)).filter(Project.status == "Completed").scalar() or 0
    projects_in_progress = db.query(func.count(Project.id)).filter(Project.status == "In Progress").scalar() or 0
    delayed_projects = db.query(func.count(Project.id)).filter(Project.status == "Delayed").scalar() or 0
    
    # Risk metrics
    high_risk_projects = db.query(func.count(RiskScore.id)).filter(
        RiskScore.risk_category.in_(["High", "Critical"])
    ).scalar() or 0
    
    critical_alerts = db.query(func.count(Anomaly.id)).filter(
        Anomaly.risk_level == "Critical"
    ).scalar() or 0
    
    # Duplicate and anomaly metrics
    potential_duplicate_works = db.query(func.count(Anomaly.id)).filter(
        Anomaly.anomaly_type == "Duplicate Work"
    ).scalar() or 0
    
    anomalous_transactions = db.query(func.count(Anomaly.id)).filter(
        Anomaly.risk_level.in_(["High", "Critical"])
    ).scalar() or 0

    return DashboardMetrics(
        total_projects=total_projects,
        total_fund_allocated=total_fund_allocated,
        total_fund_utilized=total_fund_utilized,
        fund_utilization_percentage=fund_utilization_percentage,
        projects_completed=projects_completed,
        projects_in_progress=projects_in_progress,
        delayed_projects=delayed_projects,
        high_risk_projects=high_risk_projects,
        critical_alerts=critical_alerts,
        potential_duplicate_works=potential_duplicate_works,
        anomalous_transactions=anomalous_transactions,
    )


@router.get("/states")
def get_statewise_analytics(db: Session = Depends(get_db)) -> List[StatewisePerformance]:
    """Get state-wise performance metrics."""
    states = db.query(Project.state).distinct().all()
    state_list = [s[0] for s in states]
    
    results = []
    for state in state_list:
        state_projects = db.query(Project).filter(Project.state == state).all()
        
        if not state_projects:
            continue
        
        num_projects = len(state_projects)
        fund_allocated = sum(p.estimated_cost for p in state_projects)
        fund_utilized = sum(p.actual_expenditure for p in state_projects)
        completed = sum(1 for p in state_projects if p.status == "Completed")
        completion_rate = (completed / num_projects * 100) if num_projects > 0 else 0
        fund_utilization = (fund_utilized / fund_allocated * 100) if fund_allocated > 0 else 0
        
        # Calculate average risk score
        risk_scores = db.query(RiskScore).filter(
            RiskScore.project_id.in_([p.id for p in state_projects])
        ).all()
        
        avg_risk_score = (
            sum(r.overall_score for r in risk_scores) / len(risk_scores)
            if risk_scores
            else 0
        )
        
        delayed = sum(1 for p in state_projects if p.status == "Delayed")
        
        results.append(
            StatewisePerformance(
                state=state,
                num_projects=num_projects,
                fund_utilization=fund_utilization,
                completion_rate=completion_rate,
                risk_score=avg_risk_score,
                delayed_projects=delayed,
            )
        )
    
    return sorted(results, key=lambda x: x.fund_utilization, reverse=True)


@router.get("/districts/{state}")
def get_districtwise_analytics(state: str, db: Session = Depends(get_db)) -> dict:
    """Get district-wise analytics for a state."""
    districts = db.query(Project.district).filter(Project.state == state).distinct().all()
    district_list = [d[0] for d in districts]
    
    results = []
    for district in district_list:
        district_projects = db.query(Project).filter(
            (Project.state == state) & (Project.district == district)
        ).all()
        
        if not district_projects:
            continue
        
        num_projects = len(district_projects)
        fund_allocated = sum(p.estimated_cost for p in district_projects)
        fund_utilized = sum(p.actual_expenditure for p in district_projects)
        completed = sum(1 for p in district_projects if p.status == "Completed")
        
        results.append({
            "district": district,
            "num_projects": num_projects,
            "fund_allocated": fund_allocated,
            "fund_utilized": fund_utilized,
            "completion_rate": (completed / num_projects * 100) if num_projects > 0 else 0,
            "fund_utilization": (fund_utilized / fund_allocated * 100) if fund_allocated > 0 else 0,
        })
    
    return {"state": state, "districts": results}


@router.get("/fund-utilization-trend")
def get_fund_utilization_trend(db: Session = Depends(get_db)) -> dict:
    """Get fund utilization trend over time."""
    projects = db.query(Project).all()
    
    # Group by month from sanction date
    trend_data = {}
    for project in projects:
        if project.sanction_date:
            month_key = project.sanction_date.strftime("%Y-%m")
            if month_key not in trend_data:
                trend_data[month_key] = {
                    "allocated": 0,
                    "sanctioned": 0,
                    "spent": 0,
                    "count": 0,
                }
            trend_data[month_key]["allocated"] += project.estimated_cost
            trend_data[month_key]["sanctioned"] += project.sanctioned_amount
            trend_data[month_key]["spent"] += project.actual_expenditure
            trend_data[month_key]["count"] += 1
    
    return {
        "trend": [
            {
                "month": month,
                "allocated": data["allocated"],
                "sanctioned": data["sanctioned"],
                "spent": data["spent"],
            }
            for month, data in sorted(trend_data.items())
        ]
    }


@router.get("/project-status-distribution")
def get_project_status_distribution(db: Session = Depends(get_db)) -> dict:
    """Get project status distribution."""
    statuses = ["Not Started", "In Progress", "Completed", "Delayed"]
    distribution = {}
    
    for status in statuses:
        count = db.query(func.count(Project.id)).filter(Project.status == status).scalar() or 0
        distribution[status] = count
    
    return {"status_distribution": distribution}


@router.get("/risk-distribution")
def get_risk_distribution(db: Session = Depends(get_db)) -> dict:
    """Get risk score distribution."""
    risk_categories = ["Low", "Medium", "High", "Critical"]
    distribution = {}
    
    for category in risk_categories:
        count = db.query(func.count(RiskScore.id)).filter(
            RiskScore.risk_category == category
        ).scalar() or 0
        distribution[category] = count
    
    return {"risk_distribution": distribution}
