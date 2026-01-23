# Real-World Deployment Examples

This file contains practical, real-world deployment scenarios to complement the fundamentals chapter.

---

## Scenario 1: E-Commerce Product Recommendation System

### Business Context
An e-commerce company wants to show personalized product recommendations to users on their website. They need:
- Real-time recommendations (< 100ms latency)
- Handle 10,000 requests per second during peak hours
- Update recommendations based on user behavior

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│            E-COMMERCE RECOMMENDATION SYSTEM - REAL EXAMPLE                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Website/App                                                               │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────┐                                                       │
│   │ API Gateway     │  ◄── Rate limiting: 1000 req/sec per user            │
│   │ (AWS/GCP)       │                                                       │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────┐     ┌─────────────────┐                              │
│   │ Feature Service │────►│   Redis Cache   │  ◄── User features cached   │
│   │ (Lambda/CF)     │     │ (ElastiCache)   │      TTL: 5 minutes          │
│   └────────┬────────┘     └─────────────────┘                              │
│            │                                                                │
│            │  Features: user_history, cart_items, browsing_session          │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │ ML Model        │  ◄── XGBoost model for ranking                       │
│   │ (SageMaker)     │      Instance: ml.c5.xlarge x 4                      │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            │  Top 20 product IDs with scores                                │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │ Product Service │  ◄── Fetch product details                           │
│   │ (DynamoDB)      │                                                       │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   Response: [{product_id, name, price, image, score}, ...]                  │
│                                                                             │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   OFFLINE PIPELINE (Daily):                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                    │
│   │ User Events │───►│  Spark on   │───►│  Retrain    │                    │
│   │ (S3)        │    │  EMR        │    │  Model      │                    │
│   └─────────────┘    └─────────────┘    └─────────────┘                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Actual AWS Commands to Deploy

```bash
# Step 1: Create ECR Repository
aws ecr create-repository --repository-name recommendation-service --region us-east-1

# Step 2: Build and Push Docker Image
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker build -t recommendation-service .
docker tag recommendation-service:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/recommendation-service:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/recommendation-service:latest

# Step 3: Create SageMaker Endpoint
python deploy_sagemaker.py  # See code below

# Step 4: Create Redis Cache (ElastiCache)
aws elasticache create-cache-cluster \
    --cache-cluster-id recommendation-cache \
    --cache-node-type cache.r6g.large \
    --engine redis \
    --num-cache-nodes 2 \
    --cache-subnet-group-name my-subnet-group

# Step 5: Deploy Lambda for Feature Service
zip -r function.zip feature_service/
aws lambda create-function \
    --function-name recommendation-feature-service \
    --runtime python3.10 \
    --role arn:aws:iam::123456789:role/lambda-role \
    --handler handler.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 \
    --memory-size 1024

# Step 6: Create API Gateway
aws apigatewayv2 create-api \
    --name recommendation-api \
    --protocol-type HTTP \
    --target arn:aws:lambda:us-east-1:123456789:function:recommendation-feature-service
```

### Cost Breakdown (Monthly Estimate)

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| SageMaker Endpoint | ml.c5.xlarge x 4 | $1,200 |
| ElastiCache Redis | r6g.large x 2 | $400 |
| Lambda | 10M invocations | $200 |
| API Gateway | 10M requests | $35 |
| DynamoDB | On-demand | $300 |
| **Total** | | **~$2,135/month** |

---

## Scenario 2: Customer Support Chatbot with RAG

