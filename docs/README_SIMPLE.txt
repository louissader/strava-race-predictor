================================================================================
                    STRAVA RACE TIME PREDICTOR
                  The Easiest ML Project Ever!
================================================================================

🎯 WHAT THIS DOES:
   Predicts your race times (5K, 10K, Half, Marathon) using machine learning
   based on your Strava training data.

⚡ QUICKEST WAY TO USE IT:

   Method 1 (Interactive Menu):
   ./go.sh

   Method 2 (Direct Command):
   python3 show_predictions_simple.py

   Method 3 (Full Pipeline):
   python3 run_everything.py

================================================================================

📊 WHAT YOU GET:

   ✅ Race predictions based on your training
   ✅ Model accuracy scores (how confident the predictions are)
   ✅ Training analysis and visualizations
   ✅ Pace trends and patterns

================================================================================

🎓 YOUR CURRENT DATA:

   • 1,580 total activities
   • 1,369 runs (8,722 km)
   • 18 x 5K races
   • 28 x 10K races
   • 1 x Half Marathon

   Models Trained:
   ✅ 5K - Accuracy: ±1 min
   ✅ 10K - Accuracy: ±1.2 min

================================================================================

📁 FILES YOU'LL USE:

   START HERE:
   ./go.sh                         ← Interactive menu (EASIEST!)
   show_predictions_simple.py      ← Quick predictions

   FULL PIPELINE:
   run_everything.py               ← Analyzes + trains + predicts

   UPDATE DATA:
   fetch_strava_data_rest.py       ← Get latest from Strava

   INDIVIDUAL STEPS:
   analyze_training.py             ← Create charts only
   train_model.py                  ← Retrain models only

================================================================================

🔄 TYPICAL WORKFLOW:

   1. Run races, upload to Strava 🏃
   2. Periodically: python3 fetch_strava_data_rest.py
   3. See predictions: python3 show_predictions_simple.py

================================================================================

📚 DOCUMENTATION:

   Quick Start:      START_HERE.md (read this first!)
   Complete Guide:   README.md
   Setup Guide:      QUICKSTART.md
   Detailed Setup:   GETTING_STARTED.md

================================================================================

🆘 HELP:

   1. Install dependencies:
      pip install -r requirements.txt

   2. Having issues?
      Read START_HERE.md

   3. Need to reauthorize Strava?
      python3 reauthorize_strava.py

================================================================================

💡 PRO TIPS:

   • Run ./go.sh for an interactive menu
   • More races = better predictions (need 5+ per distance)
   • Update data monthly for best results
   • Check plots/ folder for beautiful charts

================================================================================

🎉 YOU'RE ALL SET!

   Just run: ./go.sh

   Or: python3 show_predictions_simple.py

================================================================================
