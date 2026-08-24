"""Duplicate and similar project detection using TF-IDF and cosine similarity."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session

from app.models import Project, DuplicateProject


def detect_duplicate_projects(db: Session, similarity_threshold: float = 0.75) -> dict:
    """
    Detect potentially duplicate or similar projects using TF-IDF and cosine similarity.
    
    Args:
        db: Database session
        similarity_threshold: Similarity score threshold for flagging (0-1)
    
    Returns:
        Dictionary with duplicate detection results
    """
    projects = db.query(Project).all()
    
    if len(projects) < 2:
        return {"status": "No duplicates found", "duplicate_count": 0}
    
    # Prepare project descriptions
    descriptions = [
        f"{p.project_name} {p.description or ''} {p.category} {p.state} {p.district}"
        for p in projects
    ]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Clear existing duplicate records
    db.query(DuplicateProject).delete()
    db.commit()
    
    # Find and store duplicates
    duplicates_found = 0
    for i in range(len(projects)):
        for j in range(i + 1, len(projects)):
            similarity_score = similarity_matrix[i][j]
            
            if similarity_score >= similarity_threshold:
                # Determine risk level based on similarity and cost proximity
                risk_level = determine_duplicate_risk(
                    projects[i], projects[j], similarity_score
                )
                
                # Determine similarity type
                similarity_type = determine_similarity_type(projects[i], projects[j])
                
                duplicate_record = DuplicateProject(
                    project_id_1=projects[i].id,
                    project_id_2=projects[j].id,
                    similarity_score=float(similarity_score),
                    similarity_type=similarity_type,
                    risk_level=risk_level,
                    explanation=generate_duplicate_explanation(
                        projects[i], projects[j], similarity_score
                    ),
                    status="Pending",
                )
                db.add(duplicate_record)
                duplicates_found += 1
    
    db.commit()
    
    return {
        "status": "success",
        "duplicates_detected": duplicates_found,
        "total_projects": len(projects),
        "similarity_threshold": similarity_threshold,
    }


def determine_duplicate_risk(
    project1: Project, project2: Project, text_similarity: float
) -> str:
    """Determine risk level for potential duplicate projects."""
    # Check cost proximity
    cost_diff_pct = abs(project1.estimated_cost - project2.estimated_cost) / max(
        project1.estimated_cost, project2.estimated_cost
    )
    
    # Check location match
    location_match = project1.state == project2.state and project1.district == project2.district
    
    # Calculate risk
    if text_similarity > 0.85 and location_match and cost_diff_pct < 0.2:
        return "High"
    elif text_similarity > 0.8 and location_match:
        return "High"
    elif text_similarity > 0.75:
        return "Medium"
    else:
        return "Low"


def determine_similarity_type(project1: Project, project2: Project) -> str:
    """Determine type of similarity between projects."""
    factors = []
    
    if project1.category == project2.category:
        factors.append("Category")
    
    if project1.state == project2.state and project1.district == project2.district:
        factors.append("Location")
    
    cost_diff_pct = abs(project1.estimated_cost - project2.estimated_cost) / max(
        project1.estimated_cost, project2.estimated_cost
    )
    if cost_diff_pct < 0.15:
        factors.append("Cost")
    
    if factors:
        return " + ".join(factors)
    else:
        return "Description"


def generate_duplicate_explanation(
    project1: Project, project2: Project, similarity_score: float
) -> str:
    """Generate explanation for duplicate detection."""
    explanation = [
        f"High textual similarity ({similarity_score*100:.1f}%) detected between projects."
    ]
    
    if project1.category == project2.category:
        explanation.append("Both projects are in the same category.")
    
    if project1.state == project2.state and project1.district == project2.district:
        explanation.append("Both projects are in the same state and district.")
    
    cost_diff = abs(project1.estimated_cost - project2.estimated_cost)
    cost_diff_pct = cost_diff / max(project1.estimated_cost, project2.estimated_cost) * 100
    explanation.append(
        f"Estimated costs differ by {cost_diff_pct:.1f}% "
        f"({project1.estimated_cost:.0f} vs {project2.estimated_cost:.0f})."
    )
    
    explanation.append(
        "This may indicate duplicate work or two independent projects with similar scope."
    )
    
    return " ".join(explanation)


def find_similar_projects(db: Session, project_id: int, similarity_threshold: float = 0.70) -> list:
    """Find projects similar to a specific project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return []
    
    all_projects = db.query(Project).all()
    
    # Prepare descriptions
    descriptions = [
        f"{p.project_name} {p.description or ''} {p.category}"
        for p in all_projects
    ]
    
    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3), lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    
    # Calculate similarity
    project_idx = next(i for i, p in enumerate(all_projects) if p.id == project_id)
    similarities = cosine_similarity([tfidf_matrix[project_idx]], tfidf_matrix)[0]
    
    # Get similar projects
    similar = []
    for idx, sim_score in enumerate(similarities):
        if idx != project_idx and sim_score >= similarity_threshold:
            similar.append({
                "project_id": all_projects[idx].id,
                "project_name": all_projects[idx].project_name,
                "similarity_score": float(sim_score),
                "state": all_projects[idx].state,
                "district": all_projects[idx].district,
                "category": all_projects[idx].category,
            })
    
    return sorted(similar, key=lambda x: x["similarity_score"], reverse=True)
