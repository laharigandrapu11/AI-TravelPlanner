import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Plane, MapPin, Calendar, DollarSign, Clock, Star, Users } from 'lucide-react';
import apiClient from '../config/api';

const TripResults = () => {
  const { tripId } = useParams();
  const [tripData, setTripData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTripData();
  }, [tripId]);

  const fetchTripData = async () => {
    try {
      const response = await apiClient.get(`/api/trip-status/${tripId}`);
      if (response.data.status === 'completed') {
        setTripData(response.data.result);
      } else {
        setError('Trip data not found or still processing');
      }
    } catch (error) {
      setError('Failed to load trip data');
      console.error('Error fetching trip data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your trip plan...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 mb-4">
          <Plane className="h-12 w-12 mx-auto mb-2" />
          <h2 className="text-xl font-semibold">Error Loading Trip</h2>
        </div>
        <p className="text-gray-600">{error}</p>
      </div>
    );
  }

  if (!tripData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No trip data available</p>
      </div>
    );
  }

  const { flights, hotels, itinerary, recommendations, budget_analysis } = tripData;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Trip Summary */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Your Trip to {tripData.destination}
            </h1>
            <p className="text-gray-600">
              {tripData.start_date} - {tripData.end_date} • {itinerary?.duration || 0} days
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-primary-600">
              ${budget_analysis?.summary?.total_cost?.toFixed(2) || 0}
            </div>
            <div className="text-sm text-gray-500">Total Cost</div>
          </div>
        </div>

        {/* Budget Status */}
        <div className="bg-gray-50 rounded-lg p-4 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-gray-900">Budget Status</h3>
              <p className="text-sm text-gray-600">
                ${budget_analysis?.summary?.budget_remaining?.toFixed(2) || 0} remaining
              </p>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              budget_analysis?.summary?.status === 'within_budget' 
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800'
            }`}>
              {budget_analysis?.summary?.status?.replace('_', ' ').toUpperCase() || 'UNKNOWN'}
            </div>
          </div>
        </div>
      </div>

      {/* Flights Section */}
      {flights && flights.flight_options && flights.flight_options.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Plane className="h-6 w-6 text-blue-600 mr-2" />
            Flights
          </h2>
          <div className="space-y-4">
            {flights.flight_options.slice(0, 3).map((flight, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <div className="font-semibold text-gray-900">
                    {flight.outbound?.departure?.airport} → {flight.outbound?.arrival?.airport}
                  </div>
                  <div className="text-lg font-bold text-primary-600">
                    ${flight.total_price?.toFixed(2)}
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm text-gray-600">
                  <div>
                    <div className="font-medium">Outbound</div>
                    <div>{flight.outbound?.airline} • {flight.outbound?.departure?.time}</div>
                  </div>
                  <div>
                    <div className="font-medium">Return</div>
                    <div>{flight.return?.airline} • {flight.return?.departure?.time}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hotels Section */}
      {hotels && hotels.hotel_options && hotels.hotel_options.length > 0 && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <MapPin className="h-6 w-6 text-green-600 mr-2" />
            Accommodation
          </h2>
          <div className="space-y-4">
            {hotels.hotel_options.slice(0, 3).map((hotel, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="font-semibold text-gray-900">{hotel.name}</div>
                    <div className="text-sm text-gray-600">{hotel.address}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-primary-600">
                      ${hotel.estimated_price?.toFixed(2)}
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      {hotel.rating}
                    </div>
                  </div>
                </div>
                {hotel.amenities && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {hotel.amenities.map((amenity, i) => (
                      <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                        {amenity}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Itinerary Section */}
      {itinerary && itinerary.daily_plans && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Calendar className="h-6 w-6 text-purple-600 mr-2" />
            Daily Itinerary
          </h2>
          <div className="space-y-6">
            {itinerary.daily_plans.map((day, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-3">
                  Day {day.day} - {day.date}
                </h3>
                
                {/* Activities */}
                <div className="space-y-3 mb-4">
                  {day.activities.map((activity, actIndex) => (
                    <div key={actIndex} className="flex items-center space-x-3">
                      <Clock className="h-4 w-4 text-gray-400 flex-shrink-0" />
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">{activity.activity}</div>
                        <div className="text-sm text-gray-600">
                          {activity.time} • {activity.duration}
                        </div>
                      </div>
                      <div className="text-sm text-gray-600">
                        ${activity.estimated_cost?.toFixed(2)}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Meals */}
                <div className="border-t pt-3">
                  <h4 className="font-medium text-gray-900 mb-2">Meals</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {Object.entries(day.meals).map(([mealType, meal]) => (
                      <div key={mealType} className="text-sm">
                        <div className="font-medium capitalize">{mealType}</div>
                        <div className="text-gray-600">{meal.suggestion}</div>
                        <div className="text-gray-500">${meal.estimated_cost?.toFixed(2)}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-3 pt-3 border-t">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Daily Total:</span>
                    <span className="font-semibold">
                      ${day.estimated_cost?.total?.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations Section */}
      {recommendations && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Personalized Recommendations
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(recommendations.activity_recommendations || {}).map(([category, recs]) => (
              <div key={category} className="space-y-3">
                <h3 className="font-semibold text-gray-900 capitalize">
                  {category.replace('_', ' ')}
                </h3>
                <div className="space-y-2">
                  {recs.slice(0, 3).map((rec, index) => (
                    <div key={index} className="text-sm p-3 bg-gray-50 rounded-lg">
                      <div className="font-medium text-gray-900">{rec.name}</div>
                      <div className="text-gray-600 mt-1">{rec.description}</div>
                      <div className="flex justify-between items-center mt-2">
                        <span className="text-gray-500">${rec.estimated_cost?.toFixed(2)}</span>
                        <span className="text-gray-500">{rec.duration}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Budget Analysis */}
      {budget_analysis && (
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <DollarSign className="h-6 w-6 text-yellow-600 mr-2" />
            Budget Analysis
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Cost Breakdown</h3>
              <div className="space-y-2">
                {Object.entries(budget_analysis.summary?.categories || {}).map(([category, data]) => (
                  <div key={category} className="flex justify-between items-center">
                    <span className="capitalize text-gray-700">{category}</span>
                    <span className="font-medium">${data.cost?.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-3">Budget Recommendations</h3>
              <div className="space-y-2">
                {budget_analysis.recommendations?.slice(0, 3).map((rec, index) => (
                  <div key={index} className="text-sm p-3 bg-blue-50 rounded-lg">
                    <div className="font-medium text-blue-900">{rec.message}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TripResults; 