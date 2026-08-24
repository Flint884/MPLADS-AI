"""Risk scoring engine for MPLADS projects."""
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Project, RiskScore, Anomaly


def calculate_all_project_risk_scores(db: Session) -> dict:
    """Calculate risk scores for all projects."""
    projects = db.query(Project).all()
    
    if len(projects) == 0:
        return {"status": "No projects", "scores_calculated": 0}
    
    # Clear existing risk scores
    db.query(RiskScore).delete()
    db.commit()
    
    scores_calculated = 0
    for project in projects:
        score = calculate_project_risk_score(db, project)
        scores_calculated += 1
    
    return {
        "status": "success",
        "scores_calculated": scores_calculated,
        "total_projects": len(projects),
    }


def calculate_project_risk_score(db: Session, project: Project) -> RiskScore:
    """
    Calculate comprehensive risk score for a single project.
    
    Risk Score = 0-100
    Risk Categories:
    - 0-24: Low
    - 25-49: Medium
    - 50-74: High
    - 75-100: Critical
    """
    
    # 1. Cost Overrun Risk (25% weight)
    cost_overrun_risk = calculate_cost_overrun_risk(project)
    
    # 2. Project Delay Risk (20% weight)
    delay_risk = calculate_delay_risk(project)
    
    # 3. Unusual Expenditure Risk (20% weight)
    expenditure_risk = calculate_expenditure_risk(project)
    
    # 4. Duplicate Work Risk (15% weight)
    duplicate_risk = calculate_duplicate_risk(db, project)
    
    # 5. Payment Pattern Risk (10% weight)
    payment_risk = calculate_payment_pattern_risk(db, project)
    
    # 6. Low Progress vs High Spending Risk (10% weight)
    progress_risk = calculate_progress_risk(project)
    
    # Calculate weighted overall score
    overall_score = (
        cost_overrun_risk * 0.25
        + delay_risk * 0.20
        + expenditure_risk * 0.20
        + duplicate_risk * 0.15
        + payment_risk * 0.10
        + progress_risk * 0.10
    )
    
    # Determine risk category
    risk_category = categorize_risk_score(overall_score)
    
    # Generate explanation
    explanation = generate_risk_explanation(
        project,
        cost_overrun_risk,
        delay_risk,
        expenditure_risk,
        duplicate_risk,
        payment_risk,
        progress_risk,
    )
    
    # Create and store risk score
    risk_score = RiskScore(
        project_id=project.id,
        overall_score=overall_score,
        risk_category=risk_category,
        cost_overrun_risk=cost_overrun_risk,
        delay_risk=delay_risk,
        unusual_expenditure_risk=expenditure_risk,
        duplicate_work_risk=duplicate_risk,
        payment_pattern_risk=payment_risk,
        low_progress_risk=progress_risk,
        explanation=explanation,
    )
    
    db.add(risk_score)
    db.commit()
    
    return risk_score


def calculate_cost_overrun_risk(project: Project) -> float:
    """
    Calculate cost overrun risk (0-100).
    Compares actual expenditure against estimated cost.
    """
    if project.estimated_cost <= 0:
        return 0
    
    overrun_percentage = (
        (project.actual_expenditure - project.estimated_cost) / project.estimated_cost * 100
    )
    
    if overrun_percentage <= 0:
        return 0
    elif overrun_percentage <= 10:
        return 20
    elif overrun_percentage <= 20:
        return 40
    elif overrun_percentage <= 30:
        return 60
    elif overrun_percentage <= 50:
        return 80
    else:
        return 100


def calculate_delay_risk(project: Project) -> float:
    """
    Calculate project delay risk (0-100).
    Compares expected completion date with current date.
    """
    if not project.expected_completion_date:
        return 0
    
    from datetime import datetime
    delay_days = (datetime.utcnow() - project.expected_completion_date).days
    
    if delay_days <= 0:
        return 0
    elif delay_days <= 30:
        return 20
    elif delay_days <= 90:
        return 40
    elif delay_days <= 180:
        return 60
    elif delay_days <= 365:
        return 80
    else:
        return 100


