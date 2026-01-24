# Chapter 5: Best Practices for AI Cloud Deployment

## Overview

This chapter covers essential best practices for deploying AI applications in production:
- Security
- Scalability
- Monitoring & Observability
- Cost Optimization
- MLOps & CI/CD

---

## 1. Security Best Practices

### Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS FOR AI APPLICATIONS                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    PERIMETER SECURITY                            │  │
│   │   • WAF (Web Application Firewall)                              │  │
│   │   • DDoS Protection                                             │  │
│   │   • Rate Limiting                                               │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    AUTHENTICATION & AUTHORIZATION                │  │
│   │   • API Keys / JWT Tokens                                       │  │
│   │   • OAuth 2.0 / OIDC                                            │  │
│   │   • IAM Roles (least privilege)                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    NETWORK SECURITY                              │  │
│   │   • VPC / Private Subnets                                       │  │
│   │   • Security Groups / Firewalls                                 │  │
│   │   • VPC Endpoints (no public internet)                          │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    DATA SECURITY                                 │  │
│   │   • Encryption at rest (KMS)                                    │  │
│   │   • Encryption in transit (TLS)                                 │  │
│   │   • Data masking for PII                                        │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│                              ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    APPLICATION SECURITY                          │  │
│   │   • Input validation                                            │  │
│   │   • Prompt injection protection                                 │  │
│   │   • Output sanitization                                         │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Secret Management

**Never hardcode secrets!** Use managed secret services.

```python
# AWS Secrets Manager
import boto3
import json

def get_secret(secret_name: str) -> dict:
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
secrets = get_secret('my-app/production')
api_key = secrets['OPENAI_API_KEY']
```

```python
# GCP Secret Manager
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version: str = 'latest') -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

# Usage
api_key = get_secret('my-project', 'openai-api-key')
```

### IAM Best Practices

```yaml
# AWS IAM Policy - Least Privilege for ML Service
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:InvokeEndpoint"
      ],
      "Resource": "arn:aws:sagemaker:*:*:endpoint/my-model-endpoint"
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/models/*"
    }
  ]
}
```

### Prompt Injection Protection

```python
# prompt_safety.py
import re
from typing import Tuple

class PromptSafetyChecker:
    """Check for prompt injection attacks"""
    
    INJECTION_PATTERNS = [
        r"ignore (previous|all|above) instructions",
        r"disregard (previous|all|above)",
        r"forget (previous|all|everything)",
        r"you are now",
        r"new instructions:",
        r"system prompt:",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
    ]
    
    def __init__(self):
        self.patterns = [re.compile(p, re.IGNORECASE) for p in self.INJECTION_PATTERNS]
    
    def check(self, user_input: str) -> Tuple[bool, str]:
        """
        Check if input contains potential injection.
        Returns (is_safe, reason)
        """
        for pattern in self.patterns:
            if pattern.search(user_input):
                return False, f"Potential injection detected: {pattern.pattern}"
        return True, "Input appears safe"
    
    def sanitize(self, user_input: str) -> str:
        """Remove or escape potentially dangerous content"""
        # Remove special tokens
        sanitized = re.sub(r'<\|[^|]+\|>', '', user_input)
        # Escape curly braces (template injection)
        sanitized = sanitized.replace('{', '{{').replace('}', '}}')
        return sanitized

# Usage
checker = PromptSafetyChecker()
is_safe, reason = checker.check(user_input)
if not is_safe:
    raise ValueError(f"Unsafe input: {reason}")
```

---

## 2. Scalability Best Practices

### Auto-Scaling Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUTO-SCALING ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │                       Load Balancer                               │ │
│   │   (distributes traffic across instances)                         │ │
│   └─────────────────────────────┬────────────────────────────────────┘ │
│                                 │                                       │
│                                 ▼                                       │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │                    Auto Scaling Group                             │ │
│   │                                                                   │ │
│   │   Min: 2  │  Desired: 4  │  Max: 20                              │ │
│   │                                                                   │ │
│   │   ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐                            │ │
│   │   │ I-1 │  │ I-2 │  │ I-3 │  │ I-4 │   ...                      │ │
│   │   └─────┘  └─────┘  └─────┘  └─────┘                            │ │
│   │                                                                   │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                 │                                       │
│                                 │  Metrics                              │
│                                 ▼                                       │
│   ┌──────────────────────────────────────────────────────────────────┐ │
│   │                    Scaling Policies                               │ │
│   │                                                                   │ │
│   │   Scale OUT when:                                                 │ │
│   │   • CPU > 70% for 2 minutes                                      │ │
│   │   • Request latency > 500ms                                      │ │
│   │   • Queue depth > 100                                            │ │
│   │                                                                   │ │
│   │   Scale IN when:                                                  │ │
│   │   • CPU < 30% for 10 minutes                                     │ │
│   │   • Requests per instance < 10/min                               │ │
│   │                                                                   │ │
│   └──────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Caching Strategies

