# MPLADS Sentinel AI

**AI-Powered Anomaly, Fraud and Inefficiency Detection System for MPLADS Scheme Implementation**

MPLADS Sentinel AI is a full-stack monitoring platform for analyzing Members of Parliament Local Area Development Scheme (MPLADS) projects. It combines transparent risk scoring, anomaly detection, project analytics, and investigation workflows in one place.

The application includes fictional demonstration data and is intended for evaluation and development use. AI results are decision-support indicators and always require review by authorized officials.

## Features

- **AI Anomaly Detection**: Isolation Forest-based anomaly detection on financial and project data
- **Risk Scoring Engine**: Transparent hybrid rule-based and ML-based risk scoring
- **Duplicate Work Detection**: TF-IDF and cosine similarity-based project comparison
- **Cost Overrun Analysis**: Automatic detection of unusual expenditure patterns
- **Project Delay Monitoring**: Predictive alerts for delayed projects
- **Payment Pattern Analysis**: Detection of suspicious payment transactions
- **Compliance Monitoring**: Automated compliance status tracking
- **Investigation Workflow**: Investigation queue and audit trail
- **Role-Based Dashboards**: Tailored views for different user types
- **Predictive Analytics**: ML-based risk prediction models

## Technology Stack

### Frontend
- React 18+ with TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components
- Recharts for data visualization
- Lucide icons

### Backend
- Python FastAPI
- SQLAlchemy ORM
- SQLite (with PostgreSQL support)

### ML/Analytics
- Scikit-learn (Isolation Forest, TF-IDF, Cosine Similarity)
- Pandas & NumPy
- StandardScaler

## Project Structure

```
project/
├── backend/               # FastAPI backend service
│   ├── app/
│   │   ├── main.py       # FastAPI application entry
│   │   ├── database.py   # Database configuration
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   ├── routes/       # API endpoints
│   │   ├── ml/           # ML models and algorithms
│   │   ├── utils/        # Utility functions
│   │   └── seeds/        # Demo data generation
│   ├── requirements.txt
│   └── .env.example
└── frontend/              # React frontend application
    ├── src/
    │   ├── components/   # Reusable components
    │   ├── pages/        # Page components
    │   ├── services/     # API services
    │   └── types/        # TypeScript types
    └── package.json
```

## Installation & Setup

### Quick Start on Windows

From the project directory, double-click `START_APP.cmd`. The launcher builds the frontend, starts the FastAPI backend, and opens the application at `http://127.0.0.1:8000`.

For a manual setup, use the following steps.

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seeds.demo_data  # Generate demo dataset
python -m uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Generate Demo Data

```bash
cd backend
python -m app.seeds.demo_data
```

### Run Anomaly Detection

```bash
cd backend
python -c "from app.ml.anomaly_detection import run_anomaly_detection; run_anomaly_detection()"
```

## API Endpoints

The backend provides interactive API documentation at `http://localhost:8000/docs`.

### Projects

- `GET /api/projects` - List projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects` - Create a project
- `PUT /api/projects/{id}` - Update a project
- `GET /api/projects/{id}/risk-assessment` - Get a project risk assessment

### Anomalies and Analysis

- `GET /api/anomalies` - List anomaly alerts
- `GET /api/anomalies/{id}` - Get an anomaly alert
- `PUT /api/anomalies/{id}` - Update an anomaly alert
- `POST /api/analysis/run-anomaly-detection` - Run anomaly detection
- `POST /api/analysis/run-risk-scoring` - Calculate risk scores
- `POST /api/analysis/detect-duplicates` - Detect duplicate projects
- `POST /api/analysis/detect-cost-overruns` - Detect cost overruns
- `POST /api/analysis/detect-low-progress` - Detect low-progress projects
- `POST /api/analysis/run-full-analysis` - Run the complete analysis pipeline

### Analytics and Reports

- `GET /api/analytics/dashboard` - National dashboard metrics
- `GET /api/analytics/states` - State-wise analytics
- `GET /api/analytics/districts/{state}` - District analytics
- `GET /api/analytics/fund-utilization-trend` - Fund utilization trend
- `GET /api/analytics/project-status-distribution` - Project status distribution
- `GET /api/analytics/risk-distribution` - Risk distribution
- `GET /api/reports/high-risk-projects` - High-risk projects report
- `GET /api/reports/delayed-projects` - Delayed projects report
- `GET /api/reports/cost-overrun-projects` - Cost overrun report
- `GET /api/reports/compliance-report` - Compliance report
- `GET /api/reports/export-csv` - Export a report as CSV

### Data Management

- `GET /api/data/demo` - Get demo dataset information
- `POST /api/data/generate-demo` - Generate demo data
- `POST /api/data/import-csv` - Import project data from CSV
- `DELETE /api/data/clear-all` - Clear application data
- `GET /api/health` - Check API health

## User Roles

1. **Ministry Administrator** - National-level statistics and insights
2. **Member of Parliament** - View recommended projects
3. **State Nodal Authority** - State-wise monitoring
4. **District Authority** - District project management
5. **Auditor/Monitoring Officer** - Investigation and review

## Demo Data

The application includes a realistic fictional dataset with:
- 150+ sample MPLADS projects
- Multiple states and districts
- Various project categories
- Intentional anomalies for testing
- **All data is completely fictional for demonstration purposes**

## Responsible AI

This system generates AI-powered insights and anomaly scores for **decision support only**. All scores represent:
- Statistical indicators
- Machine learning predictions
- Potential risk factors

**Important**: AI results do not constitute proof of fraud or wrongdoing. All high-risk cases require human review and authorization.

## Development

### Available Scripts

```bash
# Backend
uvicorn app.main:app --reload        # Start dev server
python -m pytest                     # Run tests

# Frontend
npm run dev                          # Start dev server
npm run build                        # Production build
npm run preview                      # Preview production build
```

## Testing

Run the frontend production build to check TypeScript and Vite compilation:

```bash
cd frontend
npm run build
```

Check that the backend is healthy:

```bash
curl http://localhost:8000/api/health
```

The API also provides interactive documentation at `http://localhost:8000/docs`.

## Troubleshooting

### Port 8000 is already in use

Stop the process using port 8000, or start FastAPI on another port:

```bash
cd backend
python -m uvicorn app.main:app --port 8001 --reload
```

### Frontend dependencies are missing

Install them before building or starting the frontend:

```bash
cd frontend
npm install
```

### Database or demo data needs to be reset

Remove the local SQLite database and generate fresh demo data:

```bash
cd backend
Remove-Item mplads.db -ErrorAction SilentlyContinue  # Windows PowerShell
python -m app.seeds.demo_data
```

## Deployment Notes

For local or single-server deployment, build the frontend and run the FastAPI application from the project root. The backend serves the compiled frontend from `frontend/dist` when that directory exists. Before deploying, set production values in `backend/.env`, use a production database such as PostgreSQL when required, and disable API reload mode.

## Repository

Source code and project updates are maintained at:

https://github.com/Flint884/MPLADS-AI

## License

Proprietary - Government of India

## Support

For technical support or queries, contact the development team.

---

**Disclaimer**: This application uses fictional data for demonstration purposes only. Any resemblance to real projects, organizations, or individuals is purely coincidental.
