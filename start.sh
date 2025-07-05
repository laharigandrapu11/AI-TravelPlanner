#!/bin/bash

# SmartTripPlanner Startup Script

echo "🧳 Starting SmartTripPlanner - AI Travel Management System"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   Required keys: AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, GOOGLE_MAPS_API_KEY"
    read -p "Press Enter to continue or Ctrl+C to exit and configure .env first..."
fi

echo "🚀 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ SmartTripPlanner is starting up!"
echo ""
echo "🌐 Access the application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo "   FastAPI: http://localhost:8000"
echo ""
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
echo ""
echo "🎉 Happy traveling with AI!" 