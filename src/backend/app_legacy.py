"""
Flask Web Application for Strava Race Time Predictor
Interactive dashboard with predictions, analytics, and visualizations
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json
from datetime import datetime, timedelta
import joblib
from utils.data_preprocessing import load_activities, create_race_dataset, calculate_training_features
import folium
from folium.plugins import HeatMap
import os

app = Flask(__name__,
            template_folder='web_app/templates',
            static_folder='web_app/static')

# Load data on startup
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

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()

    stats = {
        'total_activities': len(activities_df),
        'total_runs': len(runs),
        'total_distance_km': round(runs['distance_km'].sum(), 1),
        'total_time_hours': round(runs['moving_time_min'].sum() / 60, 1),
        'avg_pace': round(runs['pace_min_per_km'].mean(), 2),
        'best_pace': round(runs['pace_min_per_km'].min(), 2),
        'longest_run_km': round(runs['distance_km'].max(), 1),
        'first_run_date': runs['start_date'].min().strftime('%Y-%m-%d'),
        'last_run_date': runs['start_date'].max().strftime('%Y-%m-%d'),
    }

    return jsonify(stats)

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

            # Get race history
            races = race_df[race_df['race_distance'] == distance]

            if len(races) > 0:
                predictions[distance] = {
                    'num_races': len(races),
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
            'time_min': round(race['race_time_min'], 2),
            'pace': round(race['race_pace_min_per_km'], 2),
            'name': race['race_name']
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
        return jsonify({'error': 'Model not found'})

    # Get dates every month for the past year of data
    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs['start_date'] = pd.to_datetime(runs['start_date'])

    latest_date = runs['start_date'].max()
    earliest_date = latest_date - timedelta(days=730)  # 2 years

    timeline = []
    current_date = earliest_date

    while current_date <= latest_date:
        # Calculate features for this date
        features = calculate_training_features(activities_df, current_date)

        # Make prediction
        feature_values = []
        for feature_name in feature_names:
            value = features.get(feature_name, 0)
            if value is None or pd.isna(value):
                value = 0
            feature_values.append(value)

        X = np.array(feature_values).reshape(1, -1)
        X_scaled = scaler.transform(X)
        predicted_time = model.predict(X_scaled)[0]

        timeline.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'predicted_time_min': round(predicted_time, 2),
            'weekly_distance': round(features.get('past_7d_total_distance_km', 0), 1),
            'monthly_distance': round(features.get('past_30d_total_distance_km', 0), 1)
        })

        current_date += timedelta(days=30)  # Monthly intervals

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
        'id': 'count'
    }).reset_index()
    monthly.columns = ['month', 'distance_km', 'time_min', 'num_runs']

    return jsonify(monthly.to_dict(orient='records'))

@app.route('/api/pace_distribution')
def get_pace_distribution():
    """Get pace distribution data"""
    if activities_df is None:
        load_data()

    runs = activities_df[activities_df['type'] == 'Run'].copy()
    runs = runs[runs['pace_min_per_km'] > 0]

    # Create pace bins
    pace_data = runs['pace_min_per_km'].values

    return jsonify({
        'paces': pace_data.tolist(),
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

    day_counts = runs['day_of_week'].value_counts().to_dict()
    hour_counts = runs['hour'].value_counts().sort_index().to_dict()

    return jsonify({
        'by_day': day_counts,
        'by_hour': hour_counts
    })

@app.route('/api/heatmap_data')
def get_heatmap_data():
    """Get data for route heatmap (simplified without GPS data)"""
    # Note: Strava API doesn't return GPS coordinates by default
    # This would require detailed activity streams from Strava API
    # For now, return placeholder
    return jsonify({
        'message': 'GPS heatmap requires detailed activity streams from Strava API',
        'total_runs': len(activities_df[activities_df['type'] == 'Run']) if activities_df is not None else 0
    })

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

@app.route('/timeline')
def timeline():
    """Timeline predictions page"""
    return render_template('timeline.html')

if __name__ == '__main__':
    print("=" * 70)
    print("  STRAVA RACE TIME PREDICTOR - WEB APP")
    print("=" * 70)
    print("\nLoading data...")

    if load_data():
        print("✅ Data loaded successfully!")
        print(f"   Total activities: {len(activities_df)}")
        print(f"   Total runs: {len(activities_df[activities_df['type'] == 'Run'])}")
        print("\n" + "=" * 70)
        print("  Starting web server...")
        print("=" * 70)
        print("\n🌐 Open your browser and go to:")
        print("   http://localhost:5001")
        print("\n   Press Ctrl+C to stop the server\n")
        app.run(debug=True, host='0.0.0.0', port=5001)
    else:
        print("❌ Failed to load data. Please run fetch_strava_data_rest.py first.")
