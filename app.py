"""
Alfido Tech Internship — Task 3
Flask API for Customer Churn Prediction
Author: Akshat Rathore
"""

from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# ── Load model artifacts on startup ──────────────────────
model         = pickle.load(open("model.pkl",         "rb"))
scaler        = pickle.load(open("scaler.pkl",        "rb"))
encoders      = pickle.load(open("encoders.pkl",      "rb"))
feature_names = pickle.load(open("feature_names.pkl", "rb"))

# ── Home route ────────────────────────────────────────────
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message"  : "Customer Churn Prediction API",
        "author"   : "Akshat Rathore — Alfido Tech Internship Task 3",
        "endpoints": {
            "GET  /health"  : "Check if the API is running",
            "POST /predict" : "Predict churn for a single customer",
            "POST /predict_batch": "Predict churn for multiple customers",
            "GET  /features": "List all required input features",
        }
    })

# ── Health check ──────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status" : "healthy",
        "model"  : "RandomForestClassifier",
        "version": "1.0.0"
    }), 200

# ── Feature list ──────────────────────────────────────────
@app.route("/features", methods=["GET"])
def features():
    return jsonify({
        "required_features": feature_names,
        "total_features"   : len(feature_names),
        "categorical_features": list(encoders.keys()),
        "example_request"  : {
            "gender"          : "Male",
            "SeniorCitizen"   : 0,
            "Partner"         : "Yes",
            "Dependents"      : "No",
            "tenure"          : 12,
            "PhoneService"    : "Yes",
            "MultipleLines"   : "No",
            "InternetService" : "Fiber optic",
            "OnlineSecurity"  : "No",
            "TechSupport"     : "No",
            "Contract"        : "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod"   : "Electronic check",
            "MonthlyCharges"  : 75.5,
            "TotalCharges"    : 906.0
        }
    })

# ── Single prediction ─────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Encode categorical fields
        for col, le in encoders.items():
            if col in data and col != "Churn":
                val = data[col]
                if val not in le.classes_:
                    return jsonify({
                        "error": f"Invalid value '{val}' for field '{col}'",
                        "valid_values": list(le.classes_)
                    }), 400
                data[col] = int(le.transform([val])[0])

        # Build feature vector in correct order
        row = []
        for feat in feature_names:
            if feat not in data:
                return jsonify({"error": f"Missing required field: '{feat}'"}), 400
            row.append(data[feat])

        X = np.array(row).reshape(1, -1)
        X_scaled = scaler.transform(X)

        prediction  = int(model.predict(X_scaled)[0])
        probability = model.predict_proba(X_scaled)[0]
        churn_prob  = float(probability[1])

        return jsonify({
            "prediction"       : prediction,
            "churn_label"      : "YES — Will Churn" if prediction == 1 else "NO — Will NOT Churn",
            "churn_probability": round(churn_prob, 4),
            "confidence"       : f"{max(probability)*100:.1f}%",
            "risk_level"       : "HIGH" if churn_prob > 0.7 else "MEDIUM" if churn_prob > 0.4 else "LOW"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Batch prediction ──────────────────────────────────────
@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    try:
        data = request.get_json(force=True)
        if not data or "customers" not in data:
            return jsonify({"error": "Provide JSON with key 'customers' as a list"}), 400

        customers = data["customers"]
        results   = []

        for i, customer in enumerate(customers):
            # Encode categorical
            customer_copy = dict(customer)
            for col, le in encoders.items():
                if col in customer_copy and col != "Churn":
                    val = customer_copy[col]
                    if val in le.classes_:
                        customer_copy[col] = int(le.transform([val])[0])

            row = [customer_copy.get(feat, 0) for feat in feature_names]
            X = np.array(row).reshape(1, -1)
            X_scaled = scaler.transform(X)

            pred     = int(model.predict(X_scaled)[0])
            prob     = float(model.predict_proba(X_scaled)[0][1])
            results.append({
                "customer_index"   : i,
                "prediction"       : pred,
                "churn_label"      : "YES" if pred == 1 else "NO",
                "churn_probability": round(prob, 4),
                "risk_level"       : "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.4 else "LOW"
            })

        churners = sum(1 for r in results if r["prediction"] == 1)
        return jsonify({
            "total_customers": len(results),
            "predicted_churners": churners,
            "churn_rate": f"{churners/len(results)*100:.1f}%",
            "results": results
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Run ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Churn Prediction API starting on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
