# Project Structure

This document describes the professional folder structure of the Strava Race Time Predictor.

## Directory Layout

```
strava-race-predictor/
├── src/                          # Source code
│   ├── backend/                  # Python Flask API
│   │   ├── __init__.py
│   │   ├── api.py               # Main REST API server
│   │   ├── app_legacy.py        # Legacy Flask app (archived)
│   │   ├── models/              # ML models and training
│   │   │   ├── __init__.py
│   │   │   ├── train_model.py   # Model training scripts
│   │   │   ├── predict_race_time.py
│   │   │   └── analyze_training.py
│   │   ├── services/            # External service integrations
│   │   │   ├── __init__.py
│   │   │   ├── strava_auth.py   # Strava OAuth
│   │   │   ├── fetch_strava_data.py
│   │   │   └── reauthorize_strava.py
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       ├── data_preprocessing.py
│   │       ├── show_predictions.py
│   │       └── quickstart.py
│   ├── frontend/                # React application
│   │   ├── src/
│   │   │   ├── pages/          # React pages
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Timeline.jsx
│   │   │   │   ├── Analytics.jsx
│   │   │   │   └── Heatmap.jsx
│   │   │   ├── utils/          # Frontend utilities
│   │   │   │   └── formatters.js
│   │   │   ├── App.jsx
│   │   │   ├── App.css
│   │   │   └── main.jsx
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── web_app_legacy/          # Legacy Flask web app (archived)
│       └── templates/
├── data/                        # Data files
│   ├── cache/                   # Cached API responses
│   │   └── gps_routes_cache.json (46MB)
│   ├── raw/                     # Raw data from Strava
│   │   └── strava_activities_raw.json
│   └── processed/               # Processed datasets
│       ├── strava_activities.csv
│       └── race_features.csv
├── models/                      # Trained ML models
│   ├── 5K_model.joblib
│   └── 10K_model.joblib
├── plots/                       # Generated visualizations
│   ├── feature_importance_5K.png
│   ├── predictions_5K.png
│   ├── predictions_10K.png
│   ├── model_comparison_5K.png
│   └── model_comparison_10K.png
├── docs/                        # Documentation
│   ├── GETTING_STARTED.md
│   ├── QUICKSTART.md
│   ├── START_REACT_APP.md
│   ├── COMMANDS.md
│   └── ... (other docs)
├── scripts/                     # Shell scripts
│   ├── setup.sh
│   ├── run_react_app.sh
│   ├── run_web_app.sh
│   └── run_everything.py
├── config/                      # Configuration files
│   ├── requirements.txt
│   └── .env.example
├── tests/                       # Test files (future)
├── README.md                    # Main readme
├── setup.py                     # Python package setup
├── .gitignore
├── start_api.sh                # Quick start API
└── start_frontend.sh           # Quick start frontend
```

## Key Design Decisions

### Modular Backend Structure

The backend is organized into clear modules:

- **models/**: Machine learning training, prediction, and analysis
- **services/**: External API integrations (Strava)
- **utils/**: Data processing and utility functions

This allows for:
- Easy navigation and maintenance
- Clear separation of concerns
- Simple imports within modules

### Data Organization

Data is categorized by purpose:

- **cache/**: Temporary cached data (gitignored)
- **raw/**: Original data from APIs
- **processed/**: Cleaned and processed datasets

### Frontend Separation

The React frontend lives in `src/frontend/` with:
- Clean separation from backend
- Standard React/Vite structure
- Organized pages and utilities

### Documentation Consolidation

All markdown docs are in `docs/` for easy reference.

### Scripts Organization

Automation scripts in `scripts/` folder, with convenience launchers at root.

## Import Conventions

### Backend Imports

From within `src/backend/`, use relative imports:

```python
# From api.py
from utils.data_preprocessing import load_activities
from models.train_model import train_model
from services.strava_auth import get_client
```

### Running from Root

Use the convenience scripts:

```bash
./start_api.sh       # Starts backend API
./start_frontend.sh  # Starts React app
```

## Benefits of This Structure

1. **Professional**: Follows Python and React best practices
2. **Scalable**: Easy to add new modules or features
3. **Maintainable**: Clear organization makes code easy to find
4. **Collaborative**: New developers can quickly understand structure
5. **Clean**: Separates source, data, docs, config, and output
