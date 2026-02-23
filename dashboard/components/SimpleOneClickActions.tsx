import React, { useState } from 'react';
import { useToast } from './NotificationToast';

interface ActionResult {
  success: boolean;
  message: string;
  data?: any;
}

interface SimpleOneClickActionsProps {
  businessId: string;
}

const SimpleOneClickActions: React.FC<SimpleOneClickActionsProps> = ({ businessId }) => {
  const [loading, setLoading] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, ActionResult>>({});
  const { showSuccess, showError, ToastContainer } = useToast();

  const executeAction = async (actionId: string, actionName: string) => {
    setLoading(actionId);
    try {
      let apiResult;
      switch (actionId) {
        case 'create-sprint':
          apiResult = await QuickActionsAPI.createSprint({ business_id: businessId, sprint_duration: 14 });
          break;
        case 'investor-update':
          apiResult = await QuickActionsAPI.investorUpdate({ business_id: businessId, period: 'monthly', include_financials: true, include_metrics: true });
          break;
        case 'deploy-feature':
          apiResult = await QuickActionsAPI.deployFeature({ business_id: businessId, environment: 'staging', run_tests: true });
          break;
        case 'team-checkin':
          apiResult = await QuickActionsAPI.teamCheckin({ business_id: businessId, include_mood: true, include_blockers: true, generate_summary: true });
          break;
        case 'generate-report':
          apiResult = await QuickActionsAPI.generateReport({ business_id: businessId, report_type: 'comprehensive', include_predictions: true, include_recommendations: true, time_period: 'last_30_days' });
          break;
        default:
          throw new Error('Unknown action');
      }

      const result = {
        success: apiResult.success,
        message: apiResult.message,
        data: apiResult.data,
      };

      setResults(prev => ({ ...prev, [actionId]: result }));
      showSuccess(
        `${actionName} Completed!`,
        result.message,
        {
          label: 'View Details',
          onClick: () => console.log(`Viewing details for ${actionName}`),
        }
      );
    } catch (err: any) {
      setResults(prev => ({ ...prev, [actionId]: { success: false, message: err.message } }));
      showError(`${actionName} Failed`, err.message);
    } finally {
      setLoading(null);
    }
  };

  const actions = [
    { id: 'create-sprint', name: 'Create Sprint', color: 'bg-blue-500', time: '30s' },
    { id: 'investor-update', name: 'Send Investor Update', color: 'bg-green-500', time: '45s' },
    { id: 'deploy-feature', name: 'Deploy Feature', color: 'bg-purple-500', time: '2m' },
    { id: 'team-checkin', name: 'Team Check-in', color: 'bg-orange-500', time: '1m' },
    { id: 'generate-report', name: 'Generate Report', color: 'bg-indigo-500', time: '1m' }
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="flex items-center space-x-3 mb-6">
        <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
          <span className="text-white font-bold">⚡</span>
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">One-Click Actions</h2>
          <p className="text-sm text-gray-600">Execute common founder tasks instantly</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {actions.map((action) => {
          const isLoading = loading === action.id;
          const result = results[action.id];
          
          return (
            <div
              key={action.id}
              className={`relative p-4 rounded-lg border-2 border-gray-200 transition-all duration-200 cursor-pointer hover:border-blue-300 hover:shadow-md ${action.color.replace('bg-', 'hover:bg-').replace('500', '50')}`}
              onClick={() => !isLoading && executeAction(action.id, action.name)}
            >
              {isLoading && (
                <div className="absolute inset-0 bg-white bg-opacity-75 rounded-lg flex items-center justify-center">
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                    <span className="text-sm font-medium text-gray-700">Executing...</span>
                  </div>
                </div>
              )}

              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg ${action.color}`}>
                  <span className="text-white font-bold">🚀</span>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-semibold text-gray-900 mb-1">{action.name}</h3>
                  <p className="text-xs text-gray-600 mb-2">AI-powered automation</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">⏱️ {action.time}</span>
                    {result && (
                      <span className="text-xs font-medium text-green-600">
                        ✅ Done
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {result && (
                <div className="mt-3 p-2 rounded text-xs bg-green-50 text-green-700 border border-green-200">
                  {result.message}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-bold text-gray-900">{Object.keys(results).length}</div>
          <div className="text-xs text-gray-600">Actions Executed</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-bold text-green-600">
            {Object.values(results).filter(r => r.success).length}
          </div>
          <div className="text-xs text-gray-600">Successful</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-bold text-blue-600">4.2h</div>
          <div className="text-xs text-gray-600">Time Saved</div>
        </div>
      </div>
      
      {/* Toast Notifications */}
      <ToastContainer />
    </div>
  );
};

import { QuickActionsAPI } from '../utils/quickActionsClient';
export default SimpleOneClickActions;