```python
# caching.py
import redis
import hashlib
import json
from typing import Optional
from functools import wraps

class MLCache:
    """Cache for ML predictions"""
    
    def __init__(self, redis_host: str, redis_port: int = 6379, ttl: int = 3600):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = ttl
    
    def _generate_key(self, prefix: str, data: dict) -> str:
        """Generate cache key from input data"""
        data_str = json.dumps(data, sort_keys=True)
        hash_value = hashlib.md5(data_str.encode()).hexdigest()
        return f"{prefix}:{hash_value}"
    
    def get(self, prefix: str, data: dict) -> Optional[dict]:
        """Get cached prediction"""
        key = self._generate_key(prefix, data)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def set(self, prefix: str, data: dict, result: dict):
        """Cache prediction result"""
        key = self._generate_key(prefix, data)
        self.redis.setex(key, self.ttl, json.dumps(result))

# Decorator for caching
def cached_prediction(cache: MLCache, prefix: str):
    def decorator(func):
        @wraps(func)
        def wrapper(data: dict, *args, **kwargs):
            # Try cache first
            cached = cache.get(prefix, data)
            if cached:
                return cached
            
            # Compute prediction
            result = func(data, *args, **kwargs)
            
            # Cache result
            cache.set(prefix, data, result)
            
            return result
        return wrapper
    return decorator

# Usage
cache = MLCache(redis_host='localhost')

@cached_prediction(cache, 'sentiment')
def predict_sentiment(data: dict) -> dict:
    # Expensive model inference
    return model.predict(data)
```

### Async Processing for Long-Running Tasks

```python
# async_processing.py
import boto3
import json
from celery import Celery

# Using Celery with SQS
celery_app = Celery('tasks', broker='sqs://')

@celery_app.task
def process_document(document_id: str, s3_bucket: str, s3_key: str):
    """Async task for document processing"""
    # Download document
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=s3_bucket, Key=s3_key)
    content = response['Body'].read().decode('utf-8')
    
    # Process with model (expensive operation)
    result = expensive_model_inference(content)
    
    # Save result
    save_result(document_id, result)
    
    return {"status": "completed", "document_id": document_id}

# API endpoint
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

@app.post("/process")
async def submit_processing(document_id: str, s3_bucket: str, s3_key: str):
    # Submit async task
    task = process_document.delay(document_id, s3_bucket, s3_key)
    return {"task_id": task.id, "status": "submitted"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": task.status, "result": task.result}
```

---

## 3. Monitoring & Observability

### The Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY FOR AI SYSTEMS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │
│   │     LOGS        │  │    METRICS      │  │    TRACES       │        │
│   │                 │  │                 │  │                 │        │
│   │ • Request/      │  │ • Latency       │  │ • Request flow  │        │
│   │   Response      │  │ • Throughput    │  │   through       │        │
│   │ • Errors        │  │ • Error rates   │  │   services      │        │
│   │ • Model         │  │ • Model         │  │ • Bottleneck    │        │
│   │   predictions   │  │   accuracy      │  │   identification│        │
│   │ • Token usage   │  │ • Token usage   │  │ • Dependency    │        │
│   │                 │  │ • Cost          │  │   mapping       │        │
│   └────────┬────────┘  └────────┬────────┘  └────────┬────────┘        │
│            │                    │                    │                  │
│            └──────────────┬─────┴────────────────────┘                  │
│                           │                                             │
│                           ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    DASHBOARDS & ALERTS                           │  │
│   │                                                                  │  │
│   │   • Real-time monitoring                                        │  │
│   │   • Anomaly detection                                           │  │
│   │   • Alert on threshold breaches                                 │  │
│   │   • On-call notifications                                       │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### ML-Specific Metrics to Monitor

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| **Inference Latency** | Time to generate prediction | > 500ms (p99) |
| **Throughput** | Requests per second | < 80% of expected |
| **Error Rate** | Failed predictions | > 1% |
| **Token Usage** | LLM tokens consumed | > budget |
| **Model Drift** | Prediction distribution change | Statistical significance |
| **Data Drift** | Input feature distribution change | Statistical significance |

### Implementing Monitoring

