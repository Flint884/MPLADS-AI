import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { projectsApi } from '../services/api';
import { Project } from '../types';
import { ArrowLeft } from 'lucide-react';

export default function ProjectDetailsPage() {
  const { id } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [riskScore, setRiskScore] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchProjectDetails();
    }
  }, [id]);

  const fetchProjectDetails = async () => {
    try {
      const res = await projectsApi.get(parseInt(id!));
      setProject(res.data.project);
      setRiskScore({
        overall_score: res.data.risk_score,
        risk_category: res.data.risk_category,
      });
    } catch (err) {
      console.error('Error fetching project:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!project) return <div>Project not found</div>;

  const getRiskColor = (risk?: string) => {
    switch (risk) {
      case 'Low':
        return 'text-green-600 bg-green-50';
      case 'Medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'High':
        return 'text-orange-600 bg-orange-50';
      case 'Critical':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      <button className="flex items-center gap-2 text-blue-600 hover:text-blue-700">
        <ArrowLeft className="w-4 h-4" />
        Back to Projects
      </button>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{project.project_name}</h1>
            <p className="text-gray-600 mt-2">{project.project_id}</p>
          </div>
          <div className={`px-4 py-2 rounded-lg font-semibold ${getRiskColor(riskScore?.risk_category)}`}>
            {riskScore?.risk_category || 'Not Assessed'}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="border-l-4 border-blue-500 pl-4">
            <p className="text-sm text-gray-600">Location</p>
            <p className="text-lg font-semibold text-gray-900">{project.state}, {project.district}</p>
          </div>
          <div className="border-l-4 border-green-500 pl-4">
            <p className="text-sm text-gray-600">Category</p>
            <p className="text-lg font-semibold text-gray-900">{project.category}</p>
          </div>
          <div className="border-l-4 border-purple-500 pl-4">
            <p className="text-sm text-gray-600">Status</p>
            <p className="text-lg font-semibold text-gray-900">{project.status}</p>
          </div>
          <div className="border-l-4 border-orange-500 pl-4">
            <p className="text-sm text-gray-600">Progress</p>
            <p className="text-lg font-semibold text-gray-900">{project.progress_percentage.toFixed(1)}%</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Financial Information</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Estimated Cost</span>
                <span className="font-medium">₹{(project.estimated_cost / 1000000).toFixed(2)}M</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Sanctioned Amount</span>
                <span className="font-medium">₹{(project.sanctioned_amount / 1000000).toFixed(2)}M</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Amount Released</span>
                <span className="font-medium">₹{(project.amount_released / 1000000).toFixed(2)}M</span>
              </div>
              <div className="flex justify-between border-t pt-3">
                <span className="text-gray-600 font-semibold">Actual Expenditure</span>
                <span className="font-bold text-lg">₹{(project.actual_expenditure / 1000000).toFixed(2)}M</span>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Implementation Details</h2>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Implementing Agency</span>
                <span className="font-medium">{project.implementing_agency || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">MP Name</span>
                <span className="font-medium">{project.mp_name || 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Sanction Date</span>
                <span className="font-medium">{project.sanction_date ? new Date(project.sanction_date).toLocaleDateString() : 'N/A'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Expected Completion</span>
                <span className="font-medium">{project.expected_completion_date ? new Date(project.expected_completion_date).toLocaleDateString() : 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>

        {riskScore && (
          <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 className="text-lg font-semibold text-blue-900 mb-4">AI Risk Assessment</h2>
            <p className="text-blue-800">Risk Score: {riskScore.overall_score?.toFixed(1) || 'N/A'} / 100</p>
          </div>
        )}
      </div>
    </div>
  );
}
