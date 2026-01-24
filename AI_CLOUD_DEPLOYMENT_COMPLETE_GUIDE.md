# AI Cloud Deployment Guide - Interview Ready

**A concise guide focused on what to say in interviews about deploying AI applications on AWS and GCP.**

---

## Table of Contents

1. [Fundamentals & Key Concepts](#1-fundamentals--key-concepts)
2. [ML/DL Model Deployment](#2-mldl-model-deployment)
3. [GenAI & RAG Deployment](#3-genai--rag-deployment)
4. [Agentic AI Deployment](#4-agentic-ai-deployment)
5. [Best Practices](#5-best-practices)
6. [Interview Questions & Answers](#6-interview-questions--answers)
7. [Real-World Scenarios](#7-real-world-scenarios)
8. [Quick Reference Cheat Sheet](#8-quick-reference-cheat-sheet)

---

# 1. Fundamentals & Key Concepts

## Why Cloud Deployment?

| Benefit | What to Say in Interview |
|---------|-------------------------|
| **Scalability** | "Cloud auto-scales based on traffic - handles 10 or 10 million users" |
| **Reliability** | "99.9%+ uptime with automatic failover across availability zones" |
| **Cost Efficiency** | "Pay-per-use model - no idle server costs" |
| **Managed Services** | "Focus on ML logic, cloud handles infrastructure" |

## The Deployment Lifecycle

```
TRAIN → PACKAGE → DEPLOY → SERVE → MONITOR → RETRAIN (loop)
```

**Interview Explanation:**
> "I train the model locally or on cloud, package it in a Docker container with dependencies, deploy to a managed service like SageMaker or Cloud Run, expose via REST API, monitor performance, and retrain when needed."

---

## AWS vs GCP Service Comparison

### Compute Services

| Purpose | AWS | GCP | When to Use |
|---------|-----|-----|-------------|
| ML Platform | **SageMaker** | **Vertex AI** | End-to-end ML lifecycle |
| Serverless | **Lambda** | **Cloud Functions** | Event-driven, light workloads |
| Containers | **ECS/Fargate** | **Cloud Run** | Containerized apps, auto-scale |
| Kubernetes | **EKS** | **GKE** | Complex microservices |

### AI/ML Services

| Purpose | AWS | GCP |
|---------|-----|-----|
| LLM/GenAI | **Bedrock** (Claude, Llama, Titan) | **Vertex AI** (Gemini, PaLM) |
| Embeddings | **Bedrock Titan Embeddings** | **Vertex AI Embeddings** |
| Vector DB | **OpenSearch Serverless** | **Vertex AI Vector Search** |
| AutoML | SageMaker Autopilot | Vertex AI AutoML |

### Supporting Services

| Purpose | AWS | GCP |
|---------|-----|-----|
| Object Storage | S3 | Cloud Storage |
| NoSQL Database | DynamoDB | Firestore |
| Cache | ElastiCache (Redis) | Memorystore |
| Secrets | Secrets Manager | Secret Manager |
| Monitoring | CloudWatch | Cloud Monitoring |
| API Gateway | API Gateway | Cloud Endpoints |

---

## Key Concepts to Know

### Containerization (Docker)
**What it is:** Package your app + all dependencies into a single unit that runs the same everywhere.

**Why needed:** Solves "works on my machine" problem. Same environment in dev, test, and production.

**Interview point:** "I containerize the model with Docker - includes the model file, inference code, and all Python dependencies. This ensures consistent behavior across environments."

### REST APIs
**What it is:** Standard way for applications to communicate over HTTP.

**Interview point:** "I wrap the model in a FastAPI application that exposes a `/predict` endpoint. Clients send JSON with features, get back predictions."

### CI/CD Pipeline
**What it is:** Automated pipeline that builds, tests, and deploys when you push code.

**Interview point:** "I use GitHub Actions to automatically run tests, build Docker image, push to registry, and deploy to production on every merge to main."

---

## Deployment Patterns

### Pattern 1: Real-time Inference
- **Latency:** < 100ms
- **Use cases:** Chatbots, fraud detection, recommendations
- **Services:** SageMaker Endpoints, Vertex AI Endpoints, Cloud Run

### Pattern 2: Batch Inference
- **Latency:** Hours acceptable
- **Use cases:** Daily reports, bulk scoring, ETL
- **Services:** SageMaker Batch Transform, Vertex AI Batch Prediction

### Pattern 3: Streaming Inference
- **Latency:** Near real-time on continuous data
- **Use cases:** IoT sensors, real-time anomaly detection
- **Services:** Kinesis + Lambda, Pub/Sub + Cloud Functions

---

# 2. ML/DL Model Deployment

## Architecture Overview

```
┌────────────────────────────────────────────────────────────┐
│                    ML DEPLOYMENT ARCHITECTURE               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   Client → API Gateway → Load Balancer → Model Service     │
│                                              │             │
│                                    ┌─────────┴─────────┐   │
│                                    │                   │   │
│                                Instance 1         Instance N│
│                                (Model)           (Auto-scaled)
│                                    │                        │
│                             ┌──────┴──────┐                │
│                             │             │                │
│                        Model Registry  Monitoring          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## AWS SageMaker Deployment

### What is SageMaker?
Fully managed ML platform for building, training, and deploying models.

### Deployment Options

| Option | Use Case | Pricing |
|--------|----------|---------|
| **Real-time Endpoints** | Low latency, always-on | Per hour (instance) |
| **Serverless Inference** | Sporadic traffic | Per request + duration |
| **Batch Transform** | Large batch processing | Per hour during job |
| **Multi-Model Endpoints** | Multiple models, save costs | Shared instance |

### Interview Explanation:
> "For deployment, I use SageMaker. I package the model as a tarball with inference code, upload to S3, create a Model object pointing to it, then deploy to an endpoint. I configure auto-scaling based on invocations per instance - scales out at 70% utilization, scales in after 10 minutes of low traffic."

### Key Components:
1. **Model Artifact** - model.tar.gz in S3
2. **Inference Script** - tells SageMaker how to load and predict
3. **Endpoint Configuration** - instance type, count, auto-scaling
4. **Endpoint** - the actual deployed service

---

## GCP Vertex AI Deployment

### What is Vertex AI?
Google's unified ML platform with integrated tools for the full ML lifecycle.

### Deployment Options

| Option | Use Case |
|--------|----------|
| **Online Prediction** | Real-time, low latency |
| **Batch Prediction** | Large datasets |
| **Private Endpoints** | VPC-only access |

### Interview Explanation:
> "On GCP, I use Vertex AI. I upload the model to Cloud Storage, register it in Model Registry, create an endpoint, then deploy with traffic splitting - useful for A/B testing. I typically start with 90/10 split, monitor metrics, then shift traffic to the better model."

### Key Features:
- **Traffic Splitting** - Route % of traffic to different model versions
- **Auto-scaling** - Set min/max replicas, scales based on CPU
- **Model Registry** - Version control for models

---

## Containerized Deployment (Universal)

### When to Use:
- Custom preprocessing logic
- Non-standard frameworks
- Full control over serving

### AWS Path:
```
Docker Image → ECR → ECS/Fargate → ALB → Users
```

### GCP Path:
```
Docker Image → Artifact Registry → Cloud Run → Users
```

### Interview Explanation:
> "For custom requirements, I containerize with Docker. I create a FastAPI app that loads the model on startup, build the image, push to ECR/Artifact Registry, then deploy to ECS Fargate or Cloud Run. Cloud Run is great because it scales to zero - no cost when idle."

---

## Auto-Scaling Configuration

### SageMaker Auto-Scaling:
- **Metric:** InvocationsPerInstance
- **Target:** 70% utilization
- **Scale-out cooldown:** 60 seconds
- **Scale-in cooldown:** 300 seconds

### Cloud Run Auto-Scaling:
- **Metric:** Concurrent requests per instance
- **Min instances:** 1 (or 0 for cost savings)
- **Max instances:** 100 (configurable)

---

# 3. GenAI & RAG Deployment

## Understanding the Difference

| Type | What it is | Use Case |
|------|------------|----------|
| **Simple LLM App** | Direct API call to LLM | Chatbots, summarization |
| **RAG System** | LLM + your documents | Q&A over company docs |
| **Fine-tuned Model** | LLM trained on your data | Domain-specific tasks |

---

## RAG Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INDEXING (Offline):                                            │
│  Documents → Chunk → Embed → Store in Vector DB                 │
│                                                                 │
│  QUERY (Online):                                                │
│  User Query → Embed → Search Vector DB → Get Top-K docs         │
│       │                                                         │
│       └──→ Augmented Prompt (Context + Query) → LLM → Response  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Interview Explanation:
> "RAG works in two phases. Offline: I chunk documents into ~500 token pieces, generate embeddings using Titan or Gecko, store in a vector database like OpenSearch. Online: When a user asks a question, I embed their query, search for top 5 similar chunks, then pass those as context to the LLM with the question. The LLM generates an answer grounded in the retrieved documents."

---

## AWS RAG Stack

| Component | Service | Purpose |
|-----------|---------|---------|
| Documents | S3 | Store source documents |
| Processing | Lambda | Chunk and process documents |
| Embeddings | Bedrock (Titan) | Generate embeddings |
| Vector DB | OpenSearch Serverless | Store and search vectors |
| Generation | Bedrock (Claude) | Generate responses |
| API | API Gateway + Lambda/ECS | Expose to users |

### Interview Explanation:
> "On AWS, I use Bedrock for both embeddings and generation. Titan for embeddings - 1536 dimensions, fast and cheap. Claude for generation - great reasoning. OpenSearch Serverless for vector storage - managed, scales automatically. The whole pipeline is serverless - Lambda for processing, API Gateway for routing."

---

## GCP RAG Stack

| Component | Service | Purpose |
|-----------|---------|---------|
| Documents | Cloud Storage | Store source documents |
| Processing | Cloud Functions | Chunk and process |
| Embeddings | Vertex AI (text-embedding-004) | Generate embeddings |
| Vector DB | Vertex AI Vector Search | Store and search vectors |
| Generation | Vertex AI (Gemini) | Generate responses |
| API | Cloud Run | Expose to users |

### Interview Explanation:
> "On GCP, I use Vertex AI for the full stack. Text-embedding-004 for embeddings, Vector Search for the database - it's a managed Matching Engine, very fast. Gemini Pro for generation. Cloud Run hosts the FastAPI service. I trigger document ingestion from Cloud Storage events via Cloud Functions."

---

## RAG Best Practices

### Chunking Strategy:
- **Size:** 500-1000 tokens per chunk
- **Overlap:** 50-100 tokens between chunks
- **Boundary:** Try to break at sentence/paragraph boundaries

### Retrieval:
- **Top-K:** Start with 5, tune based on results
- **Hybrid Search:** Combine semantic (vector) + keyword (BM25)
- **Re-ranking:** Use cross-encoder to re-rank top results

### Generation:
- **System prompt:** Clear instructions, stay grounded
- **Temperature:** 0.1-0.3 for factual, higher for creative
- **Max tokens:** Set reasonable limit

---

## Prompt Injection Protection

**What it is:** Attackers try to override your system prompt.

**Interview Explanation:**
> "I implement multiple defense layers: input validation to scan for injection patterns, clear delimiters in prompts between system and user content, output filtering to check for sensitive data leakage, and never trust user input directly in prompts."

---

# 4. Agentic AI Deployment

## What Makes an Agent?

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT COMPONENTS                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────────┐  │
│   │                  LLM BRAIN                       │  │
│   │   • Understands intent                          │  │
│   │   • Plans actions                               │  │
│   │   • Decides which tools to use                  │  │
│   └─────────────────────────────────────────────────┘  │
│                         │                               │
│         ┌───────────────┼───────────────┐              │
│         ▼               ▼               ▼              │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐          │
│   │  Tool 1  │   │  Tool 2  │   │  Tool 3  │          │
│   │ (Search) │   │ (Calculate)│  │  (API)   │          │
│   └──────────┘   └──────────┘   └──────────┘          │
│                                                         │
│   ┌─────────────────────────────────────────────────┐  │
│   │                   MEMORY                         │  │
│   │   • Short-term: Current conversation            │  │
│   │   • Long-term: Past interactions                │  │
│   └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Interview Explanation:
> "An agent has three components: an LLM brain that reasons and plans, tools it can call to interact with external systems, and memory to maintain context. The agent follows a ReAct loop - Reason about the task, Act by calling a tool, Observe the result, then decide next step."

---

## ReAct Pattern (Reasoning + Acting)

```
User: "What's the weather in NYC and should I bring an umbrella?"

THOUGHT 1: I need to get NYC weather
ACTION 1: call weather_tool("NYC")
OBSERVATION 1: {"temp": 65, "rain_chance": 70%}

THOUGHT 2: 70% rain chance - recommend umbrella
ACTION 2: respond to user

FINAL: "It's 65°F with 70% rain chance. Bring an umbrella."
```

---

## Multi-Agent Patterns

### Pattern 1: Hierarchical (Manager-Worker)
```
              Manager Agent
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Researcher   Writer    Reviewer
     Agent       Agent      Agent
```
**Use case:** Complex tasks with clear delegation

### Pattern 2: Pipeline (Sequential)
```
Input → Parser Agent → Enricher Agent → Analyzer Agent → Output
```
**Use case:** Sequential processing stages

### Pattern 3: Collaborative (Peer-to-Peer)
**Use case:** Peer review, consensus needed

---

## Cloud Deployment for Agents

### AWS Architecture:
| Component | Service |
|-----------|---------|
| Orchestrator | Lambda or ECS |
| Workflow | Step Functions |
| Messaging | SQS |
| State/Memory | DynamoDB |
| LLM | Bedrock |

### GCP Architecture:
| Component | Service |
|-----------|---------|
| Orchestrator | Cloud Run |
| Workflow | Cloud Workflows |
| Messaging | Pub/Sub |
| State/Memory | Firestore |
| LLM | Vertex AI (Gemini) |

### Interview Explanation:
> "For multi-agent systems, I use Step Functions on AWS or Cloud Workflows on GCP to orchestrate agent execution. Each agent runs as a Lambda/Cloud Function. They communicate via SQS/Pub/Sub queues. State is persisted in DynamoDB/Firestore. This gives me fault tolerance, retry logic, and observability built-in."

---

## Agent Safety Guardrails

**Key protections:**
1. **Input validation** - Block dangerous patterns
2. **Tool restrictions** - Allowlist of permitted tools
3. **Output filtering** - Remove PII, check for harmful content
4. **Rate limiting** - Max tool calls per request
5. **Timeouts** - Max execution time

---

# 5. Best Practices

## Security

### Security Layers:
```
1. PERIMETER: WAF, DDoS protection, Rate limiting
2. AUTH: API keys, JWT, OAuth 2.0, IAM roles
3. NETWORK: VPC, Private subnets, Security groups
4. DATA: Encryption at rest (KMS), Encryption in transit (TLS)
5. APPLICATION: Input validation, Prompt injection protection
```

### Secret Management:
- **AWS:** Secrets Manager
- **GCP:** Secret Manager
- **Rule:** NEVER hardcode secrets, always fetch at runtime

### IAM Best Practice:
> "Least privilege - each service gets only the permissions it needs. My inference service only has InvokeEndpoint permission for SageMaker, nothing else."

---

## Scalability

### Auto-Scaling Strategy:
| Metric | Scale Out | Scale In |
|--------|-----------|----------|
| CPU | > 70% for 2 min | < 30% for 10 min |
| Latency | > 500ms p99 | - |
| Queue depth | > 100 messages | < 10 messages |

### Caching:
- **What to cache:** Embeddings, frequent queries, model weights
- **Service:** ElastiCache (Redis) or Memorystore
- **TTL:** 1 hour for embeddings, 5 min for predictions

### Interview Explanation:
> "For scalability, I configure auto-scaling based on custom metrics. For ML services, I track invocations per instance rather than just CPU. I also implement caching - Redis for embeddings and frequent queries. This reduces load by 50%+ for common requests."

---

## Monitoring & Observability

### Three Pillars:
| Pillar | What to Track |
|--------|---------------|
| **Logs** | Requests, errors, predictions, token usage |
| **Metrics** | Latency, throughput, error rate, model drift |
| **Traces** | Request flow through services |

### ML-Specific Metrics:
| Metric | Alert Threshold |
|--------|-----------------|
| Inference Latency | > 500ms (p99) |
| Error Rate | > 1% |
| Model Drift | Statistical significance |
| Token Usage | > budget |

### Interview Explanation:
> "I implement comprehensive monitoring. CloudWatch/Cloud Monitoring for metrics and logs. I track inference latency, throughput, and error rates. For ML-specific monitoring, I track prediction distribution to detect model drift. Alerts trigger on latency spikes or error rate increases."

---

## Cost Optimization

### Strategies:
1. **Model Routing** - Use cheaper models for simple queries (Haiku vs Opus)
2. **Caching** - Cache embeddings and frequent queries
3. **Spot Instances** - Use for training (60-90% cheaper)
4. **Right-sizing** - Don't over-provision instances
5. **Scale to Zero** - Cloud Run/Serverless for sporadic traffic

### Cost Breakdown Example (RAG System):
| Component | Monthly Cost |
|-----------|-------------|
| LLM API (Claude) | $500-2000 |
| Vector Database | $200-500 |
| Compute (Cloud Run) | $100-300 |
| Storage | $50-100 |

---

# 6. Interview Questions & Answers

## Q1: How would you deploy a machine learning model to production?

> "I follow a structured approach:
> 
> 1. **Package** - Serialize model, create inference code, containerize with Docker
> 2. **Deploy** - Push to ECR/Artifact Registry, deploy to SageMaker or Cloud Run
> 3. **Expose** - Set up API Gateway with authentication and rate limiting
> 4. **Configure** - Auto-scaling based on traffic, min 2 instances for HA
> 5. **Monitor** - Track latency, errors, and model drift with CloudWatch/Cloud Monitoring"

---

## Q2: Real-time vs Batch inference - when to use each?

> "**Real-time** - Single predictions, immediate response (< 100ms). Use for fraud detection, chatbots, recommendations. Deploy as always-on endpoints.
>
> **Batch** - Process large datasets offline. Use for daily reports, bulk scoring. Lower cost per prediction, latency acceptable.
>
> I choose real-time for user-facing features, batch for background processing."

---

## Q3: Explain RAG and when to use it over fine-tuning.

> "RAG retrieves relevant documents and provides them as context to the LLM.
>
> **Use RAG when:**
> - Data changes frequently (just update vector DB)
> - Need to cite sources
> - Want to reduce hallucination
>
> **Use fine-tuning when:**
> - Need specific output format/style
> - Domain terminology
> - Retrieval latency is unacceptable
>
> RAG is cheaper and easier to update. Fine-tuning gives better style control."

---

## Q4: How would you scale an ML system to handle 10x traffic?

> "Systematic approach:
>
> 1. **Profile** - Find bottlenecks (CPU, memory, I/O)
> 2. **Horizontal scaling** - Auto-scaling with pre-warming
> 3. **Caching** - Redis for embeddings and frequent queries (50%+ reduction)
> 4. **Model optimization** - Quantization (FP16), ONNX runtime
> 5. **Async processing** - Queue non-urgent requests
>
> For 10x: ~10x instances + caching + model optimization"

---

## Q5: How do you handle model versioning and rollbacks?

> "I implement versioning at multiple levels:
>
> 1. **Model Registry** - Store all versions with metrics and git commit
> 2. **Blue-green deployments** - Keep previous version running
> 3. **Canary releases** - Route 10% to new model first
> 4. **Automated rollback** - Trigger on error rate spike
>
> In Vertex AI, I use traffic splitting - deploy new model at 10%, monitor 24 hours, then increase."

---

## Q6: Compare SageMaker vs Vertex AI

> "Both are excellent. Choice depends on existing infrastructure:
>
> **Choose SageMaker when:**
> - AWS-first organization
> - Need Claude/Anthropic models (Bedrock)
> - Already using S3, Lambda
>
> **Choose Vertex AI when:**
> - GCP-first organization
> - Heavy BigQuery usage
> - Want Gemini models
>
> For most use cases, default to whichever cloud you're already on."

---

## Q7: How do you handle prompt injection attacks?

> "Multiple defense layers:
>
> 1. **Input validation** - Scan for injection patterns, limit length
> 2. **Prompt design** - Clear delimiters, user input in sandboxed section
> 3. **Output filtering** - Check for sensitive data leakage
> 4. **Architecture** - Separate sensitive operations from user-facing LLM"

---

# 7. Real-World Scenarios

## Scenario 1: E-Commerce Recommendation System

### Architecture:
```
User Request → API Gateway → Feature Service → Redis Cache
                                    │
                                    ▼
                            SageMaker Endpoint (XGBoost)
                                    │
                                    ▼
                            DynamoDB (Products) → Response
```

### Key Points:
- **Latency requirement:** < 100ms
- **Features:** User history, cart items, browsing session
- **Caching:** Redis for user features (5 min TTL)
- **Scaling:** 4 SageMaker instances, auto-scale on invocations

### Cost Estimate: ~$2,000/month
- SageMaker: $1,200
- Redis: $400
- Lambda/API Gateway: $250
- DynamoDB: $150

---

## Scenario 2: Customer Support RAG Chatbot

### Architecture:
```
Customer → Cloud Run (FastAPI) → Intent Classifier
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
              RAG Pipeline                      Escalate to Human
                    │
    Vertex AI Embeddings → Vector Search → Gemini Pro → Response
```

### Key Points:
- **Documents:** 50K chunks from support docs
- **Intent routing:** Simple classifier routes to right knowledge base
- **Escalation:** Route complex issues to human agents
- **Guardrails:** Don't answer outside scope, cite sources

### Cost Estimate: ~$500/month
- Cloud Run: $150
- Embeddings: $50
- Vector Search: $200
- Gemini Pro: $100

---

## Scenario 3: Real-Time Fraud Detection

### Architecture:
```
Transaction → ALB → ECS Fargate (Feature Service)
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
         Redis       DynamoDB    Real-time
       (velocity)   (history)    features
             │            │            │
             └────────────┼────────────┘
                          ▼
                 SageMaker Endpoint → Decision Engine
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                     APPROVE             REVIEW              BLOCK
```

### Key Points:
- **Latency requirement:** < 50ms p99
- **Throughput:** 1,000 TPS
- **Features:** Transaction velocity, device fingerprint, location
- **Decision thresholds:** >0.9 block, >0.7 review, >0.5 challenge

---

# 8. Quick Reference Cheat Sheet

## Service Mapping

| Purpose | AWS | GCP |
|---------|-----|-----|
| ML Platform | SageMaker | Vertex AI |
| LLM API | Bedrock | Vertex AI (Gemini) |
| Serverless Containers | ECS Fargate | Cloud Run |
| Serverless Functions | Lambda | Cloud Functions |
| Vector DB | OpenSearch | Vector Search |
| Object Storage | S3 | Cloud Storage |
| Cache | ElastiCache | Memorystore |
| Secrets | Secrets Manager | Secret Manager |
| Monitoring | CloudWatch | Cloud Monitoring |
| CI/CD | CodePipeline | Cloud Build |

---

## Deployment Commands (Know These)

### AWS:
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker push ACCOUNT.dkr.ecr.REGION.amazonaws.com/my-app:latest

# Deploy SageMaker endpoint
# (via Python SDK or console)

# Update ECS service
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

### GCP:
```bash
# Deploy to Cloud Run
gcloud run deploy my-service --image gcr.io/PROJECT/my-app --region us-central1 --allow-unauthenticated

# Deploy Vertex AI model
# (via Python SDK or console)
```

---

## Cost Estimates (Know the Ballpark)

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| SageMaker ml.t2.medium | 1 instance | ~$50 |
| SageMaker ml.c5.xlarge | 1 instance | ~$150 |
| Cloud Run | 1 vCPU, 1GB, always-on | ~$40 |
| Bedrock Claude Sonnet | 1M tokens | ~$15 |
| Vertex AI Gemini Pro | 1M tokens | ~$7 |
| OpenSearch Serverless | Minimal | ~$200 |
| Vector Search | 50K vectors | ~$200 |

---

## Interview Checklist

Before the interview, be ready to explain:

- [ ] How you containerize ML models (Docker)
- [ ] Difference between SageMaker and Vertex AI
- [ ] When to use real-time vs batch inference
- [ ] How RAG works and when to use it
- [ ] Auto-scaling configuration
- [ ] Monitoring and alerting strategy
- [ ] Cost optimization approaches
- [ ] Security best practices (secrets, IAM, encryption)
- [ ] CI/CD pipeline for ML
- [ ] How you'd handle 10x traffic increase

---

## Key Phrases for Interviews

**On Deployment:**
> "I containerize with Docker, push to ECR/Artifact Registry, deploy to SageMaker/Cloud Run with auto-scaling based on traffic patterns."

**On RAG:**
> "I chunk documents, embed with Titan/Gecko, store in OpenSearch/Vector Search, retrieve top-K at query time, and pass as context to the LLM."

**On Scaling:**
> "I configure auto-scaling based on custom metrics like invocations per instance, implement caching for frequent queries, and use async processing for non-urgent requests."

**On Monitoring:**
> "I track latency, throughput, error rates, and ML-specific metrics like prediction distribution for drift detection. Alerts on threshold breaches."

**On Cost:**
> "I optimize by using appropriate model tiers, caching embeddings, spot instances for training, and scaling to zero for dev environments."

---

**Good luck with your interviews!**

Focus on explaining:
1. What services you'd use and why
2. The architecture and data flow
3. How you'd handle scale and failures
4. Trade-offs you considered
