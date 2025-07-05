from .base_agent import BaseAgent
import json
from datetime import datetime

class UserAgent(BaseAgent):
    """Agent responsible for processing user preferences and requirements"""
    
    def __init__(self):
        super().__init__("UserAgent")
        self.preference_categories = {
            'activities': ['culture', 'adventure', 'relaxation', 'food', 'shopping', 'nature'],
            'accommodation': ['luxury', 'budget', 'boutique', 'hostel', 'apartment'],
            'transportation': ['public', 'private', 'walking', 'biking'],
            'dining': ['fine_dining', 'casual', 'street_food', 'local_cuisine'],
            'pace': ['relaxed', 'moderate', 'fast']
        }
    
    def process(self, data):
        """Main processing method"""
        return self.process_preferences(data)
    
    def process_preferences(self, trip_data):
        """Process and validate user preferences"""
        self.log_info("Processing user preferences")
        
        try:
            # Validate required fields
            required_fields = ['destination', 'start_date', 'end_date', 'budget', 'preferences']
            self.validate_input(trip_data, required_fields)
            
            # Process and enhance preferences
            processed_preferences = self._enhance_preferences(trip_data['preferences'])
            
            # Calculate trip duration
            start_date = datetime.strptime(trip_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(trip_data['end_date'], '%Y-%m-%d')
            duration = (end_date - start_date).days
            
            # Create enhanced trip data
            enhanced_data = {
                'destination': trip_data['destination'],
                'start_date': trip_data['start_date'],
                'end_date': trip_data['end_date'],
                'duration': duration,
                'budget': float(trip_data['budget']),
                'preferences': processed_preferences,
                'origin': trip_data.get('origin', ''),
                'travelers': trip_data.get('travelers', 1),
                'processed_at': datetime.now().isoformat()
            }
            
            self.log_info(f"Processed preferences for {duration}-day trip to {trip_data['destination']}")
            return enhanced_data
            
        except Exception as e:
            self.log_error(f"Error processing preferences: {str(e)}")
            raise
    
    def _enhance_preferences(self, preferences):
        """Enhance and validate user preferences"""
        enhanced = {
            'activities': preferences.get('activities', []),
            'accommodation_style': preferences.get('accommodation_style', 'moderate'),
            'transportation_preference': preferences.get('transportation_preference', 'mixed'),
            'dining_preference': preferences.get('dining_preference', 'mixed'),
            'pace': preferences.get('pace', 'moderate'),
            'special_requirements': preferences.get('special_requirements', []),
            'must_see': preferences.get('must_see', []),
            'avoid': preferences.get('avoid', [])
        }
        
        # Validate and normalize preferences
        for category, valid_options in self.preference_categories.items():
            if category in enhanced:
                if isinstance(enhanced[category], list):
                    # Filter out invalid options
                    enhanced[category] = [
                        pref for pref in enhanced[category] 
                        if pref in valid_options
                    ]
                elif enhanced[category] not in valid_options:
                    # Set default if invalid
                    enhanced[category] = valid_options[0]
        
        return enhanced
    
    def get_user_profile(self, user_id=None):
        """Get user profile and preferences (placeholder for future user management)"""
        # This would typically connect to a user database
        return {
            'user_id': user_id,
            'preferences': {
                'activities': ['culture', 'food'],
                'accommodation_style': 'moderate',
                'transportation_preference': 'mixed',
                'dining_preference': 'mixed',
                'pace': 'moderate'
            },
            'travel_history': [],
            'budget_preference': 'moderate'
        } 