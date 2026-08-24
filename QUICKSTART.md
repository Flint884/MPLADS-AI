# 🚀 MPLADS Sentinel AI - Quick Start

> AI-Powered Anomaly, Fraud and Inefficiency Detection System for MPLADS Scheme Implementation

## ⚡ 5-Minute Setup

### Prerequisites
- Python 3.9+
- Node.js 16+

### Backend (Terminal 1)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Backend runs on:** `http://localhost:8000`

### Frontend (Terminal 2)

```powershell
cd frontend
npm install
npm run dev
```

**Frontend runs on:** `http://localhost:5173`

## 🌐 Access Application

1. Open `http://localhost:5173`
2. Select your role (Admin, MP, State Authority, District Authority, Auditor)
3. Click "Enter Dashboard"
4. **Demo data auto-generates on first load** ✨

## 📊 What You'll See

### Dashboard
- 11 Key Performance Indicators
- Fund utilization trends
- Project status distribution
- Risk score breakdown
- State-wise performance rankings

### Features
- **Projects** - Browse 150+ demo projects
- **Anomalies** - View AI-detected anomalies
- **Analytics** - State and district analysis
- **Reports** - Download various reports
- **Data** - Generate and manage datasets

## 🤖 ML Features

### Automatic Analysis
- **Anomaly Detection** - Identifies unusual patterns (Isolation Forest)
- **Risk Scoring** - Rates project risk 0-100
- **Duplicate Detection** - Finds similar projects (TF-IDF)
- **Cost Overrun Alerts** - Flags high expenditure
- **Delay Warnings** - Identifies project delays

### API Endpoints
```
GET  /api/dashboard          - Dashboard metrics
POST /api/analysis/run-*     - Trigger ML analysis
GET  /api/projects           - List projects
GET  /api/anomalies          - List anomalies
GET  /api/reports/*          - Generate reports
```

## 📁 Project Structure

```
Project/
├── backend/          # FastAPI server (Python)
│   └── app/
│       ├── routes/   # 40+ API endpoints
│       ├── ml/       # ML algorithms
│       └── models.py # 8 database models
├── frontend/         # React app (TypeScript)
│   └── src/
│       ├── pages/    # 9 pages
│       ├── services/ # API client
│       └── types/    # TypeScript types
└── docs/            # Documentation
```

## 📚 Documentation

- **[README.md](README.md)** - Main project overview
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup (detailed)
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Features & architecture
- **[FILE_INDEX.md](FILE_INDEX.md)** - Complete file listing
- **[backend/README.md](backend/README.md)** - Backend API docs
- **[frontend/README.md](frontend/README.md)** - Frontend setup

## 🎯 Key Features

✅ **Dashboard Analytics**
- Real-time KPI metrics
- Interactive charts (Recharts)
- State-wise comparisons

✅ **Project Management**
- List 150+ demo projects
- Filter by state, category, status
- Search functionality
- Progress tracking

✅ **AI Anomaly Detection**
- Isolation Forest algorithm
- Analyzes 8 financial features
- Generates risk scores & explanations

✅ **Duplicate Detection**
- TF-IDF text similarity
- Location & cost comparison
- Risk assessment

✅ **Risk Scoring**
- 6 weighted components
- Scores 0-100
- 4 risk categories (Low/Medium/High/Critical)

✅ **Report Generation**
- High-risk projects
- Delayed projects
- Cost overruns
- Compliance status
- CSV export

## 🔧 Common Commands

```powershell
# Backend: Generate demo data
curl -X POST http://localhost:8000/api/data/generate-demo

# Backend: Run anomaly detection
curl -X POST http://localhost:8000/api/analysis/run-anomaly-detection

# Backend: Get dashboard metrics
curl http://localhost:8000/api/analytics/dashboard

# Frontend: Build for production
npm run build

# Frontend: Preview production build
npm run preview
```

## 🎨 User Roles

| Role | Access |
|------|--------|
| **Ministry Admin** | National overview, state rankings, trends |
| **MP** | Recommended projects, fund tracking |
| **State Authority** | State-wise projects, district performance |
| **District Authority** | District projects, progress updates |
| **Auditor** | Investigation queue, risk review |

## ⚠️ Important Notes

- **Fictional Data:** All demo data is completely fictional
- **AI Decision Support:** Scores indicate risk, not proof of fraud
- **Human Authority:** High-risk cases require human review
- **No Real Data:** No real projects or financial information used

## 🚀 Deployment

### Production Setup
1. Use PostgreSQL instead of SQLite
2. Implement JWT authentication
3. Set environment variables
4. Build frontend: `npm run build`
5. Deploy to cloud (AWS, GCP, Azure)

See [SETUP_GUIDE.md](SETUP_GUIDE.md#production-deployment) for details.

## 📞 Troubleshooting

### Port Already in Use
```powershell
# Use different port
python -m uvicorn app.main:app --port 8001
```

### Dependencies Missing
```powershell
# Backend
pip install -r requirements.txt --upgrade

# Frontend  
npm install
```

### Database Issues
```powershell
# Remove SQLite database and restart
rm mplads.db
```

## 🔗 Useful Links

- **Swagger API Docs:** `http://localhost:8000/docs`
- **ReDoc API Docs:** `http://localhost:8000/redoc`
- **Frontend:** `http://localhost:5173`
- **Backend:** `http://localhost:8000`

## 📊 Demo Dataset

- **150+ Projects** across multiple states
- **8 Categories** (Roads, Education, Healthcare, etc.)
- **₹15+ Crore** total demo portfolio
- **Intentional Anomalies** for testing
- **Realistic Patterns** for ML training

## ✅ Next Steps

1. ✅ Run backend and frontend
2. ✅ Login and select role
3. ✅ Explore dashboard
4. ✅ Browse projects
5. ✅ Run anomaly detection
6. ✅ Review risk scores
7. ✅ Generate reports
8. ✅ Test data import

## 🎓 Learning Path

1. Start with **Dashboard** - understand the data
2. Browse **Projects** - see individual items
3. Check **Anomalies** - view ML results
4. Explore **Analytics** - understand patterns
5. Generate **Reports** - create insights
6. Review **Data Management** - import/export

## 💡 Pro Tips

- Dashboard auto-refreshes after data import
- Use search on Projects page for quick lookup
- Anomalies show which projects need attention
- Reports can be exported as CSV
- Settings page explains AI methodology

## 📖 Full Documentation

For complete documentation including:
- Detailed API endpoints
- Database schema
- ML algorithms explained
- Development guidelines
- Deployment instructions

→ See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🎉 You're Ready!

The complete MPLADS Sentinel AI application is ready to use. 

**Start the backend and frontend, then login to explore!**

Questions? Check the documentation files or review the code comments.

**Status: ✅ Complete & Functional**
