import { Link, useLocation } from 'react-router-dom';
import {
  BarChart3,
  FileText,
  AlertCircle,
  Settings,
  Menu,
  Home,
  Database,
  Shield,
} from 'lucide-react';
import { useState } from 'react';

interface SidebarProps {
  userRole?: string;
}

export default function Sidebar(_props: SidebarProps) {
  const [isOpen, setIsOpen] = useState(true);
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/projects', label: 'Projects', icon: Database },
    { path: '/anomalies', label: 'Anomaly Alerts', icon: AlertCircle },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/reports', label: 'Reports', icon: FileText },
    { path: '/data-management', label: 'Data Management', icon: Menu },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside
      className={`${
        isOpen ? 'w-64' : 'w-20'
      } bg-black text-white transition-all duration-300 shadow-xl flex flex-col`}
    >
      {/* Logo */}
      <div className="p-5 border-b border-neutral-800">
        <div className="flex items-center gap-3">
          <Shield className="w-8 h-8 text-emerald-400" />
          {isOpen && <span className="font-bold text-lg tracking-tight">MPLADS AI</span>}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive(item.path)
                  ? 'bg-emerald-400 text-black shadow-sm'
                  : 'text-neutral-300 hover:bg-neutral-900'
              }`}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {isOpen && <span className="text-sm font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Toggle */}
      <div className="p-4 border-t border-neutral-800">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-center p-2 rounded-lg hover:bg-neutral-900 transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
      </div>
    </aside>
  );
}
