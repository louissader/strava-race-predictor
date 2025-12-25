# 🏃 START HERE - Easiest Way to Use This Project

## ⚡ Super Quick Start (3 Commands)

```bash
# 1. Install dependencies (one time only)
pip install -r requirements.txt

# 2. Fetch your Strava data (already done for you!)
# Skip this step - you already have 1,580 activities loaded!

# 3. Run everything!
python3 show_predictions_simple.py
```

That's it! You'll see:
- ✅ Your racing history (best times, averages)
- 🤖 ML model predictions
- 📊 Recent training summary

---

## 📊 Want Full Analysis with Charts?

If you want detailed visualizations and training analysis:

```bash
python3 run_everything.py
```

This will create beautiful charts in the `plots/` folder showing:
- Training volume over time
- Pace progression
- Weekly patterns
- Model accuracy
- Feature importance

---

## 🔄 Updating After New Runs

When you've done more training or races:

```bash
# Fetch latest activities from Strava
python3 fetch_strava_data_rest.py

# See updated predictions
python3 show_predictions_simple.py
```

---

## 📈 What You Currently Have

Based on your Strava data:

### Your Racing Stats
- **18 x 5K races** → Best: 17.00 min (3:24 min/km pace)
- **28 x 10K races** → Best: 40.93 min (4:05 min/km pace)
- **1 x Half Marathon** → Time: 1:38:56 (4:41 min/km pace)

### ML Models Trained
- ✅ **5K Model** - Accuracy: ±1.0 min (69% R²)
- ✅ **10K Model** - Accuracy: ±1.2 min (75% R²)

### Your Data
- 1,580 total activities
- 1,369 runs
- 8,722 km total distance
- 719 hours of running

---

## 🎯 Quick Commands Reference

| I Want To... | Command |
|-------------|---------|
| **See my predictions NOW** | `python3 show_predictions_simple.py` |
| **Run full analysis** | `python3 run_everything.py` |
| **Fetch new Strava data** | `python3 fetch_strava_data_rest.py` |
| **Just create charts** | `python3 analyze_training.py` |
| **Retrain models** | `python3 train_model.py` |

---

## 💡 Tips for Best Results

1. **More races = better predictions**
   - You have great data for 5K and 10K!
   - Need 5+ races at each distance for Half/Full marathon models

2. **Consistent training = accurate predictions**
   - Your models learn from the relationship between training and racing
   - Keep uploading all your runs to Strava

3. **Update regularly**
   - Re-fetch data monthly: `python3 fetch_strava_data_rest.py`
   - Retrain models after big races or training blocks

---

## 🆘 Troubleshooting

**Problem:** "Module not found" error
**Solution:** Run `pip install -r requirements.txt`

**Problem:** "No module named 'pytz'"
**Solution:** Run `pip install pytz`

**Problem:** Need to re-authorize Strava
**Solution:** Visit this URL and click Authorize:
```
https://www.strava.com/oauth/authorize?client_id=154571&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read,activity:read_all
```
Then run `python3 reauthorize_strava.py` and paste the code

---

## 🎉 You're All Set!

Your simplest workflow:

1. Train and race regularly 🏃‍♂️
2. Activities auto-sync to Strava 📱
3. Occasionally run: `python3 fetch_strava_data_rest.py`
4. See predictions: `python3 show_predictions_simple.py`

**That's it!** The ML models will predict your race times based on your training patterns.

---

## 📂 What's in This Project?

- `plots/` - Beautiful training visualizations
- `models/` - Your trained ML models
- `data/` - Your Strava activities (CSV & JSON)
- `show_predictions_simple.py` - Quick predictions (START HERE)
- `run_everything.py` - Full pipeline with charts
- `fetch_strava_data_rest.py` - Get latest activities
- `analyze_training.py` - Create visualizations only
- `train_model.py` - Retrain ML models

For full documentation, see [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)

---

**Happy Running! 🏃💨**
