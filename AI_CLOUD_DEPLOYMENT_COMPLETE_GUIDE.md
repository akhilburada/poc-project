# AI Cloud Deployment Guide - Beginner Friendly

**Learn cloud deployment from zero knowledge. Simple explanations with real examples.**

---

# PART 1: UNDERSTANDING THE BASICS

---

## What Does "Deployment" Mean?

**Simple Explanation:**
You built an ML model on your laptop. It works great locally. But how do others use it? They can't access your laptop!

**Deployment** = Making your model available on the internet so anyone (or any app) can use it.

**Real-world analogy:**
- Your laptop = Your kitchen where you cook
- Deployment = Opening a restaurant so others can eat your food
- Cloud = A building where you rent restaurant space

---

## What is Cloud?

**Simple Explanation:**
Cloud = Someone else's computers that you rent over the internet.

Instead of buying expensive servers, you rent them from:
- **AWS (Amazon Web Services)** - Amazon's cloud
- **GCP (Google Cloud Platform)** - Google's cloud
- **Azure** - Microsoft's cloud

**Why use cloud?**
| Your Own Server | Cloud |
|-----------------|-------|
| Buy hardware ($10,000+) | Pay monthly ($50-500) |
| You maintain it | They maintain it |
| Fixed capacity | Scale up/down anytime |
| If it breaks, your problem | They fix it |

---

## What is an API?

**Simple Explanation:**
API = A waiter in a restaurant.

You (customer) don't go into the kitchen. You tell the waiter what you want. The waiter goes to kitchen, gets your food, brings it back.

**For ML:**
- Your app = Customer
- API = Waiter
- ML Model = Kitchen

Your app sends data to the API → API sends to model → Model returns prediction → API sends back to your app.

**Example:**
```
Your App: "Is this email spam?" 
    ↓ (sends to API)
API receives request
    ↓ (sends to model)
Model: "Yes, 95% sure it's spam"
    ↓ (returns via API)
Your App: Shows "Spam" label
```

---

## What is Docker?

**Simple Explanation:**
Docker = A shipping container for software.

**Problem:** Your code works on your laptop but fails on the server because:
- Different Python version
- Missing libraries
- Different operating system

**Solution:** Docker packages EVERYTHING together:
- Your code
- Python version
- All libraries
- Settings

Now it runs the same everywhere - your laptop, server, cloud.

**Real-world analogy:**
- Without Docker = Moving house by carrying items loose (things break, get lost)
- With Docker = Moving house with everything in sealed containers (safe, organized)

---

## What is a Container?

**Simple Explanation:**
Container = A running Docker package.

- **Docker Image** = The recipe/blueprint (like a cake recipe)
- **Container** = The actual running thing (like the actual cake)

You create one image, run many containers from it.

---

# PART 2: AWS SERVICES EXPLAINED

---

## AWS Overview

AWS has 200+ services. For ML deployment, you need to know only ~10.

Think of AWS as a huge mall with different shops. Each shop (service) does one thing well.

---

## S3 (Simple Storage Service)

### What is it?
S3 = A giant hard drive in the cloud.

### What does it do?
Stores files - any files: images, videos, documents, ML models, data.

### How it works:
1. You create a "bucket" (like a folder)
2. Upload files to the bucket
3. Access files from anywhere via URL

### Why you need it for ML:
- Store your trained model files
- Store training data
- Store input/output data

### Real-world analogy:
S3 = Google Drive or Dropbox, but for applications.

### Key terms:
- **Bucket** = Top-level folder
- **Object** = Any file you store
- **Key** = File path/name

---

## EC2 (Elastic Compute Cloud)

### What is it?
EC2 = A computer in the cloud that you rent.

### What does it do?
Gives you a virtual server. You can install anything, run any software.

### How it works:
1. Choose instance type (how powerful - CPU, RAM, GPU)
2. Choose operating system (Linux, Windows)
3. Start the instance
4. Connect to it like a remote computer
5. Pay by the hour

### Why you need it for ML:
- Run training jobs (especially with GPU)
- Host your model API

### Real-world analogy:
EC2 = Renting a computer instead of buying one.

