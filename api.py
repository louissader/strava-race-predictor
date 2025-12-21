"""
Flask REST API for Strava Race Time Predictor
Serves data to React frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
from data_preprocessing import load_activities, create_race_dataset, calculate_training_features
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global data
activities_df = None
race_df = None

def load_data():
    """Load activities and race data"""
    global activities_df, race_df
    try:
        activities_df = load_activities()
        race_df = create_race_dataset(activities_df)
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    stats = {
        'total_activities': int(len(activities_df)),
        'total_runs': int(len(runs)),
        'total_distance_km': round(float(runs['distance_km'].sum()), 1),
        'total_time_hours': round(float(runs['moving_time_min'].sum() / 60), 1),
        'avg_pace': round(float(runs['pace_min_per_km'].mean()), 2),
        'best_pace': round(float(runs['pace_min_per_km'].min()), 2),
        'longest_run_km': round(float(runs['distance_km'].max()), 1),
        'first_run_date': runs['start_date'].min().strftime('%Y-%m-%d'),
        'last_run_date': runs['start_date'].max().strftime('%Y-%m-%d'),
        'total_elevation_m': round(float(runs['total_elevation_gain'].sum()), 0),
    }

    return jsonify(stats)

@app.route('/api/impressive-activities')
def get_impressive_activities():
    """Get most impressive activities - longest runs, fastest paces, highest elevation"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    # Longest runs
    longest = runs.nlargest(5, 'distance_km')[['name', 'distance_km', 'start_date', 'moving_time_min', 'pace_min_per_km', 'total_elevation_gain']].to_dict('records')

    # Fastest paces (filter out unrealistic paces)
    fastest_pace = runs[runs['pace_min_per_km'] > 2.5].nsmallest(5, 'pace_min_per_km')[['name', 'distance_km', 'start_date', 'pace_min_per_km', 'moving_time_min']].to_dict('records')

    # Highest elevation gain
    highest_elevation = runs[runs['total_elevation_gain'] > 0].nlargest(5, 'total_elevation_gain')[['name', 'distance_km', 'start_date', 'total_elevation_gain', 'pace_min_per_km']].to_dict('records')

    # Most consistent (similar pace across long distance)
    long_runs = runs[runs['distance_km'] > 10]
    if len(long_runs) > 0:
        consistent = long_runs.nsmallest(5, 'pace_min_per_km')[['name', 'distance_km', 'start_date', 'pace_min_per_km', 'moving_time_min']].to_dict('records')
    else:
        consistent = []

    return jsonify({
        'longest_runs': longest,
        'fastest_paces': fastest_pace,
        'highest_elevation': highest_elevation,
        'most_consistent': consistent
    })

@app.route('/api/predictions')
def get_predictions():
    """Get current race time predictions"""
    if activities_df is None or race_df is None:
        load_data()

    predictions = {}
    distances = ['5K', '10K', 'Half Marathon', 'Marathon']

    for distance in distances:
        try:
            model_data = joblib.load(f'models/{distance.replace(" ", "_")}_model.joblib')
            races = race_df[race_df['race_distance'] == distance]

            if len(races) > 0:
                predictions[distance] = {
                    'num_races': int(len(races)),
                    'best_time_min': float(races['race_time_min'].min()),
                    'avg_time_min': float(races['race_time_min'].mean()),
                    'recent_time_min': float(races['race_time_min'].iloc[0]),
                    'model_accuracy_mae': float(model_data['test_mae']),
                    'model_r2': float(model_data['test_r2']),
                    'has_model': True
                }
            else:
                predictions[distance] = {'has_model': False, 'num_races': 0}
        except:
            predictions[distance] = {'has_model': False, 'num_races': 0}

    return jsonify(predictions)

@app.route('/api/race_history')
def get_race_history():
    """Get complete race history"""
    if race_df is None:
        load_data()

    races = race_df.copy()
    races['race_date_str'] = races['race_date'].dt.strftime('%Y-%m-%d')

    history = []
    for _, race in races.iterrows():
        history.append({
            'date': race['race_date_str'],
            'distance': race['race_distance'],
            'time_min': round(float(race['race_time_min']), 2),
            'pace': round(float(race['race_pace_min_per_km']), 2),
            'name': race['race_name'],
            'elevation': round(float(race['race_elevation_gain_m']), 0) if pd.notna(race['race_elevation_gain_m']) else 0
        })

    return jsonify(history)

