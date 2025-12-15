#!/usr/bin/env python3
"""
ONE-CLICK SCRIPT: Runs the entire Strava race prediction pipeline
This is the easiest way to use the project!
"""

import os
import sys
import subprocess

def print_header(text):
    """Print a nice header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def run_step(name, command, description):
    """Run a step in the pipeline"""
    print_header(f"STEP: {name}")
    print(f"📋 {description}")
    print(f"⚙️  Running: {command}\n")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"\n❌ {name} failed!")
        return False

    print(f"\n✅ {name} completed successfully!")
    return True

def main():
    """Run the complete pipeline"""
    print("\n" + "🏃" * 35)
    print_header("STRAVA RACE TIME PREDICTOR - ONE-CLICK RUN")
    print("This script will:")
    print("  1. ✅ Your data is already fetched (1580 activities)")
    print("  2. 📊 Analyze your training data")
    print("  3. 🤖 Train ML models for race prediction")
    print("  4. 🎯 Generate race time predictions")
    print("\n" + "🏃" * 35)

    input("\nPress ENTER to start...")

    # Change to project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Step 1: Data already fetched, skip
    print_header("STEP 1: FETCH DATA")
    print("✅ Data already fetched! Found 1580 activities (1369 runs)")
    print("   Skipping fetch step...")

    # Step 2: Analyze training data
    if not run_step(
        "ANALYZE TRAINING DATA",
        "python3 analyze_training.py",
        "Creating visualizations of your training patterns, pace progression, and more"
    ):
        return

    # Step 3: Train models
    if not run_step(
        "TRAIN ML MODELS",
        "python3 train_model.py",
        "Training machine learning models to predict your race times"
    ):
        return

    # Step 4: Show predictions (simple version)
    if not run_step(
        "SHOW YOUR PREDICTIONS",
        "python3 show_predictions_simple.py",
        "Showing your racing history and ML predictions"
    ):
        return

    # Success!
    print("\n" + "🎉" * 35)
    print_header("SUCCESS! PIPELINE COMPLETE")
    print("📊 Check the 'plots/' directory for visualizations")
    print("🤖 Check the 'models/' directory for trained models")
    print("\n💡 To update predictions in the future:")
    print("   1. Run: python3 fetch_strava_data_rest.py")
    print("   2. Run: python3 run_everything.py")
    print("\n🔍 To see predictions anytime:")
    print("   python3 predict_race_time.py --all")
    print("\n" + "🎉" * 35 + "\n")

if __name__ == "__main__":
    main()