### Key terms:
- **Instance** = One virtual computer
- **Instance Type** = Size/power (t2.micro = small, p3.xlarge = powerful with GPU)
- **AMI** = Pre-configured operating system image

---

## Lambda

### What is it?
Lambda = Run code without managing servers.

### What does it do?
You upload your code. Lambda runs it when triggered. You don't worry about servers.

### How it works:
1. Upload your function code
2. Set a trigger (API call, file upload, schedule)
3. When triggered, Lambda runs your code
4. You pay only for execution time

### Why you need it for ML:
- Simple API endpoints
- Process files when uploaded
- Lightweight inference

### Real-world analogy:
- EC2 = Renting an entire restaurant kitchen (always paying, even when empty)
- Lambda = Food truck that only operates when customers come (pay per order)

### Key terms:
- **Function** = Your code
- **Trigger** = What starts the function
- **Cold start** = First run is slower (loading code)

### Limitations:
- Max 15 minutes runtime
- Limited memory (10GB max)
- Not great for heavy ML models

---

## ECR (Elastic Container Registry)

### What is it?
ECR = Storage for Docker images.

### What does it do?
Stores your Docker images so AWS services can use them.

### How it works:
1. Build Docker image on your computer
2. Push image to ECR
3. Other AWS services pull the image and run it

### Real-world analogy:
ECR = A warehouse that stores your shipping containers (Docker images).

### Why you need it:
Before deploying to ECS or SageMaker, your Docker image must be in ECR.

---

## ECS (Elastic Container Service)

### What is it?
ECS = Runs your Docker containers.

### What does it do?
Takes your Docker image, runs it, manages it, scales it.

### How it works:
1. Create a "cluster" (group of servers)
2. Define "task" (what container to run, how much CPU/RAM)
3. Create "service" (how many copies to run)
4. ECS handles the rest

### Two modes:
- **EC2 mode** = You manage the servers
- **Fargate mode** = AWS manages servers (serverless, easier)

### Real-world analogy:
ECS = A manager that runs your restaurants (containers) across multiple locations, hires staff when busy, closes when slow.

### Why you need it for ML:
- Run your model API in containers
- Auto-scale based on traffic
- High availability

---

## SageMaker

### What is it?
SageMaker = AWS's complete ML platform.

### What does it do?
Everything for ML:
- Notebooks for experimentation
- Training at scale
- Deploying models
- Monitoring models

### How deployment works:
1. **Upload model** to S3 (model.tar.gz file)
2. **Create Model** - Tell SageMaker where the model is
3. **Create Endpoint Config** - Choose instance type, how many
4. **Create Endpoint** - The actual running API

### Deployment options:

| Type | What it is | When to use |
|------|------------|-------------|
| **Real-time Endpoint** | Always running, instant response | User-facing apps |
| **Serverless Inference** | Starts when needed | Sporadic traffic |
| **Batch Transform** | Process large files | Offline bulk scoring |

### Real-world analogy:
SageMaker = A full-service ML restaurant. They provide the kitchen (training), dining room (deployment), and waiters (API). You just bring the recipe (model).

### Why use SageMaker over ECS?
- Built-in model monitoring
- Easy A/B testing
- Auto-scaling specifically for ML
- Less setup required

---

## Bedrock

### What is it?
Bedrock = AWS's service for using pre-trained large language models (LLMs).

### What does it do?
Gives you access to powerful AI models without training them yourself:
- Claude (by Anthropic) - Great for reasoning
- Llama (by Meta) - Open source
- Titan (by Amazon) - Amazon's own models

### How it works:
1. Enable the model you want in AWS console
2. Call the API with your prompt
3. Get response

### Use cases:
- Chatbots
- Text summarization
- Question answering
- Code generation

### Real-world analogy:
Bedrock = Instead of building a car (training a model), you rent a car (use their model).

### Why use Bedrock:
- No training needed
- No infrastructure to manage
- Pay per use (per token)
- Multiple models to choose from

---

## OpenSearch (for Vector Database)

### What is it?
OpenSearch = A search and analytics engine. Can store vectors for AI.

### What does it do for AI?
Stores "embeddings" (vector representations of text) and finds similar items.

