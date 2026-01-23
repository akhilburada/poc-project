# Chapter 7: Project Templates

## Overview

This chapter provides ready-to-use project templates you can build and showcase in interviews. Each project includes:
- Project description and learning goals
- Architecture diagram
- Folder structure
- Core code templates
- Deployment instructions

---

## Project 1: ML Model API Service

### Description
Deploy a machine learning model (sentiment analysis) as a production-ready REST API with monitoring, auto-scaling, and CI/CD.

### Learning Goals
- Containerize ML models with Docker
- Deploy to AWS ECS or GCP Cloud Run
- Implement monitoring and logging
- Set up CI/CD pipeline

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ML API SERVICE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   User ──► API Gateway ──► Load Balancer ──► ECS/Cloud Run     │
│                                                   │             │
│                                          ┌────────┴────────┐    │
│                                          │                 │    │
│                                     Container 1      Container N│
│                                     (FastAPI +       (Auto-    │
│                                      Model)          scaled)   │
│                                          │                      │
│                                          ▼                      │
│                                   CloudWatch/Cloud Monitoring   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
ml-api-service/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── model.py               # Model loading and inference
│   ├── schemas.py             # Pydantic models
│   └── config.py              # Configuration
├── model/
│   └── sentiment_model.joblib # Trained model
├── tests/
│   ├── __init__.py
│   ├── test_app.py            # API tests
│   └── test_model.py          # Model tests
├── scripts/
│   ├── train_model.py         # Training script
│   └── validate_model.py      # Validation script
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Core Code

**src/app.py**
```python
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import logging

from src.model import SentimentModel
from src.schemas import PredictionRequest, PredictionResponse
from src.config import settings

# Initialize
app = FastAPI(title="Sentiment Analysis API", version="1.0.0")
model = SentimentModel(settings.MODEL_PATH)

# Metrics
REQUEST_COUNT = Counter('predictions_total', 'Total predictions', ['status'])
REQUEST_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model.is_loaded()}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    start_time = time.time()
    
    try:
        result = model.predict(request.text)
        
        latency = time.time() - start_time
        REQUEST_COUNT.labels(status='success').inc()
        REQUEST_LATENCY.observe(latency)
        
        logger.info(f"Prediction: {result['sentiment']}, latency: {latency:.3f}s")
        
        return PredictionResponse(
            text=request.text,
            sentiment=result['sentiment'],
            confidence=result['confidence'],
            latency_ms=round(latency * 1000, 2)
        )
    except Exception as e:
        REQUEST_COUNT.labels(status='error').inc()
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**src/model.py**
```python
import joblib
import numpy as np
from typing import Dict

class SentimentModel:
    def __init__(self, model_path: str):
        self.model = None
        self.vectorizer = None
        self._load_model(model_path)
    
    def _load_model(self, model_path: str):
        data = joblib.load(model_path)
        self.model = data['model']
        self.vectorizer = data['vectorizer']
    
    def is_loaded(self) -> bool:
        return self.model is not None
    
    def predict(self, text: str) -> Dict:
        # Vectorize input
        features = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = float(np.max(probabilities))
        
        sentiment_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
        
        return {
            'sentiment': sentiment_map.get(prediction, 'unknown'),
            'confidence': confidence
        }
```

**src/schemas.py**
```python
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This product is amazing! I love it."
            }
        }

class PredictionResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float
    latency_ms: float
```

**Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY model/ ./model/

ENV MODEL_PATH=/app/model/sentiment_model.joblib

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deploy to Cloud Run:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/sentiment-api

# Deploy
gcloud run deploy sentiment-api \
    --image gcr.io/PROJECT_ID/sentiment-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --min-instances 1
```

---

## Project 2: RAG Document Q&A System

### Description
Build a RAG system that answers questions about uploaded documents (PDF, TXT) using vector search and LLM generation.

### Learning Goals
- Implement document ingestion pipeline
- Use vector databases for semantic search
- Integrate with LLM APIs (Bedrock/Vertex AI)
- Deploy as scalable service

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     RAG DOCUMENT Q&A ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                    INGESTION PIPELINE                            │  │
│   │                                                                  │  │
│   │   Upload ──► S3/GCS ──► Lambda/CF ──► Chunk ──► Embed ──► VectorDB│
│   │   (PDF)                 (Trigger)                                │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                      QUERY PIPELINE                              │  │
│   │                                                                  │  │
│   │   Query ──► Embed ──► Search ──► Rerank ──► LLM ──► Response    │  │
│   │                        VectorDB    Top-K    Generate             │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
rag-document-qa/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py          # Document loaders
│   │   ├── chunker.py         # Text chunking
│   │   └── embedder.py        # Embedding generation
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── vector_store.py    # Vector DB operations
│   │   └── reranker.py        # Result reranking
│   ├── generation/
│   │   ├── __init__.py
│   │   └── llm.py             # LLM integration
│   └── config.py
├── tests/
│   └── ...
├── lambda/
│   └── ingest_handler.py      # Lambda for ingestion
├── infrastructure/
│   └── terraform/             # IaC files
├── Dockerfile
├── requirements.txt
└── README.md
```

### Core Code

**src/ingestion/chunker.py**
```python
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
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence boundary
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

