import { LogOut, User } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface TopNavProps {
  userName?: string;
  onLogout: () => void;
}

export default function TopNav({ userName, onLogout }: TopNavProps) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/');
  };

  return (
    <header className="bg-black shadow-sm border-b border-emerald-900 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-emerald-700">
            MPLADS Sentinel AI
          </h1>
          <p className="text-sm text-emerald-200">
            AI-Powered Anomaly Detection & Monitoring Platform
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="h-8 w-px bg-emerald-200"></div>

          <div className="flex items-center gap-2">
            <User className="w-5 h-5 text-emerald-700" />
            <span className="text-sm font-semibold text-emerald-700">{userName || 'User'}</span>
          </div>

          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-emerald-700 hover:bg-emerald-950 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
