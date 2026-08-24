import { useState } from 'react';
import { AlertTriangle, CalendarClock, CheckCircle2, Download, FileText } from 'lucide-react';
import { reportsApi } from '../services/api';

const reports = [
  { title: 'High Risk Projects', type: 'high-risk', description: 'Projects requiring immediate review', icon: AlertTriangle, tone: 'text-emerald-300 bg-emerald-950' },
  { title: 'Delayed Projects', type: 'delayed', description: 'Works beyond their expected completion date', icon: CalendarClock, tone: 'text-emerald-300 bg-emerald-950' },
  { title: 'Cost Overrun', type: 'cost-overrun', description: 'Projects exceeding their estimated cost', icon: FileText, tone: 'text-emerald-300 bg-emerald-950' },
  { title: 'Compliance Report', type: 'compliance', description: 'Data quality and compliance review', icon: CheckCircle2, tone: 'text-emerald-300 bg-emerald-950' },
];

export default function ReportsPage() {
  const [generating, setGenerating] = useState<string | null>(null);
  const [message, setMessage] = useState('');

  const generateReport = async (type: string, title: string) => {
    try {
      setGenerating(type);
      const response = type === 'high-risk' ? await reportsApi.getHighRisk() : type === 'delayed' ? await reportsApi.getDelayed() : type === 'cost-overrun' ? await reportsApi.getCostOverrun() : await reportsApi.getCompliance();
      const exportType = type === 'high-risk' || type === 'delayed' ? type : 'all';
      const exportResponse = await reportsApi.exportCSV(exportType);
      const blob = new Blob([exportResponse.data.csv_data], { type: 'text/csv;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = exportResponse.data.filename || `mplads_${type}_report.csv`;
      link.click();
      URL.revokeObjectURL(url);
      const count = response.data.projects?.length ?? response.data.total_high_risk ?? response.data.total_delayed ?? response.data.total_cost_overrun ?? 0;
      setMessage(`${title} generated successfully: ${count} records downloaded.`);
    } catch (error: any) {
      setMessage(`Unable to generate report: ${error.response?.data?.message || error.message}`);
    } finally {
      setGenerating(null);
    }
  };

  return (
    <div className="space-y-8">
      <div className="page-header-accent">
        <p className="eyebrow">Evidence & oversight</p>
        <h1 className="text-3xl font-bold text-slate-950">Reports</h1>
        <p className="text-slate-600 mt-2">Generate audit-ready extracts from the current MPLADS monitoring dataset.</p>
      </div>
      {message && <div className="notice-success"><CheckCircle2 className="w-5 h-5" />{message}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {reports.map(({ title, type, description, icon: Icon, tone }) => (
          <div key={type} className="surface-panel p-6 flex flex-col justify-between min-h-56">
            <div>
              <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${tone}`}><Icon className="w-5 h-5" /></div>
              <h3 className="text-lg font-semibold text-slate-950 mt-5">{title}</h3>
              <p className="text-sm text-slate-500 mt-2">{description}</p>
            </div>
            <button onClick={() => generateReport(type, title)} disabled={generating !== null} className="action-button action-button-primary mt-6 w-fit">
              <Download className="w-4 h-4" />{generating === type ? 'Generating...' : 'Generate & download'}
            </button>
          </div>
        ))}
      </div>
      <div className="notice-info"><FileText className="w-5 h-5" /><span>Reports contain fictional demonstration data and are intended for review and prototype evaluation.</span></div>
    </div>
  );
}
