import { Outlet } from 'react-router-dom';
import Sidebar from '../common/Sidebar';
import TopNav from '../common/TopNav';

interface LayoutProps {
  userRole?: string;
  userName?: string;
  onLogout: () => void;
}

export default function Layout({ userRole, userName, onLogout }: LayoutProps) {
  return (
    <div className="flex h-screen bg-black">
      <Sidebar userRole={userRole} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopNav userName={userName} onLogout={onLogout} />
        <main className="flex-1 overflow-auto bg-black">
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
