# End-to-End Deployment Guide: Complete Walkthrough

This guide provides step-by-step instructions to deploy a complete ML application from scratch.

---

## Complete Example: Deploy a Sentiment Analysis API

This is a fully working example you can follow from start to finish.

### Prerequisites

```bash
# Install required tools
pip install scikit-learn joblib fastapi uvicorn boto3 google-cloud-aiplatform

# For Docker
# Install Docker Desktop from https://www.docker.com/products/docker-desktop

# For AWS
pip install awscli sagemaker
aws configure  # Enter your credentials

# For GCP
# Install gcloud from https://cloud.google.com/sdk/docs/install
gcloud init
gcloud auth application-default login
```

---

## Step 1: Train and Save the Model

Create the following files:

### train_model.py

```python
#!/usr/bin/env python3
"""
Train a sentiment analysis model and save it.
Run: python train_model.py
"""

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Sample training data (in production, use a real dataset)
texts = [
    "I love this product, it's amazing!",
    "This is the best purchase I've ever made",
    "Absolutely fantastic, highly recommend",
    "Great quality and fast shipping",
    "Exceeded my expectations, very happy",
    "This product is terrible, waste of money",
    "Very disappointed with the quality",
    "Worst purchase ever, do not buy",
    "Complete garbage, returning immediately",
    "Horrible experience, never again",
    "It's okay, nothing special",
    "Average product, does the job",
    "Not bad but not great either",
    "Decent for the price",
    "Mediocre at best"
]

labels = [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # 0=negative, 1=neutral, 2=positive

# More training data for better model
texts = texts * 100  # Replicate for demo
labels = labels * 100
# Add some noise
np.random.seed(42)
for i in range(len(texts)):
    if np.random.random() < 0.1:
        labels[i] = np.random.randint(0, 3)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# Create and train model
print("Training model...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, multi_class='multinomial')
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['negative', 'neutral', 'positive']))

# Save model
print("\nSaving model...")
model_data = {
    'model': model,
    'vectorizer': vectorizer
}
joblib.dump(model_data, 'sentiment_model.joblib')
print("Model saved to sentiment_model.joblib")

# Test prediction
test_text = "This product is absolutely wonderful!"
vec = vectorizer.transform([test_text])
pred = model.predict(vec)[0]
proba = model.predict_proba(vec)[0]
print(f"\nTest prediction for '{test_text}':")
print(f"  Prediction: {['negative', 'neutral', 'positive'][pred]}")
print(f"  Probabilities: {dict(zip(['negative', 'neutral', 'positive'], proba.round(3)))}")
```

Run the training:
```bash
python train_model.py
```

---

## Step 2: Create the FastAPI Application

### src/app.py

```python
"""
Sentiment Analysis API
Run locally: uvicorn src.app:app --reload --port 8080
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
import time
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Sentiment Analysis API",
    description="Analyze sentiment of text (positive, neutral, negative)",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "sentiment_model.joblib")
logger.info(f"Loading model from {MODEL_PATH}")

try:
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    vectorizer = model_data['vectorizer']
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None
    vectorizer = None

# Pydantic models
class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This product is amazing! I love it so much."
            }
        }

class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    probabilities: dict
    latency_ms: float

class BatchRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100)

class BatchResponse(BaseModel):
    predictions: List[PredictionResponse]
    total_latency_ms: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# Endpoints
@app.get("/", include_in_schema=False)
def root():
    return {"message": "Sentiment Analysis API. Visit /docs for documentation."}

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Check API health and model status"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
def predict(request: PredictionRequest):
    """
    Analyze sentiment of a single text.
    
    Returns sentiment (positive/neutral/negative) with confidence score.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    
    try:
        # Vectorize and predict
        vec = vectorizer.transform([request.text])
        prediction = model.predict(vec)[0]
        probabilities = model.predict_proba(vec)[0]
        
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        sentiment = sentiment_map[prediction]
        confidence = float(np.max(probabilities))
        
        latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Prediction: {sentiment} (confidence: {confidence:.3f}, latency: {latency_ms:.2f}ms)")
        
        return PredictionResponse(
            text=request.text,
            sentiment=sentiment,
            confidence=round(confidence, 4),
            probabilities={
                'negative': round(float(probabilities[0]), 4),
                'neutral': round(float(probabilities[1]), 4),
                'positive': round(float(probabilities[2]), 4)
            },
            latency_ms=round(latency_ms, 2)
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", response_model=BatchResponse, tags=["Predictions"])
def predict_batch(request: BatchRequest):
    """
    Analyze sentiment of multiple texts in a single request.
    
    Maximum 100 texts per request.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    start_time = time.time()
    predictions = []
    
    for text in request.texts:
        req = PredictionRequest(text=text)
        pred = predict(req)
        predictions.append(pred)
    
    total_latency = (time.time() - start_time) * 1000
    
    return BatchResponse(
        predictions=predictions,
        total_latency_ms=round(total_latency, 2)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Test locally:

```bash
# Run the API
uvicorn src.app:app --reload --port 8080

# In another terminal, test it
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Expected response:
# {"text":"This product is amazing!","sentiment":"positive","confidence":0.8542,...}
```

---

## Step 3: Containerize with Docker

### Dockerfile

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY sentiment_model.joblib .

# Set environment variables
ENV MODEL_PATH=/app/sentiment_model.joblib
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
scikit-learn==1.3.0
joblib==1.3.0
numpy==1.24.0
```

### Build and test Docker image:

