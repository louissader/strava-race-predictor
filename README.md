# Strava Race Time Predictor

Machine learning-powered race time predictions based on your Strava training data.

## Features

- **Race Time Predictions**: ML models predict your 5K, 10K, Half Marathon, and Marathon times
- **Interactive Timeline**: View how your predicted times evolved over your training period
- **Training Analytics**: Deep insights into your running patterns and metrics
- **GPS Heatmap**: Visualize all your runs with pace-colored routes
- **Training Dashboard**: Overview of your running statistics

## Project Structure

```
strava-project/
├── src/
│   ├── backend/          # Python Flask API
│   │   ├── api.py        # Main REST API
│   │   ├── models/       # ML models and training
│   │   ├── services/     # Strava integration
│   │   └── utils/        # Data processing utilities
│   ├── frontend/         # React application
│   └── web_app_legacy/   # Legacy Flask web app
├── data/
│   ├── cache/           # Cached API responses
│   ├── raw/             # Raw Strava data
│   └── processed/       # Processed datasets
├── models/              # Trained ML models
├── plots/               # Visualization outputs
├── docs/                # Documentation
├── scripts/             # Utility scripts
└── config/              # Configuration files
```

## Quick Start

### 1. Setup Environment

```bash
# Install Python dependencies
pip install -r config/requirements.txt

# Install frontend dependencies
cd src/frontend
npm install
cd ../..
```

### 2. Configure Strava API

Copy `.env.example` to `.env` and add your Strava API credentials:

```bash
cp config/.env.example .env
# Edit .env with your credentials
```

### 3. Start the Application

```bash
# Terminal 1: Start API server
./start_api.sh

# Terminal 2: Start React frontend
./start_frontend.sh
```

The app will be available at `http://localhost:3000`

## Documentation

See the `/docs` folder for detailed documentation:

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Quick Start](docs/QUICKSTART.md)
- [React App Guide](docs/START_REACT_APP.md)
- [Commands Reference](docs/COMMANDS.md)

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (REST API)
- scikit-learn (ML models)
- pandas, numpy (data processing)

**Frontend:**
- React 18
- React Router
- Leaflet (maps)
- Recharts (visualizations)
- Framer Motion (animations)

## License

MIT
