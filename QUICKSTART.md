# 🏃 Quick Start Guide - 3 Easy Steps!

## For First-Time Users

### Step 1: Install Python Packages (One Time Only)

```bash
pip install -r requirements.txt
```

### Step 2: Connect to Strava (One Time Only)

You need to authorize this app to read your Strava activities. This is already done for you, but if you need to do it again:

1. Visit this URL in your browser:
   ```
   https://www.strava.com/oauth/authorize?client_id=154571&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read,activity:read_all
   ```

2. Click "Authorize"

3. Copy the code from the redirect URL (the part after `code=`)

4. Run: `python3 reauthorize_strava.py` and paste the code

### Step 3: Run Everything!

```bash
python3 run_everything.py
```

That's it! The script will:
- ✅ Analyze your training data
- 🤖 Train ML models
- 🎯 Predict your race times

---

## 🎯 The Easiest Way to Use This

**Just run this one command:**

```bash
python3 run_everything.py
```

It does everything automatically!

---

## 📊 What You'll Get

After running, check these folders:

### `plots/` - Training Visualizations
- Monthly distance and training volume
- Pace progression over time
- Weekly running patterns
- Elevation analysis
- Model accuracy charts

### `models/` - Trained ML Models
- Models for 5K, 10K, Half Marathon, Marathon
- Automatically saved for future use

### Terminal Output
- Your predicted race times for each distance
- Model accuracy (how confident the predictions are)
- Training summary (recent mileage, pace, etc.)

---

## 🔄 Updating Predictions

After you run more races or add more training:

```bash
# Fetch latest Strava data
python3 fetch_strava_data_rest.py

# Re-run the analysis and predictions
python3 run_everything.py
```

---

## 💡 Quick Commands

| What You Want | Command |
|---------------|---------|
| **Run everything** | `python3 run_everything.py` |
| **Just see predictions** | `python3 predict_race_time.py --all` |
| **Fetch new Strava data** | `python3 fetch_strava_data_rest.py` |
| **Just analyze training** | `python3 analyze_training.py` |
| **Predict specific distance** | `python3 predict_race_time.py --distance "5K"` |

---

## ❓ FAQ

**Q: How accurate are the predictions?**
A: The models show their accuracy (MAE = Mean Absolute Error). For example, "±2 minutes" means predictions are typically within 2 minutes of actual race times.

**Q: Do I need to re-authorize Strava often?**
A: No! Once you authorize, the refresh token works indefinitely.

**Q: How many races do I need?**
A: At least 5 races at each distance for reliable predictions. More races = better predictions!

**Q: What if I don't have enough race data?**
A: The system will skip that distance and tell you. Focus on distances you race more often.

**Q: Can I use this for other sports?**
A: Currently only running is supported, but the code could be adapted for cycling or other endurance sports.

---

## 🎉 That's It!

The simplest workflow:

1. **First time:** `pip install -r requirements.txt`
2. **Any time:** `python3 run_everything.py`
3. **View results** in the `plots/` folder and terminal output

Happy running! 🏃‍♂️💨