### How it works for RAG:
1. Convert your documents to vectors (embeddings)
2. Store vectors in OpenSearch
3. When user asks a question, convert question to vector
4. Find similar document vectors
5. Return matching documents

### Real-world analogy:
- Regular database = Filing cabinet organized alphabetically
- Vector database = Filing cabinet organized by meaning/similarity

### Why you need it:
Essential for RAG (Retrieval Augmented Generation) systems.

---

## API Gateway

### What is it?
API Gateway = The front door to your APIs.

### What does it do?
- Receives requests from internet
- Routes to your backend (Lambda, ECS, etc.)
- Handles authentication
- Rate limiting
- Caching

### How it works:
1. Create an API in API Gateway
2. Define routes (/predict, /health, etc.)
3. Connect each route to a backend
4. Deploy the API
5. Get a public URL

### Real-world analogy:
API Gateway = Reception desk at a company. Checks who you are, directs you to the right department.

### Why you need it:
- Single entry point for all your APIs
- Security (authentication, rate limiting)
- Monitoring

---

## CloudWatch

### What is it?
CloudWatch = Monitoring and logging service.

### What does it do?
- Collects logs from all your services
- Tracks metrics (CPU, memory, requests)
- Sets up alerts

### How it works:
1. Services automatically send logs to CloudWatch
2. You create dashboards to visualize metrics
3. You set alarms (alert me if error rate > 5%)

### Real-world analogy:
CloudWatch = Security cameras + dashboard for your entire system.

### Why you need it:
- See what's happening in your system
- Debug errors
- Get alerted to problems

---

## Secrets Manager

### What is it?
Secrets Manager = Secure storage for passwords and API keys.

### What does it do?
Stores sensitive information securely. Your code retrieves secrets at runtime.

### Why you need it:
NEVER put passwords in code! Use Secrets Manager instead.

### How it works:
1. Store secret in Secrets Manager
2. Your code calls Secrets Manager API
3. Gets the secret value
4. Uses it

---

# PART 3: GCP SERVICES EXPLAINED

---

## GCP Overview

GCP is Google's cloud. Similar to AWS but with different names and some unique strengths.

**GCP Strengths:**
- Better for data/analytics (BigQuery)
- Simpler pricing
- Good Kubernetes support (GKE)
- Gemini AI models

---

## Cloud Storage

### What is it?
Same as AWS S3 = File storage in the cloud.

### GCP term: "Bucket"

### Why use it:
Store model files, training data, any files.

---

## Compute Engine

### What is it?
Same as AWS EC2 = Virtual machines.

### When to use:
When you need full control over a server.

---

## Cloud Functions

### What is it?
Same as AWS Lambda = Serverless functions.

### How it works:
Upload code → Set trigger → Runs automatically when triggered.

### Use for:
- Simple API endpoints
- Event-driven processing

---

## Cloud Run

### What is it?
Run Docker containers without managing servers.

### How it works:
1. Build Docker image
2. Push to Artifact Registry (like ECR)
3. Deploy to Cloud Run
4. Get a URL

### Why it's great:
- **Scales to zero** = No cost when no traffic
- Very simple to use
- Automatic HTTPS

### Real-world analogy:
Cloud Run = A food truck that appears when customers come, disappears when they leave. You only pay when serving.

### Why use for ML:
- Easy deployment
- Auto-scaling
- Cost-effective for variable traffic

---

## Vertex AI

### What is it?
GCP's complete ML platform (like SageMaker).

### What does it do?
- Training
- Deployment
- Model management
- AutoML

### Deployment process:
1. Upload model to Cloud Storage
2. Register in Model Registry
3. Create Endpoint
4. Deploy model to endpoint

### Special features:
- **Traffic splitting** = Send 90% to model A, 10% to model B (for testing)
- **Batch prediction** = Process large files
- **Online prediction** = Real-time API

---

## Vertex AI (Gemini)

### What is it?
Google's large language model (like ChatGPT).

### Available through:
Vertex AI

### Models:
- Gemini Pro - Good balance of speed and quality
- Gemini Ultra - Most powerful

