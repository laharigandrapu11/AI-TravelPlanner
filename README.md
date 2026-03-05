# SmartTripPlanner

A multi agent travel planning system that automates itinerary planning, flight and hotel search, and personalized trip recommendations. You give it a destination, dates, budget, and preferences. It spins up six specialized agents that work in parallel to build a full trip plan.

---

## What It Does

A user submits a trip request through the frontend. The system hands it off to a Celery task so the user gets an immediate response with a task ID instead of waiting. In the background, six agents coordinate to search flights, find hotels, generate recommendations, build a daily itinerary, and validate everything against the budget. The frontend polls for status and displays the result when it is ready.

---

## Architecture Decisions

### Why Two Backend Frameworks: Flask and FastAPI

This is the question that comes up most when people look at the code. Flask runs on port 5000 and FastAPI runs on port 8000. They are doing different jobs.

Flask handles all incoming requests from the frontend. It is the stable, synchronous API layer that the React app talks to. It kicks off Celery tasks and returns task IDs. It is simple, predictable, and easy to reason about for standard request handling.

FastAPI handles all agent to agent communication. The agents run async operations, call external APIs in parallel, and use background tasks to coordinate without blocking. FastAPI is built for exactly this. Its native async support via Python asyncio means the flight agent and hotel agent can run simultaneously instead of sequentially. It also gives us automatic API docs via Swagger which made debugging inter agent communication much easier during development.

The trade off is that running two frameworks adds complexity. There are two servers to manage, two sets of routes, and two places to look when something breaks. In hindsight a single FastAPI application could have handled both concerns since FastAPI supports synchronous routes too. We kept the split because Flask was already established when we introduced the agent layer, and refactoring mid project carried more risk than the operational overhead.

### Why Six Agents Instead of One or Two

The first version had a single planning function that did everything in sequence. It worked but it had two problems. First, it was slow because every step waited for the previous one to finish. Second, any failure anywhere killed the whole plan.

We broke it into six agents based on single responsibility. Each agent owns one domain: user preferences, flights, hotels, recommendations, itinerary building, and budget validation. This means flight search and hotel search can run in parallel instead of one after the other. It also means if the recommendation agent fails, the rest of the plan can still complete with a degraded result rather than a total failure.

The six agent breakdown also maps cleanly to the external APIs. FlightAgent owns the Amadeus API. HotelAgent owns accommodation search. RecommendationAgent owns Google Maps. Having one agent per external dependency makes it easy to swap out or mock an API without touching anything else.

The trade off is coordination overhead. More agents means more message passing, more session state to track, and more places for things to go wrong silently. We use FastAPI background tasks and in memory session storage to track agent state, which works for the current scale but would need to move to Redis backed persistence for production.

### Why Celery for Task Queue

Trip planning involves multiple external API calls and can take several seconds. Making the user wait on a synchronous HTTP request was not acceptable. Celery lets us return a task ID immediately and process the work in the background.

Redis serves as the Celery broker and result backend. It stores task state so the frontend can poll for updates without the backend holding a connection open.

The trade off is that Celery adds operational complexity. You need the broker running, the worker running, and the main app running as three separate processes. For a simpler project this would be overkill. For a system making six external API calls per request it is the right call.

### Why Mock Data Fallback for Amadeus API

The Amadeus API has rate limits and requires credentials that not everyone running this locally will have. We built a mock data fallback that activates when the API credentials are missing or when the API returns an error. The mock data returns realistic looking flight and hotel results so the rest of the system can be developed and tested without a live API connection.

The trade off is that mock data does not reflect real prices, availability, or routing. Any UI built around the mock results will need retesting against the real API. We documented which responses are mock in the API response so the frontend can surface a warning to the user.

---

## How the Agents Work Together

```
User Request
    |
UserAgent (validate and process preferences)
    |
+----------------------------------+
| Parallel Execution               |
| FlightAgent    HotelAgent        |
|      |              |            |
|      RecommendationAgent         |
|              |                   |
|        ItineraryAgent            |
+----------------------------------+
    |
BudgetAgent (validate total cost against budget)
    |
Final Trip Plan returned to user
```

FlightAgent and HotelAgent run in parallel because they are independent. RecommendationAgent also runs in parallel since it does not depend on flight or hotel results. ItineraryAgent runs last because it needs all three to build the daily schedule. BudgetAgent always runs at the end to validate the complete plan.

---

## Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | React 18 + Tailwind | Component model suits the multi step trip form |
| Client API | Flask | Simple synchronous layer for frontend requests |
| Agent API | FastAPI | Native async for parallel agent execution |
| Task Queue | Celery | Non blocking background processing for trip planning |
| Message Broker | Redis | Celery broker and result backend |
| Flight Data | Amadeus API | Industry standard travel API with mock fallback |
| Places Data | Google Maps API | Geocoding and place recommendations |
| Containers | Docker Compose | Single command startup for all services |

---

## Project Structure

```
AI-TravelPlanner/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── base_agent.py
│   │   │   ├── user_agent.py
│   │   │   ├── flight_agent.py
│   │   │   ├── hotel_agent.py
│   │   │   ├── itinerary_agent.py
│   │   │   ├── budget_agent.py
│   │   │   └── recommendation_agent.py
│   │   ├── celery_app.py
│   │   ├── fastapi_app.py
│   │   └── tasks.py
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   └── config/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── env.example
├── DEPLOYMENT.md
└── README.md
```

---

## Running Locally

```bash
cp env.example .env
# Add your API keys to .env
# Required: AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, GOOGLE_MAPS_API_KEY
# The system falls back to mock data if keys are missing

docker compose up --build
```

Frontend runs at http://localhost:3000, Flask API at http://localhost:5000, FastAPI at http://localhost:8000.

Or use the startup script:

```bash
./start.sh
```

---

## API Endpoints

**Trip Planning (Flask)**

`POST /api/plan-trip` — submit a trip request, returns a task ID immediately

`GET /api/trip-status/{task_id}` — poll for planning status and results

**Agent Endpoints (FastAPI)**

`POST /api/agents/coordinate` — coordinate all agents for a trip

`GET /api/agents/session/{session_id}` — check agent session status

`POST /api/agents/message` — send messages between agents

Individual agent endpoints: `/api/agents/flight/search`, `/api/agents/hotel/search`, `/api/agents/recommendations`, `/api/agents/itinerary/create`, `/api/agents/budget/analyze`

---

## Testing

```bash
# Backend
cd backend
python -m pytest tests/

# Frontend
cd frontend
npm test
```

---

## Decision Summary

| Decision | What we picked | What we considered | Why |
|---|---|---|---|
| Client API | Flask | FastAPI only | Stable synchronous layer, already established |
| Agent API | FastAPI | Flask only | Native async for parallel agent execution |
| Task queue | Celery + Redis | Synchronous processing | Non blocking, user gets response immediately |
| Agent count | Six specialized agents | Fewer larger agents | Single responsibility, parallel execution, easier to test |
| External API fallback | Mock data | Hard failure | Development without API credentials, resilience |
| Containers | Docker Compose | Manual setup | Single command startup for all five services |
