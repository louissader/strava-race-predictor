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
import requests
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global data
activities_df = None
race_df = None
access_token_cache = None

def get_access_token():
    """Get fresh Strava access token using refresh token"""
    global access_token_cache

    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')

    if not all([refresh_token, client_id, client_secret]):
        print("Missing Strava credentials in .env file")
        return None

    # Request new access token
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.post(auth_url, data=payload)
        if response.status_code == 200:
            access_token_cache = response.json()['access_token']
            return access_token_cache
        else:
            print(f"Failed to get access token: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

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
    """Get overall statistics (in miles)"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    # Convert km to miles (1 km = 0.621371 miles)
    KM_TO_MILES = 0.621371

    # Calculate pace in min/mile from min/km
    avg_pace_min_per_mile = runs['pace_min_per_km'].mean() / KM_TO_MILES
    best_pace_min_per_mile = runs['pace_min_per_km'].min() / KM_TO_MILES

    stats = {
        'total_activities': int(len(activities_df)),
        'total_runs': int(len(runs)),
        'total_distance_mi': round(float(runs['distance_km'].sum() * KM_TO_MILES), 1),
        'total_time_hours': round(float(runs['moving_time_min'].sum() / 60), 1),
        'avg_pace': round(float(avg_pace_min_per_mile), 2),
        'best_pace': round(float(best_pace_min_per_mile), 2),
        'longest_run_mi': round(float(runs['distance_km'].max() * KM_TO_MILES), 1),
        'first_run_date': runs['start_date'].min().strftime('%Y-%m-%d'),
        'last_run_date': runs['start_date'].max().strftime('%Y-%m-%d'),
        'total_elevation_ft': round(float(runs['total_elevation_gain'].sum() * 3.28084), 0),  # meters to feet
    }

    return jsonify(stats)

@app.route('/api/impressive-activities')
def get_impressive_activities():
    """Get most impressive activities - longest runs, fastest paces, highest elevation (in miles)"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    KM_TO_MILES = 0.621371
    M_TO_FT = 3.28084

    # Longest runs
    longest_raw = runs.nlargest(5, 'distance_km')[['name', 'distance_km', 'start_date', 'moving_time_min', 'pace_min_per_km', 'total_elevation_gain']].to_dict('records')
    longest = [{**r, 'distance_mi': r['distance_km'] * KM_TO_MILES, 'pace_min_per_mi': r['pace_min_per_km'] / KM_TO_MILES, 'elevation_ft': r['total_elevation_gain'] * M_TO_FT} for r in longest_raw]

    # Fastest paces (filter out unrealistic paces)
    fastest_raw = runs[runs['pace_min_per_km'] > 2.5].nsmallest(5, 'pace_min_per_km')[['name', 'distance_km', 'start_date', 'pace_min_per_km', 'moving_time_min']].to_dict('records')
    fastest_pace = [{**r, 'distance_mi': r['distance_km'] * KM_TO_MILES, 'pace_min_per_mi': r['pace_min_per_km'] / KM_TO_MILES} for r in fastest_raw]

    # Highest elevation gain
    highest_raw = runs[runs['total_elevation_gain'] > 0].nlargest(5, 'total_elevation_gain')[['name', 'distance_km', 'start_date', 'total_elevation_gain', 'pace_min_per_km']].to_dict('records')
    highest_elevation = [{**r, 'distance_mi': r['distance_km'] * KM_TO_MILES, 'elevation_ft': r['total_elevation_gain'] * M_TO_FT, 'pace_min_per_mi': r['pace_min_per_km'] / KM_TO_MILES} for r in highest_raw]

    # Most consistent (similar pace across long distance)
    long_runs = runs[runs['distance_km'] > 10]
    if len(long_runs) > 0:
        consistent_raw = long_runs.nsmallest(5, 'pace_min_per_km')[['name', 'distance_km', 'start_date', 'pace_min_per_km', 'moving_time_min']].to_dict('records')
        consistent = [{**r, 'distance_mi': r['distance_km'] * KM_TO_MILES, 'pace_min_per_mi': r['pace_min_per_km'] / KM_TO_MILES} for r in consistent_raw]
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

@app.route('/api/routes')
def get_routes():
    """Fetch GPS polylines with pace data - uses cache for speed"""
    if activities_df is None:
        load_data()

    # Check if we should use cache or force refresh
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'

    # Try to load from cache first
    cache_file = 'data/gps_routes_cache.json'
    if not force_refresh and os.path.exists(cache_file):
        try:
            print("Loading GPS routes from cache...")
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)

            # Check if cache is recent (within 7 days)
            cache_time = datetime.fromisoformat(cached_data.get('cached_at', '2000-01-01'))
            if datetime.now() - cache_time < timedelta(days=7):
                print(f"✅ Loaded {len(cached_data['routes'])} routes from cache")
                return jsonify({
                    'routes': cached_data['routes'],
                    'center': cached_data['center'],
                    'total_routes': len(cached_data['routes']),
                    'cached': True,
                    'cached_at': cached_data['cached_at']
                })
            else:
                print("Cache is stale (>7 days), fetching fresh data...")
        except Exception as e:
            print(f"Error loading cache: {e}")

    # Cache miss or refresh requested - fetch from Strava
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to get Strava access token'}), 401

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    # Get ALL runs (sorted by date, most recent first)
    all_runs = runs.sort_values('start_date', ascending=False)

    routes = []
    center_coords = None
    KM_TO_MILES = 0.621371

    print(f"Fetching GPS data for ALL {len(all_runs)} runs (this will take 5-10 minutes)...")

    for idx, (_, run) in enumerate(all_runs.iterrows()):
        activity_id = run['id']

        # Progress indicator
        if (idx + 1) % 50 == 0:
            print(f"  Progress: {idx + 1}/{len(all_runs)} runs processed...")

        try:
            # Fetch activity streams from Strava
            stream_url = f'https://www.strava.com/api/v3/activities/{activity_id}/streams'
            params = {'keys': 'latlng,time,distance', 'key_by_type': True}
            headers = {'Authorization': f'Bearer {access_token}'}

            response = requests.get(stream_url, headers=headers, params=params)

            if response.status_code == 200:
                streams = response.json()

                # Check if we have GPS data
                if 'latlng' in streams and streams['latlng']['data']:
                    latlng_data = streams['latlng']['data']
                    time_data = streams.get('time', {}).get('data', [])
                    distance_data = streams.get('distance', {}).get('data', [])

                    # Set map center to first activity's midpoint
                    if not center_coords and latlng_data:
                        mid_idx = len(latlng_data) // 2
                        center_coords = latlng_data[mid_idx]

                    # Calculate pace for each segment
                    paces = []
                    for i in range(1, len(time_data)):
                        time_diff = time_data[i] - time_data[i-1]  # seconds
                        dist_diff = (distance_data[i] - distance_data[i-1]) / 1000  # km

                        if dist_diff > 0.01:  # At least 10 meters
                            pace_min_per_km = (time_diff / 60) / dist_diff
                            pace_min_per_mi = pace_min_per_km / KM_TO_MILES

                            # Filter unrealistic paces (< 3 min/mi or > 20 min/mi)
                            if 3 < pace_min_per_mi < 20:
                                paces.append(pace_min_per_mi)
                            else:
                                paces.append(None)
                        else:
                            paces.append(None)

                    # Add first point with no pace
                    paces.insert(0, None)

                    routes.append({
                        'activity_id': int(activity_id),
                        'name': run['name'],
                        'date': run['start_date'].strftime('%Y-%m-%d'),
                        'coordinates': latlng_data,
                        'paces': paces,
                        'avg_pace': round(run['pace_min_per_km'] / KM_TO_MILES, 2)
                    })

        except Exception as e:
            print(f"Error fetching streams for activity {activity_id}: {e}")
            continue

    # Default center if no GPS data found
    if not center_coords:
        center_coords = [41.8781, -71.4774]  # Default to Providence, RI

    # Save to cache
    try:
        cache_data = {
            'routes': routes,
            'center': center_coords,
            'cached_at': datetime.now().isoformat(),
            'total_runs_fetched': len(all_runs),
            'routes_with_gps': len(routes)
        }
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)
        print(f"✅ Saved {len(routes)} routes to cache")
    except Exception as e:
        print(f"Error saving cache: {e}")

    return jsonify({
        'routes': routes,
        'center': center_coords,
        'total_routes': len(routes),
        'cached': False
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
