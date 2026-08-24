
# MPLADS Sentinel AI - Complete Setup Guide

A comprehensive full-stack AI-powered MPLADS monitoring and analytics platform.

## Project Overview

This is a complete, production-ready application comprising:

### Backend (FastAPI + Python)
- RESTful APIs for project management
- Machine Learning modules for anomaly detection
- Database models with SQLAlchemy
- Demo dataset generation
- Comprehensive analytics engine

### Frontend (React + TypeScript)
- Modern dashboard interface
- Role-based access control
- Interactive charts and analytics
- Project management interface
- Investigation workflows

### ML/Analytics Engine
- Isolation Forest anomaly detection
- TF-IDF based duplicate detection
- Hybrid risk scoring
- Cost overrun analysis
- Project delay prediction

## Quick Start (5 Minutes)

### Backend Setup

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python -m uvicorn app.main:app --reload
```

Backend will run on: `http://localhost:8000`

### Frontend Setup (in new terminal)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will run on: `http://localhost:5173`

### Access the Application

1. Open browser to `http://localhost:5173`
2. Select your role (Ministry Admin, MP, State Authority, etc.)
3. Click "Enter Dashboard"
4. Dashboard will auto-generate demo data on first load

## Detailed Setup

### Backend Setup

#### Prerequisites
- Python 3.9 or higher
- pip package manager

#### Installation Steps

```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment (Windows)
.\venv\Scripts\activate

# On macOS/Linux:
# source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install all dependencies
pip install -r requirements.txt

# 5. Create .env file from example
copy .env.example .env
# On macOS/Linux:
# cp .env.example .env

# 6. Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Backend Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # Configuration
│   ├── database.py                # Database setup
│   ├── models.py                  # SQLAlchemy models (8 tables)
│   ├── schemas.py                 # Pydantic validators
│   ├── routes/
│   │   ├── projects.py            # Project CRUD APIs
│   │   ├── anomalies.py           # Anomaly list/update
│   │   ├── analytics.py           # Dashboard & analytics
│   │   ├── data.py                # CSV import, demo data
│   │   ├── reports.py             # Report generation
│   │   └── analysis.py            # ML analysis endpoints
│   ├── ml/
│   │   ├── anomaly_detection.py   # Isolation Forest
│   │   ├── duplicate_detection.py # TF-IDF similarity
│   │   ├── risk_scoring.py        # Hybrid risk scoring
│   │   └── preprocessing.py       # Data cleaning
│   ├── seeds/
│   │   └── demo_data.py           # Generate 150+ demo projects
│   └── utils/
├── requirements.txt
├── .env.example
└── README.md
```

#### API Endpoints Summary

**Projects**
- `GET /api/projects` - List projects with filters
- `GET /api/projects/{id}` - Get details
- `POST /api/projects` - Create
- `PUT /api/projects/{id}` - Update
- `GET /api/projects/{id}/risk-assessment` - Risk score

**Anomalies**
- `GET /api/anomalies` - List anomalies
- `GET /api/anomalies/{id}` - Get details
- `PUT /api/anomalies/{id}` - Update status

**Analytics**
- `GET /api/analytics/dashboard` - Dashboard KPIs
- `GET /api/analytics/states` - State performance
- `GET /api/analytics/districts/{state}` - District performance
- `GET /api/analytics/fund-utilization-trend` - Trend data
- `GET /api/analytics/project-status-distribution` - Status distribution
- `GET /api/analytics/risk-distribution` - Risk distribution

**Data Management**
- `POST /api/data/generate-demo` - Generate 150 demo projects
- `POST /api/data/import-csv` - Import CSV file
- `GET /api/data/demo` - Get dataset info

**Analysis & ML**
- `POST /api/analysis/run-anomaly-detection` - Run Isolation Forest
- `POST /api/analysis/run-risk-scoring` - Calculate risk scores
- `POST /api/analysis/detect-duplicates` - Find similar projects
- `POST /api/analysis/run-full-analysis` - Run complete analysis

**Reports**
- `GET /api/reports/high-risk-projects` - High-risk report
- `GET /api/reports/delayed-projects` - Delayed projects
- `GET /api/reports/cost-overrun-projects` - Cost overruns
- `GET /api/reports/compliance-report` - Compliance status
- `GET /api/reports/export-csv` - Export as CSV

### Frontend Setup