```bash
# Build the image
docker build -t sentiment-api:latest .

# Run locally
docker run -p 8080:8080 sentiment-api:latest

# Test
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "I hate this product!"}'
```

---

## Step 4: Deploy to AWS

### Option A: AWS ECS (Recommended for production)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name sentiment-api --region us-east-1

# 2. Get the repository URI
REPO_URI=$(aws ecr describe-repositories --repository-names sentiment-api --query 'repositories[0].repositoryUri' --output text)
echo "Repository URI: $REPO_URI"

# 3. Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $REPO_URI

# 4. Build, tag, and push
docker build -t sentiment-api .
docker tag sentiment-api:latest $REPO_URI:latest
docker push $REPO_URI:latest

# 5. Create ECS cluster
aws ecs create-cluster --cluster-name sentiment-cluster --region us-east-1

# 6. Register task definition (save as task-definition.json first)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 7. Create service
aws ecs create-service \
    --cluster sentiment-cluster \
    --service-name sentiment-service \
    --task-definition sentiment-api:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### task-definition.json

```json
{
    "family": "sentiment-api",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT:role/ecsTaskExecutionRole",
    "containerDefinitions": [
        {
            "name": "sentiment-api",
            "image": "YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest",
            "portMappings": [
                {
                    "containerPort": 8080,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
                "interval": 30,
                "timeout": 5,
                "retries": 3,
                "startPeriod": 60
            },
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/sentiment-api",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs"
                }
            }
        }
    ]
}
```

### Option B: AWS Lambda (Serverless)

For Lambda, you'll need to use Mangum adapter:

```python
# lambda_handler.py
from mangum import Mangum
from src.app import app

handler = Mangum(app, lifespan="off")
```

Deploy with SAM or Serverless Framework.

---

## Step 5: Deploy to GCP

### Deploy to Cloud Run (Easiest)

```bash
# 1. Set project
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# 2. Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 3. Build and push using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/sentiment-api

# 4. Deploy to Cloud Run
gcloud run deploy sentiment-api \
    --image gcr.io/$PROJECT_ID/sentiment-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --port 8080

# 5. Get the URL
gcloud run services describe sentiment-api --region us-central1 --format 'value(status.url)'

# 6. Test
SERVICE_URL=$(gcloud run services describe sentiment-api --region us-central1 --format 'value(status.url)')
curl -X POST "$SERVICE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is wonderful!"}'
```

### Configure auto-scaling

```bash
# Update with auto-scaling settings
gcloud run services update sentiment-api \
    --region us-central1 \
    --min-instances 1 \
    --max-instances 100 \
    --concurrency 80 \
    --cpu-throttling
```

---

## Step 6: Set Up CI/CD

### .github/workflows/deploy.yml

```yaml
name: Deploy Sentiment API

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  REGION: us-central1
  SERVICE_NAME: sentiment-api

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest httpx
      
      - name: Train model
        run: python train_model.py
      
      - name: Run tests
        run: pytest tests/ -v

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
      
      - name: Train model
        run: python train_model.py
      
      - name: Build and Deploy
        run: |
          gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME
          gcloud run deploy $SERVICE_NAME \
            --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --allow-unauthenticated
```

### tests/test_app.py

```python
"""
API Tests
Run: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '.')
from src.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] == True

def test_predict_positive():
    response = client.post("/predict", json={
        "text": "This is absolutely amazing! I love it!"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert data["confidence"] > 0.5

def test_predict_negative():
    response = client.post("/predict", json={
        "text": "This is terrible. Worst product ever."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "negative"

def test_predict_empty():
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422  # Validation error

def test_batch_predict():
    response = client.post("/predict/batch", json={
        "texts": ["Great product!", "Terrible service", "It's okay"]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["predictions"]) == 3
```

---

## Step 7: Monitor Your Deployment

### Add monitoring to the application

```python
# Add to src/app.py

from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

# Metrics
PREDICTION_COUNT = Counter(
    'sentiment_predictions_total',
    'Total predictions',
    ['sentiment', 'status']
)

PREDICTION_LATENCY = Histogram(
    'sentiment_prediction_latency_seconds',
    'Prediction latency'
)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# Update predict endpoint to record metrics
# Add after prediction:
PREDICTION_COUNT.labels(sentiment=sentiment, status='success').inc()
PREDICTION_LATENCY.observe(latency_ms / 1000)
```

---

## Complete Project Structure

```
sentiment-api/
├── src/
│   ├── __init__.py
│   └── app.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── train_model.py
├── sentiment_model.joblib
├── Dockerfile
├── requirements.txt
├── task-definition.json      # For AWS ECS
└── README.md
```

---

## Cost Summary

### AWS (ECS Fargate)
| Component | Monthly Cost |
|-----------|-------------|
| 2 tasks (0.5 vCPU, 1GB) | ~$30 |
| Application Load Balancer | ~$20 |
| CloudWatch Logs | ~$5 |
| **Total** | **~$55/month** |

### GCP (Cloud Run)
| Component | Monthly Cost |
|-----------|-------------|
| Cloud Run (pay per use) | ~$10-30 |
| Cloud Logging | ~$5 |
| **Total** | **~$15-35/month** |

---

## What You've Learned

After completing this guide, you can now:

1. Train and save an ML model
2. Create a production-ready API with FastAPI
3. Containerize with Docker
4. Deploy to AWS ECS or GCP Cloud Run
5. Set up CI/CD with GitHub Actions
6. Add monitoring and health checks

This is exactly what interviewers want to see in candidates!