**src/retrieval/vector_store.py**
```python
from typing import List, Dict
import numpy as np

class VectorStore:
    """Abstract vector store - implement for your DB"""
    
    def __init__(self, embedding_client, db_client):
        self.embedder = embedding_client
        self.db = db_client
    
    def add_documents(self, documents: List[Dict]):
        """Add documents to vector store"""
        texts = [doc['text'] for doc in documents]
        embeddings = self.embedder.embed_batch(texts)
        
        for doc, embedding in zip(documents, embeddings):
            self.db.upsert(
                id=doc['id'],
                vector=embedding,
                metadata={
                    'text': doc['text'],
                    **doc.get('metadata', {})
                }
            )
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.embedder.embed(query)
        
        results = self.db.search(
            vector=query_embedding,
            top_k=k
        )
        
        return [
            {
                'id': r['id'],
                'text': r['metadata']['text'],
                'score': r['score'],
                'metadata': r['metadata']
            }
            for r in results
        ]
```

**src/generation/llm.py**
```python
import boto3
import json
from typing import List, Dict

class LLMClient:
    """AWS Bedrock LLM client"""
    
    def __init__(self, model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = model_id
    
    def generate(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response with RAG context"""
        context = "\n\n".join([
            f"Document {i+1}:\n{doc['text']}"
            for i, doc in enumerate(context_docs)
        ])
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided documents.

<documents>
{context}
</documents>

<question>
{query}
</question>

Instructions:
1. Answer based ONLY on the information in the documents above
2. If the answer is not in the documents, say "I couldn't find this information in the provided documents"
3. Cite which document(s) you used for your answer

Answer:"""
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = self.bedrock.invoke_model(modelId=self.model_id, body=body)
        result = json.loads(response['body'].read())
        
        return result['content'][0]['text']
```

**src/app.py**
```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

from src.ingestion.loader import DocumentLoader
from src.ingestion.chunker import TextChunker
from src.retrieval.vector_store import VectorStore
from src.generation.llm import LLMClient

app = FastAPI(title="RAG Document Q&A")

# Initialize components
loader = DocumentLoader()
chunker = TextChunker(chunk_size=500, overlap=50)
vector_store = VectorStore(...)  # Configure with your DB
llm = LLMClient()

class QueryRequest(BaseModel):
    question: str
    max_docs: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and index a document"""
    try:
        # Load document
        content = await file.read()
        text = loader.load(content, file.filename)
        
        # Chunk
        doc_id = str(uuid.uuid4())
        chunks = chunker.chunk(text, metadata={'doc_id': doc_id, 'filename': file.filename})
        
        # Index
        documents = [
            {'id': f"{doc_id}_{c.chunk_index}", 'text': c.text, 'metadata': c.metadata}
            for c in chunks
        ]
        vector_store.add_documents(documents)
        
        return {"message": f"Indexed {len(chunks)} chunks", "doc_id": doc_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the document knowledge base"""
    try:
        # Retrieve relevant chunks
        relevant_docs = vector_store.search(request.question, k=request.max_docs)
        
        # Generate answer
        answer = llm.generate(request.question, relevant_docs)
        
        return QueryResponse(
            answer=answer,
            sources=[{'text': d['text'][:200], 'score': d['score']} for d in relevant_docs]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Project 3: AI Agent with Tools

### Description
Build an AI agent that can use tools (web search, calculator, database queries) to answer complex questions.

### Learning Goals
- Implement tool-using agent architecture
- Handle multi-step reasoning
- Deploy stateful agent service
- Implement safety guardrails

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      AI AGENT ARCHITECTURE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User ──► API ──► Agent Controller ──┬──► LLM (Reasoning)              │
│                         │             │                                  │
│                         │             ├──► Tool: Web Search             │
│                         │             ├──► Tool: Calculator             │
│                         │             ├──► Tool: Database               │
│                         │             └──► Tool: Weather                │
│                         │                                               │
│                         └──► Memory Store (DynamoDB/Redis)              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
ai-agent/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── controller.py      # Agent orchestration
│   │   ├── tools.py           # Tool definitions
│   │   └── memory.py          # Conversation memory
│   ├── llm/
│   │   ├── __init__.py
│   │   └── client.py          # LLM client
│   └── safety/
│       ├── __init__.py
│       └── guardrails.py      # Safety checks
├── tests/
│   └── ...
├── Dockerfile
├── requirements.txt
└── README.md
```

