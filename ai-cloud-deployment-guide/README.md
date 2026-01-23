# AI Cloud Deployment Guide for Interview Preparation

A comprehensive guide for deploying ML/DL, GenAI, and Agentic AI applications on AWS and GCP.

## Who is this for?

- Engineers with 2+ years experience preparing for cloud AI/ML roles
- Anyone looking to learn practical cloud deployment for AI applications
- Interview preparation for ML Engineer, AI Engineer, and MLOps roles

## Prerequisites

- Python programming experience
- Basic understanding of ML/DL concepts
- Familiarity with Docker basics (helpful but not required)

---

## Guide Structure

### 1. [Fundamentals](./01-fundamentals/README.md)
- Cloud deployment concepts
- AWS vs GCP service comparison
- Essential tools (Docker, APIs, CI/CD)

### 2. [ML/DL Deployment](./02-ml-dl-deployment/README.md)
- AWS SageMaker deployment
- GCP Vertex AI deployment
- Containerized model serving
- Real-time vs batch inference

### 3. [GenAI Deployment (LLM & RAG)](./03-genai-deployment/README.md)
- LLM application architecture
- RAG system design and deployment
- AWS Bedrock integration
- GCP Vertex AI for GenAI

### 4. [Agentic AI Deployment](./04-agentic-ai-deployment/README.md)
- Agent architectures
- Tool-using agents deployment
- Multi-agent systems
- Orchestration patterns

### 5. [Best Practices](./05-best-practices/README.md)
- Security
- Scalability
- Monitoring and observability
- Cost optimization

### 6. [Interview Preparation](./06-interview-prep/README.md)
- Common interview questions with answers
- System design scenarios
- Whiteboard exercises

### 7. [Project Templates](./07-project-templates/README.md)
- Ready-to-use code templates
- Sample projects to build and showcase
- Folder structures

---

## Quick Start Commands

### AWS CLI Setup
```bash
# Install AWS CLI
pip install awscli boto3 sagemaker

# Configure credentials
aws configure
```

### GCP CLI Setup
```bash
# Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Docker Basics
```bash
# Build image
docker build -t my-ml-app .

# Run locally
docker run -p 8080:8080 my-ml-app

# Push to registry (AWS ECR)
aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ECR_URL
docker tag my-ml-app:latest YOUR_ECR_URL/my-ml-app:latest
docker push YOUR_ECR_URL/my-ml-app:latest

# Push to registry (GCP Artifact Registry)
gcloud auth configure-docker
docker tag my-ml-app gcr.io/YOUR_PROJECT/my-ml-app
docker push gcr.io/YOUR_PROJECT/my-ml-app
```

---

## Service Quick Reference

| What You Need | AWS Service | GCP Service |
|--------------|-------------|-------------|
| ML Platform | SageMaker | Vertex AI |
| LLM API | Bedrock | Vertex AI (Gemini) |
| Serverless Compute | Lambda | Cloud Functions |
| Container Platform | ECS / EKS | Cloud Run / GKE |
| Object Storage | S3 | Cloud Storage |
| Vector Database | OpenSearch | Vertex AI Vector Search |
| API Gateway | API Gateway | Cloud Endpoints |
| Monitoring | CloudWatch | Cloud Monitoring |
| Secret Management | Secrets Manager | Secret Manager |
| Queue/Messaging | SQS | Pub/Sub |

---

## Learning Path Recommendation

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

## How to Use This Guide

1. **Read sequentially** if you're new to cloud deployment
2. **Jump to specific sections** if you need focused learning
3. **Use the code templates** to build real projects
4. **Practice interview questions** before interviews
5. **Build at least 2-3 projects** from the project templates section

Good luck with your interview preparation!
