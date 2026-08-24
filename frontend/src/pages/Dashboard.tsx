import { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, DollarSign, CheckCircle, Zap } from 'lucide-react';
import { analyticsApi, analysisApi, dataApi } from '../services/api';
import { DashboardMetrics } from '../types';

interface DashboardProps {
  userRole?: string;
}

export default function Dashboard(_props: DashboardProps) {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fundTrend, setFundTrend] = useState<any[]>([]);
  const [statusDist, setStatusDist] = useState<any[]>([]);
  const [riskDist, setRiskDist] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Check if demo data exists, if not generate it
      const demoInfo = await dataApi.getDemoInfo();
      if (demoInfo.data.project_count === 0) {
        await dataApi.generateDemo();
      }

      await analysisApi.runFullAnalysis();

      // Fetch dashboard metrics
      const metricsRes = await analyticsApi.getDashboard();
      setMetrics(metricsRes.data);

      // Fetch fund utilization trend
      const fundRes = await analyticsApi.getFundTrend();
      setFundTrend(fundRes.data.trend || []);

      // Fetch status distribution
      const statusRes = await analyticsApi.getStatusDistribution();
      const statusData = statusRes.data.status_distribution || {};
      setStatusDist(
        Object.entries(statusData).map(([key, value]) => ({
          name: key,
          value: value,
        }))
      );

      // Fetch risk distribution
      const riskRes = await analyticsApi.getRiskDistribution();
      const riskData = riskRes.data.risk_distribution || {};
      setRiskDist(
        Object.entries(riskData).map(([key, value]) => ({
          name: key,
          value: value,
        }))
      );

      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-red-800">
        <h3 className="font-semibold mb-2">Error Loading Dashboard</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (!metrics) {
    return <div>No data available</div>;
  }

  const STATUS_COLORS = ['#34d399', '#10b981', '#059669', '#047857'];
  const RISK_COLORS = ['#6ee7b7', '#34d399', '#10b981', '#047857'];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">National Dashboard</h1>
        <p className="text-gray-600 mt-1">MPLADS Scheme Monitoring and Analytics</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Projects"
          value={metrics.total_projects}
          icon={<Zap className="w-6 h-6" />}
          color="bg-black text-emerald-300 border-emerald-900"
        />
        <KPICard
          title="Fund Allocated"
          value={`₹${(metrics.total_fund_allocated / 10000000).toFixed(1)}Cr`}
          icon={<DollarSign className="w-6 h-6" />}
          color="bg-black text-emerald-300 border-emerald-900"
        />
        <KPICard
          title="Fund Utilized"
          value={`${metrics.fund_utilization_percentage.toFixed(1)}%`}
          icon={<CheckCircle className="w-6 h-6" />}
          color="bg-black text-emerald-300 border-emerald-900"
        />
        <KPICard
          title="High Risk Projects"
          value={metrics.high_risk_projects}
          icon={<AlertCircle className="w-6 h-6" />}
          color="bg-black text-emerald-300 border-emerald-900"
        />
      </div>

      {/* Secondary KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPICard
          title="Projects Completed"
          value={metrics.projects_completed}
          subtitle={`of ${metrics.total_projects}`}
          color="bg-black text-emerald-300 border-emerald-900"
        />
        <KPICard
          title="Delayed Projects"
          value={metrics.delayed_projects}
          subtitle="Requires Review"
          color="bg-black text-emerald-300 border-emerald-900"
        />
        <KPICard
          title="Critical Alerts"
          value={metrics.critical_alerts}
          subtitle="Immediate Action"
          color="bg-black text-emerald-300 border-emerald-900"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Project Status Distribution */}
        <div className="bg-black border border-emerald-900 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusDist}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {statusDist.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={STATUS_COLORS[index % STATUS_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="bg-black border border-emerald-900 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Score Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={riskDist}
              margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6">
                {riskDist.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={RISK_COLORS[index % RISK_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Fund Utilization Trend */}
      {fundTrend.length > 0 && (
        <div className="bg-black border border-emerald-900 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Fund Utilization Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              data={fundTrend}
              margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="allocated" stroke="#3b82f6" strokeWidth={2} name="Allocated" />
              <Line type="monotone" dataKey="sanctioned" stroke="#10b981" strokeWidth={2} name="Sanctioned" />
              <Line type="monotone" dataKey="spent" stroke="#f59e0b" strokeWidth={2} name="Spent" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Statistics Summary */}
      <div className="bg-black border border-emerald-900 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Total Fund Utilized</p>
            <p className="text-xl font-bold text-blue-600">₹{(metrics.total_fund_utilized / 10000000).toFixed(1)}Cr</p>
          </div>
          <div>
            <p className="text-gray-600">Potential Duplicates</p>
            <p className="text-xl font-bold text-orange-600">{metrics.potential_duplicate_works}</p>
          </div>
          <div>
            <p className="text-gray-600">Anomalous Transactions</p>
            <p className="text-xl font-bold text-red-600">{metrics.anomalous_transactions}</p>
          </div>
          <div>
            <p className="text-gray-600">In Progress</p>
            <p className="text-xl font-bold text-green-600">{metrics.projects_in_progress}</p>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-emerald-950 border border-emerald-800 rounded-lg p-4 text-sm text-emerald-100">
        <strong>⚠️ Responsible AI Notice:</strong> All AI-generated anomaly scores are decision-support indicators based on available data and statistical models. They do not constitute proof of fraud or wrongdoing. All high-risk cases require review by authorized human officials.
      </div>
    </div>
  );
}

interface KPICardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  subtitle?: string;
  color?: string;
}

function KPICard({ title, value, icon, subtitle, color = 'bg-gray-50 text-gray-600 border-gray-200' }: KPICardProps) {
  return (
    <div className={`border rounded-lg p-6 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium opacity-75">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          {subtitle && <p className="text-xs opacity-60 mt-1">{subtitle}</p>}
        </div>
        {icon && <div className="opacity-20">{icon}</div>}
      </div>
    </div>
  );
}
