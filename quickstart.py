"""
Quick start script to run the entire pipeline
"""

import os
import sys

def check_env_file():
    """Check if .env file exists with credentials"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\nPlease create a .env file with your Strava API credentials:")
        print("  1. Copy .env.example to .env")
        print("  2. Go to https://www.strava.com/settings/api")
        print("  3. Create an application and get your Client ID and Client Secret")
        print("  4. Run: python strava_auth.py to get your refresh token")
        print("  5. Add all credentials to .env file")
        return False

    from dotenv import load_dotenv
    load_dotenv()

    client_id = os.getenv('STRAVA_CLIENT_ID')
    client_secret = os.getenv('STRAVA_CLIENT_SECRET')
    refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing credentials in .env file!")
        print("\nYour .env file should contain:")
        print("  STRAVA_CLIENT_ID=your_client_id")
        print("  STRAVA_CLIENT_SECRET=your_client_secret")
        print("  STRAVA_REFRESH_TOKEN=your_refresh_token")
        print("\nRun: python strava_auth.py to get your refresh token")
        return False

    print("✅ .env file configured")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n" + "=" * 70)
    print("INSTALLING DEPENDENCIES")
    print("=" * 70)

    import subprocess
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        print(result.stderr)
        return False

def fetch_data():
    """Fetch Strava activities"""
    print("\n" + "=" * 70)
    print("FETCHING STRAVA DATA")
    print("=" * 70)

    try:
        from fetch_strava_data import main as fetch_main
        fetch_main()
        print("✅ Data fetched successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return False

def analyze_data():
    """Analyze training data"""
    print("\n" + "=" * 70)
    print("ANALYZING TRAINING DATA")
    print("=" * 70)

    try:
        from analyze_training import main as analyze_main
        analyze_main()
        print("✅ Analysis complete")
        return True
    except Exception as e:
        print(f"❌ Failed to analyze data: {e}")
        return False

def train_models():
    """Train prediction models"""
    print("\n" + "=" * 70)
    print("TRAINING ML MODELS")
    print("=" * 70)

    try:
        from train_model import main as train_main
        train_main()
        print("✅ Models trained successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to train models: {e}")
        return False

def make_predictions():
    """Make race time predictions"""
    print("\n" + "=" * 70)
    print("GENERATING PREDICTIONS")
    print("=" * 70)

    try:
        from predict_race_time import predict_all_distances, print_prediction_report
        predictions = predict_all_distances()
        if predictions:
            print_prediction_report(predictions)
            print("✅ Predictions generated successfully")
            return True
        else:
            print("❌ No predictions available")
            return False
    except Exception as e:
        print(f"❌ Failed to generate predictions: {e}")
        return False

def main():
    """Run the entire pipeline"""
    print("=" * 70)
    print("STRAVA RACE TIME PREDICTOR - QUICK START")
    print("=" * 70)

    # Check environment
    if not check_env_file():
        return

    # Install dependencies
    print("\nDo you want to install dependencies? (y/n): ", end="")
    if input().lower() == 'y':
        if not install_dependencies():
            return

    # Check if data already exists
    data_exists = os.path.exists('data/strava_activities.csv')

    if data_exists:
        print("\n✅ Data file found at data/strava_activities.csv")
        print("Do you want to re-fetch data from Strava? (y/n): ", end="")
        fetch_new = input().lower() == 'y'
    else:
        print("\n⚠️  No data file found. Will fetch from Strava.")
        fetch_new = True

    # Fetch data
    if fetch_new:
        if not fetch_data():
            return
    else:
        print("✅ Using existing data")

    # Analyze data
    print("\nDo you want to analyze training data and create visualizations? (y/n): ", end="")
    if input().lower() == 'y':
        analyze_data()

    # Train models
    print("\nDo you want to train prediction models? (y/n): ", end="")
    if input().lower() == 'y':
        if not train_models():
            print("\n⚠️  Model training failed or insufficient data for predictions")
            return

    # Make predictions
    print("\nDo you want to generate race time predictions? (y/n): ", end="")
    if input().lower() == 'y':
        make_predictions()

    print("\n" + "=" * 70)
    print("QUICK START COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  - View plots in the 'plots' directory")
    print("  - Check trained models in the 'models' directory")
    print("  - Run 'python predict_race_time.py --all' anytime for new predictions")
    print("  - Run 'python analyze_training.py' to regenerate analysis")

if __name__ == "__main__":
    main()
