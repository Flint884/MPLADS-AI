import { useEffect, useState } from 'react';
import { Activity, Database, FileUp, RefreshCw, RotateCcw, ShieldCheck } from 'lucide-react';
import { analysisApi, dataApi } from '../services/api';

interface DatasetInfo { project_count: number; total_fund_allocated?: number; data_type?: string; }

export default function DataManagementPage() {
  const [info, setInfo] = useState<DatasetInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const loadInfo = async () => {
    const response = await dataApi.getDemoInfo();
    setInfo(response.data);
  };

  useEffect(() => { loadInfo().catch(() => setMessage('Unable to connect to the data service.')); }, []);

  const runAction = async (action: () => Promise<any>, success: (data: any) => string) => {
    try { setLoading(true); setMessage(''); const response = await action(); setMessage(success(response.data)); await loadInfo(); }
    catch (error: any) { setMessage(`Action failed: ${error.response?.data?.message || error.message}`); }
    finally { setLoading(false); }
  };

  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) await runAction(() => dataApi.importCSV(file), (data) => `Imported ${data.imported_count || 0} projects successfully.`);
    event.target.value = '';
  };

  const regenerateDemo = async () => {
    await dataApi.clearAll();
    const generated = await dataApi.generateDemo();
    const analysis = await analysisApi.runFullAnalysis();
    return { data: { ...generated.data, analysis: analysis.data } };
  };

  return (
    <div className="space-y-8">
      <div className="page-header-accent">
        <p className="eyebrow">Data operations</p>
        <h1 className="text-3xl font-bold text-slate-950">Data Management</h1>
        <p className="text-slate-600 mt-2">Control the monitoring dataset, refresh intelligence, and validate source coverage.</p>
      </div>
      {message && <div className={message.includes('failed') || message.includes('Unable') ? 'notice-error' : 'notice-success'}><Activity className="w-5 h-5" />{message}</div>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="metric-panel"><Database className="w-5 h-5 text-blue-700" /><span>Projects loaded</span><strong>{info?.project_count ?? '—'}</strong></div>
        <div className="metric-panel"><ShieldCheck className="w-5 h-5 text-emerald-700" /><span>Dataset status</span><strong>{info?.project_count ? 'Ready' : 'Empty'}</strong></div>
        <div className="metric-panel"><Activity className="w-5 h-5 text-amber-700" /><span>Coverage</span><strong>{info?.project_count ? 'National' : 'Awaiting data'}</strong></div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <section className="surface-panel p-6">
          <p className="eyebrow">Prototype workspace</p><h2 className="text-xl font-semibold text-slate-950 mt-2">Demo dataset</h2>
          <p className="text-sm text-slate-500 mt-2">Load a fictional 150-project portfolio spanning every Indian state and union territory.</p>
          <button disabled={loading} onClick={() => runAction(regenerateDemo, (data) => `Generated ${data.projects_created || 0} demo projects and found ${data.analysis?.anomaly_detection?.anomalies_detected || 0} anomalies.`)} className="action-button action-button-primary mt-6"><RefreshCw className="w-4 h-4" />{loading ? 'Generating and analyzing...' : 'Regenerate demo data'}</button>
        </section>
        <section className="surface-panel p-6">
          <p className="eyebrow">Source intake</p><h2 className="text-xl font-semibold text-slate-950 mt-2">Import project records</h2>
          <p className="text-sm text-slate-500 mt-2">Upload a CSV using the required project, location, category, and financial columns.</p>
          <label className="action-button action-button-secondary mt-6 w-fit"><FileUp className="w-4 h-4" />Choose CSV<input type="file" accept=".csv" onChange={handleUpload} disabled={loading} className="hidden" /></label>
        </section>
        <section className="surface-panel p-6 lg:col-span-2 flex flex-col md:flex-row md:items-center md:justify-between gap-5">
          <div><p className="eyebrow">Intelligence pipeline</p><h2 className="text-xl font-semibold text-slate-950 mt-2">Refresh monitoring signals</h2><p className="text-sm text-slate-500 mt-2">Recalculate risk scores, statistical anomalies, and duplicate-work indicators.</p></div>
          <button disabled={loading || !info?.project_count} onClick={() => runAction(analysisApi.runFullAnalysis, (data) => `Analysis complete: ${data.anomaly_detection?.anomalies_detected || 0} anomalies, ${data.duplicate_detection?.duplicates_detected || 0} duplicate signals, and ${data.risk_scoring?.scores_calculated || 0} risk scores.`)} className="action-button action-button-primary"><Activity className="w-4 h-4" />Run full analysis</button>
        </section>
        <section className="surface-panel p-6 lg:col-span-2 flex flex-col md:flex-row md:items-center md:justify-between gap-5 border-red-200">
          <div><p className="eyebrow text-red-700">Administrative action</p><h2 className="text-xl font-semibold text-slate-950 mt-2">Reset demo workspace</h2><p className="text-sm text-slate-500 mt-2">Remove all project records before importing a clean dataset.</p></div>
          <button disabled={loading} onClick={() => runAction(dataApi.clearAll, () => 'Workspace cleared. Generate or import a dataset to continue.')} className="action-button action-button-danger"><RotateCcw className="w-4 h-4" />Clear all data</button>
        </section>
      </div>
      <div className="notice-info"><ShieldCheck className="w-5 h-5" /><span>{info?.data_type || 'Fictional demonstration data'} is used for this prototype. No real government records are included.</span></div>
    </div>
  );
}
