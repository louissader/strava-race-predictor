"""
Analyze and visualize training data from Strava
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from data_preprocessing import load_activities

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

def plot_training_volume_over_time(df, save_path='plots/training_volume.png'):
    """Plot training volume over time"""
    runs = df[df['type'] == 'Run'].copy()

    if len(runs) == 0:
        print("No running activities found")
        return

    # Group by month
    runs['month'] = runs['start_date'].dt.to_period('M')
    monthly = runs.groupby('month').agg({
        'distance_km': 'sum',
        'moving_time_min': 'sum',
        'id': 'count'
    }).rename(columns={'id': 'num_runs'})

    fig, axes = plt.subplots(3, 1, figsize=(15, 12))

    # Distance per month
    monthly['distance_km'].plot(kind='bar', ax=axes[0], color='steelblue', alpha=0.7)
    axes[0].set_title('Monthly Running Distance', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Distance (km)', fontsize=12)
    axes[0].set_xlabel('')
    axes[0].grid(True, alpha=0.3)

    # Time per month
    monthly['moving_time_min'].plot(kind='bar', ax=axes[1], color='green', alpha=0.7)
    axes[1].set_title('Monthly Running Time', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Time (minutes)', fontsize=12)
    axes[1].set_xlabel('')
    axes[1].grid(True, alpha=0.3)

    # Number of runs per month
    monthly['num_runs'].plot(kind='bar', ax=axes[2], color='coral', alpha=0.7)
    axes[2].set_title('Monthly Number of Runs', fontsize=14, fontweight='bold')
    axes[2].set_ylabel('Number of Runs', fontsize=12)
    axes[2].set_xlabel('Month', fontsize=12)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Training volume plot saved to {save_path}")
    plt.close()

def plot_pace_progression(df, save_path='plots/pace_progression.png'):
    """Plot pace progression over time"""
    runs = df[df['type'] == 'Run'].copy()
    runs = runs[runs['pace_min_per_km'] > 0]

    if len(runs) == 0:
        print("No pace data available")
        return

    fig, axes = plt.subplots(2, 1, figsize=(15, 10))

    # Pace over time with rolling average
    axes[0].scatter(runs['start_date'], runs['pace_min_per_km'], alpha=0.3, s=30)
    if len(runs) > 10:
        runs_sorted = runs.sort_values('start_date')
        rolling_pace = runs_sorted.set_index('start_date')['pace_min_per_km'].rolling(window=10, center=True).mean()
        axes[0].plot(rolling_pace.index, rolling_pace.values, color='red', linewidth=2, label='10-run moving average')
        axes[0].legend()

    axes[0].set_title('Pace Progression Over Time', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Pace (min/km)', fontsize=12)
    axes[0].set_xlabel('Date', fontsize=12)
    axes[0].invert_yaxis()
    axes[0].grid(True, alpha=0.3)

    # Pace distribution
    axes[1].hist(runs['pace_min_per_km'], bins=30, alpha=0.7, color='steelblue', edgecolor='black')
    axes[1].axvline(runs['pace_min_per_km'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {runs["pace_min_per_km"].median():.2f} min/km')
    axes[1].axvline(runs['pace_min_per_km'].mean(), color='green', linestyle='--', linewidth=2, label=f'Mean: {runs["pace_min_per_km"].mean():.2f} min/km')
    axes[1].set_title('Pace Distribution', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Pace (min/km)', fontsize=12)
    axes[1].set_ylabel('Frequency', fontsize=12)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Pace progression plot saved to {save_path}")
    plt.close()

def plot_distance_distribution(df, save_path='plots/distance_distribution.png'):
    """Plot distribution of run distances"""
    runs = df[df['type'] == 'Run'].copy()

    if len(runs) == 0:
        print("No running activities found")
        return

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Distance histogram
    axes[0].hist(runs['distance_km'], bins=30, alpha=0.7, color='green', edgecolor='black')
    axes[0].set_title('Run Distance Distribution', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Distance (km)', fontsize=12)
    axes[0].set_ylabel('Frequency', fontsize=12)
    axes[0].axvline(runs['distance_km'].median(), color='red', linestyle='--', linewidth=2, label=f'Median: {runs["distance_km"].median():.2f} km')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Distance over time
    axes[1].scatter(runs['start_date'], runs['distance_km'], alpha=0.5, s=50)
    if len(runs) > 10:
        runs_sorted = runs.sort_values('start_date')
        rolling_dist = runs_sorted.set_index('start_date')['distance_km'].rolling(window=10, center=True).mean()
        axes[1].plot(rolling_dist.index, rolling_dist.values, color='red', linewidth=2, label='10-run moving average')
        axes[1].legend()

    axes[1].set_title('Run Distance Over Time', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Date', fontsize=12)
    axes[1].set_ylabel('Distance (km)', fontsize=12)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Distance distribution plot saved to {save_path}")
    plt.close()

def plot_weekly_patterns(df, save_path='plots/weekly_patterns.png'):
    """Plot weekly running patterns"""
    runs = df[df['type'] == 'Run'].copy()

    if len(runs) == 0:
        print("No running activities found")
        return

    runs['day_of_week'] = runs['start_date_local'].dt.day_name()
    runs['hour_of_day'] = runs['start_date_local'].dt.hour

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Runs by day of week
    day_counts = runs['day_of_week'].value_counts().reindex(day_order, fill_value=0)
    day_counts.plot(kind='bar', ax=axes[0], color='steelblue', alpha=0.7)
    axes[0].set_title('Runs by Day of Week', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Number of Runs', fontsize=12)
    axes[0].set_xlabel('Day of Week', fontsize=12)
    axes[0].set_xticklabels(day_order, rotation=45)
    axes[0].grid(True, alpha=0.3)

    # Runs by hour of day
    hour_counts = runs['hour_of_day'].value_counts().sort_index()
    axes[1].bar(hour_counts.index, hour_counts.values, alpha=0.7, color='coral')
    axes[1].set_title('Runs by Hour of Day', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Number of Runs', fontsize=12)
    axes[1].set_xlabel('Hour of Day', fontsize=12)
    axes[1].set_xticks(range(0, 24, 2))
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Weekly patterns plot saved to {save_path}")
    plt.close()

def plot_elevation_analysis(df, save_path='plots/elevation_analysis.png'):
    """Plot elevation gain analysis"""
    runs = df[df['type'] == 'Run'].copy()
    runs = runs[runs['total_elevation_gain'] > 0]

    if len(runs) == 0:
        print("No elevation data available")
        return

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # Elevation gain over time
    axes[0, 0].scatter(runs['start_date'], runs['total_elevation_gain'], alpha=0.5, s=50)
    axes[0, 0].set_title('Elevation Gain Over Time', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Elevation Gain (m)', fontsize=12)
    axes[0, 0].set_xlabel('Date', fontsize=12)
    axes[0, 0].grid(True, alpha=0.3)

    # Elevation gain distribution
    axes[0, 1].hist(runs['total_elevation_gain'], bins=30, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].set_title('Elevation Gain Distribution', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Elevation Gain (m)', fontsize=12)
    axes[0, 1].set_ylabel('Frequency', fontsize=12)
    axes[0, 1].grid(True, alpha=0.3)

    # Elevation gain vs distance
    axes[1, 0].scatter(runs['distance_km'], runs['total_elevation_gain'], alpha=0.5, s=50)
    axes[1, 0].set_title('Elevation Gain vs Distance', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Distance (km)', fontsize=12)
    axes[1, 0].set_ylabel('Elevation Gain (m)', fontsize=12)
    axes[1, 0].grid(True, alpha=0.3)

    # Elevation gain vs pace
    runs_with_pace = runs[runs['pace_min_per_km'] > 0]
    if len(runs_with_pace) > 0:
        axes[1, 1].scatter(runs_with_pace['total_elevation_gain'], runs_with_pace['pace_min_per_km'], alpha=0.5, s=50)
        axes[1, 1].set_title('Elevation Gain vs Pace', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Elevation Gain (m)', fontsize=12)
        axes[1, 1].set_ylabel('Pace (min/km)', fontsize=12)
        axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Elevation analysis plot saved to {save_path}")
    plt.close()

def print_summary_statistics(df):
    """Print summary statistics for running activities"""
    runs = df[df['type'] == 'Run'].copy()

    if len(runs) == 0:
        print("No running activities found")
        return

    print("\n" + "=" * 70)
    print("RUNNING ACTIVITY SUMMARY")
    print("=" * 70)

    print(f"\nTotal runs: {len(runs)}")
    print(f"Date range: {runs['start_date'].min().date()} to {runs['start_date'].max().date()}")
    print(f"Total distance: {runs['distance_km'].sum():.2f} km")
    print(f"Total time: {runs['moving_time_min'].sum():.2f} minutes ({runs['moving_time_min'].sum() / 60:.1f} hours)")

    print(f"\n{'DISTANCE STATISTICS':^70}")
    print(f"Average distance per run: {runs['distance_km'].mean():.2f} km")
    print(f"Median distance: {runs['distance_km'].median():.2f} km")
    print(f"Shortest run: {runs['distance_km'].min():.2f} km")
    print(f"Longest run: {runs['distance_km'].max():.2f} km")

    print(f"\n{'PACE STATISTICS':^70}")
    print(f"Average pace: {runs['pace_min_per_km'].mean():.2f} min/km")
    print(f"Median pace: {runs['pace_min_per_km'].median():.2f} min/km")
    print(f"Best pace: {runs['pace_min_per_km'].min():.2f} min/km")
    print(f"Slowest pace: {runs['pace_min_per_km'].max():.2f} min/km")

    if runs['total_elevation_gain'].sum() > 0:
        print(f"\n{'ELEVATION STATISTICS':^70}")
        print(f"Total elevation gain: {runs['total_elevation_gain'].sum():.0f} m")
        print(f"Average elevation gain per run: {runs['total_elevation_gain'].mean():.0f} m")
        print(f"Maximum elevation gain: {runs['total_elevation_gain'].max():.0f} m")

    if runs['average_heartrate'].notna().any():
        hr_runs = runs[runs['average_heartrate'].notna()]
        print(f"\n{'HEART RATE STATISTICS':^70}")
        print(f"Runs with HR data: {len(hr_runs)} ({len(hr_runs) / len(runs) * 100:.1f}%)")
        print(f"Average heart rate: {hr_runs['average_heartrate'].mean():.0f} bpm")
        print(f"Max heart rate recorded: {hr_runs['max_heartrate'].max():.0f} bpm")

    # Recent training
    recent_30d = runs[runs['start_date'] >= runs['start_date'].max() - timedelta(days=30)]
    recent_7d = runs[runs['start_date'] >= runs['start_date'].max() - timedelta(days=7)]

    print(f"\n{'RECENT TRAINING':^70}")
    print(f"Last 7 days: {len(recent_7d)} runs, {recent_7d['distance_km'].sum():.2f} km")
    print(f"Last 30 days: {len(recent_30d)} runs, {recent_30d['distance_km'].sum():.2f} km")

def main():
    """Main analysis function"""
    print("Strava Training Data Analysis")
    print("=" * 70)

    # Load activities
    print("\nLoading activities...")
    df = load_activities()

    # Print summary statistics
    print_summary_statistics(df)

    # Create visualizations
    print("\n" + "=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)

    plot_training_volume_over_time(df)
    plot_pace_progression(df)
    plot_distance_distribution(df)
    plot_weekly_patterns(df)
    plot_elevation_analysis(df)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nAll plots saved to the 'plots' directory")

if __name__ == "__main__":
    main()
