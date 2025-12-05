#!/bin/bash

echo "🚀 Starting PolicySwarm..."
echo "========================="
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama not running. Starting Ollama serve in background..."
    ollama serve &> /dev/null &
    sleep 2
fi

echo "Starting Backend (FastAPI)..."
cd backend
source virtualpyenv/bin/activate
python main.py &> ../backend.log &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) - Log: backend.log"

cd ..

echo "Starting Frontend (Next.js)..."
cd frontend
npm run dev &> ../frontend.log &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) - Log: frontend.log"

cd ..

echo ""
echo "🎉 PolicySwarm is running!"
echo ""
echo "📍 Frontend: http://localhost:3001"
echo "📍 Backend API: http://localhost:8000"
echo ""
echo "💡 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "📋 Logs:"
echo "   Backend: tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
