import { useEffect, useState } from 'react';
import { anomaliesApi } from '../services/api';
import { Anomaly } from '../types';

export default function AnomaliesPage() {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterRiskLevel, setFilterRiskLevel] = useState('');

  useEffect(() => {
    fetchAnomalies();
  }, [filterRiskLevel]);

  const fetchAnomalies = async () => {
    try {
      const res = await anomaliesApi.list({
        risk_level: filterRiskLevel || undefined,
      });
      setAnomalies(res.data.anomalies || []);
    } catch (err) {
      console.error('Error fetching anomalies:', err);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'Low':
        return 'bg-green-100 text-green-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'High':
        return 'bg-orange-100 text-orange-800';
      case 'Critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) return <div>Loading anomalies...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Anomaly Alerts</h1>
        <p className="text-gray-600 mt-1">AI-Detected Anomalies and Risk Indicators</p>
      </div>

      <div className="bg-white rounded-lg shadow p-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">Filter by Risk Level</label>
        <select
          value={filterRiskLevel}
          onChange={(e) => setFilterRiskLevel(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg"
        >
          <option value="">All</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Critical">Critical</option>
        </select>
      </div>

      <div className="space-y-4">
        {anomalies.length === 0 ? (
          <div className="bg-gray-50 rounded-lg p-8 text-center text-gray-600">
            No anomalies detected
          </div>
        ) : (
          anomalies.map((anomaly) => (
            <div key={anomaly.id} className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{anomaly.anomaly_type}</h3>
                  <p className="text-sm text-gray-600 mt-1">Project ID: {anomaly.project_id}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(anomaly.risk_level)}`}>
                  {anomaly.risk_level}
                </span>
              </div>
              {anomaly.explanation && (
                <p className="text-gray-700 mb-3">{anomaly.explanation}</p>
              )}
              <div className="flex justify-between text-sm text-gray-600">
                <span>Score: {anomaly.anomaly_score.toFixed(3)}</span>
                <span>Status: {anomaly.status}</span>
                <span>Detected: {new Date(anomaly.detected_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