### Use for:
- Chatbots
- Text generation
- Analysis

---

## Vertex AI Vector Search

### What is it?
Vector database for AI (like OpenSearch on AWS).

### What does it do:
Stores embeddings, finds similar items fast.

### Use for:
RAG systems, similarity search, recommendations.

---

## Artifact Registry

### What is it?
Same as AWS ECR = Stores Docker images.

### How it works:
Build image → Push to Artifact Registry → Deploy from there.

---

## Pub/Sub

### What is it?
Messaging service for communication between services.

### How it works:
- **Publisher** sends message to a "topic"
- **Subscribers** listen to the topic and receive messages

### Use for:
- Async processing
- Decoupling services
- Event-driven architecture

### Real-world analogy:
Pub/Sub = A bulletin board. Someone posts a notice, everyone subscribed sees it.

---

## Cloud Monitoring

### What is it?
Same as AWS CloudWatch = Monitoring and logging.

### What it does:
- Collects logs
- Tracks metrics
- Alerts on issues

---

## Secret Manager

### What is it?
Same as AWS Secrets Manager = Store passwords securely.

---

# PART 4: HOW TO DEPLOY (Step by Step)

---

## Deploying ML Model - The Big Picture

```
1. TRAIN MODEL (on your laptop or cloud)
        ↓
2. SAVE MODEL (to a file)
        ↓
3. CREATE API (wrap model in web service)
        ↓
4. CONTAINERIZE (put everything in Docker)
        ↓
5. PUSH TO CLOUD (upload Docker image)
        ↓
6. DEPLOY (run the container)
        ↓
7. EXPOSE (make it accessible via URL)
        ↓
8. MONITOR (watch for errors)
```

---

## Option 1: Deploy with SageMaker (AWS)

### Step-by-step:

**Step 1: Save your model**
- Save model to a file (model.pkl or model.joblib)
- Create inference code (tells SageMaker how to use the model)
- Package as model.tar.gz

**Step 2: Upload to S3**
- Create S3 bucket
- Upload model.tar.gz

**Step 3: Create SageMaker Model**
- Point to S3 location
- Specify container (pre-built or custom)

**Step 4: Create Endpoint Configuration**
- Choose instance type (ml.t2.medium for testing, ml.c5.xlarge for production)
- Set number of instances

**Step 5: Create Endpoint**
- SageMaker deploys your model
- You get an endpoint URL

**Step 6: Test**
- Send request to endpoint
- Get prediction back

### When to use SageMaker:
- Standard ML models (sklearn, PyTorch, TensorFlow)
- Want managed infrastructure
- Need built-in monitoring

---

## Option 2: Deploy with Cloud Run (GCP)

### Step-by-step:

**Step 1: Create your application**
- Load model
- Create API endpoints (using FastAPI or Flask)
- Test locally

**Step 2: Create Dockerfile**
- Define base image
- Copy code and model
- Set startup command

**Step 3: Build Docker image**
- Build locally
- Test locally

**Step 4: Push to Artifact Registry**
- Create repository
- Push image

**Step 5: Deploy to Cloud Run**
- Select image
- Set memory and CPU
- Set min/max instances
- Deploy

**Step 6: Get URL**
- Cloud Run gives you a URL
- Anyone can call your API

### When to use Cloud Run:
- Custom applications
- Variable traffic (scales to zero)
- Simple deployment process

---

## Option 3: Deploy with ECS (AWS)

Similar to Cloud Run but on AWS:
1. Build Docker image
2. Push to ECR
3. Create ECS cluster
4. Define task (container settings)
5. Create service
6. Set up load balancer
7. Deploy

### When to use ECS:
- Need more control than SageMaker
- Complex applications
- Already using AWS infrastructure

---

# PART 5: RAG DEPLOYMENT EXPLAINED

---

## What is RAG?

**RAG = Retrieval Augmented Generation**

### The Problem:
LLMs (like ChatGPT, Claude) know general things but don't know YOUR data:
- Your company's policies
- Your product documentation
- Your private information

### The Solution:
Before asking the LLM, FIND relevant information from your documents and GIVE it to the LLM as context.

### How it works:

```
User: "What is our vacation policy?"
        ↓
1. SEARCH your documents for "vacation policy"
        ↓
2. FIND relevant paragraphs:
   "Employees get 20 days vacation per year..."
        ↓
3. SEND to LLM with context:
   "Based on this document: [vacation policy text]
    Answer: What is our vacation policy?"
        ↓
4. LLM RESPONDS:
   "According to your policy, employees get 20 days..."
```

---

## RAG Architecture Explained

### Part 1: Indexing (One-time setup)

```
Your Documents (PDFs, Word, etc.)
        ↓
CHUNK: Split into small pieces (500 words each)
        ↓
EMBED: Convert each chunk to numbers (vector)
        ↓
STORE: Save vectors in vector database
```

### Part 2: Querying (Every user question)

```
User Question: "What is vacation policy?"
        ↓
EMBED: Convert question to vector
        ↓
SEARCH: Find similar vectors in database
        ↓
RETRIEVE: Get the matching document chunks
        ↓
AUGMENT: Add chunks to LLM prompt
        ↓
GENERATE: LLM creates answer
        ↓
RESPOND: Return answer to user
```

---

## What is an Embedding?

**Simple Explanation:**
Embedding = Converting text to numbers that capture meaning.

**Example:**
- "King" → [0.2, 0.8, 0.1, 0.5, ...]
- "Queen" → [0.2, 0.7, 0.1, 0.6, ...]  (similar numbers!)
- "Car" → [0.9, 0.1, 0.8, 0.2, ...]  (very different numbers)

**Why it matters:**
Similar meanings = Similar numbers = Easy to find related documents.

---

## What is a Vector Database?

**Simple Explanation:**
A database optimized for finding similar vectors.

**Regular database:** "Find all users named John"
**Vector database:** "Find all documents similar to this question"

**AWS Option:** OpenSearch Serverless
**GCP Option:** Vertex AI Vector Search

---

## RAG on AWS - Services Used

| Step | Service | What it does |
|------|---------|--------------|
| Store documents | S3 | Holds original files |
| Process documents | Lambda | Chunks text |
| Create embeddings | Bedrock (Titan) | Converts text to vectors |
| Store vectors | OpenSearch | Vector database |
| Answer questions | Bedrock (Claude) | Generates responses |
| API | API Gateway + Lambda | User interface |

---

## RAG on GCP - Services Used

| Step | Service | What it does |
|------|---------|--------------|
| Store documents | Cloud Storage | Holds original files |
| Process documents | Cloud Functions | Chunks text |
| Create embeddings | Vertex AI Embeddings | Converts text to vectors |
| Store vectors | Vector Search | Vector database |
| Answer questions | Vertex AI (Gemini) | Generates responses |
| API | Cloud Run | User interface |

---

# PART 6: AUTO-SCALING EXPLAINED

---

## What is Auto-Scaling?

**Problem:**
- 9 AM: 1000 users → Need 10 servers
- 3 AM: 10 users → Need 1 server
- Paying for 10 servers 24/7 wastes money

**Solution:**
Auto-scaling automatically adjusts servers based on demand.

---

## How Auto-Scaling Works

```
Traffic increases → Metric goes up (CPU, requests)
        ↓
Crosses threshold (e.g., CPU > 70%)
        ↓
Auto-scaler adds more instances
        ↓
Traffic handled smoothly

Traffic decreases → Metric goes down
        ↓
Crosses lower threshold (e.g., CPU < 30%)
        ↓
Auto-scaler removes instances
        ↓
Save money
```

---

## Key Terms

| Term | Meaning |
|------|---------|
| **Min instances** | Minimum servers always running |
| **Max instances** | Maximum servers allowed |
| **Desired instances** | Current target |
| **Scale out** | Add more servers |
| **Scale in** | Remove servers |
| **Cooldown** | Wait time between scaling actions |

---

## Typical Settings for ML

| Setting | Value | Why |
|---------|-------|-----|
| Min instances | 2 | High availability (if one fails) |
| Max instances | 20 | Cost control |
| Scale out threshold | CPU > 70% | Don't overload servers |
| Scale in threshold | CPU < 30% | Save money when quiet |
| Scale out cooldown | 60 seconds | React quickly |
| Scale in cooldown | 300 seconds | Don't remove too fast |

