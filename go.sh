#!/bin/bash

# ONE-CLICK launcher for Strava Race Predictor
# This is the EASIEST way to use the project!

clear

echo "🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃"
echo ""
echo "           STRAVA RACE TIME PREDICTOR"
echo ""
echo "🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃🏃"
echo ""
echo "What would you like to do?"
echo ""
echo "  1) 🎯 Show my race predictions (FASTEST)"
echo "  2) 📊 Full analysis with charts"
echo "  3) 🔄 Update data from Strava"
echo "  4) 📈 Just create training visualizations"
echo "  5) 🤖 Retrain ML models"
echo "  6) ❓ Help / Documentation"
echo "  0) Exit"
echo ""
read -p "Enter choice [0-6]: " choice

case $choice in
    1)
        echo ""
        echo "========================================================================"
        echo "  SHOWING YOUR RACE PREDICTIONS"
        echo "========================================================================"
        echo ""
        python3 show_predictions_simple.py
        ;;
    2)
        echo ""
        echo "========================================================================"
        echo "  RUNNING FULL ANALYSIS"
        echo "========================================================================"
        echo ""
        python3 run_everything.py
        ;;
    3)
        echo ""
        echo "========================================================================"
        echo "  FETCHING LATEST DATA FROM STRAVA"
        echo "========================================================================"
        echo ""
        python3 fetch_strava_data_rest.py
        echo ""
        echo "✅ Data updated! Now run option 1 or 2 to see predictions."
        ;;
    4)
        echo ""
        echo "========================================================================"
        echo "  CREATING TRAINING VISUALIZATIONS"
        echo "========================================================================"
        echo ""
        python3 analyze_training.py
        echo ""
        echo "✅ Check the 'plots/' folder for your charts!"
        ;;
    5)
        echo ""
        echo "========================================================================"
        echo "  RETRAINING ML MODELS"
        echo "========================================================================"
        echo ""
        python3 train_model.py
        ;;
    6)
        echo ""
        cat START_HERE.md
        ;;
    0)
        echo ""
        echo "👋 Happy running!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run again and choose 0-6."
        exit 1
        ;;
esac

echo ""
echo "========================================================================"
echo "  DONE!"
echo "========================================================================"
echo ""
