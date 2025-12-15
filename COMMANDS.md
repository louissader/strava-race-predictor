# 🎯 All Commands in One Place

## The Absolute Easiest Way

```bash
./go.sh
```
Interactive menu - choose what you want to do!

---

## Quick Commands (Copy & Paste)

### See Your Predictions NOW
```bash
python3 show_predictions_simple.py
```

### Full Analysis with Charts
```bash
python3 run_everything.py
```

### Update Data from Strava
```bash
python3 fetch_strava_data_rest.py
```

### Just Make Charts
```bash
python3 analyze_training.py
```

### Retrain Models
```bash
python3 train_model.py
```

---

## First Time Setup (One Time Only)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Or with Virtual Environment
```bash
./setup.sh
source venv/bin/activate
```

---

## Strava Authorization (If Needed)

If you need to reauthorize or get a new refresh token:

```bash
python3 reauthorize_strava.py
```

Or visit this URL directly:
```
https://www.strava.com/oauth/authorize?client_id=154571&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read,activity:read_all
```

---

## Advanced Commands

### Predict Specific Distance
```bash
python3 predict_race_time.py --distance "5K"
python3 predict_race_time.py --distance "10K"
python3 predict_race_time.py --distance "Half Marathon"
python3 predict_race_time.py --distance "Marathon"
```

### Test Data Preprocessing
```bash
python3 data_preprocessing.py
```

### Quick Strava Auth
```bash
python3 strava_auth.py
```

---

## Typical Workflows

### Monthly Update
```bash
# 1. Get latest data
python3 fetch_strava_data_rest.py

# 2. See new predictions
python3 show_predictions_simple.py
```

### After a Training Block
```bash
# 1. Update data
python3 fetch_strava_data_rest.py

# 2. Retrain models
python3 train_model.py

# 3. See predictions
python3 show_predictions_simple.py
```

### Before a Race
```bash
# Just check your prediction
python3 show_predictions_simple.py
```

### Quarterly Deep Analysis
```bash
# Full pipeline with all charts
python3 run_everything.py

# Check plots/ folder for visualizations
```

---

## File Locations

### Your Data
- `data/strava_activities.csv` - All your activities
- `data/race_features.csv` - Processed race data

### Your Models
- `models/5K_model.joblib`
- `models/10K_model.joblib`
- `models/Half_Marathon_model.joblib`
- `models/Marathon_model.joblib`

### Your Charts
- `plots/training_volume.png`
- `plots/pace_progression.png`
- `plots/distance_distribution.png`
- `plots/weekly_patterns.png`
- `plots/elevation_analysis.png`
- `plots/model_comparison_*.png`
- `plots/predictions_*.png`
- `plots/feature_importance_*.png`

---

## Most Commonly Used Commands

In order of frequency:

1. `python3 show_predictions_simple.py` - Quick check
2. `python3 fetch_strava_data_rest.py` - Monthly update
3. `python3 run_everything.py` - Full analysis
4. `./go.sh` - Interactive menu
5. `python3 analyze_training.py` - Just charts

---

## One-Liner Combos

### Update Everything
```bash
python3 fetch_strava_data_rest.py && python3 train_model.py && python3 show_predictions_simple.py
```

### Quick Analysis
```bash
python3 analyze_training.py && open plots/
```

### Full Refresh
```bash
python3 fetch_strava_data_rest.py && python3 run_everything.py
```

---

## Getting Help

### Show Documentation
```bash
cat START_HERE.md
cat README.md
cat QUICKSTART.md
```

### Check Python Version
```bash
python3 --version
```

### Check Installed Packages
```bash
pip list | grep -E "strava|pandas|sklearn|matplotlib"
```

---

## Troubleshooting Commands

### Reinstall Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Check Data
```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/strava_activities.csv'); print(f'{len(df)} activities loaded')"
```

### Check Models
```bash
ls -lh models/
```

### Check Plots
```bash
ls -lh plots/
```

---

**Remember: The easiest way is just `./go.sh`!** 🎯
