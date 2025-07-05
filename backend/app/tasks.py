from app.celery_app import celery_app
from app.agents.user_agent import UserAgent
from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.recommendation_agent import RecommendationAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def plan_trip_task(self, trip_data):
    """Main task that coordinates all agents for trip planning"""
    try:
        logger.info(f"Starting trip planning for destination: {trip_data['destination']}")
        
        # Initialize agents
        user_agent = UserAgent()
        flight_agent = FlightAgent()
        hotel_agent = HotelAgent()
        itinerary_agent = ItineraryAgent()
        budget_agent = BudgetAgent()
        recommendation_agent = RecommendationAgent()
        
        # Step 1: Process user preferences
        self.update_state(state='PROGRESS', meta={'step': 'Processing user preferences'})
        user_preferences = user_agent.process_preferences(trip_data)
        
        # Step 2: Search for flights
        self.update_state(state='PROGRESS', meta={'step': 'Searching flights'})
        flights = flight_agent.search_flights({
            'origin': trip_data.get('origin', ''),
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'budget': trip_data['budget']
        })
        
        # Step 3: Search for hotels
        self.update_state(state='PROGRESS', meta={'step': 'Searching hotels'})
        hotels = hotel_agent.search_hotels({
            'destination': trip_data['destination'],
            'check_in': trip_data['start_date'],
            'check_out': trip_data['end_date'],
            'budget': trip_data['budget'],
            'preferences': trip_data['preferences']
        })
        
        # Step 4: Get recommendations
        self.update_state(state='PROGRESS', meta={'step': 'Getting recommendations'})
        recommendations = recommendation_agent.get_recommendations({
            'destination': trip_data['destination'],
            'preferences': trip_data['preferences'],
            'budget': trip_data['budget']
        })
        
        # Step 5: Create itinerary
        self.update_state(state='PROGRESS', meta={'step': 'Creating itinerary'})
        itinerary = itinerary_agent.create_itinerary({
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'preferences': trip_data['preferences'],
            'recommendations': recommendations,
            'flights': flights,
            'hotels': hotels
        })
        
        # Step 6: Budget analysis
        self.update_state(state='PROGRESS', meta={'step': 'Analyzing budget'})
        budget_analysis = budget_agent.analyze_budget({
            'flights': flights,
            'hotels': hotels,
            'itinerary': itinerary,
            'total_budget': trip_data['budget']
        })
        
        # Step 7: Finalize trip plan
        self.update_state(state='PROGRESS', meta={'step': 'Finalizing trip plan'})
        
        trip_plan = {
            'trip_id': f"trip_{self.request.id}",
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'flights': flights,
            'hotels': hotels,
            'itinerary': itinerary,
            'recommendations': recommendations,
            'budget_analysis': budget_analysis,
            'total_cost': budget_analysis.get('total_cost', 0),
            'budget_remaining': budget_analysis.get('budget_remaining', 0),
            'status': 'completed'
        }
        
        logger.info(f"Trip planning completed successfully for {trip_data['destination']}")
        return trip_plan
        
    except Exception as e:
        logger.error(f"Error in trip planning: {str(e)}")
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise

@celery_app.task
def search_flights_task(search_data):
    """Task for searching flights"""
    try:
        flight_agent = FlightAgent()
        return flight_agent.search_flights(search_data)
    except Exception as e:
        logger.error(f"Error searching flights: {str(e)}")
        raise

@celery_app.task
def search_hotels_task(search_data):
    """Task for searching hotels"""
    try:
        hotel_agent = HotelAgent()
        return hotel_agent.search_hotels(search_data)
    except Exception as e:
        logger.error(f"Error searching hotels: {str(e)}")
        raise

@celery_app.task
def get_recommendations_task(data):
    """Task for getting recommendations"""
    try:
        recommendation_agent = RecommendationAgent()
        return recommendation_agent.get_recommendations(data)
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise 