import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plane, MapPin, Calendar, DollarSign, TrendingUp, Users, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Dashboard = () => {
  const [tripHistory, setTripHistory] = useState([]);
  const [stats, setStats] = useState({
    totalTrips: 0,
    totalSpent: 0,
    averageBudget: 0,
    favoriteDestination: ''
  });

  useEffect(() => {
    // Mock data for demo purposes
    const mockTripHistory = [
      {
        id: 'trip_1',
        destination: 'Rome, Italy',
        startDate: '2024-03-15',
        endDate: '2024-03-20',
        budget: 1500,
        actualCost: 1420,
        status: 'completed'
      },
      {
        id: 'trip_2',
        destination: 'Paris, France',
        startDate: '2024-02-10',
        endDate: '2024-02-15',
        budget: 2000,
        actualCost: 1850,
        status: 'completed'
      },
      {
        id: 'trip_3',
        destination: 'Tokyo, Japan',
        startDate: '2024-04-01',
        endDate: '2024-04-08',
        budget: 3000,
        actualCost: 3200,
        status: 'completed'
      }
    ];

    setTripHistory(mockTripHistory);

    // Calculate stats
    const totalTrips = mockTripHistory.length;
    const totalSpent = mockTripHistory.reduce((sum, trip) => sum + trip.actualCost, 0);
    const averageBudget = mockTripHistory.reduce((sum, trip) => sum + trip.budget, 0) / totalTrips;
    const favoriteDestination = 'Rome, Italy'; // In real app, calculate from history

    setStats({
      totalTrips,
      totalSpent,
      averageBudget,
      favoriteDestination
    });
  }, []);

  const budgetData = [
    { name: 'Flights', value: 40, color: '#3B82F6' },
    { name: 'Hotels', value: 30, color: '#10B981' },
    { name: 'Activities', value: 15, color: '#8B5CF6' },
    { name: 'Food', value: 10, color: '#F59E0B' },
    { name: 'Transport', value: 5, color: '#EF4444' }
  ];

  const spendingTrend = [
    { month: 'Jan', spent: 1200 },
    { month: 'Feb', spent: 1850 },
    { month: 'Mar', spent: 1420 },
    { month: 'Apr', spent: 3200 },
    { month: 'May', spent: 0 },
    { month: 'Jun', spent: 0 }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Travel Dashboard</h1>
          <p className="text-gray-600">Track your trips and travel spending</p>
        </div>
        <Link to="/" className="btn-primary">
          Plan New Trip
        </Link>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="bg-blue-100 p-3 rounded-lg">
              <Plane className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Trips</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalTrips}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="bg-green-100 p-3 rounded-lg">
              <DollarSign className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Spent</p>
              <p className="text-2xl font-bold text-gray-900">${stats.totalSpent.toLocaleString()}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="bg-purple-100 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Budget</p>
              <p className="text-2xl font-bold text-gray-900">${stats.averageBudget.toFixed(0)}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="bg-yellow-100 p-3 rounded-lg">
              <MapPin className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Favorite Destination</p>
              <p className="text-lg font-bold text-gray-900">{stats.favoriteDestination}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Spending Trend */}
        <div className="card">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Spending Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={spendingTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => [`$${value}`, 'Spent']} />
              <Line type="monotone" dataKey="spent" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Budget Breakdown */}
        <div className="card">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Budget Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={budgetData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {budgetData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => [`${value}%`, 'Budget']} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Trips */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Recent Trips</h3>
        <div className="space-y-4">
          {tripHistory.map((trip) => (
            <div key={trip.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h4 className="text-lg font-semibold text-gray-900">{trip.destination}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      trip.status === 'completed' 
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {trip.status}
                    </span>
                  </div>
                  <div className="flex items-center space-x-6 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {trip.startDate} - {trip.endDate}
                    </div>
                    <div className="flex items-center">
                      <DollarSign className="h-4 w-4 mr-1" />
                      Budget: ${trip.budget} | Spent: ${trip.actualCost}
                    </div>
                  </div>
                </div>
                <Link 
                  to={`/results/${trip.id}`}
                  className="btn-secondary text-sm"
                >
                  View Details
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h3 className="text-xl font-bold text-gray-900 mb-6">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link 
            to="/"
            className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors"
          >
            <Plane className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <div className="font-medium text-gray-900">Plan New Trip</div>
              <div className="text-sm text-gray-600">Start planning your next adventure</div>
            </div>
          </Link>

          <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors text-left">
            <Users className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <div className="font-medium text-gray-900">Share Trip</div>
              <div className="text-sm text-gray-600">Share your trip with friends</div>
            </div>
          </button>

          <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors text-left">
            <Clock className="h-6 w-6 text-primary-600 mr-3" />
            <div>
              <div className="font-medium text-gray-900">Trip History</div>
              <div className="text-sm text-gray-600">View all your past trips</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 