### Business Context
A SaaS company wants to automate customer support using a chatbot that:
- Answers questions from product documentation
- Handles 5,000 conversations per day
- Escalates complex issues to human agents

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              CUSTOMER SUPPORT RAG CHATBOT - REAL EXAMPLE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Customer (Website Widget / Slack / Teams)                                 │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────┐                                                       │
│   │ Cloud Run       │  ◄── FastAPI application                             │
│   │ (Auto-scaling)  │      Min: 1, Max: 10 instances                       │
│   └────────┬────────┘                                                       │
│            │                                                                │
│            ▼                                                                │
│   ┌─────────────────┐                                                       │
│   │ Intent          │  ◄── Simple classifier                               │
│   │ Classifier      │      Routes: FAQ, Technical, Billing, Escalate       │
│   └────────┬────────┘                                                       │
│            │                                                                │
│       ┌────┴────────────────────────────────┐                              │
│       │                                     │                              │
│       ▼                                     ▼                              │
│   ┌─────────────────┐              ┌─────────────────┐                     │
│   │ RAG Pipeline    │              │ Escalate to     │                     │
│   │                 │              │ Human Agent     │                     │
│   │ 1. Embed query  │              │ (Zendesk/       │                     │
│   │ 2. Search docs  │              │  Intercom)      │                     │
│   │ 3. Generate     │              └─────────────────┘                     │
│   └────────┬────────┘                                                       │
│            │                                                                │
│   ┌────────┴────────┐                                                       │
│   │                 │                                                       │
│   ▼                 ▼                                                       │
│  Vertex AI      Vertex AI                                                   │
│  Embeddings     Vector Search     ◄── 50,000 doc chunks indexed            │
│  (Gecko)        (Matching Engine)                                           │
│                      │                                                       │
│                      ▼                                                       │
│              ┌─────────────────┐                                            │
│              │ Vertex AI       │                                            │
│              │ (Gemini Pro)    │  ◄── Generate answer with context         │
│              └────────┬────────┘                                            │
│                       │                                                     │
│                       ▼                                                     │
│              Response + Sources + Confidence Score                          │
│                                                                             │
│   ═══════════════════════════════════════════════════════════════════════  │
│                                                                             │
│   DOCUMENT INGESTION (Triggered on doc updates):                            │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐        │
│   │ Cloud Storage   │───►│ Cloud Function  │───►│ Vector Search   │        │
│   │ (Help docs)     │    │ (Process/Embed) │    │ (Index)         │        │
│   └─────────────────┘    └─────────────────┘    └─────────────────┘        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete GCP Deployment

```bash
# Step 1: Enable required APIs
gcloud services enable \
    run.googleapis.com \
    aiplatform.googleapis.com \
    cloudfunctions.googleapis.com \
    cloudbuild.googleapis.com

# Step 2: Create Vector Search Index
# First, create embeddings and upload to GCS
python create_embeddings.py --input docs/ --output gs://my-bucket/embeddings/

# Create the index (via gcloud or Python SDK)
gcloud ai index create \
    --display-name="support-docs-index" \
    --metadata-file=index_metadata.json \
    --region=us-central1

# Step 3: Deploy the index to an endpoint
gcloud ai index-endpoints create \
    --display-name="support-docs-endpoint" \
    --region=us-central1

gcloud ai index-endpoints deploy-index ENDPOINT_ID \
    --index=INDEX_ID \
    --deployed-index-id="deployed-support-index" \
    --display-name="Deployed Support Index" \
    --region=us-central1

# Step 4: Build and deploy the chatbot service
gcloud builds submit --tag gcr.io/my-project/support-chatbot

gcloud run deploy support-chatbot \
    --image gcr.io/my-project/support-chatbot \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 1 \
    --max-instances 10 \
    --set-env-vars "PROJECT_ID=my-project,INDEX_ENDPOINT_ID=123456"

# Step 5: Deploy document ingestion function
gcloud functions deploy process-docs \
    --runtime python310 \
    --trigger-bucket my-docs-bucket \
    --entry-point process_document \
    --memory 1024MB \
    --timeout 300s
```

### Python Code for the Chatbot Service

```python
# main.py - Complete RAG Chatbot
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel

app = FastAPI(title="Support Chatbot")

# Initialize
PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = "us-central1"
INDEX_ENDPOINT_ID = os.environ["INDEX_ENDPOINT_ID"]

vertexai.init(project=PROJECT_ID, location=LOCATION)
aiplatform.init(project=PROJECT_ID, location=LOCATION)

embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
generation_model = GenerativeModel("gemini-1.5-pro")
index_endpoint = aiplatform.MatchingEngineIndexEndpoint(INDEX_ENDPOINT_ID)

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

class ChatResponse(BaseModel):
    answer: str
    sources: list
    confidence: float
    should_escalate: bool

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Get embedding for the query
    embeddings = embedding_model.get_embeddings([request.message])
    query_embedding = embeddings[0].values
    
    # 2. Search for relevant documents
    response = index_endpoint.find_neighbors(
        deployed_index_id="deployed-support-index",
        queries=[query_embedding],
        num_neighbors=5
    )
    
    # 3. Get document texts (stored in metadata or separate DB)
    context_docs = []
    for neighbor in response[0]:
        # In production, fetch from Firestore/BigQuery
        doc_text = fetch_document(neighbor.id)
        context_docs.append({"id": neighbor.id, "text": doc_text, "score": neighbor.distance})
    
    # 4. Check if we have good enough context
    top_score = context_docs[0]["score"] if context_docs else 0
    should_escalate = top_score > 0.5  # High distance = low relevance
    
    if should_escalate:
        return ChatResponse(
            answer="I'm not confident I can answer this accurately. Let me connect you with a support agent.",
            sources=[],
            confidence=1 - top_score,
            should_escalate=True
        )
    
    # 5. Generate response with context
    context = "\n\n".join([f"Document: {d['text']}" for d in context_docs[:3]])
    
    prompt = f"""You are a helpful customer support assistant. Answer the customer's question based on the documentation provided.

Documentation:
{context}

Customer Question: {request.message}

Instructions:
- Answer based ONLY on the documentation above
- If unsure, say so
- Be concise and helpful
- If the question is about billing, pricing, or account issues, suggest contacting support

Answer:"""
    
    response = generation_model.generate_content(prompt)
    
    return ChatResponse(
        answer=response.text,
        sources=[{"title": d["id"], "relevance": 1-d["score"]} for d in context_docs[:3]],
        confidence=1 - top_score,
        should_escalate=False
    )

@app.get("/health")
def health():
    return {"status": "healthy"}
```

