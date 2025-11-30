from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
from datetime import datetime
import logging

from app.agents.user_agent import UserAgent
from app.agents.flight_agent import FlightAgent
from app.agents.hotel_agent import HotelAgent
from app.agents.itinerary_agent import ItineraryAgent
from app.agents.budget_agent import BudgetAgent
from app.agents.recommendation_agent import RecommendationAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SmartTripPlanner Agent Communication API",
    description="FastAPI service for multi-agent communication in SmartTripPlanner",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
user_agent = UserAgent()
flight_agent = FlightAgent()
hotel_agent = HotelAgent()
itinerary_agent = ItineraryAgent()
budget_agent = BudgetAgent()
recommendation_agent = RecommendationAgent()

# Pydantic models
class TripRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: Dict[str, Any]
    origin: Optional[str] = ""
    travelers: Optional[int] = 1

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    message_type: str
    data: Dict[str, Any]
    timestamp: Optional[str] = None

class AgentResponse(BaseModel):
    agent: str
    status: str
    data: Dict[str, Any]
    timestamp: str

# In-memory storage for agent communication (in production, use Redis or database)
agent_messages = []
trip_sessions = {}

@app.get("/")
async def root():
    return {"message": "SmartTripPlanner Agent Communication API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SmartTripPlanner Agent Communication API",
        "timestamp": datetime.now().isoformat(),
        "agents": [
            "UserAgent", "FlightAgent", "HotelAgent", 
            "ItineraryAgent", "BudgetAgent", "RecommendationAgent"
        ]
    }

@app.post("/api/agents/coordinate", response_model=Dict[str, Any])
async def coordinate_agents(trip_request: TripRequest, background_tasks: BackgroundTasks):
    """Coordinate all agents for trip planning"""
    try:
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize session
        trip_sessions[session_id] = {
            "status": "initializing",
            "trip_data": trip_request.dict(),
            "agent_results": {},
            "created_at": datetime.now().isoformat()
        }
        
        # Start coordination in background
        background_tasks.add_task(
            coordinate_trip_planning, session_id, trip_request.dict()
        )
        
        return {
            "session_id": session_id,
            "status": "coordinating",
            "message": "Trip planning coordination started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error coordinating agents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/session/{session_id}")
async def get_session_status(session_id: str):
    """Get the status of a trip planning session"""
    if session_id not in trip_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return trip_sessions[session_id]

@app.post("/api/agents/message")
async def send_agent_message(message: AgentMessage):
    """Send a message between agents"""
    try:
        message.timestamp = datetime.now().isoformat()
        agent_messages.append(message.dict())
        
        # Process message based on type
        response = await process_agent_message(message)
        
        return {
            "status": "sent",
            "message_id": len(agent_messages),
            "response": response
        }
        
    except Exception as e:
        logger.error(f"Error sending agent message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/messages")
async def get_agent_messages(limit: int = 50):
    """Get recent agent messages"""
    return {
        "messages": agent_messages[-limit:],
        "total": len(agent_messages)
    }

