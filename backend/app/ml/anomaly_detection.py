"""Anomaly detection module using Isolation Forest."""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import Project, Anomaly
from app.ml.preprocessing import prepare_project_data, scale_features, handle_missing_values


def run_anomaly_detection(db: Session, contamination: float = 0.1) -> dict:
    """
    Run Isolation Forest anomaly detection on all projects.
    
    Args:
        db: Database session
        contamination: Expected proportion of anomalies (default 0.1)
    
    Returns:
        Dictionary with anomaly detection results
    """
    # Get all projects
    projects = db.query(Project).all()
    
    if len(projects) == 0:
        return {"status": "error", "message": "No projects found"}
    
    # Prepare data
    df = prepare_project_data(projects)
    df = handle_missing_values(df)
    df_scaled, scaler = scale_features(df)
    
    # Select features for anomaly detection
    feature_cols = [
        'estimated_cost',
        'sanctioned_amount',
        'actual_expenditure',
        'amount_released',
        'progress_percentage',
        'fund_utilization',
        'delay_days',
        'num_payments',
    ]
    
    X = df_scaled[feature_cols].values
    
    # Train Isolation Forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    anomaly_labels = iso_forest.fit_predict(X)
    anomaly_scores = -iso_forest.score_samples(X)  # Convert to positive anomaly scores
    
    # Normalize scores to 0-1 range
    anomaly_scores = (anomaly_scores - anomaly_scores.min()) / (anomaly_scores.max() - anomaly_scores.min())
    
    # Clear existing anomalies of type "Statistical Anomaly"
    db.query(Anomaly).filter(Anomaly.anomaly_type == "Statistical Anomaly").delete()
    db.commit()
    
    # Store anomalies in database
    anomalies_created = 0
    for idx, (project_id, score, label) in enumerate(
        zip(df['project_id'], anomaly_scores, anomaly_labels)
    ):
        if label == -1:  # Anomaly detected
            risk_level = categorize_risk_level(score)
            
            anomaly = Anomaly(
                project_id=project_id,
                anomaly_type="Statistical Anomaly",
                anomaly_score=float(score),
                risk_level=risk_level,
                explanation=generate_anomaly_explanation(db, projects[idx], score),
                contributing_factors=get_contributing_factors(df.iloc[idx]),
                status="New",
            )
            db.add(anomaly)
            anomalies_created += 1
    
    db.commit()
    
    return {
        "status": "success",
        "anomalies_detected": anomalies_created,
        "total_projects": len(projects),
        "anomaly_percentage": (anomalies_created / len(projects) * 100) if len(projects) > 0 else 0,
    }


def categorize_risk_level(anomaly_score: float) -> str:
    """Categorize anomaly score to risk level."""
    if anomaly_score < 0.3:
        return "Low"
    elif anomaly_score < 0.6:
        return "Medium"
    elif anomaly_score < 0.8:
        return "High"
    else:
        return "Critical"


def generate_anomaly_explanation(db: Session, project: Project, score: float) -> str:
    """Generate human-readable explanation for anomaly."""
    explanations = []
    
    # Cost analysis
    if project.actual_expenditure > project.estimated_cost * 1.3:
        overrun_pct = ((project.actual_expenditure - project.estimated_cost) / project.estimated_cost) * 100
        explanations.append(
            f"Project expenditure is {overrun_pct:.1f}% higher than estimated cost."
        )
    
    # Progress vs expenditure
    if project.actual_expenditure > project.sanctioned_amount * 0.7 and project.progress_percentage < 0.5:
        explanations.append(
            f"High expenditure ({project.actual_expenditure:.0f}) relative to "
            f"low progress ({project.progress_percentage:.1f}%)."
        )
    
    # Delay analysis
    if project.expected_completion_date:
        from datetime import datetime
        delay_days = (datetime.utcnow() - project.expected_completion_date).days
        if delay_days > 180:
            explanations.append(f"Project is delayed by {delay_days} days.")
    
    # Fund utilization
    utilization = (project.actual_expenditure / project.estimated_cost * 100) if project.estimated_cost > 0 else 0
    if utilization > 90:
        explanations.append(f"High fund utilization rate ({utilization:.1f}%).")
    
    if explanations:
        return " ".join(explanations)
    else:
        return "Statistical anomaly detected based on project financial and progress patterns."


def get_contributing_factors(project_row) -> str:
    """Get contributing factors for anomaly."""
    factors = []
    
    if abs(project_row['estimated_cost']) > 2:  # High scaled value
        factors.append("High Project Cost")
    if abs(project_row['actual_expenditure']) > 2:
        factors.append("High Actual Expenditure")
    if abs(project_row['delay_days']) > 2:
        factors.append("Project Delays")
    if abs(project_row['fund_utilization']) > 2:
        factors.append("Unusual Fund Utilization")
    if abs(project_row['progress_percentage']) < -1:
        factors.append("Low Progress")
    
    return ",".join(factors) if factors else "Multiple Factors"


def detect_cost_overrun(db: Session, threshold_percentage: float = 20.0) -> list:
    """Detect projects with cost overruns."""
    projects = db.query(Project).all()
    cost_overruns = []
    
    for project in projects:
        if project.estimated_cost > 0:
            overrun_pct = (
                (project.actual_expenditure - project.estimated_cost) / project.estimated_cost * 100
            )
            if overrun_pct > threshold_percentage:
                cost_overruns.append({
                    "project_id": project.id,
                    "overrun_percentage": overrun_pct,
                    "overrun_amount": project.actual_expenditure - project.estimated_cost,
                })
    
    return cost_overruns


def detect_low_progress_high_expenditure(db: Session) -> list:
    """Detect projects with high expenditure but low progress."""
    projects = db.query(Project).all()
    flagged_projects = []
    
    for project in projects:
        fund_utilization = (
            (project.actual_expenditure / project.estimated_cost * 100)
            if project.estimated_cost > 0
            else 0
        )
        
        if fund_utilization > 75 and project.progress_percentage < 40:
            flagged_projects.append({
                "project_id": project.id,
                "fund_utilization": fund_utilization,
                "progress": project.progress_percentage,
                "risk_factor": "High Expenditure - Low Progress",
            })
    
    return flagged_projects
