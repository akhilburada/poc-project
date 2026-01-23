# Chapter 1: Fundamentals of Cloud AI Deployment

## What is Cloud Deployment?

Cloud deployment means running your AI/ML applications on remote servers managed by cloud providers (AWS, GCP) instead of your local machine.

### Why Deploy to Cloud?

| Benefit | Explanation |
|---------|-------------|
| **Scalability** | Handle 10 or 10 million users - cloud scales automatically |
| **Reliability** | 99.9%+ uptime, automatic failover, disaster recovery |
| **Cost Efficiency** | Pay only for what you use (no idle servers) |
| **Global Reach** | Deploy in multiple regions close to your users |
| **Managed Services** | Focus on ML, let cloud handle infrastructure |

---

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

---

## Key Concepts You Must Know

### 1. Containerization (Docker)

**What is it?** A way to package your application with ALL its dependencies into a single unit that runs the same everywhere.

**Why needed?** 
- "It works on my machine" problem solved
- Same environment in development, testing, and production
- Easy to scale and deploy

**Basic Docker Commands:**
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

**What is it?** A way for applications to communicate over HTTP using standard methods (GET, POST, PUT, DELETE).

**For ML/AI:** Your model is wrapped in an API so other applications can send data and get predictions.

```
┌─────────────┐         HTTP POST          ┌─────────────────┐
│   Client    │ ─────────────────────────► │   Your ML API   │
│  (Browser,  │  {"features": [1,2,3,4]}   │  /predict       │
│   App)      │ ◄───────────────────────── │                 │
└─────────────┘  {"prediction": "cat"}     └─────────────────┘
```

### 3. Infrastructure as Code (IaC)

**What is it?** Defining your cloud infrastructure in code files instead of clicking in the console.

**Tools:**
- **Terraform** - Cloud-agnostic, works with AWS, GCP, Azure
- **AWS CloudFormation** - AWS-specific
- **GCP Deployment Manager** - GCP-specific
- **Pulumi** - Uses real programming languages (Python, JS)

**Why needed?**
- Reproducible deployments
- Version control for infrastructure
- Easy to replicate environments (dev, staging, prod)

### 4. CI/CD (Continuous Integration / Continuous Deployment)

**What is it?** Automated pipelines that build, test, and deploy your code when you push changes.

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───►│  Build  │───►│  Test   │───►│ Deploy  │───►│  Live!  │
│  Code   │    │  Image  │    │  Model  │    │ to Cloud│    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
   GitHub       Docker         pytest       AWS/GCP
   GitLab       build          ML tests     services
```

**Tools:**
- GitHub Actions
- GitLab CI/CD
- AWS CodePipeline
- GCP Cloud Build

---

## AWS vs GCP: Complete Service Comparison

### Compute Services

| Purpose | AWS | GCP | When to Use |
|---------|-----|-----|-------------|
| Virtual Machines | EC2 | Compute Engine | Custom setup, full control |
| Serverless Functions | Lambda | Cloud Functions | Event-driven, light workloads |
| Containers (Managed) | ECS | Cloud Run | Containerized apps, auto-scale |
| Kubernetes | EKS | GKE | Complex microservices |

### AI/ML Services

| Purpose | AWS | GCP | Notes |
|---------|-----|-----|-------|
| ML Platform | **SageMaker** | **Vertex AI** | End-to-end ML lifecycle |
| LLM/GenAI | **Bedrock** | **Vertex AI + Gemini** | Foundation models |
| AutoML | SageMaker Autopilot | Vertex AI AutoML | No-code ML |
| Pre-trained APIs | Rekognition, Comprehend | Vision AI, Natural Language | Ready-to-use AI |

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
| CDN | CloudFront | Cloud CDN |
| VPC | VPC | VPC |
| Secrets | Secrets Manager | Secret Manager |
| IAM | IAM | Cloud IAM |

### Monitoring & DevOps

| Purpose | AWS | GCP |
|---------|-----|-----|
| Monitoring | CloudWatch | Cloud Monitoring |
| Logging | CloudWatch Logs | Cloud Logging |
| Tracing | X-Ray | Cloud Trace |
| CI/CD | CodePipeline | Cloud Build |
| Container Registry | ECR | Artifact Registry |

---

## Essential Tools Setup

### Local Development Environment

```bash
# 1. Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate  # Windows

# 2. Install core packages
pip install boto3 google-cloud-aiplatform
pip install fastapi uvicorn
pip install docker

# 3. AWS CLI
pip install awscli
aws configure
# Enter: Access Key, Secret Key, Region, Output format

# 4. GCP CLI
# Download from: https://cloud.google.com/sdk/docs/install
gcloud init
gcloud auth application-default login
```

### Verify Setup

```bash
# AWS
aws sts get-caller-identity  # Should return your account info

# GCP
gcloud auth list  # Should show your account
gcloud config list project  # Should show your project
```

---

## Understanding Model Deployment Patterns

### Pattern 1: Real-time Inference (Synchronous)

```
User Request → API → Model → Response (within milliseconds)
```

**Use Cases:**
- Chatbots
- Fraud detection
- Real-time recommendations
- Image classification

**Requirements:**
- Low latency (< 100ms)
- High availability
- Auto-scaling

### Pattern 2: Batch Inference (Asynchronous)

```
Data Batch → Queue → Model Processing → Results Store
```

**Use Cases:**
- Nightly predictions
- Bulk document processing
- Report generation
- Model retraining

**Requirements:**
- High throughput
- Cost efficiency
- Can tolerate delays

### Pattern 3: Streaming Inference

```
Data Stream → Stream Processor → Model → Output Stream
```

**Use Cases:**
- IoT sensor analysis
- Real-time anomaly detection
- Live video analysis

**Requirements:**
- Continuous processing
- Handling data velocity
- Ordered processing

---

## Cost Awareness

### Pay-Per-Use Pricing Models

| Service Type | AWS Pricing | GCP Pricing |
|-------------|-------------|-------------|
| Compute (EC2/GCE) | Per hour/second | Per second |
| Lambda/Functions | Per request + duration | Per request + duration |
| SageMaker Endpoint | Per hour (instance) | Per hour (node) |
| Storage (S3/GCS) | Per GB stored + requests | Per GB stored + requests |
| Data Transfer | Per GB out | Per GB out |

### Cost Optimization Tips

1. **Use spot/preemptible instances** for training (60-90% cheaper)
2. **Right-size your instances** - don't over-provision
3. **Set up auto-scaling** - scale down when not needed
4. **Use serverless** for sporadic workloads
5. **Monitor with cost alerts** - set budget thresholds

---

## Interview Tip: How to Explain This

When asked "How do you deploy ML models to production?", structure your answer:

1. **Start with the big picture:**
   > "I package the model with its dependencies in a Docker container, deploy it to a cloud service like SageMaker or Vertex AI, and expose it through a REST API."

2. **Add specifics based on requirements:**
   > "For real-time inference, I'd use SageMaker endpoints with auto-scaling. For cost-sensitive batch processing, I'd use Lambda or batch transform jobs."

3. **Mention operational concerns:**
   > "I also set up monitoring for latency, error rates, and model drift, with automated alerts and CI/CD pipelines for updates."

---

## Next Steps

Continue to [Chapter 2: ML/DL Deployment](../02-ml-dl-deployment/README.md) to learn specific deployment techniques for traditional ML and deep learning models.
