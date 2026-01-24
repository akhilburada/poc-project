# Chapter 2: ML/DL Application Deployment

## Overview

This chapter covers deploying traditional Machine Learning and Deep Learning models on AWS and GCP.

---

## ML Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ML SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────┐                                                       │
│   │   Client    │                                                       │
│   │  (App/Web)  │                                                       │
│   └──────┬──────┘                                                       │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────────────────┐  │
│   │ API Gateway │────►│Load Balancer│────►│   Model Serving Layer   │  │
│   │  (Auth,     │     │  (Traffic   │     │  ┌─────┐ ┌─────┐       │  │
│   │   Rate      │     │   Routing)  │     │  │Pod 1│ │Pod 2│ ...   │  │
│   │   Limiting) │     └─────────────┘     │  └─────┘ └─────┘       │  │
│   └─────────────┘                         └───────────┬─────────────┘  │
│                                                       │                 │
│   ┌───────────────────────────────────────────────────┼─────────────┐  │
│   │                    Supporting Services            │             │  │
│   │  ┌────────────┐  ┌────────────┐  ┌────────────┐  │             │  │
│   │  │  Feature   │  │   Model    │  │ Monitoring │◄─┘             │  │
│   │  │   Store    │  │  Registry  │  │  & Logging │               │  │
│   │  └────────────┘  └────────────┘  └────────────┘               │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## AWS SageMaker Deployment

### What is SageMaker?

AWS SageMaker is a fully managed ML platform that provides:
- **Build**: Notebooks, feature store, data labeling
- **Train**: Managed training with distributed computing
- **Deploy**: Real-time endpoints, batch transform, serverless inference

### SageMaker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAGEMAKER DEPLOYMENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐                                                  │
│   │  Client  │                                                  │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────┐     ┌──────────────────────────────────┐ │
│   │  API Gateway    │────►│      SageMaker Endpoint          │ │
│   │  (Optional)     │     │  ┌────────────────────────────┐  │ │
│   └─────────────────┘     │  │   Endpoint Configuration   │  │ │
│                           │  │  - Instance type           │  │ │
│                           │  │  - Instance count          │  │ │
│                           │  │  - Auto-scaling rules      │  │ │
│                           │  └────────────────────────────┘  │ │
│                           │                                  │ │
│                           │  ┌─────────┐    ┌─────────┐     │ │
│                           │  │Instance │    │Instance │     │ │
│                           │  │   1     │    │   2     │ ... │ │
│                           │  │ (Model) │    │ (Model) │     │ │
│                           │  └─────────┘    └─────────┘     │ │
│                           └──────────────────────────────────┘ │
│                                        │                        │
│                                        ▼                        │
│   Model Artifacts ◄──── S3 Bucket ◄──── Model Registry          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step: Deploy Sklearn Model to SageMaker

#### Step 1: Train and Save Model Locally

```python
# train.py
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.4f}")

# Save model
joblib.dump(model, 'model.joblib')
print("Model saved to model.joblib")
```

#### Step 2: Create Inference Script

```python
# inference.py - This tells SageMaker how to use your model
import joblib
import json
import numpy as np
import os

def model_fn(model_dir):
    """
    Load model from the model directory.
    SageMaker calls this when starting the endpoint.
    """
    model_path = os.path.join(model_dir, 'model.joblib')
    model = joblib.load(model_path)
    return model

def input_fn(request_body, request_content_type):
    """
    Deserialize input data.
    SageMaker calls this to process incoming requests.
    """
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        return np.array(data['features'])
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """
    Make prediction using the loaded model.
    """
    # Reshape if single sample
    if input_data.ndim == 1:
        input_data = input_data.reshape(1, -1)
    
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    
    return {
        'predictions': predictions,
        'probabilities': probabilities
    }

def output_fn(prediction, response_content_type):
    """
    Serialize predictions to response.
    """
    if response_content_type == 'application/json':
        return json.dumps({
            'predictions': prediction['predictions'].tolist(),
            'probabilities': prediction['probabilities'].tolist()
        })
    else:
        raise ValueError(f"Unsupported content type: {response_content_type}")
```

#### Step 3: Package Model for SageMaker

```bash
# Create directory structure
mkdir -p model_package/code

# Copy files
cp model.joblib model_package/
cp inference.py model_package/code/

# Create requirements file
echo "scikit-learn==1.3.0
joblib==1.3.0
numpy==1.24.0" > model_package/code/requirements.txt

# Create tarball (SageMaker requires this format)
cd model_package
tar -czvf ../model.tar.gz .
cd ..
```