---

# PART 7: BEST PRACTICES SIMPLIFIED

---

## Security (How to Keep Things Safe)

### 1. Never Put Secrets in Code
**Bad:** Password written in your code
**Good:** Store in Secrets Manager, fetch at runtime

### 2. Use IAM Roles
**What:** Give each service only permissions it needs
**Example:** Your API should only call the model endpoint, nothing else

### 3. Use HTTPS
**What:** Encrypt data in transit
**How:** Cloud services provide this automatically

### 4. Validate Input
**What:** Check user input before processing
**Why:** Prevent attacks, crashes

---

## Monitoring (How to Watch Your System)

### What to Monitor:

| Metric | Why | Alert When |
|--------|-----|------------|
| **Latency** | User experience | > 500ms |
| **Error rate** | System health | > 1% |
| **CPU usage** | Capacity | > 80% |
| **Memory usage** | Stability | > 80% |
| **Request count** | Traffic | Unusual spikes |

### How to Monitor:
- **AWS:** CloudWatch dashboards and alarms
- **GCP:** Cloud Monitoring dashboards and alerts

---

## Cost Control (How to Save Money)

### 1. Right-size Instances
Don't use powerful instances for simple tasks.

### 2. Use Auto-scaling
Don't run servers when not needed.

### 3. Use Serverless When Possible
- Cloud Run scales to zero
- Lambda charges per request

### 4. Cache Results
Store frequent predictions → Don't recompute.

### 5. Choose Appropriate Model
Smaller/cheaper model for simple queries.

---

# PART 8: INTERVIEW QUESTIONS & ANSWERS

---

## Q1: How would you deploy a machine learning model?

**Answer:**
> "I would:
> 1. **Save** the trained model to a file
> 2. **Create an API** using FastAPI that loads the model and exposes a predict endpoint
> 3. **Containerize** with Docker - includes code, model, dependencies
> 4. **Push** the image to a container registry (ECR or Artifact Registry)
> 5. **Deploy** to SageMaker Endpoint or Cloud Run
> 6. **Configure auto-scaling** based on traffic
> 7. **Set up monitoring** in CloudWatch or Cloud Monitoring"

---

## Q2: What's the difference between SageMaker and Vertex AI?

**Answer:**
> "Both are managed ML platforms. SageMaker is AWS, Vertex AI is GCP.
>
> **Key differences:**
> - SageMaker has more deployment options (serverless, async)
> - Vertex AI has simpler traffic splitting for A/B tests
> - SageMaker connects to Bedrock for LLMs, Vertex AI has Gemini built-in
>
> **I'd choose based on:**
> - Which cloud the company already uses
> - Which LLMs are needed (Claude → AWS, Gemini → GCP)"

---

## Q3: What is RAG and how does it work?

**Answer:**
> "RAG means Retrieval Augmented Generation. It helps LLMs answer questions about your specific documents.
>
> **How it works:**
> 1. **Index phase:** Split documents into chunks, convert to embeddings, store in vector database
> 2. **Query phase:** Convert user question to embedding, find similar document chunks, add them to the prompt, let LLM generate answer
>
> **Why use RAG:**
> - LLM can answer about YOUR data
> - Reduces hallucination
> - No need to fine-tune the model"

---

## Q4: How does auto-scaling work?

**Answer:**
> "Auto-scaling automatically adjusts the number of servers based on demand.
>
> **How:**
> - Monitor a metric (CPU, requests, etc.)
> - When metric exceeds threshold, add servers
> - When metric drops, remove servers
>
> **My typical setup:**
> - Min: 2 instances for availability
> - Max: 20 instances for cost control
> - Scale out at 70% CPU
> - Scale in at 30% CPU"

---

## Q5: Real-time vs Batch inference - when to use each?

**Answer:**
> "**Real-time inference:**
> - Single predictions, immediate response (< 100ms)
> - Use for: chatbots, fraud detection, recommendations
> - Always-on endpoint
>
> **Batch inference:**
> - Process large amounts of data offline
> - Use for: daily reports, bulk predictions
> - Run as scheduled job
>
> **I choose real-time for user-facing features, batch for background processing.**"