@app.route('/api/timeline_predictions')
def get_timeline_predictions():
    """Get predictions at different points in time"""
    if activities_df is None or race_df is None:
        load_data()

    distance = request.args.get('distance', '5K')

    try:
        model_data = joblib.load(f'models/{distance.replace(" ", "_")}_model.joblib')
        model = model_data['model']
        scaler = model_data['scaler']
        feature_names = model_data['feature_names']
    except:
        return jsonify({'error': 'Model not found'}), 404

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs['start_date'] = pd.to_datetime(runs['start_date'])

    latest_date = runs['start_date'].max()
    earliest_date = latest_date - timedelta(days=730)

    timeline = []
    current_date = earliest_date

    while current_date <= latest_date:
        features = calculate_training_features(activities_df, current_date)
        feature_values = [features.get(fn, 0) or 0 for fn in feature_names]

        X = np.array(feature_values).reshape(1, -1)
        X_scaled = scaler.transform(X)
        predicted_time = float(model.predict(X_scaled)[0])

        timeline.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'predicted_time_min': round(predicted_time, 2),
            'weekly_distance': round(float(features.get('past_7d_total_distance_km', 0)), 1),
            'monthly_distance': round(float(features.get('past_30d_total_distance_km', 0)), 1)
        })

        current_date += timedelta(days=30)

    return jsonify(timeline)

@app.route('/api/training_trends')
def get_training_trends():
    """Get training trends over time"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs['start_date'] = pd.to_datetime(runs['start_date'])
    runs['month'] = runs['start_date'].dt.to_period('M').astype(str)

    monthly = runs.groupby('month').agg({
        'distance_km': 'sum',
        'moving_time_min': 'sum',
        'id': 'count',
        'pace_min_per_km': 'mean'
    }).reset_index()
    monthly.columns = ['month', 'distance_km', 'time_min', 'num_runs', 'avg_pace']

    return jsonify(monthly.to_dict(orient='records'))

@app.route('/api/pace_distribution')
def get_pace_distribution():
    """Get pace distribution data"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs = runs[(runs['pace_min_per_km'] > 0) & (runs['pace_min_per_km'] < 10)]

    pace_data = runs['pace_min_per_km'].values.tolist()

    return jsonify({
        'paces': pace_data,
        'mean': float(runs['pace_min_per_km'].mean()),
        'median': float(runs['pace_min_per_km'].median())
    })

@app.route('/api/weekly_patterns')
def get_weekly_patterns():
    """Get running patterns by day of week and hour"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs['start_date_local'] = pd.to_datetime(runs['start_date_local'])
    runs['day_of_week'] = runs['start_date_local'].dt.day_name()
    runs['hour'] = runs['start_date_local'].dt.hour
    runs['month'] = runs['start_date_local'].dt.month

    day_counts = runs['day_of_week'].value_counts().to_dict()
    hour_counts = runs['hour'].value_counts().sort_index().to_dict()
    month_counts = runs['month'].value_counts().sort_index().to_dict()

    return jsonify({
        'by_day': day_counts,
        'by_hour': {str(k): v for k, v in hour_counts.items()},
        'by_month': {str(k): v for k, v in month_counts.items()}
    })

@app.route('/api/heatmap_coordinates')
def get_heatmap_coordinates():
    """Get approximate coordinates for heatmap (simulated for demo)"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    # Since we don't have GPS data, create simulated heatmap based on run frequency
    # In real implementation, this would use actual GPS polylines from Strava API
    coordinates = []

    # Use run frequency to create density
    for idx, run in runs.head(50).iterrows():
        # Simulate coordinates (replace with actual GPS data in production)
        # This is just for demo - shows concept of heatmap
        base_lat = 41.8781  # Example: Providence, RI area
        base_lon = -71.4774

        for i in range(int(run['distance_km'])):
            coordinates.append([
                base_lat + (np.random.random() - 0.5) * 0.01,
                base_lon + (np.random.random() - 0.5) * 0.01
            ])

    return jsonify({
        'coordinates': coordinates,
        'center': [41.8781, -71.4774],
        'note': 'Simulated data - integrate Strava polyline API for actual routes'
    })

if __name__ == '__main__':
    print("=" * 70)
    print("  STRAVA PREDICTOR API SERVER")
    print("=" * 70)
    print("\nLoading data...")

    if load_data():
        print("✅ Data loaded!")
        print(f"   Activities: {len(activities_df)}")
        print(f"   Runs: {len(activities_df[activities_df['type'] == 'Run'])}")
        print("\n" + "=" * 70)
        print("  API Server running on:")
        print("  http://localhost:5001")
        print("=" * 70 + "\n")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to load data.")
