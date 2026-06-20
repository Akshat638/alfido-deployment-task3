"""
test_api.py — Example API Requests & Responses
Alfido Tech Internship Task 3 | Akshat Rathore

Run this AFTER starting the Flask server:
    python app.py

Then in another terminal:
    python test_api.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def pretty(title, response):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")
    print(f"  Status Code : {response.status_code}")
    print(f"  Response    :")
    print(json.dumps(response.json(), indent=4))

# ── 1. Health Check ───────────────────────────────────────
r = requests.get(f"{BASE_URL}/health")
pretty("GET /health — API Health Check", r)

# ── 2. Feature List ───────────────────────────────────────
r = requests.get(f"{BASE_URL}/features")
pretty("GET /features — List Required Fields", r)

# ── 3. Single Prediction — HIGH RISK customer ────────────
high_risk_customer = {
    "gender"          : "Male",
    "SeniorCitizen"   : 0,
    "Partner"         : "No",
    "Dependents"      : "No",
    "tenure"          : 2,
    "PhoneService"    : "Yes",
    "MultipleLines"   : "No",
    "InternetService" : "Fiber optic",
    "OnlineSecurity"  : "No",
    "TechSupport"     : "No",
    "Contract"        : "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod"   : "Electronic check",
    "MonthlyCharges"  : 95.5,
    "TotalCharges"    : 191.0
}
r = requests.post(f"{BASE_URL}/predict", json=high_risk_customer)
pretty("POST /predict — HIGH RISK Customer (Month-to-month, 2 months tenure)", r)

# ── 4. Single Prediction — LOW RISK customer ─────────────
low_risk_customer = {
    "gender"          : "Female",
    "SeniorCitizen"   : 0,
    "Partner"         : "Yes",
    "Dependents"      : "Yes",
    "tenure"          : 60,
    "PhoneService"    : "Yes",
    "MultipleLines"   : "Yes",
    "InternetService" : "DSL",
    "OnlineSecurity"  : "Yes",
    "TechSupport"     : "Yes",
    "Contract"        : "Two year",
    "PaperlessBilling": "No",
    "PaymentMethod"   : "Bank transfer",
    "MonthlyCharges"  : 45.0,
    "TotalCharges"    : 2700.0
}
r = requests.post(f"{BASE_URL}/predict", json=low_risk_customer)
pretty("POST /predict — LOW RISK Customer (Two year contract, 60 months tenure)", r)

# ── 5. Batch Prediction ───────────────────────────────────
batch_data = {
    "customers": [high_risk_customer, low_risk_customer, {
        "gender"          : "Male",
        "SeniorCitizen"   : 1,
        "Partner"         : "No",
        "Dependents"      : "No",
        "tenure"          : 5,
        "PhoneService"    : "Yes",
        "MultipleLines"   : "No",
        "InternetService" : "Fiber optic",
        "OnlineSecurity"  : "No",
        "TechSupport"     : "No",
        "Contract"        : "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod"   : "Electronic check",
        "MonthlyCharges"  : 88.0,
        "TotalCharges"    : 440.0
    }]
}
r = requests.post(f"{BASE_URL}/predict_batch", json=batch_data)
pretty("POST /predict_batch — 3 Customers at Once", r)

print("\n✅ All API tests completed successfully!")
print("📌 curl equivalent example:")
print("""
curl -X POST http://127.0.0.1:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "gender": "Male", "SeniorCitizen": 0, "Partner": "No",
    "Dependents": "No", "tenure": 2, "PhoneService": "Yes",
    "MultipleLines": "No", "InternetService": "Fiber optic",
    "OnlineSecurity": "No", "TechSupport": "No",
    "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 95.5, "TotalCharges": 191.0
  }'
""")
