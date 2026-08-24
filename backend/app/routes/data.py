"""Data import and management API routes."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO

from app.database import get_db
from app.models import Project
from app.seeds.demo_data import generate_demo_projects

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/demo")
def get_demo_data_info(db: Session = Depends(get_db)) -> dict:
    """Get information about demo dataset."""
    project_count = db.query(Project).count()
    
    if project_count == 0:
        return {
            "status": "No demo data loaded",
            "project_count": 0,
            "message": "Use POST /api/data/generate-demo to generate demo data",
        }
    
    projects = db.query(Project).all()
    total_fund = sum(p.estimated_cost for p in projects)
    
    return {
        "status": "Demo data loaded",
        "project_count": project_count,
        "total_fund_allocated": total_fund,
        "data_type": "Fictional Demonstration Data",
        "disclaimer": "All data is completely fictional for demonstration purposes",
    }


@router.post("/generate-demo")
def generate_demo_data(db: Session = Depends(get_db)) -> dict:
    """Generate and load fictional demo dataset."""
    # Check if data already exists
    existing_count = db.query(Project).count()
    if existing_count > 0:
        return {
            "status": "Demo data already exists",
            "project_count": existing_count,
            "message": "Delete existing projects first if you want to regenerate",
        }
    
    # Generate demo projects
    demo_projects = generate_demo_projects()
    
    # Insert into database
    for proj_data in demo_projects:
        project = Project(**proj_data)
        db.add(project)
    
    db.commit()
    
    return {
        "status": "Demo data generated successfully",
        "projects_created": len(demo_projects),
        "data_type": "Fictional Demonstration Data",
        "disclaimer": "All data is completely fictional for demonstration purposes",
    }


@router.post("/import-csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    """Import projects from CSV file."""
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
        
        # Validate required columns
        required_columns = [
            "project_id",
            "project_name",
            "state",
            "district",
            "category",
            "estimated_cost",
            "sanctioned_amount",
            "amount_released",
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {
                "status": "error",
                "message": f"Missing required columns: {', '.join(missing_columns)}",
                "required_columns": required_columns,
            }
        
        # Import projects
        imported_count = 0
        skipped_count = 0
        errors = []
        
        for _, row in df.iterrows():
            try:
                # Check if project already exists
                existing = db.query(Project).filter(
                    Project.project_id == row["project_id"]
                ).first()
                if existing:
                    skipped_count += 1
                    continue
                
                project = Project(
                    project_id=row["project_id"],
                    project_name=row["project_name"],
                    description=row.get("description", ""),
                    state=row["state"],
                    district=row["district"],
                    constituency=row.get("constituency", ""),
                    category=row["category"],
                    implementing_agency=row.get("implementing_agency", ""),
                    mp_name=row.get("mp_name", ""),
                    estimated_cost=float(row["estimated_cost"]),
                    sanctioned_amount=float(row["sanctioned_amount"]),
                    amount_released=float(row["amount_released"]),
                    actual_expenditure=float(row.get("actual_expenditure", 0)),
                    progress_percentage=float(row.get("progress_percentage", 0)),
                    status=row.get("status", "Not Started"),
                )
                
                db.add(project)
                imported_count += 1
            except Exception as e:
                skipped_count += 1
                errors.append(f"Row {imported_count + skipped_count}: {str(e)}")
        
        db.commit()
        
        return {
            "status": "import_completed",
            "imported_count": imported_count,
            "skipped_count": skipped_count,
            "errors": errors if errors else None,
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.delete("/clear-all")
def clear_all_data(db: Session = Depends(get_db)) -> dict:
    """Clear all project data from database. Use with caution!"""
    try:
        db.query(Project).delete()
        db.commit()
        return {"status": "success", "message": "All project data cleared"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
