# 🌐 **START HERE** - Web Application Guide

## ⚡ The Fastest Way to Use This Project

### Just Run This:
```bash
./run_web_app.sh
```

Then open: **http://localhost:5001** in your browser

That's it! 🎉

---

## 📱 What You'll See

### 🏠 **Dashboard** (Main Page)
- Your overall running stats (total runs, distance, time, pace)
- Race time predictions for 5K, 10K, Half Marathon, Marathon
- Complete race history table
- Beautiful cards with your personal bests

### 📊 **Analytics** Page
- Monthly training volume charts
- Pace distribution histogram
- Weekly running patterns (which days you run most)
- Hour-of-day analysis (when you prefer to run)
- Interactive Plotly charts (zoom, pan, hover!)

### ⏰ **Timeline** Page
- See how your predicted race times evolved over your entire career
- Interactive: click different distances (5K, 10K, Half, Marathon)
- Shows training context (weekly/monthly mileage)
- Watch your fitness progress over time!

---

## 🎯 Key Features

✅ **No Terminal Needed** - Point and click interface
✅ **Beautiful Design** - Modern purple gradient theme
✅ **Interactive Charts** - Zoom, pan, hover for details
✅ **Responsive** - Works on desktop, tablet, mobile
✅ **Real-Time** - Data updates automatically
✅ **Historical Analysis** - See predictions at any point in time

---

## 🔄 Updating Your Data

When you have new runs or races:

```bash
# 1. Fetch latest from Strava
python3 fetch_strava_data_rest.py

# 2. Retrain models (if you have new races)
python3 train_model.py

# 3. Restart the web app
./run_web_app.sh
```

---

## 💡 Cool Things To Try

1. **Timeline Feature**: Go to Timeline page, select 5K, watch how your fitness evolved!
2. **Analytics**: Check what days you run most - any patterns?
3. **Hour Analysis**: When do you prefer to run? Morning or evening?
4. **Pace Distribution**: See the spread of your paces
5. **Race History**: Sort through all your races

---

## 🆘 Troubleshooting

### Port 5000/5001 already in use?
Edit `app.py`, line 263:
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Change to 5002 or any free port
```

### Charts not loading?
- Make sure you have internet (needs CDN for chart libraries)
- Try refreshing the page (Ctrl/Cmd + R)
- Check browser console for errors (F12)

### No data showing?
Make sure you ran:
```bash
python3 fetch_strava_data_rest.py
python3 train_model.py
```

---

## 🚀 Advanced: Access from Phone/Tablet

1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```

2. On your phone/tablet, open browser to:
   ```
   http://YOUR_COMPUTER_IP:5001
   ```

3. Make sure both devices are on the same WiFi network!

---

## 📸 What It Looks Like

- **Purple gradient header** with navigation
- **Colorful stat cards** for quick overview
- **Interactive charts** that respond to mouse/touch
- **Clean, modern design** throughout
- **Smooth animations** on hover

---

## 🎨 Pages In Detail

### Dashboard (`/`)
- 4 quick stat cards at top
- Race predictions in colored boxes
- Full race history table at bottom
- Everything loads dynamically via API

### Analytics (`/analytics`)
- Monthly volume (bar + line chart)
- Pace histogram with mean/median lines
- Day of week bar chart
- Hour of day bar chart
- 3 gradient stat cards at bottom

### Timeline (`/timeline`)
- 4 distance buttons (5K, 10K, Half, Marathon)
- Interactive chart showing prediction evolution
- Training volume overlay
- Hover to see exact values at any date

---

## 🛠️ How It Works

The web app:
1. Loads your data from `data/strava_activities.csv`
2. Loads trained models from `models/` directory
3. Serves interactive pages via Flask
4. Creates charts client-side with Plotly
5. All data fetched via REST API endpoints

---

## 🌟 Why This Is Better Than Terminal

| Terminal | Web App |
|----------|---------|
| Text output | Beautiful visualizations |
| Static | Interactive charts |
| One view at a time | Multiple pages to explore |
| Terminal only | Works on any device |
| Numbers | Graphs + Numbers |
| Black and white | Colorful UI |

---

## 🎯 Perfect For

- ✅ Personal use - track your own progress
- ✅ Sharing with training partners
- ✅ Portfolio project showcase
- ✅ Understanding your training patterns
- ✅ Planning race strategies

---

**Ready to see your running data come to life?**

```bash
./run_web_app.sh
```

**Then visit: http://localhost:5001**

Enjoy! 🏃‍♂️💨
