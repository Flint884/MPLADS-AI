export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Application configuration and preferences</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">About This Application</h2>
        <div className="space-y-3 text-gray-600">
          <p><strong>Application:</strong> MPLADS Sentinel AI</p>
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Purpose:</strong> AI-powered anomaly detection and monitoring for MPLADS Scheme</p>
        </div>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-yellow-900 mb-3">⚠️ Responsible AI</h2>
        <p className="text-yellow-800 text-sm">
          All AI-generated anomaly scores and risk assessments are decision-support indicators based on available data and statistical models. 
          They do not constitute proof of fraud or wrongdoing. All high-risk cases require review and authorization by human officials.
        </p>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-blue-900 mb-3">📋 Demo Data Notice</h2>
        <p className="text-blue-800 text-sm">
          This application uses completely fictional demonstration data for testing and showcasing functionality. 
          No real projects, individuals, or financial information is used.
        </p>
      </div>
    </div>
  );
}
