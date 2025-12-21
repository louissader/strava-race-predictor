# 🚀 Strava Race Predictor - React Edition

## Modern Full-Stack ML Application

**Tech Stack:**
- **Frontend:** React + Vite, Framer Motion, React Router, Recharts, Leaflet
- **Backend:** Flask REST API
- **ML:** scikit-learn, pandas, numpy
- **Styling:** Custom CSS (cyberpunk/neon theme)

---

## ⚡ Quick Start

```bash
./run_react_app.sh
```

Then open: **http://localhost:5173**

---

## 🎨 Features

### ✨ Unique Design
- **NOT generic AI look** - Custom cyberpunk/neon theme
- Dark background with cyan/pink/yellow accents
- Smooth animations with Framer Motion
- Custom fonts (Space Grotesk + JetBrains Mono)
- Glowing effects and gradient borders

### 🏠 Dashboard
- **Hall of Fame Section**: Your most impressive runs
  - 🏅 Longest runs
  - ⚡ Fastest paces
  - 🏔️ Biggest climbs
  - 🎯 Most consistent efforts
- Quick stats cards with icons
- Race predictions for all distances

### 🗺️ Heatmap Page (NEW!)
- Interactive Leaflet map
- Shows where you run most
- Dark theme map tiles
- Cyan/neon markers

### 📊 Analytics (Coming Soon)
- Custom Recharts visualizations
- Training trends over time
- Pace analysis
- Weekly/monthly patterns

### ⏰ Timeline (Coming Soon)
- Fitness progression over career
- Prediction evolution
- Training context

---

## 🛠️ Manual Setup

### Backend:
```bash
# Install Python dependencies
pip install flask flask-cors pandas numpy scikit-learn joblib python-dotenv requests

# Start API server
python3 api.py
```

### Frontend:
```bash
cd frontend

# Install Node dependencies
npm install

# Start dev server
npm run dev
```

---

## 📁 Project Structure

```
Strava Project/
├── api.py                    # Flask REST API (port 5001)
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React app
│   │   ├── App.css          # Custom styling
│   │   └── pages/
│   │       ├── Dashboard.jsx    # Home page with impressive activities
│   │       ├── Heatmap.jsx      # Map visualization
│   │       ├── Analytics.jsx    # Training analytics
│   │       └── Timeline.jsx     # Fitness timeline
│   └── package.json
├── data/                    # Your Strava data
├── models/                  # Trained ML models
└── run_react_app.sh        # Launch script
```

---

## 🎯 What Makes This Different

### 1. **Unique Design**
- Not Tailwind templates or AI-generated
- Custom color scheme (cyan #00f5d4, pink #ff6b9d, yellow #ffd23f)
- Cyberpunk/neon aesthetic
- Space Grotesk font (modern, clean)
- Custom animations and effects

### 2. **Impressive Activities Showcase**
- Automatically finds your best runs
- Categorizes by type (longest, fastest, highest elevation, most consistent)
- Shows them prominently on homepage
- Color-coded cards with gradients

### 3. **Interactive Maps**
- Leaflet integration for heatmap
- Dark theme map tiles
- Shows running density
- Can be extended with real GPS data from Strava API

### 4. **Modern React Architecture**
- React Router for navigation
- Framer Motion for animations
- Axios for API calls
- Component-based structure

---

## 🚀 Deployment

### Build for Production:
```bash
cd frontend
npm run build
```

### Serve Static Files:
Update `api.py` to serve React build:
```python
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend/dist', 'index.html')
```

---

## 🎨 Customization

### Change Colors:
Edit `frontend/src/App.css`:
```css
:root {
  --accent-primary: #00f5d4;    /* Cyan */
  --accent-secondary: #ff6b9d;  /* Pink */
  --accent-tertiary: #ffd23f;   /* Yellow */
}
```

### Add More Pages:
1. Create new component in `frontend/src/pages/`
2. Add route in `App.jsx`
3. Add nav link in `NavBar`

---

## 💡 Future Enhancements

- [ ] Real GPS polylines from Strava API
- [ ] Interactive training calendar
- [ ] Social features (compare with friends)
- [ ] Training plan recommendations
- [ ] Custom race predictions by terrain
- [ ] Export reports as PDF
- [ ] Mobile app with React Native

---

## 🎓 For Your Portfolio / Jerry Application

**This project shows:**
- ✅ Full-stack development (React + Flask)
- ✅ Modern frontend (hooks, routing, state management)
- ✅ RESTful API design
- ✅ Machine learning integration
- ✅ Data visualization
- ✅ Custom UI/UX design (not templates!)
- ✅ Real-world problem solving

**Talking Points:**
- "Built custom ML pipeline + modern React frontend"
- "Designed unique cyberpunk UI (no templates)"
- "Integrated Leaflet for interactive mapping"
- "Created Hall of Fame feature showcasing impressive runs"
- "Full REST API with Flask + CORS"

---

**Enjoy your beautiful, modern running analytics dashboard!** 🏃‍♂️✨
