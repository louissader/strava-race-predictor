#!/bin/bash

echo "========================================================================"
echo "  🚀 STRAVA RACE PREDICTOR - REACT + FLASK"
echo "========================================================================"
echo ""

# Kill any existing processes on ports 5001 and 5173
echo "Cleaning up old processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null
sleep 2

# Start Flask API
echo "Starting Flask API on port 5001..."
cd "/Users/louissader/Strava Project"
python3 api.py > api.log 2>&1 &
API_PID=$!

sleep 3

# Start React dev server
echo "Starting React dev server on port 5173..."
cd "/Users/louissader/Strava Project/frontend"
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 3

echo ""
echo "========================================================================"
echo "  ✅ SERVERS RUNNING!"
echo "========================================================================"
echo ""
echo "  🌐 Frontend: http://localhost:5173"
echo "  🔌 API:      http://localhost:5001"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo "========================================================================"
echo ""

# Wait and cleanup on exit
trap "kill $API_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
