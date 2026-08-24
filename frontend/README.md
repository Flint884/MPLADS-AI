# MPLADS Sentinel AI - Frontend

React + TypeScript frontend for the MPLADS Sentinel AI platform.

## Setup

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment file (if needed)
cp .env.example .env.local
```

## Running the Application

### Development Server

```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview
```

## Configuration

API base URL is configured in `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change this if your backend runs on a different URL.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layouts/
│   │   │   └── Layout.tsx       # Main layout
│   │   └── common/
│   │       ├── Sidebar.tsx      # Navigation sidebar
│   │       └── TopNav.tsx       # Top navigation
│   ├── pages/                   # Page components
│   │   ├── LoginPage.tsx
│   │   ├── Dashboard.tsx
│   │   ├── ProjectsPage.tsx
│   │   ├── ProjectDetailsPage.tsx
│   │   ├── AnomaliesPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   ├── ReportsPage.tsx
│   │   ├── DataManagementPage.tsx
│   │   └── SettingsPage.tsx
│   ├── services/
│   │   └── api.ts               # API client
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── App.tsx                  # Main application
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## Pages

### Login Page
- Demo login with role selection
- 5 user roles: Admin, MP, State Authority, District Authority, Auditor

### Dashboard
- KPI cards with key metrics
- Charts for project status, risk distribution, fund utilization
- Real-time data from API
- Auto-generates demo data if none exists

### Projects
- Project listing with filters
- Search functionality
- Pagination
- Status and progress indicators

### Project Details
- Detailed project information
- Financial data
- Implementation details
- Risk assessment

### Anomalies
- List of detected anomalies
- Filtering by risk level
- Anomaly details and explanations

### Analytics
- State-wise performance metrics
- District-wise analytics
- Comparative analysis

### Reports
- Various downloadable reports
- High-risk projects
- Delayed projects
- Cost overrun analysis
- Compliance status

### Data Management
- Generate demo dataset
- Import CSV data
- Clear data

## Features

### Dashboard Analytics
- Real-time KPI metrics
- Fund utilization trends
- Project status distribution
- Risk score distribution
- State-wise performance

### AI Features
- Anomaly detection results
- Risk scoring with explanations
- Duplicate work detection
- Cost overrun alerts
- Project delay warnings

### User Interface
- Clean government analytics design
- Responsive layout
- Professional color scheme
- Icon-based navigation
- Progress indicators
- Status badges

## API Integration

All API calls go through `src/services/api.ts`. Key methods:

```typescript
// Projects
projectsApi.list(params)
projectsApi.get(id)
projectsApi.create(data)
projectsApi.update(id, data)

// Anomalies
anomaliesApi.list(params)
anomaliesApi.get(id)
anomaliesApi.update(id, data)

// Analytics
analyticsApi.getDashboard()
analyticsApi.getStateAnalytics()
analyticsApi.getFundTrend()

// Data Management
dataApi.generateDemo()
dataApi.importCSV(file)
```

## Authentication

Currently uses localStorage for simple authentication:
```typescript
localStorage.setItem('auth', JSON.stringify({
  isLoggedIn: true,
  userRole: 'admin',
  userName: 'Administrator'
}));
```

For production, implement proper JWT-based authentication.

## Styling

Uses Tailwind CSS with custom components:
- `.kpi-card` - KPI card styling
- `.badge` - Badge styling (Low/Medium/High/Critical)
- `.btn` - Button styling
- `.section-title` - Section heading

## Charts

Uses Recharts for data visualization:
- Line charts for trends
- Bar charts for comparisons
- Pie charts for distributions

## Troubleshooting

### API Connection Error
Ensure backend is running on `http://localhost:8000`

```bash
# Backend should be running on port 8000
cd backend
python -m uvicorn app.main:app --reload
```

### CORS Issues
Backend should allow frontend origin in `app/config.py`:
```python
CORS_ORIGINS=["http://localhost:5173"]
```

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules
npm install
```

## Development Tips

### Adding New Pages
1. Create new file in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation link in `Sidebar.tsx`

### Making API Calls
Use the api service:
```typescript
import { projectsApi } from '../services/api';

const data = await projectsApi.list();
```

### Adding Components
Create reusable components in `src/components/common/`

## Production Deployment

### Build

```bash
npm run build
```

Output will be in `dist/` folder.

### Deploy

- Copy `dist/` folder to web server
- Ensure backend API is accessible
- Update API_BASE_URL if needed
- Configure CORS on backend

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Proprietary - Government of India
