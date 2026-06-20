# ── Dockerfile — Churn Prediction API ────────────────────
# Alfido Tech Internship Task 3 | Akshat Rathore

# Base image — lightweight Python
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into container
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the API
CMD ["python", "app.py"]
