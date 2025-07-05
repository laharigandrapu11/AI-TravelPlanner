from .base_agent import BaseAgent
import requests
import os
from datetime import datetime, timedelta
import random

class HotelAgent(BaseAgent):
    """Agent responsible for searching and analyzing hotel options"""
    
    def __init__(self):
        super().__init__("HotelAgent")
        self.google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        
    def process(self, data):
        """Main processing method"""
        return self.search_hotels(data)
    
    def search_hotels(self, search_data):
        """Search for hotels based on criteria"""
        self.log_info("Searching for hotels")
        
        try:
            # Validate required fields
            required_fields = ['destination', 'check_in', 'check_out']
            self.validate_input(search_data, required_fields)
            
            # Extract search parameters
            destination = search_data['destination']
            check_in = search_data['check_in']
            check_out = search_data['check_out']
            budget = search_data.get('budget', 1000)
            preferences = search_data.get('preferences', {})
            travelers = search_data.get('travelers', 1)
            
            # Calculate duration
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
            duration = (check_out_date - check_in_date).days
            
            # Get hotel recommendations
            hotels = self._search_hotel_options(destination, budget, preferences, duration)
            
            # Filter and rank hotels
            filtered_hotels = self._filter_hotels(hotels, budget, preferences)
            
            self.log_info(f"Found {len(filtered_hotels)} hotel options")
            return {
                'search_criteria': {
                    'destination': destination,
                    'check_in': check_in,
                    'check_out': check_out,
                    'duration': duration,
                    'budget': budget,
                    'travelers': travelers
                },
                'hotel_options': filtered_hotels,
                'total_options': len(filtered_hotels)
            }
            
        except Exception as e:
            self.log_error(f"Error searching hotels: {str(e)}")
            # Return mock data for demo purposes
            return self._get_mock_hotels(search_data)
    
    def _search_hotel_options(self, destination, budget, preferences, duration):
        """Search for hotel options using Google Places API or mock data"""
        try:
            if self.google_maps_api_key:
                return self._search_google_places(destination, budget, preferences)
            else:
                self.log_warning("Google Maps API key not configured, using mock data")
                return self._get_mock_hotel_data(destination, budget, preferences, duration)
                
        except Exception as e:
            self.log_error(f"Error searching hotel options: {str(e)}")
            return self._get_mock_hotel_data(destination, budget, preferences, duration)
    
    def _search_google_places(self, destination, budget, preferences):
        """Search for hotels using Google Places API"""
        try:
            # Search for hotels in the destination
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'query': f'hotels in {destination}',
                'type': 'lodging',
                'key': self.google_maps_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            places_data = response.json()
            hotels = []
            
            for place in places_data.get('results', []):
                hotel = {
                    'id': place['place_id'],
                    'name': place['name'],
                    'address': place.get('formatted_address', ''),
                    'rating': place.get('rating', 0),
                    'price_level': place.get('price_level', 2),
                    'types': place.get('types', []),
                    'location': place['geometry']['location'],
                    'photos': place.get('photos', [])
                }
                hotels.append(hotel)
            
            return hotels
            
        except Exception as e:
            self.log_error(f"Error searching Google Places: {str(e)}")
            return []
    
    def _filter_hotels(self, hotels, budget, preferences):
        """Filter and rank hotels based on preferences and budget"""
        filtered = []
        
        for hotel in hotels:
            # Calculate estimated price based on price level and duration
            price_level = hotel.get('price_level', 2)
            estimated_price = self._estimate_hotel_price(price_level, 1)  # per night
            
            # Check if within budget
            if estimated_price <= budget / 10:  # Assume 10% of budget for accommodation
                score = self._calculate_hotel_score(hotel, preferences)
                hotel['estimated_price'] = estimated_price
                hotel['score'] = score
                filtered.append(hotel)
        
        # Sort by score
        filtered.sort(key=lambda x: x['score'], reverse=True)
        return filtered[:10]  # Return top 10
    
    def _estimate_hotel_price(self, price_level, nights):
        """Estimate hotel price based on price level"""
        base_prices = {
            1: 50,   # Budget
            2: 100,  # Moderate
            3: 200,  # Expensive
            4: 400   # Very expensive
        }
        return base_prices.get(price_level, 100) * nights
    
    def _calculate_hotel_score(self, hotel, preferences):
        """Calculate hotel score based on preferences"""
        score = 0
        
        # Base score from rating
        score += hotel.get('rating', 0) * 10
        
        # Price level preference
        preferred_price = preferences.get('accommodation_style', 'moderate')
        price_level = hotel.get('price_level', 2)
        
        if preferred_price == 'budget' and price_level <= 2:
            score += 20
        elif preferred_price == 'luxury' and price_level >= 3:
            score += 20
        elif preferred_price == 'moderate' and price_level == 2:
            score += 20
        
        # Location preference (if available)
        if 'location' in hotel:
            score += 10
        
        return score
    
    def _get_mock_hotels(self, search_data):
        """Generate mock hotel data for demo purposes"""
        destination = search_data['destination']
        check_in = search_data['check_in']
        check_out = search_data['check_out']
        budget = search_data.get('budget', 1000)
        travelers = search_data.get('travelers', 1)
        
        # Calculate duration
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        duration = (check_out_date - check_in_date).days
        
        hotel_names = [
            f"Grand {destination} Hotel",
            f"{destination} Plaza Hotel",
            f"Comfort Inn {destination}",
            f"{destination} Boutique Hotel",
            f"Travelodge {destination}",
            f"{destination} Resort & Spa",
            f"Best Western {destination}",
            f"{destination} City Hotel"
        ]
        
        mock_hotels = []
        
        for i in range(8):
            price_level = random.randint(1, 4)
            price_per_night = self._estimate_hotel_price(price_level, 1)
            total_price = price_per_night * duration * travelers
            
            if total_price <= budget * 0.4:  # 40% of budget for accommodation
                hotel = {
                    'id': f"hotel_{i}",
                    'name': hotel_names[i],
                    'address': f"{random.randint(100, 999)} Main St, {destination}",
                    'rating': round(random.uniform(3.5, 5.0), 1),
                    'price_level': price_level,
                    'estimated_price': total_price,
                    'price_per_night': price_per_night,
                    'amenities': random.sample([
                        'WiFi', 'Pool', 'Gym', 'Restaurant', 'Spa', 'Parking'
                    ], random.randint(2, 4)),
                    'location': {
                        'lat': random.uniform(40.0, 45.0),
                        'lng': random.uniform(-75.0, -70.0)
                    },
                    'score': random.uniform(70, 95)
                }
                mock_hotels.append(hotel)
        
        # Sort by score
        mock_hotels.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'search_criteria': {
                'destination': destination,
                'check_in': check_in,
                'check_out': check_out,
                'duration': duration,
                'budget': budget,
                'travelers': travelers
            },
            'hotel_options': mock_hotels,
            'total_options': len(mock_hotels)
        }
    
    def _get_mock_hotel_data(self, destination, budget, preferences, duration):
        """Generate mock hotel data for internal use"""
        return []  # This will be handled by _get_mock_hotels 