### Cost Breakdown (Monthly Estimate)

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| Cloud Run | 2 vCPU, 2GB, avg 3 instances | $150 |
| Vertex AI Embeddings | 500K requests | $50 |
| Vector Search | 50K vectors, 1 replica | $200 |
| Gemini Pro | 5K conversations x 2K tokens | $150 |
| Cloud Storage | 10 GB | $2 |
| **Total** | | **~$552/month** |

---

## Scenario 3: Real-Time Fraud Detection

### Business Context
A payment processing company needs to detect fraudulent transactions in real-time:
- Process 1,000 transactions per second
- Decision in < 50ms
- 99.99% availability required

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 FRAUD DETECTION SYSTEM - REAL EXAMPLE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   Payment Request                                                           │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    Application Load Balancer                         │  │
│   │                    (Multi-AZ, Health Checks)                        │  │
│   └────────────────────────────┬────────────────────────────────────────┘  │
│                                │                                            │
│                                ▼                                            │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                         ECS Fargate Cluster                          │  │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │  │
│   │   │  Task 1     │  │  Task 2     │  │  Task N     │                │  │
│   │   │  (Feature   │  │  (Feature   │  │  (Feature   │                │  │
│   │   │   Service)  │  │   Service)  │  │   Service)  │                │  │
│   │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                │  │
│   │          │                │                │                        │  │
│   └──────────┼────────────────┼────────────────┼────────────────────────┘  │
│              │                │                │                            │
│              └────────────────┼────────────────┘                            │
│                               │                                             │
│                               ▼                                             │
│   ┌───────────────────────────────────────────────────────────────────────┐│
│   │                    FEATURE COMPUTATION                                 ││
│   │                                                                        ││
│   │  ┌──────────────────┐     ┌──────────────────┐                        ││
│   │  │ Real-time        │     │ Historical       │                        ││
│   │  │ (ElastiCache)    │     │ (DynamoDB)       │                        ││
│   │  │                  │     │                  │                        ││
│   │  │ • Txn velocity   │     │ • Avg txn amount │                        ││
│   │  │ • Recent devices │     │ • Usual locations│                        ││
│   │  │ • Session data   │     │ • Account age    │                        ││
│   │  └──────────────────┘     └──────────────────┘                        ││
│   │                                                                        ││
│   └───────────────────────────────────────────────────────────────────────┘│
│                               │                                             │
│                               │ 50+ features                                │
│                               ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    SageMaker Real-time Endpoint                      │  │
│   │                    (ml.c5.xlarge x 6, Multi-AZ)                     │  │
│   │                                                                      │  │
│   │    ┌─────────────────────────────────────────────────────────────┐  │  │
│   │    │  XGBoost Model                                               │  │  │
│   │    │  • Input: 50 features                                        │  │  │
│   │    │  • Output: fraud_score (0.0 - 1.0)                          │  │  │
│   │    │  • Latency: ~15ms p99                                        │  │  │
│   │    └─────────────────────────────────────────────────────────────┘  │  │
│   │                                                                      │  │
│   └────────────────────────────┬────────────────────────────────────────┘  │
│                                │                                            │
│                                │ fraud_score                                │
│                                ▼                                            │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      DECISION ENGINE                                 │  │
│   │                                                                      │  │
│   │   if fraud_score > 0.9:        → BLOCK (notify customer)            │  │
│   │   elif fraud_score > 0.7:      → REVIEW (send to fraud team)        │  │
│   │   elif fraud_score > 0.5:      → CHALLENGE (3D Secure / OTP)        │  │
│   │   else:                        → APPROVE                             │  │
│   │                                                                      │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Performance Requirements

