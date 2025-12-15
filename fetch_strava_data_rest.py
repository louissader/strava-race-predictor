"""
Fetch all activities from Strava API using REST API directly with pagination
This script handles pagination to fetch more than 200 activities
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

def get_access_token():
    """Get a fresh access token using refresh token"""
    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("Error: Missing credentials in .env file")
        return None

    # Refresh access token
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    try:
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        return token_data['access_token']
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

def fetch_all_activities_paginated(access_token, per_page=200):
    """
    Fetch all activities using pagination

    Args:
        access_token: Strava API access token
        per_page: Number of activities per page (max 200)

    Returns:
        List of activity dictionaries
    """
    base_url = "https://www.strava.com/api/v3/athlete/activities"

    all_activities = []
    page = 1

    print("Fetching activities from Strava API...")
    print("=" * 70)

    while True:
        print(f"\nFetching page {page} (up to {per_page} activities per page)...")

        headers = {'Authorization': f'Bearer {access_token}'}
        params = {
            'per_page': per_page,
            'page': page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()
            activities = response.json()

            if not activities:
                print(f"No more activities found on page {page}")
                break

            print(f"  Retrieved {len(activities)} activities")
            all_activities.extend(activities)

            # Check rate limits
            rate_limit = response.headers.get('X-RateLimit-Limit')
            rate_usage = response.headers.get('X-RateLimit-Usage')
            print(f"  Rate limit: {rate_usage}/{rate_limit}")

            # If we got fewer activities than requested, we're done
            if len(activities) < per_page:
                print(f"\nReached end of activities (got {len(activities)} < {per_page})")
                break

            page += 1

            # Small delay to respect rate limits
            time.sleep(0.5)

        except requests.exceptions.HTTPError as e:
            print(f"\nHTTP Error: {e}")
            print(f"Response: {response.text}")
            break
        except Exception as e:
            print(f"\nError fetching page {page}: {e}")
            break

    print(f"\n{'=' * 70}")
    print(f"Total activities fetched: {len(all_activities)}")
    return all_activities

def process_activity(activity):
    """Process raw activity data from API"""
    return {
        'id': activity.get('id'),
        'name': activity.get('name'),
        'type': activity.get('type'),
        'distance': float(activity.get('distance', 0)),  # meters
        'moving_time': float(activity.get('moving_time', 0)),  # seconds
        'elapsed_time': float(activity.get('elapsed_time', 0)),  # seconds
        'total_elevation_gain': float(activity.get('total_elevation_gain', 0)),  # meters
        'start_date': activity.get('start_date'),
        'start_date_local': activity.get('start_date_local'),
        'average_speed': float(activity.get('average_speed', 0)),  # m/s
        'max_speed': float(activity.get('max_speed', 0)),  # m/s
        'average_heartrate': float(activity.get('average_heartrate')) if activity.get('average_heartrate') else None,
        'max_heartrate': float(activity.get('max_heartrate')) if activity.get('max_heartrate') else None,
        'average_cadence': float(activity.get('average_cadence')) if activity.get('average_cadence') else None,
        'has_heartrate': activity.get('has_heartrate', False),
        'elev_high': float(activity.get('elev_high')) if activity.get('elev_high') else None,
        'elev_low': float(activity.get('elev_low')) if activity.get('elev_low') else None,
        'pr_count': activity.get('pr_count', 0),
        'achievement_count': activity.get('achievement_count', 0),
        'kudos_count': activity.get('kudos_count', 0),
        'workout_type': activity.get('workout_type'),
        'description': activity.get('description'),
    }

def save_activities_to_csv(activities, filename='data/strava_activities.csv'):
    """Save activities to CSV file"""
    if not activities:
        print("No activities to save")
        return None

    # Process activities
    processed = [process_activity(act) for act in activities]
    df = pd.DataFrame(processed)

    # Convert distances to km and times to minutes for easier reading
    df['distance_km'] = df['distance'] / 1000
    df['moving_time_min'] = df['moving_time'] / 60
    df['elapsed_time_min'] = df['elapsed_time'] / 60
    df['pace_min_per_km'] = df['moving_time_min'] / df['distance_km']
    df['pace_min_per_km'] = df['pace_min_per_km'].replace([float('inf'), -float('inf')], None)

    # Convert date strings to datetime
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['start_date_local'] = pd.to_datetime(df['start_date_local'])

    # Sort by date
    df = df.sort_values('start_date', ascending=False)

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"\n{'=' * 70}")
    print(f"Activities saved to {filename}")

    # Print summary statistics
    print("\n" + "=" * 70)
    print("ACTIVITY SUMMARY")
    print("=" * 70)
    print(f"\nTotal activities: {len(df)}")
    print(f"\nActivity types:")
    print(df['type'].value_counts())

    # Filter for runs
    runs = df[df['type'] == 'Run']
    if len(runs) > 0:
        print(f"\n\nRUNNING STATISTICS")
        print("=" * 70)
        print(f"Total runs: {len(runs)}")
        print(f"Total distance: {runs['distance_km'].sum():.2f} km")
        print(f"Total time: {runs['moving_time_min'].sum():.2f} minutes ({runs['moving_time_min'].sum() / 60:.1f} hours)")
        print(f"Average distance per run: {runs['distance_km'].mean():.2f} km")
        print(f"Average pace: {runs['pace_min_per_km'].mean():.2f} min/km")
        print(f"Best pace: {runs['pace_min_per_km'].min():.2f} min/km")

        # Date range
        print(f"\nDate range: {runs['start_date'].min().date()} to {runs['start_date'].max().date()}")

    return df

def main():
    """Main function to fetch and save Strava activities"""
    print("=" * 70)
    print("Strava Activity Fetcher (REST API with Pagination)")
    print("=" * 70)

    # Get access token
    print("\nAuthenticating with Strava...")
    access_token = get_access_token()

    if not access_token:
        print("Failed to get access token")
        return

    print("✅ Authentication successful")

    # Fetch all activities with pagination
    activities = fetch_all_activities_paginated(access_token, per_page=200)

    if activities:
        # Save to CSV
        df = save_activities_to_csv(activities)

        # Also save raw JSON for backup
        with open('data/strava_activities_raw.json', 'w') as f:
            json.dump(activities, f, default=str, indent=2)
        print(f"\nRaw data saved to data/strava_activities_raw.json")

        print("\n" + "=" * 70)
        print("SUCCESS! All activities fetched and saved")
        print("=" * 70)
    else:
        print("\n❌ No activities fetched")

if __name__ == "__main__":
    main()
