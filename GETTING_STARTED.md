# Getting Started with Strava Race Time Predictor

This guide will walk you through setting up and using the Strava Race Time Predictor.

## Prerequisites

- Python 3.8 or higher
- A Strava account with running activities
- Internet connection

## Step-by-Step Setup

### 1. Initial Setup (One-Time)

Run the automated setup script:

```bash
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Strava API Access

#### A. Create a Strava API Application

1. Visit [https://www.strava.com/settings/api](https://www.strava.com/settings/api)
2. Click "Create App" or use an existing app
3. Fill in the form:
   - **Application Name**: "Race Time Predictor" (or any name)
   - **Category**: "Data Importer"
   - **Club**: Leave blank
   - **Website**: `http://localhost`
   - **Authorization Callback Domain**: `localhost`
4. Click "Create"
5. You'll see your **Client ID** and **Client Secret**

#### B. Configure Your .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   STRAVA_CLIENT_ID=12345
   STRAVA_CLIENT_SECRET=abc123def456...
   STRAVA_REFRESH_TOKEN=  # Leave this blank for now
   ```

#### C. Get Your Refresh Token

1. Run the authentication script:
   ```bash
   python strava_auth.py
   ```

2. The script will display a URL. Copy and paste it into your browser

3. Authorize the application in Strava

4. You'll be redirected to a URL like:
   ```
   http://localhost/?state=&code=XXXXXXXXXXX&scope=read,activity:read_all
   ```

5. Copy the code (everything after `code=` and before `&scope`)

6. Paste it back into the terminal

7. The script will display your refresh token. Add it to your `.env` file:
   ```
   STRAVA_REFRESH_TOKEN=your_refresh_token_here
   ```

### 3. Run the Project

Now you're ready to use the predictor!

#### Option 1: Quick Start (Recommended for First Time)

```bash
python quickstart.py
```

This interactive script will:
1. Fetch all your Strava activities
2. Analyze your training data
3. Create visualizations
4. Train ML models
5. Generate race time predictions

#### Option 2: Run Each Step Manually

```bash
# Step 1: Fetch your activities from Strava
python fetch_strava_data.py

# Step 2: Analyze your training (creates plots)
python analyze_training.py

# Step 3: Train the prediction models
python train_model.py

# Step 4: Get your race time predictions
python predict_race_time.py --all
```

## Understanding Your Results

### Training Analysis

After running `analyze_training.py`, check the `plots/` directory for:

- **training_volume.png**: Your monthly running distance, time, and frequency
- **pace_progression.png**: How your pace has improved over time
- **distance_distribution.png**: Your typical run distances
- **weekly_patterns.png**: When you prefer to run (day/time)
- **elevation_analysis.png**: Elevation patterns in your runs

### Model Training

After running `train_model.py`, you'll see:

- Model performance metrics (MAE, RMSE, R²)
- Comparison of different ML algorithms
- Feature importance (what matters most for predictions)
- Plots showing actual vs predicted times

Models are saved in `models/` directory for each race distance.

### Race Time Predictions

When you run `predict_race_time.py --all`, you'll get:

```
======================================================================
RACE TIME PREDICTIONS
======================================================================

5K:
  Predicted Time: 00:24:30
  Predicted Pace: 4:54 min/km
  Model Accuracy (MAE): ±1.2 minutes

10K:
  Predicted Time: 00:51:15
  Predicted Pace: 5:07 min/km
  Model Accuracy (MAE): ±2.3 minutes

...
```

## Common Workflows

### After Each Training Block

Update your predictions to see improvement:

```bash
# Fetch latest activities
python fetch_strava_data.py

# Get updated predictions
python predict_race_time.py --all
```

### Before a Race

Check your predicted time:

```bash
python predict_race_time.py --distance "5K"
```

### Monthly Analysis

Review your training progress:

```bash
python analyze_training.py
```

## Tips for Accurate Predictions

1. **Have enough race data**: You need at least 5 races at each distance
2. **Consistent training**: Regular running leads to better predictions
3. **Race-specific training**: Include tempo runs and intervals
4. **Update regularly**: Fetch new data after each training block
5. **Similar conditions**: Predictions work best for similar terrain/weather

## Troubleshooting

### "No races identified in the dataset"

**Solution**: The system needs runs at race distances (4.5-5.5K for 5K, etc.). Either:
- Run some actual races
- Do tempo runs at race distances
- Adjust the race detection threshold in `data_preprocessing.py`

### "Not enough data to train model for X"

**Solution**: You need at least 5 races at that distance. Options:
- Focus on distances you race more often
- Wait until you have more race data
- Lower the minimum threshold (but predictions may be less accurate)

### "Authentication failed"

**Solution**:
1. Check all three values in `.env` are filled in
2. Make sure there are no extra spaces
3. Try getting a new refresh token with `python strava_auth.py`

### Predictions seem inaccurate

**Solution**:
- Check if you have enough training data
- Ensure your races are properly detected
- Look at the model's MAE (Mean Absolute Error) - this tells you typical error range
- Consider if your recent training matches your historical patterns

## File Reference

### Scripts You'll Use Often
- `quickstart.py` - Interactive setup and full pipeline
- `fetch_strava_data.py` - Download latest Strava data
- `predict_race_time.py` - Get race time predictions
- `analyze_training.py` - Create training visualizations

### Scripts for Setup
- `strava_auth.py` - Get Strava API credentials
- `setup.sh` - Automated environment setup

### Behind the Scenes
- `data_preprocessing.py` - Feature engineering
- `train_model.py` - ML model training

### Configuration
- `.env` - Your API credentials (keep secret!)
- `requirements.txt` - Python packages needed

### Data Directories
- `data/` - Downloaded activities and processed features
- `models/` - Trained ML models
- `plots/` - Generated visualizations

## Next Steps

Once everything is working:

1. Explore the plots in the `plots/` directory
2. Review your race predictions
3. Keep training and upload to Strava
4. Re-run predictions periodically to track fitness
5. Use predictions to set race goals

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review the main README.md
3. Make sure all dependencies are installed
4. Verify your Strava API credentials
5. Check that you have enough race data

Happy running and predicting!
