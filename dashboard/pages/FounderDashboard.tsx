import React, { useState, useEffect } from 'react';
import SimpleOneClickActions from '../components/SimpleOneClickActions';
import { 
  ChartBarIcon, 
  CogIcon, 
  BellIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline';

interface BusinessMetrics {
  revenue: number;
  growth_rate: number;
  active_users: number;
  team_size: number;
  health_score: number;
}

const FounderDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<BusinessMetrics>({
    revenue: 125000,
    growth_rate: 23.5,
    active_users: 2847,
    team_size: 8,
    health_score: 87
  });

  const [notifications, setNotifications] = useState([
    {
      id: 1,
      type: 'success',
      title: 'Sprint Completed',
      message: 'Q4 Development Sprint completed with 95% task completion rate',
      timestamp: '2 hours ago'
    },
    {
      id: 2,
      type: 'info',
      title: 'Investor Update Sent',
      message: 'Monthly investor update sent to 12 investors',
      timestamp: '1 day ago'
    },
    {
      id: 3,
      type: 'warning',
      title: 'Team Check-in Due',
      message: 'Weekly team check-in scheduled for today at 3 PM',
      timestamp: '3 hours ago'
    }
  ]);

  // Simulate real-time updates
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        active_users: prev.active_users + Math.floor(Math.random() * 10),
        health_score: Math.min(100, prev.health_score + (Math.random() - 0.5) * 2)
      }));
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getHealthScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getHealthScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">FD</span>
                </div>
                <h1 className="text-xl font-bold text-gray-900">Founder Dashboard</h1>
              </div>
              <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
                <span>•</span>
                <span>FitTrack Pro</span>
                <span>•</span>
                <span className="text-green-600 font-medium">Active</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <div className="relative">
                <button className="p-2 text-gray-400 hover:text-gray-600 relative">
                  <BellIcon className="h-6 w-6" />
                  <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                    {notifications.length}
                  </span>
                </button>
              </div>
              
              {/* Settings */}
              <button className="p-2 text-gray-400 hover:text-gray-600">
                <CogIcon className="h-6 w-6" />
              </button>
              
              {/* Profile */}
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <span className="text-gray-600 font-medium text-sm">JD</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Business Health Score */}
        <div className="mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">Business Health Score</h2>
              <div className="text-sm text-gray-500">Last updated: just now</div>
            </div>
            
            <div className="flex items-center space-x-8">
              {/* Health Score Circle */}
              <div className="relative">
                <div className={`w-24 h-24 rounded-full ${getHealthScoreBg(metrics.health_score)} flex items-center justify-center`}>
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getHealthScoreColor(metrics.health_score)}`}>
                      {Math.round(metrics.health_score)}
                    </div>
                    <div className="text-xs text-gray-600">Health</div>
                  </div>
                </div>
              </div>
              
              {/* Key Metrics */}
              <div className="flex-1 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center mb-1">
                    <CurrencyDollarIcon className="h-5 w-5 text-green-600 mr-1" />
                    <span className="text-lg font-bold text-gray-900">
                      ${(metrics.revenue / 1000).toFixed(0)}K
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">Monthly Revenue</div>
                </div>
                
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center mb-1">
                    <ArrowTrendingUpIcon className="h-5 w-5 text-blue-600 mr-1" />
                    <span className="text-lg font-bold text-gray-900">
                      {metrics.growth_rate.toFixed(1)}%
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">Growth Rate</div>
                </div>
                
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center mb-1">
                    <ChartBarIcon className="h-5 w-5 text-purple-600 mr-1" />
                    <span className="text-lg font-bold text-gray-900">
                      {metrics.active_users.toLocaleString()}
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">Active Users</div>
                </div>
                
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-center mb-1">
                    <UserGroupIcon className="h-5 w-5 text-orange-600 mr-1" />
                    <span className="text-lg font-bold text-gray-900">
                      {metrics.team_size}
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">Team Members</div>
                </div>
              </div>
            </div>
            
            {/* Health Insights */}
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="text-sm">
                <span className="font-medium text-blue-900">AI Insight: </span>
                <span className="text-blue-700">
                  Your business health is strong at {Math.round(metrics.health_score)}%. 
                  Revenue growth of {metrics.growth_rate.toFixed(1)}% is above industry average. 
                  Consider expanding your team to support continued growth.
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* One-Click Actions Component */}
        <SimpleOneClickActions businessId="fittrack_pro" />

        {/* Recent Activity & Notifications */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Recent Activity */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Activity</h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">Sprint Created Successfully</div>
                  <div className="text-xs text-gray-600">AI generated 12 tasks for Q4 development sprint</div>
                  <div className="text-xs text-gray-500 mt-1">2 minutes ago</div>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">Team Check-in Completed</div>
                  <div className="text-xs text-gray-600">Collected status from 8 team members</div>
                  <div className="text-xs text-gray-500 mt-1">1 hour ago</div>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 p-3 bg-purple-50 rounded-lg">
                <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">Features Deployed</div>
                  <div className="text-xs text-gray-600">3 features deployed to staging environment</div>
                  <div className="text-xs text-gray-500 mt-1">3 hours ago</div>
                </div>
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-bold text-gray-900 mb-4">Notifications</h3>
            <div className="space-y-3">
              {notifications.map((notification) => (
                <div key={notification.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    notification.type === 'success' ? 'bg-green-500' :
                    notification.type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-900">{notification.title}</div>
                    <div className="text-xs text-gray-600">{notification.message}</div>
                    <div className="text-xs text-gray-500 mt-1">{notification.timestamp}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-gray-900">15</div>
                <div className="text-sm text-gray-600">Actions This Week</div>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <ChartBarIcon className="h-6 w-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-green-600">+20% from last week</div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-gray-900">4.2h</div>
                <div className="text-sm text-gray-600">Time Saved</div>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <ArrowTrendingUpIcon className="h-6 w-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-green-600">Automation efficiency</div>
          </div>
          
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-gray-900">98%</div>
                <div className="text-sm text-gray-600">Success Rate</div>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <UserGroupIcon className="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-green-600">All systems operational</div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default FounderDashboard;