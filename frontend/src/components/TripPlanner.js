import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import Select from 'react-select';
import { Plane, MapPin, Calendar, DollarSign, Users, Sparkles, Loader } from 'lucide-react';
import apiClient from '../config/api';
import 'react-datepicker/dist/react-datepicker.css';

const TripPlanner = () => {
  const navigate = useNavigate();
  const [isPlanning, setIsPlanning] = useState(false);
  const [planningStep, setPlanningStep] = useState('');
  const [formData, setFormData] = useState({
    destination: '',
    origin: '',
    startDate: null,
    endDate: null,
    budget: '',
    travelers: 1,
    activities: [],
    accommodationStyle: 'moderate',
    transportationPreference: 'mixed',
    diningPreference: 'mixed',
    pace: 'moderate'
  });

  const activityOptions = [
    { value: 'culture', label: 'Culture & History' },
    { value: 'adventure', label: 'Adventure & Sports' },
    { value: 'relaxation', label: 'Relaxation & Wellness' },
    { value: 'food', label: 'Food & Dining' },
    { value: 'shopping', label: 'Shopping & Markets' },
    { value: 'nature', label: 'Nature & Outdoors' }
  ];

  const accommodationOptions = [
    { value: 'budget', label: 'Budget' },
    { value: 'moderate', label: 'Moderate' },
    { value: 'luxury', label: 'Luxury' }
  ];

  const transportationOptions = [
    { value: 'public', label: 'Public Transport' },
    { value: 'private', label: 'Private Transport' },
    { value: 'mixed', label: 'Mixed' }
  ];

  const diningOptions = [
    { value: 'fine_dining', label: 'Fine Dining' },
    { value: 'casual', label: 'Casual' },
    { value: 'street_food', label: 'Street Food' },
    { value: 'mixed', label: 'Mixed' }
  ];

  const paceOptions = [
    { value: 'relaxed', label: 'Relaxed' },
    { value: 'moderate', label: 'Moderate' },
    { value: 'fast', label: 'Fast-paced' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.destination || !formData.startDate || !formData.endDate || !formData.budget) {
      alert('Please fill in all required fields');
      return;
    }

    setIsPlanning(true);
    setPlanningStep('Initializing agents...');

    try {
      const tripData = {
        destination: formData.destination,
        origin: formData.origin || 'NYC',
        start_date: formData.startDate.toISOString().split('T')[0],
        end_date: formData.endDate.toISOString().split('T')[0],
        budget: parseFloat(formData.budget),
        travelers: formData.travelers,
        preferences: {
          activities: formData.activities.map(a => a.value),
          accommodation_style: formData.accommodationStyle,
          transportation_preference: formData.transportationPreference,
          dining_preference: formData.diningPreference,
          pace: formData.pace
        }
      };

      setPlanningStep('Processing user preferences...');
      
      // Start trip planning
      const response = await apiClient.post('/api/plan-trip', tripData);
      
      // Check if response is synchronous (completed) or asynchronous (task_id)
      if (response.data.status === 'completed' && response.data.result) {
        // Synchronous response - store result and navigate directly
        const tripId = response.data.result.trip_id || `sync-${Date.now()}`;
        localStorage.setItem(`trip_${tripId}`, JSON.stringify(response.data.result));
        setIsPlanning(false);
        navigate(`/results/${tripId}`);
      } else if (response.data.task_id) {
        // Asynchronous response - poll for completion
        const { task_id } = response.data;
        setPlanningStep('Coordinating agents...');

        // Poll for completion
        const pollInterval = setInterval(async () => {
          try {
            const statusResponse = await apiClient.get(`/api/trip-status/${task_id}`);
            
            if (statusResponse.data.status === 'completed') {
              clearInterval(pollInterval);
              setIsPlanning(false);
              navigate(`/results/${task_id}`);
            } else if (statusResponse.data.status === 'failed') {
              clearInterval(pollInterval);
              setIsPlanning(false);
              alert('Trip planning failed. Please try again.');
            } else {
              setPlanningStep('Creating your perfect itinerary...');
            }
          } catch (error) {
            clearInterval(pollInterval);
            setIsPlanning(false);
            console.error('Error checking trip status:', error);
          }
        }, 2000);
      } else {
        throw new Error('Unexpected response format');
      }

    } catch (error) {
      setIsPlanning(false);
      console.error('Error planning trip:', error);
      alert('Error planning trip. Please try again.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Plan Your Perfect Trip with AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Our intelligent agents work together to create personalized travel experiences
        </p>
        
        {/* Agent Icons */}
        <div className="flex justify-center space-x-8 mb-8">
          <div className="flex flex-col items-center">
            <div className="bg-blue-100 p-3 rounded-full mb-2">
              <Plane className="h-6 w-6 text-blue-600" />
            </div>
            <span className="text-sm text-gray-600">Flight Agent</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-green-100 p-3 rounded-full mb-2">
              <MapPin className="h-6 w-6 text-green-600" />
            </div>
            <span className="text-sm text-gray-600">Hotel Agent</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-purple-100 p-3 rounded-full mb-2">
              <Calendar className="h-6 w-6 text-purple-600" />
            </div>
            <span className="text-sm text-gray-600">Itinerary Agent</span>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-yellow-100 p-3 rounded-full mb-2">
              <DollarSign className="h-6 w-6 text-yellow-600" />
            </div>
            <span className="text-sm text-gray-600">Budget Agent</span>
          </div>
        </div>
      </div>

      {/* Planning Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Trip Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Destination *
              </label>
              <input
                type="text"
                value={formData.destination}
                onChange={(e) => handleInputChange('destination', e.target.value)}
                placeholder="e.g., Rome, Italy"
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Origin (Optional)
              </label>
              <input
                type="text"
                value={formData.origin}
                onChange={(e) => handleInputChange('origin', e.target.value)}
                placeholder="e.g., New York"
                className="input-field"
              />
            </div>
          </div>

          {/* Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Start Date *
              </label>
              <DatePicker
                selected={formData.startDate}
                onChange={(date) => handleInputChange('startDate', date)}
                minDate={new Date()}
                placeholderText="Select start date"
                className="input-field"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                End Date *
              </label>
              <DatePicker
                selected={formData.endDate}
                onChange={(date) => handleInputChange('endDate', date)}
                minDate={formData.startDate || new Date()}
                placeholderText="Select end date"
                className="input-field"
                required
              />
            </div>
          </div>

          {/* Budget and Travelers */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Budget (USD) *
              </label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="number"
                  value={formData.budget}
                  onChange={(e) => handleInputChange('budget', e.target.value)}
                  placeholder="1500"
                  className="input-field pl-10"
                  min="100"
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Travelers
              </label>
              <div className="relative">
                <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="number"
                  value={formData.travelers}
                  onChange={(e) => handleInputChange('travelers', parseInt(e.target.value))}
                  className="input-field pl-10"
                  min="1"
                  max="10"
                />
              </div>
            </div>
          </div>

          {/* Preferences */}
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Activities of Interest
              </label>
              <Select
                isMulti
                value={formData.activities}
                onChange={(selected) => handleInputChange('activities', selected)}
                options={activityOptions}
                placeholder="Select activities..."
                className="react-select-container"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Accommodation Style
                </label>
                <Select
                  value={accommodationOptions.find(opt => opt.value === formData.accommodationStyle)}
                  onChange={(selected) => handleInputChange('accommodationStyle', selected.value)}
                  options={accommodationOptions}
                  className="react-select-container"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Transportation Preference
                </label>
                <Select
                  value={transportationOptions.find(opt => opt.value === formData.transportationPreference)}
                  onChange={(selected) => handleInputChange('transportationPreference', selected.value)}
                  options={transportationOptions}
                  className="react-select-container"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Dining Preference
                </label>
                <Select
                  value={diningOptions.find(opt => opt.value === formData.diningPreference)}
                  onChange={(selected) => handleInputChange('diningPreference', selected.value)}
                  options={diningOptions}
                  className="react-select-container"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Trip Pace
                </label>
                <Select
                  value={paceOptions.find(opt => opt.value === formData.pace)}
                  onChange={(selected) => handleInputChange('pace', selected.value)}
                  options={paceOptions}
                  className="react-select-container"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-center">
            <button
              type="submit"
              disabled={isPlanning}
              className="btn-primary flex items-center space-x-2 px-8 py-3 text-lg disabled:opacity-50"
            >
              {isPlanning ? (
                <>
                  <Loader className="h-5 w-5 animate-spin" />
                  <span>{planningStep}</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5" />
                  <span>Plan My Trip</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TripPlanner; 