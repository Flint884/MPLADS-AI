import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

// Import pages
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import ProjectsPage from './pages/ProjectsPage';
import ProjectDetailsPage from './pages/ProjectDetailsPage';
import AnomaliesPage from './pages/AnomaliesPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ReportsPage from './pages/ReportsPage';
import DataManagementPage from './pages/DataManagementPage';
import SettingsPage from './pages/SettingsPage';

// Import layout
import Layout from './components/layouts/Layout';

interface AuthState {
  isLoggedIn: boolean;
  userRole?: string;
  userName?: string;
}

function App() {
  const [authState, setAuthState] = useState<AuthState>({
    isLoggedIn: false,
  });

  // Check if user is logged in from localStorage
  useEffect(() => {
    const storedAuth = localStorage.getItem('auth');
    if (storedAuth) {
      setAuthState(JSON.parse(storedAuth));
    }
  }, []);

  const handleLogin = (role: string, name: string) => {
    const auth = { isLoggedIn: true, userRole: role, userName: name };
    setAuthState(auth);
    localStorage.setItem('auth', JSON.stringify(auth));
  };

  const handleLogout = () => {
    setAuthState({ isLoggedIn: false });
    localStorage.removeItem('auth');
  };

  return (
    <Router>
      <Routes>
        {!authState.isLoggedIn ? (
          <>
            <Route path="/" element={<LoginPage onLogin={handleLogin} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </>
        ) : (
          <Route element={<Layout userRole={authState.userRole} userName={authState.userName} onLogout={handleLogout} />}>
            <Route path="/" element={<Dashboard userRole={authState.userRole} />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/projects/:id" element={<ProjectDetailsPage />} />
            <Route path="/anomalies" element={<AnomaliesPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/data-management" element={<DataManagementPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Route>
        )}
      </Routes>
    </Router>
  );
}

export default App;