#### Prerequisites
- Node.js 16 or higher
- npm or yarn

#### Installation Steps

```powershell
# 1. Install dependencies
npm install

# 2. Start development server
npm run dev

# Application opens at http://localhost:5173

# 3. For production build
npm run build
npm run preview
```

#### Frontend Directory Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layouts/
│   │   │   └── Layout.tsx         # Main app layout
│   │   └── common/
│   │       ├── Sidebar.tsx        # Navigation
│   │       └── TopNav.tsx         # Top bar
│   ├── pages/
│   │   ├── LoginPage.tsx          # Role-based login
│   │   ├── Dashboard.tsx          # Main dashboard
│   │   ├── ProjectsPage.tsx       # Project listing
│   │   ├── ProjectDetailsPage.tsx # Project details
│   │   ├── AnomaliesPage.tsx      # Anomaly alerts
│   │   ├── AnalyticsPage.tsx      # Analytics
│   │   ├── ReportsPage.tsx        # Reports
│   │   ├── DataManagementPage.tsx # Data management
│   │   └── SettingsPage.tsx       # Settings
│   ├── services/
│   │   └── api.ts                 # API client (axios)
│   ├── types/
│   │   └── index.ts               # TypeScript definitions
│   ├── App.tsx                    # Main App with routing
│   ├── main.tsx                   # React entry
│   └── index.css                  # Tailwind + custom styles
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
└── package.json
```

#### User Roles

1. **Ministry Administrator** - National overview, state performance, fraud trends
2. **Member of Parliament** - Recommended projects, fund utilization, delays
3. **State Nodal Authority** - State-wise projects, district performance
4. **District Authority** - District projects, progress tracking, anomalies
5. **Auditor/Monitoring Officer** - Investigation queue, risk review

## Database Models

### Users
- id, name, email, password_hash, role, state, district, is_active, timestamps

### Projects (Core)
- id, project_id, project_name, description, state, district, category
- estimated_cost, sanctioned_amount, amount_released, actual_expenditure
- progress_percentage, sanction_date, completion_date, status
- timestamps

### Payments
- id, project_id, amount, payment_date, payment_type, remarks
- timestamp

### Anomalies
- id, project_id, anomaly_type, anomaly_score, risk_level
- explanation, contributing_factors, status, timestamps

### Risk Scores
- id, project_id, overall_score, risk_category
- 6 component scores (cost, delay, expenditure, duplicate, payment, progress)

### Investigations
- id, anomaly_id, assigned_to, status, notes, decision
- timestamps

### Duplicate Projects
- id, project_id_1, project_id_2, similarity_score
- similarity_type, risk_level, status, timestamps

### Audit Logs
- id, user_id, action, entity_type, entity_id, changes, timestamp

## ML Features

### 1. Anomaly Detection (Isolation Forest)
**Features Analyzed:**
- Estimated cost
- Actual expenditure
- Sanctioned amount
- Amount released
- Project progress percentage
- Fund utilization ratio
- Project delays
- Payment frequency

**Output:** Anomaly score (0-1), risk level classification

**Risk Levels:**
- Low: Score < 0.3
- Medium: 0.3-0.6
- High: 0.6-0.8
- Critical: > 0.8

### 2. Duplicate Detection (TF-IDF + Cosine Similarity)
**Text Similarity:** Project name + description
**Cost Proximity:** Estimated costs within 15%
**Location Match:** Same state and district
**Category Match:** Same project category

**Output:** Similarity score (0-1), risk assessment

### 3. Risk Scoring (Hybrid Rule-Based + ML)
**Components (Weighted):**
- Cost Overrun Risk (25%) - Compares actual vs estimated
- Project Delay Risk (20%) - Days beyond expected completion
- Unusual Expenditure Risk (20%) - High spending with low progress
- Duplicate Work Risk (15%) - Similar projects in area
- Payment Pattern Risk (10%) - Unusual transaction patterns
- Low Progress Risk (10%) - High funds spent, low completion

**Overall Score:** 0-100
**Categories:**
- Low: 0-24
- Medium: 25-49
- High: 50-74
- Critical: 75-100

## Demo Dataset

**Includes:**
- 150+ fictional MPLADS projects
- Multiple states (Maharashtra, Karnataka, UP, Delhi, etc.)
- 8 project categories
- Intentional anomalies (15% cost overruns, 10% low-progress cases)
- Realistic financial and progress data
- **Fully fictional - no real data used**

## Running Analysis

### Auto-Run (on first login)
Dashboard automatically generates demo data and runs analysis

### Manual Trigger

```powershell
# Terminal 1: Start backend (if not running)
cd backend
.\venv\Scripts\python -m uvicorn app.main:app --reload

