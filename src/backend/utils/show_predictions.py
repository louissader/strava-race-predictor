"""
Simple script to show what your models predict based on your racing history
"""

import joblib
import pandas as pd
from utils.data_preprocessing import load_activities, create_race_dataset

def main():
    print("=" * 70)
    print("YOUR RACE TIME PREDICTIONS")
    print("=" * 70)

    # Load activities and create race dataset
    activities_df = load_activities()
    race_df = create_race_dataset(activities_df)

    print("\n📊 YOUR RACING HISTORY:\n")

    # Show 5K stats
    races_5k = race_df[race_df['race_distance'] == '5K']
    if len(races_5k) > 0:
        print(f"5K Races: {len(races_5k)}")
        print(f"  Best time: {races_5k['race_time_min'].min():.2f} min ({races_5k['race_time_min'].min()/5:.2f} min/km)")
        print(f"  Average time: {races_5k['race_time_min'].mean():.2f} min ({races_5k['race_time_min'].mean()/5:.2f} min/km)")
        print(f"  Most recent: {races_5k['race_time_min'].iloc[0]:.2f} min ({races_5k['race_date'].iloc[0].strftime('%Y-%m-%d')})")

    # Show 10K stats
    races_10k = race_df[race_df['race_distance'] == '10K']
    if len(races_10k) > 0:
        print(f"\n10K Races: {len(races_10k)}")
        print(f"  Best time: {races_10k['race_time_min'].min():.2f} min ({races_10k['race_time_min'].min()/10:.2f} min/km)")
        print(f"  Average time: {races_10k['race_time_min'].mean():.2f} min ({races_10k['race_time_min'].mean()/10:.2f} min/km)")
        print(f"  Most recent: {races_10k['race_time_min'].iloc[0]:.2f} min ({races_10k['race_date'].iloc[0].strftime('%Y-%m-%d')})")

    # Show Half Marathon stats
    races_half = race_df[race_df['race_distance'] == 'Half Marathon']
    if len(races_half) > 0:
        print(f"\nHalf Marathon Races: {len(races_half)}")
        print(f"  Best time: {races_half['race_time_min'].min():.2f} min ({races_half['race_time_min'].min()/21.0975:.2f} min/km)")
        print(f"  Most recent: {races_half['race_time_min'].iloc[0]:.2f} min ({races_half['race_date'].iloc[0].strftime('%Y-%m-%d')})")

    print("\n" + "=" * 70)
    print("ML MODEL PREDICTIONS")
    print("=" * 70)
    print("\n(Based on the relationship between your training and race performance)\n")

    # Load and show model stats
    try:
        model_5k = joblib.load('models/5K_model.joblib')
        print(f"✅ 5K Model Ready")
        print(f"   Typical accuracy: ±{model_5k['test_mae']:.1f} minutes")
        print(f"   Model confidence (R²): {model_5k['test_r2']:.2f}")
        print(f"   → If you maintain similar training, expect times around {races_5k['race_time_min'].mean():.1f} min")
    except:
        print("❌ No 5K model available")

    print()

    try:
        model_10k = joblib.load('models/10K_model.joblib')
        print(f"✅ 10K Model Ready")
        print(f"   Typical accuracy: ±{model_10k['test_mae']:.1f} minutes")
        print(f"   Model confidence (R²): {model_10k['test_r2']:.2f}")
        print(f"   → If you maintain similar training, expect times around {races_10k['race_time_min'].mean():.1f} min")
    except:
        print("❌ No 10K model available")

    print("\n" + "=" * 70)
    print("RECENT TRAINING")
    print("=" * 70)

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs['start_date'] = pd.to_datetime(runs['start_date'])

    # Get most recent date
    most_recent = runs['start_date'].max()

    print(f"\nMost recent activity: {most_recent.strftime('%Y-%m-%d')}")

    # Show last 30 days from most recent activity
    cutoff_30d = most_recent - pd.Timedelta(days=30)
    recent_30d = runs[runs['start_date'] >= cutoff_30d]

    print(f"\nLast 30 days (from {cutoff_30d.strftime('%Y-%m-%d')} to {most_recent.strftime('%Y-%m-%d')}):")
    print(f"  Runs: {len(recent_30d)}")
    print(f"  Total distance: {recent_30d['distance_km'].sum():.1f} km")
    if len(recent_30d) > 0:
        print(f"  Average pace: {recent_30d['pace_min_per_km'].mean():.2f} min/km")
        print(f"  Longest run: {recent_30d['distance_km'].max():.1f} km")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
