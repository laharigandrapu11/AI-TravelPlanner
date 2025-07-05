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

- **Frontend**: React.js + Axios
- **Backend**:
  - **Flask** – API gateway for agent communication
  - **FastAPI** – Agent-to-agent communication
  - **Celery + Redis** – Task queue for agent tasks
- **Agents**:
  - `UserAgent`, `FlightAgent`, `HotelAgent`, `ItineraryAgent`, `BudgetAgent`, `RecommendationAgent`
- **External APIs**: Amadeus, Booking.com, Skyscanner, Google Maps
- **Deployment**: Docker + AWS ECS (Fargate)

---
## Sample Use case
“Plan a 5-day trip to Rome under $1500 focused on history and cafes.”

🧳 UserAgent collects preferences

✈️ FlightAgent finds affordable flights

🏨 HotelAgent finds stays with breakfast

📅 ItineraryAgent builds daily plan

💸 BudgetAgent keeps everything within $1500

🎯 RecommendationAgent suggests local food tours + museums