---

## Q6: How do you ensure your ML system is secure?

**Answer:**
> "Multiple layers:
> 1. **Secrets:** Store in Secrets Manager, never in code
> 2. **Access:** IAM roles with minimum needed permissions
> 3. **Network:** VPC, security groups, private endpoints
> 4. **Data:** Encryption at rest and in transit
> 5. **Input:** Validate all user input
> 6. **Monitoring:** Track for unusual activity"

---

## Q7: How would you reduce costs for an ML deployment?

**Answer:**
> "Several strategies:
> 1. **Right-size instances** - Don't over-provision
> 2. **Auto-scaling** - Scale down when traffic is low
> 3. **Serverless** - Use Cloud Run/Lambda for variable traffic
> 4. **Caching** - Store frequent predictions in Redis
> 5. **Model selection** - Use smaller models for simple queries
> 6. **Spot instances** - For training (60-90% cheaper)"

---

## Q8: What would you monitor for an ML system?

**Answer:**
> "I monitor:
> - **Latency** - How fast predictions are returned
> - **Error rate** - Percentage of failed requests
> - **Throughput** - Requests per second
> - **Resource usage** - CPU, memory
> - **Model performance** - Track prediction distribution for drift
>
> I set alerts for:
> - Latency > 500ms
> - Error rate > 1%
> - CPU > 80%"

---

# PART 9: QUICK REFERENCE

---

## AWS vs GCP Service Mapping

| Purpose | AWS | GCP |
|---------|-----|-----|
| File storage | S3 | Cloud Storage |
| Virtual machines | EC2 | Compute Engine |
| Serverless functions | Lambda | Cloud Functions |
| Container running | ECS/Fargate | Cloud Run |
| Docker image storage | ECR | Artifact Registry |
| ML platform | SageMaker | Vertex AI |
| LLM service | Bedrock | Vertex AI (Gemini) |
| Vector database | OpenSearch | Vector Search |
| Monitoring | CloudWatch | Cloud Monitoring |
| Secrets | Secrets Manager | Secret Manager |
| API management | API Gateway | Cloud Endpoints |
| Cache | ElastiCache | Memorystore |
| Message queue | SQS | Pub/Sub |

---

## Common Deployment Patterns

### Pattern 1: Simple ML API
```
User → API Gateway → Lambda/Cloud Function → Model → Response
```
**Use for:** Light traffic, simple models

### Pattern 2: Production ML API
```
User → Load Balancer → ECS/Cloud Run (multiple instances) → Model → Response
```
**Use for:** Production traffic, need scaling

### Pattern 3: Managed ML Endpoint
```
User → SageMaker Endpoint / Vertex AI Endpoint → Response
```
**Use for:** Standard ML models, want managed service

### Pattern 4: RAG System
```
User → API → Embed Query → Search Vector DB → Get Docs → LLM → Response
```
**Use for:** Q&A over documents

---

## Cost Estimates (Approximate Monthly)

| Setup | Cost |
|-------|------|
| Small API (Lambda/Cloud Functions) | $20-50 |
| Medium API (ECS/Cloud Run, 2 instances) | $100-200 |
| SageMaker endpoint (ml.t2.medium) | $50-100 |
| Production ML (multiple instances) | $500-2000 |
| RAG system (vector DB + LLM) | $300-1000 |

---

## Interview Preparation Checklist

Before your interview, make sure you can explain:

- [ ] What is cloud deployment and why use it
- [ ] What Docker does and why it's needed
- [ ] Difference between Lambda/Cloud Functions and ECS/Cloud Run
- [ ] What SageMaker/Vertex AI does
- [ ] How RAG works (indexing and querying)
- [ ] What auto-scaling is and how to configure it
- [ ] Basic security practices (secrets, IAM)
- [ ] What to monitor and why
- [ ] Cost optimization strategies
- [ ] When to use real-time vs batch inference

---

**Good luck with your interviews!**

Remember: Focus on explaining WHAT services do and WHY you'd use them, not memorizing code.
