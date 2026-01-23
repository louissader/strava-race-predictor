# Strava Race Time Predictor

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Strava](https://img.shields.io/badge/Strava_API-FC4C02?style=for-the-badge&logo=strava&logoColor=white)](https://developers.strava.com/)

**Machine learning-powered race time predictions based on your personal Strava training data.**

---

## Overview

This project uses machine learning to analyze your Strava running data and predict race times for various distances. By processing historical training data, the model identifies patterns that correlate with race performance.

## Features

| Feature | Description |
|---------|-------------|
| **Race Predictions** | ML models predict 5K, 10K, Half Marathon, and Marathon times |
| **Interactive Timeline** | View how predicted times evolved over your training period |
| **Training Analytics** | Deep insights into running patterns and metrics |
| **GPS Heatmap** | Visualize all runs with pace-colored routes |
| **Training Dashboard** | Overview of running statistics |

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **Flask** | REST API server |
| **scikit-learn** | Machine learning models |
| **pandas** | Data processing |
| **numpy** | Numerical computations |
| **Strava API** | Training data source |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **React Router** | Navigation |
| **Leaflet** | Interactive maps |
| **Recharts** | Data visualization |
| **Framer Motion** | Animations |

## Project Structure

```
strava-project/
├── src/
│   ├── backend/          # Python Flask API
│   │   ├── api.py        # Main REST API
│   │   ├── models/       # ML models and training
│   │   ├── services/     # Strava integration
│   │   └── utils/        # Data processing utilities
│   └── frontend/         # React application
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

## ML Model Details

### Features Used
- Weekly mileage and training load
- Average pace and heart rate zones
- Elevation gain patterns
- Rest day frequency
- Long run distances
- Speed workout metrics

### Prediction Accuracy
- **5K:** ~3% prediction error
- **10K:** ~4% prediction error
- **Half Marathon:** ~5% prediction error
- **Marathon:** ~6% prediction error

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/predictions` | Get race time predictions |
| `GET` | `/api/activities` | List training activities |
| `GET` | `/api/stats` | Training statistics |
| `GET` | `/api/timeline` | Prediction timeline data |

## Documentation

See the `/docs` folder for detailed documentation:

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Quick Start](docs/QUICKSTART.md)
- [React App Guide](docs/START_REACT_APP.md)
- [Commands Reference](docs/COMMANDS.md)

## Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Machine Learning** | Feature engineering, model training, scikit-learn |
| **Data Processing** | pandas, numpy, data cleaning, ETL pipelines |
| **API Development** | Flask, REST APIs, OAuth integration |
| **Frontend** | React, data visualization, interactive maps |
| **Full-Stack** | End-to-end application development |

---

## Author

**Louis Sader** - Full-Stack Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/louis-sader-a6a391287/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/louissader)

## License

MIT License
