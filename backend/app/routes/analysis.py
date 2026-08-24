"""Analysis and ML execution API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.anomaly_detection import run_anomaly_detection, detect_cost_overrun, detect_low_progress_high_expenditure
from app.ml.duplicate_detection import detect_duplicate_projects
from app.ml.risk_scoring import calculate_all_project_risk_scores

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.post("/run-anomaly-detection")
def run_anomaly_analysis(db: Session = Depends(get_db)):
    """Trigger anomaly detection analysis."""
    try:
        result = run_anomaly_detection(db)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/run-risk-scoring")
def run_risk_scoring(db: Session = Depends(get_db)):
    """Trigger risk score calculation for all projects."""
    try:
        result = calculate_all_project_risk_scores(db)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/detect-duplicates")
def detect_duplicates(db: Session = Depends(get_db)):
    """Trigger duplicate project detection."""
    try:
        result = detect_duplicate_projects(db)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/detect-cost-overruns")
def detect_cost_overruns(db: Session = Depends(get_db)):
    """Detect projects with cost overruns."""
    try:
        overruns = detect_cost_overrun(db)
        return {"status": "success", "cost_overruns": overruns, "count": len(overruns)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/detect-low-progress")
def detect_low_progress(db: Session = Depends(get_db)):
    """Detect projects with high expenditure but low progress."""
    try:
        projects = detect_low_progress_high_expenditure(db)
        return {"status": "success", "projects": projects, "count": len(projects)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/run-full-analysis")
def run_full_analysis(db: Session = Depends(get_db)):
    """Run complete analysis including anomaly detection, risk scoring, and duplicate detection."""
    
    try:
        risk_result = calculate_all_project_risk_scores(db)
        anomaly_result = run_anomaly_detection(db)
        duplicate_result = detect_duplicate_projects(db)
        return {
            "status": "success",
            "message": "Full analysis completed.",
            "risk_scoring": risk_result,
            "anomaly_detection": anomaly_result,
            "duplicate_detection": duplicate_result,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
