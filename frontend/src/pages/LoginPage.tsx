import { useState } from 'react';
import { Shield, LogIn } from 'lucide-react';

interface LoginPageProps {
  onLogin: (role: string, name: string) => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [selectedRole, setSelectedRole] = useState<string>('admin');

  const roles = [
    {
      id: 'admin',
      label: 'Ministry Administrator',
      description: 'National-level statistics and insights',
      color: 'from-emerald-600 to-emerald-800',
    },
    {
      id: 'mp',
      label: 'Member of Parliament',
      description: 'View recommended projects and progress',
      color: 'from-emerald-600 to-emerald-800',
    },
    {
      id: 'state_authority',
      label: 'State Nodal Authority',
      description: 'State-wise monitoring and analytics',
      color: 'from-emerald-600 to-emerald-800',
    },
    {
      id: 'district_authority',
      label: 'District Authority',
      description: 'District project management',
      color: 'from-emerald-600 to-emerald-800',
    },
    {
      id: 'auditor',
      label: 'Auditor/Monitoring Officer',
      description: 'Investigation and review',
      color: 'from-emerald-600 to-emerald-800',
    },
  ];

  const handleLogin = () => {
    const roleNames: { [key: string]: string } = {
      admin: 'Ministry Administrator',
      mp: 'Member of Parliament',
      state_authority: 'State Authority',
      district_authority: 'District Authority',
      auditor: 'Auditor',
    };
    onLogin(selectedRole, roleNames[selectedRole] || selectedRole);
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="w-full max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Shield className="w-12 h-12 text-emerald-400" />
            <h1 className="text-4xl font-bold text-white">MPLADS Sentinel AI</h1>
          </div>
          <p className="text-lg text-emerald-100">
            AI-Powered Anomaly, Fraud and Inefficiency Detection System for MPLADS Scheme Implementation
          </p>
          <p className="text-sm text-emerald-300 mt-2">
            Select your role to access the monitoring dashboard
          </p>
        </div>

        {/* Role Selection */}
        <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
          {roles.map((role) => (
            <button
              key={role.id}
              onClick={() => setSelectedRole(role.id)}
              className={`p-4 rounded-lg transition-all ${
                selectedRole === role.id
                  ? `bg-gradient-to-br ${role.color} text-white shadow-2xl scale-105`
                  : 'bg-neutral-950 text-emerald-200 hover:bg-emerald-950'
              }`}
            >
              <div className="font-semibold text-sm mb-2">{role.label}</div>
              <div className="text-xs opacity-75">{role.description}</div>
            </button>
          ))}
        </div>

        {/* Login Button */}
        <div className="text-center">
          <button
            onClick={handleLogin}
            className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-600 text-black font-bold rounded-lg hover:bg-emerald-500 hover:shadow-xl hover:scale-105 transition-all"
          >
            <LogIn className="w-5 h-5" />
            Enter Dashboard as {roles.find((r) => r.id === selectedRole)?.label}
          </button>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-emerald-100 text-sm">
          <p className="mb-2">
            <strong>Disclaimer:</strong> This application uses fictional demonstration data.
          </p>
          <p>
            AI-generated anomaly scores are decision-support indicators based on available data and statistical or machine learning models.
          </p>
          <p className="mt-2 text-xs">
            They do not constitute proof of fraud or wrongdoing. All high-risk cases require review by authorized human officials.
          </p>
        </div>
      </div>
    </div>
  );
}
