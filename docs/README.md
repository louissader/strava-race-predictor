# Strava Race Time Predictor

A full-stack web application that visualizes your Strava running data and predicts race times using machine learning.

![React](https://img.shields.io/badge/React-18.3-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![Python](https://img.shields.io/badge/Python-3.9+-yellow)

## Live Demo

Interactive React web application with:
- 📊 **Dashboard** - Real-time statistics and impressive activities
- 🗺️ **GPS Heatmap** - Routes colored by pace with Leaflet maps
- 📈 **Race Predictions** - ML-powered time predictions for all distances
- 📉 **Analytics** - Training trends and performance insights

## Key Features

### Frontend (React 18 + Vite)
- **Interactive Dashboard**: Real-time running statistics (total miles, elevation, pace trends)
- **GPS Route Heatmap**: Visualizes ALL runs with pace-based color coding
  - Red (≤6:00/mi) to Blue (≥11:00/mi) gradient
  - GPS polyline rendering with Leaflet
  - Shows exactly where you sped up or slowed down
- **Race Predictions**: ML model predictions displayed in clean cards
- **Responsive Design**: Custom cyberpunk-inspired UI with Framer Motion animations
- **Client-Side Routing**: React Router v6 for smooth navigation

### Backend (Flask REST API)
- **Strava OAuth 2.0**: Automatic token refresh for API access
- **Real-time GPS Fetching**: Pulls detailed activity streams (coordinates, pace, elevation)
- **ML Pipeline**: Random Forest/Gradient Boosting models for race prediction
- **Unit Conversion**: All data served in miles and feet
- **CORS-enabled**: Seamless React integration

### Machine Learning
- **Smart Race Detection**: Identifies potential race activities (5K, 10K, Half Marathon, Marathon)
- **Feature Engineering**: 30+ training features including volume, pace trends, elevation
- **Multiple Models**: Compares Random Forest, Gradient Boosting, Ridge, and Lasso
- **Cross-Validation**: Ensures robust predictions

## Quick Start

The fastest way to get started:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up Strava credentials (see Setup section below)

# 3. Run the quick start script
python quickstart.py
```

This interactive script will guide you through fetching data, training models, and making predictions.

## Detailed Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Strava API Credentials

1. Go to [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Create a new application:
   - **Application Name**: Choose any name (e.g., "Race Time Predictor")
   - **Category**: Choose "Data Importer" or similar
   - **Website**: Can use http://localhost
   - **Authorization Callback Domain**: Use `localhost`
3. Note your **Client ID** and **Client Secret**
4. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
5. Edit `.env` and add your Client ID and Client Secret

### 3. Get Your Refresh Token

```bash
python strava_auth.py
```

This will:
1. Print an authorization URL
2. Open it in your browser and authorize the app
3. Copy the `code` from the redirect URL
4. Paste it back into the terminal
5. The script will give you a refresh token to add to `.env`

## Usage

### Web Application (Recommended)

Start the full-stack React app:

```bash
./run_react_app.sh
```

This will:
1. Start the Flask API server on `http://localhost:5001`
2. Start the React dev server on `http://localhost:5173`
3. Open the app in your browser

**Tech Stack:**
- Frontend: React 18, Vite, React Router v6, Leaflet, Framer Motion, Axios
- Backend: Flask, Flask-CORS, pandas, scikit-learn
- API Integration: Strava OAuth 2.0 with automatic token refresh

### Command Line Tools

#### Option 1: Use the Quick Start Script

```bash
python quickstart.py
```

This interactive script walks you through the entire process.

### Option 2: Run Each Step Manually

#### Step 1: Fetch Your Strava Activities

```bash
python fetch_strava_data.py
```

This downloads all your activities and saves them to `data/strava_activities.csv`.

#### Step 2: Analyze Your Training Data (Optional)

```bash
python analyze_training.py
```

This generates visualizations of your training:
- Monthly distance and time trends
- Pace progression over time
- Weekly running patterns
- Elevation analysis

All plots are saved to the `plots/` directory.

#### Step 3: Train the Prediction Models

```bash
python train_model.py
```

This will:
- Identify potential race activities
- Extract training features for each race
- Train multiple ML models for each distance
- Compare model performance
- Save the best model for each distance

#### Step 4: Make Predictions

Predict all distances:
```bash
python predict_race_time.py --all
```

Predict a specific distance:
```bash
python predict_race_time.py --distance "5K"
python predict_race_time.py --distance "10K"
python predict_race_time.py --distance "Half Marathon"
python predict_race_time.py --distance "Marathon"
```

## How It Works

### Race Detection
The system identifies potential races using:
- Distance matching (5K, 10K, 21K, 42K with tolerance)
- Pace analysis (faster than average runs)
- Achievement counts and PRs from Strava

### Feature Engineering
For each race, the model calculates training features from preceding weeks:
- **Volume metrics**: Total distance, number of runs (7, 14, 30, 60, 90 days)
- **Intensity metrics**: Average pace, best pace
- **Long run metrics**: Longest run distance
- **Elevation metrics**: Total elevation gain
- **Recovery metrics**: Days since last run
- **Fitness indicators**: Average heart rate (if available)

### Machine Learning Models
The system trains and compares four models:
1. **Random Forest**: Ensemble of decision trees
2. **Gradient Boosting**: Sequential boosting algorithm
3. **Ridge Regression**: Linear model with L2 regularization
4. **Lasso Regression**: Linear model with L1 regularization

The best model is automatically selected based on cross-validated performance.

### Predictions
Using your current training data, the model predicts your race time based on:
- Your recent training volume
- Your recent pace trends
- Your longest runs
- Your fitness progression

## Project Structure

```
Strava Project/
├── api.py                      # Flask REST API server
├── run_react_app.sh            # Launch script for web app
├── strava_auth.py              # OAuth authentication helper
├── fetch_strava_data.py        # Downloads activities from Strava
├── data_preprocessing.py       # Feature engineering and data prep
├── train_model.py              # Model training and evaluation
├── predict_race_time.py        # Race time prediction interface
├── analyze_training.py         # Training data analysis and visualization
├── quickstart.py               # Interactive quick start script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env                        # Your credentials (not in git)
├── frontend/                   # React web application
│   ├── src/
│   │   ├── App.jsx            # Main app component with routing
│   │   ├── main.jsx           # React entry point
│   │   ├── index.css          # Global styles
│   │   └── pages/
│   │       ├── Dashboard.jsx  # Homepage with stats
│   │       ├── Heatmap.jsx    # GPS route visualization
│   │       ├── Analytics.jsx  # Training analytics
│   │       └── Timeline.jsx   # Prediction timeline
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
├── data/
│   ├── strava_activities.csv   # Raw activity data
│   ├── race_features.csv       # Processed race features
│   └── strava_activities_raw.json  # JSON backup
├── models/
│   ├── 5K_model.joblib         # Trained 5K model
│   ├── 10K_model.joblib        # Trained 10K model
│   ├── Half_Marathon_model.joblib  # Trained half marathon model
│   └── Marathon_model.joblib   # Trained marathon model
└── plots/
    ├── training_volume.png     # Training volume over time
    ├── pace_progression.png    # Pace trends
    ├── distance_distribution.png  # Distance patterns
    ├── weekly_patterns.png     # Day/time patterns
    ├── elevation_analysis.png  # Elevation metrics
    ├── model_comparison_*.png  # Model performance
    ├── predictions_*.png       # Actual vs predicted
    └── feature_importance_*.png # Feature importance
```

## Troubleshooting

### "No races identified"
- You need at least a few runs at standard race distances (5K, 10K, etc.)
- The system looks for faster-than-average efforts at these distances
- Try running more races or tempo runs at race distances

### "Not enough data to train model"
- You need at least 5 races at a given distance to train a model
- If you don't have enough races, the model will skip that distance

### "Authentication failed"
- Make sure your `.env` file has all three credentials
- Try running `python strava_auth.py` again to get a fresh refresh token
- Check that your Strava app has the correct callback domain

### Poor prediction accuracy
- Model accuracy improves with more race data
- Consistent training patterns yield better predictions
- Try training more at race-specific distances

## Tips for Best Results

1. **Run races regularly**: The more race data, the better the predictions
2. **Maintain consistent training**: Regular running improves model accuracy
3. **Record all activities**: Don't forget to upload every run to Strava
4. **Use similar race conditions**: Models work best when predicting similar terrain/conditions
5. **Update predictions regularly**: Re-run after major training blocks

## Future Enhancements

Potential improvements:
- Weather data integration
- Course difficulty adjustment
- Training plan recommendations
- Real-time fitness tracking
- Multi-sport support
- Race day readiness score

## License

This project is for personal use. Strava API usage must comply with Strava's Terms of Service.