```python
# monitoring.py
import time
import logging
from prometheus_client import Counter, Histogram, Gauge
from functools import wraps

# Prometheus metrics
REQUEST_COUNT = Counter(
    'ml_requests_total',
    'Total ML prediction requests',
    ['model', 'status']
)

REQUEST_LATENCY = Histogram(
    'ml_request_latency_seconds',
    'ML prediction latency',
    ['model'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

TOKEN_USAGE = Counter(
    'llm_tokens_total',
    'Total LLM tokens used',
    ['model', 'type']  # type: input or output
)

MODEL_PREDICTION_VALUE = Histogram(
    'ml_prediction_value',
    'Distribution of prediction values',
    ['model']
)

# Structured logging
logging.basicConfig(
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def monitor_prediction(model_name: str):
    """Decorator to monitor ML predictions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Record metrics
                latency = time.time() - start_time
                REQUEST_COUNT.labels(model=model_name, status='success').inc()
                REQUEST_LATENCY.labels(model=model_name).observe(latency)
                
                # Log prediction
                logger.info({
                    'event': 'prediction',
                    'model': model_name,
                    'latency_ms': round(latency * 1000, 2),
                    'status': 'success'
                })
                
                return result
                
            except Exception as e:
                REQUEST_COUNT.labels(model=model_name, status='error').inc()
                logger.error({
                    'event': 'prediction_error',
                    'model': model_name,
                    'error': str(e)
                })
                raise
        
        return wrapper
    return decorator

# Usage
@monitor_prediction('sentiment-model')
def predict_sentiment(text: str) -> dict:
    return model.predict(text)
```

### CloudWatch/Cloud Monitoring Setup

```python
# aws_monitoring.py
import boto3

cloudwatch = boto3.client('cloudwatch')

def put_custom_metric(metric_name: str, value: float, unit: str, dimensions: dict):
    """Send custom metric to CloudWatch"""
    cloudwatch.put_metric_data(
        Namespace='AI/Production',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Dimensions': [
                {'Name': k, 'Value': v} for k, v in dimensions.items()
            ]
        }]
    )

# Example: Track token usage
def track_llm_usage(model: str, input_tokens: int, output_tokens: int):
    put_custom_metric(
        'InputTokens',
        input_tokens,
        'Count',
        {'Model': model}
    )
    put_custom_metric(
        'OutputTokens',
        output_tokens,
        'Count',
        {'Model': model}
    )
```

---

## 4. Cost Optimization

### Cost Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI COST BREAKDOWN                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Category          | Daily Cost | Monthly Est. | % of Total            │
│   ─────────────────────────────────────────────────────────────         │
│   LLM API Calls     | $150       | $4,500       | 45%                   │
│   Compute (ECS)     | $80        | $2,400       | 24%                   │
│   Vector Database   | $40        | $1,200       | 12%                   │
│   Storage (S3/GCS)  | $20        | $600         | 6%                    │
│   Data Transfer     | $30        | $900         | 9%                    │
│   Other             | $13        | $400         | 4%                    │
│   ─────────────────────────────────────────────────────────────         │
│   TOTAL             | $333       | $10,000      | 100%                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Cost Optimization Strategies

#### 1. Model Selection

```python
# cost_aware_routing.py
from enum import Enum
from dataclasses import dataclass

class ModelTier(Enum):
    CHEAP = "cheap"      # Fast, simple queries
    STANDARD = "standard" # Most queries
    PREMIUM = "premium"   # Complex reasoning

@dataclass
class ModelConfig:
    model_id: str
    cost_per_1k_tokens: float
    max_context: int

MODELS = {
    ModelTier.CHEAP: ModelConfig(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        cost_per_1k_tokens=0.00025,
        max_context=200000
    ),
    ModelTier.STANDARD: ModelConfig(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        cost_per_1k_tokens=0.003,
        max_context=200000
    ),
    ModelTier.PREMIUM: ModelConfig(
        model_id="anthropic.claude-3-opus-20240229-v1:0",
        cost_per_1k_tokens=0.015,
        max_context=200000
    )
}

def route_to_model(query: str, complexity_score: float) -> ModelConfig:
    """Route query to appropriate model based on complexity"""
    if complexity_score < 0.3:
        return MODELS[ModelTier.CHEAP]
    elif complexity_score < 0.7:
        return MODELS[ModelTier.STANDARD]
    else:
        return MODELS[ModelTier.PREMIUM]
```

#### 2. Caching & Batching

