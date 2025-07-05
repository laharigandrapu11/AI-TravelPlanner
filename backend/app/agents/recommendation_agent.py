from .base_agent import BaseAgent
import requests
import os
import random

class RecommendationAgent(BaseAgent):
    """Agent responsible for providing personalized recommendations"""
    
    def __init__(self):
        super().__init__("RecommendationAgent")
        self.google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        
    def process(self, data):
        """Main processing method"""
        return self.get_recommendations(data)
    
    def get_recommendations(self, recommendation_data):
        """Get personalized recommendations based on preferences"""
        self.log_info("Getting personalized recommendations")
        
        try:
            # Validate required fields
            required_fields = ['destination', 'preferences']
            self.validate_input(recommendation_data, required_fields)
            
            destination = recommendation_data['destination']
            preferences = recommendation_data['preferences']
            budget = recommendation_data.get('budget', 1000)
            
            # Get recommendations for each activity category
            recommendations = {}
            
            activities = preferences.get('activities', [])
            for activity_type in activities:
                category_recommendations = self._get_category_recommendations(
                    destination, activity_type, budget, preferences
                )
                recommendations[activity_type] = category_recommendations
            
            # Get general destination recommendations
            general_recommendations = self._get_general_recommendations(destination, preferences)
            
            # Get seasonal recommendations
            seasonal_recommendations = self._get_seasonal_recommendations(destination, preferences)
            
            result = {
                'destination': destination,
                'activity_recommendations': recommendations,
                'general_recommendations': general_recommendations,
                'seasonal_recommendations': seasonal_recommendations,
                'budget_considerations': self._get_budget_considerations(budget, preferences),
                'total_recommendations': sum(len(recs) for recs in recommendations.values())
            }
            
            self.log_info(f"Generated {result['total_recommendations']} recommendations for {destination}")
            return result
            
        except Exception as e:
            self.log_error(f"Error getting recommendations: {str(e)}")
            # Return mock recommendations for demo purposes
            return self._get_mock_recommendations(recommendation_data)
    
    def _get_category_recommendations(self, destination, activity_type, budget, preferences):
        """Get recommendations for a specific activity category"""
        recommendations = []
        
        if activity_type == 'culture':
            recommendations = self._get_culture_recommendations(destination, budget)
        elif activity_type == 'adventure':
            recommendations = self._get_adventure_recommendations(destination, budget)
        elif activity_type == 'relaxation':
            recommendations = self._get_relaxation_recommendations(destination, budget)
        elif activity_type == 'food':
            recommendations = self._get_food_recommendations(destination, budget, preferences)
        elif activity_type == 'shopping':
            recommendations = self._get_shopping_recommendations(destination, budget)
        elif activity_type == 'nature':
            recommendations = self._get_nature_recommendations(destination, budget)
        
        # Filter by budget and preferences
        filtered_recommendations = self._filter_recommendations(
            recommendations, budget, preferences
        )
        
        return filtered_recommendations[:5]  # Return top 5
    
    def _get_culture_recommendations(self, destination, budget):
        """Get cultural recommendations"""
        cultural_places = [
            f"Visit the {destination} Museum of Art",
            f"Explore the {destination} Historical District",
            f"Tour the {destination} Cathedral",
            f"Visit the {destination} Cultural Center",
            f"Explore the {destination} Archaeological Museum",
            f"Attend a performance at {destination} Opera House",
            f"Visit the {destination} National Gallery",
            f"Explore the {destination} Palace"
        ]
        
        recommendations = []
        for place in cultural_places:
            recommendations.append({
                'name': place,
                'type': 'culture',
                'estimated_cost': random.uniform(10, 30),
                'duration': f"{random.randint(1, 3)}h",
                'rating': round(random.uniform(4.0, 5.0), 1),
                'description': f"Immerse yourself in the rich cultural heritage of {destination}",
                'tips': f"Best visited in the morning to avoid crowds"
            })
        
        return recommendations
    
    def _get_adventure_recommendations(self, destination, budget):
        """Get adventure recommendations"""
        adventure_activities = [
            f"Go hiking in {destination} National Park",
            f"Try rock climbing at {destination} Cliffs",
            f"Go kayaking on {destination} River",
            f"Take a zip-lining tour in {destination}",
            f"Go mountain biking in {destination}",
            f"Try paragliding over {destination}",
            f"Go scuba diving near {destination}",
            f"Take a white-water rafting trip"
        ]
        
        recommendations = []
        for activity in adventure_activities:
            recommendations.append({
                'name': activity,
                'type': 'adventure',
                'estimated_cost': random.uniform(50, 150),
                'duration': f"{random.randint(2, 6)}h",
                'rating': round(random.uniform(4.0, 5.0), 1),
                'description': f"Experience the thrill of adventure in {destination}",
                'tips': f"Book in advance and check weather conditions"
            })
        
        return recommendations
    
    def _get_relaxation_recommendations(self, destination, budget):
        """Get relaxation recommendations"""
        relaxation_activities = [
            f"Visit {destination} Botanical Gardens",
            f"Relax at {destination} Spa Resort",
            f"Walk along {destination} Beach",
            f"Meditate at {destination} Zen Garden",
            f"Take a yoga class in {destination}",
            f"Visit {destination} Hot Springs",
            f"Enjoy a sunset cruise from {destination}",
            f"Take a peaceful walk in {destination} Park"
        ]
        
        recommendations = []
        for activity in relaxation_activities:
            recommendations.append({
                'name': activity,
                'type': 'relaxation',
                'estimated_cost': random.uniform(20, 100),
                'duration': f"{random.randint(1, 4)}h",
                'rating': round(random.uniform(4.0, 5.0), 1),
                'description': f"Find peace and tranquility in {destination}",
                'tips': f"Best enjoyed during quieter hours"
            })
        
        return recommendations
    
    def _get_food_recommendations(self, destination, budget, preferences):
        """Get food recommendations"""
        dining_preference = preferences.get('dining_preference', 'mixed')
        
        food_activities = [
            f"Take a food tour of {destination}",
            f"Visit {destination} Food Market",
            f"Try traditional {destination} cuisine",
            f"Take a cooking class in {destination}",
            f"Go wine tasting in {destination}",
            f"Visit {destination} Brewery",
            f"Try street food in {destination}",
            f"Have dinner at a rooftop restaurant in {destination}"
        ]
        
        recommendations = []
        for activity in food_activities:
            base_cost = random.uniform(30, 80)
            if dining_preference == 'fine_dining':
                base_cost *= 1.5
            elif dining_preference == 'street_food':
                base_cost *= 0.7
            
            recommendations.append({
                'name': activity,
                'type': 'food',
                'estimated_cost': base_cost,
                'duration': f"{random.randint(1, 3)}h",
                'rating': round(random.uniform(4.0, 5.0), 1),
                'description': f"Experience the culinary delights of {destination}",
                'tips': f"Reservations recommended for popular restaurants"
            })
        
        return recommendations
    
    def _get_shopping_recommendations(self, destination, budget):
        """Get shopping recommendations"""
        shopping_places = [
            f"Visit {destination} Central Market",
            f"Explore {destination} Shopping District",
            f"Shop at {destination} Craft Market",
            f"Visit {destination} Mall",
            f"Explore {destination} Boutique District",
            f"Shop for souvenirs in {destination}",
            f"Visit {destination} Artisan Market",
            f"Explore {destination} Fashion District"
        ]
        
        recommendations = []
        for place in shopping_places:
            recommendations.append({
                'name': place,
                'type': 'shopping',
                'estimated_cost': random.uniform(20, 100),
                'duration': f"{random.randint(1, 3)}h",
                'rating': round(random.uniform(3.5, 5.0), 1),
                'description': f"Discover unique shopping experiences in {destination}",
                'tips': f"Bargaining is common in local markets"
            })
        
        return recommendations
    
    def _get_nature_recommendations(self, destination, budget):
        """Get nature recommendations"""
        nature_activities = [
            f"Visit {destination} National Park",
            f"Explore {destination} Wildlife Reserve",
            f"Take a nature walk in {destination}",
            f"Visit {destination} Botanical Gardens",
            f"Go bird watching in {destination}",
            f"Take a scenic drive around {destination}",
            f"Visit {destination} Nature Center",
            f"Explore {destination} Forest"
        ]
        
        recommendations = []
        for activity in nature_activities:
            recommendations.append({
                'name': activity,
                'type': 'nature',
                'estimated_cost': random.uniform(10, 40),
                'duration': f"{random.randint(2, 5)}h",
                'rating': round(random.uniform(4.0, 5.0), 1),
                'description': f"Connect with nature in {destination}",
                'tips': f"Best visited early morning or late afternoon"
            })
        
        return recommendations
    
    def _filter_recommendations(self, recommendations, budget, preferences):
        """Filter recommendations based on budget and preferences"""
        filtered = []
        
        for rec in recommendations:
            # Check if within budget
            if rec['estimated_cost'] <= budget * 0.1:  # 10% of budget per activity
                # Check if matches preferences
                if self._matches_preferences(rec, preferences):
                    filtered.append(rec)
        
        # Sort by rating
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        return filtered
    
    def _matches_preferences(self, recommendation, preferences):
        """Check if recommendation matches user preferences"""
        # This is a simplified matching logic
        # In a real implementation, this would be more sophisticated
        return True
    
    def _get_general_recommendations(self, destination, preferences):
        """Get general destination recommendations"""
        return [
            {
                'name': f"Best time to visit {destination}",
                'description': f"Spring and fall offer the best weather and fewer crowds",
                'type': 'general'
            },
            {
                'name': f"Getting around {destination}",
                'description': f"Public transportation is efficient and affordable",
                'type': 'general'
            },
            {
                'name': f"Local customs in {destination}",
                'description': f"Learn a few basic phrases in the local language",
                'type': 'general'
            }
        ]
    
    def _get_seasonal_recommendations(self, destination, preferences):
        """Get seasonal recommendations"""
        return [
            {
                'name': "Seasonal activities",
                'description': f"Check local events and festivals during your visit to {destination}",
                'type': 'seasonal'
            }
        ]
    
    def _get_budget_considerations(self, budget, preferences):
        """Get budget-related recommendations"""
        return [
            {
                'name': "Budget tips",
                'description': f"With a budget of ${budget}, consider mixing free and paid activities",
                'type': 'budget'
            }
        ]
    
    def _get_mock_recommendations(self, recommendation_data):
        """Generate mock recommendations for demo purposes"""
        destination = recommendation_data['destination']
        preferences = recommendation_data.get('preferences', {})
        budget = recommendation_data.get('budget', 1000)
        
        activities = preferences.get('activities', ['culture', 'food'])
        
        recommendations = {}
        for activity in activities:
            recommendations[activity] = [
                {
                    'name': f"Sample {activity} activity in {destination}",
                    'type': activity,
                    'estimated_cost': random.uniform(20, 80),
                    'duration': f"{random.randint(1, 3)}h",
                    'rating': round(random.uniform(4.0, 5.0), 1),
                    'description': f"Experience {activity} in {destination}",
                    'tips': f"Best visited during your trip"
                }
            ]
        
        return {
            'destination': destination,
            'activity_recommendations': recommendations,
            'general_recommendations': self._get_general_recommendations(destination, preferences),
            'seasonal_recommendations': self._get_seasonal_recommendations(destination, preferences),
            'budget_considerations': self._get_budget_considerations(budget, preferences),
            'total_recommendations': len(activities)
        } 