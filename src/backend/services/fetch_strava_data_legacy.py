"""
Fetch all activities from Strava API and save to CSV
"""

import os
import json
import pandas as pd
from datetime import datetime
from services.strava_auth import get_client
from dotenv import load_dotenv

load_dotenv()

def fetch_all_activities(limit=None):
    """
    Fetch all activities from Strava

    Args:
        limit: Maximum number of activities to fetch (None for all)

    Returns:
        List of activity dictionaries
    """
    client = get_client()
    if not client:
        print("Failed to authenticate with Strava")
        return []

    print("Fetching activities from Strava...")
    activities = []

    try:
        for activity in client.get_activities(limit=limit):
            activity_data = {
                'id': activity.id,
                'name': activity.name,
                'type': activity.type,
                'distance': float(activity.distance) if activity.distance else 0,  # meters
                'moving_time': activity.moving_time.total_seconds() if activity.moving_time else 0,  # seconds
                'elapsed_time': activity.elapsed_time.total_seconds() if activity.elapsed_time else 0,  # seconds
                'total_elevation_gain': float(activity.total_elevation_gain) if activity.total_elevation_gain else 0,  # meters
                'start_date': activity.start_date,
                'start_date_local': activity.start_date_local,
                'average_speed': float(activity.average_speed) if activity.average_speed else 0,  # m/s
                'max_speed': float(activity.max_speed) if activity.max_speed else 0,  # m/s
                'average_heartrate': float(activity.average_heartrate) if activity.average_heartrate else None,
                'max_heartrate': float(activity.max_heartrate) if activity.max_heartrate else None,
                'average_cadence': float(activity.average_cadence) if activity.average_cadence else None,
                'has_heartrate': activity.has_heartrate,
                'elev_high': float(activity.elev_high) if activity.elev_high else None,
                'elev_low': float(activity.elev_low) if activity.elev_low else None,
                'pr_count': activity.pr_count if activity.pr_count else 0,
                'achievement_count': activity.achievement_count if activity.achievement_count else 0,
                'kudos_count': activity.kudos_count if activity.kudos_count else 0,
                'workout_type': activity.workout_type,
                'description': activity.description,
            }
            activities.append(activity_data)

            if len(activities) % 50 == 0:
                print(f"Fetched {len(activities)} activities...")

        print(f"\nTotal activities fetched: {len(activities)}")

    except Exception as e:
        print(f"Error fetching activities: {e}")

    return activities

def save_activities_to_csv(activities, filename='data/strava_activities.csv'):
    """Save activities to CSV file"""
    if not activities:
        print("No activities to save")
        return

    df = pd.DataFrame(activities)

    # Convert distances to km and times to minutes for easier reading
    df['distance_km'] = df['distance'] / 1000
    df['moving_time_min'] = df['moving_time'] / 60
    df['elapsed_time_min'] = df['elapsed_time'] / 60
    df['pace_min_per_km'] = df['moving_time_min'] / df['distance_km']
    df['pace_min_per_km'] = df['pace_min_per_km'].replace([float('inf'), -float('inf')], None)

    # Sort by date
    df = df.sort_values('start_date', ascending=False)

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"\nActivities saved to {filename}")

    # Print summary statistics
    print("\n" + "=" * 50)
    print("ACTIVITY SUMMARY")
    print("=" * 50)
    print(f"\nTotal activities: {len(df)}")
    print(f"\nActivity types:")
    print(df['type'].value_counts())

    # Filter for runs
    runs = df[df['type'] == 'Run']
    if len(runs) > 0:
        print(f"\n\nRUNNING STATISTICS")
        print("=" * 50)
        print(f"Total runs: {len(runs)}")
        print(f"Total distance: {runs['distance_km'].sum():.2f} km")
        print(f"Total time: {runs['moving_time_min'].sum():.2f} minutes")
        print(f"Average distance per run: {runs['distance_km'].mean():.2f} km")
        print(f"Average pace: {runs['pace_min_per_km'].mean():.2f} min/km")
        print(f"Best pace: {runs['pace_min_per_km'].min():.2f} min/km")

    return df

def main():
    """Main function to fetch and save Strava activities"""
    print("Strava Activity Fetcher")
    print("=" * 50)

    # Fetch all activities (remove limit to get all)
    activities = fetch_all_activities(limit=None)

    if activities:
        # Save to CSV
        df = save_activities_to_csv(activities)

        # Also save raw JSON for backup
        with open('data/strava_activities_raw.json', 'w') as f:
            json.dump(activities, f, default=str, indent=2)
        print(f"Raw data saved to data/strava_activities_raw.json")
    else:
        print("No activities fetched")

if __name__ == "__main__":
    main()