### Core Code

**src/agent/tools.py**
```python
from typing import Callable, Dict, Any
from dataclasses import dataclass
import httpx
import math

@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict
    function: Callable

def search_web(query: str) -> str:
    """Search the web using a search API"""
    # Replace with actual API
    return f"Search results for: {query}"

def calculate(expression: str) -> str:
    """Safely evaluate mathematical expression"""
    allowed_funcs = {
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'abs': abs,
        'round': round,
    }
    
    try:
        # Very simple safe eval - use a proper parser in production
        for name in allowed_funcs:
            expression = expression.replace(name, f"_funcs['{name}']")
        
        result = eval(expression, {"__builtins__": {}, "_funcs": allowed_funcs})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(location: str) -> str:
    """Get weather for a location"""
    # Replace with actual API
    return f"Weather in {location}: 72°F, Sunny"

# Tool registry
TOOLS = {
    "search_web": Tool(
        name="search_web",
        description="Search the web for information. Use for current events, facts, and general knowledge.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        },
        function=search_web
    ),
    "calculate": Tool(
        name="calculate",
        description="Perform mathematical calculations. Supports basic arithmetic and functions like sqrt, sin, cos.",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"]
        },
        function=calculate
    ),
    "get_weather": Tool(
        name="get_weather",
        description="Get current weather for a location.",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        },
        function=get_weather
    )
}
```

**src/agent/controller.py**
```python
from typing import List, Dict, Optional
import json

from src.agent.tools import TOOLS, Tool
from src.llm.client import LLMClient
from src.agent.memory import ConversationMemory
from src.safety.guardrails import SafetyGuardrails

class AgentController:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.tools = TOOLS
        self.safety = SafetyGuardrails()
        self.max_iterations = 10
    
    def _format_tools(self) -> List[Dict]:
        """Format tools for LLM"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters
            }
            for tool in self.tools.values()
        ]
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool safely"""
        if tool_name not in self.tools:
            return f"Error: Unknown tool {tool_name}"
        
        # Safety check
        if not self.safety.validate_tool_call(tool_name, tool_input):
            return "Error: Tool call blocked by safety guardrails"
        
        try:
            tool = self.tools[tool_name]
            result = tool.function(**tool_input)
            return result
        except Exception as e:
            return f"Error executing tool: {str(e)}"
    
    def run(self, user_message: str, memory: ConversationMemory) -> str:
        """Run agent with user message"""
        
        # Safety check input
        if not self.safety.validate_input(user_message):
            return "I can't process that request."
        
        # Add user message to memory
        memory.add_message("user", user_message)
        
        messages = memory.get_messages()
        tools = self._format_tools()
        
        for iteration in range(self.max_iterations):
            # Call LLM
            response = self.llm.call_with_tools(messages, tools)
            
            # Check if done
            if response['stop_reason'] == 'end_turn':
                assistant_text = self._extract_text(response['content'])
                memory.add_message("assistant", assistant_text)
                return self.safety.sanitize_output(assistant_text)
            
            # Execute tools
            if response['stop_reason'] == 'tool_use':
                messages.append({"role": "assistant", "content": response['content']})
                
                tool_results = []
                for block in response['content']:
                    if block.get('type') == 'tool_use':
                        result = self._execute_tool(
                            block['name'],
                            block['input']
                        )
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block['id'],
                            "content": result
                        })
                
                messages.append({"role": "user", "content": tool_results})
        
        return "I couldn't complete your request within the allowed steps."
    
    def _extract_text(self, content: List) -> str:
        """Extract text from response content"""
        for block in content:
            if block.get('type') == 'text':
                return block.get('text', '')
        return ""
```

**src/app.py**
```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid

from src.agent.controller import AgentController
from src.agent.memory import ConversationMemory
from src.llm.client import LLMClient

app = FastAPI(title="AI Agent API")

# Initialize
llm = LLMClient()
agent = AgentController(llm)
sessions: Dict[str, ConversationMemory] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        sessions[session_id] = ConversationMemory()
    
    memory = sessions[session_id]
    
    # Run agent
    response = agent.run(request.message, memory)
    
    return ChatResponse(
        response=response,
        session_id=session_id
    )

@app.delete("/session/{session_id}")
async def end_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session ended"}
```

---

## Project 4: Multi-Model A/B Testing Platform

### Description
Build a platform to A/B test different ML models in production and automatically select the best performer.