| Metric | Target | How We Achieve It |
|--------|--------|-------------------|
| Latency (p99) | < 50ms | Warm instances, cached features |
| Throughput | 1,000 TPS | 6 SageMaker instances, load balanced |
| Availability | 99.99% | Multi-AZ, health checks, auto-recovery |
| False Positive Rate | < 1% | Regular model retraining with feedback |

### Feature Service Code

```python
# feature_service.py
import redis
import boto3
from typing import Dict, List
import time

class FraudFeatureService:
    def __init__(self):
        self.redis = redis.Redis(host='fraud-cache.xxxxx.cache.amazonaws.com', port=6379)
        self.dynamodb = boto3.resource('dynamodb')
        self.user_table = self.dynamodb.Table('user_profiles')
        self.sagemaker = boto3.client('sagemaker-runtime')
    
    def compute_features(self, transaction: Dict) -> Dict:
        """Compute all features for fraud scoring"""
        user_id = transaction['user_id']
        
        # Real-time features from Redis
        realtime = self._get_realtime_features(user_id, transaction)
        
        # Historical features from DynamoDB
        historical = self._get_historical_features(user_id)
        
        # Transaction-level features
        txn_features = self._compute_txn_features(transaction)
        
        return {**realtime, **historical, **txn_features}
    
    def _get_realtime_features(self, user_id: str, txn: Dict) -> Dict:
        """Get velocity and session features from Redis"""
        pipe = self.redis.pipeline()
        
        # Transaction count in last hour
        hour_key = f"txn_count_1h:{user_id}"
        pipe.incr(hour_key)
        pipe.expire(hour_key, 3600)
        
        # Unique devices in last 24h
        device_key = f"devices_24h:{user_id}"
        pipe.sadd(device_key, txn.get('device_id', 'unknown'))
        pipe.expire(device_key, 86400)
        pipe.scard(device_key)
        
        # Amount sum in last hour
        amount_key = f"amount_sum_1h:{user_id}"
        pipe.incrbyfloat(amount_key, txn['amount'])
        pipe.expire(amount_key, 3600)
        
        results = pipe.execute()
        
        return {
            'txn_count_1h': results[0],
            'unique_devices_24h': results[4],
            'amount_sum_1h': float(results[5] or 0)
        }
    
    def _get_historical_features(self, user_id: str) -> Dict:
        """Get historical features from DynamoDB"""
        response = self.user_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return {
                'account_age_days': 0,
                'avg_txn_amount': 0,
                'total_txn_count': 0,
                'usual_country': 'unknown'
            }
        
        item = response['Item']
        return {
            'account_age_days': item.get('account_age_days', 0),
            'avg_txn_amount': float(item.get('avg_txn_amount', 0)),
            'total_txn_count': item.get('total_txn_count', 0),
            'usual_country': item.get('usual_country', 'unknown')
        }
    
    def _compute_txn_features(self, txn: Dict) -> Dict:
        """Compute transaction-specific features"""
        return {
            'amount': txn['amount'],
            'is_international': txn.get('country') != txn.get('usual_country'),
            'hour_of_day': time.localtime().tm_hour,
            'day_of_week': time.localtime().tm_wday,
            'is_weekend': time.localtime().tm_wday >= 5
        }
    
    def score_transaction(self, features: Dict) -> float:
        """Call SageMaker endpoint for fraud score"""
        # Convert features to CSV format expected by XGBoost
        feature_values = [str(features.get(f, 0)) for f in FEATURE_ORDER]
        payload = ','.join(feature_values)
        
        response = self.sagemaker.invoke_endpoint(
            EndpointName='fraud-detection-endpoint',
            ContentType='text/csv',
            Body=payload
        )
        
        result = response['Body'].read().decode('utf-8')
        return float(result)
```

---

## Key Takeaways for Interviews

When discussing these scenarios in interviews, emphasize:

1. **Trade-offs you made**
   - Cost vs latency
   - Accuracy vs speed
   - Complexity vs maintainability

2. **Scaling considerations**
   - How would you handle 10x traffic?
   - What breaks first under load?

3. **Failure modes**
   - What happens if the ML model is slow?
   - How do you handle cache misses?

4. **Monitoring**
   - What metrics do you track?
   - How do you detect model degradation?

5. **Cost optimization**
   - Where are the major cost drivers?
   - How would you reduce costs by 50%?
