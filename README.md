# Task 3 — Model Deployment: API & Containerisation
## Customer Churn Prediction REST API with Flask + Docker
**Alfido Tech Data Science Internship | Akshat Rathore | June 2026**

---

## 📌 Problem Statement
Wrap the trained Random Forest churn prediction model (from Task 1) into a production-ready REST API using Flask, and containerise it with Docker for easy deployment anywhere.

## 🏗️ Architecture
```
Client (curl / Python / Browser)
        │
        ▼ HTTP Request (JSON)
   ┌─────────────────────┐
   │    Flask API         │  ← app.py running on port 5000
   │  ┌───────────────┐  │
   │  │ GET  /health  │  │
   │  │ GET  /features│  │
   │  │ POST /predict │  │  ← loads model.pkl + scaler.pkl + encoders.pkl
   │  │ POST /predict │  │
   │  │      _batch   │  │
   │  └───────────────┘  │
   └─────────────────────┘
        │
        ▼ Wrapped in Docker Container
   docker run -p 5000:5000 churn-api
```

## 📁 Project Structure
```
alfido_task3/
├── app.py                     ← Flask API (main file)
├── test_api.py                ← Test script with example requests
├── Dockerfile                 ← Container definition
├── docker-compose.yml         ← One-command deployment
├── requirements.txt           ← Exact package versions
├── README.md                  ← This file
├── model.pkl                  ← Trained Random Forest model
├── scaler.pkl                 ← StandardScaler (fitted on training data)
├── encoders.pkl               ← LabelEncoders for categorical columns
├── feature_names.pkl          ← Ordered list of feature names
└── churn_data.csv             ← Dataset used to train the model
```

## ⚙️ Option A — Run Locally (Without Docker)

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the API
```bash
python app.py
```
API will start at: **http://127.0.0.1:5000**

### Step 3: Test it
```bash
python test_api.py
```

## 🐳 Option B — Run with Docker

### Step 1: Install Docker
Download from: https://www.docker.com/products/docker-desktop

### Step 2: Build the image
```bash
docker build -t churn-api .
```

### Step 3: Run the container
```bash
docker run -p 5000:5000 churn-api
```

### OR use docker-compose (one command)
```bash
docker-compose up --build
```

API will be live at: **http://localhost:5000**

## 🔌 API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| GET    | /                 | API overview and endpoint list     |
| GET    | /health           | Health check — returns status      |
| GET    | /features         | List all required input features   |
| POST   | /predict          | Predict churn for one customer     |
| POST   | /predict_batch    | Predict churn for many customers   |

## 📤 Example Request (curl)

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "TechSupport": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.5,
    "TotalCharges": 191.0
  }'
```

## 📥 Example Response
```json
{
  "prediction": 1,
  "churn_label": "YES — Will Churn",
  "churn_probability": 0.85,
  "confidence": "85.0%",
  "risk_level": "HIGH"
}
```

## 📦 Package Versions
- flask==3.0.3
- scikit-learn==1.8.0
- pandas==3.0.2
- numpy==2.4.4
- gunicorn==23.0.0

## ✅ Deliverables
- [x] Flask REST API with 5 endpoints (`app.py`)
- [x] Dockerfile for containerisation
- [x] docker-compose.yml for one-command deployment
- [x] Example requests & responses (`test_api.py`)
- [x] curl example in README
- [x] Model artifacts saved (model.pkl, scaler.pkl, encoders.pkl)
- [x] README with full setup and run instructions
