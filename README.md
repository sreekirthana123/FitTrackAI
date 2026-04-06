# 🏋️ FitTrack AI
### AI-Powered Personalized Health & Fitness Tracking Platform

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-green?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 🌟 About

FitTrack AI is a full-stack web application that tracks a user's physical health, mental wellbeing, diet, sleep, and work performance. It uses Machine Learning models to deliver **personalized predictions**, **actionable recommendations**, and **friendly health insights** — treating every user as an individual with unique health patterns, goals, and lifestyle.

> Built independently as a personal project following the **Spiral Model** of software development.

---

## ✨ Features

- 👤 **User Profiles** — Register with personal health details and fitness goals
- 🏃 **Workout Logging** — Track exercise type, duration, calories, and intensity
- 🍽️ **Meal Logging** — Log daily meals, calories, and water intake
- 😴 **Sleep Tracking** — Monitor sleep hours and quality
- ❤️ **Health Vitals** — Track weight, heart rate, and steps
- 🧠 **Mental Health Logging** — Record mood, stress, energy, and productivity
- 📊 **Dashboard API** — Fetch last 7 days of all health data in one call
- 🤖 **ML Predictions** — Predict weight trend and sleep risk based on user patterns
- 💬 **Friendly Insights** — Personalized, human-readable health insight messages

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + Flask |
| Database | MySQL 8.0 |
| ML Models | scikit-learn (Random Forest, Logistic Regression) |
| API Testing | Postman |
| Version Control | Git + GitHub |
| ML Environment | Google Colab |

---

## 📁 Project Structure

```
FitTrackAI/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── weight_model.pkl    # Trained weight prediction model
│   ├── sleep_model.pkl     # Trained sleep risk classifier
│   └── scaler.pkl          # StandardScaler for ML preprocessing
└── README.md
```

---

## 🗄️ Database Schema

The MySQL database `fitness_db` contains 6 tables:

| Table | Purpose |
|-------|---------|
| `users` | User profiles and goals |
| `workouts` | Daily workout logs |
| `meals` | Daily meal and nutrition logs |
| `health_logs` | Daily vitals (weight, sleep, steps, heart rate) |
| `mental_logs` | Mood, stress, energy, and productivity logs |
| `predictions` | ML model output and insight text |

---

## 🤖 ML Models

### Weight Prediction
- **Algorithm:** Random Forest Regressor
- **Input:** Sleep hours, calories, steps, heart rate, mood, stress, productivity
- **Output:** Predicted weight for tomorrow (kg)

### Sleep Risk Classification
- **Algorithm:** Logistic Regression
- **Input:** Sleep hours, stress, mood, productivity, heart rate
- **Output:** At Risk ⚠️ or No Risk ✅

### Insight Card Example
```
⚠️ You only slept 5.0 hours last night and your stress is high.
Based on your patterns, your predicted weight tomorrow is 54.9 kg.
Try to sleep early tonight and take short breaks during work!
```

---

## 🚀 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/register` | Register a new user |
| POST | `/log/workout` | Log a workout session |
| POST | `/log/meal` | Log a meal |
| POST | `/log/health` | Log health vitals |
| POST | `/log/mental` | Log mood and productivity |
| GET | `/dashboard/<user_id>` | Fetch last 7 days of all data |
| GET | `/predict/<user_id>` | Get ML predictions and insight |
| GET | `/test-db` | Test database connection |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.13+
- MySQL 8.0
- Git

### 1. Clone the repository
```bash
git clone https://github.com/sreekirthana123/FitTrackAI.git
cd FitTrackAI
```

### 2. Install dependencies
```bash
pip install flask flask-cors sqlalchemy mysql-connector-python scikit-learn pandas numpy joblib
```

### 3. Set up MySQL database
```sql
CREATE DATABASE fitness_db;
USE fitness_db;
-- Run the table creation scripts from the backend/app.py setup
```

### 4. Run the Flask server
```bash
cd backend
python app.py
```

### 5. Test the API
Open Postman and send a GET request to:
```
http://127.0.0.1:5000/
```

---

## 🗺️ Development Roadmap (Spiral Model)

- [x] Phase 1 — Software Requirements Document (SRD)
- [x] Phase 2 — Environment Setup + MySQL Database
- [x] Phase 3 — Flask Backend API
- [x] Phase 4 — ML Model (Google Colab + Flask integration)
- [ ] Phase 5 — Frontend Dashboard (HTML/CSS/JS → React)
- [ ] Phase 6 — Connect Frontend to Backend
- [ ] Phase 7 — Polish, Testing & Deployment

---

## 👩‍💻 Author

**V Sree Kirthana**
B.Tech CSE — JBIET, Hyderabad
2nd Year | AI/ML Engineer in process
sreekeerthana64@gmail.com

[![GitHub](https://img.shields.io/badge/GitHub-sreekirthana123-black?logo=github)](https://github.com/sreekirthana123)

---

> *Built with curiosity, caffeine, and a lot of debugging* ☕🔥
