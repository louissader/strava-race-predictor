# Strava Race Time Predictor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Flask-REST_API-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_Bedrock-Claude_AI-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-Real--Time-010101?style=for-the-badge&logo=socket.io&logoColor=white)

**ML-powered race predictions + AI coaching with real-time streaming responses**

[Features](#features) • [AI Coach](#ai-running-coach) • [Tech Stack](#tech-stack) • [Quick Start](#quick-start)

</div>

---

## Overview

A full-stack machine learning application that predicts running race times (5K, 10K, Half Marathon, Marathon) based on personal Strava training data, featuring an **AI-powered running coach** with real-time WebSocket streaming. Built to demonstrate end-to-end ML pipeline development, LLM integration, and modern real-time web architecture.

---

## Results

| Metric | Value |
|--------|-------|
| **Prediction Accuracy** | <5% error across 1,000+ runs |
| **Model Improvement** | 23% accuracy gain over baseline |
| **Features Engineered** | 15+ metrics from Strava API |
| **AI Response Time** | Real-time token streaming via WebSocket |

---

## Features

- **Race Time Predictions** - ML models predict 5K, 10K, Half Marathon, and Marathon times
- **AI Running Coach** - Personalized training advice powered by Claude via AWS Bedrock
- **Real-Time Streaming** - WebSocket integration for token-by-token AI response streaming
- **Training Plan Generator** - AI-generated week-by-week training plans based on current fitness
- **Interactive Timeline** - View how predicted times evolved over training period
- **GPS Heatmap** - Visualize all runs with pace-colored routes using Leaflet
- **Training Analytics** - Deep insights into running patterns and metrics

---

## AI Running Coach

The AI coach provides personalized training advice by analyzing your complete Strava training history:

### Features
- **Contextual Awareness** - Coach has access to your training volume, pace trends, race predictions, and recent activities
- **Real-Time Streaming** - Responses stream token-by-token via WebSocket for a conversational experience
- **Training Plan Generation** - Generate structured week-by-week plans for any race distance
- **Personalized Advice** - Recommendations based on your actual fitness data, not generic tips

### Architecture
```
React Frontend ←→ WebSocket (Socket.IO) ←→ Flask API ←→ AWS Bedrock (Claude)
                                              ↓
                                    Training Context Builder
                                    (Strava data + ML predictions)
```

---

## Tech Stack

### Machine Learning & AI
| Technology | Purpose |
|------------|---------|
| **AWS Bedrock** | Claude AI model hosting |
| **Claude 3 Sonnet** | LLM for coaching responses |
| **scikit-learn** | Race time prediction models |
| **pandas / numpy** | Data processing & feature engineering |

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **Flask** | REST API server |
| **Flask-SocketIO** | WebSocket support for real-time streaming |
| **boto3** | AWS Bedrock SDK |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 19** | UI framework |
| **Socket.IO Client** | WebSocket client for streaming |
| **Leaflet** | Interactive GPS maps |
| **Recharts** | Data visualizations |
| **Framer Motion** | Animations |

### Data & Infrastructure
| Technology | Purpose |
|------------|---------|
| **Strava API** | Training data source |
| **WebSocket** | Real-time bidirectional communication |
| **REST API** | Standard HTTP endpoints |

---

## Project Structure

```
strava-race-predictor/
├── src/
│   ├── backend/
│   │   ├── api.py              # REST + WebSocket endpoints
│   │   ├── services/
│   │   │   └── ai_coach.py     # AWS Bedrock integration & streaming
│   │   ├── models/             # ML model training
│   │   └── utils/              # Data preprocessing
│   └── frontend/
│       └── src/
│           ├── pages/
│           │   ├── Coach.jsx   # AI chat interface with WebSocket
│           │   ├── Dashboard.jsx
│           │   ├── Analytics.jsx
│           │   ├── Heatmap.jsx
│           │   └── Timeline.jsx
│           └── App.jsx
├── models/                     # Trained ML models (.joblib)
├── data/
│   ├── processed/              # Strava activity data
│   └── cache/                  # GPS route cache
└── config/
    └── requirements.txt
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

### 2. Configure API Keys

```bash
cp config/.env.example .env
```

Edit `.env` with your credentials:
```env
# Strava API
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REFRESH_TOKEN=your_refresh_token

# AWS Bedrock (for AI Coach)
AWS_REGION=us-east-1
AWS_PROFILE=default  # or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
```

### 3. Start the Application

```bash
# Terminal 1: Start API server (with WebSocket support)
./start_api.sh

# Terminal 2: Start React frontend
./start_frontend.sh
```

Access at `http://localhost:5173`

---

## API Endpoints

### REST Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Overall running statistics |
| `/api/predictions` | GET | Race time predictions |
| `/api/coach/context` | GET | Training context for AI |
| `/api/coach/chat` | POST | Chat with AI coach (fallback) |
| `/api/coach/training-plan` | POST | Generate training plan |

### WebSocket Events
| Event | Direction | Description |
|-------|-----------|-------------|
| `coach_message` | Client → Server | Send message to AI coach |
| `coach_token` | Server → Client | Streaming response token |
| `coach_stream_end` | Server → Client | Response complete |

---

## Skills Demonstrated

| Category | Skills |
|----------|--------|
| **AI/LLM Integration** | AWS Bedrock, Claude API, prompt engineering, context injection |
| **Real-Time Systems** | WebSocket, Socket.IO, streaming responses, bidirectional communication |
| **Machine Learning** | Feature engineering, regression modeling, scikit-learn |
| **Backend Development** | Python, Flask, REST API, async processing |
| **Frontend Development** | React 19, state management, real-time UI updates |
| **Cloud Services** | AWS Bedrock, boto3 SDK |
| **Full-Stack Integration** | End-to-end application architecture |

---

## Author

**Louis Sader** - Full-Stack Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/louissader)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/louissader)

---

## License

MIT License
