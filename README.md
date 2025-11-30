# SmartTripPlanner

A multi-agent system (MAS) travel management platform that automates itinerary planning, price tracking, and personalized trip recommendations using intelligent agents.

## Overview

SmartTripPlanner leverages a distributed agent architecture to coordinate complex travel planning tasks. The system features a modern React frontend and a Python-based backend with Flask and FastAPI, orchestrated through Docker containers.

## Key Features

- **Multi-Agent Architecture**: Intelligent task delegation across specialized agents
- **Dynamic Itinerary Planning**: Automated schedule generation based on user preferences
- **Real-Time Price Tracking**: Flight, hotel, and transportation price monitoring
- **Personalized Recommendations**: AI-driven attraction and activity suggestions
- **Interactive User Interface**: Modern, responsive web application for trip customization
- **Scalable Deployment**: Containerized architecture with Docker Compose

## Architecture

### Technology Stack

**Frontend:**
- React 18.2 with React Router
- Tailwind CSS for styling
- Axios for HTTP communication
- Modern UI components (React DatePicker, React Select, Recharts)

**Backend:**
- **Flask** (Port 5000): Primary API gateway for client requests
- **FastAPI** (Port 8000): High-performance agent-to-agent communication layer
- **Celery**: Asynchronous task queue for agent coordination
- **Redis**: Message broker and result backend for Celery

**Multi-Agent System:**
- `UserAgent`: Processes and validates user preferences
- `FlightAgent`: Searches and analyzes flight options via Amadeus API
- `HotelAgent`: Finds accommodation based on preferences
- `ItineraryAgent`: Creates daily schedules and activity plans
- `BudgetAgent`: Manages budget constraints and cost optimization
- `RecommendationAgent`: Provides personalized destination suggestions

**External Integrations:**
- Amadeus API for flight data (with mock data fallback)
- Google Maps API for places and geocoding
- Additional travel APIs can be integrated as needed

## Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-TravelPlanner
   ```

2. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Flask API: http://localhost:5000
   - FastAPI: http://localhost:8000
   - Redis: localhost:6379

### Local Development Setup

#### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment variables
export FLASK_ENV=development
export REDIS_URL=redis://localhost:6379
export CELERY_BROKER_URL=redis://localhost:6379
export CELERY_RESULT_BACKEND=redis://localhost:6379

# Start Redis (if not using Docker)
redis-server

# Start Celery worker (in one terminal)
celery -A app.celery_app worker --loglevel=info

# Start Flask application (in another terminal)
python app.py

# Start FastAPI service (in a third terminal)
uvicorn app.fastapi_app:app --reload --port 8000
```

#### Frontend Development

```bash
cd frontend
npm install
npm start
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Redis Configuration
REDIS_URL=redis://localhost:6379
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# External API Keys
AMADEUS_CLIENT_ID=your_amadeus_client_id
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000
```

### API Keys Setup

1. **Amadeus API** (for flight data):
   - Sign up at [Amadeus for Developers](https://developers.amadeus.com/)
   - Obtain your Client ID and Client Secret
   - Add credentials to `.env` file

2. **Google Maps API** (for places and geocoding):
   - Access [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Places API and Maps JavaScript API
   - Generate an API key
   - Add key to `.env` file

## Usage

### Example Use Case

**Request**: "Plan a 5-day trip to Rome under $1500 focused on history and cafes."

**Process Flow**:
1. **UserAgent** collects and processes preferences
2. **FlightAgent** searches for affordable flights
3. **HotelAgent** finds suitable accommodations
4. **RecommendationAgent** suggests historical sites and cafes
5. **ItineraryAgent** builds a daily schedule
6. **BudgetAgent** ensures total cost stays within $1500

### API Endpoints

#### Main Trip Planning
- `POST /api/plan-trip` - Initiate trip planning process (returns task_id)
- `GET /api/trip-status/{task_id}` - Check planning task status

#### Individual Agent Endpoints
- `POST /api/flights/search` - Search flights
- `POST /api/hotels/search` - Search hotels
- `POST /api/recommendations` - Get personalized recommendations
- `POST /api/budget/analyze` - Analyze budget constraints

#### FastAPI Agent Communication
- `POST /api/agents/coordinate` - Coordinate all agents for trip planning
- `GET /api/agents/session/{session_id}` - Get agent session status
- `POST /api/agents/message` - Send messages between agents

### API Testing Examples

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Trip Planning:**
```bash
curl -X POST http://localhost:5000/api/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Rome",
    "start_date": "2024-06-01",
    "end_date": "2024-06-05",
    "budget": 1500,
    "preferences": {
      "activities": ["culture", "food"],
      "accommodation_style": "moderate"
    }
  }'
```

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
│   │   │   ├── Header.js
│   │   │   ├── TripPlanner.js
│   │   │   ├── TripResults.js
│   │   │   └── Dashboard.js
│   │   ├── config/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── env.example
├── README.md
└── DEPLOYMENT.md
```

## Multi-Agent System

### Agent Responsibilities

1. **UserAgent**: Processes user preferences and requirements, validates input data
2. **FlightAgent**: Searches and analyzes flight options using Amadeus API
3. **HotelAgent**: Finds accommodation based on preferences and budget
4. **ItineraryAgent**: Creates daily schedules and activity plans
5. **BudgetAgent**: Manages budget constraints and cost optimization
6. **RecommendationAgent**: Provides personalized destination suggestions

### Agent Communication Flow

```
User Request
    ↓
UserAgent (process preferences)
    ↓
┌─────────────────────────────────┐
│  Parallel Agent Execution       │
├─────────────────────────────────┤
│  FlightAgent  →  HotelAgent     │
│       ↓              ↓          │
│  RecommendationAgent            │
│       ↓                         │
│  ItineraryAgent                 │
└─────────────────────────────────┘
    ↓
BudgetAgent (validate constraints)
    ↓
Final Trip Plan
```

## Deployment

### Quick Deploy (Recommended)

The easiest way to deploy is using **Railway** - it automatically detects Docker Compose and handles everything:

1. Sign up at [railway.app](https://railway.app)
2. Create new project → Deploy from GitHub
3. Add environment variables (see `DEPLOYMENT.md`)
4. Deploy (automatic)

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions** including Railway, Render, and DigitalOcean options.

### Local Docker Deployment

**Start services:**
```bash
docker-compose up --build -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop services:**
```bash
docker-compose down
```

**View specific service logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery
```

## Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

## Monitoring & Logging

- **Application Logs**: Monitor via Docker logs for each service
- **Agent Communication**: Track agent messages through FastAPI endpoints
- **Task Queue**: Monitor Celery task status and execution
- **Error Handling**: Check application logs for agent failures and API errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Review the API endpoint documentation
- Check the agent implementation details

## Future Enhancements

- [ ] Real-time price alerts and notifications
- [ ] Machine learning models for improved recommendations
- [ ] Mobile application development
- [ ] Integration with additional travel APIs
- [ ] Advanced budget optimization algorithms
- [ ] Social features and trip sharing capabilities
- [ ] User authentication and trip history persistence
- [ ] Database integration for data persistence
