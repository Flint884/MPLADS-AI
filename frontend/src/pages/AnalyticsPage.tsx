import { useEffect, useState } from 'react';
import { analyticsApi } from '../services/api';
import { StatewisePerformance } from '../types';

export default function AnalyticsPage() {
  const [states, setStates] = useState<StatewisePerformance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStateAnalytics();
  }, []);

  const fetchStateAnalytics = async () => {
    try {
      const res = await analyticsApi.getStateAnalytics();
      setStates(res.data || []);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading analytics...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics & Insights</h1>
        <p className="text-gray-600 mt-1">State-wise and District-wise Performance Metrics</p>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">State</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Projects</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Fund Utilization</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Completion Rate</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Avg Risk Score</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Delayed Projects</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {states.map((state) => (
              <tr key={state.state} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm font-medium text-gray-900">{state.state}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{state.num_projects}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{state.fund_utilization.toFixed(1)}%</td>
                <td className="px-6 py-4 text-sm text-gray-600">{state.completion_rate.toFixed(1)}%</td>
                <td className="px-6 py-4 text-sm text-gray-600">{state.risk_score.toFixed(1)}</td>
                <td className="px-6 py-4 text-sm text-red-600 font-medium">{state.delayed_projects}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