### Learning Goals
- Implement traffic splitting
- Collect and analyze metrics
- Automate model selection
- Handle multiple model versions

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    A/B TESTING PLATFORM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Request ──► Router ──┬──► Model A (Control - 50%)                    │
│                        │                                                │
│                        └──► Model B (Treatment - 50%)                   │
│                                    │                                    │
│                                    ▼                                    │
│                            Metrics Collector                            │
│                                    │                                    │
│                                    ▼                                    │
│                          Statistical Analysis                           │
│                                    │                                    │
│                                    ▼                                    │
│                          Winner Selection                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Components

**Traffic Router:**
```python
import hashlib
import random
from typing import Dict, List

class TrafficRouter:
    def __init__(self, variants: Dict[str, float]):
        """
        Initialize with variants and their traffic percentages.
        Example: {"model_a": 0.5, "model_b": 0.5}
        """
        self.variants = variants
        assert abs(sum(variants.values()) - 1.0) < 0.001, "Weights must sum to 1"
    
    def route(self, user_id: str) -> str:
        """Route user to a variant deterministically"""
        # Use hash for consistent routing
        hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        normalized = (hash_value % 10000) / 10000
        
        cumulative = 0
        for variant, weight in self.variants.items():
            cumulative += weight
            if normalized < cumulative:
                return variant
        
        return list(self.variants.keys())[-1]

class ExperimentManager:
    def __init__(self):
        self.experiments: Dict[str, TrafficRouter] = {}
        self.metrics: Dict[str, List[Dict]] = {}
    
    def create_experiment(self, name: str, variants: Dict[str, float]):
        self.experiments[name] = TrafficRouter(variants)
        self.metrics[name] = []
    
    def record_metric(self, experiment: str, variant: str, metric: str, value: float):
        self.metrics[experiment].append({
            'variant': variant,
            'metric': metric,
            'value': value
        })
    
    def get_results(self, experiment: str) -> Dict:
        """Calculate experiment results"""
        from scipy import stats
        import numpy as np
        
        metrics = self.metrics.get(experiment, [])
        variants = {}
        
        for m in metrics:
            if m['variant'] not in variants:
                variants[m['variant']] = []
            variants[m['variant']].append(m['value'])
        
        results = {}
        for variant, values in variants.items():
            results[variant] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'count': len(values)
            }
        
        # Statistical test if 2 variants
        if len(variants) == 2:
            v1, v2 = list(variants.values())
            stat, p_value = stats.ttest_ind(v1, v2)
            results['p_value'] = p_value
            results['significant'] = p_value < 0.05
        
        return results
```

---

## Deployment Cheat Sheet

### AWS Deployment

```bash
# ECR + ECS deployment
# 1. Create ECR repository
aws ecr create-repository --repository-name my-ml-app

# 2. Build and push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t my-ml-app .
docker tag my-ml-app:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-ml-app:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/my-ml-app:latest

# 3. Create ECS cluster and service (via console or CloudFormation)
```

### GCP Deployment

```bash
# Cloud Run deployment
# 1. Build with Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/my-ml-app

# 2. Deploy to Cloud Run
gcloud run deploy my-ml-app \
    --image gcr.io/PROJECT_ID/my-ml-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --min-instances 1 \
    --max-instances 10
```

---

## Project Ideas for Portfolio

### Beginner
1. **Sentiment API** - Deploy a sentiment classifier
2. **Image Classifier** - Deploy an image classification model
3. **Text Summarizer** - Deploy a summarization model

### Intermediate
4. **RAG Chatbot** - Q&A over documents
5. **Real-time Fraud Detector** - Streaming ML inference
6. **Recommendation API** - Product recommendations

### Advanced
7. **Multi-Agent System** - Agents that collaborate
8. **MLOps Pipeline** - Full CI/CD for ML
9. **Model A/B Testing Platform** - Experiment management
10. **Vector Search Engine** - Semantic search at scale

---

## Summary

Each project in this chapter is designed to:
1. Teach a specific deployment skill
2. Be completable in 1-2 weeks
3. Be impressive in interviews
4. Use real-world architectures

Pick 2-3 projects that align with your target role and build them end-to-end. Be prepared to discuss:
- Architecture decisions
- Trade-offs you made
- How you'd scale it
- What you'd improve

Good luck with your interview preparation!

---

## Complete Step-by-Step Guide

For a detailed walkthrough of deploying your first ML application from scratch, see:

**[End-to-End Deployment Guide](./end-to-end-deployment-guide.md)**

This guide takes you through:
1. Training and saving a sentiment analysis model
2. Creating a FastAPI application
3. Containerizing with Docker
4. Deploying to AWS ECS
5. Deploying to GCP Cloud Run
6. Setting up CI/CD with GitHub Actions
7. Adding monitoring

Every step includes actual commands you can copy and run!