```python
# batch_embeddings.py
from typing import List
import numpy as np

class EmbeddingBatcher:
    """Batch embedding requests to reduce API calls"""
    
    def __init__(self, embedding_fn, batch_size: int = 100):
        self.embedding_fn = embedding_fn
        self.batch_size = batch_size
        self.cache = {}
    
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Get embeddings with caching and batching"""
        results = [None] * len(texts)
        texts_to_embed = []
        indices = []
        
        # Check cache
        for i, text in enumerate(texts):
            if text in self.cache:
                results[i] = self.cache[text]
            else:
                texts_to_embed.append(text)
                indices.append(i)
        
        # Batch embed uncached texts
        for batch_start in range(0, len(texts_to_embed), self.batch_size):
            batch = texts_to_embed[batch_start:batch_start + self.batch_size]
            embeddings = self.embedding_fn(batch)
            
            for j, embedding in enumerate(embeddings):
                idx = indices[batch_start + j]
                results[idx] = embedding
                self.cache[texts_to_embed[batch_start + j]] = embedding
        
        return results
```

#### 3. Spot/Preemptible Instances for Training

```python
# AWS Spot Instance for SageMaker Training
from sagemaker.estimator import Estimator

estimator = Estimator(
    image_uri='your-training-image',
    role='your-role',
    instance_count=1,
    instance_type='ml.p3.2xlarge',
    use_spot_instances=True,              # Enable spot
    max_wait=7200,                         # Max wait time
    max_run=3600,                          # Max run time
    checkpoint_s3_uri='s3://bucket/checkpoints'  # For spot interruptions
)
```

---

## 5. MLOps & CI/CD

### ML CI/CD Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ML CI/CD PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────┐│
│   │  Code   │───►│  Build  │───►│  Test   │───►│ Deploy  │───►│Serve ││
│   │  Push   │    │  Image  │    │  Model  │    │ Staging │    │Prod  ││
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    └──────┘│
│       │              │              │              │              │     │
│   git push      Docker         pytest         Canary         100%      │
│                 build          Model           10%          traffic    │
│                               metrics                                   │
│                                                                         │
│   ════════════════════════════════════════════════════════════════════ │
│                                                                         │
│   AUTOMATED CHECKS:                                                     │
│   ✓ Unit tests pass                                                    │
│   ✓ Model accuracy > threshold                                         │
│   ✓ Latency < threshold                                                │
│   ✓ No security vulnerabilities                                        │
│   ✓ Integration tests pass                                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### GitHub Actions for ML

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Model quality checks
        run: |
          python scripts/validate_model.py
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/ml-api:$IMAGE_TAG .
          docker push $ECR_REGISTRY/ml-api:$IMAGE_TAG
  
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          # Update ECS service with new image
          aws ecs update-service \
            --cluster staging \
            --service ml-api \
            --force-new-deployment
  
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - name: Deploy to production
        run: |
          aws ecs update-service \
            --cluster production \
            --service ml-api \
            --force-new-deployment
```

### Model Validation Script

```python
# scripts/validate_model.py
import json
import sys
from sklearn.metrics import accuracy_score, f1_score
import joblib

def validate_model():
    # Load model
    model = joblib.load('model/model.joblib')
    
    # Load test data
    with open('data/test.json') as f:
        test_data = json.load(f)
    
    X_test = test_data['features']
    y_test = test_data['labels']
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Thresholds
    MIN_ACCURACY = 0.85
    MIN_F1 = 0.80
    
    if accuracy < MIN_ACCURACY:
        print(f"FAIL: Accuracy {accuracy:.4f} < {MIN_ACCURACY}")
        sys.exit(1)
    
    if f1 < MIN_F1:
        print(f"FAIL: F1 {f1:.4f} < {MIN_F1}")
        sys.exit(1)
    
    print("PASS: Model meets quality thresholds")
    sys.exit(0)

if __name__ == "__main__":
    validate_model()
```

---

## Summary Checklist

### Security Checklist
- [ ] Secrets stored in secret manager
- [ ] IAM roles with least privilege
- [ ] VPC configured with private subnets
- [ ] Encryption at rest and in transit
- [ ] Input validation and sanitization
- [ ] Rate limiting configured
- [ ] WAF rules in place

### Scalability Checklist
- [ ] Auto-scaling configured
- [ ] Load balancer health checks
- [ ] Caching implemented
- [ ] Async processing for long tasks
- [ ] Database connection pooling

### Monitoring Checklist
- [ ] Logging configured (structured logs)
- [ ] Metrics exported (latency, throughput, errors)
- [ ] Traces enabled for request flow
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] On-call rotation set up

### Cost Checklist
- [ ] Cost budgets and alerts set
- [ ] Model tier routing implemented
- [ ] Caching for repeated queries
- [ ] Spot instances for training
- [ ] Right-sized instances
- [ ] Auto-scale to zero where possible

---

## Next Steps

Continue to [Chapter 6: Interview Preparation](../06-interview-prep/README.md) for common interview questions and system design scenarios.
