# Complete Guide to Deploying AI Applications on AWS and GCP

**A comprehensive guide for deploying ML/DL, GenAI, and Agentic AI applications**

---

## Table of Contents

1. [Introduction & Fundamentals](#1-introduction--fundamentals)
2. [ML/DL Application Deployment](#2-mldl-application-deployment)
3. [GenAI Application Deployment (LLM & RAG)](#3-genai-application-deployment-llm--rag)
4. [Agentic AI Application Deployment](#4-agentic-ai-application-deployment)
5. [Best Practices](#5-best-practices)
6. [Interview Questions & Answers](#6-interview-questions--answers)
7. [Project Templates & Code](#7-project-templates--code)
8. [Real-World Deployment Examples](#8-real-world-deployment-examples)
9. [End-to-End Deployment Walkthrough](#9-end-to-end-deployment-walkthrough)
10. [Quick Reference Cheat Sheet](#10-quick-reference-cheat-sheet)

---

# 1. Introduction & Fundamentals

## What is Cloud Deployment for AI?

Cloud deployment means running your AI/ML applications on remote servers managed by cloud providers (AWS, GCP) instead of your local machine.

### Why Deploy to Cloud?

| Benefit | Explanation |
|---------|-------------|
| **Scalability** | Handle 10 or 10 million users - cloud scales automatically |
| **Reliability** | 99.9%+ uptime, automatic failover, disaster recovery |
| **Cost Efficiency** | Pay only for what you use (no idle servers) |
| **Global Reach** | Deploy in multiple regions close to your users |
| **Managed Services** | Focus on ML, let cloud handle infrastructure |

## The Deployment Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI APPLICATION DEPLOYMENT LIFECYCLE                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │  TRAIN   │───►│ PACKAGE  │───►│  DEPLOY  │───►│  SERVE   │         │
│   │  Model   │    │ (Docker) │    │  (Cloud) │    │  (API)   │         │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘         │
│        │               │               │               │                │
│   Local/Cloud     Dockerfile      AWS/GCP         REST API              │
│   Training        requirements    Services        Endpoint              │
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │                         CONTINUOUS                                │ │
│   │  ┌──────────┐    ┌──────────┐    ┌──────────┐                    │ │
│   │  │ MONITOR  │───►│  RETRAIN │───►│  UPDATE  │ (CI/CD Loop)       │ │
│   │  └──────────┘    └──────────┘    └──────────┘                    │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## AWS vs GCP: Complete Service Comparison

### AI/ML Services

| Purpose | AWS | GCP | Notes |
|---------|-----|-----|-------|
| ML Platform | **SageMaker** | **Vertex AI** | End-to-end ML lifecycle |
| LLM/GenAI | **Bedrock** | **Vertex AI + Gemini** | Foundation models |
| AutoML | SageMaker Autopilot | Vertex AI AutoML | No-code ML |
| Pre-trained APIs | Rekognition, Comprehend | Vision AI, Natural Language | Ready-to-use AI |

### Compute Services

| Purpose | AWS | GCP | When to Use |
|---------|-----|-----|-------------|
| Virtual Machines | EC2 | Compute Engine | Custom setup, full control |
| Serverless Functions | Lambda | Cloud Functions | Event-driven, light workloads |
| Containers (Managed) | ECS | Cloud Run | Containerized apps, auto-scale |
| Kubernetes | EKS | GKE | Complex microservices |

### Data & Storage

| Purpose | AWS | GCP |
|---------|-----|-----|
| Object Storage | S3 | Cloud Storage |
| Data Warehouse | Redshift | BigQuery |
| NoSQL Database | DynamoDB | Firestore/Bigtable |
| Vector Database | OpenSearch | Vertex AI Vector Search |
| Cache | ElastiCache | Memorystore |

### Networking & Security

| Purpose | AWS | GCP |
|---------|-----|-----|
| API Gateway | API Gateway | Cloud Endpoints / API Gateway |
| Load Balancer | ALB/NLB | Cloud Load Balancing |
| Secrets | Secrets Manager | Secret Manager |
| IAM | IAM | Cloud IAM |

### Monitoring & DevOps

| Purpose | AWS | GCP |
|---------|-----|-----|
| Monitoring | CloudWatch | Cloud Monitoring |
| Logging | CloudWatch Logs | Cloud Logging |
| CI/CD | CodePipeline | Cloud Build |
| Container Registry | ECR | Artifact Registry |

## Key Concepts You Must Know

### 1. Containerization (Docker)

**What is it?** A way to package your application with ALL its dependencies into a single unit.

```bash
# Build an image from Dockerfile
docker build -t my-app:v1 .

# Run container locally
docker run -p 8080:8080 my-app:v1

# List running containers
docker ps

# Stop a container
docker stop <container_id>
```

### 2. REST APIs

Your model is wrapped in an API so other applications can send data and get predictions.

```
┌─────────────┐         HTTP POST          ┌─────────────────┐
│   Client    │ ─────────────────────────► │   Your ML API   │
│  (Browser,  │  {"features": [1,2,3,4]}   │  /predict       │
│   App)      │ ◄───────────────────────── │                 │
└─────────────┘  {"prediction": "cat"}     └─────────────────┘
```

### 3. CI/CD Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───►│  Build  │───►│  Test   │───►│ Deploy  │───►│  Live!  │
│  Code   │    │  Image  │    │  Model  │    │ to Cloud│    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## Model Deployment Patterns

### Pattern 1: Real-time Inference (Synchronous)
- User sends request → Gets response immediately (< 100ms)
- Use for: Chatbots, fraud detection, recommendations

### Pattern 2: Batch Inference (Asynchronous)
- Process large datasets offline
- Use for: Daily predictions, bulk scoring

### Pattern 3: Streaming Inference
- Process continuous data streams
- Use for: IoT sensors, real-time analytics

## Essential Tools Setup

```bash
# 1. Python environment
python -m venv venv
source venv/bin/activate

# 2. Install core packages
pip install boto3 google-cloud-aiplatform fastapi uvicorn

# 3. AWS CLI
pip install awscli
aws configure

# 4. GCP CLI
gcloud init
gcloud auth application-default login

# Verify setup
aws sts get-caller-identity
gcloud auth list
```

---

# 2. ML/DL Application Deployment

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

## AWS SageMaker Deployment

### SageMaker Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAGEMAKER DEPLOYMENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Client ──► API Gateway ──► SageMaker Endpoint                 │
│                                      │                          │
│                              ┌───────┴───────┐                  │
│                              │               │                  │
│                         Instance 1      Instance 2              │
│                         (Model A)       (Model A)               │
│                              │               │                  │
│                              └───────┬───────┘                  │
│                                      │                          │
│                              Auto Scaling Group                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step SageMaker Deployment

#### Step 1: Train and Save Model

```python
# train.py
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load and split data
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
```

#### Step 2: Create Inference Script

```python
# inference.py
import joblib
import json
import numpy as np
import os

def model_fn(model_dir):
    """Load model from the model directory"""
    model_path = os.path.join(model_dir, 'model.joblib')
    model = joblib.load(model_path)
    return model

def input_fn(request_body, request_content_type):
    """Deserialize input data"""
    if request_content_type == 'application/json':
        data = json.loads(request_body)
        return np.array(data['features'])
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Make prediction"""
    if input_data.ndim == 1:
        input_data = input_data.reshape(1, -1)
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)
    return {'predictions': predictions, 'probabilities': probabilities}

def output_fn(prediction, response_content_type):
    """Serialize predictions"""
    return json.dumps({
        'predictions': prediction['predictions'].tolist(),
        'probabilities': prediction['probabilities'].tolist()
    })
```

#### Step 3: Package Model

```bash
mkdir -p model_package/code
cp model.joblib model_package/
cp inference.py model_package/code/

echo "scikit-learn==1.3.0
joblib==1.3.0
numpy==1.24.0" > model_package/code/requirements.txt

cd model_package && tar -czvf ../model.tar.gz . && cd ..
```

#### Step 4: Deploy to SageMaker

```python
# deploy.py
import boto3
import sagemaker
from sagemaker.sklearn import SKLearnModel

sagemaker_session = sagemaker.Session()
role = 'arn:aws:iam::YOUR_ACCOUNT_ID:role/SageMakerExecutionRole'
bucket = sagemaker_session.default_bucket()

# Upload model to S3
model_artifact = sagemaker_session.upload_data(
    path='model.tar.gz',
    bucket=bucket,
    key_prefix='sklearn-iris-model'
)

# Create and deploy model
sklearn_model = SKLearnModel(
    model_data=model_artifact,
    role=role,
    entry_point='inference.py',
    source_dir='model_package/code',
    framework_version='1.0-1',
    py_version='py3'
)

predictor = sklearn_model.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium',
    endpoint_name='iris-classifier-endpoint'
)
```

#### Step 5: Make Predictions

```python
# predict.py
import boto3
import json

runtime = boto3.client('sagemaker-runtime')

test_data = {'features': [5.1, 3.5, 1.4, 0.2]}

response = runtime.invoke_endpoint(
    EndpointName='iris-classifier-endpoint',
    ContentType='application/json',
    Body=json.dumps(test_data)
)

result = json.loads(response['Body'].read().decode())
print(f"Prediction: {result['predictions']}")
```

### SageMaker Deployment Options

| Option | Use Case | Pricing |
|--------|----------|---------|
| **Real-time Endpoints** | Low latency, always-on | Per hour (instance) |
| **Serverless Inference** | Sporadic traffic | Per request + duration |
| **Batch Transform** | Large batch processing | Per hour during job |
| **Async Inference** | Long-running predictions | Per hour + queue |

## GCP Vertex AI Deployment

### Vertex AI Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   VERTEX AI DEPLOYMENT                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Client ──► Vertex AI Endpoint ──► Model (Deployed)            │
│                      │                                          │
│              ┌───────┴───────┐                                  │
│              │               │                                  │
│         Replica 1       Replica 2                               │
│              │               │                                  │
│              └───────┬───────┘                                  │
│                      │                                          │
│              Traffic Splitting                                  │
│           (A/B Testing, Canary)                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Step-by-Step Vertex AI Deployment

```python
# deploy_vertex.py
from google.cloud import aiplatform

aiplatform.init(project='your-project-id', location='us-central1')

# Upload model
model = aiplatform.Model.upload(
    display_name='iris-classifier',
    artifact_uri='gs://your-bucket/models/iris/',
    serving_container_image_uri='us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest'
)

# Create endpoint
endpoint = aiplatform.Endpoint.create(display_name='iris-endpoint')

# Deploy
deployed_model = endpoint.deploy(
    model=model,
    machine_type='n1-standard-4',
    min_replica_count=1,
    max_replica_count=3,
    traffic_percentage=100
)

# Make prediction
prediction = endpoint.predict(instances=[[5.1, 3.5, 1.4, 0.2]])
print(prediction.predictions)
```

## Docker for ML Deployment

### Production-Ready Dockerfile

```dockerfile
FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home appuser
USER appuser

COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser model/ ./model/

ENV PYTHONUNBUFFERED=1
ENV MODEL_PATH=/app/model/model.joblib

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### FastAPI Application

```python
# src/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import joblib
import numpy as np
import time
import os

app = FastAPI(title="ML Model API", version="1.0.0")

model = joblib.load(os.getenv("MODEL_PATH", "model/model.joblib"))

class PredictionRequest(BaseModel):
    features: List[float] = Field(..., min_items=1)

class PredictionResponse(BaseModel):
    prediction: List[int]
    probability: Optional[List[List[float]]] = None
    latency_ms: float

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    start_time = time.time()
    
    try:
        X = np.array(request.features).reshape(1, -1)
        prediction = model.predict(X).tolist()
        probability = model.predict_proba(X).tolist() if hasattr(model, 'predict_proba') else None
        latency_ms = (time.time() - start_time) * 1000
        
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            latency_ms=round(latency_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Deploy to AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t ml-api .
docker tag ml-api:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/ml-api:latest
```

### Deploy to GCP Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT/ml-api

gcloud run deploy ml-api \
    --image gcr.io/YOUR_PROJECT/ml-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --min-instances 1 \
    --max-instances 10
```

## Auto-Scaling Configuration

### SageMaker Auto-Scaling

```python
import boto3

client = boto3.client('application-autoscaling')

client.register_scalable_target(
    ServiceNamespace='sagemaker',
    ResourceId='endpoint/my-endpoint/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    MinCapacity=1,
    MaxCapacity=10
)

client.put_scaling_policy(
    PolicyName='my-scaling-policy',
    ServiceNamespace='sagemaker',
    ResourceId='endpoint/my-endpoint/variant/AllTraffic',
    ScalableDimension='sagemaker:variant:DesiredInstanceCount',
    PolicyType='TargetTrackingScaling',
    TargetTrackingScalingPolicyConfiguration={
        'TargetValue': 70.0,
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'SageMakerVariantInvocationsPerInstance'
        },
        'ScaleInCooldown': 300,
        'ScaleOutCooldown': 60
    }
)
```

---

# 3. GenAI Application Deployment (LLM & RAG)

## Understanding GenAI Architectures

### Simple LLM Application

```
┌─────────────────────────────────────────────────────────────────┐
│                 SIMPLE LLM APPLICATION                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User Input: "Explain quantum computing"                       │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │   Prompt Template                                        │  │
│   │   "You are an expert teacher. Explain {topic} in        │  │
│   │    simple terms for a beginner."                        │  │
│   └─────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │   LLM API (Bedrock/Vertex AI/OpenAI)                    │  │
│   └─────────────────────┬───────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│   Response: "Quantum computing is like..."                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### RAG (Retrieval Augmented Generation) Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RAG SYSTEM ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ═══════════════════════ INDEXING PIPELINE (Offline) ═══════════════════════│
│                                                                             │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌───────────┐ │
│  │Documents│──►│  Loader  │──►│ Chunker  │──►│ Embedder │──►│Vector DB  │ │
│  │(PDF,etc)│   │          │   │(split)   │   │          │   │(store)    │ │
│  └─────────┘   └──────────┘   └──────────┘   └──────────┘   └───────────┘ │
│                                                                             │
│  ═══════════════════════ QUERY PIPELINE (Online) ═══════════════════════════│
│                                                                             │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐                                 │
│  │  User   │──►│  Embed   │──►│  Search  │                                 │
│  │  Query  │   │  Query   │   │ Top-K    │                                 │
│  └─────────┘   └──────────┘   └────┬─────┘                                 │
│                                    │                                        │
│                    ┌───────────────┴───────────────┐                       │
│                    │     Retrieved Documents       │                        │
│                    └───────────────┬───────────────┘                        │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │   PROMPT = System Instructions + Retrieved Context + User Query       │  │
│  └──────────────────────────────────┬───────────────────────────────────┘  │
│                                     │                                       │
│                                     ▼                                       │
│                            ┌───────────────┐                                │
│                            │   LLM API     │──► Generated Answer            │
│                            └───────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## AWS Bedrock Services

| Model Provider | Models Available | Best For |
|---------------|------------------|----------|
| Anthropic | Claude 3 (Opus, Sonnet, Haiku) | General tasks, reasoning |
| Meta | Llama 2, Llama 3 | Open-source, customizable |
| Amazon | Titan Text, Titan Embeddings | Cost-effective |

### Basic Bedrock LLM Call

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_claude(prompt: str, max_tokens: int = 1000) -> str:
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=body
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

# Usage
response = call_claude("Explain machine learning in 3 sentences.")
print(response)
```

### Bedrock Embeddings

```python
def get_embedding(text: str) -> list:
    body = json.dumps({"inputText": text})
    
    response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=body
    )
    
    result = json.loads(response['body'].read())
    return result['embedding']  # 1536 dimensions

embedding = get_embedding("Hello, world!")
print(f"Embedding dimension: {len(embedding)}")
```

## Complete RAG Implementation (AWS)

```python
import boto3
import json
from typing import List, Dict
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

class AWSRAGSystem:
    def __init__(self, opensearch_host: str, index_name: str, region: str = 'us-east-1'):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        self.index_name = index_name
        
        credentials = boto3.Session().get_credentials()
        awsauth = AWS4Auth(
            credentials.access_key, credentials.secret_key,
            region, 'es', session_token=credentials.token
        )
        
        self.opensearch = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    
    def get_embedding(self, text: str) -> List[float]:
        response = self.bedrock.invoke_model(
            modelId='amazon.titan-embed-text-v1',
            body=json.dumps({'inputText': text})
        )
        return json.loads(response['body'].read())['embedding']
    
    def index_document(self, doc_id: str, text: str, metadata: Dict = None):
        embedding = self.get_embedding(text)
        document = {
            'text': text,
            'embedding': embedding,
            'metadata': metadata or {}
        }
        self.opensearch.index(index=self.index_name, id=doc_id, body=document)
    
    def search_similar(self, query: str, k: int = 5) -> List[Dict]:
        query_embedding = self.get_embedding(query)
        
        search_query = {
            'size': k,
            'query': {
                'knn': {
                    'embedding': {'vector': query_embedding, 'k': k}
                }
            }
        }
        
        response = self.opensearch.search(index=self.index_name, body=search_query)
        return [
            {'text': hit['_source']['text'], 'score': hit['_score']}
            for hit in response['hits']['hits']
        ]
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        context = "\n\n".join([doc['text'] for doc in context_docs])
        
        prompt = f"""Based on the following context, answer the question.
If the answer is not in the context, say "I don't have enough information."

Context:
{context}

Question: {query}

Answer:"""
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        return json.loads(response['body'].read())['content'][0]['text']
    
    def query(self, question: str, k: int = 5) -> str:
        relevant_docs = self.search_similar(question, k=k)
        return self.generate_response(question, relevant_docs)

# Usage
rag = AWSRAGSystem(
    opensearch_host='your-domain.us-east-1.es.amazonaws.com',
    index_name='documents'
)

# Index documents
rag.index_document("doc1", "Python is a programming language created by Guido van Rossum.")
rag.index_document("doc2", "Machine learning is a subset of artificial intelligence.")

# Query
answer = rag.query("Who created Python?")
print(answer)
```

## GCP Vertex AI for GenAI

### Basic Gemini Call

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project='your-project-id', location='us-central1')

def call_gemini(prompt: str) -> str:
    model = GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    return response.text

response = call_gemini("Explain quantum computing in simple terms.")
print(response)
```

### Vertex AI Embeddings

```python
from vertexai.language_models import TextEmbeddingModel

def get_embeddings(texts: list) -> list:
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings(texts)
    return [embedding.values for embedding in embeddings]

texts = ["Hello world", "Machine learning is awesome"]
embeddings = get_embeddings(texts)
print(f"Embedding dimension: {len(embeddings[0])}")
```

## Production RAG FastAPI Service

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
import time

app = FastAPI(title="RAG API", version="1.0.0")

class QueryRequest(BaseModel):
    question: str
    max_docs: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    latency_ms: float

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    start_time = time.time()
    
    try:
        relevant_docs = rag_system.search_similar(request.question, k=request.max_docs)
        answer = rag_system.generate_response(request.question, relevant_docs)
        latency_ms = (time.time() - start_time) * 1000
        
        return QueryResponse(
            answer=answer,
            sources=relevant_docs,
            latency_ms=round(latency_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Advanced RAG Patterns

### Hybrid Search (Keyword + Semantic)

```python
def hybrid_search(query: str, k: int = 5) -> List[Dict]:
    semantic_results = vector_db.search(get_embedding(query), k=k)
    keyword_results = elasticsearch.search(query, k=k)
    combined = reciprocal_rank_fusion(semantic_results, keyword_results)
    return combined[:k]
```

### Re-ranking

```python
from sentence_transformers import CrossEncoder

def rerank_results(query: str, documents: List[str], k: int = 5) -> List[str]:
    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = [[query, doc] for doc in documents]
    scores = model.predict(pairs)
    ranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:k]]
```

---

# 4. Agentic AI Application Deployment

## What Makes an Agent?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT COMPONENTS                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         LLM BRAIN                                │  │
│   │   • Understands user intent                                      │  │
│   │   • Plans actions                                                │  │
│   │   • Decides which tools to use                                   │  │
│   │   • Synthesizes final response                                   │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│              ┌───────────────┼───────────────┐                         │
│              │               │               │                          │
│              ▼               ▼               ▼                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │    TOOL 1    │  │    TOOL 2    │  │    TOOL 3    │                 │
│   │  (Search)    │  │  (Calculator)│  │   (API)      │                 │
│   └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         MEMORY                                   │  │
│   │   • Short-term: Current conversation                             │  │
│   │   • Long-term: Past interactions, learned preferences            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## ReAct (Reasoning + Acting) Pattern

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ReAct LOOP EXAMPLE                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User: "What's the weather in NYC and should I bring an umbrella?"     │
│                                    │                                    │
│                                    ▼                                    │
│   THOUGHT 1: I need to get the current weather for NYC.                 │
│   ACTION 1: Call weather_tool("New York City")                          │
│                                    │                                    │
│                                    ▼                                    │
│   OBSERVATION 1: {"temp": 65, "condition": "Cloudy", "rain_chance": 70%}│
│                                    │                                    │
│                                    ▼                                    │
│   THOUGHT 2: 70% rain chance - user should bring umbrella.              │
│   ACTION 2: respond_to_user                                             │
│                                    │                                    │
│                                    ▼                                    │
│   Final Answer: "It's 65°F in NYC with 70% rain chance.                 │
│                  I recommend bringing an umbrella."                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Building a Tool-Using Agent

### Step 1: Define Tools

```python
from typing import Callable, Dict, Any
from dataclasses import dataclass
import math

@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict
    function: Callable

def search_web(query: str) -> str:
    """Search the web for information"""
    # Replace with actual API
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    """Safely evaluate mathematical expression"""
    allowed = {'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'abs': abs}
    try:
        result = eval(expression, {"__builtins__": {}, **allowed})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(location: str) -> str:
    """Get weather for a location"""
    return f"Weather in {location}: 72°F, Sunny"

TOOLS = {
    "search_web": Tool(
        name="search_web",
        description="Search the web for information",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Search query"}},
            "required": ["query"]
        },
        function=search_web
    ),
    "calculate": Tool(
        name="calculate",
        description="Perform mathematical calculations",
        parameters={
            "type": "object",
            "properties": {"expression": {"type": "string", "description": "Math expression"}},
            "required": ["expression"]
        },
        function=calculate
    ),
    "get_weather": Tool(
        name="get_weather",
        description="Get current weather for a location",
        parameters={
            "type": "object",
            "properties": {"location": {"type": "string", "description": "City name"}},
            "required": ["location"]
        },
        function=get_weather
    )
}
```

### Step 2: Build the Agent

```python
import json
from typing import List, Dict, Any
import boto3

class ToolUsingAgent:
    def __init__(self, tools: Dict[str, Tool], model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'):
        self.tools = tools
        self.model_id = model_id
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.conversation_history = []
        self.max_iterations = 10
    
    def _format_tools_for_llm(self) -> List[Dict]:
        return [
            {"name": tool.name, "description": tool.description, "input_schema": tool.parameters}
            for tool in self.tools.values()
        ]
    
    def _call_llm(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": messages,
            "tools": tools
        })
        response = self.bedrock.invoke_model(modelId=self.model_id, body=body)
        return json.loads(response['body'].read())
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> Any:
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        try:
            return self.tools[tool_name].function(**tool_input)
        except Exception as e:
            return {"error": str(e)}
    
    def run(self, user_message: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})
        tools = self._format_tools_for_llm()
        
        for _ in range(self.max_iterations):
            response = self._call_llm(self.conversation_history, tools)
            stop_reason = response.get('stop_reason')
            content = response.get('content', [])
            
            self.conversation_history.append({"role": "assistant", "content": content})
            
            if stop_reason == 'end_turn':
                for block in content:
                    if block.get('type') == 'text':
                        return block.get('text', '')
                return ""
            
            if stop_reason == 'tool_use':
                tool_results = []
                for block in content:
                    if block.get('type') == 'tool_use':
                        result = self._execute_tool(block['name'], block.get('input', {}))
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block['id'],
                            "content": json.dumps(result)
                        })
                self.conversation_history.append({"role": "user", "content": tool_results})
        
        return "Agent reached maximum iterations."

# Usage
agent = ToolUsingAgent(tools=TOOLS)
response = agent.run("What's the weather in San Francisco and what's 25 * 4?")
print(response)
```

### Step 3: FastAPI Service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Agent API")
agents = {}

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in agents:
        agents[session_id] = ToolUsingAgent(tools=TOOLS)
    
    try:
        response = agents[session_id].run(request.message)
        return ChatResponse(session_id=session_id, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    if session_id in agents:
        del agents[session_id]
    return {"message": "Session deleted"}
```

## Multi-Agent Patterns

### Pattern 1: Hierarchical (Manager-Worker)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL MULTI-AGENT SYSTEM                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌───────────────────┐                           │
│                         │   MANAGER AGENT   │                           │
│                         │   (Orchestrator)  │                           │
│                         └─────────┬─────────┘                           │
│                                   │                                     │
│                   ┌───────────────┼───────────────┐                     │
│                   │               │               │                     │
│                   ▼               ▼               ▼                     │
│   ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐    │
│   │  RESEARCH AGENT   │ │   WRITER AGENT    │ │  REVIEWER AGENT   │    │
│   │  • Web search     │ │  • Content writing│ │  • Quality check  │    │
│   └───────────────────┘ └───────────────────┘ └───────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Pipeline (Sequential)

```
Input ──► Agent 1 (Parser) ──► Agent 2 (Enricher) ──► Agent 3 (Analyzer) ──► Output
```

## Cloud Deployment for Agents

### AWS Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                AWS MULTI-AGENT DEPLOYMENT                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Client ──► API Gateway ──► Lambda/ECS (Orchestrator)                  │
│                                      │                                  │
│                     ┌────────────────┼────────────────┐                 │
│                     │                │                │                 │
│                     ▼                ▼                ▼                 │
│              Step Functions    SQS Queues       DynamoDB                │
│              (Workflow)        (Messaging)      (State)                 │
│                     │                │                │                 │
│                     └────────────────┼────────────────┘                 │
│                                      │                                  │
│                                      ▼                                  │
│                               Bedrock (LLM)                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Safety Guardrails

```python
import re

class AgentGuardrails:
    def __init__(self):
        self.blocked_patterns = [
            r"rm\s+-rf",
            r"DROP\s+TABLE",
            r"DELETE\s+FROM.*WHERE\s+1=1",
        ]
        self.max_tool_calls = 20
    
    def validate_tool_input(self, tool_name: str, input_data: dict) -> bool:
        input_str = str(input_data)
        for pattern in self.blocked_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                return False
        return True
    
    def validate_output(self, output: str) -> str:
        # Remove PII
        output = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', output)
        output = re.sub(r'\b\d{16}\b', '[CARD REDACTED]', output)
        return output
```

---

# 5. Best Practices

## Security Best Practices

### Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   1. PERIMETER: WAF, DDoS Protection, Rate Limiting                     │
│                              │                                          │
│                              ▼                                          │
│   2. AUTH: API Keys, JWT, OAuth 2.0, IAM Roles                          │
│                              │                                          │
│                              ▼                                          │
│   3. NETWORK: VPC, Private Subnets, Security Groups                     │
│                              │                                          │
│                              ▼                                          │
│   4. DATA: Encryption at rest (KMS), Encryption in transit (TLS)        │
│                              │                                          │
│                              ▼                                          │
│   5. APPLICATION: Input validation, Prompt injection protection         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Secret Management

```python
# AWS Secrets Manager
import boto3
import json

def get_secret(secret_name: str) -> dict:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

secrets = get_secret('my-app/production')
api_key = secrets['OPENAI_API_KEY']
```

```python
# GCP Secret Manager
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')
```

### Prompt Injection Protection

```python
import re
from typing import Tuple

class PromptSafetyChecker:
    INJECTION_PATTERNS = [
        r"ignore (previous|all|above) instructions",
        r"disregard (previous|all|above)",
        r"you are now",
        r"system prompt:",
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
    
    def check(self, user_input: str) -> Tuple[bool, str]:
        for pattern in self.patterns:
            if pattern.search(user_input):
                return False, f"Potential injection detected"
        return True, "Input appears safe"
    
    def sanitize(self, user_input: str) -> str:
        sanitized = re.sub(r'<\|[^|]+\|>', '', user_input)
        sanitized = sanitized.replace('{', '{{').replace('}', '}}')
        return sanitized
```

## Scalability Best Practices

### Auto-Scaling Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUTO-SCALING                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Load Balancer ──► Auto Scaling Group                                  │
│                     Min: 2 | Desired: 4 | Max: 20                       │
│                                                                         │
│   Scale OUT when:                     Scale IN when:                    │
│   • CPU > 70% for 2 min              • CPU < 30% for 10 min            │
│   • Latency > 500ms                  • Requests < 10/min               │
│   • Queue depth > 100                                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Caching

```python
import redis
import hashlib
import json
from functools import wraps

class MLCache:
    def __init__(self, redis_host: str, ttl: int = 3600):
        self.redis = redis.Redis(host=redis_host, decode_responses=True)
        self.ttl = ttl
    
    def _generate_key(self, prefix: str, data: dict) -> str:
        data_str = json.dumps(data, sort_keys=True)
        hash_value = hashlib.md5(data_str.encode()).hexdigest()
        return f"{prefix}:{hash_value}"
    
    def get(self, prefix: str, data: dict):
        key = self._generate_key(prefix, data)
        cached = self.redis.get(key)
        return json.loads(cached) if cached else None
    
    def set(self, prefix: str, data: dict, result: dict):
        key = self._generate_key(prefix, data)
        self.redis.setex(key, self.ttl, json.dumps(result))

def cached_prediction(cache: MLCache, prefix: str):
    def decorator(func):
        @wraps(func)
        def wrapper(data: dict, *args, **kwargs):
            cached = cache.get(prefix, data)
            if cached:
                return cached
            result = func(data, *args, **kwargs)
            cache.set(prefix, data, result)
            return result
        return wrapper
    return decorator
```

## Monitoring Best Practices

### ML-Specific Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Inference Latency | Time to generate prediction | > 500ms (p99) |
| Throughput | Requests per second | < 80% of expected |
| Error Rate | Failed predictions | > 1% |
| Token Usage | LLM tokens consumed | > budget |
| Model Drift | Prediction distribution change | Statistical significance |

### Monitoring Implementation

```python
from prometheus_client import Counter, Histogram
import time
from functools import wraps

REQUEST_COUNT = Counter('ml_requests_total', 'Total requests', ['model', 'status'])
REQUEST_LATENCY = Histogram('ml_request_latency_seconds', 'Latency', ['model'])

def monitor_prediction(model_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(model=model_name, status='success').inc()
                REQUEST_LATENCY.labels(model=model_name).observe(time.time() - start_time)
                return result
            except Exception as e:
                REQUEST_COUNT.labels(model=model_name, status='error').inc()
                raise
        return wrapper
    return decorator
```

## Cost Optimization

### Model Tier Routing

```python
from enum import Enum
from dataclasses import dataclass

class ModelTier(Enum):
    CHEAP = "cheap"
    STANDARD = "standard"
    PREMIUM = "premium"

@dataclass
class ModelConfig:
    model_id: str
    cost_per_1k_tokens: float

MODELS = {
    ModelTier.CHEAP: ModelConfig("claude-3-haiku", 0.00025),
    ModelTier.STANDARD: ModelConfig("claude-3-sonnet", 0.003),
    ModelTier.PREMIUM: ModelConfig("claude-3-opus", 0.015)
}

def route_to_model(complexity_score: float) -> ModelConfig:
    if complexity_score < 0.3:
        return MODELS[ModelTier.CHEAP]
    elif complexity_score < 0.7:
        return MODELS[ModelTier.STANDARD]
    return MODELS[ModelTier.PREMIUM]
```

## CI/CD for ML

### GitHub Actions

```yaml
name: ML Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt && pip install pytest
      - run: pytest tests/ --cov=src
      - run: python scripts/validate_model.py
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker build -t $ECR_REGISTRY/ml-api:${{ github.sha }} .
          docker push $ECR_REGISTRY/ml-api:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: |
          aws ecs update-service --cluster production --service ml-api --force-new-deployment
```

---

# 6. Interview Questions & Answers

## ML Deployment Fundamentals

### Q1: How would you deploy a machine learning model to production?

**Answer:**

> "I follow a structured approach:
>
> 1. **Model Preparation**: Serialize model (joblib, ONNX), create inference code, write tests
>
> 2. **Containerization**: Package in Docker with all dependencies, multi-stage builds
>
> 3. **Cloud Deployment**: SageMaker/Vertex AI endpoints or ECS/Cloud Run with auto-scaling
>
> 4. **API Layer**: FastAPI with authentication, rate limiting, input validation
>
> 5. **Monitoring**: Track latency, throughput, error rates, model drift with alerts"

### Q2: Real-time vs Batch inference - when to use each?

**Answer:**

> "**Real-time**: Single predictions, immediate response (< 100ms). Use for fraud detection, chatbots, recommendations. Higher cost, lower latency.
>
> **Batch**: Process large datasets offline. Use for daily reports, bulk scoring. Lower cost, latency acceptable.
>
> Choose real-time for user-facing features, batch for background processing."

### Q3: How do you handle model versioning and rollbacks?

**Answer:**

> "I implement versioning at multiple levels:
>
> 1. **Model Registry**: Store all versions with tags (version, metrics, git commit)
> 2. **Blue-green/Canary deployments**: Keep previous version running
> 3. **Automated rollback**: Trigger on error rate spike or latency increase
> 4. **A/B Testing**: Route traffic percentage to new model before full rollout"

## GenAI & RAG Questions

### Q4: Explain RAG and when to use it over fine-tuning

**Answer:**

> "RAG enhances LLM responses with external document context.
>
> | Aspect | RAG | Fine-tuning |
> |--------|-----|-------------|
> | Data freshness | Update anytime | Requires retraining |
> | Cost | Lower (no training) | Higher (GPU) |
> | Hallucination | Reduced (grounded) | Still possible |
>
> **Use RAG for**: Dynamic knowledge bases, customer support, legal/compliance
>
> **Use fine-tuning for**: Specific output format, domain terminology"

### Q5: How would you evaluate a RAG system?

**Answer:**

> "I evaluate on retrieval and generation:
>
> **Retrieval**: Recall@K, MRR, Precision@K
>
> **Generation**: Faithfulness (matches context?), Answer Relevance, Context Relevance
>
> **End-to-End**: Human evaluation, A/B testing, LLM-as-judge
>
> I create a golden test set, run automated metrics on deployment, block if metrics drop."

### Q6: How do you handle prompt injection attacks?

**Answer:**

> "Multiple defense layers:
>
> 1. **Input validation**: Scan for injection patterns, limit length, sanitize
> 2. **Prompt design**: Clear delimiters, sandboxed user input section
> 3. **Output filtering**: Check for sensitive data leakage
> 4. **Architecture**: Separate sensitive operations from user-facing LLM"

## Infrastructure & Scaling

### Q7: Scale ML system to handle 10x traffic?

**Answer:**

> "Systematic approach:
>
> 1. **Identify bottlenecks**: Profile CPU, memory, I/O, network
> 2. **Horizontal scaling**: Auto-scaling, pre-warm instances
> 3. **Caching**: Redis for embeddings and frequent queries
> 4. **Model optimization**: Quantization (FP32→FP16), ONNX runtime
> 5. **Async processing**: Queue non-urgent requests
> 6. **Database**: Read replicas, connection pooling
>
> For 10x: ~10x instances + caching (50%+ reduction) + model optimization"

### Q8: Compare SageMaker vs Vertex AI

**Answer:**

> | Aspect | SageMaker | Vertex AI |
> |--------|-----------|-----------|
> | Strengths | Mature, extensive | BigQuery integration |
> | LLM Support | Bedrock (Claude) | Gemini (native) |
> | Pricing | Complex | Simpler |
>
> **Choose SageMaker**: AWS-first org, need Claude, using S3/Lambda
>
> **Choose Vertex AI**: GCP-first org, BigQuery, want Gemini
>
> Both work well - default to existing cloud to simplify IAM."

## System Design Questions

### Q9: Design a real-time fraud detection system

```
┌─────────────────────────────────────────────────────────────────┐
│                 FRAUD DETECTION SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Transaction ──► API Gateway ──► Feature Service               │
│                                        │                        │
│                              ┌─────────┼─────────┐              │
│                              ▼         ▼         ▼              │
│                           Redis    DynamoDB   Real-time         │
│                         (velocity) (history)  features          │
│                              │         │         │              │
│                              └─────────┼─────────┘              │
│                                        │                        │
│                                        ▼                        │
│                              ML Model Endpoint                  │
│                              (fraud_score 0-1)                  │
│                                        │                        │
│                                        ▼                        │
│                              Decision Engine                    │
│                              > 0.9: BLOCK                       │
│                              > 0.7: REVIEW                      │
│                              > 0.5: CHALLENGE                   │
│                              else: APPROVE                      │
│                                                                 │
│   Requirements: < 100ms p99, 99.99% availability, 10K TPS       │
└─────────────────────────────────────────────────────────────────┘
```

### Q10: Design a RAG-based customer support chatbot

```
┌─────────────────────────────────────────────────────────────────┐
│              CUSTOMER SUPPORT CHATBOT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   INGESTION: Docs ──► Chunker ──► Embeddings ──► Vector DB      │
│                                                                 │
│   QUERY: User ──► Intent Classify ──► Query Expand ──►          │
│          Retrieve Top-K ──► Rerank ──► LLM Generate             │
│                                                                 │
│   COMPONENTS:                                                   │
│   • Intent Classifier: Route to right knowledge base            │
│   • Query Expansion: Better retrieval                           │
│   • Reranker: Cross-encoder for relevance                       │
│   • Guardrails: Prevent hallucination                           │
│   • Escalation: Route complex issues to humans                  │
│                                                                 │
│   METRICS:                                                      │
│   • Resolution rate (no human needed)                           │
│   • User satisfaction                                           │
│   • Accuracy, Latency < 3s                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Behavioral Questions

### Q11: ML model failed in production - what did you do?

**Answer Framework:**

> "**Situation**: Launched recommendation model with 15% CTR improvement in A/B tests
>
> **Problem**: Quality degraded over 2 weeks - users clicking less
>
> **What I did**:
> 1. Investigated data pipeline - found feature drift
> 2. Discovered data source changed format
> 3. Implemented feature distribution monitoring
> 4. Added automatic drift alerts
> 5. Created rollback automation
>
> **Result**: Recovered in 4 hours, drift monitoring caught 3 similar issues
>
> **Learned**: Always monitor input distributions, not just outputs"

### Q12: Prioritize model accuracy vs deployment speed?

**Answer:**

> "Based on use case criticality:
>
> **High Stakes (Healthcare, Finance)**: Prioritize accuracy, extensive validation
>
> **Medium Stakes (Recommendations)**: Balance both, canary deployments, A/B test
>
> **Low Stakes (Internal tools, POCs)**: Prioritize speed, iterate on feedback
>
> Always: MVP first, automated testing, gradual rollout, iterate on production data"

---

# 7. Project Templates & Code

## Project 1: ML Model API Service

### Folder Structure

```
ml-api-service/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── model.py               # Model loading
│   └── schemas.py             # Pydantic models
├── model/
│   └── model.joblib
├── tests/
│   └── test_app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### src/app.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import joblib
import numpy as np
import time
import os

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

MODEL_PATH = os.getenv("MODEL_PATH", "model/model.joblib")
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
vectorizer = model_data['vectorizer']

class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    latency_ms: float

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    start_time = time.time()
    
    features = vectorizer.transform([request.text])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = float(np.max(probabilities))
    
    sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
    
    return PredictionResponse(
        text=request.text,
        sentiment=sentiment_map.get(prediction, 'unknown'),
        confidence=round(confidence, 4),
        latency_ms=round((time.time() - start_time) * 1000, 2)
    )
```

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY model/ ./model/

ENV MODEL_PATH=/app/model/model.joblib
EXPOSE 8080

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

### Deploy Commands

```bash
# GCP Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/sentiment-api
gcloud run deploy sentiment-api \
    --image gcr.io/PROJECT_ID/sentiment-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --min-instances 1

# AWS ECS
aws ecr create-repository --repository-name sentiment-api
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t sentiment-api .
docker tag sentiment-api:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest
```

## Project 2: RAG Document Q&A

### Core Components

```python
# ingestion/chunker.py
from typing import List
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    metadata: dict
    chunk_index: int

class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, metadata: dict = None) -> List[Chunk]:
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            if end < len(text):
                last_period = chunk_text.rfind('.')
                if last_period > self.chunk_size * 0.5:
                    chunk_text = chunk_text[:last_period + 1]
                    end = start + last_period + 1
            
            chunks.append(Chunk(
                text=chunk_text.strip(),
                metadata={**(metadata or {}), 'chunk_index': chunk_index},
                chunk_index=chunk_index
            ))
            
            start = end - self.overlap
            chunk_index += 1
        
        return chunks
```

```python
# retrieval/vector_store.py
from typing import List, Dict

class VectorStore:
    def __init__(self, embedding_client, db_client):
        self.embedder = embedding_client
        self.db = db_client
    
    def add_documents(self, documents: List[Dict]):
        texts = [doc['text'] for doc in documents]
        embeddings = self.embedder.embed_batch(texts)
        
        for doc, embedding in zip(documents, embeddings):
            self.db.upsert(
                id=doc['id'],
                vector=embedding,
                metadata={'text': doc['text'], **doc.get('metadata', {})}
            )
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        query_embedding = self.embedder.embed(query)
        results = self.db.search(vector=query_embedding, top_k=k)
        return [
            {'id': r['id'], 'text': r['metadata']['text'], 'score': r['score']}
            for r in results
        ]
```

```python
# generation/llm.py
import boto3
import json
from typing import List, Dict

class LLMClient:
    def __init__(self, model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = model_id
    
    def generate(self, query: str, context_docs: List[Dict]) -> str:
        context = "\n\n".join([f"Document {i+1}:\n{doc['text']}" for i, doc in enumerate(context_docs)])
        
        prompt = f"""Answer based on the documents provided.

Documents:
{context}

Question: {query}

Answer:"""
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.bedrock.invoke_model(modelId=self.model_id, body=body)
        return json.loads(response['body'].read())['content'][0]['text']
```

## Project 3: AI Agent with Tools

See Section 4 for complete implementation.

---

# 8. Real-World Deployment Examples

## Example 1: E-Commerce Recommendation System

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│            E-COMMERCE RECOMMENDATION SYSTEM                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Website ──► API Gateway ──► Feature Service ──► Redis (cache)         │
│                                     │                                   │
│                                     ▼                                   │
│                              SageMaker Endpoint                         │
│                              (XGBoost model)                            │
│                                     │                                   │
│                                     ▼                                   │
│                              DynamoDB (products)                        │
│                                     │                                   │
│                                     ▼                                   │
│                              Response: Top 20 products                  │
│                                                                         │
│   OFFLINE: S3 (events) ──► Spark/EMR ──► Model Retrain (daily)         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cost Estimate (Monthly)

| Component | Configuration | Cost |
|-----------|--------------|------|
| SageMaker | ml.c5.xlarge x 4 | $1,200 |
| ElastiCache | r6g.large x 2 | $400 |
| Lambda | 10M invocations | $200 |
| API Gateway | 10M requests | $35 |
| DynamoDB | On-demand | $300 |
| **Total** | | **~$2,135** |

## Example 2: Customer Support RAG Chatbot

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│              CUSTOMER SUPPORT RAG CHATBOT (GCP)                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Customer ──► Cloud Run (FastAPI) ──► Intent Classifier                │
│                        │                    │                           │
│                        │         ┌──────────┴──────────┐                │
│                        │         │                     │                │
│                        │    RAG Pipeline         Escalate to            │
│                        │         │              Human Agent             │
│                        │         ▼                                      │
│                        │  Vertex AI Embeddings                          │
│                        │         │                                      │
│                        │         ▼                                      │
│                        │  Vector Search (50K docs)                      │
│                        │         │                                      │
│                        │         ▼                                      │
│                        │  Gemini Pro (generate)                         │
│                        │         │                                      │
│                        └─────────┴──► Response + Sources                │
│                                                                         │
│   INGESTION: Cloud Storage ──► Cloud Function ──► Vector Search         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cost Estimate (Monthly)

| Component | Configuration | Cost |
|-----------|--------------|------|
| Cloud Run | 2 vCPU, 2GB, ~3 instances | $150 |
| Vertex AI Embeddings | 500K requests | $50 |
| Vector Search | 50K vectors | $200 |
| Gemini Pro | 5K conversations | $150 |
| **Total** | | **~$550** |

## Example 3: Real-Time Fraud Detection

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                 FRAUD DETECTION SYSTEM (AWS)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Payment ──► ALB ──► ECS Fargate (Feature Service)                     │
│                              │                                          │
│                     ┌────────┼────────┐                                 │
│                     ▼        ▼        ▼                                 │
│                  Redis   DynamoDB  Real-time                            │
│                (velocity) (history) features                            │
│                     │        │        │                                 │
│                     └────────┼────────┘                                 │
│                              │                                          │
│                              ▼                                          │
│                    SageMaker Endpoint                                   │
│                    (XGBoost, ml.c5.xlarge x 6)                         │
│                    Latency: ~15ms p99                                   │
│                              │                                          │
│                              ▼                                          │
│                    Decision Engine                                      │
│                    > 0.9: BLOCK | > 0.7: REVIEW | > 0.5: CHALLENGE      │
│                                                                         │
│   Requirements: < 50ms p99, 99.99% availability, 1000 TPS               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Feature Service Code

```python
import redis
import boto3
import time

class FraudFeatureService:
    def __init__(self):
        self.redis = redis.Redis(host='fraud-cache.xxx.cache.amazonaws.com')
        self.dynamodb = boto3.resource('dynamodb')
        self.user_table = self.dynamodb.Table('user_profiles')
        self.sagemaker = boto3.client('sagemaker-runtime')
    
    def compute_features(self, transaction: dict) -> dict:
        user_id = transaction['user_id']
        realtime = self._get_realtime_features(user_id, transaction)
        historical = self._get_historical_features(user_id)
        txn_features = self._compute_txn_features(transaction)
        return {**realtime, **historical, **txn_features}
    
    def _get_realtime_features(self, user_id: str, txn: dict) -> dict:
        pipe = self.redis.pipeline()
        pipe.incr(f"txn_count_1h:{user_id}")
        pipe.expire(f"txn_count_1h:{user_id}", 3600)
        pipe.sadd(f"devices_24h:{user_id}", txn.get('device_id'))
        pipe.scard(f"devices_24h:{user_id}")
        results = pipe.execute()
        return {'txn_count_1h': results[0], 'unique_devices_24h': results[3]}
    
    def _get_historical_features(self, user_id: str) -> dict:
        response = self.user_table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            return {'account_age_days': 0, 'avg_txn_amount': 0}
        item = response['Item']
        return {
            'account_age_days': item.get('account_age_days', 0),
            'avg_txn_amount': float(item.get('avg_txn_amount', 0))
        }
    
    def score_transaction(self, features: dict) -> float:
        payload = ','.join([str(features.get(f, 0)) for f in FEATURE_ORDER])
        response = self.sagemaker.invoke_endpoint(
            EndpointName='fraud-detection-endpoint',
            ContentType='text/csv',
            Body=payload
        )
        return float(response['Body'].read().decode())
```

---

# 9. End-to-End Deployment Walkthrough

## Complete Example: Sentiment Analysis API

### Step 1: Train Model

```python
# train_model.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Sample data
texts = [
    "I love this product!", "This is amazing!", "Great quality!",
    "Terrible product", "Waste of money", "Very disappointed",
    "It's okay", "Average product", "Nothing special"
] * 100

labels = [2, 2, 2, 0, 0, 0, 1, 1, 1] * 100  # 0=negative, 1=neutral, 2=positive

X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

print(f"Accuracy: {model.score(vectorizer.transform(X_test), y_test):.2%}")

joblib.dump({'model': model, 'vectorizer': vectorizer}, 'sentiment_model.joblib')
print("Model saved!")
```

### Step 2: Create FastAPI App

```python
# src/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
import time
import os

app = FastAPI(title="Sentiment Analysis API")

MODEL_PATH = os.getenv("MODEL_PATH", "sentiment_model.joblib")
data = joblib.load(MODEL_PATH)
model, vectorizer = data['model'], data['vectorizer']

class Request(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class Response(BaseModel):
    sentiment: str
    confidence: float
    latency_ms: float

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict", response_model=Response)
def predict(req: Request):
    start = time.time()
    vec = vectorizer.transform([req.text])
    pred = model.predict(vec)[0]
    proba = model.predict_proba(vec)[0]
    
    return Response(
        sentiment=['negative', 'neutral', 'positive'][pred],
        confidence=round(float(np.max(proba)), 4),
        latency_ms=round((time.time() - start) * 1000, 2)
    )
```

### Step 3: Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY sentiment_model.joblib .
ENV MODEL_PATH=/app/sentiment_model.joblib
EXPOSE 8080
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Step 4: requirements.txt

```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
scikit-learn==1.3.0
joblib==1.3.0
numpy==1.24.0
```

### Step 5: Test Locally

```bash
# Train model
python train_model.py

# Build and run
docker build -t sentiment-api .
docker run -p 8080:8080 sentiment-api

# Test
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

### Step 6: Deploy to GCP Cloud Run

```bash
export PROJECT_ID=your-project-id

gcloud builds submit --tag gcr.io/$PROJECT_ID/sentiment-api

gcloud run deploy sentiment-api \
    --image gcr.io/$PROJECT_ID/sentiment-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --min-instances 1

# Get URL and test
URL=$(gcloud run services describe sentiment-api --format 'value(status.url)')
curl -X POST "$URL/predict" -H "Content-Type: application/json" -d '{"text": "I love this!"}'
```

### Step 7: Deploy to AWS ECS

```bash
# Create ECR repository
aws ecr create-repository --repository-name sentiment-api

# Get login and push
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag sentiment-api:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sentiment-api:latest

# Create ECS cluster and deploy (via console or CloudFormation)
```

### Step 8: GitHub Actions CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_CREDENTIALS }}
      - uses: google-github-actions/setup-gcloud@v1
      - run: python train_model.py
      - run: |
          gcloud builds submit --tag gcr.io/$PROJECT_ID/sentiment-api
          gcloud run deploy sentiment-api --image gcr.io/$PROJECT_ID/sentiment-api --region us-central1
```

---

# 10. Quick Reference Cheat Sheet

## Service Mapping

| Purpose | AWS | GCP |
|---------|-----|-----|
| ML Platform | SageMaker | Vertex AI |
| LLM API | Bedrock | Vertex AI (Gemini) |
| Serverless | Lambda | Cloud Functions |
| Containers | ECS / EKS | Cloud Run / GKE |
| Storage | S3 | Cloud Storage |
| Vector DB | OpenSearch | Vertex AI Vector Search |
| Cache | ElastiCache | Memorystore |
| Monitoring | CloudWatch | Cloud Monitoring |
| Secrets | Secrets Manager | Secret Manager |

## Common Commands

### Docker

```bash
docker build -t my-app .
docker run -p 8080:8080 my-app
docker push REGISTRY/my-app:latest
```

### AWS

```bash
# ECR login
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com

# SageMaker endpoint
aws sagemaker create-endpoint --endpoint-name my-endpoint --endpoint-config-name my-config

# Lambda deploy
aws lambda update-function-code --function-name my-func --zip-file fileb://code.zip
```

### GCP

```bash
# Cloud Run deploy
gcloud run deploy SERVICE --image IMAGE --region REGION --allow-unauthenticated

# Vertex AI endpoint
gcloud ai endpoints deploy-model ENDPOINT_ID --model=MODEL_ID --region=REGION
```

## Cost Estimates

| Service | Config | Monthly Cost |
|---------|--------|-------------|
| SageMaker ml.t2.medium | 1 instance | ~$50 |
| SageMaker ml.c5.xlarge | 1 instance | ~$150 |
| Cloud Run | 1 vCPU, 1GB, always-on | ~$40 |
| Bedrock Claude Sonnet | 1M tokens | ~$15 |
| Vertex AI Gemini Pro | 1M tokens | ~$7 |

## Deployment Checklist

- [ ] Model serialized and tested
- [ ] Dockerfile created and tested locally
- [ ] Health endpoint implemented
- [ ] Input validation added
- [ ] Authentication configured
- [ ] Auto-scaling configured
- [ ] Monitoring and logging set up
- [ ] CI/CD pipeline configured
- [ ] Cost alerts set

---

## Learning Path

```
Week 1-2: Fundamentals + Docker
    │
    ▼
Week 3-4: ML/DL Deployment (SageMaker & Vertex AI)
    │
    ▼
Week 5-6: GenAI Deployment (RAG Systems)
    │
    ▼
Week 7-8: Agentic AI + Best Practices
    │
    ▼
Week 9+: Build Projects + Interview Prep
```

---

**Good luck with your interview preparation!**

Build 2-3 projects from this guide and be prepared to discuss:
- Architecture decisions and trade-offs
- How you'd scale to 10x traffic
- Failure modes and recovery strategies
- Cost optimization approaches