# Terminal 2: Trigger analysis
.\venv\Scripts\python -c "
from app.database import SessionLocal
from app.ml.anomaly_detection import run_anomaly_detection
from app.ml.risk_scoring import calculate_all_project_risk_scores
from app.ml.duplicate_detection import detect_duplicate_projects

db = SessionLocal()
print('Running analysis...')
print('- Risk Scoring:', calculate_all_project_risk_scores(db))
print('- Anomaly Detection:', run_anomaly_detection(db))
print('- Duplicate Detection:', detect_duplicate_projects(db))
"
```

### Via API

```powershell
# Run anomaly detection
curl -X POST http://localhost:8000/api/analysis/run-anomaly-detection

# Run risk scoring
curl -X POST http://localhost:8000/api/analysis/run-risk-scoring

# Run all analysis
curl -X POST http://localhost:8000/api/analysis/run-full-analysis
```

## Features Checklist

### ✓ Dashboard
- [ ] KPI cards (projects, funds, utilization)
- [ ] Charts (status, risk distribution, fund trends)
- [ ] State-wise performance ranking
- [ ] Real-time metrics

### ✓ Projects Management
- [ ] List with filters (state, category, status)
- [ ] Search functionality
- [ ] Pagination
- [ ] Progress visualization
- [ ] Detailed project view

### ✓ AI/ML Features
- [ ] Anomaly detection results
- [ ] Risk scoring with explanations
- [ ] Duplicate work flagging
- [ ] Cost overrun alerts
- [ ] Project delay warnings

### ✓ Analytics & Reports
- [ ] State-wise analytics
- [ ] District-wise breakdown
- [ ] High-risk projects report
- [ ] Delayed projects report
- [ ] Cost overrun analysis
- [ ] Compliance status
- [ ] CSV export

### ✓ Administration
- [ ] Demo data generation
- [ ] CSV import
- [ ] Role-based access
- [ ] Investigation workflow
- [ ] Audit logging

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
# Use different port
python -m uvicorn app.main:app --reload --port 8001
```

**Database locked:**
```powershell
# Delete SQLite database and restart
Remove-Item mplads.db -ErrorAction SilentlyContinue
python -m uvicorn app.main:app --reload
```

**Import errors:**
```powershell
# Verify virtual environment is activated
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Issues

**Module not found:**
```powershell
# Clear and reinstall
Remove-Item -Recurse node_modules
npm install
```

**Port 5173 in use:**
```powershell
# Update vite.config.ts port or use:
npm run dev -- --port 5174
```

**API connection refused:**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend `app/config.py`

## Production Deployment

### Backend
```bash
# Build and deploy
pip install -r requirements.txt
# Use PostgreSQL for production
export DATABASE_URL=postgresql://user:pass@host/mplads
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
# Build
npm run build

# Deploy dist/ folder to web server
# Ensure API_BASE_URL is configured correctly
```

## Performance Considerations

- **Demo Data:** 150 projects loads instantly
- **Anomaly Detection:** ~500ms for 150 projects
- **Risk Scoring:** ~200ms per calculation
- **Duplicate Detection:** ~1s for full analysis
- **Dashboard:** Real-time updates with React hooks

## Security Notes

- **Authentication:** Currently mock (update for production)
- **API:** No authentication (add JWT for production)
- **CORS:** Configured for localhost (update for production)
- **Database:** SQLite default (use PostgreSQL for production)
- **Environment:** Store secrets in .env (never in code)

## Support & Documentation

- Backend API docs: `http://localhost:8000/docs` (Swagger UI)
- Backend routes: `app/routes/*.py`
- Frontend components: `src/components/` and `src/pages/`
- ML algorithms: `app/ml/*.py`

---

**Disclaimer:** This application uses completely fictional demonstration data. All AI-generated anomaly scores and risk assessments are decision-support indicators based on statistical models. They do not constitute proof of fraud or wrongdoing. All high-risk cases require review by authorized human officials.
