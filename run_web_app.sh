#!/bin/bash

echo "========================================================================"
echo "  STRAVA RACE TIME PREDICTOR - WEB APPLICATION"
echo "========================================================================"
echo ""

# Check if data exists
if [ ! -f "data/strava_activities.csv" ]; then
    echo "⚠️  No data found!"
    echo ""
    echo "Please fetch your Strava data first:"
    echo "  python3 fetch_strava_data_rest.py"
    echo ""
    exit 1
fi

# Check if models exist
if [ ! -d "models" ] || [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo "⚠️  No trained models found!"
    echo ""
    echo "Training models now..."
    python3 train_model.py
    echo ""
fi

echo "✅ Data and models ready!"
echo ""
echo "Starting web application..."
echo ""
echo "========================================================================"
echo "  🌐 Open your browser and go to:"
echo "     http://localhost:5000"
echo "========================================================================"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""

python3 app.py
