# MPLADS Sentinel AI

**AI-Powered Anomaly, Fraud and Inefficiency Detection System for MPLADS Scheme Implementation**

A comprehensive full-stack application for monitoring and analyzing Members of Parliament Local Area Development Scheme (MPLADS) projects using artificial intelligence, machine learning, and advanced analytics.

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

- `GET /api/dashboard` - National dashboard metrics
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Project details
- `POST /api/projects` - Create project
- `GET /api/anomalies` - List anomalies
- `POST /api/analysis/run` - Run anomaly detection
- `GET /api/duplicate-detection` - Find duplicate projects
- `GET /api/analytics/states` - State-wise analytics
- `GET /api/analytics/districts` - District-wise analytics
- `POST /api/data/import` - Import data from CSV
- `GET /api/data/demo` - Get demo dataset info

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

## License

Proprietary - Government of India

## Support

For technical support or queries, contact the development team.

---

**Disclaimer**: This application uses fictional data for demonstration purposes only. Any resemblance to real projects, organizations, or individuals is purely coincidental.
