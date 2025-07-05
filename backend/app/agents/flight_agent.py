from .base_agent import BaseAgent
import requests
import os
from datetime import datetime, timedelta
import random

class FlightAgent(BaseAgent):
    """Agent responsible for searching and analyzing flight options"""
    
    def __init__(self):
        super().__init__("FlightAgent")
        self.amadeus_client_id = os.getenv('AMADEUS_CLIENT_ID')
        self.amadeus_client_secret = os.getenv('AMADEUS_CLIENT_SECRET')
        self.api_base_url = "https://test.api.amadeus.com/v1"
        
    def process(self, data):
        """Main processing method"""
        return self.search_flights(data)
    
    def search_flights(self, search_data):
        """Search for flights based on criteria"""
        self.log_info("Searching for flights")
        
        try:
            # Validate required fields
            required_fields = ['destination', 'start_date', 'end_date']
            self.validate_input(search_data, required_fields)
            
            # Extract search parameters
            origin = search_data.get('origin', 'NYC')  # Default origin
            destination = search_data['destination']
            start_date = search_data['start_date']
            end_date = search_data['end_date']
            budget = search_data.get('budget', 1000)
            travelers = search_data.get('travelers', 1)
            
            # Get access token for Amadeus API
            access_token = self._get_amadeus_token()
            
            # Search for outbound flights
            outbound_flights = self._search_flight_offers(
                access_token, origin, destination, start_date, budget
            )
            
            # Search for return flights
            return_flights = self._search_flight_offers(
                access_token, destination, origin, end_date, budget
            )
            
            # Combine and rank flights
            flight_options = self._combine_flight_options(
                outbound_flights, return_flights, budget, travelers
            )
            
            self.log_info(f"Found {len(flight_options)} flight options")
            return {
                'search_criteria': {
                    'origin': origin,
                    'destination': destination,
                    'start_date': start_date,
                    'end_date': end_date,
                    'budget': budget,
                    'travelers': travelers
                },
                'flight_options': flight_options,
                'total_options': len(flight_options)
            }
            
        except Exception as e:
            self.log_error(f"Error searching flights: {str(e)}")
            # Return mock data for demo purposes
            return self._get_mock_flights(search_data)
    
    def _get_amadeus_token(self):
        """Get access token from Amadeus API"""
        try:
            if not self.amadeus_client_id or not self.amadeus_client_secret:
                self.log_warning("Amadeus credentials not configured, using mock data")
                return None
            
            url = f"{self.api_base_url}/security/oauth2/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.amadeus_client_id,
                'client_secret': self.amadeus_client_secret
            }
            
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            
            return response.json()['access_token']
            
        except Exception as e:
            self.log_error(f"Error getting Amadeus token: {str(e)}")
            return None
    
    def _search_flight_offers(self, access_token, origin, destination, date, budget):
        """Search for flight offers using Amadeus API"""
        try:
            if not access_token:
                return []
            
            url = f"{self.api_base_url}/shopping/flight-offers"
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': date,
                'adults': 1,
                'max': 10,
                'currencyCode': 'USD'
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            return response.json().get('data', [])
            
        except Exception as e:
            self.log_error(f"Error searching flight offers: {str(e)}")
            return []
    
    def _combine_flight_options(self, outbound_flights, return_flights, budget, travelers):
        """Combine outbound and return flights into complete options"""
        options = []
        
        for outbound in outbound_flights[:5]:  # Limit to top 5 outbound
            for return_flight in return_flights[:5]:  # Limit to top 5 return
                total_price = (
                    float(outbound['price']['total']) + 
                    float(return_flight['price']['total'])
                ) * travelers
                
                if total_price <= budget:
                    option = {
                        'id': f"{outbound['id']}_{return_flight['id']}",
                        'outbound': self._format_flight(outbound),
                        'return': self._format_flight(return_flight),
                        'total_price': total_price,
                        'price_per_person': total_price / travelers,
                        'airlines': list(set([
                            outbound['validatingAirlineCodes'][0],
                            return_flight['validatingAirlineCodes'][0]
                        ]))
                    }
                    options.append(option)
        
        # Sort by price
        options.sort(key=lambda x: x['total_price'])
        return options[:10]  # Return top 10 options
    
    def _format_flight(self, flight_data):
        """Format flight data for consistent structure"""
        return {
            'id': flight_data['id'],
            'airline': flight_data['validatingAirlineCodes'][0],
            'departure': {
                'airport': flight_data['itineraries'][0]['segments'][0]['departure']['iataCode'],
                'time': flight_data['itineraries'][0]['segments'][0]['departure']['at']
            },
            'arrival': {
                'airport': flight_data['itineraries'][0]['segments'][-1]['arrival']['iataCode'],
                'time': flight_data['itineraries'][0]['segments'][-1]['arrival']['at']
            },
            'duration': flight_data['itineraries'][0]['duration'],
            'stops': len(flight_data['itineraries'][0]['segments']) - 1,
            'price': float(flight_data['price']['total'])
        }
    
    def _get_mock_flights(self, search_data):
        """Generate mock flight data for demo purposes"""
        destination = search_data['destination']
        start_date = search_data['start_date']
        end_date = search_data['end_date']
        budget = search_data.get('budget', 1000)
        travelers = search_data.get('travelers', 1)
        
        airlines = ['AA', 'UA', 'DL', 'BA', 'LH', 'AF']
        mock_options = []
        
        for i in range(5):
            outbound_price = random.uniform(200, 400)
            return_price = random.uniform(200, 400)
            total_price = (outbound_price + return_price) * travelers
            
            if total_price <= budget:
                option = {
                    'id': f"mock_flight_{i}",
                    'outbound': {
                        'id': f"outbound_{i}",
                        'airline': random.choice(airlines),
                        'departure': {
                            'airport': 'JFK',
                            'time': f"{start_date}T08:00:00"
                        },
                        'arrival': {
                            'airport': destination,
                            'time': f"{start_date}T10:30:00"
                        },
                        'duration': 'PT2H30M',
                        'stops': random.randint(0, 1),
                        'price': outbound_price
                    },
                    'return': {
                        'id': f"return_{i}",
                        'airline': random.choice(airlines),
                        'departure': {
                            'airport': destination,
                            'time': f"{end_date}T18:00:00"
                        },
                        'arrival': {
                            'airport': 'JFK',
                            'time': f"{end_date}T20:30:00"
                        },
                        'duration': 'PT2H30M',
                        'stops': random.randint(0, 1),
                        'price': return_price
                    },
                    'total_price': total_price,
                    'price_per_person': total_price / travelers,
                    'airlines': [random.choice(airlines), random.choice(airlines)]
                }
                mock_options.append(option)
        
        return {
            'search_criteria': {
                'origin': 'JFK',
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'budget': budget,
                'travelers': travelers
            },
            'flight_options': mock_options,
            'total_options': len(mock_options)
        } 