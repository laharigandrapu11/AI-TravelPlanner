from flask import Flask, request, jsonify
from flask_cors import CORS
from celery.result import AsyncResult
import os
from dotenv import load_dotenv
from app.agents.user_agent import UserAgent
from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.celery_app import celery_app
from app.tasks import plan_trip_task

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize agents
user_agent = UserAgent()
flight_agent = FlightAgent()
hotel_agent = HotelAgent()
itinerary_agent = ItineraryAgent()
budget_agent = BudgetAgent()
recommendation_agent = RecommendationAgent()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'SmartTripPlanner API Gateway'})

@app.route('/api/plan-trip', methods=['POST'])
def plan_trip():
    """Main endpoint for trip planning - coordinates all agents"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['destination', 'start_date', 'end_date', 'budget', 'preferences']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Start the trip planning process
        task = plan_trip_task.delay(data)
        
        return jsonify({
            'message': 'Trip planning started',
            'task_id': task.id,
            'status': 'processing'
        }), 202
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trip-status/<task_id>', methods=['GET'])
def get_trip_status(task_id):
    """Check the status of a trip planning task"""
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.ready():
            if task_result.successful():
                return jsonify({
                    'status': 'completed',
                    'result': task_result.result
                })
            else:
                return jsonify({
                    'status': 'failed',
                    'error': str(task_result.result)
                }), 500
        else:
            return jsonify({
                'status': 'processing',
                'task_id': task_id
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/flights/search', methods=['POST'])
def search_flights():
    """Search for flights using FlightAgent"""
    try:
        data = request.get_json()
        flights = flight_agent.search_flights(data)
        return jsonify(flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/hotels/search', methods=['POST'])
def search_hotels():
    """Search for hotels using HotelAgent"""
    try:
        data = request.get_json()
        hotels = hotel_agent.search_hotels(data)
        return jsonify(hotels)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized recommendations using RecommendationAgent"""
    try:
        data = request.get_json()
        recommendations = recommendation_agent.get_recommendations(data)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/budget/analyze', methods=['POST'])
def analyze_budget():
    """Analyze budget using BudgetAgent"""
    try:
        data = request.get_json()
        analysis = budget_agent.analyze_budget(data)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 