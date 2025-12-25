"""
Data preprocessing and feature engineering for race time prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_activities(filepath='data/strava_activities.csv'):
    """Load activities from CSV file"""
    df = pd.read_csv(filepath)
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['start_date_local'] = pd.to_datetime(df['start_date_local'])
    return df

def identify_race_activities(df, min_distance_km=5.0):
    """
    Identify potential race activities based on heuristics:
    - High pace (faster than average)
    - Certain distances (5k, 10k, half marathon, marathon)
    - Achievement count or PR count
    """
    runs = df[df['type'] == 'Run'].copy()

    if len(runs) == 0:
        return pd.DataFrame()

    # Calculate percentiles for pace
    pace_threshold = runs['pace_min_per_km'].quantile(0.25)  # Top 25% fastest

    # Common race distances (km) with tolerance
    race_distances = {
        '5K': (4.5, 5.5),
        '10K': (9.5, 10.5),
        'Half Marathon': (20.5, 21.5),
        'Marathon': (41.5, 42.5),
    }

    def classify_race_distance(distance_km):
        """Classify distance into race categories"""
        for race_name, (min_dist, max_dist) in race_distances.items():
            if min_dist <= distance_km <= max_dist:
                return race_name
        return None

    runs['race_distance'] = runs['distance_km'].apply(classify_race_distance)
    runs['is_potential_race'] = (
        (runs['pace_min_per_km'] <= pace_threshold) &
        (runs['race_distance'].notna()) &
        (runs['distance_km'] >= min_distance_km)
    ) | (runs['pr_count'] > 0) | (runs['achievement_count'] > 2)

    # Filter to only potential races
    races = runs[runs['is_potential_race']].copy()

    return races

def calculate_training_features(df, target_date, lookback_days=[7, 14, 30, 60, 90]):
    """
    Calculate training features for a specific date

    Features include:
    - Total distance in past N days
    - Number of runs in past N days
    - Average pace in past N days
    - Longest run in past N days
    - Total elevation gain in past N days
    - Days since last run
    """
    runs = df[df['type'] == 'Run'].copy()
    features = {}

    for days in lookback_days:
        lookback_date = target_date - timedelta(days=days)
        recent_runs = runs[
            (runs['start_date'] < target_date) &
            (runs['start_date'] >= lookback_date)
        ]

        prefix = f'past_{days}d'

        features[f'{prefix}_total_distance_km'] = recent_runs['distance_km'].sum()
        features[f'{prefix}_num_runs'] = len(recent_runs)
        features[f'{prefix}_avg_pace'] = recent_runs['pace_min_per_km'].mean() if len(recent_runs) > 0 else None
        features[f'{prefix}_avg_distance_km'] = recent_runs['distance_km'].mean() if len(recent_runs) > 0 else None
        features[f'{prefix}_longest_run_km'] = recent_runs['distance_km'].max() if len(recent_runs) > 0 else 0
        features[f'{prefix}_total_elevation_m'] = recent_runs['total_elevation_gain'].sum()
        features[f'{prefix}_avg_heartrate'] = recent_runs['average_heartrate'].mean() if len(recent_runs) > 0 else None

    # Days since last run
    past_runs = runs[runs['start_date'] < target_date]
    if len(past_runs) > 0:
        last_run_date = past_runs['start_date'].max()
        features['days_since_last_run'] = (target_date - last_run_date).days
    else:
        features['days_since_last_run'] = None

    # Best pace in past 90 days
    past_90d = runs[
        (runs['start_date'] < target_date) &
        (runs['start_date'] >= target_date - timedelta(days=90))
    ]
    features['best_pace_90d'] = past_90d['pace_min_per_km'].min() if len(past_90d) > 0 else None

    return features

def create_race_dataset(activities_df):
    """
    Create a dataset for race time prediction

    Each row represents a race with features from prior training
    """
    races = identify_race_activities(activities_df)

    if len(races) == 0:
        print("No races identified in the dataset")
        return None

    print(f"Identified {len(races)} potential race activities")
    print(f"\nRace distance breakdown:")
    print(races['race_distance'].value_counts())

    # Create feature dataset
    race_features_list = []

    for idx, race in races.iterrows():
        race_date = race['start_date']

        # Calculate training features before this race
        training_features = calculate_training_features(activities_df, race_date)

        # Combine with race information
        race_data = {
            'race_id': race['id'],
            'race_date': race_date,
            'race_name': race['name'],
            'race_distance': race['race_distance'],
            'race_distance_km': race['distance_km'],
            'race_time_min': race['moving_time_min'],
            'race_pace_min_per_km': race['pace_min_per_km'],
            'race_elevation_gain_m': race['total_elevation_gain'],
            'race_avg_heartrate': race['average_heartrate'],
            **training_features
        }

        race_features_list.append(race_data)

    race_df = pd.DataFrame(race_features_list)

    # Sort by date
    race_df = race_df.sort_values('race_date')

    return race_df

def prepare_features_for_ml(race_df, target_distance='5K'):
    """
    Prepare features for machine learning

    Args:
        race_df: DataFrame with race features
        target_distance: Target race distance to predict (5K, 10K, Half Marathon, Marathon)

    Returns:
        X (features), y (target), feature_names
    """
    # Filter for target distance
    df = race_df[race_df['race_distance'] == target_distance].copy()

    if len(df) < 5:
        print(f"Warning: Only {len(df)} races found for {target_distance}. Need at least 5 for reliable predictions.")
        return None, None, None

    # Target variable: race time in minutes
    y = df['race_time_min'].values

    # Select features for training
    feature_cols = [col for col in df.columns if col.startswith('past_') or col.startswith('days_') or col.startswith('best_')]

    X = df[feature_cols].copy()

    # Handle missing values
    X = X.fillna(X.median())

    feature_names = X.columns.tolist()

    return X.values, y, feature_names

def main():
    """Test the preprocessing pipeline"""
    print("Data Preprocessing Test")
    print("=" * 50)

    # Load activities
    df = load_activities()
    print(f"\nLoaded {len(df)} activities")

    # Create race dataset
    race_df = create_race_dataset(df)

    if race_df is not None:
        # Save processed data
        race_df.to_csv('data/race_features.csv', index=False)
        print(f"\nRace features saved to data/race_features.csv")

        # Show sample
        print("\nSample of race features:")
        print(race_df.head())

        # Test ML preparation for different distances
        for distance in ['5K', '10K', 'Half Marathon', 'Marathon']:
            X, y, features = prepare_features_for_ml(race_df, distance)
            if X is not None:
                print(f"\n{distance}:")
                print(f"  Training samples: {len(X)}")
                print(f"  Features: {len(features)}")
                print(f"  Time range: {y.min():.2f} - {y.max():.2f} minutes")

if __name__ == "__main__":
    main()
