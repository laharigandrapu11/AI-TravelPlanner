from .base_agent import BaseAgent
from datetime import datetime, timedelta
import random

class ItineraryAgent(BaseAgent):
    """Agent responsible for creating and optimizing daily itineraries"""
    
    def __init__(self):
        super().__init__("ItineraryAgent")
        self.activity_categories = {
            'culture': ['museums', 'historical_sites', 'art_galleries', 'theaters'],
            'adventure': ['hiking', 'water_sports', 'rock_climbing', 'zip_lining'],
            'relaxation': ['spas', 'beaches', 'parks', 'gardens'],
            'food': ['restaurants', 'food_tours', 'cooking_classes', 'wine_tasting'],
            'shopping': ['markets', 'malls', 'boutiques', 'craft_stores'],
            'nature': ['parks', 'gardens', 'wildlife_reserves', 'botanical_gardens']
        }
        
    def process(self, data):
        """Main processing method"""
        return self.create_itinerary(data)
    
    def create_itinerary(self, itinerary_data):
        """Create a comprehensive daily itinerary"""
        self.log_info("Creating itinerary")
        
        try:
            # Validate required fields
            required_fields = ['destination', 'start_date', 'end_date', 'preferences']
            self.validate_input(itinerary_data, required_fields)
            
            # Extract data
            destination = itinerary_data['destination']
            start_date = datetime.strptime(itinerary_data['start_date'], '%Y-%m-%d')
            end_date = datetime.strptime(itinerary_data['end_date'], '%Y-%m-%d')
            preferences = itinerary_data['preferences']
            recommendations = itinerary_data.get('recommendations', {})
            flights = itinerary_data.get('flights', {})
            hotels = itinerary_data.get('hotels', {})
            
            # Calculate trip duration
            duration = (end_date - start_date).days
            
            # Create daily itineraries
            daily_itineraries = []
            
            for day in range(duration):
                current_date = start_date + timedelta(days=day)
                day_itinerary = self._create_daily_plan(
                    destination, current_date, day + 1, preferences, recommendations
                )
                daily_itineraries.append(day_itinerary)
            
            # Create overall itinerary
            itinerary = {
                'destination': destination,
                'start_date': itinerary_data['start_date'],
                'end_date': itinerary_data['end_date'],
                'duration': duration,
                'daily_plans': daily_itineraries,
                'transportation': self._plan_transportation(flights, hotels, duration),
                'budget_breakdown': self._calculate_budget_breakdown(daily_itineraries),
                'created_at': datetime.now().isoformat()
            }
            
            self.log_info(f"Created {duration}-day itinerary for {destination}")
            return itinerary
            
        except Exception as e:
            self.log_error(f"Error creating itinerary: {str(e)}")
            raise
    
    def _create_daily_plan(self, destination, date, day_number, preferences, recommendations):
        """Create a detailed plan for a single day"""
        activities = preferences.get('activities', [])
        pace = preferences.get('pace', 'moderate')
        
        # Determine number of activities based on pace
        if pace == 'relaxed':
            num_activities = 2
        elif pace == 'moderate':
            num_activities = 3
        else:  # fast
            num_activities = 4
        
        # Get activities for the day
        daily_activities = self._select_daily_activities(
            activities, recommendations, num_activities, day_number
        )
        
        # Create time slots
        time_slots = self._create_time_slots(daily_activities, pace)
        
        # Add meals
        meals = self._plan_meals(preferences, date)
        
        return {
            'day': day_number,
            'date': date.strftime('%Y-%m-%d'),
            'activities': time_slots,
            'meals': meals,
            'transportation': self._plan_daily_transportation(daily_activities),
            'estimated_cost': self._calculate_daily_cost(time_slots, meals)
        }
    
    def _select_daily_activities(self, activities, recommendations, num_activities, day_number):
        """Select activities for the day based on preferences and recommendations"""
        selected_activities = []
        
        # Get recommendations for each activity category
        for activity_type in activities:
            if activity_type in recommendations:
                category_recommendations = recommendations[activity_type]
                if category_recommendations:
                    # Select activities based on day number (for variety)
                    selected = self._select_activities_for_category(
                        category_recommendations, day_number
                    )
                    selected_activities.extend(selected)
        
        # If not enough activities, add some generic ones
        while len(selected_activities) < num_activities:
            generic_activity = self._get_generic_activity(activities, day_number)
            if generic_activity not in selected_activities:
                selected_activities.append(generic_activity)
        
        return selected_activities[:num_activities]
    
    def _select_activities_for_category(self, recommendations, day_number):
        """Select activities from a specific category"""
        if not recommendations:
            return []
        
        # Rotate through recommendations based on day number
        index = (day_number - 1) % len(recommendations)
        return [recommendations[index]]
    
    def _get_generic_activity(self, activities, day_number):
        """Get a generic activity when recommendations are not available"""
        activity_templates = {
            'culture': [
                'Visit local museum',
                'Explore historical district',
                'Tour art gallery',
                'Visit cultural center'
            ],
            'adventure': [
                'Go hiking in nature',
                'Try water sports',
                'Explore outdoor trails',
                'Visit adventure park'
            ],
            'relaxation': [
                'Visit local park',
                'Relax at spa',
                'Walk along beach',
                'Visit botanical gardens'
            ],
            'food': [
                'Try local restaurant',
                'Visit food market',
                'Take cooking class',
                'Go wine tasting'
            ],
            'shopping': [
                'Visit local market',
                'Explore shopping district',
                'Visit craft stores',
                'Go souvenir shopping'
            ],
            'nature': [
                'Visit national park',
                'Explore wildlife reserve',
                'Walk in botanical gardens',
                'Visit nature center'
            ]
        }
        
        if activities:
            activity_type = activities[day_number % len(activities)]
            templates = activity_templates.get(activity_type, ['Explore the area'])
            return templates[day_number % len(templates)]
        
        return 'Explore the area'
    
    def _create_time_slots(self, activities, pace):
        """Create time slots for activities"""
        time_slots = []
        
        if pace == 'relaxed':
            start_time = 10  # 10 AM
            duration = 2  # 2 hours per activity
        elif pace == 'moderate':
            start_time = 9  # 9 AM
            duration = 1.5  # 1.5 hours per activity
        else:  # fast
            start_time = 8  # 8 AM
            duration = 1  # 1 hour per activity
        
        for i, activity in enumerate(activities):
            slot = {
                'time': f"{start_time + i * 2:02d}:00",
                'duration': f"{duration:.1f}h",
                'activity': activity,
                'type': self._categorize_activity(activity),
                'estimated_cost': self._estimate_activity_cost(activity)
            }
            time_slots.append(slot)
        
        return time_slots
    
    def _categorize_activity(self, activity):
        """Categorize an activity based on its description"""
        activity_lower = activity.lower()
        
        if any(word in activity_lower for word in ['museum', 'gallery', 'historical', 'cultural']):
            return 'culture'
        elif any(word in activity_lower for word in ['hiking', 'adventure', 'sports', 'park']):
            return 'adventure'
        elif any(word in activity_lower for word in ['spa', 'beach', 'relax', 'park']):
            return 'relaxation'
        elif any(word in activity_lower for word in ['restaurant', 'food', 'cooking', 'wine']):
            return 'food'
        elif any(word in activity_lower for word in ['market', 'shopping', 'store', 'boutique']):
            return 'shopping'
        else:
            return 'exploration'
    
    def _estimate_activity_cost(self, activity):
        """Estimate the cost of an activity"""
        activity_lower = activity.lower()
        
        if any(word in activity_lower for word in ['museum', 'gallery', 'park']):
            return random.uniform(10, 25)
        elif any(word in activity_lower for word in ['restaurant', 'food', 'cooking']):
            return random.uniform(30, 80)
        elif any(word in activity_lower for word in ['spa', 'adventure']):
            return random.uniform(50, 150)
        elif any(word in activity_lower for word in ['shopping', 'market']):
            return random.uniform(20, 100)
        else:
            return random.uniform(15, 50)
    
    def _plan_meals(self, preferences, date):
        """Plan meals for the day"""
        dining_preference = preferences.get('dining_preference', 'mixed')
        
        meals = {
            'breakfast': {
                'time': '08:00',
                'type': 'breakfast',
                'suggestion': self._get_meal_suggestion('breakfast', dining_preference),
                'estimated_cost': random.uniform(15, 30)
            },
            'lunch': {
                'time': '13:00',
                'type': 'lunch',
                'suggestion': self._get_meal_suggestion('lunch', dining_preference),
                'estimated_cost': random.uniform(20, 50)
            },
            'dinner': {
                'time': '19:00',
                'type': 'dinner',
                'suggestion': self._get_meal_suggestion('dinner', dining_preference),
                'estimated_cost': random.uniform(30, 80)
            }
        }
        
        return meals
    
    def _get_meal_suggestion(self, meal_type, dining_preference):
        """Get meal suggestions based on dining preference"""
        suggestions = {
            'breakfast': {
                'fine_dining': 'Upscale breakfast at hotel restaurant',
                'casual': 'Local café or breakfast spot',
                'street_food': 'Street food breakfast market',
                'local_cuisine': 'Traditional local breakfast',
                'mixed': 'Hotel breakfast or local café'
            },
            'lunch': {
                'fine_dining': 'Upscale restaurant lunch',
                'casual': 'Casual dining restaurant',
                'street_food': 'Street food lunch',
                'local_cuisine': 'Traditional local restaurant',
                'mixed': 'Mix of casual and local dining'
            },
            'dinner': {
                'fine_dining': 'Fine dining restaurant',
                'casual': 'Casual dinner restaurant',
                'street_food': 'Evening street food',
                'local_cuisine': 'Traditional local dinner',
                'mixed': 'Mix of dining experiences'
            }
        }
        
        return suggestions[meal_type].get(dining_preference, 'Local dining option')
    
    def _plan_transportation(self, flights, hotels, duration):
        """Plan overall transportation for the trip"""
        return {
            'arrival': {
                'type': 'flight',
                'details': flights.get('flight_options', [{}])[0] if flights.get('flight_options') else {}
            },
            'departure': {
                'type': 'flight',
                'details': flights.get('flight_options', [{}])[0] if flights.get('flight_options') else {}
            },
            'local_transportation': 'Mix of public transport and walking',
            'estimated_daily_cost': random.uniform(10, 30)
        }
    
    def _plan_daily_transportation(self, activities):
        """Plan transportation for daily activities"""
        return {
            'primary_mode': 'Walking and public transport',
            'estimated_cost': random.uniform(5, 20),
            'notes': 'Most attractions are within walking distance or accessible by public transport'
        }
    
    def _calculate_daily_cost(self, activities, meals):
        """Calculate total cost for a day"""
        activity_cost = sum(activity.get('estimated_cost', 0) for activity in activities)
        meal_cost = sum(meal.get('estimated_cost', 0) for meal in meals.values())
        transportation_cost = random.uniform(5, 20)
        
        return {
            'activities': activity_cost,
            'meals': meal_cost,
            'transportation': transportation_cost,
            'total': activity_cost + meal_cost + transportation_cost
        }
    
    def _calculate_budget_breakdown(self, daily_plans):
        """Calculate budget breakdown for the entire trip"""
        total_activities = sum(day['estimated_cost']['activities'] for day in daily_plans)
        total_meals = sum(day['estimated_cost']['meals'] for day in daily_plans)
        total_transportation = sum(day['estimated_cost']['transportation'] for day in daily_plans)
        
        return {
            'activities': total_activities,
            'meals': total_meals,
            'transportation': total_transportation,
            'total': total_activities + total_meals + total_transportation
        } 