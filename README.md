# 🧳 SmartTripPlanner – MAS-based Travel Management App

SmartTripPlanner is a multi-agent system (MAS) travel management platform that automates itinerary planning, price tracking, and personalized trip recommendations using intelligent agents. It features a React frontend, a Python/Flask + FastAPI backend, and is deployed with Docker and AWS ECS.

---

## 🚀 Key Features

- 🧠 Multi-agent backend for intelligent task delegation
- 📅 Dynamic itinerary planning based on user preferences
- ✈️ Real-time price tracking for flights, hotels, and local transport
- 🤖 Personalized attraction and activity suggestions
- 📲 Interactive UI for trip customization and comparison
- ☁️ Scalable deployment with Docker + AWS ECS

---

## 🧱 Architecture Overview

- **Frontend**: React.js + Tailwind CSS + Axios
- **Backend**:
  - **Flask** – API gateway for agent communication
  - **FastAPI** – Agent-to-agent communication
  - **Celery + Redis** – Task queue for agent tasks
- **Agents**:
  - `UserAgent`, `FlightAgent`, `HotelAgent`, `ItineraryAgent`, `BudgetAgent`, `RecommendationAgent`
- **External APIs**: Amadeus, Booking.com, Skyscanner, Google Maps
- **Deployment**: Docker + AWS ECS (Fargate)

---

## 🛠️ Installation & Setup

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-TravelPlanner
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - FastAPI: http://localhost:8000
   - Redis: localhost:6379

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export REDIS_URL=redis://localhost:6379

# Start Redis (if not using Docker)
redis-server

# Start Celery worker
celery -A app.celery_app worker --loglevel=info

# Start Flask app
python app.py

# Start FastAPI (in another terminal)
uvicorn app.fastapi_app:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

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
   - Get your Client ID and Client Secret

2. **Google Maps API** (for places and geocoding):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Places API and Maps JavaScript API
   - Create API key

---

## 📖 Usage

### Sample Use Case
"Plan a 5-day trip to Rome under $1500 focused on history and cafes."

🧳 **UserAgent** collects preferences

✈️ **FlightAgent** finds affordable flights

🏨 **HotelAgent** finds stays with breakfast

📅 **ItineraryAgent** builds daily plan

💸 **BudgetAgent** keeps everything within $1500

🎯 **RecommendationAgent** suggests local food tours + museums

### API Endpoints

#### Main Trip Planning
- `POST /api/plan-trip` - Start trip planning process
- `GET /api/trip-status/{task_id}` - Check planning status

#### Individual Agent Endpoints
- `POST /api/flights/search` - Search flights
- `POST /api/hotels/search` - Search hotels
- `POST /api/recommendations` - Get recommendations
- `POST /api/budget/analyze` - Analyze budget

#### FastAPI Agent Communication
- `POST /api/agents/coordinate` - Coordinate all agents
- `GET /api/agents/session/{session_id}` - Get session status
- `POST /api/agents/message` - Send agent messages

---

## 🏗️ Project Structure

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
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── env.example
└── README.md
```

---

## 🤖 Multi-Agent System

### Agent Responsibilities

1. **UserAgent**: Processes user preferences and requirements
2. **FlightAgent**: Searches and analyzes flight options
3. **HotelAgent**: Finds accommodation based on preferences
4. **ItineraryAgent**: Creates daily schedules and activities
5. **BudgetAgent**: Manages budget constraints and optimization
6. **RecommendationAgent**: Provides personalized suggestions

### Agent Communication Flow

```
User Request → UserAgent → RecommendationAgent
                    ↓
FlightAgent ←→ HotelAgent ←→ ItineraryAgent
                    ↓
BudgetAgent ←→ Final Trip Plan
```

---

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### AWS ECS Deployment
1. Build and push Docker images to ECR
2. Create ECS cluster and task definitions
3. Deploy with Fargate for serverless scaling

---

## 🧪 Testing

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

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test trip planning
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

---

## 📊 Monitoring & Logging

- **Application Logs**: Check Docker logs for each service
- **Agent Communication**: Monitor FastAPI agent messages
- **Task Queue**: Monitor Celery task status
- **Performance**: Use AWS CloudWatch for production monitoring

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API endpoints

---

## 🔮 Future Enhancements

- [ ] Real-time price alerts
- [ ] Machine learning for better recommendations
- [ ] Mobile app development
- [ ] Integration with more travel APIs
- [ ] Advanced budget optimization
- [ ] Social features and trip sharing