#### Step 4: Deploy to SageMaker

```python
# deploy.py
import boto3
import sagemaker
from sagemaker.sklearn import SKLearnModel

# Initialize
sagemaker_session = sagemaker.Session()
role = 'arn:aws:iam::YOUR_ACCOUNT_ID:role/SageMakerExecutionRole'
bucket = sagemaker_session.default_bucket()

# Upload model to S3
model_artifact = sagemaker_session.upload_data(
    path='model.tar.gz',
    bucket=bucket,
    key_prefix='sklearn-iris-model'
)
print(f"Model uploaded to: {model_artifact}")

# Create SageMaker model
sklearn_model = SKLearnModel(
    model_data=model_artifact,
    role=role,
    entry_point='inference.py',
    source_dir='model_package/code',
    framework_version='1.0-1',  # sklearn version in container
    py_version='py3'
)

# Deploy to endpoint
predictor = sklearn_model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',  # Small instance for demo
    endpoint_name='iris-classifier-endpoint'
)

print(f"Endpoint deployed: {predictor.endpoint_name}")
```

#### Step 5: Make Predictions

```python
# predict.py
import boto3
import json

# Create runtime client
runtime = boto3.client('sagemaker-runtime')

# Prepare data
test_data = {
    'features': [5.1, 3.5, 1.4, 0.2]  # Sample iris features
}

# Invoke endpoint
response = runtime.invoke_endpoint(
    EndpointName='iris-classifier-endpoint',
    ContentType='application/json',
    Body=json.dumps(test_data)
)

# Parse response
result = json.loads(response['Body'].read().decode())
print(f"Prediction: {result['predictions']}")
print(f"Probabilities: {result['probabilities']}")
```

#### Step 6: Clean Up

```python
# cleanup.py
import boto3

# Delete endpoint
sm_client = boto3.client('sagemaker')
sm_client.delete_endpoint(EndpointName='iris-classifier-endpoint')
sm_client.delete_endpoint_config(EndpointConfigName='iris-classifier-endpoint')

print("Endpoint deleted")
```

### SageMaker Deployment Options

| Option | Use Case | Pricing |
|--------|----------|---------|
| **Real-time Endpoints** | Low latency, always-on | Per hour (instance) |
| **Serverless Inference** | Sporadic traffic, cost-sensitive | Per request + duration |
| **Batch Transform** | Large batch processing | Per hour during job |
| **Async Inference** | Long-running predictions | Per hour + queue |

---

## GCP Vertex AI Deployment

### What is Vertex AI?

Google Cloud's unified ML platform that provides:
- **Vertex AI Workbench**: Managed notebooks
- **Vertex AI Training**: Distributed training
- **Vertex AI Prediction**: Model deployment
- **Vertex AI Pipelines**: ML workflow orchestration

### Vertex AI Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERTEX AI DEPLOYMENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐                                                  │
│   │  Client  │                                                  │
│   └────┬─────┘                                                  │
│        │                                                        │
│        ▼                                                        │
│   ┌──────────────────────────────────────────────────────────┐ │
│   │                  Vertex AI Endpoint                       │ │
│   │  ┌─────────────────────────────────────────────────────┐ │ │
│   │  │              Traffic Split Configuration            │ │ │
│   │  │   Model A (90%) ─────┬───── Model B (10%)          │ │ │
│   │  │        │             │           │                  │ │ │
│   │  └────────┼─────────────┼───────────┼──────────────────┘ │ │
│   │           │             │           │                    │ │
│   │     ┌─────▼─────┐ ┌─────▼─────┐ ┌───▼───────┐           │ │
│   │     │ Replica 1 │ │ Replica 2 │ │ Replica 1 │           │ │
│   │     │ (Model A) │ │ (Model A) │ │ (Model B) │           │ │
│   │     └───────────┘ └───────────┘ └───────────┘           │ │
│   └──────────────────────────────────────────────────────────┘ │
│                          │                                      │
│                          ▼                                      │
│   Model Artifacts ◄── Cloud Storage ◄── Model Registry          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step: Deploy Model to Vertex AI

#### Step 1: Prepare Model and Upload to GCS

```python
# prepare_model.py
import joblib
from google.cloud import storage
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train model
iris = load_iris()
model = RandomForestClassifier(n_estimators=100)
model.fit(iris.data, iris.target)

# Save locally
joblib.dump(model, 'model.joblib')

# Upload to GCS
storage_client = storage.Client()
bucket = storage_client.bucket('your-bucket-name')
blob = bucket.blob('models/iris/model.joblib')
blob.upload_from_filename('model.joblib')

print("Model uploaded to GCS")
```

