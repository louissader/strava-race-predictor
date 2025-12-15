"""
Predict race times using trained models
"""

import os
import argparse
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from data_preprocessing import load_activities, calculate_training_features

def load_model(distance):
    """Load trained model for a specific distance"""
    model_path = f'models/{distance.replace(" ", "_")}_model.joblib'

    if not os.path.exists(model_path):
        print(f"Model not found for {distance} at {model_path}")
        print(f"Available models:")
        if os.path.exists('models'):
            for file in os.listdir('models'):
                if file.endswith('.joblib'):
                    print(f"  - {file}")
        return None

    model_data = joblib.load(model_path)
    return model_data

def predict_race_time(distance, activities_df=None, prediction_date=None):
    """
    Predict race time for a given distance

    Args:
        distance: Race distance (5K, 10K, Half Marathon, Marathon)
        activities_df: DataFrame of activities (optional, will load if not provided)
        prediction_date: Date to predict for (optional, defaults to today)

    Returns:
        Predicted race time in minutes
    """
    # Load model
    model_data = load_model(distance)
    if model_data is None:
        return None

    model = model_data['model']
    scaler = model_data['scaler']
    feature_names = model_data['feature_names']

    # Load activities if not provided
    if activities_df is None:
        activities_df = load_activities()

    # Use today's date if not specified (or last activity date if it's more recent)
    if prediction_date is None:
        import pytz
        prediction_date = datetime.now(pytz.UTC)
        # If we have activities, use the latest activity date + 1 day
        if activities_df is not None and len(activities_df) > 0:
            latest_activity = pd.to_datetime(activities_df['start_date']).max()
            if latest_activity > prediction_date:
                prediction_date = latest_activity + pd.Timedelta(days=1)

    # Calculate training features for the prediction date
    training_features = calculate_training_features(activities_df, prediction_date)

    # Create feature vector in the correct order
    feature_values = []
    for feature_name in feature_names:
        value = training_features.get(feature_name)
        if value is None or pd.isna(value):
            # Use median or 0 as fallback
            value = 0
        feature_values.append(value)

    X = np.array(feature_values).reshape(1, -1)

    # Scale features
    X_scaled = scaler.transform(X)

    # Make prediction
    predicted_time_min = model.predict(X_scaled)[0]

    # Convert to hours:minutes:seconds format
    hours = int(predicted_time_min // 60)
    minutes = int(predicted_time_min % 60)
    seconds = int((predicted_time_min % 1) * 60)

    return {
        'distance': distance,
        'predicted_time_min': predicted_time_min,
        'predicted_time_formatted': f"{hours:02d}:{minutes:02d}:{seconds:02d}",
        'test_mae': model_data.get('test_mae', None),
        'test_r2': model_data.get('test_r2', None),
        'features': training_features
    }

def predict_all_distances(activities_df=None):
    """Predict race times for all available distances"""
    distances = ['5K', '10K', 'Half Marathon', 'Marathon']

    if activities_df is None:
        activities_df = load_activities()

    predictions = {}

    for distance in distances:
        result = predict_race_time(distance, activities_df)
        if result:
            predictions[distance] = result

    return predictions

def format_pace(time_min, distance_km):
    """Format pace in min/km"""
    pace = time_min / distance_km
    pace_min = int(pace)
    pace_sec = int((pace % 1) * 60)
    return f"{pace_min}:{pace_sec:02d}"

def print_prediction_report(predictions):
    """Print a formatted prediction report"""
    print("\n" + "=" * 70)
    print("RACE TIME PREDICTIONS")
    print("=" * 70)

    distance_km_map = {
        '5K': 5.0,
        '10K': 10.0,
        'Half Marathon': 21.0975,
        'Marathon': 42.195
    }

    for distance, result in predictions.items():
        print(f"\n{distance}:")
        print(f"  Predicted Time: {result['predicted_time_formatted']}")
        if distance in distance_km_map:
            pace = format_pace(result['predicted_time_min'], distance_km_map[distance])
            print(f"  Predicted Pace: {pace} min/km")
        if result['test_mae']:
            print(f"  Model Accuracy (MAE): ±{result['test_mae']:.2f} minutes")
        if result['test_r2']:
            print(f"  Model R² Score: {result['test_r2']:.3f}")

    print("\n" + "=" * 70)
    print("RECENT TRAINING SUMMARY")
    print("=" * 70)

    # Show training summary from any prediction (they all use the same features)
    if predictions:
        sample_result = next(iter(predictions.values()))
        features = sample_result['features']

        print("\nPast 7 days:")
        print(f"  Total distance: {features.get('past_7d_total_distance_km', 0):.1f} km")
        print(f"  Number of runs: {features.get('past_7d_num_runs', 0):.0f}")
        if features.get('past_7d_avg_pace'):
            print(f"  Average pace: {features['past_7d_avg_pace']:.2f} min/km")

        print("\nPast 30 days:")
        print(f"  Total distance: {features.get('past_30d_total_distance_km', 0):.1f} km")
        print(f"  Number of runs: {features.get('past_30d_num_runs', 0):.0f}")
        if features.get('past_30d_avg_pace'):
            print(f"  Average pace: {features['past_30d_avg_pace']:.2f} min/km")
        print(f"  Longest run: {features.get('past_30d_longest_run_km', 0):.1f} km")

        print("\nPast 90 days:")
        print(f"  Total distance: {features.get('past_90d_total_distance_km', 0):.1f} km")
        print(f"  Number of runs: {features.get('past_90d_num_runs', 0):.0f}")
        if features.get('best_pace_90d'):
            print(f"  Best pace: {features['best_pace_90d']:.2f} min/km")

def main():
    """Main prediction function"""
    parser = argparse.ArgumentParser(description='Predict race times based on Strava training data')
    parser.add_argument('--distance', type=str, help='Race distance (5K, 10K, Half Marathon, Marathon)')
    parser.add_argument('--all', action='store_true', help='Predict all distances')
    args = parser.parse_args()

    print("Strava Race Time Predictor")
    print("=" * 70)

    # Load activities
    print("\nLoading activities...")
    activities_df = load_activities()

    if args.all or not args.distance:
        # Predict all distances
        predictions = predict_all_distances(activities_df)
        if predictions:
            print_prediction_report(predictions)
        else:
            print("\nNo trained models found. Please run train_model.py first.")
    else:
        # Predict specific distance
        result = predict_race_time(args.distance, activities_df)
        if result:
            print_prediction_report({args.distance: result})
        else:
            print(f"\nFailed to predict for {args.distance}")
            print("Available distances: 5K, 10K, Half Marathon, Marathon")

if __name__ == "__main__":
    main()