def calculate_expenditure_risk(project: Project) -> float:
    """
    Calculate unusual expenditure risk (0-100).
    Compares actual expenditure against sanctioned amount relative to project progress.
    """
    if project.estimated_cost <= 0:
        return 0
    
    fund_utilization = (project.actual_expenditure / project.estimated_cost * 100)
    
    # Check if expenditure is unusually high relative to progress
    if project.progress_percentage < 50 and fund_utilization > 75:
        return 85  # High expenditure with low progress
    elif fund_utilization > 100:
        return 70
    elif fund_utilization > 80:
        return 50
    elif fund_utilization > 60:
        return 30
    else:
        return 10


def calculate_duplicate_risk(db: Session, project: Project) -> float:
    """
    Calculate duplicate work risk (0-100).
    Checks for similar projects in the same area with similar costs.
    """
    similar_projects = db.query(Project).filter(
        (Project.state == project.state)
        & (Project.district == project.district)
        & (Project.category == project.category)
        & (Project.id != project.id)
    ).all()
    
    if not similar_projects:
        return 0
    
    # Check for highly similar costs
    high_cost_similarity = 0
    for other_project in similar_projects:
        if other_project.estimated_cost > 0:
            cost_diff_pct = abs(project.estimated_cost - other_project.estimated_cost) / other_project.estimated_cost * 100
            if cost_diff_pct < 15:
                high_cost_similarity += 1
    
    if high_cost_similarity > 0:
        return min(80, 20 * high_cost_similarity)
    
    return 10


def calculate_payment_pattern_risk(db: Session, project: Project) -> float:
    """
    Calculate payment pattern risk (0-100).
    Detects unusual payment transactions or patterns.
    """
    if not hasattr(project, 'payments') or len(project.payments) == 0:
        return 0
    
    payments = project.payments
    
    # Check for unusually frequent payments
    if len(payments) > 50:
        return 70
    elif len(payments) > 20:
        return 40
    
    # Check for duplicate payment amounts
    amounts = [p.amount for p in payments]
    unique_amounts = len(set(amounts))
    duplicate_ratio = 1 - (unique_amounts / len(amounts)) if len(amounts) > 0 else 0
    
    if duplicate_ratio > 0.5:
        return 60
    elif duplicate_ratio > 0.3:
        return 30
    
    return 10


def calculate_progress_risk(project: Project) -> float:
    """
    Calculate low progress vs high spending risk (0-100).
    Flags projects with high fund utilization but low physical progress.
    """
    if project.estimated_cost <= 0:
        return 0
    
    fund_utilization = (project.actual_expenditure / project.estimated_cost * 100)
    
    if fund_utilization > 75 and project.progress_percentage < 40:
        return 90
    elif fund_utilization > 60 and project.progress_percentage < 30:
        return 70
    elif fund_utilization > 50 and project.progress_percentage < 20:
        return 50
    else:
        return 20


def categorize_risk_score(score: float) -> str:
    """Categorize numerical risk score to qualitative risk level."""
    if score < 25:
        return "Low"
    elif score < 50:
        return "Medium"
    elif score < 75:
        return "High"
    else:
        return "Critical"


def generate_risk_explanation(
    project: Project,
    cost_overrun_risk: float,
    delay_risk: float,
    expenditure_risk: float,
    duplicate_risk: float,
    payment_risk: float,
    progress_risk: float,
) -> str:
    """Generate human-readable risk explanation."""
    factors = []
    
    if cost_overrun_risk > 50:
        overrun_pct = ((project.actual_expenditure - project.estimated_cost) / project.estimated_cost * 100)
        factors.append(f"Cost is {overrun_pct:.1f}% higher than estimated.")
    
    if delay_risk > 50 and project.expected_completion_date:
        from datetime import datetime
        delay_days = (datetime.utcnow() - project.expected_completion_date).days
        factors.append(f"Project is delayed by {delay_days} days.")
    
    if expenditure_risk > 60:
        utilization = (project.actual_expenditure / project.estimated_cost * 100) if project.estimated_cost > 0 else 0
        factors.append(f"Unusual expenditure pattern ({utilization:.1f}% fund utilization).")
    
    if progress_risk > 70:
        factors.append(f"Low progress ({project.progress_percentage:.1f}%) despite high spending.")
    
    if duplicate_risk > 40:
        factors.append("Potential similarity with other projects detected.")
    
    if not factors:
        return "Project shows expected patterns with minimal risk indicators."
    
    return " ".join(factors)