#### Step 2: Create Custom Serving Container (Optional)

For custom preprocessing, create a custom container:

```python
# app.py - Custom serving application
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# Load model from GCS mount or local path
MODEL_PATH = os.environ.get('AIP_STORAGE_URI', '/model') + '/model.joblib'
model = joblib.load(MODEL_PATH)

class PredictRequest(BaseModel):
    instances: list

class PredictResponse(BaseModel):
    predictions: list

@app.get('/health')
def health():
    return {'status': 'healthy'}

@app.post('/predict')
def predict(request: PredictRequest):
    instances = np.array(request.instances)
    predictions = model.predict(instances)
    return PredictResponse(predictions=predictions.tolist())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
```

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### Step 3: Deploy Using Pre-built Container (Easier)

```python
# deploy_vertex.py
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(
    project='your-project-id',
    location='us-central1'
)

# Upload model to Vertex AI Model Registry
model = aiplatform.Model.upload(
    display_name='iris-classifier',
    artifact_uri='gs://your-bucket-name/models/iris/',
    serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest'
)

print(f"Model resource name: {model.resource_name}")

# Create endpoint
endpoint = aiplatform.Endpoint.create(
    display_name='iris-classifier-endpoint'
)

print(f"Endpoint resource name: {endpoint.resource_name}")

# Deploy model to endpoint
deployed_model = endpoint.deploy(
    model=model,
    deployed_model_display_name='iris-v1',
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=3,
    traffic_percentage=100,
    sync=True
)

print("Model deployed successfully!")
```

#### Step 4: Make Predictions

```python
# predict_vertex.py
from google.cloud import aiplatform

aiplatform.init(project='your-project-id', location='us-central1')

# Get endpoint
endpoint = aiplatform.Endpoint('projects/YOUR_PROJECT/locations/us-central1/endpoints/ENDPOINT_ID')

# Make prediction
instances = [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]
prediction = endpoint.predict(instances=instances)

print(f"Predictions: {prediction.predictions}")
```

---

## Deep Learning Model Deployment

### PyTorch Model on SageMaker

```python
# inference.py for PyTorch
import torch
import torch.nn as nn
import json
import os

class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def model_fn(model_dir):
    """Load PyTorch model"""
    model = SimpleNN(input_size=4, hidden_size=64, num_classes=3)
    model.load_state_dict(torch.load(os.path.join(model_dir, 'model.pth')))
    model.eval()
    return model

def input_fn(request_body, request_content_type):
    """Deserialize input"""
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        return torch.tensor(data['features'], dtype=torch.float32)
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Run inference"""
    with torch.no_grad():
        output = model(input_data)
        probabilities = torch.softmax(output, dim=1)
        predictions = torch.argmax(output, dim=1)
    return {'predictions': predictions, 'probabilities': probabilities}

def output_fn(prediction, response_content_type):
    """Serialize output"""
    return json.dumps({
        'predictions': prediction['predictions'].tolist(),
        'probabilities': prediction['probabilities'].tolist()
    })
```

### TensorFlow Model on Vertex AI

```python
# For TensorFlow, use SavedModel format
import tensorflow as tf

# Save model in SavedModel format
model.save('saved_model/')

# Upload to GCS
# gsutil cp -r saved_model/ gs://your-bucket/models/tf-model/

# Deploy with TF serving container
from google.cloud import aiplatform

model = aiplatform.Model.upload(
    display_name='tf-classifier',
    artifact_uri='gs://your-bucket/models/tf-model/',
    serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-11:latest'
)
```

---

## Containerized Deployment (Universal Approach)

### Standard Project Structure

```
ml-project/
├── src/
│   ├── __init__.py
│   ├── app.py              # FastAPI application
│   ├── model.py            # Model loading and inference
│   └── preprocessing.py    # Data preprocessing
├── model/
│   └── model.joblib        # Trained model file
├── tests/
│   ├── test_app.py
│   └── test_model.py
├── Dockerfile
├── requirements.txt
├── docker-compose.yml      # Local development
└── README.md
```

### Production-Ready Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.10-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN useradd --create-home appuser
USER appuser

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser model/ ./model/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/model/model.joblib

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### FastAPI Application with Best Practices