@app.post("/api/agents/flight/search")
async def agent_flight_search(search_data: Dict[str, Any]):
    """Flight agent search endpoint"""
    try:
        result = flight_agent.search_flights(search_data)
        return AgentResponse(
            agent="FlightAgent",
            status="completed",
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Flight agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/hotel/search")
async def agent_hotel_search(search_data: Dict[str, Any]):
    """Hotel agent search endpoint"""
    try:
        result = hotel_agent.search_hotels(search_data)
        return AgentResponse(
            agent="HotelAgent",
            status="completed",
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Hotel agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/recommendations")
async def agent_recommendations(request_data: Dict[str, Any]):
    """Recommendation agent endpoint"""
    try:
        result = recommendation_agent.get_recommendations(request_data)
        return AgentResponse(
            agent="RecommendationAgent",
            status="completed",
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Recommendation agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/itinerary/create")
async def agent_create_itinerary(itinerary_data: Dict[str, Any]):
    """Itinerary agent endpoint"""
    try:
        result = itinerary_agent.create_itinerary(itinerary_data)
        return AgentResponse(
            agent="ItineraryAgent",
            status="completed",
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Itinerary agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/budget/analyze")
async def agent_budget_analysis(budget_data: Dict[str, Any]):
    """Budget agent endpoint"""
    try:
        result = budget_agent.analyze_budget(budget_data)
        return AgentResponse(
            agent="BudgetAgent",
            status="completed",
            data=result,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Budget agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def coordinate_trip_planning(session_id: str, trip_data: Dict[str, Any]):
    """Coordinate the trip planning process between all agents"""
    try:
        logger.info(f"Starting trip planning coordination for session {session_id}")
        
        # Update session status
        trip_sessions[session_id]["status"] = "processing"
        
        # Step 1: Process user preferences
        logger.info("Step 1: Processing user preferences")
        user_preferences = user_agent.process_preferences(trip_data)
        trip_sessions[session_id]["agent_results"]["user_preferences"] = user_preferences
        
        # Step 2: Get recommendations
        logger.info("Step 2: Getting recommendations")
        recommendations = recommendation_agent.get_recommendations({
            'destination': trip_data['destination'],
            'preferences': trip_data['preferences'],
            'budget': trip_data['budget']
        })
        trip_sessions[session_id]["agent_results"]["recommendations"] = recommendations
        
        # Step 3: Search flights
        logger.info("Step 3: Searching flights")
        flights = flight_agent.search_flights({
            'origin': trip_data.get('origin', ''),
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'budget': trip_data['budget']
        })
        trip_sessions[session_id]["agent_results"]["flights"] = flights
        
        # Step 4: Search hotels
        logger.info("Step 4: Searching hotels")
        hotels = hotel_agent.search_hotels({
            'destination': trip_data['destination'],
            'check_in': trip_data['start_date'],
            'check_out': trip_data['end_date'],
            'budget': trip_data['budget'],
            'preferences': trip_data['preferences']
        })
        trip_sessions[session_id]["agent_results"]["hotels"] = hotels
        
        # Step 5: Create itinerary
        logger.info("Step 5: Creating itinerary")
        itinerary = itinerary_agent.create_itinerary({
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'preferences': trip_data['preferences'],
            'recommendations': recommendations,
            'flights': flights,
            'hotels': hotels
        })
        trip_sessions[session_id]["agent_results"]["itinerary"] = itinerary
        
        # Step 6: Analyze budget
        logger.info("Step 6: Analyzing budget")
        budget_analysis = budget_agent.analyze_budget({
            'flights': flights,
            'hotels': hotels,
            'itinerary': itinerary,
            'total_budget': trip_data['budget']
        })
        trip_sessions[session_id]["agent_results"]["budget_analysis"] = budget_analysis
        
        # Step 7: Finalize trip plan
        logger.info("Step 7: Finalizing trip plan")
        trip_plan = {
            'trip_id': session_id,
            'destination': trip_data['destination'],
            'start_date': trip_data['start_date'],
            'end_date': trip_data['end_date'],
            'flights': flights,
            'hotels': hotels,
            'itinerary': itinerary,
            'recommendations': recommendations,
            'budget_analysis': budget_analysis,
            'total_cost': budget_analysis.get('summary', {}).get('total_cost', 0),
            'budget_remaining': budget_analysis.get('summary', {}).get('remaining', 0),
            'status': 'completed',
            'completed_at': datetime.now().isoformat()
        }
        
        trip_sessions[session_id]["status"] = "completed"
        trip_sessions[session_id]["trip_plan"] = trip_plan
        
        logger.info(f"Trip planning completed for session {session_id}")
        
    except Exception as e:
        logger.error(f"Error in trip planning coordination: {str(e)}")
        trip_sessions[session_id]["status"] = "failed"
        trip_sessions[session_id]["error"] = str(e)

async def process_agent_message(message: AgentMessage):
    """Process messages between agents"""
    try:
        if message.message_type == "flight_search":
            return await agent_flight_search(message.data)
        elif message.message_type == "hotel_search":
            return await agent_hotel_search(message.data)
        elif message.message_type == "recommendations":
            return await agent_recommendations(message.data)
        elif message.message_type == "create_itinerary":
            return await agent_create_itinerary(message.data)
        elif message.message_type == "budget_analysis":
            return await agent_budget_analysis(message.data)
        else:
            return {"status": "unknown_message_type", "data": {}}
            
    except Exception as e:
        logger.error(f"Error processing agent message: {str(e)}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 