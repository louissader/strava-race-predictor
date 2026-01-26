# Strava Race Time Predictor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

**ML-powered race time prediction system that transforms training data into accurate race predictions**

[Features](#features) • [Results](#results) • [Tech Stack](#tech-stack) • [Quick Start](#quick-start)

</div>

---

## Overview

A machine learning application that predicts running race times (5K, 10K, Half Marathon, Marathon) based on personal Strava training data. Built to demonstrate end-to-end ML pipeline development, from data engineering to production UI.

---

## Results

| Metric | Value |
|--------|-------|
| **Prediction Accuracy** | <5% error across 1,000+ runs |
| **Model Improvement** | 23% accuracy gain over baseline |
| **Features Engineered** | 15+ metrics from Strava API |
| **Time Saved** | 2+ hours manual analysis → 30 seconds |

---

## Features

- **Race Time Predictions** - ML models predict 5K, 10K, Half Marathon, and Marathon times
- **Interactive Timeline** - View how predicted times evolved over training period
- **GPS Heatmap** - Visualize all runs with pace-colored routes using Leaflet
- **Training Analytics** - Deep insights into running patterns and metrics
- **Training Dashboard** - Overview of running statistics and trends

---

## Tech Stack

### Machine Learning & Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **Flask** | REST API server |
| **scikit-learn** | ML model training & prediction |
| **pandas** | Data processing & feature engineering |
| **numpy** | Numerical computations |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **Leaflet** | Interactive GPS maps |
| **Recharts** | Data visualizations |
| **Framer Motion** | Animations |
| **React Router** | Client-side routing |

### Data Pipeline
| Technology | Purpose |
|------------|---------|
| **Strava API** | Training data source |
| **Feature Engineering** | 15+ custom metrics |
| **Regression Models** | Time predictions |

---

## Project Structure

```
strava-race-predictor/
├── src/
│   ├── backend/              # Python Flask API
│   │   ├── api.py            # REST endpoints
│   │   ├── models/           # ML models and training
│   │   ├── services/         # Strava API integration
│   │   └── utils/            # Data processing utilities
│   └── frontend/             # React application
│       ├── components/       # UI components
│       └── pages/            # Route pages
├── data/
│   ├── cache/                # Cached API responses
│   ├── raw/                  # Raw Strava data
│   └── processed/            # Processed datasets
├── models/                   # Trained ML models
├── config/                   # Configuration files
└── docs/                     # Documentation
```

---

## Quick Start

### 1. Setup Environment

```bash
# Clone repository
git clone https://github.com/louissader/strava-race-predictor.git
cd strava-race-predictor

# Install Python dependencies
pip install -r config/requirements.txt

# Install frontend dependencies
cd src/frontend && npm install && cd ../..
```

### 2. Configure Strava API

```bash
cp config/.env.example .env
# Edit .env with your Strava API credentials
```

### 3. Start the Application

```bash
# Terminal 1: Start API server
./start_api.sh

# Terminal 2: Start React frontend
./start_frontend.sh
```

Access at `http://localhost:3000`

---

## Skills Demonstrated

| Category | Skills |
|----------|--------|
| **Machine Learning** | Feature engineering, regression modeling, model evaluation |
| **Data Engineering** | API integration, data pipelines, ETL processing |
| **Backend Development** | Python, Flask, REST API design |
| **Frontend Development** | React, data visualization, interactive maps |
| **Full-Stack Integration** | End-to-end application development |

---

## Author

**Louis Sader** - Full-Stack Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/louissader)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/louissader)

---

## License

MIT License
