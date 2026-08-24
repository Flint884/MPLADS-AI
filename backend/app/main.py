"""FastAPI application entry point."""
from pathlib import Path
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine
from app.models import Base
from app.routes import projects, anomalies, analytics, data, reports, analysis

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    print("Application startup")
    yield
    print("Application shutdown")


# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan,
    description="AI-Powered MPLADS Sentinel Monitoring and Analytics Platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(projects.router)
app.include_router(anomalies.router)
app.include_router(analytics.router)
app.include_router(data.router)
app.include_router(reports.router)
app.include_router(analysis.router)

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if (FRONTEND_DIST / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="frontend-assets")


@app.get("/")
def read_root():
    """API health check and basic information."""
    if (FRONTEND_DIST / "index.html").is_file():
        return FileResponse(FRONTEND_DIST / "index.html")
    return {
        "status": "operational",
        "api_name": settings.api_title,
        "version": settings.api_version,
        "endpoints": {
            "projects": "/api/projects",
            "anomalies": "/api/anomalies",
            "analytics": "/api/analytics",
            "data": "/api/data",
            "reports": "/api/reports",
        }
    }


@app.get("/api/health")
def health_check():
    """API health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": str(__import__("datetime").datetime.utcnow())
    }


@app.get("/{frontend_path:path}", response_model=None)
def serve_frontend(frontend_path: str) -> Union[FileResponse, dict]:
    """Serve the React SPA when the backend is running as the single app."""
    if (FRONTEND_DIST / "index.html").is_file():
        return FileResponse(FRONTEND_DIST / "index.html")
    return {"detail": "Frontend build not found. Run start.ps1 after installing Node.js."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
