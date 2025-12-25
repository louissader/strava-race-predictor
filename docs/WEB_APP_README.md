# 🌐 Strava Race Predictor - Web Application

## 🚀 Quick Start

### The Easiest Way to Use This Project!

```bash
# 1. Install dependencies (if you haven't already)
pip install -r requirements.txt

# 2. Run the web app
./run_web_app.sh
```

Then open your browser to: **http://localhost:5000**

---

## 📊 What You Get

### Dashboard (Home Page)
- **Overall Stats**: Total runs, distance, time, average pace
- **Race Predictions**: AI-predicted times for 5K, 10K, Half Marathon, Marathon
- **Race History**: Complete table of all your races with times and paces

### Analytics Page
- **Monthly Training Volume**: Bar chart showing distance and number of runs per month
- **Pace Distribution**: Histogram of all your paces with mean/median lines
- **Weekly Patterns**: Which days you run most
- **Hour Analysis**: What time of day you prefer to run
- **Personal Bests**: Longest run, best pace, running since date

### Timeline Page
- **Prediction Evolution**: See how your predicted race times changed throughout your career
- **Training Context**: Understand how your training volume affected predictions
- **Interactive**: Click different distances to see different timelines
- **Historical Analysis**: Watch your fitness progress over time

---

## 🎯 Features

### Interactive & Beautiful
- ✅ Modern, responsive design (works on phone, tablet, desktop)
- ✅ Real-time data visualization with Plotly charts
- ✅ Color-coded cards and statistics
- ✅ Smooth animations and transitions

### Comprehensive Analytics
- ✅ Training volume trends
- ✅ Pace distributions
- ✅ Weekly running patterns
- ✅ Time-of-day preferences
- ✅ Historical predictions timeline

### Race Predictions
- ✅ Current predictions for all distances
- ✅ Best times, average times, recent times
- ✅ Model accuracy metrics (MAE, R²)
- ✅ Number of races at each distance

---

## 🛠️ How It Works

The web app uses:
- **Flask**: Python web framework
- **Plotly**: Interactive charts and graphs
- **Tailwind CSS**: Beautiful, responsive styling
- **Chart.js**: Additional visualizations
- **Your trained ML models**: To make predictions

All the data comes from your `data/strava_activities.csv` file and your trained models in the `models/` directory.

---

## 🔄 Updating Data

When you have new Strava activities:

```bash
# 1. Fetch latest data
python3 fetch_strava_data_rest.py

# 2. Retrain models (optional, if you have new races)
python3 train_model.py

# 3. Restart the web app
./run_web_app.sh
```

The web app will automatically load the updated data!

---

## 🎨 Pages Overview

### 1. Dashboard (`/`)
Your main hub with:
- Quick stats cards
- Race predictions for all distances
- Recent race history table

### 2. Analytics (`/analytics`)
Deep dive into your training:
- Monthly volume charts
- Pace analysis
- Day/time patterns
- Personal records

### 3. Timeline (`/timeline`)
See predictions over time:
- How would you have raced at different points?
- Relationship between training and predictions
- Fitness progression visualization

---

## 💡 Tips

1. **Best Viewed On**: Desktop or tablet (charts are interactive!)
2. **Refresh Data**: Just restart the app after updating your data
3. **Explore**: Click around! All charts are interactive (zoom, pan, hover)
4. **Timeline Feature**: Shows how your fitness evolved - lower predictions = better fitness!

---

## 🔧 Troubleshooting

### "No data found"
Run: `python3 fetch_strava_data_rest.py` first

### "No trained models"
The script will train them automatically, or run: `python3 train_model.py`

### Charts not loading
- Check browser console for errors
- Make sure you have internet (for CDN libraries)
- Try refreshing the page

### Port 5000 already in use
Edit `app.py` and change `port=5000` to another port like `port=5001`

---

## 🚀 Advanced Usage

### Run on a different port:
```bash
# Edit app.py, change this line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Access from other devices on your network:
The app runs on `0.0.0.0` so you can access it from:
```
http://YOUR_COMPUTER_IP:5000
```

Find your IP:
- Mac: System Preferences → Network
- Or run: `ifconfig | grep "inet "`

---

## 📱 Screenshots

(The web app features a modern purple gradient theme with interactive charts!)

**Dashboard**: Race predictions, stats cards, race history table
**Analytics**: Beautiful Plotly charts for all your training data
**Timeline**: Interactive timeline showing fitness progression

---

## 🎓 What Makes This Special

- **No terminal needed**: Just point and click in your browser
- **Beautiful UI**: Modern design that's actually pleasant to use
- **Interactive**: Zoom, pan, hover on all charts
- **Comprehensive**: Everything from the terminal app, but way better
- **Shareable**: Can run on a server and share with training partners

---

## 🌟 Future Enhancements

Potential additions:
- Route maps with GPS heatmaps (requires additional Strava API calls)
- Export data to PDF reports
- Compare with other runners
- Training plan recommendations
- Social features (share predictions)

---

**Enjoy your beautiful, interactive running analytics dashboard!** 🏃‍♂️💨
