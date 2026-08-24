# MPLADS Sentinel AI - Backend

FastAPI backend for the MPLADS Sentinel AI platform.

## Setup

### Prerequisites
- Python 3.9+
- pip or conda

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Configuration

Edit `.env` file as needed (default values work for local development):

```
DATABASE_URL=sqlite:///./mplads.db
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
ANOMALY_THRESHOLD=0.7
```

## Running the Application

### Start development server

```bash
# Make sure venv is activated
python -m uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### Generate Demo Data

```bash
# Activate venv first
python -m app.seeds.demo_data

# Or use the API endpoint:
# POST http://localhost:8000/api/data/generate-demo
```

### Run ML Analysis

```bash
# Run anomaly detection
python -c "from app.database import SessionLocal; from app.ml.anomaly_detection import run_anomaly_detection; db = SessionLocal(); result = run_anomaly_detection(db); print(result)"

# Or use the API endpoint:
# POST http://localhost:8000/api/analysis/run-anomaly-detection
```

## API Endpoints

### Projects
- `GET /api/projects` - List projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects` - Create project
- `PUT /api/projects/{id}` - Update project
- `GET /api/projects/{id}/risk-assessment` - Get risk assessment

### Anomalies
- `GET /api/anomalies` - List anomalies
- `GET /api/anomalies/{id}` - Get anomaly details
- `PUT /api/anomalies/{id}` - Update anomaly

### Analytics
- `GET /api/analytics/dashboard` - Dashboard metrics
- `GET /api/analytics/states` - State-wise analytics
- `GET /api/analytics/districts/{state}` - District analytics
- `GET /api/analytics/fund-utilization-trend` - Fund trend
- `GET /api/analytics/project-status-distribution` - Status distribution
- `GET /api/analytics/risk-distribution` - Risk distribution

### Data Management
- `GET /api/data/demo` - Demo data info
- `POST /api/data/generate-demo` - Generate demo data
- `POST /api/data/import-csv` - Import CSV data
- `DELETE /api/data/clear-all` - Clear all data

### Reports
- `GET /api/reports/high-risk-projects` - High risk report
- `GET /api/reports/delayed-projects` - Delayed projects report
- `GET /api/reports/cost-overrun-projects` - Cost overrun report
- `GET /api/reports/compliance-report` - Compliance report
- `GET /api/reports/export-csv` - Export as CSV

### Analysis
- `POST /api/analysis/run-anomaly-detection` - Run anomaly detection
- `POST /api/analysis/run-risk-scoring` - Calculate risk scores
- `POST /api/analysis/detect-duplicates` - Detect duplicate projects
- `POST /api/analysis/run-full-analysis` - Run complete analysis

## Database

The application uses SQLite by default (file: `mplads.db`).

To use PostgreSQL, update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/mplads
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routes/              # API endpoints
│   │   ├── projects.py
│   │   ├── anomalies.py
│   │   ├── analytics.py
│   │   ├── data.py
│   │   ├── reports.py
│   │   └── analysis.py
│   ├── ml/                  # ML modules
│   │   ├── anomaly_detection.py
│   │   ├── duplicate_detection.py
│   │   ├── risk_scoring.py
│   │   └── preprocessing.py
│   ├── seeds/               # Database seeding
│   │   └── demo_data.py
│   └── utils/
├── requirements.txt
└── .env.example
```

## ML Algorithms

### Anomaly Detection
- **Algorithm**: Isolation Forest
- **Features**: Project cost, expenditure, progress, delay, payments
- **Output**: Anomaly score (0-1), risk level

### Duplicate Detection
- **Algorithm**: TF-IDF + Cosine Similarity
- **Features**: Project name, description, category, location
- **Output**: Similarity score, risk level

### Risk Scoring
- **Approach**: Hybrid rule-based + ML
- **Components**: Cost overrun, delay, expenditure, duplicate, payment, progress risks
- **Output**: Overall score (0-100), risk category

## Testing

The API includes `/api/health` endpoint for checking status.

```bash
curl http://localhost:8000/api/health
```

## Troubleshooting

### Database locked error
Remove `mplads.db` file and restart:
```bash
rm mplads.db
python -m uvicorn app.main:app --reload
```

### Port already in use
Change API_PORT in `.env` or use:
```bash
python -m uvicorn app.main:app --port 8001 --reload
```

## Notes

- All demo data is completely fictional
- ML models are trained on generated sample data
- Risk scores are for decision support only
- High-risk cases require human review