```python
# src/app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
import time
import os

from src.model import ModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ML Model API",
    description="Production ML model serving API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model manager
model_manager = None

# Request/Response models
class PredictionRequest(BaseModel):
    features: List[float] = Field(..., min_items=1, description="Input features")
    
class PredictionResponse(BaseModel):
    prediction: List[int]
    probability: Optional[List[List[float]]] = None
    model_version: str
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str

# Startup event
@app.on_event("startup")
async def load_model():
    global model_manager
    model_path = os.getenv("MODEL_PATH", "model/model.joblib")
    model_manager = ModelManager(model_path)
    logger.info(f"Model loaded from {model_path}")

# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        model_loaded=model_manager is not None,
        model_version=model_manager.version if model_manager else "unknown"
    )

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    start_time = time.time()
    
    try:
        prediction, probability = model_manager.predict(request.features)
        latency_ms = (time.time() - start_time) * 1000
        
        logger.info(f"Prediction made in {latency_ms:.2f}ms")
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            model_version=model_manager.version,
            latency_ms=round(latency_ms, 2)
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Batch prediction endpoint
@app.post("/predict/batch")
async def predict_batch(requests: List[PredictionRequest]):
    results = []
    for req in requests:
        result = await predict(req)
        results.append(result)
    return results
```

```python
# src/model.py
import joblib
import numpy as np
from typing import Tuple, List, Optional
import logging

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)
        self.version = "1.0.0"
        logger.info(f"Model loaded: {type(self.model).__name__}")
    
    def predict(self, features: List[float]) -> Tuple[List[int], Optional[List[List[float]]]]:
        """Make prediction with the loaded model"""
        X = np.array(features).reshape(1, -1)
        
        prediction = self.model.predict(X).tolist()
        
        probability = None
        if hasattr(self.model, 'predict_proba'):
            probability = self.model.predict_proba(X).tolist()
        
        return prediction, probability
```

### Deploy to AWS ECS

```bash
# 1. Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t ml-api .
docker tag ml-api:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest

# 2. Create ECS task definition and service via AWS Console or CLI
```

### Deploy to GCP Cloud Run

```bash
# 1. Build and push to Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

docker build -t us-central1-docker.pkg.dev/YOUR_PROJECT/ml-repo/ml-api:latest .
docker push us-central1-docker.pkg.dev/YOUR_PROJECT/ml-repo/ml-api:latest

# 2. Deploy to Cloud Run
gcloud run deploy ml-api \
    --image us-central1-docker.pkg.dev/YOUR_PROJECT/ml-repo/ml-api:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 1 \
    --max-instances 10
```

---

## Auto-Scaling Configuration

### SageMaker Auto-Scaling

```python
import boto3

client = boto3.client('application-autoscaling')

# Register scalable target
client.register_scalable_target(
    ServiceNamespace='sagemaker',
    ResourceId='endpoint/my-endpoint/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    MinCapacity=1,
    MaxCapacity=10
)

# Create scaling policy
client.put_scaling_policy(
    PolicyName='my-scaling-policy',
    ServiceNamespace='sagemaker',
    ResourceId='endpoint/my-endpoint/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    PolicyType='TargetTrackingScaling',
    TargetTrackingScalingPolicyConfiguration={
        'TargetValue': 70.0,  # Target CPU utilization
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
        },
        'ScaleInCooldown': 300,
        'ScaleOutCooldown': 60
    }
)
```

### Vertex AI Auto-Scaling

```python
# Auto-scaling is configured during deployment
endpoint.deploy(
    model=model,
    machine_type='n1-standard-4',
    min_replica_count=1,    # Minimum instances
    max_replica_count=10,   # Maximum instances
    # Vertex AI automatically scales based on traffic
)
```

---

## Summary: When to Use What

| Scenario | AWS Solution | GCP Solution |
|----------|--------------|--------------|
| Simple sklearn model | SageMaker Serverless | Cloud Run |
| Production sklearn/XGBoost | SageMaker Endpoint | Vertex AI Endpoint |
| Deep Learning (GPU) | SageMaker GPU Instance | Vertex AI GPU |
| Custom preprocessing | ECS with Docker | Cloud Run |
| Batch predictions | SageMaker Batch Transform | Vertex AI Batch Prediction |
| Multi-model serving | SageMaker Multi-Model Endpoint | Vertex AI with Traffic Split |

---

## Next Steps

Continue to [Chapter 3: GenAI Deployment](../03-genai-deployment/README.md) to learn how to deploy LLM and RAG applications.
